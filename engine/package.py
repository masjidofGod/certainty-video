"""The posting folder: the film, the covers, the captions file and the narration as text.

    certainty package <episode>

Copies out/film.mp4 and the covers byte for byte (never re-encoded) into <episode>/publish/, and writes the
captions file (the same cards and times as the ones in the picture) and the narration as plain text. The post copy
and the manifest (publish/README.md, publish/publish.json) are yours to fill in from the templates.
"""
import filecmp
import json
import shutil

from .episode import Episode
from .scenes import Captions


def main(argv):
    if not argv:
        raise SystemExit("usage: certainty package <episode>")
    ep = Episode(argv[0])
    pub = ep.path("publish")
    pub.mkdir(exist_ok=True)
    eid = ep.cfg.get("id", ep.dir.name)
    for src, dst in (("out/film.mp4", f"{eid}.mp4"), ("out/cover.png", f"{eid}-cover.png"),
                     ("out/cover-reels.jpg", "cover-reels-1080x1920.jpg"), ("out/cover-tiktok.jpg", "cover-tiktok-1080x1440.jpg")):
        s = ep.path(src)
        if not s.exists():
            print(f"  missing {src}: skipped")
            continue
        shutil.copyfile(s, pub / dst)
        assert filecmp.cmp(s, pub / dst, shallow=False)
        print(f"  {dst}")
    clock = json.load(open(ep.path("clock.json"), encoding="utf-8"))
    if clock["lines"]:
        (pub / f"{eid}.en.srt").write_text(Captions(clock).srt(), encoding="utf-8")
        (pub / f"{eid}.txt").write_text("\n".join(l["text"] for l in clock["lines"]) + "\n", encoding="utf-8")
        print(f"  {eid}.en.srt, {eid}.txt")
    print(f"publish folder: {pub}")
    return 0
