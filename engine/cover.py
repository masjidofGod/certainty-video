"""The episode's cover: 1080 x 1920, in the look, over a painting if you give one.

    certainty cover <episode>

Settings in episode.toml (every key optional but headline):

    [cover]
    painting = "covers/painting.jpg"   # a painting you may use (public domain: record its source in covers/SOURCES.md)
    focus = [0.5, 0.3]                 # the point of the painting to keep in view (fractions of its width, height)
    place = [0.5, 0.33]                # where that point sits on the cover
    series = "CERTAINTY"
    episode = "EPISODE 1"
    arabic = "art/cover-phrase.json"   # a phrase from `certainty glyphs phrase`, drawn in gold
    numbers = ["19"]                   # a row of large numbers (take them from your claims)
    number_labels = ["LETTERS IN 1:1"]
    headline = ["COUNT IT"]            # one or two lines
    gold_words = ["COUNT"]
    logo = ""                          # your own mark: a white-on-black PNG, drawn in gold

Writes out/cover.png (the master), out/cover-reels.jpg (9:16) and out/cover-tiktok.jpg (3:4, the middle 1440 rows).
Everything to be read sits inside the middle 4:5 band (y 285 to 1635), so profile grids that crop to 3:4 keep it.
"""
import numpy as np
from PIL import Image

from .canvas import BG, GOLD, GOLD_DEEP, INK, MONO, MONO_LIGHT, Cam, Frame, Patch, background, label
from .episode import Episode
from .scenes import Phrase

HEAD = "Poppins-SemiBold.ttf"


def painted(path, focus, place, W=1080, H=1920):
    """The painting covering the frame, graded into the look: a little darker and warmer, a vignette, the lower part
    sinking to the canvas color so the type reads."""
    im = Image.open(path).convert("RGB")
    pw, ph = im.size
    s = max(W / pw, H / ph) * 1.08
    sw, sh = int(pw * s), int(ph * s)
    x0 = int(np.clip(focus[0] * sw - place[0] * W, 0, sw - W))
    y0 = int(np.clip(focus[1] * sh - place[1] * H, 0, sh - H))
    a = np.asarray(im.resize((sw, sh), Image.LANCZOS), np.float32)[y0:y0 + H, x0:x0 + W]
    lum = a.mean(axis=2, keepdims=True)
    a = 0.6 * a + 0.4 * lum * np.array([1.0, 0.93, 0.78], np.float32)
    a = 255 * (a / 255) ** 1.1 * 0.88
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    vign = 1 - 0.55 * np.clip(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.4) / (H * 0.62)) ** 2, 0, 1)
    sink = 1 - 0.88 * np.clip((yy - H * 0.47) / (H * 0.2), 0, 1)
    k = (vign * sink)[..., None]
    return a * k + np.array(BG, np.float32) * (1 - k)


def headline(fr, lines, y, px, gold_words=()):
    for i, line in enumerate(lines):
        words = line.split(" ")
        widths = [fr.text_width(w, HEAD, px, track=-1) for w in words]
        sp = fr.text_width(" ", HEAD, px)
        x = 540 - (sum(widths) + sp * (len(words) - 1)) / 2
        for w, wd in zip(words, widths):
            g = w.strip(".?!,") in gold_words
            fr.text((x, y + i * px * 1.08), w, HEAD, px, GOLD if g else INK, 1.0, track=-1, soft=(GOLD, 10, 0.35) if g else None)
            x += wd + sp


def make(ep):
    c = ep.cfg.get("cover", {})
    bg = painted(ep.path(c["painting"]), c.get("focus", [0.5, 0.3]), c.get("place", [0.5, 0.33])) if c.get("painting") else background()
    fr = Frame(Cam(), bg)
    fr.text((540, 300), c.get("series", "CERTAINTY"), HEAD, 30, INK, 0.95, anchor="ma", track=12)
    if c.get("episode"):
        fr.text((540, 344), c["episode"], MONO, 17, GOLD, 0.95, anchor="ma", track=6)
    lines = c.get("headline", [])
    y_head = 1405 if len(lines) <= 1 else 1330
    y = y_head - 140
    if c.get("numbers"):
        nums, labels = c["numbers"], c.get("number_labels", [""] * len(c["numbers"]))
        xs = [540 + (k - (len(nums) - 1) / 2) * 210 for k in range(len(nums))]
        for x, s, lab in zip(xs, nums, labels):
            big = s.strip() not in ("=", "+", "×")
            fr.text((x, y), s, MONO_LIGHT, 150 if big else 100, GOLD if big else INK, 1.0 if big else 0.85, anchor="mm",
                    glow=("gold", GOLD_DEEP, 1.0, 7.0) if big else None, soft=(GOLD, 16, 0.4) if big else None)
            if lab:
                label(fr, (x, y + 84), lab, 1.0, px=18, alpha=0.9, anchor="ma")
        y -= 130
    if c.get("arabic"):
        P = Phrase(ep.path(c["arabic"]), 540, y, 170)
        fr.fill(P.fill, GOLD, 0.97, glow=("gold", GOLD_DEEP, 0.9, 6.0), soft=(GOLD, 10, 0.3))
    headline(fr, lines, y_head, 104 if len(lines) <= 1 else 92, tuple(c.get("gold_words", [])))
    if c.get("logo"):
        m = Image.open(ep.path(c["logo"])).convert("L")
        w = 170
        m = np.asarray(m.resize((w, int(m.height * w / m.width)), Image.LANCZOS), np.float32) / 255.0
        pt = Patch(m, 540 - w // 2, 1548)
        fr.layers.append((pt, GOLD, 0.95))
        fr.glow_add(pt, "gold", GOLD_DEEP, 0.45, 4.0, amount=0.95)
    return Image.fromarray(fr.render())


def main(argv):
    if not argv:
        raise SystemExit("usage: certainty cover <episode>")
    ep = Episode(argv[0])
    out = ep.path("out")
    out.mkdir(parents=True, exist_ok=True)
    im = make(ep)
    im.save(out / "cover.png")
    im.save(out / "cover-reels.jpg", quality=95, subsampling=0)
    im.crop((0, 240, 1080, 1680)).save(out / "cover-tiktok.jpg", quality=95, subsampling=0)
    print(f"wrote {out / 'cover.png'}, cover-reels.jpg, cover-tiktok.jpg")
    return 0
