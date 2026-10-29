"""{{EPISODE_ID}}'s timeline: what is on screen at every frame.

Start here and grow it line by line with the script (ask the certainty:studio skill in Claude Code). The demo
(examples/demo/timeline.py) is a complete small example: a verse written by the pen, opened and counted.

The rules the code keeps:
- every time comes from clock.json (a word's start, a click, the numeral), never typed;
- every number comes from claims.toml through verify.measured(), never typed;
- every Arabic shape comes from a JSON made by `certainty glyphs`, never typed or drawn by hand;
- everything to be read stays inside the platforms' safe area (certainty safe checks the film).

As it stands it renders the background, the pen if a scene uses it, and the captions: a valid film to start from.
"""
import json
import pathlib

from engine import verify  # noqa: F401  (for verify.measured)
from engine.canvas import CamPath, Frame, background
from engine.scenes import Captions, draw_pen

HERE = pathlib.Path(__file__).resolve().parent
CL = json.load(open(HERE / "clock.json", encoding="utf-8"))
FPS, NFR = CL["fps"], CL["frames_total"]
LN = {int(l["id"][1:]): l for l in CL["lines"]}
CAPS = Captions(CL)
CAMERA = CamPath([(-1.0, 540, 960, 1.0), (CL["end_s"] + 1, 540, 960, 1.0)])


def w0(n, k):
    """When word k of line n starts (seconds)."""
    return LN[n]["words"][k]["start"]


def w1(n, k):
    """When word k of line n ends."""
    return LN[n]["words"][k]["end"]


# FILL IN: the scenes. For example, a verse written by the pen and underlined as it is spoken:
#
#   from engine.scenes import Phrase
#   OPENING = Phrase(HERE / "art" / "opening.json", 540, 900, 150)   # certainty glyphs phrase 74:30 0 2 art/opening.json
#   ...in frame():  OPENING.write(fr, t, w0(1, 0), w1(1, 5)); OPENING.underline(fr, t, w0(2, 0), w1(2, 3))

_bg = None


def frame(i):
    global _bg
    if _bg is None:
        _bg = background()
    t = i / FPS
    fr = Frame(CAMERA.at(t), _bg)
    fr.pen = None
    # FILL IN: draw this frame's scenes here, each from the clock's times
    draw_pen(fr)
    CAPS.draw(fr, t)
    return fr.render()
