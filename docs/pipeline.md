# The pipeline, step by step

One episode, from an idea to three uploads, in a workspace (`certainty init`). With the plugin installed, `certainty`
is on Claude Code's PATH; from a clone of the kit it is `bin/certainty` (`bin\certainty.cmd` in Command Prompt or
PowerShell), with the same arguments. Every step is a command; the department skills in Claude Code decide what goes
into each step and stop at each approval. Nothing that costs money runs without `--yes`, and nothing is
posted without you.

| # | Step | Command | You approve |
| --- | --- | --- | --- |
| 0 | Start the episode | `certainty new <series> <id>` | |
| 1 | The pattern, and its claims | `certainty verify <ep>/claims.toml` | the claims |
| 2 | The script | edit `<ep>/script.md` (the `sw-*` skills help) | **the script** |
| 3 | The Arabic it draws | `certainty glyphs verse 1:1 <ep>/art/basmala.json`, `glyphs phrase 74:30 0 2 <ep>/art/x.json` | |
| 4 | The voice | `certainty voice <ep>` (a dry run: its size), then `--yes` | **the credits** |
| 5 | The takes, word for word | `certainty whisper <ep>`, then `certainty takes <ep>` | |
| 6 | The clock | `certainty clock <ep>` | |
| 7 | The music | `certainty music <ep>/music/M1.json`, then `--yes` | **the credits** |
| 8 | The mix | `certainty mix <ep>` | |
| 9 | The picture | write `<ep>/timeline.py`; `certainty stills <ep> 3 12 40`; `certainty film <ep> --draft` | **the draft** |
| 10 | The film | `certainty film <ep>` | |
| 11 | The checks | `certainty check <ep>/out/film.mp4 --frames N`, `certainty safe <ep>/out/film.mp4` | |
| 12 | The cover | `certainty cover <ep>` | **the cover** |
| 13 | The package | `certainty package <ep>`; fill in `<ep>/publish/README.md` | **each post** |

## The data

Everything starts from your Quran data file (`docs/data-format.md`). `certainty data check` reads it;
`certainty count` counts from it; `verify` checks claims against it. Arabic on screen is shaped from it.

## The voice (step 4 and 5)

`certainty voice <ep>` sends each line of the script to ElevenLabs as the voice in `.env`, two takes a line
(episode.toml [voice]), into `<ep>/takes/`. Then check every take word for word:

```
certainty whisper <ep>
certainty takes <ep>
```

`whisper` runs Whisper (medium.en, with word times) on every take that has no JSON in `<ep>/whisper/` yet. It needs
Whisper installed in any Python (README, "Set up"); on a computer without a graphics card the medium model takes
about as long as the takes themselves, or longer.

A take that differs from the script by a word is never used. Names the recognizer cannot spell go in [takes] names.

## The clock (step 6)

The clock puts the picked takes end to end with the air in episode.toml [clock], trims long pauses inside a take,
makes each "(beat)" at the take's own silence, and places the count. Every frame of the film is timed from it:
`clock.json` has each line's start, each word's start and end, and the count's clicks and numeral. Change the air,
run `clock` again; the picture follows.

## Music (step 7)

A composition plan is ElevenLabs Music's: `music/M1.json` with `model_id` ("music_v2_5"), `output_format`
("mp3_48000_320") and `composition_plan.chunks`, each with `text`, `duration_ms` (3,000 to 120,000),
`positive_styles`, `negative_styles` and `context_adherence`. Size the chunks to the clock's stretches (the cold
open, the act, the count). Measure a cue before using it (its level every few seconds, where its cadence falls), and
place it in [[mix.music]] so its cadence lands on the line it belongs to.

## The picture (step 9)

`timeline.py` draws each frame from the engine (`engine/canvas.py`: the look; `engine/scenes.py`: the pen, phrases,
the counted verse, the numeral, captions). Review stills before any motion, then a 480p draft. The finished film is
rendered once, at 1080 x 1920.

## The checks (step 11)

`check` reads the upload file: size, 24 fps, H.264 High, Rec.709 tags, AAC 48 kHz stereo, at most 180 s, true peak
at most -2 dBTP. `safe` scans the frames for anything drawn under the platforms' buttons and captions. Both must
pass before the film is posted.
