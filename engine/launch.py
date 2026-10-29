"""Start the kit: make sure its Python environment is ready, then run the command in it.

bin/certainty (and bin\\certainty.cmd) run this with any Python 3.12 or 3.13. The environment holds the pinned
packages, each a prebuilt wheel checked against the hashes in requirements.txt, so nothing is compiled and nothing
unexpected is installed. It is made on first use (about a minute) and lives outside the kit, so updating the kit or
working in a second folder reuses it:

    Windows   %LOCALAPPDATA%\\certainty-kit
    macOS     ~/Library/Application Support/certainty-kit
    Linux     $XDG_DATA_HOME/certainty-kit (~/.local/share/certainty-kit)

CERTAINTY_HOME moves it. `certainty setup --again` makes it afresh.
"""
import hashlib
import os
import pathlib
import shutil
import subprocess
import sys
import venv

KIT = pathlib.Path(__file__).resolve().parents[1]
REQUIREMENTS = KIT / "requirements.txt"


def home():
    if os.environ.get("CERTAINTY_HOME"):
        return pathlib.Path(os.environ["CERTAINTY_HOME"]).expanduser()
    if os.name == "nt":
        base = pathlib.Path(os.environ.get("LOCALAPPDATA") or pathlib.Path.home() / "AppData" / "Local")
    elif sys.platform == "darwin":
        base = pathlib.Path.home() / "Library" / "Application Support"
    else:
        base = pathlib.Path(os.environ.get("XDG_DATA_HOME") or pathlib.Path.home() / ".local" / "share")
    return base / "certainty-kit"


def env_dir():
    """One environment per Python version and set of pinned packages."""
    tag = hashlib.sha256(REQUIREMENTS.read_bytes()).hexdigest()[:10]
    return home() / f"python{sys.version_info[0]}{sys.version_info[1]}-{tag}"


def env_python(d):
    return d / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def ready(again=False):
    d = env_dir()
    if (d / ".ready").exists() and not again:
        return env_python(d)
    print(f"Setting up the kit's Python packages in {d} (one time, about a minute) ...", flush=True)
    venv.EnvBuilder(with_pip=True, clear=True).create(d)
    r = subprocess.run([str(env_python(d)), "-m", "pip", "install", "--disable-pip-version-check", "-q",
                        "--only-binary=:all:", "--require-hashes", "-r", str(REQUIREMENTS)])
    if r.returncode:
        raise SystemExit("Installing the packages failed (above). Check the internet connection, then run "
                         "`certainty setup` again.")
    (d / ".ready").write_text(f"{sys.version.split()[0]}\n", encoding="utf-8")
    print("The kit's Python is ready.", flush=True)
    return env_python(d)


def main():
    if sys.version_info[:2] not in ((3, 12), (3, 13)):
        sys.exit(f"The kit needs Python 3.12 or 3.13; this is {sys.version.split()[0]}. Install Python 3.12 from "
                 "python.org (Windows: winget install --id Python.Python.3.12).")
    args = sys.argv[1:]
    if args[:1] == ["setup"]:
        ready(again="--again" in args)
        if not shutil.which("ffmpeg"):
            print("ffmpeg is not on PATH yet. Windows: winget install --id Gyan.FFmpeg (then open a new terminal); "
                  "macOS: brew install ffmpeg; Linux: your package manager.")
        print("Next: `certainty init` in the folder for your series, then `certainty doctor`.")
        return 0
    py = ready()
    try:
        return subprocess.run([str(py), "-I", str(KIT / "engine" / "cli.py"), *args]).returncode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
