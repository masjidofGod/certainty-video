# Certainty

Skills for Claude Code that make short vertical films counting one of the Quran's number patterns, so a viewer can
check the count for themselves. Arabic drawn from the exact outlines of the Quran's text, a pen that writes it,
letters that turn gold as they are counted, a narrator, music, captions, and an upload file for Reels, TikTok and
Shorts. Everything is drawn by code on your own computer: no video generator, no account with us.

The plugin brings a crew of skills, an engine that draws in one consistent look, and one command, `certainty`,
that runs the pipeline from claims to upload file. You bring your Quran data, your own ElevenLabs account for the
voice and music, and your own social accounts.

## Install

In Claude Code:

```text
/plugin marketplace add masjidofGod/certainty-video
/plugin install certainty@certainty-video
```

Then open Claude Code in an empty folder for your series and say: *"Set up a Certainty workspace here and run the
demo."* The first run sets up the kit's Python packages (about a minute, once). The demo writes the Basmalah with the
pen and counts its 19 letters, with no credits and no data of your own, and ends with `demo/out/film.mp4`.

To update later: `/plugin`, then Marketplaces, `certainty-video`, Update marketplace.

## What you need

| | Windows | macOS | Linux |
| --- | --- | --- | --- |
| Python 3.12 (or 3.13) | `winget install --id Python.Python.3.12` | python.org | your package manager |
| ffmpeg | `winget install --id Gyan.FFmpeg` | `brew install ffmpeg` | your package manager |
| Whisper, to check the narration word for word | `py -3.12 -m pip install openai-whisper` | `python3 -m pip install openai-whisper` | the same, or `pipx install openai-whisper` |

On Windows, open a new terminal after installing so the new programs are found. Windows x64, macOS (Apple Silicon or
Intel) and Linux are supported, and checked on all three on every change.

Also yours to bring:

- **Your Quran data file**, in the format of [docs/data-format.md](docs/data-format.md). The kit ships no Quran text;
  use a text and a translation you have the right to use. Every number in an episode is counted from this file.
- **An ElevenLabs account** for the narration and the music (paid by credits; nothing is spent without your yes).
- **Your own accounts** on the platforms you post to. The skills never ask for a password.

## The skills

| Skill | What it does |
| --- | --- |
| `certainty:studio` | Takes an episode through the departments in order: claims, script, Arabic, voice, clock, music, mix, picture, checks, cover, package. Stops for your approval at each gate. |
| `certainty:publish` | Posts a finished episode to Instagram Reels, TikTok and YouTube Shorts with you: post copy, AI disclosure, each platform's settings and traps, your yes before every post. |
| `certainty:sw-*` (10) | Screenwriting: premise and theme, structure, scenes, dialogue, characters, genre, workflow. |
| `certainty:art-*` (8), `certainty:cam-*` (3) | Look, color script, lighting, references, frames; shot direction and camera. |
| `certainty:snd-*` (5) | Dialogue and narration, music, sound design, mix and master. |
| `certainty:ed-*` (6) | Editing judgment, montage, captions, titles, compositing, FFmpeg finishing. |
| `certainty:prod-*` (7), `certainty:sb-*` (2), two more | Production, QC and delivery, provenance and rights, storyboards, explainers, performance, shot prompts. |

The craft skills are third-party, each with its own license and source in [THIRD_PARTY.md](THIRD_PARTY.md).

## The command

Claude runs it for you; you can too. `certainty` alone lists everything.

```text
certainty init                     make this folder a workspace (certainty.toml, .env, data/, stories/)
certainty doctor                   what is installed and what is missing
certainty demo                     the demo film, no credits needed
certainty new <series> <id>        start an episode in stories/<series>/<id>/
certainty verify <ep>/claims.toml  every number against your data
certainty film <ep> --draft        a quick draft; without --draft, the 1080 x 1920 film
certainty check <ep>/out/film.mp4  the upload file against the delivery spec
```

The whole pipeline, step by step: [docs/pipeline.md](docs/pipeline.md).

## The rules

Every number is computed from your data and checked before it is shown; every quotation is verbatim, with its
address; nothing is said about God that is not a verbatim quotation; kind words; and every post says how the film
was made. All of them: [docs/rules.md](docs/rules.md).

## Without the plugin

Clone the repository and run `bin/certainty` from it (`bin\certainty.cmd` in Command Prompt or PowerShell), with the
same arguments, in a folder made a workspace with `bin/certainty init`. The skills are in `skills/`.

## What is in here

| Folder | What |
| --- | --- |
| `skills/` | The skills above |
| `engine/` | The pipeline: the data and counts, exact Arabic outlines, the look (`canvas.py`), reusable scenes (`scenes.py`), the voice and music calls, the take check, the clock, the mix, rendering, the delivery and safe-area checks, the cover, the package |
| `bin/` | `certainty` (and `certainty.cmd` for Windows) |
| `templates/` | A workspace and an episode, ready to fill in |
| `examples/demo/` | A complete small episode: the Basmalah counted |
| `docs/` | The pipeline, the data format, the rules, the look |
| `fonts/` | Amiri Quran, IBM Plex Mono, Poppins, Source Serif 4, with their licenses |
| `tests/` | The kit's own tests (`certainty test`), run on Windows, macOS and Linux by `.github/workflows/check.yml` |

## License

Free to use for noncommercial purposes. The code is under the PolyForm Noncommercial License 1.0.0 and the
documents under CC BY-NC 4.0; the third-party skills and the fonts keep their own licenses. See
[LICENSE.md](LICENSE.md) and [THIRD_PARTY.md](THIRD_PARTY.md).
