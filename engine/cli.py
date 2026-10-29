"""certainty: one command for the whole pipeline. Run `certainty` for the list."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
for _s in (sys.stdout, sys.stderr):          # Arabic and curly quotes print on any console, Windows included
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

USAGE = """certainty <command> ...

  setup [--again]                        the kit's Python packages (made on first use anyway)
  init [folder]                          make a folder a workspace: certainty.toml, .env, data/, stories/
  doctor                                 what the kit needs, and whether it is here
  demo                                   build and render the demo episode into demo/ (no credits, no data needed)
  new <series> <id>                      start an episode in stories/<series>/<id>/
  test                                   the kit's own tests
  data check                             check your Quran data file (docs/data-format.md)
  count letters|words|verses|letter ...  count from the data (letters 1:1, words 96:1-5, verses 96, letter ب 1)
  verify <episode>/claims.toml           every claim against the data; exit 1 if any differs
  glyphs verse|phrase ...                exact Arabic outlines for a timeline (verse 1:1 out.json; phrase 74:30 0 2 out.json)
  voice <episode> [--yes]                voice takes with ElevenLabs (a dry run without --yes)
  music <plan.json> [--take N] [--yes]   a music cue with ElevenLabs (a dry run without --yes)
  whisper <episode> [--model medium.en]  the words and their times in every new take (Whisper)
  takes <episode>                        check the takes word for word, pick one per line
  clock <episode>                        the clock: lines, words, the count
  mix <episode>                          the mix on the clock
  stills <episode> <seconds> ...         still frames for review
  film <episode> [--draft]               the film (or a 540 x 960 draft)
  check <film.mp4> [--frames N]          the delivery check
  safe <film.mp4> [--profile all]        nothing drawn under the platforms' buttons and captions
  cover <episode>                        the cover and its platform copies
  package <episode>                      the posting folder
"""


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, argv = sys.argv[1], sys.argv[2:]
    if cmd == "new":
        from engine import newep
        return newep.main(argv)
    if cmd == "test":
        import unittest
        root = pathlib.Path(__file__).resolve().parents[1]
        suite = unittest.defaultTestLoader.discover(str(root / "tests"))
        return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
    if cmd == "setup":
        print("The kit's Python packages are ready (`certainty setup --again` makes them afresh).")
        return 0
    if cmd == "init":
        from engine import workspace
        return workspace.main(argv)
    if cmd == "doctor":
        from engine import doctor
        return doctor.main(argv)
    if cmd == "data":
        from engine import data
        return data.main(argv)
    if cmd in ("count", "verify"):
        from engine import verify
        return verify.main(argv, verify=cmd == "verify")
    if cmd == "glyphs":
        from engine import glyphs
        return glyphs.main(argv)
    if cmd in ("voice", "music"):
        from engine import eleven
        return getattr(eleven, cmd)(argv)
    if cmd in ("whisper", "takes"):
        from engine import takes
        return (takes.transcribe if cmd == "whisper" else takes.main)(argv)
    if cmd == "clock":
        from engine import clock
        return clock.main(argv)
    if cmd == "mix":
        from engine import mix
        return mix.main(argv)
    if cmd in ("stills", "film"):
        from engine import render
        return getattr(render, cmd)(argv)
    if cmd == "check":
        from engine import deliver
        return deliver.main(argv)
    if cmd == "safe":
        from engine import safe_areas
        return safe_areas.main(argv)
    if cmd == "cover":
        from engine import cover
        return cover.main(argv)
    if cmd == "package":
        from engine import package
        return package.main(argv)
    if cmd == "demo":
        from engine import demo
        return demo.main(argv)
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main() or 0)
