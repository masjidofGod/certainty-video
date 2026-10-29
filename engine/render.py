"""Render an episode's timeline: still frames for review, a 480p draft, or the finished film.

    certainty stills <episode> 3.5 12 40.2          full-size PNGs at those seconds, in <episode>/out/stills/
    certainty film <episode> [--draft] [--jobs 8]    <episode>/out/film.mp4 (or film-draft.mp4), with mix.wav

The timeline is the episode's timeline.py: it must define frame(i), returning a 1920 x 1080 x 3 uint8 array for
frame i, and read its times from clock.json. Frames are rendered in parallel and piped in order into ffmpeg
(no intermediate files), with the upload preset of engine/deliver.py: 1080 x 1920, 24 fps, H.264 High, CRF 16,
Rec.709 tags, AAC 256 kb/s. A draft is 540 x 960 at CRF 23 (review only, never scaled up for delivery).
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from multiprocessing import Pool

from PIL import Image

from .episode import Episode
from . import deliver

_TL = None


def _load(path):
    global _TL
    spec = importlib.util.spec_from_file_location("timeline", path)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(mod)
    _TL = mod
    return mod


def _frame(i):
    return i, _TL.frame(i).tobytes()


def stills(argv):
    ap = argparse.ArgumentParser(prog="certainty stills")
    ap.add_argument("episode")
    ap.add_argument("times", nargs="+", type=float)
    a = ap.parse_args(argv)
    ep = Episode(a.episode)
    tl = _load(str(ep.path("timeline.py")))
    out = ep.path("out", "stills")
    out.mkdir(parents=True, exist_ok=True)
    for s in a.times:
        i = int(round(s * ep.fps))
        p = out / f"t{s:07.2f}.png"
        Image.fromarray(tl.frame(i)).save(p)
        print(p)
    return 0


def film(argv):
    ap = argparse.ArgumentParser(prog="certainty film")
    ap.add_argument("episode")
    ap.add_argument("--draft", action="store_true")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args(argv)
    ep = Episode(a.episode)
    clock = json.load(open(ep.path("clock.json"), encoding="utf-8"))
    n = clock["frames_total"]
    audio = ep.path("mix.wav")
    out = ep.path("out", "film-draft.mp4" if a.draft else "film.mp4")
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = deliver.export_command("draft" if a.draft else "upload", str(out), str(audio) if audio.exists() else None, n,
                                 pipe=True)
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    t0 = time.time()
    with Pool(a.jobs, initializer=_load, initargs=(str(ep.path("timeline.py")),)) as pool:
        for k, (i, buf) in enumerate(pool.imap(_frame, range(n), chunksize=2)):
            enc.stdin.write(buf)
            if k % 240 == 0:
                el = time.time() - t0
                print(f"frame {i} of {n}, {el:.0f} s elapsed, {el / max(1, k) * (n - k):.0f} s left", flush=True)
    enc.stdin.close()
    err = enc.stderr.read().decode(errors="replace")
    if enc.wait():
        raise SystemExit("ffmpeg failed: " + err[-800:])
    print(f"wrote {out}: {n} frames in {time.time() - t0:.0f} s" + ("" if audio.exists() else " (no mix.wav: silent)"))
    return 0
