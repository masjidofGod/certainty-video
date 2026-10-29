"""Check every take word for word against the script and pick one per line.

    certainty whisper <episode> [--model medium.en] [--again]
    certainty takes <episode>

`takes` needs a recognizer's word times for each take, as Whisper writes them (one JSON per take, named like the
take, in the episode's whisper/ folder). `whisper` runs Whisper on every take that has no JSON yet, passing each
file by name, so it works the same in Command Prompt, PowerShell, Git Bash and on macOS and Linux. It finds the
whisper command on your PATH or, failing that, a Python that has Whisper installed (`python -m whisper`).

A take is exact when the recognized words equal the script's: numbers read as words, apostrophes ignored, words
heard joined ("everyone" for "every one") allowed, and the names in episode.toml [takes] names allowed
(names = { basmalah = ["bismillah"] }). Among exact takes the shorter is picked, unless [takes] prefer names a take
for a line (prefer = { 4 = 1 }). Writes picks.json: per line the file, its voiced span and the caption's words
with their times in the file. Exit 1 if a line has no exact take.
"""
import argparse
import difflib
import json
import os
import re
import shutil
import subprocess

from .episode import Episode, caption

INSTALL = ("py -3.12 -m pip install openai-whisper" if os.name == "nt" else
           "python3 -m pip install openai-whisper (or pipx install openai-whisper)")

ONES = ("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
        "seventeen eighteen nineteen").split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _w99(n):
    return ONES[n] if n < 20 else TENS[n // 10] + ("" if n % 10 == 0 else " " + ONES[n % 10])


def number_words(tok):
    m = re.fullmatch(r"(\d+)(s?)", tok)
    if not m:
        return tok
    n, plural = int(m.group(1)), m.group(2)
    if 1900 <= n <= 2099:
        w = ("nineteen " if n < 2000 else "twenty ") + _w99(n % 100)
    elif n < 100:
        w = _w99(n)
    elif n < 1000:
        w = ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _w99(n % 100))
    else:
        w = _w99(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + number_words(str(n % 1000)))
    if plural:
        w = w[:-1] + "ies" if w.endswith("y") else w + "s"
    return w


def norm_words(text):
    out = []
    for tok in text.replace("—", " ").split():
        tok = tok.lower().replace("’", "'").strip(" .,:;?!\"'“”").replace("'", "")
        out += [p for p in number_words(tok).replace("-", " ").split() if p]
    return out


def voiced(path, floor_db=-35):
    """Start and end of the sound in a take, from ffmpeg's silence detection."""
    out = subprocess.run(["ffmpeg", "-v", "info", "-i", str(path), "-af", f"silencedetect=noise={floor_db}dB:d=0.1",
                          "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                str(path)], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip())
    sil, start = [], None
    for line in out.splitlines():
        if "silence_start:" in line:
            start = float(line.split("silence_start:")[1].split()[0])
        elif "silence_end:" in line and start is not None:
            sil.append((start, float(line.split("silence_end:")[1].split("|")[0])))
            start = None
    if start is not None:
        sil.append((start, dur))
    head = sil[0][1] if sil and sil[0][0] <= 0.05 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
    return [round(head, 2), round(tail, 2)]


def align(tokens, heard, span):
    """Each caption token gets the time of the recognized word it matches; the rest are shared out by length."""
    def nt(x):
        return " ".join(norm_words(x))
    sm = difflib.SequenceMatcher(a=[nt(x) for x in tokens], b=[nt(h[0]) for h in heard], autojunk=False)
    times = [None] * len(tokens)
    for blk in sm.get_matching_blocks():
        for i in range(blk.size):
            times[blk.a + i] = heard[blk.b + i][1:]
    i = 0
    while i < len(tokens):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(tokens) and times[j] is None:
            j += 1
        s0 = times[i - 1][1] if i > 0 else span[0]
        s1 = times[j][0] if j < len(tokens) else span[1]
        sizes = [len(x) + 1 for x in tokens[i:j]]
        acc = s0
        for k, n in zip(range(i, j), sizes):
            step = (s1 - s0) * n / sum(sizes)
            times[k] = (acc, acc + step)
            acc += step
        i = j
    out = []
    for i, (tok, (s0, s1)) in enumerate(zip(tokens, times)):
        s0 = max(s0, span[0]) if i == 0 else s0
        out.append(dict(w=tok, start=round(s0, 3), end=round(max(s0 + 0.05, min(s1, span[1])), 3)))
    return out


def whisper_command():
    """Whisper as this computer has it: the whisper command, or a Python with Whisper installed. On Windows its
    Scripts folder is often not on PATH, so the py launcher's Pythons are tried too. None if there is none."""
    w = shutil.which("whisper")
    if w:
        return [w]
    has = "import importlib.util, sys; sys.exit(importlib.util.find_spec('whisper') is None)"
    tries = [["py", f"-{v}"] for v in ("3.13", "3.12", "3.11", "3.10")] if shutil.which("py") else []
    tries += [[p] for p in ("python3", "python") if shutil.which(p)]
    for t in tries:
        if subprocess.run(t + ["-c", has], capture_output=True).returncode == 0:
            return t + ["-m", "whisper"]
    return None


def transcribe(argv):
    ap = argparse.ArgumentParser(prog="certainty whisper")
    ap.add_argument("episode")
    ap.add_argument("--model", default="medium.en")
    ap.add_argument("--again", action="store_true", help="also the takes that already have their JSON")
    a = ap.parse_args(argv)
    ep = Episode(a.episode)
    out = ep.path("whisper")
    wavs = [w for w in sorted(ep.path("takes").glob("*.wav")) if a.again or not (out / f"{w.stem}.json").exists()]
    if not wavs:
        print("Every take has its words already (--again to redo them).")
        return 0
    cmd = whisper_command()
    if not cmd:
        raise SystemExit(f"Whisper is not installed: {INSTALL}")
    print(f"Whisper ({a.model}) on {len(wavs)} takes, into {out}", flush=True)
    for i in range(0, len(wavs), 40):          # 40 files a run keeps the command line short on Windows
        r = subprocess.run(cmd + [str(w) for w in wavs[i:i + 40]] + [
            "--model", a.model, "--language", "en", "--word_timestamps", "True", "--output_format", "json",
            "--output_dir", str(out)])
        if r.returncode:
            raise SystemExit("Whisper stopped with an error (above)")
    lost = [w.name for w in wavs if not (out / f"{w.stem}.json").exists()]
    if lost:
        raise SystemExit(f"Whisper wrote no JSON for: {', '.join(lost)}")
    print(f"{len(wavs)} takes heard; next: certainty takes {a.episode}")
    return 0


def main(argv):
    if not argv:
        raise SystemExit("usage: certainty takes <episode>")
    ep = Episode(argv[0])
    cfg = ep.cfg.get("takes", {})
    names = {k.lower(): {v.lower() for v in vs} for k, vs in cfg.get("names", {}).items()}
    prefer = {int(k): v for k, v in cfg.get("prefer", {}).items()}

    def same(a, b):
        return a == b or b in names.get(a, ())

    picks, missing = {}, []
    for n, text in ep.lines().items():
        tokens = caption(text).split()
        takes = []
        for wav in sorted(ep.path("takes").glob(f"{ep.cue(n)}_take*.wav")):
            k = int(re.search(r"_take(\d+)", wav.name).group(1))
            js = ep.path("whisper", wav.stem + ".json")
            if not js.exists():
                print(f"L{n} take {k}: no recognizer JSON ({js.name}); run Whisper first")
                continue
            rec = json.load(open(js, encoding="utf-8"))
            heard = [(w["word"].strip(), w["start"], w["end"]) for s in rec["segments"] for w in s["words"]]
            a, b = norm_words(text), norm_words(" ".join(h[0] for h in heard))
            ok = (len(a) == len(b) and all(same(x, y) for x, y in zip(a, b))) or "".join(a) == "".join(b)
            span = voiced(wav)
            takes.append(dict(take=k, file=wav.name, ok=ok, heard=heard, voiced=span))
            print(f"L{n} take {k}: {'exact' if ok else 'DIFFERS'} {span[1] - span[0]:.2f} s  {' '.join(b)}")
        good = [t for t in takes if t["ok"]]
        if not good:
            missing.append(n)
            continue
        pick = next((t for t in good if t["take"] == prefer.get(n)), None) or min(good, key=lambda t: t["voiced"][1] - t["voiced"][0])
        picks[f"L{n:02d}"] = dict(take=pick["take"], file="takes/" + pick["file"], voiced=pick["voiced"],
                                  tokens=align(tokens, pick["heard"], pick["voiced"]))
    json.dump(dict(picked_by="the shorter exact take, unless [takes] prefer says otherwise", picks=picks),
              open(ep.path("picks.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"picks.json: {len(picks)} lines; with no exact take: {missing or 'none'}")
    return 1 if missing else 0
