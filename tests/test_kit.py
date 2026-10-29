"""The kit's own tests: certainty test. They use the one-verse sample in tests/fixtures and throwaway folders, so
they run anywhere and touch nothing of yours."""
import contextlib
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
import unittest
import wave
from unittest import mock

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ["CERTAINTY_QURAN_DATA"] = str(ROOT / "tests" / "fixtures" / "quran-sample.json")

from engine import clock, cover, data, eleven, episode, glyphs, mix, newep, package, takes, verify, workspace  # noqa: E402

# Stands in for Whisper: writes the JSON Whisper would for each take it is given.
FAKE_WHISPER = """import json, pathlib, sys
a = sys.argv[1:]
out = pathlib.Path(a[a.index("--output_dir") + 1])
out.mkdir(parents=True, exist_ok=True)
for f in a[:a.index("--model")]:
    words = [dict(word=" Nineteen", start=0.32, end=0.8), dict(word=" letters.", start=0.85, end=1.28)]
    (out / (pathlib.Path(f).stem + ".json")).write_text(json.dumps(dict(segments=[dict(words=words)])))
"""


def quietly(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(list(args))


class Data(unittest.TestCase):
    def test_sample_reads_clean(self):
        problems, summary = data.check()
        self.assertEqual(problems, [])
        self.assertEqual(summary["records"], 1)

    def test_basmalah_has_19_letters(self):
        self.assertEqual(len(data.letters(data.text("1:1"))), 19)
        self.assertEqual(verify.count("letters", verses="1:1"), 19)
        self.assertEqual(verify.count("words", verses="1:1"), 4)


class Arabic(unittest.TestCase):
    def test_verse_outlines(self):
        out = glyphs.export_verse("1:1")
        self.assertEqual(out["letters"], 19)
        self.assertEqual([len(w["letters"]) for w in out["words"]], [3, 4, 6, 6])
        self.assertTrue(all(w["marks"] for w in out["words"]))

    def test_phrase_outlines(self):
        out = glyphs.export_phrase("1:1", 0, 1)
        self.assertEqual(len(out["words"]), 2)
        self.assertGreater(out["space"], 0)


class Words(unittest.TestCase):
    def test_numbers_read_as_words(self):
        self.assertEqual(takes.norm_words("19 and 114, in the 1970s"),
                         "nineteen and one hundred fourteen in the nineteen seventies".split())
        self.assertEqual(takes.norm_words("Twenty-one. Every one."), ["twenty", "one", "every", "one"])

    def test_quotes(self):
        self.assertEqual(episode.caption("The verse says: 'In the name of GOD.' Let's count."),
                         "The verse says: “In the name of GOD.” Let’s count.")
        self.assertEqual(episode.spoken("The verse says: 'In the name of GOD.' Let's count."),
                         "The verse says: In the name of God. Let's count.")


class Demo(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.ep = self.tmp / "demo"
        shutil.copytree(ROOT / "examples" / "demo", self.ep, ignore=shutil.ignore_patterns("out", "art", "clock.json", "mix.wav"))
        (self.ep / "art").mkdir()
        json.dump(glyphs.export_verse("1:1"), open(self.ep / "art" / "basmala.json", "w", encoding="utf-8"), ensure_ascii=False)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_claims_match(self):
        self.assertTrue(all(r["ok"] for r in verify.check(self.ep / "claims.toml")))

    def test_clock_counts_every_letter(self):
        c = clock.build(episode.Episode(self.ep))
        clicks = c["count"]["clicks"]
        self.assertEqual(len(clicks), 19)
        self.assertEqual(clicks, sorted(clicks))
        self.assertGreater(c["count"]["numeral"], clicks[-1])
        self.assertEqual(c["frames_total"], round(c["end_s"] * 24))

    def test_a_frame_renders(self):
        c = clock.build(episode.Episode(self.ep))
        json.dump(c, open(self.ep / "clock.json", "w", encoding="utf-8"))
        import importlib.util
        spec = importlib.util.spec_from_file_location("demo_timeline", self.ep / "timeline.py")
        tl = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tl)
        img = tl.frame(int(c["count"]["numeral"] * 24) + 12)
        self.assertEqual(img.shape, (1920, 1080, 3))
        self.assertGreater(int(img.max()), 100)


class AfterTheVoice(unittest.TestCase):
    """An episode from its recorded take to the posting folder, with no credits and no Whisper, in a folder whose
    path has a space (as many Windows accounts do)."""

    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.ep = self.tmp / "my episode"
        (self.ep / "takes").mkdir(parents=True)
        (self.ep / "episode.toml").write_text('id = "t"\n[cover]\nheadline = ["COUNT IT"]\n', encoding="utf-8")
        (self.ep / "script.md").write_text('| L1 | "Nineteen letters." | | | |\n', encoding="utf-8")
        tone = 0.3 * 32767 * np.sin(2 * np.pi * 220 * np.arange(48000) / 48000)
        pad = np.zeros(14400)
        with wave.open(str(self.ep / "takes" / "t-L01_take1.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(48000)
            w.writeframes(np.concatenate([pad, tone, pad]).astype("<i2").tobytes())
        (self.tmp / "fake_whisper.py").write_text(FAKE_WHISPER, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_dry_runs_send_nothing(self):
        plan = self.ep / "music" / "M1.json"
        plan.parent.mkdir()
        plan.write_text(json.dumps(dict(model_id="music_v2_5", composition_plan=dict(chunks=[dict(
            text="kalimba", duration_ms=5000, positive_styles=[], negative_styles=[])]))), encoding="utf-8")
        self.assertEqual(quietly(eleven.voice, str(self.ep)), 0)
        self.assertEqual(quietly(eleven.music, str(plan)), 0)
        self.assertEqual(sorted(p.name for p in (self.ep / "takes").iterdir()), ["t-L01_take1.wav"])
        self.assertEqual(sorted(p.name for p in plan.parent.iterdir()), ["M1.json"])

    def test_takes_to_posting_folder(self):
        ep = str(self.ep)
        with mock.patch.object(takes, "whisper_command", return_value=[sys.executable, str(self.tmp / "fake_whisper.py")]):
            self.assertEqual(quietly(takes.transcribe, ep), 0)
        self.assertTrue((self.ep / "whisper" / "t-L01_take1.json").exists())
        self.assertEqual(quietly(takes.main, ep), 0)
        pick = json.load(open(self.ep / "picks.json", encoding="utf-8"))["picks"]["L01"]
        self.assertEqual(pick["take"], 1)
        self.assertAlmostEqual(pick["voiced"][0], 0.3, delta=0.05)
        self.assertAlmostEqual(pick["voiced"][1], 1.3, delta=0.05)
        self.assertEqual([t["w"] for t in pick["tokens"]], ["Nineteen", "letters."])
        json.dump(clock.build(episode.Episode(ep)), open(self.ep / "clock.json", "w", encoding="utf-8"))
        self.assertEqual(quietly(mix.main, ep), 0)
        self.assertTrue((self.ep / "mix.wav").exists())
        self.assertEqual(quietly(cover.main, ep), 0)
        self.assertEqual(Image.open(self.ep / "out" / "cover.png").size, (1080, 1920))
        self.assertEqual(Image.open(self.ep / "out" / "cover-tiktok.jpg").size, (1080, 1440))
        self.assertEqual(quietly(package.main, ep), 0)
        pub = self.ep / "publish"
        self.assertEqual((pub / "t-cover.png").read_bytes(), (self.ep / "out" / "cover.png").read_bytes())
        self.assertIn("Nineteen letters.", (pub / "t.en.srt").read_text(encoding="utf-8"))


class Workspace(unittest.TestCase):
    def setUp(self):
        self.tmp = pathlib.Path(tempfile.mkdtemp())
        self.ws = self.tmp / "my series"

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_init_then_new_episode(self):
        self.assertEqual(quietly(workspace.main, str(self.ws)), 0)
        for f in ("certainty.toml", ".env", ".gitignore", "CLAUDE.md", "data/README.md", "stories/README.md"):
            self.assertTrue((self.ws / f).exists(), f)
        (self.ws / ".env").write_text("ELEVENLABS_VOICE_ID=abc\n", encoding="utf-8")
        self.assertEqual(quietly(workspace.main, str(self.ws)), 0)          # a second init keeps your files
        self.assertIn("abc", (self.ws / ".env").read_text(encoding="utf-8"))
        with mock.patch.dict(os.environ, {"CERTAINTY_WORKSPACE": str(self.ws)}):
            self.assertEqual(quietly(newep.main, "zz-series", "ep-test"), 0)
            from engine import settings
            self.assertEqual(settings.env("ELEVENLABS_VOICE_ID"), "abc")
        ep = self.ws / "stories" / "zz-series" / "ep-test"
        self.assertIn('id = "ep-test"', (ep / "episode.toml").read_text(encoding="utf-8"))
        self.assertTrue((ep / "timeline.py").exists() and (ep / "publish" / "publish.json").exists())


if __name__ == "__main__":
    unittest.main()
