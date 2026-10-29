"""Check a delivered file against the safe areas of Instagram Reels, TikTok and YouTube Shorts.

    certainty safe <file.mp4> [--fps 4] [--profile reels|tiktok|shorts|all]

The platforms' buttons, captions and headers cover parts of a 1080 x 1920 frame. These areas take the conservative
figures of current guides (they disagree; re-check them now and then):

  reels   x 80 to 1000, y 280 to 1560; right edge 940 below y 1150 (the like, comment and share buttons)
  tiktok  x 60 to 960, y 140 to 1440 (its caption block runs deepest); right edge 930 below y 900
  shorts  x 60 to 1000, y 140 to 1540; right edge 900 below y 950
  all     the three together: lay out inside x 80 to 1000 and y 280 to 1440, and x 180 to 900 below y 900

Each sampled frame is compared with the series' background; a pixel counts as drawn when it differs by more than
24 levels. Prints each frame with drawing outside the area, then pass or fail (exit 1).
"""
import argparse
import subprocess

import numpy as np

from .canvas import background

W, H = 1080, 1920


def zone(x0, y0, x1, y1, low_y, low_x1):
    o = np.ones((H, W), bool)
    o[y0:y1, x0:x1] = False
    o[low_y:y1, low_x1:x1] = True
    return o


def main(argv):
    ap = argparse.ArgumentParser(prog="certainty safe")
    ap.add_argument("file")
    ap.add_argument("--fps", type=float, default=4.0)
    ap.add_argument("--profile", default="all", choices=["reels", "tiktok", "shorts", "all"])
    a = ap.parse_args(argv)
    Z = {"reels": zone(80, 280, 1000, 1560, 1150, 940), "tiktok": zone(60, 140, 960, 1440, 900, 930),
         "shorts": zone(60, 140, 1000, 1540, 950, 900)}
    out = (Z["reels"] | Z["tiktok"] | Z["shorts"]) if a.profile == "all" else Z[a.profile]
    bg = background().astype(np.int16)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", a.file, "-vf", f"fps={a.fps}", "-f", "rawvideo", "-pix_fmt",
                          "rgb24", "-"], stdout=subprocess.PIPE)
    n, bad = 0, []
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.int16)
        drawn = (np.abs(f - bg).max(axis=2) > 24) & out
        k = int(drawn.sum())
        if k > 120:
            ys, xs = np.nonzero(drawn)
            bad.append((n / a.fps, k, (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))))
        n += 1
    if n == 0:
        raise SystemExit(f"{a.file}: no frames read")
    for t, k, b in bad:
        print(f"  {int(t // 60)}:{t % 60:05.2f}  {k:6d} px outside, x {b[0]}-{b[2]}, y {b[1]}-{b[3]}")
    print(f"{a.profile}: {n} frames at {a.fps} fps: {'pass' if not bad else f'{len(bad)} frames outside the safe area'}")
    return 1 if bad else 0
