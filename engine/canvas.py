"""The series' line-art engine: the look as code.

Everything is drawn through a camera onto one dark canvas at 1080 x 1920. Shapes are rasterized in a local box
at 4x supersampling and composited in order; glow is the series' halftone (dots on a grid fixed to the canvas,
sized by a blurred copy of the shapes, outside the shapes only), computed once per color per frame under the
shapes. Arabic is the font's own outline (Amiri Quran through HarfBuzz, `certainty glyphs`), never retyped:
joined letters are outlined from the union of their polygons, so a word shows no seam at its joins.

Coordinates: world units equal screen pixels at zoom 1 with the camera centered on (540, 960). Glyph data is
in em units with y up; Glyph.place() puts it in the world.
"""
import math
import os

import numpy as np
import pathops
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter

from .settings import FONTS as _FONTS

FONTS = str(_FONTS)

W, H, SS = 1080, 1920, 4
CX, CY = W / 2, H / 2

# the palette (measured from the series' reference)
BG = (13, 15, 16)
INK = (240, 233, 230)
GOLD = (237, 214, 170)
GOLD_DEEP = (178, 150, 104)
GOLD_HOT = (250, 236, 206)
BLUE = (134, 160, 186)
BLUE_DEEP = (88, 107, 128)
LABEL = (205, 198, 200)
CAP_SAID = (232, 226, 230)
CAP_NOW = (246, 240, 243)
CAP_NEXT = (87, 82, 88)


# ---- time ----------------------------------------------------------------------------------------------------------
def ramp(t, t0, t1):
    if t1 <= t0:
        return 1.0 if t >= t1 else 0.0
    return min(1.0, max(0.0, (t - t0) / (t1 - t0)))


def ease(u):
    """Cubic in and out."""
    return 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2


def eout(u):
    return 1 - (1 - u) ** 3


def ein(u):
    return u ** 3


def ew(t, t0, t1):
    return ease(ramp(t, t0, t1))


def window(t, a, b, c, d):
    """0 before a, up to 1 by b, 1 until c, down to 0 by d (eased)."""
    return ew(t, a, b) * (1 - ew(t, c, d))


def lerp(a, b, u):
    return a + (b - a) * u


def lerp2(p, q, u):
    return (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u)


def mix(c1, c2, u):
    return tuple(a + (b - a) * u for a, b in zip(c1, c2))


# ---- camera --------------------------------------------------------------------------------------------------------
class Cam:
    def __init__(self, cx=CX, cy=CY, zoom=1.0):
        self.cx, self.cy, self.zoom = cx, cy, zoom

    def pt(self, x, y):
        return ((x - self.cx) * self.zoom + CX, (y - self.cy) * self.zoom + CY)

    def pts(self, a):
        a = np.asarray(a, float)
        out = np.empty_like(a)
        out[:, 0] = (a[:, 0] - self.cx) * self.zoom + CX
        out[:, 1] = (a[:, 1] - self.cy) * self.zoom + CY
        return out


SCREEN = Cam()                                    # identity: for the captions and the claim and result tags


# ---- fonts ---------------------------------------------------------------------------------------------------------
_fonts = {}


def font(name, px):
    key = (name, max(4, int(round(px * SS))))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONTS, name), key[1])
    return _fonts[key]


# ---- polylines -----------------------------------------------------------------------------------------------------
def bez(p0, c1, c2, p1, n):
    t = np.linspace(0, 1, n + 1)[1:, None]
    p0, c1, c2, p1 = map(np.asarray, (p0, c1, c2, p1))
    return (1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * c1 + 3 * (1 - t) * t ** 2 * c2 + t ** 3 * p1


def flatten(contour, n=10):
    """A contour of export_glyphs.py (p0, then c1 c2 p1 per cubic) as a closed polygon, em units."""
    pts = [np.asarray(contour[0], float)[None]]
    for k in range(1, len(contour) - 2, 3):
        pts.append(bez(contour[k - 1], contour[k], contour[k + 1], contour[k + 2], n))
    return np.concatenate(pts)


def union(polys):
    """Union of closed polygons (nonzero winding), as closed polygons."""
    p = pathops.Path()
    pen = p.getPen()
    for poly in polys:
        if len(poly) < 3:
            continue
        pen.moveTo(tuple(poly[0]))
        for q in poly[1:]:
            pen.lineTo(tuple(q))
        pen.closePath()
    p.simplify(fix_winding=True)
    out, cur = [], []
    for verb, pts in p.segments:
        if verb == "moveTo":
            cur = [pts[0]]
        elif verb == "lineTo":
            cur.append(pts[0])
        elif verb in ("closePath", "endPath"):
            if len(cur) > 2:
                out.append(np.array(cur, float))
            cur = []
        else:
            cur.extend(pts)
    return out


def closed(poly):
    return np.vstack([poly, poly[:1]])


def arclen(poly):
    d = np.hypot(*np.diff(poly, axis=0).T)
    return np.concatenate([[0], np.cumsum(d)])


def partial(poly, u):
    """The first u (0 to 1) of an open polyline by length, and its end point."""
    s = arclen(poly)
    if s[-1] <= 0 or u >= 1:
        return poly, poly[-1]
    if u <= 0:
        return poly[:1], poly[0]
    L = u * s[-1]
    k = int(np.searchsorted(s, L))
    f = (L - s[k - 1]) / max(1e-9, s[k] - s[k - 1])
    end = poly[k - 1] + (poly[k] - poly[k - 1]) * f
    return np.vstack([poly[:k], end[None]]), end


def start_at_right(poly):
    """A closed polygon re-ordered to start at its rightmost point, open (first point repeated at the end):
    a pen writing right to left begins there."""
    k = int(np.argmax(poly[:, 0]))
    p = np.vstack([poly[k:], poly[:k]])
    return closed(p)


class Strokes:
    """An ordered set of open polylines drawn by one pen. Between two lines the pen travels in the air (faster
    than it draws), so its tip never jumps. reveal(u) gives the visible part and the tip."""

    def __init__(self, lines, travel=0.3):
        self.lines = [np.asarray(l, float) for l in lines if len(l) > 1]
        self.segs = []
        for i, l in enumerate(self.lines):
            if i:
                a, b = self.lines[i - 1][-1], l[0]
                self.segs.append(("air", (a, b), float(np.hypot(*(b - a))) * travel))
            self.segs.append(("ink", i, float(arclen(l)[-1])))
        lens = np.array([s[2] for s in self.segs])
        self.total = float(lens.sum())
        self.cum = np.concatenate([[0], np.cumsum(lens)])

    def reveal(self, u):
        if not self.lines:
            return [], (0.0, 0.0)
        if u >= 1:
            return self.lines, tuple(self.lines[-1][-1])
        if u <= 0:
            return [], tuple(self.lines[0][0])
        L = u * self.total
        k = min(len(self.segs) - 1, int(np.searchsorted(self.cum, L, side="right")) - 1)
        kind, data, n = self.segs[k]
        f = (L - self.cum[k]) / max(1e-9, n)
        if kind == "air":
            done = self.lines[:self.segs[k + 1][1]]
            return done, tuple(data[0] + (data[1] - data[0]) * f)
        part, tip = partial(self.lines[data], f)
        return self.lines[:data] + [part], tuple(tip)


def rtl_strokes(polys, travel=0.3):
    """Outline polygons ordered right to left by their right edge, each starting at its rightmost point."""
    return Strokes([start_at_right(p) for p in sorted(polys, key=lambda p: -p[:, 0].max())], travel)


def ltr_strokes(polys, travel=0.3):
    """Ordered left to right, each starting at its topmost point: Latin capitals and digits."""
    out = []
    for p in sorted(polys, key=lambda p: p[:, 0].min()):
        k = int(np.argmin(p[:, 1]))
        out.append(closed(np.vstack([p[k:], p[:k]])))
    return Strokes(out, travel)


# ---- outlines of Latin type ----------------------------------------------------------------------------------------
_ttf = {}


def text_polys(fname, s, px, track=0.0):
    """Each character of s as closed polygons in pixels, baseline at y 0, y down, from x 0; and the advance."""
    from fontTools.pens.basePen import BasePen
    from fontTools.ttLib import TTFont
    if fname not in _ttf:
        _ttf[fname] = TTFont(os.path.join(FONTS, fname))
    tt = _ttf[fname]
    gs, cmap, upem, hmtx = tt.getGlyphSet(), tt.getBestCmap(), tt["head"].unitsPerEm, tt["hmtx"]
    k = px / upem

    class Flat(BasePen):
        def __init__(self):
            super().__init__(gs)
            self.polys, self.cur = [], []

        def _moveTo(self, p):
            self.cur = [p]

        def _lineTo(self, p):
            self.cur.append(p)

        def _curveToOne(self, p1, p2, p3):
            self.cur.extend(map(tuple, bez(self.cur[-1], p1, p2, p3, 8)))

        def _qCurveToOne(self, p1, p2):
            p0 = np.asarray(self.cur[-1], float)
            t = np.linspace(0, 1, 9)[1:, None]
            q = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * np.asarray(p1, float) + t ** 2 * np.asarray(p2, float)
            self.cur.extend(map(tuple, q))

        def _closePath(self):
            if len(self.cur) > 2:
                self.polys.append(np.array(self.cur, float))
            self.cur = []

        _endPath = _closePath

    x, chars = 0.0, []
    for ch in s:
        g = cmap[ord(ch)]
        pen = Flat()
        gs[g].draw(pen)
        chars.append([np.column_stack([x + p[:, 0] * k, -p[:, 1] * k]) for p in pen.polys])
        x += hmtx[g][0] * k + track
    return chars, x - track


# ---- the camera's path ---------------------------------------------------------------------------------------------
class CamPath:
    """Keyframes (t, cx, cy, zoom); eased between each pair, zoom interpolated in log space."""

    def __init__(self, keys):
        self.keys = sorted(keys)

    def at(self, t):
        k = self.keys
        if t <= k[0][0]:
            return Cam(*k[0][1:])
        if t >= k[-1][0]:
            return Cam(*k[-1][1:])
        i = max(j for j in range(len(k)) if k[j][0] <= t)
        a, b = k[i], k[i + 1]
        u = ease(ramp(t, a[0], b[0]))
        return Cam(lerp(a[1], b[1], u), lerp(a[2], b[2], u), math.exp(lerp(math.log(a[3]), math.log(b[3]), u)))


# ---- glyphs --------------------------------------------------------------------------------------------------------
class Glyph:
    """One exact glyph (letter or mark): its polygons in em units, y up."""

    def __init__(self, contours, bbox, kind="letter", char=""):
        self.polys = [flatten(c) for c in contours]
        self.bbox = bbox
        self.kind, self.char = kind, char
        self.outline = union(self.polys)

    @property
    def center(self):
        b = self.bbox
        return ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)


def place(polys, ox, base, em):
    """em-unit polygons (y up) to world: left edge ox, baseline base."""
    out = []
    for p in polys:
        q = np.empty_like(p)
        q[:, 0] = ox + p[:, 0] * em
        q[:, 1] = base - p[:, 1] * em
        out.append(q)
    return out


def xform(polys, fn):
    return [fn(p) for p in polys]


def about(polys, c, s=1.0, dx=0.0, dy=0.0):
    """Scale polygons about the point c, then move them."""
    return [np.column_stack([(p[:, 0] - c[0]) * s + c[0] + dx, (p[:, 1] - c[1]) * s + c[1] + dy]) for p in polys]


def bbox_of(polys):
    a = np.vstack(polys)
    return a[:, 0].min(), a[:, 1].min(), a[:, 0].max(), a[:, 1].max()


# ---- the frame -----------------------------------------------------------------------------------------------------
class Patch:
    __slots__ = ("a", "x0", "y0")

    def __init__(self, a, x0, y0):
        self.a, self.x0, self.y0 = a, x0, y0


def _box(b, pad):
    x0 = max(0, int(math.floor(b[0] - pad)))
    y0 = max(0, int(math.floor(b[1] - pad)))
    x1 = min(W, int(math.ceil(b[2] + pad)))
    y1 = min(H, int(math.ceil(b[3] + pad)))
    return x0, y0, x1, y1


def _raster(box, fn, mode="L"):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        return None
    im = Image.new(mode, (w * SS, h * SS), 0)
    fn(ImageDraw.Draw(im), lambda p: [((x - x0) * SS, (y - y0) * SS) for x, y in p], im)
    a = np.asarray(im, np.float32)
    if mode == "1":
        a = a.astype(np.float32)
    else:
        a = a / 255.0
    return Patch(a.reshape(h, SS, w, SS).mean(axis=(1, 3)), x0, y0)


class Frame:
    """A display list for one frame. Shapes are rasterized at once; glow sources are collected per color and
    turned into halftone dots under all shapes when the frame is finished."""

    def __init__(self, cam, background):
        self.cam = cam
        self.bg = background
        self.layers = []                          # (patch, color, alpha) in draw order
        self.glows = {}                           # key -> dict(src, color, ...)
        self.soft = []                            # (patch, color, sigma, alpha) soft glows, under shapes

    # -- coordinates
    def S(self, screen):
        return SCREEN if screen else self.cam

    def lw(self, width, screen=False):
        return width if screen else max(1.0, width * self.cam.zoom)

    # -- primitives
    def fill(self, polys, color, alpha=1.0, glow=None, soft=None, screen=False, glow_amount=None):
        """Even-odd fill of world polygons. glow=(key, color, strength, sigma) adds them to a halftone source, by
        glow_amount (the alpha unless given); soft=(color, sigma, alpha) a soft glow. Alpha 0 with a glow_amount
        draws the glow alone."""
        if (alpha <= 0.003 and not glow_amount) or not polys:
            return None
        cam = self.S(screen)
        sp = [cam.pts(p) for p in polys]
        b = bbox_of(sp)
        if b[2] < 0 or b[0] > W or b[3] < 0 or b[1] > H:
            return None

        def fn(d, tr, im):
            acc = None
            for p in sp:
                m = Image.new("1", im.size, 0)
                ImageDraw.Draw(m).polygon(tr(p), fill=1)
                acc = np.asarray(m) if acc is None else (acc ^ np.asarray(m))
            im.paste(Image.fromarray((acc * 255).astype(np.uint8)))

        pt = _raster(_box(b, 2), fn)
        return self._add(pt, color, alpha, glow, soft, glow_amount)

    def _add(self, pt, color, alpha, glow, soft, glow_amount):
        if pt is None:
            return None
        if alpha > 0.003:
            self.layers.append((pt, color, alpha))
        if glow:
            self.glow_add(pt, *glow, amount=alpha if glow_amount is None else glow_amount)
        if soft and soft[2] > 0.003:
            self.soft.append((pt, soft[0], soft[1], soft[2]))
        return pt

    def stroke(self, lines, color, width=1.7, alpha=1.0, glow=None, screen=False, dash=None, glow_amount=None):
        """Polylines (world), round joins. dash=(on, off) in world units."""
        if alpha <= 0.003 and not glow_amount:
            return None
        cam = self.S(screen)
        sp = [cam.pts(l) for l in lines if len(l) > 1]
        if dash:
            sp = [seg for l in sp for seg in _dash(l, dash[0] * (1 if screen else cam.zoom), dash[1] * (1 if screen else cam.zoom))]
        if not sp:
            return None
        b = bbox_of(sp)
        if b[2] < -20 or b[0] > W + 20 or b[3] < -20 or b[1] > H + 20:
            return None
        lw = self.lw(width, screen)

        def fn(d, tr, im):
            r = lw * SS / 2
            for p in sp:
                q = tr(p)
                d.line(q, fill=255, width=max(1, int(round(lw * SS))), joint="curve")
                for e in (q[0], q[-1]):
                    d.ellipse([e[0] - r, e[1] - r, e[0] + r, e[1] + r], fill=255)

        pt = _raster(_box(b, lw + 2), fn)
        return self._add(pt, color, alpha, glow, None, glow_amount)

    def dot(self, xy, r, color, alpha=1.0, glow=None, soft=None, screen=False):
        cam = self.S(screen)
        x, y = cam.pt(*xy)
        rr = r if screen else max(0.6, r * cam.zoom)

        def fn(d, tr, im):
            (cx, cy), = tr([(x, y)])
            d.ellipse([cx - rr * SS, cy - rr * SS, cx + rr * SS, cy + rr * SS], fill=255)

        pt = _raster(_box((x - rr, y - rr, x + rr, y + rr), 2), fn)
        return self._add(pt, color, alpha, glow, soft, None)

    def text(self, xy, s, fname, px, color, alpha=1.0, anchor="la", track=0.0, screen=False, glow=None, soft=None):
        """Text at a world point; track in px at zoom 1. anchor as PIL's, for the whole run."""
        if alpha <= 0.003 or not s:
            return None
        cam = self.S(screen)
        z = 1.0 if screen else cam.zoom
        f = font(fname, px * z)
        x, y = cam.pt(*xy)
        widths = [f.getlength(ch) / SS for ch in s]
        total = sum(widths) + track * z * (len(s) - 1)
        asc, desc = f.getmetrics()
        asc, desc = asc / SS, desc / SS
        if anchor[0] == "m":
            x -= total / 2
        elif anchor[0] == "r":
            x -= total
        top = {"a": y, "t": y, "m": y - (asc + desc) / 2, "s": y - asc, "b": y - asc - desc}[anchor[1]]
        b = (x, top, x + total, top + asc + desc)

        def fn(d, tr, im):
            cx = x
            for ch, wd in zip(s, widths):
                (px_, py_), = tr([(cx, top)])
                d.text((px_, py_), ch, font=f, fill=255)
                cx += wd + track * z

        pt = _raster(_box(b, 4), fn)
        return self._add(pt, color, alpha, glow, soft, None)

    def text_width(self, s, fname, px, track=0.0):
        f = font(fname, px)
        return sum(f.getlength(ch) / SS for ch in s) + track * (len(s) - 1)

    # -- glow
    def glow_add(self, pt, key, color, strength=1.0, sigma=5.0, amount=1.0):
        g = self.glows.setdefault(key, dict(src=np.zeros((H, W), np.float32), color=color, strength=strength,
                                            sigma=sigma))
        g["src"][pt.y0:pt.y0 + pt.a.shape[0], pt.x0:pt.x0 + pt.a.shape[1]] += pt.a * amount

    # -- finish
    def render(self):
        img = self.bg.copy()
        occupied = np.zeros((H, W), np.float32)
        for pt, color, alpha in self.layers:
            sl = (slice(pt.y0, pt.y0 + pt.a.shape[0]), slice(pt.x0, pt.x0 + pt.a.shape[1]))
            occupied[sl] = np.maximum(occupied[sl], pt.a * min(1.0, alpha * 1.4))
        for key, g in self.glows.items():
            _halftone(img, np.minimum(g["src"], 1.0), occupied, g["color"], g["strength"], g["sigma"], self.cam)
        for pt, color, sigma, alpha in self.soft:
            _soft(img, pt, color, sigma, alpha)
        for pt, color, alpha in self.layers:
            sl = (slice(pt.y0, pt.y0 + pt.a.shape[0]), slice(pt.x0, pt.x0 + pt.a.shape[1]))
            a = (pt.a * alpha)[..., None]
            img[sl] = img[sl] * (1 - a) + np.asarray(color, np.float32) * a
        return np.clip(img + 0.5, 0, 255).astype(np.uint8)


def _dash(poly, on, off):
    s = arclen(poly)
    out, L = [], 0.0
    period = on + off
    while L < s[-1]:
        a, b = L, min(L + on, s[-1])
        seg = _between(poly, s, a, b)
        if len(seg) > 1:
            out.append(seg)
        L += period
    return out


def _between(poly, s, a, b):
    def at(L):
        k = min(len(s) - 1, max(1, int(np.searchsorted(s, L))))
        f = (L - s[k - 1]) / max(1e-9, s[k] - s[k - 1])
        return poly[k - 1] + (poly[k] - poly[k - 1]) * f
    inner = poly[(s > a) & (s < b)]
    return np.vstack([at(a)[None], inner, at(b)[None]])


def _halftone(img, src, occupied, color, strength, sigma, cam, cell=5.0, gamma=0.8, alpha=0.6):
    ys, xs = np.nonzero(src > 0.004)
    if len(ys) == 0:
        return
    pad = int(3 * sigma * max(1.0, cam.zoom)) + 8
    y0, y1 = max(0, ys.min() - pad), min(H, ys.max() + pad)
    x0, x1 = max(0, xs.min() - pad), min(W, xs.max() + pad)
    crop = src[y0:y1, x0:x1]
    sig = sigma * max(0.35, min(1.6, cam.zoom))
    g = gaussian_filter(crop, sig)
    c = cell * cam.zoom                                       # the grid is fixed to the canvas
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    wx = (xx + 0.5 - CX) / cam.zoom + cam.cx
    wy = (yy + 0.5 - CY) / cam.zoom + cam.cy
    cxw = (np.floor(wx / cell) + 0.5) * cell
    cyw = (np.floor(wy / cell) + 0.5) * cell
    sx = (cxw - cam.cx) * cam.zoom + CX
    sy = (cyw - cam.cy) * cam.zoom + CY
    ix = np.clip(np.round(sx - 0.5).astype(int) - x0, 0, x1 - x0 - 1)
    iy = np.clip(np.round(sy - 0.5).astype(int) - y0, 0, y1 - y0 - 1)
    v = np.clip(g[iy, ix], 0, None) ** gamma * strength
    inside = occupied[y0:y1, x0:x1][iy, ix] > 0.3
    r = 0.5 * c * np.sqrt(np.minimum(1.0, v)) * 0.9
    r = np.where((v < 0.05) | inside, 0.0, r)
    d = np.hypot(xx + 0.5 - sx, yy + 0.5 - sy)
    cov = np.clip(r - d + 0.5, 0, 1) * np.clip(r * 2, 0, 1)    # no dot where r is 0; small dots stay faint
    if c < 2.0:                                               # dots smaller than a pixel: their area, spread
        cov = np.clip(np.pi * r * r / (c * c), 0, 1) * (r > 0)
    a = (cov * alpha)[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + np.asarray(color, np.float32) * a


def _soft(img, pt, color, sigma, alpha):
    pad = int(3 * sigma) + 2
    h, w = pt.a.shape
    y0, x0 = max(0, pt.y0 - pad), max(0, pt.x0 - pad)
    y1, x1 = min(H, pt.y0 + h + pad), min(W, pt.x0 + w + pad)
    big = np.zeros((y1 - y0, x1 - x0), np.float32)
    big[pt.y0 - y0:pt.y0 - y0 + h, pt.x0 - x0:pt.x0 - x0 + w] = pt.a
    g = gaussian_filter(big, sigma)
    m = g.max()
    if m <= 1e-6:
        return
    a = (g / m * alpha)[..., None]
    img[y0:y1, x0:x1] = img[y0:y1, x0:x1] * (1 - a) + np.asarray(color, np.float32) * a


# ---- the canvas ----------------------------------------------------------------------------------------------------
def background():
    """the series' canvas: #0D0F10 with a faint low-frequency mottle, a fixed fine texture and a soft vignette."""
    rng = np.random.default_rng(1974)
    mott = gaussian_filter(rng.normal(0, 1, (H, W)), 38)
    mott = mott / np.abs(mott).max()
    fine = gaussian_filter(rng.normal(0, 1, (H, W)), 0.7)
    fine = fine / np.abs(fine).max()
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.hypot((xx - W / 2) / (W * 0.62), (yy - H * 0.45) / (H * 0.62))
    vig = 1 - 0.28 * np.clip(r - 0.35, 0, 1) ** 1.5
    img = np.empty((H, W, 3), np.float32)
    for i, c in enumerate(BG):
        img[..., i] = (c + 2.2 * mott + 0.9 * fine) * vig
    return img


# ---- the pen -------------------------------------------------------------------------------------------------------
def pen(fr, tip, alpha=1.0, angle=58.0, length=300.0):
    """the series' pen: a slim line drawing of a stylus whose nib is at the tip, the body up and to the right."""
    if alpha <= 0.01:
        return
    a = math.radians(angle)
    ux, uy = math.cos(a), -math.sin(a)                       # along the body, away from the tip
    nx, ny = -uy, ux
    tx, ty = tip
    cone, half = 30.0, 5.5
    sh = (tx + ux * cone, ty + uy * cone)
    far = (tx + ux * length, ty + uy * length)
    body = [np.array([(sh[0] + nx * half, sh[1] + ny * half), (far[0] + nx * half, far[1] + ny * half)]),
            np.array([(sh[0] - nx * half, sh[1] - ny * half), (far[0] - nx * half, far[1] - ny * half)]),
            np.array([(sh[0] + nx * half, sh[1] + ny * half), (tx, ty), (sh[0] - nx * half, sh[1] - ny * half)]),
            np.array([(sh[0] + nx * half, sh[1] + ny * half), (sh[0] - nx * half, sh[1] - ny * half)])]
    fr.stroke(body, INK, 1.4, 0.85 * alpha)
    fr.dot(tip, 2.6, GOLD_HOT, alpha, glow=("pen", GOLD, 3.0, 4.0), soft=(GOLD_HOT, 6, 0.5 * alpha))


# ---- labels --------------------------------------------------------------------------------------------------------
MONO = "IBMPlexMono-Regular.ttf"
MONO_LIGHT = "IBMPlexMono-Light.ttf"


def label(fr, xy, s, u=1.0, px=15, alpha=0.8, anchor="la", color=LABEL, screen=False, fname=MONO):
    """Monospace capitals, tracked +2, typed on as u goes from 0 to 1."""
    if u <= 0:
        return
    n = max(1, int(math.ceil(len(s) * min(1.0, u))))
    fr.text(xy, s[:n] if anchor[0] == "l" else s, fname, px, color, alpha * (1 if anchor[0] == "l" else u),
            anchor=anchor, track=2.0, screen=screen)


def leader(fr, pts, u, color=LABEL, alpha=0.7, width=1.2, screen=False, dash=None, glow=None):
    """A hairline drawn on along its points as u goes from 0 to 1."""
    if u <= 0:
        return
    part, _ = partial(np.asarray(pts, float), u)
    fr.stroke([part], color, width, alpha, screen=screen, dash=dash, glow=glow)


def corners(fr, box, u=1.0, arm=26, color=LABEL, alpha=0.55, width=1.3, screen=False):
    l, t, r, b = box
    for x, y, sx, sy in ((l, t, 1, 1), (r, t, -1, 1), (l, b, 1, -1), (r, b, -1, -1)):
        a = arm * u
        if a > 0.5:
            fr.stroke([np.array([(x, y + sy * a), (x, y), (x + sx * a, y)])], color, width, alpha, screen=screen)


def ring(fr, c, r, u=1.0, color=INK, alpha=0.8, width=1.4, start=-90.0, screen=False, dash=None, n=96):
    if u <= 0:
        return
    th = np.radians(start + np.linspace(0, 360 * u, max(2, int(n * u) + 1)))
    fr.stroke([np.column_stack([c[0] + r * np.cos(th), c[1] + r * np.sin(th)])], color, width, alpha, screen=screen,
              dash=dash)


def rect_path(l, t, r, b, radius=0.0):
    if radius <= 0:
        return np.array([(r, t), (r, b), (l, b), (l, t), (r, t)], float)
    pts = []
    for (cx, cy, a0) in ((r - radius, t + radius, -90), (r - radius, b - radius, 0), (l + radius, b - radius, 90),
                         (l + radius, t + radius, 180)):
        th = np.radians(np.linspace(a0, a0 + 90, 7))
        pts.extend(zip(cx + radius * np.cos(th), cy + radius * np.sin(th)))
    pts.append(pts[0])
    return np.array(pts, float)
