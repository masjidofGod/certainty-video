# Operating modes, KPIs, retries, and Pareto decisions

Read this file when the user asks for quality, speed, trade-offs, budget policy, throughput, or success metrics.

The three modes are evidence-supported starting policies. This research did not run paid generation to prove an optimum. [FP-16]

## Quality-max

Use for hero work, enduring character/IP, cinema/high-end delivery, key performance, difficult physics, or strict brand continuity.

- Full bible, rights, location maps, entity schedules, color/sound scripts first.
- Hero and high-risk shots receive previz, keyframes/blockout and feasibility tests.
- More candidates and independent reviewers, with blind comparison where practical.
- Hard gates plus intra-shot, adherence/fidelity, cross-shot, and neighbor-cut review.
- Full VFX/cleanup/color/ADR/foley/music/subtitle/mastering after picture lock.

Trade-off: higher asset, review, retry, coordination and finishing time. It is not simultaneously speed-max.

## Speed-max-with-floor

Use when wall-clock matters and story can use simplified coverage.

- Lock the minimum bible: protagonists, main locations, critical props, camera/color/sound grammar.
- Produce a complete animatic and blocking rough cut first.
- Favor short, single-event, low-cast, simple-camera shots and editorial cuts.
- Run one first blocking candidate; upgrade only story-blocking A/B shots.
- Route exact text, subtitles, clean plates, local defects, transitions and sound to mature post tools.
- Do not relax story beat, identity, required entities, direction/prop state, understandable sound, rights, delivery, or blocking-artifact gates.

Stop after a repeated hard defect and change route; do not endlessly rephrase.

## Recommended hybrid

1. Make the full film work end to end.
2. Grade each shot by narrative value × technical risk.
3. A: quality workflow for hero/turn/identity close-up/complex physics.
4. B: standard references and QC, upgrade only when blocked.
5. C: fast parallel connective/texture/insert coverage.
6. Fix script, coverage and continuity before pixel polish.
7. Keep safety, rights, story, identity, continuity and delivery floors common to all tiers.

Recommended means the current evidence best supports it as an initial policy, not that it is globally optimal.

## Hard gates before scores

- rights/safety/delivery and required story beats;
- correct identity, entities and state;
- unambiguous continuity-critical direction/ownership;
- no uneditable structural or blocking artifact;
- complete usable interval and neighbor compatibility;
- no rendered text outside the scene's on-screen-text inventory and no audio outside its declared layer assignment (both are defined in the editorial and finishing reference);
- sound/text requirements either pass or have an approved post route.

Project-specific numeric floors may be added, but never present them as model averages.

## Quality KPIs [FP-17]

- prompt/story-beat adherence;
- character/wardrobe/injury/location/prop/voice/style continuity;
- temporal stability and anatomy/artifact rate;
- motion, contact, inertia, physical/commonsense causality;
- camera/composition/light/material;
- dialogue, lip-sync, ambience, SFX, music and subtitle correctness;
- editorial usability, handles and neighbor compatibility.

## Efficiency KPIs

```text
first_pass_approval = approved on first valid run / valid first runs
additional_retries = extra valid runs before approval / approved shots
time_per_approved_shot = shot-ready to approved wall clock
usable_seconds_per_hour = approved seconds entering cut / production-review hours
cost_per_approved_second = all billable runs + dedicated post tools / in-cut seconds
human_correction_time = prep + review + edit/VFX/sound fix hours
queue_wait_ratio = queue time / shot-ready-to-result time
waste_rate = generated seconds or cost not entering cut / total generated seconds or cost
```

Report median, distribution and P90 retries/time where sample size permits. Split `first_pass_approval`, `additional_retries` and `waste_rate` by retry class; a shot whose retries are mostly resamples has a different problem from one whose retries are mostly revisions, and the merged figure distinguishes neither. Costs and times come from actual ledgers. Marketing counters, UI asset totals, price pages and claimed schedules do not substitute for production data.

## Retry and route policy

Set ceiling by shot risk, budget and delivery clock. Change one prompt, reference, parameter, or shot-design variable at a time. Stop and route when the same blocking defect persists, critical constraints oscillate, the ceiling is reached, a rejected frame would need promotion, or rights/delivery cannot pass.

Retries divide into two classes, and a merged count hides both:

- **resample**, the same prompt, references and parameters submitted again for a different sample. It tests whether the defect was sampling variance. Because nothing changed, it can never repair a specification error.
- **revision**, the single-variable change the retry policy already requires [FP-14]. Only this class yields attribution.

Record `retry_class` on every run alongside the reviewer's stated reason: which observed defect made this a variance problem rather than a specification problem. Count each class against its own ceiling rather than a shared one; where the project has set no ceiling, keep it unknown [FP-14].

Provider records may expose no parent link between attempts, and a single submission may return several samples, so neither attempt order nor sibling grouping is recoverable from platform records afterwards. Assign lineage and `retry_class` in the production ledger at submission time; never plan to reconstruct them later.

Unchanged re-submission is common enough in practice to need its own line in the ledger, and no controlled evidence shows whether it repairs shots or burns budget. That is the reason to count it separately, not a reason to recommend or forbid it.

Possible routes: cleaner/state-specific asset, simpler prompt/action, locked camera, shorter/split shot, insert/reaction/cutaway, local edit, grade/color correction for exposure, black-level or shot-match defects, traditional VFX/composite, 2D/3D/live action, ADR/dubbing, graphic overlay, or story redesign.

## Pareto decision [FP-18]

First apply all quality floors. A workflow dominates another only when it is no worse on every required quality/efficiency dimension and better on at least one. Better quality but slower may remain a non-dominated choice.

Never collapse the trade-off into “fastest and best” without controlled evidence. State conclusions only for the tested suite, model ID, platform, date, reviewers, quality floor, and budget. Same-seed comparisons reduce variance where supported but do not prove deterministic reproduction.
