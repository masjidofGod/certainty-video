"""certainty demo: build the demo episode end to end, with no credits and no data of your own needed.

Copies the kit's examples/demo into demo/ in your workspace (or in the folder you are in), then: checks the data,
exports the Basmalah's outlines, verifies the claims, builds the clock, mixes the clicks, renders the film, and runs
the delivery check and the safe-area check. Ends with demo/out/film.mp4. Without a Quran data file of your own it
uses the kit's one-verse sample, which is all the demo needs.
"""
import os
import pathlib
import shutil
import subprocess
import sys

from .settings import KIT, SAMPLE_DATA, quran_data, workspace


def step(title, args, env):
    print(f"\n== {title}", flush=True)
    r = subprocess.run([sys.executable, "-I", str(KIT / "engine" / "cli.py")] + args, env=env)
    if r.returncode:
        raise SystemExit(f"demo stopped at: {title}")


def main(argv):
    demo = (workspace() or pathlib.Path.cwd()) / "demo"
    if not (demo / "episode.toml").exists():
        shutil.copytree(KIT / "examples" / "demo", demo, dirs_exist_ok=True)
    env = dict(os.environ)
    try:
        has_data = quran_data().exists()
    except SystemExit:
        has_data = False
    if not has_data:
        env["CERTAINTY_QURAN_DATA"] = str(SAMPLE_DATA)
        print("No Quran data file of yours yet: the demo uses the kit's one-verse sample (1:1).")
    step("Quran data", ["data", "check"], env)
    step("the Basmalah's outlines", ["glyphs", "verse", "1:1", str(demo / "art" / "basmala.json")], env)
    step("claims", ["verify", str(demo / "claims.toml")], env)
    step("clock", ["clock", str(demo)], env)
    step("mix", ["mix", str(demo)], env)
    step("film", ["film", str(demo)], env)
    step("delivery check", ["check", str(demo / "out" / "film.mp4")], env)
    step("safe areas", ["safe", str(demo / "out" / "film.mp4"), "--fps", "2"], env)
    print(f"\nThe demo is ready: {demo / 'out' / 'film.mp4'}")
    return 0
