"""Reusable pieces for an episode's timeline, in the series' look (engine/canvas.py).

A timeline (an episode's timeline.py) draws each frame from these and from canvas.py's primitives. Times always come
from the clock (words, count events), never typed. The pieces:

  Phrase        a phrase from `certainty glyphs phrase`, placed, written by the pen right to left
  VerseCount    a verse from `certainty glyphs verse`: at rest in rows, written by the pen, opened into its
                letters one word a row, counted letter by letter on the clock's clicks (outline, then gold, the
                newest brightest), marks set aside as the words open, closed back together
  numeral       a large number drawn and filled in gold (IBM Plex Mono Light)
  pen_session   the pen arriving, drawing and lifting
  Captions      the spoken words as cards, word by word, from the clock

Meaning of color (the look): an outline is a letter not yet counted, gold is counted, blue is set aside.
"""
import json

import numpy as np

from .canvas import (GOLD, GOLD_DEEP, GOLD_HOT, INK, CAP_NEXT, CAP_NOW, CAP_SAID, MONO_LIGHT, Glyph, Strokes,
                     bbox_of, ease, ew, font, leader, lerp, lerp2, ltr_strokes, mix, pen, ramp, rtl_strokes,
                     start_at_right, text_polys, union, window)


# ---- geometry ------------------------------------------------------------------------------------------------------
def put(polys_em, c_em, center, em):
    """em polygons (y up) placed so that the em point c_em lands on the world point center."""
    return [np.column_stack([center[0] + (p[:, 0] - c_em[0]) * em, center[1] - (p[:, 1] - c_em[1]) * em]) for p in polys_em]


def em_place(polys, ox, base, em):
    return [np.column_stack([ox + p[:, 0] * em, base - p[:, 1] * em]) for p in polys]


def shift(polys, dx, dy):
    return [np.column_stack([p[:, 0] + dx, p[:, 1] + dy]) for p in polys]


def scale_about(polys, c, s):
    return [np.column_stack([c[0] + (p[:, 0] - c[0]) * s, c[1] + (p[:, 1] - c[1]) * s]) for p in polys]


# ---- the pen ---------------------------------------------------------------------------------------------------------
def pen_session(fr, t, t0, t1, tip, arrive=True, lift=True):
    """The pen comes in just before t0, draws until t1, and lifts away. The timeline draws fr.pen at the end."""
    if arrive and t0 - 0.3 <= t < t0:
        k = ease(ramp(t, t0 - 0.3, t0))
        fr.pen = ((tip[0] + 70 * (1 - k), tip[1] - 50 * (1 - k)), k)
    elif t0 <= t <= t1:
        fr.pen = (tip, 1.0)
    elif lift and t1 < t <= t1 + 0.4:
        k = ease(ramp(t, t1, t1 + 0.4))
        fr.pen = ((tip[0] + 80 * k, tip[1] - 60 * k), 1 - k)


def draw_pen(fr):
    """Draw the pen where pen_session put it, last, over everything. Near the right edge it stands more upright,
    so its body stays clear of the platforms' buttons."""
    if getattr(fr, "pen", None):
        tip, a = fr.pen
        x = fr.cam.pt(*tip)[0]
        pen(fr, tip, a, angle=58 + 30 * float(np.clip((x - 640) / 240, 0, 1)))


# ---- a phrase ----------------------------------------------------------------------------------------------------------
def load_phrase(path):
    """Words of a phrase JSON laid right to left with the font's space: per word its letters (one union), marks and
    fill (everything), and the total width in em."""
    P = json.load(open(path, encoding="utf-8"))
    total = sum(w["width"] for w in P["words"]) + P["space"] * (len(P["words"]) - 1)
    out, x = [], 0.0
    for w in P["words"]:
        left = total - x - w["width"]

        def polys(g):
            return [np.column_stack([left + p[:, 0], p[:, 1]]) for p in Glyph(g["contours"], g["bbox"]).polys]
        out.append(dict(letters=union([p for g in w["glyphs"] if not g["mark"] for p in polys(g)]),
                        marks=[union(polys(g)) for g in w["glyphs"] if g["mark"]],
                        fill=[p for g in w["glyphs"] for p in polys(g)], width=w["width"]))
        x += w["width"] + P["space"]
    return out, total, P


class Phrase:
    """A phrase centered on cx with its baseline at base, em pixels to the em; written by the pen right to left."""

    def __init__(self, path, cx, base, em, travel=0.25):
        self.words, self.width, self.data = load_phrase(path)
        self.em, self.ox, self.base = em, cx - self.width * em / 2, base
        outl = [p for w in self.words for p in w["letters"] + [q for m in w["marks"] for q in m]]
        self.outline = em_place(outl, self.ox, base, em)
        self.fill = em_place([p for w in self.words for p in w["fill"]], self.ox, base, em)
        self.strokes = rtl_strokes(self.outline, travel=travel)

    def box(self, top=1.05, bottom=0.35):
        return (self.ox, self.base - top * self.em, self.ox + self.width * self.em, self.base + bottom * self.em)

    def write(self, fr, t, t0, t1, color=INK, width=1.7, alpha=0.85, pen=True):
        vis, tip = self.strokes.reveal(ramp(t, t0, t1))
        fr.stroke(vis, color, width, alpha)
        if pen:
            pen_session(fr, t, t0, t1, tip)

    def underline(self, fr, t, t0, t1, alpha=0.95):
        u = ease(ramp(t, t0, t1))
        if u > 0:
            y = self.base + 0.42 * self.em
            leader(fr, [(self.ox + self.width * self.em, y), (self.ox, y)], u, GOLD, alpha, 2.2,
                   glow=("gold_line", GOLD, 3.0, 4.0))


# ---- a verse, counted -----------------------------------------------------------------------------------------------
class _Letter:
    def __init__(self, d, wi):
        self.ctx = Glyph(d["contours"], d["bbox"], "letter", d["char"])
        self.iso = Glyph(d["iso_contours"], d["iso_bbox"], "letter", d["char"])
        self.word, self.index, self.char = wi, d["index"], d["char"]


class VerseCount:
    """A verse from `glyphs verse`. At rest it sits in rows (rows=[[0, 1], [2, 3]] puts words 0 and 1 on the first
    row, right to left); counting, each word takes a row of its own and opens into its standalone letters.

    Times it needs, all from the clock: write (t0, t1) for the pen; open_t for the words opening; clicks (one time per
    letter, in reading order); numeral (the landing); close_t to bring it back together."""

    def __init__(self, path, rows, em_rest=165, row_base=(600, 960), gap_rest=0.28, cx=540,
                 em_count=150, count_base=None, gap_count=0.24):
        B = json.load(open(path, encoding="utf-8"))
        self.words = []
        for w in B["words"]:
            letters = [_Letter(l, w["index"]) for l in w["letters"]]
            marks = [Glyph(m["contours"], m["bbox"], "mark", m["glyph"]) for m in w["marks"]]
            self.words.append(dict(letters=letters, marks=marks, width=w["width"],
                                   union=union([p for l in letters for p in l.ctx.polys])))
        self.letters = [l for w in self.words for l in w["letters"]]
        self.n = len(self.letters)
        self.em_r, self.em_c = em_rest, em_count
        self.rest = {}
        for row, base in zip(rows, row_base):
            total = sum(self.words[i]["width"] for i in row) + gap_rest * (len(row) - 1)
            right = cx + total * em_rest / 2
            for i in row:
                left = right - self.words[i]["width"] * em_rest
                self.rest[i] = (left, base)
                right = left - gap_rest * em_rest
        nw = len(self.words)
        assert nw <= 5, "a counted verse takes one row a word: five words at most"
        count_base = count_base or [450 + 225 * k * 4 / max(4, nw) for k in range(nw)]
        self.count_base = count_base
        self.count = {}
        self.rows = []
        for k, w in enumerate(self.words):
            ws = [l.iso.bbox[2] - l.iso.bbox[0] for l in w["letters"]]
            total = sum(ws) + gap_count * (len(ws) - 1)
            right = 540 + total * em_count / 2
            self.rows.append((540 - total * em_count / 2, 540 + total * em_count / 2))
            for l, wd in zip(w["letters"], ws):
                ox = right - l.iso.bbox[2] * em_count
                self.count[l.index] = (ox + l.iso.center[0] * em_count, count_base[k] - l.iso.center[1] * em_count)
                right -= (wd + gap_count) * em_count
            assert self.rows[-1][1] - self.rows[-1][0] <= 760, f"word {k} is too wide to count on one row"
        strokes = []
        for wi in range(nw):
            strokes.extend(sorted(self.word_polys(wi) + [p for m in self.words[wi]["marks"]
                                                        for p in self.mark_polys(m, wi)], key=lambda p: -p[:, 0].max()))
        self.strokes = Strokes([start_at_right(p) for p in strokes], travel=0.25)
        xs = [self.rest[i][0] for i in range(nw)] + [self.rest[i][0] + self.words[i]["width"] * em_rest for i in range(nw)]
        self.box = (min(xs) - 26, row_base[0] - 1.15 * em_rest, max(xs) + 26, row_base[len(rows) - 1] + 0.86 * em_rest)

    def word_polys(self, wi, outline=True):
        ox, base = self.rest[wi]
        w = self.words[wi]
        src = w["union"] if outline else [p for l in w["letters"] for p in l.ctx.polys]
        return [np.column_stack([ox + p[:, 0] * self.em_r, base - p[:, 1] * self.em_r]) for p in src]

    def mark_polys(self, m, wi, outline=True):
        ox, base = self.rest[wi]
        c = (ox + m.center[0] * self.em_r, base - m.center[1] * self.em_r)
        return put(m.outline if outline else m.polys, m.center, c, self.em_r)

    def draw(self, fr, t, write, open_t, clicks, numeral, close_t=None, alpha=1.0):
        """The whole life of the counted verse, in one call per frame."""
        t0, t1 = write
        nw = len(self.words)
        if t < t1 + 0.05:                                            # the pen writes it, marks and all
            vis, tip = self.strokes.reveal(ramp(t, t0, t1))
            fr.stroke(vis, INK, 1.7, 0.72 * alpha)
            pen_session(fr, t, t0, t1, tip)
            return
        if t < t1 + 0.4:
            pen_session(fr, t, t0, t1, self.strokes.reveal(1.0)[1])
        marks_a = (1 - ew(t, open_t, open_t + 0.45)) * alpha
        back = ew(t, close_t + 0.55, close_t + 0.95) if close_t else 0
        for wi in range(nw):
            for m in self.words[wi]["marks"]:
                if marks_a > 0:
                    fr.stroke(self.mark_polys(m, wi), INK, 1.7, 0.72 * marks_a)
                if back > 0:
                    fr.fill(self.mark_polys(m, wi, outline=False), GOLD, 0.85 * back * alpha)
        if t < open_t:                                               # at rest
            for wi in range(nw):
                fr.stroke(self.word_polys(wi), INK, 1.7, 0.72 * alpha)
            return
        if t < open_t + 1.0:                                         # the words take a row each and open
            for wi in range(nw):
                mv = ew(t, open_t + wi * 0.04, open_t + 0.55 + wi * 0.04)
                op = ew(t, open_t + 0.4 + wi * 0.08, open_t + 0.85 + wi * 0.05)
                ox0, b0 = self.rest[wi]
                ox1, b1 = 540 - self.words[wi]["width"] * self.em_c / 2, self.count_base[wi]
                ox, base, em = lerp(ox0, ox1, mv), lerp(b0, b1, mv), lerp(self.em_r, self.em_c, mv)
                if op <= 0:
                    w = self.words[wi]
                    fr.stroke([np.column_stack([ox + p[:, 0] * em, base - p[:, 1] * em]) for p in w["union"]], INK, 1.7,
                              0.72 * alpha)
                    continue
                for l in self.words[wi]["letters"]:
                    c_ctx = (ox + l.ctx.center[0] * em, base - l.ctx.center[1] * em)
                    c = lerp2(c_ctx, self.count[l.index], op)
                    v = ease(ramp(op, 0.25, 0.85))
                    fr.stroke(put(l.ctx.outline, l.ctx.center, c, em), INK, 1.7, 0.72 * (1 - v) * alpha)
                    fr.stroke(put(l.iso.outline, l.iso.center, c, self.em_c), INK, 1.7, 0.72 * v * alpha)
            return
        if close_t is None or t < close_t:                           # the count
            for l in self.letters:
                c = self.count[l.index]
                tc = clicks[l.index]
                polys = put(l.iso.polys, l.iso.center, c, self.em_c)
                if t < tc:
                    fr.stroke(put(l.iso.outline, l.iso.center, c, self.em_c), INK, 1.7, 0.75 * alpha)
                    continue
                rise = ramp(t, tc, tc + 2 / 24)
                nxt = clicks[l.index + 1] if l.index + 1 < self.n else numeral + 0.4
                hot = 1 - ew(t, nxt, nxt + 0.25)
                pulse = window(t, numeral + 0.05, numeral + 0.3, numeral + 0.6, numeral + 1.4)
                fr.fill(polys, mix(GOLD, GOLD_HOT, hot), (0.92 + 0.08 * hot) * rise * alpha,
                        glow=("gold", GOLD_DEEP, 0.55 + 0.45 * pulse, 5.0))
                if hot > 0.02:
                    fr.fill(polys, GOLD_HOT, 0, glow=("hot", GOLD, 1.0, 7.0), glow_amount=hot * rise * alpha,
                            soft=(GOLD, 10, 0.18 * hot * rise * alpha))
                if rise < 1:
                    fr.stroke(put(l.iso.outline, l.iso.center, c, self.em_c), INK, 1.7, 0.7 * (1 - rise) * alpha)
            return
        for l in self.letters:                                       # closing, still gold
            f = ew(t, close_t + (self.n - 1 - l.index) * 0.02, close_t + 0.9 + (self.n - 1 - l.index) * 0.02)
            ox, base = self.rest[l.word]
            c = lerp2(self.count[l.index], (ox + l.ctx.center[0] * self.em_r, base - l.ctx.center[1] * self.em_r), f)
            em = lerp(self.em_c, self.em_r, f)
            v = ease(ramp(f, 0.15, 0.75))
            if v < 1:
                fr.fill(put(l.iso.polys, l.iso.center, c, em), GOLD, 0.92 * (1 - v) * alpha)
            if v > 0:
                fr.fill(put(l.ctx.polys, l.ctx.center, c, em), GOLD, 0.92 * v * alpha)

    def row_lines(self, fr, t, word_open, word_close, alpha=1.0):
        """A hairline under each row as its word is picked up; gold when the word's last letter is counted."""
        for k in range(len(self.words)):
            y = self.count_base[k] + 0.526 * self.em_c + 14
            x0, x1 = self.rows[k]
            on = ew(t, word_open[k], word_open[k] + 0.3)
            gold = ew(t, word_close[k], word_close[k] + 0.12)
            if on > 0:
                leader(fr, [(x1 + 10, y), (x0 - 10, y)], on, (205, 198, 200), 0.45 * (1 - gold) * alpha, 1.2)
            if gold > 0:
                leader(fr, [(x1 + 10, y), (x0 - 10, y)], gold, GOLD, 0.95 * alpha, 1.8, glow=("gold_line", GOLD, 2.0, 4.0))


# ---- a large number ----------------------------------------------------------------------------------------------------
def number_polys(s, c, px):
    cs, _ = text_polys(MONO_LIGHT, s, px)
    polys = [p for ch in cs for p in ch]
    b = bbox_of(polys)
    return [np.column_stack([p[:, 0] - (b[0] + b[2]) / 2 + c[0], p[:, 1] - (b[1] + b[3]) / 2 + c[1]]) for p in polys]


def numeral(fr, t, s, c, px, t0, alpha=1.0):
    """The number drawn by its outline in 0.3 s from t0, then filled gold with a soft glow."""
    polys = number_polys(s, c, px)
    if t < t0:
        return
    vis, _ = ltr_strokes(polys, travel=0.3).reveal(ramp(t, t0, t0 + 0.3))
    f = ew(t, t0 + 0.12, t0 + 0.4)
    fr.stroke(vis, GOLD, 1.6, 0.9 * alpha * (1 - 0.6 * f))
    if f > 0:
        fr.fill(polys, GOLD, 0.95 * f * alpha, glow=("gold", GOLD_DEEP, 0.9, 6.0), soft=(GOLD, 10, 0.3 * f * alpha))


# ---- captions (the spoken words, word by word) -------------------------------------------------------------------------
class Captions:
    """Cards built from the clock's lines: one per line, split at sentences or commas when too wide for two lines.
    Placed low in the frame (y 1324), inside every platform's safe area, at most 720 px wide."""

    SOFT_END = {"the", "a", "an", "of", "to", "in", "and", "has", "is", "with", "can", "for", "be", "at", "us",
                "this", "our", "his", "you", "it", "that", "those", "first", "every", "but", "after", "what"}

    def __init__(self, clock, px=40, max_w=720, y=1324, face="Poppins-SemiBold.ttf", face_said="Poppins-Regular.ttf"):
        self.px, self.max_w, self.y, self.face, self.face_said = px, max_w, y, face, face_said
        self.cards = self._build(clock)

    def _w(self, words):
        fb = font(self.face, self.px)
        return sum(fb.getlength(w["w"]) / 4 for w in words) + fb.getlength(" ") / 4 * (len(words) - 1)

    def _layout(self, words):
        fb = font(self.face, self.px)
        sp = fb.getlength(" ") / 4
        wd = [fb.getlength(w["w"]) / 4 for w in words]
        if sum(wd) + sp * (len(wd) - 1) <= 600:
            return [words]
        best = None
        for k in range(1, len(words)):
            a = sum(wd[:k]) + sp * (k - 1)
            b = sum(wd[k:]) + sp * (len(wd) - k - 1)
            last = words[k - 1]["w"].lower().strip(".,:;?!“”")
            score = max(a, b) - (150 if words[k - 1]["w"][-1] in ",.:?”" else 0) + (140 if last in self.SOFT_END else 0)
            if best is None or score < best[0]:
                best = (score, k, max(a, b))
        return [words[:best[1]], words[best[1]:]] if best[2] <= self.max_w else None

    def _build(self, clock):
        cards, lines = [], clock["lines"]
        for i, l in enumerate(lines):
            words, groups, cur = l["words"], [], []
            for j, w in enumerate(words):
                cur.append(w)
                if w["w"][-1] in ".?:" and j + 1 < len(words) and self._w(words) > 700:
                    groups.append(cur)
                    cur = []
            if cur:
                groups.append(cur)
            todo, split = list(groups), []
            while todo:
                g = todo.pop(0)
                if self._layout(g) or len(g) < 4:
                    split.append(g)
                    continue
                cuts = [j for j in range(2, len(g) - 1) if g[j - 1]["w"][-1] == ","]
                cuts = [j for j in cuts if self._layout(g[:j]) and self._layout(g[j:])] or list(range(2, len(g) - 1))
                j = min(cuts, key=lambda j: abs(self._w(g[:j]) - self._w(g[j:])))
                todo[:0] = [g[:j], g[j:]]
            nxt = lines[i + 1]["words"][0]["start"] if i + 1 < len(lines) else clock["end_s"]
            for gi, g in enumerate(split):
                t_in = g[0]["start"] - 0.12
                t_out = split[gi + 1][0]["start"] - 0.12 if gi + 1 < len(split) else min(nxt - 0.12, g[-1]["end"] + 0.75)
                lay = self._layout(g)
                assert lay, " ".join(w["w"] for w in g)
                cards.append(dict(lines=lay, t_in=t_in, t_out=t_out))
        return cards

    def draw(self, fr, t):
        for c in self.cards:
            if not (c["t_in"] <= t <= c["t_out"]):
                continue
            a = ew(t, c["t_in"], c["t_in"] + 0.12) * (1 - ew(t, c["t_out"] - 0.12, c["t_out"]))
            allw = [w for line in c["lines"] for w in line]
            n = len(c["lines"])
            for li, line in enumerate(c["lines"]):
                y = self.y + (27 if n == 1 else li * 54)
                ws = [fr.text_width(w["w"], self.face, self.px) for w in line]
                sp = fr.text_width(" ", self.face, self.px)
                x = 540 - (sum(ws) + sp * (len(line) - 1)) / 2
                for w, wd in zip(line, ws):
                    k = allw.index(w)
                    end = allw[k + 1]["start"] if k + 1 < len(allw) else w["end"] + 0.2
                    state = "said" if t >= end else ("now" if t >= w["start"] else "next")
                    if state == "now":
                        fr.text((x, y), w["w"], self.face, self.px, CAP_NOW, a, screen=True, soft=(CAP_NOW, 5, 0.35 * a))
                    else:
                        off = (wd - fr.text_width(w["w"], self.face_said, self.px)) / 2
                        fr.text((x + off, y), w["w"], self.face_said, self.px, CAP_SAID if state == "said" else CAP_NEXT, a,
                                screen=True)
                    x += wd + sp

    def srt(self):
        def ts(s):
            ms = int(round(max(0.0, s) * 1000))
            h, ms = divmod(ms, 3600000)
            m, ms = divmod(ms, 60000)
            s_, ms = divmod(ms, 1000)
            return f"{h:02d}:{m:02d}:{s_:02d},{ms:03d}"
        out = []
        for k, c in enumerate(self.cards, 1):
            text = "\n".join(" ".join(w["w"] for w in line) for line in c["lines"])
            out.append(f"{k}\n{ts(c['t_in'])} --> {ts(c['t_out'])}\n{text}\n")
        return "\n".join(out)
