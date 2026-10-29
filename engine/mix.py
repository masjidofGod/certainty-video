"""The episode's mix, on its clock: the voice, the count's clicks, small bells, and the music cues.

    certainty mix <episode>

Reads clock.json and places every voice piece where the clock says, so picture and sound meet sample for sample.
Made here, on the frame: one soft click per counted letter (each a little higher), a low note on the numeral,
and a small bell on each spoken word listed in bells_on. Music cues from episode.toml:

    [mix]
    lufs = -16              # integrated loudness of the finished mix
    true_peak = -2.5        # so the AAC upload stays under -2 dBTP
    bells_on = ["nineteen"]
    music_under_voice_db = -14     # music level under speech, relative to the voice (it comes up 7 dB between lines)

    [[mix.music]]
    file = "music/M1_take1.wav"
    start = "0"             # seconds, or "L3" (that line's start), "count", "numeral", "end"
    end = "count"
    skip = 0.0              # seconds into the file where it starts
    gain_db = 0
    fade_in = 0.0
    fade_out = 3.0

Writes mix.wav (48 kHz, 16-bit stereo), normalized with ffmpeg's loudnorm. The premix is passed as 32-bit float so
nothing clips before the normalization.
"""
import json
import re
import subprocess

import numpy as np
from scipy.ndimage import uniform_filter1d

from .episode import Episode

SR = 48000


def load(path, ss=None, to=None):
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + (["-to", str(to)] if to is not None else [])
    cmd += ["-i", str(path), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, "<f4").reshape(-1, 2).astype(np.float64)


def pan(mono, x=0.0):
    a = (x + 1) * np.pi / 4
    return np.column_stack([mono * np.cos(a), mono * np.sin(a)])


def click(k, n):
    """A soft wooden click, a little higher for each letter."""
    t = np.arange(int(0.12 * SR)) / SR
    f = 900 * 2 ** (k / max(18, n) * 0.75)
    body = np.sin(2 * np.pi * f * t) * np.exp(-t / 0.012) + 0.35 * np.sin(2 * np.pi * 2.3 * f * t) * np.exp(-t / 0.006)
    noise = np.random.default_rng(k).normal(0, 1, len(t)) * np.exp(-t / 0.002) * 0.25
    return (body + noise) * np.minimum(1, t / 0.0008)


def pluck(f, dur=2.4):
    t = np.arange(int(dur * SR)) / SR
    out = sum(np.sin(2 * np.pi * f * k * np.sqrt(1 + 0.0004 * k * k) * t) * k ** -1.4 * np.exp(-t * (1.1 + 0.9 * k))
              for k in range(1, 9))
    return out * np.minimum(1, t / 0.004)


def bell(f, dur=2.4):
    t = np.arange(int(dur * SR)) / SR
    out = sum(a * np.sin(2 * np.pi * f * r * t) * np.exp(-t / d)
              for r, a, d in ((1.0, 1.0, 1.6), (2.0, 0.35, 0.9), (2.76, 0.28, 0.6), (5.4, 0.12, 0.3), (8.93, 0.05, 0.18)))
    return out * np.minimum(1, t / 0.002)


def build(ep):
    clock = json.load(open(ep.path("clock.json"), encoding="utf-8"))
    cfg = ep.cfg.get("mix", {})
    end = clock["end_s"]
    N = int(end * SR)
    voice, music, fx = (np.zeros((N, 2)) for _ in range(3))

    def put(buf, sig, t, gain=1.0):
        i = int(round(t * SR))
        j = min(N, i + len(sig))
        if j > i:
            buf[i:j] += gain * sig[: j - i]

    for p in clock["pieces"]:
        put(voice, load(ep.path(p["file"]), p["src"][0], p["src"][1]), p["at"])
    cnt = clock.get("count")
    if cnt:
        n = len(cnt["clicks"])
        for k, tc in enumerate(cnt["clicks"]):
            put(fx, pan(click(k, n), 0.0), tc - 0.002, 0.5)
        put(fx, pan(pluck(65.41) + 0.6 * pluck(130.81) + 0.25 * bell(1046.5), 0), cnt["numeral"], 0.6)
    words = [(w["w"], w["start"]) for l in clock["lines"] for w in l["words"]]
    bells_on = {b.lower() for b in cfg.get("bells_on", [])}
    penta = [1046.5, 1174.66, 1318.51, 1567.98, 1760.0, 2093.0]
    step = 0
    for w, s in words:
        if re.sub(r"[^a-z]", "", w.lower()) in bells_on:
            put(fx, pan(bell(penta[min(step, len(penta) - 1)]), 0.2 * (-1) ** step), s, 0.12)
            step += 1

    anchors = {"0": 0.0, "end": end}
    if cnt:
        anchors.update(count=cnt["open"], numeral=cnt["numeral"])
    for l in clock["lines"]:
        anchors[l["id"]] = l["start"]
        anchors["L" + str(int(l["id"][1:]))] = l["start"]

    def when(x):
        try:
            return float(x)
        except ValueError:
            return anchors[x]

    for cue in cfg.get("music", []):
        t0, t1 = when(str(cue.get("start", "0"))), when(str(cue.get("end", "end")))
        sig = load(ep.path(cue["file"]))[int(cue.get("skip", 0.0) * SR):][: int((t1 - t0) * SR)].copy()
        fi, fo = int(cue.get("fade_in", 0.0) * SR), int(cue.get("fade_out", 0.0) * SR)
        if fi:
            sig[:fi] *= np.linspace(0, 1, fi)[:, None]
        if fo:
            sig[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2
        put(music, sig, t0, 10 ** (cue.get("gain_db", 0) / 20))

    def rms(x):
        act = x[np.abs(x).sum(1) > 1e-4]
        return np.sqrt(np.mean(act ** 2)) if len(act) else 1.0

    if np.abs(voice).max() > 0:
        voice *= 10 ** (-18 / 20) / rms(voice)
    if np.abs(music).max() > 0:
        music *= 10 ** ((-18 + cfg.get("music_under_voice_db", -14)) / 20) / rms(music)
        speaking = uniform_filter1d((np.abs(voice).sum(1) > 0.01).astype(float), int(0.25 * SR))
        speaking = np.clip(uniform_filter1d(speaking, int(0.4 * SR)) * 2, 0, 1)
        music *= (10 ** (7 / 20 * (1 - speaking)))[:, None]
    if np.abs(fx).max() > 0:
        fx *= 10 ** (-20 / 20) / np.abs(fx).max()
    return voice + music + fx, bool(np.abs(voice).max() > 0 or np.abs(music).max() > 0)


def main(argv):
    if not argv:
        raise SystemExit("usage: certainty mix <episode>")
    ep = Episode(argv[0])
    cfg = ep.cfg.get("mix", {})
    mix, program = build(ep)
    out = ep.path("mix.wav")
    if program:                       # voice or music: to the loudness target
        af = f"loudnorm=I={cfg.get('lufs', -16)}:TP={cfg.get('true_peak', -2.5)}:LRA=11"
    else:                             # clicks and bells only (the demo): their peak at -6 dBFS, no loudness push
        mix = mix * (10 ** (-6 / 20) / max(1e-9, np.abs(mix).max()))
        af = "anull"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", af,
                    "-ar", str(SR), "-c:a", "pcm_s16le", str(out)], input=mix.astype("<f4").tobytes(), check=True)
    print(f"{out}: {len(mix) / SR:.2f} s")
    return 0
