"""certainty init [folder]: make a folder a workspace (default: the folder you are in).

Writes certainty.toml, .env (for your keys), data/, stories/, a CLAUDE.md with the series' rules for Claude Code, and
a .gitignore that keeps the keys, the data and the media out of git. Never overwrites a file that is there.
"""
import pathlib
import shutil

from .settings import TEMPLATES, WORKSPACE_FILE

FILES = [("certainty.toml", WORKSPACE_FILE), ("env.example", ".env"), ("gitignore.txt", ".gitignore"),
         ("CLAUDE.md", "CLAUDE.md"), ("data/README.md", "data/README.md"), ("stories/README.md", "stories/README.md")]


def main(argv):
    ws = pathlib.Path(argv[0] if argv else ".").expanduser().resolve()
    ws.mkdir(parents=True, exist_ok=True)
    made = []
    for src, dst in FILES:
        p = ws / dst
        if p.exists():
            continue
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TEMPLATES / "workspace" / src, p)
        made.append(dst)
    print(f"Workspace: {ws}" + (f" (made {', '.join(made)})" if made else " (already set up)"))
    print("Next: put your Quran data file at data/quran.json (docs/data-format.md in the kit), your ElevenLabs key "
          "in .env when you record, then `certainty doctor`. `certainty demo` runs without either.")
    return 0
