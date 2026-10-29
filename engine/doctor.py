"""certainty doctor: what the kit needs, and whether it is here. Never prints a key."""
import importlib
import os
import shutil
import sys

from .settings import FONTS, KIT, WORKSPACE_FILE, env, quran_data, workspace


def main(argv):
    ok = True

    def line(good, what, fix=""):
        nonlocal ok
        ok &= good is not False
        tag = {True: "ok      ", False: "MISSING ", None: "optional"}[good]
        print(f"  {tag} {what}" + (f"  ({fix})" if fix and good is not True else ""))

    ws = workspace()
    print(f"The kit at {KIT}")
    print(f"Python {sys.version.split()[0]} at {sys.prefix}")
    line(sys.version_info[:2] in ((3, 12), (3, 13)), f"Python {sys.version.split()[0]}", "Python 3.12 or 3.13")
    for mod in ("numpy", "scipy", "PIL", "fontTools", "uharfbuzz", "pathops"):
        try:
            importlib.import_module(mod)
            line(True, f"package {mod}")
        except ImportError:
            line(False, f"package {mod}", "certainty setup --again")
    fix = ("winget install --id Gyan.FFmpeg, then open a new terminal" if os.name == "nt" else
           "brew install ffmpeg" if sys.platform == "darwin" else "your package manager: ffmpeg")
    for tool in ("ffmpeg", "ffprobe"):
        line(bool(shutil.which(tool)), tool, fix)
    for f in ("AmiriQuran-Regular.ttf", "IBMPlexMono-Light.ttf", "IBMPlexMono-Regular.ttf", "Poppins-SemiBold.ttf",
              "Poppins-Regular.ttf"):
        line((FONTS / f).exists(), f"font {f}")
    line(ws is not None, f"workspace {ws}" if ws else f"workspace ({WORKSPACE_FILE} here or above)",
         "certainty init, in the folder for your series")
    try:
        p = quran_data()
        if p.exists():
            from . import data
            problems, summary = data.check()
            line(not problems, f"Quran data {p.name}: {summary.get('records', 0)} records, {summary.get('suras', 0)} suras",
                 "; ".join(problems) or "certainty data check")
        else:
            line(False, f"Quran data at {p}", "docs/data-format.md; `certainty demo` runs without it")
    except SystemExit as e:
        line(False, "Quran data", str(e))
    from .takes import INSTALL, whisper_command
    line(True if whisper_command() else None, "Whisper (to check voice takes word for word)", INSTALL)
    line(True if env("ELEVENLABS_API_KEY") else None, "ELEVENLABS_API_KEY in .env (voice and music)", "only needed to record")
    line(True if env("ELEVENLABS_VOICE_ID") else None, "ELEVENLABS_VOICE_ID in .env", "only needed to record")
    line(True if shutil.which("claude") else None, "Claude Code (the skills run in it)", "https://claude.com/claude-code")
    print("Ready." if ok else "Fix the MISSING lines, then run the doctor again.")
    return 0 if ok else 1
