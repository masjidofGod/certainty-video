"""certainty new <series> <episode id>: start an episode from templates/episode, in your workspace.

    certainty new certainty ep02-sura-96      ->  stories/certainty/ep02-sura-96/

The id is lowercase letters, digits and hyphens. {{SERIES}} and {{EPISODE_ID}} in the templates are filled in.
"""
import re
import shutil

from .settings import TEMPLATES, workspace


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: certainty new <series> <episode id>")
    series, eid = argv
    for v in (series, eid):
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", v):
            raise SystemExit(f"'{v}': use lowercase letters, digits and hyphens")
    dest = workspace(required=True) / "stories" / series / eid
    if dest.exists():
        raise SystemExit(f"{dest} exists")
    shutil.copytree(TEMPLATES / "episode", dest)
    for p in dest.rglob("*"):
        if p.is_file() and p.suffix in (".md", ".toml", ".json", ".py"):
            t = p.read_text(encoding="utf-8")
            p.write_text(t.replace("{{EPISODE_ID}}", eid).replace("{{SERIES}}", series), encoding="utf-8")
    print(f"Started {dest}")
    print("Next: ask Claude Code to take this episode through its steps with the certainty:studio skill.")
    return 0
