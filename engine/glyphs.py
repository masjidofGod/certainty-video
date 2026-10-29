"""Exact Arabic outlines from the data: shaped by HarfBuzz in Amiri Quran, overlaps removed, as JSON.

    certainty glyphs verse 1:1 <out.json>          every letter (joined and standalone) and every mark
    certainty glyphs phrase 74:30 0 2 <out.json>   words 0 to 2 of a verse as written, marks and all

Arabic is never retyped or redrawn: every letter and mark is the font's own outline, placed by HarfBuzz from the
verse text in the data file. Contours are cubic, in em units with y up.

verse: letters come from verse_text_arabic_clean (one glyph per letter, or it fails loudly: a ligature would merge
letters and break the count), marks from verse_text_arabic (zero-advance glyphs, plus the wasla of an alef wasla).
phrase: each word is shaped alone from the marked text, so letters and marks come from one shaping.
"""
import json
import os

import pathops
import uharfbuzz as hb
from fontTools.ttLib import TTFont

from . import data
from .settings import FONTS

FONT = str(FONTS / "AmiriQuran-Regular.ttf")
_tt = TTFont(FONT)
_gs, _names, UPEM = _tt.getGlyphSet(), _tt.getGlyphOrder(), _tt["head"].unitsPerEm
_hbf = hb.Font(hb.Face(hb.Blob.from_file_path(FONT)))


def shape(text):
    b = hb.Buffer()
    b.add_str(text)
    b.guess_segment_properties()
    hb.shape(_hbf, b, {})
    x, out = 0, []
    for i, p in zip(b.glyph_infos, b.glyph_positions):
        out.append(dict(name=_names[i.codepoint], cluster=i.cluster, x=x + p.x_offset, y=p.y_offset, adv=p.x_advance))
        x += p.x_advance
    return out, x


def outline(name, dx=0, dy=0):
    """A glyph's contours as cubic Beziers in em units, overlaps removed, and its bounding box."""
    path = pathops.Path()
    _gs[name].draw(path.getPen(glyphSet=_gs))
    path.simplify(fix_winding=True)
    contours, cur = [], None
    for verb, pts in path.segments:
        if verb == "moveTo":
            cur = [list(pts[0])]
            continue
        if verb == "lineTo":
            p0, p1 = cur[-1], list(pts[0])
            cur += [[p0[0] + (p1[0] - p0[0]) / 3, p0[1] + (p1[1] - p0[1]) / 3],
                    [p0[0] + 2 * (p1[0] - p0[0]) / 3, p0[1] + 2 * (p1[1] - p0[1]) / 3], p1]
        elif verb == "qCurveTo":
            p0, qs = cur[-1], [list(q) for q in pts]
            for k in range(len(qs) - 1):             # implied on-curve points between consecutive off-curve points
                q = qs[k]
                e = qs[k + 1] if k == len(qs) - 2 else [(qs[k][0] + qs[k + 1][0]) / 2, (qs[k][1] + qs[k + 1][1]) / 2]
                cur += [[p0[0] + 2 / 3 * (q[0] - p0[0]), p0[1] + 2 / 3 * (q[1] - p0[1])],
                        [e[0] + 2 / 3 * (q[0] - e[0]), e[1] + 2 / 3 * (q[1] - e[1])], e]
                p0 = e
        elif verb == "curveTo":
            cur += [list(p) for p in pts]
        elif verb in ("closePath", "endPath"):
            if cur and len(cur) > 1:
                if abs(cur[-1][0] - cur[0][0]) > 1e-6 or abs(cur[-1][1] - cur[0][1]) > 1e-6:
                    p0, p1 = cur[-1], cur[0]
                    cur += [[p0[0] + (p1[0] - p0[0]) / 3, p0[1] + (p1[1] - p0[1]) / 3],
                            [p0[0] + 2 * (p1[0] - p0[0]) / 3, p0[1] + 2 * (p1[1] - p0[1]) / 3], list(p1)]
                contours.append([[(c[0] + dx) / UPEM, (c[1] + dy) / UPEM] for c in cur])
            cur = None
    xs = [p[0] for c in contours for p in c]
    ys = [p[1] for c in contours for p in c]
    return contours, ([min(xs), min(ys), max(xs), max(ys)] if xs else None)


def export_verse(vid):
    clean, marked = data.text(vid), data.marked(vid)
    cw, mw = clean.split(" "), marked.split(" ")
    assert len(cw) == len(mw), f"{vid}: the clean and marked texts split into {len(cw)} and {len(mw)} words"
    words, letter_i = [], 0
    for wi, (c, m) in enumerate(zip(cw, mw)):
        cg, cwid = shape(c)
        mg, _ = shape(m)
        n = len(data.letters(c))
        assert len(cg) == len(c), f"{vid} word {wi}: {len(cg)} glyphs for {len(c)} characters (a ligature merged letters)"
        letters = []
        for g in sorted(cg, key=lambda g: g["cluster"]):          # reading order, right to left
            ch = c[g["cluster"]]
            ctr, bb = outline(g["name"], g["x"], g["y"])
            iso, _ = shape(ch)
            assert len(iso) == 1
            ictr, ibb = outline(iso[0]["name"])
            letters.append(dict(index=letter_i, char=ch, codepoint=f"U+{ord(ch):04X}", glyph=g["name"], contours=ctr,
                                bbox=bb, iso_glyph=iso[0]["name"], iso_contours=ictr, iso_bbox=ibb))
            letter_i += 1
        assert len(letters) == n, f"{vid} word {wi}: {len(letters)} glyphs, {n} letters"
        marks = []
        for g in mg:
            gl = _tt["glyf"][g["name"]]
            if g["adv"] == 0:
                ctr, bb = outline(g["name"], g["x"], g["y"])
                marks.append(dict(glyph=g["name"], contours=ctr, bbox=bb))
            elif g["name"] == "uni0671":                            # the wasla of an alef wasla is a mark too
                for comp in gl.components:
                    if comp.glyphName != _tt["glyf"]["uni0627"].components[0].glyphName:
                        ctr, bb = outline(comp.glyphName, g["x"] + comp.x, g["y"] + comp.y)
                        marks.append(dict(glyph=comp.glyphName + " (wasla of U+0671)", contours=ctr, bbox=bb))
        words.append(dict(index=wi, clean=c, marked=m, width=cwid / UPEM, letters=letters, marks=marks))
    return dict(verse=vid, font=os.path.basename(FONT), upem=UPEM, letters=letter_i, words=words)


def export_phrase(vid, a, b):
    marked = data.marked(vid).split(" ")
    words = []
    for k in range(a, b + 1):
        text = marked[k]
        gl, wid = shape(text)
        glyphs = []
        for g in gl:
            ctr, bb = outline(g["name"], g["x"], g["y"])
            if ctr:
                glyphs.append(dict(name=g["name"], cluster=g["cluster"], mark=g["adv"] == 0, contours=ctr, bbox=bb))
        words.append(dict(index=k, marked=text, width=wid / UPEM, glyphs=glyphs))
    space = shape(" ")[1] / UPEM
    return dict(verse=vid, words_from=a, words_to=b, text=" ".join(marked[a:b + 1]), font=os.path.basename(FONT),
                upem=UPEM, space=space, words=words)


def main(argv):
    if len(argv) >= 3 and argv[0] == "verse":
        out = export_verse(argv[1])
        dest = argv[2]
    elif len(argv) >= 5 and argv[0] == "phrase":
        out = export_phrase(argv[1], int(argv[2]), int(argv[3]))
        dest = argv[4]
    else:
        raise SystemExit(__doc__)
    os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False)
    if argv[0] == "verse":
        print(f"{dest}: {out['letters']} letters, words {[len(w['letters']) for w in out['words']]}, "
              f"marks {[len(w['marks']) for w in out['words']]}")
    else:
        print(f"{dest}: {out['text']}")
    return 0
