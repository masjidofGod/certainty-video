"""The upload file: its encode, and the checks it must pass before it is posted.

    certainty check <episode>/out/film.mp4 [--frames N]

One file serves YouTube Shorts, Instagram Reels and TikTok: 1080 x 1920, 24 fps constant, H.264 High 4.1, 4:2:0,
Rec.709 tagged, AAC 48 kHz stereo, fast start, at most 180 s. The check reads the file with ffprobe and ffmpeg's
loudness meter and fails (exit 1) on anything the platforms would reject or degrade. Safe areas are checked by
`certainty safe`.
"""
import argparse
import json
import re
import subprocess

PRESETS = {
    "upload": dict(width=1080, height=1920, fps=24, crf=16, preset="slow", maxrate="25M", bufsize="50M", gop=48,
                   level="4.1", abitrate="256k"),
    "draft": dict(width=540, height=960, fps=24, crf=23, preset="medium", maxrate=None, bufsize=None, gop=48,
                  level=None, abitrate="192k"),
}


def export_command(preset, out, audio=None, frames=None, pipe=False, src=None):
    """ffmpeg for a preset. pipe=True reads raw RGB 1080 x 1920 frames from stdin; else src is a video or a
    frame pattern."""
    p = PRESETS[preset]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if pipe:
        cmd += ["-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920", "-framerate", str(p["fps"]), "-i", "-"]
    else:
        cmd += ["-i", src]
    if audio:
        cmd += ["-i", audio, "-map", "0:v:0", "-map", "1:a:0"]
    vf = [f"scale={p['width']}:{p['height']}:flags=lanczos+accurate_rnd+full_chroma_int:out_color_matrix=bt709:out_range=tv",
          "setsar=1", "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv", "format=yuv420p"]
    cmd += ["-vf", ",".join(vf), "-c:v", "libx264", "-profile:v", "high", "-preset", p["preset"], "-crf", str(p["crf"]),
            "-g", str(p["gop"]), "-keyint_min", str(p["gop"] // 2)]
    if p["maxrate"]:
        cmd += ["-maxrate", p["maxrate"], "-bufsize", p["bufsize"]]
    if p["level"]:
        cmd += ["-level:v", p["level"]]
    cmd += ["-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
            "-r", str(p["fps"]), "-fps_mode", "cfr"]
    if frames:
        cmd += ["-frames:v", str(frames)]
        if audio:
            n = int(round(frames / p["fps"] * 48000))
            cmd += ["-af", f"aresample=48000,apad=whole_len={n},atrim=end_sample={n}"]
    if audio:
        cmd += ["-c:a", "aac", "-b:a", p["abitrate"], "-ar", "48000", "-ac", "2"]
    cmd += ["-map_metadata", "-1", "-metadata", "encoder=", "-movflags", "+faststart", out]
    return cmd


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if out.returncode:
        raise SystemExit(f"{path}: not a readable video ({out.stderr.strip()[:200]})")
    return json.loads(out.stdout)


def loudness(path):
    err = subprocess.run(["ffmpeg", "-nostats", "-hide_banner", "-i", path, "-vn", "-af", "ebur128=peak=true", "-f", "null",
                          "-"], capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    s = err[err.rfind("Summary:"):]
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", s)
    tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", s)
    return (float(i.group(1)) if i else None), (float(tp.group(1)) if tp else None)


def check(path, frames=None, max_tp=-2.0):
    d = probe(path)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    rows = []

    def row(name, ok, got, want):
        rows.append((name, ok, got, want))

    row("video stream", v is not None, "yes" if v else "none", "one H.264 stream")
    if v:
        row("size", (v["width"], v["height"]) == (1080, 1920), f"{v['width']}x{v['height']}", "1080x1920")
        n, de = v["r_frame_rate"].split("/")
        fps = float(n) / float(de)
        row("frame rate", abs(fps - 24) < 0.01, f"{fps:g}", "24")
        row("codec", v["codec_name"] == "h264" and v.get("profile") == "High", f"{v['codec_name']} {v.get('profile')}", "h264 High")
        row("pixel format", v.get("pix_fmt") == "yuv420p", v.get("pix_fmt"), "yuv420p")
        row("color tags", v.get("color_primaries") == "bt709" and v.get("color_transfer") == "bt709",
            f"{v.get('color_primaries')}/{v.get('color_transfer')}", "bt709/bt709")
        if frames:
            nb = int(v.get("nb_frames", 0))
            row("frame count", nb == frames, str(nb), str(frames))
    dur = float(d["format"]["duration"])
    row("duration", dur <= 180.0, f"{dur:.2f} s", "at most 180 s")
    row("audio stream", a is not None, "yes" if a else "none", "AAC 48 kHz stereo")
    if a:
        row("audio format", a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2,
            f"{a['codec_name']} {a['sample_rate']} {a['channels']} ch", "aac 48000 2 ch")
        lufs, tp = loudness(path)
        row("true peak", tp is not None and tp <= max_tp, f"{tp} dBTP", f"at most {max_tp}")
        rows.append(("loudness", True, f"{lufs} LUFS", "reported (the series mixes to -16)"))
    return rows


def main(argv):
    ap = argparse.ArgumentParser(prog="certainty check")
    ap.add_argument("file")
    ap.add_argument("--frames", type=int)
    a = ap.parse_args(argv)
    rows = check(a.file, a.frames)
    print("| check | | got | want |\n| --- | --- | --- | --- |")
    for name, ok, got, want in rows:
        print(f"| {name} | {'pass' if ok else 'FAIL'} | {got} | {want} |")
    bad = [r for r in rows if not r[1]]
    print(f"{len(rows)} checks, {len(bad)} failed")
    return 1 if bad else 0
