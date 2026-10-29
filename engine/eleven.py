"""ElevenLabs: voice takes for an episode's lines, and music cues from composition plans. Both spend credits.

    certainty voice <episode> [--lines 1,2,5] [--takes 2]          shows what it would send and its size
    certainty voice <episode> ... --yes                             sends it
    certainty music <episode>/music/M1.json [--take 1]             shows the plan
    certainty music <episode>/music/M1.json --take 1 --yes         composes it

Nothing is sent without --yes. Keys come from .env (ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID) and are never printed.
Every request is logged to the episode's takes/log.jsonl or music/log.jsonl. A take that exists is never
overwritten: pick another --take number.

Voice settings come from episode.toml [voice]: model, settings (stability, similarity_boost, style,
use_speaker_boost), takes. Takes are 48 kHz 16-bit mono WAV, named <episode id>-L<nn>_take<k>.wav.
A composition plan is ElevenLabs Music's: model_id, output_format and composition_plan.chunks (text, duration_ms,
positive_styles, negative_styles).
"""
import argparse
import json
import pathlib
import ssl
import subprocess
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

from .episode import Episode, spoken
from .settings import env

API = "https://api.elevenlabs.io/v1"
try:
    import certifi
    _SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    _SSL = ssl.create_default_context()


def _call(path, payload, query=""):
    key = env("ELEVENLABS_API_KEY")
    if not key:
        raise SystemExit("ELEVENLABS_API_KEY is not set in .env")
    req = urllib.request.Request(f"{API}/{path}{query}", data=json.dumps(payload).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=300, context=_SSL) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"ElevenLabs {path}: HTTP {exc.code}: {exc.read().decode('utf-8', 'replace')[:400]}")


def _log(path, row):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **row}, ensure_ascii=False) + "\n")


def voice(argv):
    ap = argparse.ArgumentParser(prog="certainty voice")
    ap.add_argument("episode")
    ap.add_argument("--lines", help="comma-separated line numbers (default: every line)")
    ap.add_argument("--takes", type=int)
    ap.add_argument("--yes", action="store_true", help="send the requests (spends credits)")
    a = ap.parse_args(argv)
    ep = Episode(a.episode)
    vcfg = ep.cfg.get("voice", {})
    model = vcfg.get("model", "eleven_multilingual_v2")
    settings = vcfg.get("settings", {"stability": 0.55, "similarity_boost": 0.8, "style": 0.1, "use_speaker_boost": True})
    takes = a.takes or vcfg.get("takes", 2)
    lines = ep.lines()
    want = [int(x) for x in a.lines.split(",")] if a.lines else list(lines)
    out = ep.path("takes")
    plan, chars = [], 0
    for n in want:
        text = spoken(lines[n])
        for k in range(1, takes + 1):
            dest = out / f"{ep.cue(n)}_take{k}.wav"
            if dest.exists():
                continue
            plan.append((n, k, text, dest))
            chars += len(text)
    for n, k, text, dest in plan:
        print(f"  L{n} take {k}: {text}")
    print(f"{len(plan)} requests, {chars} characters of text to speech, model {model}")
    if not a.yes:
        print("Dry run: nothing was sent. Add --yes to spend the credits.")
        return 0
    vid = env("ELEVENLABS_VOICE_ID")
    if not vid:
        raise SystemExit("ELEVENLABS_VOICE_ID is not set in .env")
    out.mkdir(parents=True, exist_ok=True)
    for n, k, text, dest in plan:
        raw = _call(f"text-to-speech/{vid}", {"text": text, "model_id": model, "voice_settings": settings},
                    "?output_format=pcm_48000")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", "48000", "-ac", "1", "-i", "pipe:0",
                        "-c:a", "pcm_s16le", str(dest)], input=raw, check=True)
        _log(out / "log.jsonl", dict(line=n, take=k, model=model, settings=settings, text=text, file=dest.name))
        print(f"  wrote {dest.name}")
        time.sleep(0.5)
    return 0


def music(argv):
    ap = argparse.ArgumentParser(prog="certainty music")
    ap.add_argument("plan")
    ap.add_argument("--take", type=int, default=1)
    ap.add_argument("--yes", action="store_true", help="send the request (spends credits)")
    a = ap.parse_args(argv)
    plan_path = pathlib.Path(a.plan).resolve()
    plan = json.load(open(plan_path, encoding="utf-8"))
    chunks = plan["composition_plan"]["chunks"]
    total = sum(c["duration_ms"] for c in chunks) / 1000
    assert 3 <= total <= 600 and all(3000 <= c["duration_ms"] <= 120000 for c in chunks), "chunks of 3 to 120 s"
    print(f"{plan_path.stem}: {len(chunks)} chunks, {total:.1f} s, model {plan['model_id']}")
    for c in chunks:
        print(f"  {c['duration_ms'] / 1000:5.1f} s  {c['text'].splitlines()[0]}")
    mp3 = plan_path.with_name(f"{plan_path.stem}_take{a.take}.mp3")
    if mp3.exists():
        raise SystemExit(f"{mp3.name} exists; pick another --take")
    if not a.yes:
        print("Dry run: one music generation would be requested. Nothing was sent. Add --yes to spend it.")
        return 0
    raw = _call("music", {"composition_plan": plan["composition_plan"], "model_id": plan["model_id"]},
                f"?output_format={plan.get('output_format', 'mp3_48000_320')}")
    mp3.write_bytes(raw)
    wav = mp3.with_suffix(".wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-ar", "48000", "-c:a", "pcm_s16le", str(wav)], check=True)
    _log(plan_path.parent / "log.jsonl", dict(plan=plan_path.name, take=a.take, file=mp3.name))
    print(f"wrote {mp3.name} and {wav.name}")
    return 0
