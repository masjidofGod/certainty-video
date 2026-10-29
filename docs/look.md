# The look

One continuous dark canvas, 1080 x 1920, drawn by a pen in thin warm-white lines, with a halftone glow around what
matters. No cuts: each spoken line changes something in the drawing, and the camera moves only to follow it.
`engine/canvas.py` is the look as code; use its colors and functions rather than new ones.

## Meaning of color

| Treatment | Means |
| --- | --- |
| warm-white outline (`INK`) | written, not yet counted |
| gold fill (`GOLD`), the newest brightest (`GOLD_HOT`) | counted |
| blue (`BLUE`) | set aside (marks that are not letters, a place left empty) |
| grey monospace labels (`LABEL`, IBM Plex Mono) | names and addresses; labels never count |

## Type

- Arabic: Amiri Quran, the font's own outlines, shaped by HarfBuzz from the data.
- Labels and numbers: IBM Plex Mono (Light for large numbers).
- Captions: Poppins, the spoken word bold and bright, the rest regular; two lines at most, low in the frame.
- Translations: Source Serif 4 Italic, under the Arabic.

## Motion

- The pen writes Arabic right to left, stroke by stroke, and lifts away.
- A count: each letter turns from outline to gold on its click, the newest brightest; the camera holds still.
- After a peak, quiet: fewer things on screen, not more.

## Layout

Centered on x 540, balanced left and right, inside the safe area (docs/rules.md, rule 11). Leave counters and
labels their own space; nothing overlaps.
