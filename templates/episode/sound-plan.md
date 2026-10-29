# {{EPISODE_ID}}: sound plan

## Voice

- Narrator: FILL IN (the ElevenLabs voice in .env; check its terms if it is a library voice)
- Delivery: FILL IN (pace, warmth; how quotations are read)
- Takes: two a line; checked word for word (`certainty takes`); the shorter exact take is picked

## Music

| Stretch | Cue | What it does |
| --- | --- | --- |
| 0:00 to the count | M1 | FILL IN |
| the count | none | clicks only, so the ear counts with the eye |
| after the numeral | M2 | FILL IN |

Make a cue with a composition plan (`music/M1.json`, see docs/pipeline.md) and `certainty music`, or use music
you are licensed to use. The cue's cadence should land on the line it belongs to.

## Effects and level

- Clicks on the count and a note on the numeral are made by `certainty mix`; bells on words in [mix] bells_on.
- The mix: -16 LUFS integrated, -2.5 dBTP (episode.toml [mix]); the voice always on top.
