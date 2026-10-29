# A Certainty workspace

This folder makes short vertical films that count one of the Quran's number patterns, so a viewer can check them
for themselves, with the Certainty kit (the `certainty` plugin for Claude Code). It holds this series' settings
(`certainty.toml`), keys (`.env`), Quran data (`data/`) and episodes (`stories/<series>/<id>/`).

## Start every session

1. Run `certainty doctor`; fix what it reports.
2. For an episode, use the `certainty:studio` skill and read the episode's `decisions.md` first.

## Rules that are never bent

- Every number on screen or in the narration is a claim in the episode's `claims.toml` that `certainty verify`
  says matches the data. Never type a number into a timeline; read it with `verify.measured()`.
- Every quotation is verbatim, from the data, with its address. Arabic is drawn only from `certainty glyphs`.
- Nothing is said about God that is not a verbatim quotation. Kind words throughout.
- Never pass `--yes` to `voice` or `music` without the user's yes for that spend.
- Never post anything without the user's yes for that post. Never ask for, type or store a password or a key.
- Keys stay in `.env` and are never printed, logged or committed.
- Everything to be read stays inside the platforms' safe area; `certainty safe` must pass.
