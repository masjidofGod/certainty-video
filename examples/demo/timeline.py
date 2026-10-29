"""The demo's timeline: the Basmalah written by the pen, counted letter by letter on the clock's clicks, and the
count's number landing in gold. A small, complete example of a timeline: every time comes from clock.json, every
number from claims.toml, every Arabic shape from art/basmala.json (made from your data by `certainty demo`).
"""
import json
import pathlib

from engine import data, verify
from engine.canvas import INK, LABEL, CamPath, Frame, background, corners, ew, label, leader, ramp, rect_path
from engine.scenes import Captions, VerseCount, draw_pen, numeral

HERE = pathlib.Path(__file__).resolve().parent
CL = json.load(open(HERE / "clock.json", encoding="utf-8"))
FPS, NFR, CNT = CL["fps"], CL["frames_total"], CL["count"]
N = verify.measured(HERE / "claims.toml", "basmalah-letters")        # 19, or the timeline stops

V = VerseCount(HERE / "art" / "basmala.json", rows=[[0, 1], [2, 3]])
assert V.n == N == len(CNT["clicks"]), (V.n, N, len(CNT["clicks"]))
WRITE = (0.5, 3.05)
OPEN = CNT["open"]
CAPS = Captions(CL)
ENGLISH = data.english("1:1")
CAMERA = CamPath([(-1.0, 540, 960, 1.05), (WRITE[1], 540, 960, 1.0), (CL["end_s"] + 1, 540, 960, 1.0)])
RESULT = (468, 1250, 612, 1330)
_bg = None


def frame(i):
    global _bg
    if _bg is None:
        _bg = background()
    t = i / FPS
    fr = Frame(CAMERA.at(t), _bg)
    fr.pen = None
    V.draw(fr, t, WRITE, OPEN, CNT["clicks"], CNT["numeral"])
    V.row_lines(fr, t, CNT["word_open"], CNT["word_close"])
    rest = 1 - ew(t, OPEN - 0.1, OPEN + 0.3)
    if rest > 0:
        corners(fr, V.box, ew(t, WRITE[1], WRITE[1] + 0.5), alpha=0.55 * rest)
        label(fr, (V.box[0], V.box[1] - 30), "1:1", ramp(t, WRITE[1], WRITE[1] + 0.3), px=17, alpha=0.8 * rest)
        if ENGLISH:
            fr.text((540, V.box[3] + 30), ENGLISH, "SourceSerif4-Italic[opsz,wght].ttf", 30, INK,
                    0.9 * ew(t, WRITE[1] + 0.2, WRITE[1] + 0.7) * rest, anchor="ma")
        label(fr, (540, 330), "HOW MANY LETTERS?", ramp(t, WRITE[1] + 0.4, WRITE[1] + 1.0), px=17, alpha=0.85 * rest,
              anchor="ma")
    if t >= OPEN:                                     # the result box, empty through the count
        leader(fr, rect_path(*RESULT, radius=8), ew(t, OPEN, OPEN + 0.5), LABEL, 0.6, 1.3)
        label(fr, (RESULT[0], RESULT[1] - 26), "RESULT", ramp(t, OPEN + 0.15, OPEN + 0.45), alpha=0.75)
        numeral(fr, t, str(N), ((RESULT[0] + RESULT[2]) / 2, (RESULT[1] + RESULT[3]) / 2), 56, CNT["numeral"])
        label(fr, (540, RESULT[3] + 18), "THE LETTERS OF 1:1, COUNTED FROM THE TEXT", ramp(t, CNT["numeral"] + 0.5,
              CNT["numeral"] + 1.2), alpha=0.85, anchor="ma")
    draw_pen(fr)
    CAPS.draw(fr, t)
    return fr.render()
