---
name: studio
description: Make a Certainty-style episode (a short vertical film that counts one of the Quran's number patterns so the viewer can check it) through the departments in order - the claims, the script, the Arabic, the voice, the clock, the music, the mix, the picture, the checks, the cover and the package - with the kit's `certainty` command, stopping for the user's approval at each gate and never spending credits or posting without a yes. Use when starting a series or an episode, when continuing one, when asked what to do next on one, for the demo, or for any step of making one.
---

# Certainty studio

You run an episode the way a small film crew would, one department at a time. The kit is at
`${CLAUDE_PLUGIN_ROOT}`; its one command, `certainty`, is on your PATH (`certainty` alone lists what it does). Read
as you need them: the commands in order in `${CLAUDE_PLUGIN_ROOT}/docs/pipeline.md`, the rules in
`${CLAUDE_PLUGIN_ROOT}/docs/rules.md` (they win over anything else here), the look in
`${CLAUDE_PLUGIN_ROOT}/docs/look.md`, the data format in `${CLAUDE_PLUGIN_ROOT}/docs/data-format.md`, and a complete
small episode in `${CLAUDE_PLUGIN_ROOT}/examples/demo/`.

## The workspace

The user's work lives in a workspace, never in the kit: a folder with `certainty.toml`, `.env` (keys), `data/` (their
Quran data file) and `stories/<series>/<id>/` (episodes). Every command finds it from the folder it runs in.

- No workspace yet: ask which folder to use (the one Claude Code is open in is the usual answer), then
  `certainty init`. The first command also sets up the kit's Python packages, about a minute, once.
- First time: `certainty demo` shows the whole pipeline working, with no credits and no data of their own.
- No Quran data yet: the user supplies it (`docs/data-format.md`); the kit ships none. Never invent or type Quran
  text yourself.

## Rules that are never bent

- Every number on screen or in the narration is a claim in the episode's `claims.toml` that `certainty verify` says
  matches the data. Never type a number into a timeline; read it with `verify.measured()`.
- Every quotation is verbatim, from the data, with its address. Arabic is drawn only from `certainty glyphs`.
- Nothing is said about God that is not a verbatim quotation. Kind words throughout.
- Never pass `--yes` to `voice` or `music` without the user's yes for that spend.
- Never post anything without the user's yes for that post. Never ask for, type or store a password or a key.
- Keys stay in `.env` and are never printed, logged or committed.
- Everything to be read stays inside the platforms' safe area; `certainty safe` must pass.

## Before anything

- Run `certainty doctor`. Fix what it reports first.
- Read the episode's `decisions.md`. Every decision of the user's goes there, in their words, with what it
  replaces; the next session starts from it.

## The departments, in order

Start an episode with `certainty new <series> <id>`.

| # | Department | Work | Craft skills to lean on | Gate (stop and ask) |
| --- | --- | --- | --- | --- |
| 1 | Research | Pick the pattern. Write each number as a claim in `claims.toml`; `certainty verify` until every claim matches. Leave out any claim that needs a counting rule the viewer cannot see, or put the rule on screen. | | the claims |
| 2 | Script | `script.md`: a cold open that shows a count in the first frame, acts that each turn on a question, a build-up, a quiet ending, an invitation to count. Quotations verbatim, with addresses. Nothing about God that is not a quotation. Kind words. | `sw-story-structure`, `sw-scene-craft`, `sw-premise-theme`, `sw-dialogue`, `sb-cinematic-explainer` | **the script** |
| 3 | Art | The Arabic each scene draws: `certainty glyphs`. The board (`board.md`): what changes on screen during each line, in the look. Stills of the hardest frames, inside the safe area, before any motion. | `art-visual-style`, `art-color-script`, `art-reference-analysis`, `cam-shot-direction` | **the stills** |
| 4 | Sound | `sound-plan.md`. The voice: `certainty voice <ep>` as a dry run, tell the user the size, then `--yes` only after they agree. `certainty whisper <ep>`, then `certainty takes <ep>`; a line with no word-perfect take is regenerated, never fudged. | `snd-dialogue-adr`, `snd-music-scoring`, `snd-mix-master`, `snd-design-foley` | **the credits** |
| 5 | Board | `certainty clock <ep>`. Set the air between lines, the beats and the count in episode.toml; run again until the pace holds. | `ed-editor-judgment`, `ed-editing-montage` | |
| 6 | Music | Composition plans sized to the clock's stretches; dry run, a yes, then `--yes`. Measure each cue; place it so its cadence lands on its line. `certainty mix <ep>`. | `snd-music-scoring` | **the credits** |
| 7 | Picture | `timeline.py`, scene by scene from `engine/scenes.py` and the demo. Every time from the clock, every number from `verify.measured()`. Stills, then `certainty film <ep> --draft`. | `sb-cinematic-explainer`, `ed-titles-typography`, `ed-captions` | **the draft** |
| 8 | QC | `certainty film <ep>`; `check` with `--frames`; `safe`. Both pass, or fix and render again. Look at a contact sheet of the whole film. | `prod-media-qa`, `prod-qc-delivery`, `ed-ffmpeg-finishing` | |
| 9 | Cover | episode.toml [cover]; `certainty cover <ep>`. A painting only if its license allows it, with its source in `covers/SOURCES.md`. | `ed-titles-typography`, `art-color-grading` | **the cover** |
| 10 | Package | `certainty package <ep>`; fill in `publish/README.md` with the post copy (sources named, how it was made, AI disclosure). Then the `publish` skill. | `prod-provenance-rights` | **each post** |

The craft skills come with the kit (in this plugin, named `certainty:<skill>`).

## How to work

- One department at a time. Show the work, ask for the gate, wait. A "looks good" moves one step.
- Before spending credits, run the dry run and say what it will send. Never pass `--yes` without the user's yes.
- When the user gives notes on a draft, apply each note, render stills of what changed, and check the safe area
  again before showing the next draft.
- Never change a claim to make it match: if `verify` says a claim differs, the claim goes or the rule goes on screen.
- Keep the user's words in `decisions.md` for every approval and every change.
- Without the plugin (a clone of the kit), the command is `bin/certainty` in the kit's folder (`bin\certainty.cmd`
  in Command Prompt or PowerShell), with the same arguments.
