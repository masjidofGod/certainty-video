"""An episode folder: its settings (episode.toml) and its spoken lines (script.md).

script.md's script table has one row per line, the spoken words in double quotes in the second column:

    | L1 | "Count the letters of the first verse." | delivery | picture | labels |
    | L3 | "Nineteen." (beat) "Every one." | ... |

Inside the spoken words, single quotes mark a quotation ('Over it is nineteen.'); captions show them as curly
double quotes. "(beat)" is a pause the clock makes at the take's own silence (episode.toml [clock] beats).
"""
import pathlib
import re
import tomllib


class Episode:
    def __init__(self, folder):
        self.dir = pathlib.Path(folder).resolve()
        if not (self.dir / "episode.toml").exists():
            raise SystemExit(f"{self.dir} has no episode.toml (make one with certainty new)")
        with open(self.dir / "episode.toml", "rb") as fh:
            self.cfg = tomllib.load(fh)
        self.fps = self.cfg.get("fps", 24)

    def path(self, *parts):
        return self.dir.joinpath(*parts)

    def lines(self):
        """{line number: spoken text as written in the script} in order."""
        p = self.path("script.md")
        if not p.exists():
            return {}
        out = {}
        for m in re.finditer(r'^\| L(\d+) \| (.+?) \| ', p.read_text(encoding="utf-8"), re.M):
            cell = m.group(2).replace("(beat)", " ")
            parts = re.findall(r'"(.*?)"', cell)
            if parts:
                out[int(m.group(1))] = " ".join(parts)
        return dict(sorted(out.items()))

    def cue(self, n):
        return f"{self.cfg.get('id', self.dir.name)}-L{n:02d}"


def caption(s):
    """Apostrophes typographic; the script's single quotes become curly double quotation marks."""
    out = []
    for i, ch in enumerate(s):
        if ch != "'":
            out.append(ch)
            continue
        prev, nxt = s[i - 1] if i else " ", s[i + 1] if i + 1 < len(s) else " "
        out.append("’" if prev.isalpha() and nxt.isalpha() else ("“" if nxt.isalpha() and not prev.isalnum() else "”"))
    return "".join(out)


def spoken(s):
    """What the voice reads: the quotation marks dropped, GOD read as God."""
    s = re.sub(r"(?<![A-Za-z])'|'(?![A-Za-z])", "", s)
    return s.replace("GOD", "God")
