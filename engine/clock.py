"""The episode's clock: every line, every word and every count event, in seconds, from the picked takes.

    certainty clock <episode>

Lays the picked takes (picks.json) end to end with air between them, trims pauses inside a take to max_pause,
sets each "(beat)" at the take's own silence, and puts the count (if any) after its line: the words open, the
letters are counted on clicks that quicken a little, a breath between words, the numeral, then the next line.
Settings in episode.toml:

    [clock]
    start = 0.3            # the first line starts here
    gap = 0.4              # air after a line
    gaps = { 2 = 1.5 }     # air after given lines
    max_pause = 0.38       # longest pause kept inside a take
    beats = { 3 = [0, 0.6] }   # line: [the word the pause follows (0 = first), the pause it becomes]
    tail = 3.0             # after the last line

    [count]                # optional
    after_line = 17        # 0: no line before it; it starts at `start`
    start = 4.0            # (after_line = 0 only) seconds
    verse = "1:1"          # the verse counted (its letters per word come from the data)
    open = 1.0             # from the count's start to the first click
    click_first = 0.36     # seconds between the first clicks
    click_last = 0.24      # ... and the last ones
    group_breath = 0.12    # extra pause between words
    to_numeral = 0.75      # from the last click to the numeral
    after = 1.1            # from the numeral to the next line

Writes clock.json: lines (start, voice span, words), count (open, word_open, clicks, word_close, numeral), the
audio pieces for the mix, and frames_total.
"""
import json
import wave

import numpy as np

from . import data
from .episode import Episode


def _length(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def silences(p, t0, t1, floor_db=-38):
    """Every stretch of silence between t0 and t1, measured on the audio in 10 ms frames."""
    with wave.open(str(p)) as w:
        sr, ch = w.getframerate(), w.getnchannels()
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(float).reshape(-1, ch).mean(1) / 32768
    hop = sr // 100
    i0, i1 = int(t0 * sr) // hop, int(t1 * sr) // hop
    db = [20 * np.log10(np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) + 1e-9) for i in range(i0, i1)]
    runs, run = [], None
    for i, d in enumerate(db + [0]):
        if d < floor_db and run is None:
            run = i
        elif d >= floor_db and run is not None:
            runs.append(((i0 + run) * hop / sr, (i0 + i) * hop / sr))
            run = None
    return runs


def build(ep):
    picks = json.load(open(ep.path("picks.json"), encoding="utf-8"))["picks"] if ep.path("picks.json").exists() else {}
    c = ep.cfg.get("clock", {})
    gap, gaps = c.get("gap", 0.4), {int(k): v for k, v in c.get("gaps", {}).items()}
    max_pause, beats = c.get("max_pause", 0.38), {int(k): v for k, v in c.get("beats", {}).items()}
    cnt = ep.cfg.get("count")
    lines, pieces, count, t = [], [], None, c.get("start", 0.3)

    def do_count(t):
        per_word = [len(data.letters(w)) for w in data.text(cnt["verse"]).split()]
        c0 = t + 0.35
        tc, clicks, word_open, word_close, k = c0 + cnt.get("open", 1.0), [], [], [], 0
        n = sum(per_word)
        f, l_, br = cnt.get("click_first", 0.36), cnt.get("click_last", 0.24), cnt.get("group_breath", 0.12)
        for m in per_word:
            word_open.append(round(tc - 0.15, 3))
            for j in range(m):
                clicks.append(round(tc, 3))
                k += 1
                if k < n:
                    tc += f + (l_ - f) * (k - 1) / max(1, n - 2) + (br if j == m - 1 else 0)
            word_close.append(round(clicks[-1] + 0.15, 3))
        numeral = round(clicks[-1] + cnt.get("to_numeral", 0.75), 3)
        return dict(verse=cnt["verse"], open=round(c0, 3), word_open=word_open, clicks=clicks, word_close=word_close,
                    numeral=numeral), numeral + cnt.get("after", 1.1)

    if cnt and cnt.get("after_line", 0) == 0:            # a count with no line before it starts at [count] start
        count, t = do_count(max(t, cnt.get("start", t)))
    for key in sorted(picks, key=lambda k: int(k[1:])):
        n, p = int(key[1:]), picks[key]
        take = ep.path(p["file"])
        v, toks = p["voiced"], p["tokens"]
        a, b = max(0.0, v[0] - 0.1), min(v[1] + 0.1, _length(take))
        runs = [(s0, s1, max_pause) for s0, s1 in silences(take, v[0] + 0.05, v[1] - 0.05) if s1 - s0 > max_pause]
        if n in beats:
            k, want = beats[n]
            found = [r for r in silences(take, toks[k]["start"], toks[k + 1]["start"] + 0.12) if r[1] - r[0] >= 0.12]
            if found:
                s0, s1 = max(found, key=lambda r: r[1])
                runs = [r for r in runs if r[1] <= s0 or r[0] >= s1] + [(s0, s1, want)]
        parts, cur = [], a
        for s0, s1, want in sorted(runs):
            mid, have = (s0 + s1) / 2, s1 - s0
            if want < have:
                parts.append((cur, mid - want / 2, 0.0))
                cur = mid + want / 2
            else:
                parts.append((cur, mid, want - have))
                cur = mid
        parts.append((cur, b, 0.0))
        start, shift = t, []
        for s0, s1, extra in parts:
            pieces.append(dict(kind="voice", line=key, file=p["file"], src=[round(s0, 3), round(s1, 3)], at=round(t, 3)))
            shift.append((s0, t - s0))
            t += s1 - s0 + extra

        def clock(x):
            off = [o for s, o in shift if x >= s - 1e-6]
            return round(x + (off[-1] if off else shift[0][1]), 3)

        words = [dict(w=w["w"], start=clock(w["start"]), end=clock(w["end"])) for w in toks]
        for w0, w1 in zip(words, words[1:]):
            w0["end"] = min(w0["end"], w1["start"])
        lines.append(dict(id=key, text=" ".join(w["w"] for w in toks), start=round(start, 3),
                          voice=[clock(v[0]), clock(v[1])], words=words))
        if cnt and cnt.get("after_line") == n:
            count, t = do_count(t)
        else:
            t += gaps.get(n, gap)
    end = t + c.get("tail", 3.0)
    frames = int(round(end * ep.fps))
    return dict(episode=ep.cfg.get("id", ep.dir.name), fps=ep.fps, frames_total=frames, end_s=round(frames / ep.fps, 3),
                lines=lines, count=count, pieces=pieces)


def main(argv):
    if not argv:
        raise SystemExit("usage: certainty clock <episode>")
    ep = Episode(argv[0])
    out = build(ep)
    json.dump(out, open(ep.path("clock.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"clock.json: {out['frames_total']} frames, {out['end_s']:.2f} s, {len(out['lines'])} lines"
          + (f", the count {out['count']['open']:.2f} to {out['count']['numeral']:.2f} s" if out["count"] else ""))
    for l in out["lines"]:
        print(f"  {l['id']} {int(l['start'] // 60)}:{l['start'] % 60:05.2f}  {l['text']}")
    return 0
