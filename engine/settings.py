"""Where things are: the kit (engine, fonts, templates; read-only, replaced on updates) and your workspace.

A workspace is any folder you make episodes in: `certainty init` makes one (certainty.toml, .env, data/, stories/).
Every command finds it by looking for certainty.toml in the folder it runs in, then in the folders above;
CERTAINTY_WORKSPACE names one directly. Keys live in the workspace's .env; they are read here and never printed.
"""
import os
import pathlib
import tomllib

KIT = pathlib.Path(__file__).resolve().parents[1]
FONTS = KIT / "fonts"
TEMPLATES = KIT / "templates"
WORKSPACE_FILE = "certainty.toml"
SAMPLE_DATA = KIT / "tests" / "fixtures" / "quran-sample.json"


def workspace(required=False):
    raw = os.environ.get("CERTAINTY_WORKSPACE")
    if raw:
        return pathlib.Path(raw).expanduser().resolve()
    here = pathlib.Path.cwd().resolve()
    for d in (here, *here.parents):
        if (d / WORKSPACE_FILE).exists():
            return d
    if required:
        raise SystemExit(f"No workspace here (no {WORKSPACE_FILE} in this folder or above it). "
                         "Run `certainty init` in the folder for your series.")
    return None


def settings():
    ws = workspace()
    if ws and (ws / WORKSPACE_FILE).exists():
        with open(ws / WORKSPACE_FILE, "rb") as fh:
            return tomllib.load(fh)
    return {}


def quran_data():
    """The Quran data file: CERTAINTY_QURAN_DATA if set, else certainty.toml's quran_data (relative to the workspace)."""
    raw = os.environ.get("CERTAINTY_QURAN_DATA") or settings().get("quran_data", "")
    if not raw:
        raise SystemExit(f"No Quran data file set: put its path in {WORKSPACE_FILE} (quran_data = \"...\"). "
                         "See docs/data-format.md.")
    p = pathlib.Path(os.path.expanduser(raw))
    if p.is_absolute():
        return p
    return (workspace() or pathlib.Path.cwd()) / p


def env(key):
    """A value from the environment or from the workspace's .env, without overriding the environment and without
    printing it."""
    if os.environ.get(key):
        return os.environ[key]
    ws = workspace()
    p = ws / ".env" if ws else None
    if p and p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == key:
                    return v.strip().strip("'\"")
    return ""
