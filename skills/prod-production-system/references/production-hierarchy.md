# Production hierarchy and gates

Read this file when turning a concept, treatment, or screenplay into a multi-shot production plan.

## Project charter

Lock before production:

- story purpose, audience, tone boundaries, target length and delivery surfaces;
- actual generation platform, displayed model, model ID if exposed, region, current documentation date;
- aspect ratio, master frame rate, codec/color/audio/subtitle/master specifications;
- the channel of record for every delivery spec: runtime parameter, prompt text, or geometry drawn into the picture;
- rights for story, likeness, voice, music, type, brands, and every reference;
- depicted-content policy: what the chosen provider will refuse to render, and the project's own line on real people, public figures, minors, and identifiable bystanders, a charter gate, because a subject that cannot be depicted invalidates the coverage rather than one shot;
- allowed generation and post tools, budget/clock ceilings, storage and review responsibilities;
- risk tier and chosen operating mode: quality-max, speed-max-with-floor, or recommended hybrid.

A vertical or social master, 9:16 for Reels, TikTok and Shorts, 4:5 for a feed post, is decided here rather than cropped in at the end: it changes staging, shot size, and how much coverage a scene needs, so a 16:9 film reframed after picture lock loses the blocking it was shot for. Where both a wide and a vertical deliverable are required, name which one is the master and state the protect-area rule the other imposes on every shot.

Treat availability, prices, quotas, parameters and policies as time-sensitive. Archived skill knowledge is dated 2026-08-22.

## Hierarchy

| Level | Decision | Required artifact | Exit gate |
|---|---|---|---|
| Film *(standalone)* | What is the complete experience? | charter, treatment/script, bible, story/color/sound arcs | story, rights, format locked |
| Season *(series)* | What does this block of episodes establish, spend, and hold back? | season plan, declared serialization tier, per-episode pressure and motif schedule, reserve-draw schedule, season bible delta | tier declared; every ordered episode has an owner, a register, and a licensed reserve position |
| Episode *(series)* | What does this hour owe on its own, and what does it owe the season? | episode card, re-entry plan, inherited state manifest, per-episode asset-version resolution | set by the serialization tier, see [Series levels](#series-levels) |
| Sequence | What macro objective and turn occur? | sequence card, information/emotion/pace curve, duration budget | turn and dependency clear |
| Scene | When/where/who wants what and what state changes? | scene card, floor plan, continuity state, coverage plan | geography/entities/state solvable |
| Beat | What single visible behavior, reaction, or information unit occurs? | causal beat list with start/end state | each beat earns its screen time |
| Shot | From where does the audience see one beat? | shot contract, input packet, prompt, parameters, QC/route | independently generatable/reviewable/editable |

Model capability does not replace this hierarchy. Single-clip duration or extension support is not long-form memory.

## Series levels

Series form replaces the Film row with Season and Episode. The charter is written once for the series; each season carries a delta against it, register, reserve position, any change to the delivery surface, rather than a new charter. [FP-01]

The **episode exit gate is not a production choice.** It is set by the serialization tier declared in the series contract, which the `sw-*` skills owns together with what each tier costs the story. Carry the tier across the handoff and record it in the charter: a plan that has not been told the tier cannot tell a finished episode from an unfinished one, and will accept an episode ending on an unanswered question in a show whose viewers were promised a settled hour.

The tier also sets the schedule, which is the half the page cannot see. The looser the tier, the more of the season can be broken down, queued and reviewed in parallel, because an episode inherits little from its predecessor's approved takes. The tighter the tier, the more episode N's continuity state depends on episode N−1's *approved* state, so breakdown serializes behind delivery and one late pickup early in the season restates the inherited state of every episode after it. State the parallelism the tier permits at charter time; discovering it at breakdown means the dependency graph the queue was built on was already wrong.

### Season pressure and motif schedule

The season plan rates every episode on two independent axes, burst pressure, how much happens and how fast, and emotional intensity, how much it costs the people it happens to. the `sw-*` skills owns the rating; do not re-derive it. Production reads it as two separate budgets, one row per ordered episode:

| Column | Source | What it drives here |
|---|---|---|
| Burst pressure | season plan | shot count, cast and crowd load, contact and physics risk, coverage breadth, generated seconds |
| Emotional intensity | season plan | operating mode, performance coverage, close-up and eyeline discipline, review depth, retry ceiling |
| Dominant motif | this plan | the location, weather and light state, camera grammar, transition device and sound signature the episode is built on |
| Consequence | this plan | assigned mode and budget share, recorded with the reason |

Collapsing the two axes into one number is the expensive mistake. A parked-car two-hander is low burst and can be the highest-intensity hour of the season; a schedule that tracks only event volume marks it small, assigns it the speed lane, and under-covers the faces and timing that carry the season's best material. Assign the mode from the intensity axis and the volume from the burst axis.

**No dominant motif may run across more than two or three consecutive episodes without a declared reason.** A look repeated every week stops reading as a choice and becomes the show's wallpaper, so the episode that needs that rain, that lens or that cue to *mean* something has nothing left to spend. The second cost is invisible: with no contrast between neighbours, a slow slide in a location or wardrobe asset has nothing to fail against and surfaces at season assembly instead of at dailies. Derive the motif schedule from the season contract, never from a rotation.

## Planning batch and docking point

Plan one unit to contract depth at a time, one sequence in a film, one episode in a series, and keep everything beyond it at card depth: purpose, entry and exit state, obligations, risk.

- **Roll forward when the planning runway drops below the threshold recorded in the charter.** The project sets that threshold; this skill supplies no number, and a threshold nobody wrote down becomes "when we run out", which stalls the queue mid-sequence. This is planning depth only. The story runway check in the series contract is a design-time question answered at bible time and when a season is added, and re-running it per unit converts a design instrument into a rationing queue.
- **Do not break a season down to shot depth in advance.** The first delivered footage re-specifies the shots after it, and a detailed plan that is now wrong is worse than no plan, because it is already queued.
- **A planning batch ends at a dock, not in the queue.** Report what was planned, what queueing it would cost, what is unresolved, and a short menu of next actions, then stop. Generation is a separately authorized step, and a planning run that flows straight into it converts an unreviewed plan into spend: the review that would have caught the error now happens on rendered footage.
- **Invoked in an existing project with no request, produce a project-state diagnosis and stop.** Name the stage, what is approved, stale or blocked, which artifacts are missing or present-but-empty, and the smallest next action. Do not plan and do not queue, a bare invocation is the one call where the user has stated no intent, and guessing it wrong is the guess that spends money.

## Reserve enforcement at breakdown

A series holds an endgame reserve, material that can only be spent once, with an unlock milestone per entry. the `sw-*` skills authors that ledger; production owns the point at which a draw stops being reversible. Ask both questions before any unit's breakdown is queued.

1. **Does any shot in this unit render reserve material, and is that entry's unlock already true in approved material**, not in planned material, not in a card? A draw without a licensed unlock is a stop and a return to planning, never a note carried into the queue.
2. **After this unit, name what is still undrawn.** "Nothing specific" means the season has already spent its ending and the remaining episodes are executing a plan with no destination.

On the page a premature draw costs a rewrite. In the queue it costs the render, and once the material is cut and seen the audience holds it; no later pass buys it back.

Planned reserve material is not continuity state and never enters a shot contract or an input packet. A shot conditioned on a reveal the audience has not been given stages information the film has not released, and the leak arrives as footage rather than as a line that could still have been cut. [FP-06]

The restriction is on one-shot capital, not on how much a unit may contain. A sequence that advances several threads, settles a standing problem and moves a relationship is a strong unit, not an overspend; a schedule that rations content to look thrifty produces the flat, competent middle the ledger exists to prevent.

## Append-only plan lock

Once any shot in a sequence has been approved, that sequence's cards are locked. Later planning appends units at the tail; it does not edit a locked unit.

- Editing a locked unit requires an explicit instruction and is delivered with the list of approved work it invalidates and that work's recorded cost from the run ledger [FP-13]. Upstream of rendered material a plan edit discards footage that was paid for, so the price is stated before the edit rather than discovered after it.
- The drafting and queue loop never appends a unit on its own. Length is owned by the charter and the order, not by momentum inside a run.
- A locked unit that is genuinely wrong is re-planned as an amendment carrying a change record of downstream impacts, on the same terms as a change after structure lock.

## Artifact ownership

State the write class of every file the project keeps, at scaffold time, so it is known before anyone edits.

| Class | Who writes it | Rule |
|---|---|---|
| Skill-owned | this skill, regenerated whole | Derived views: shot manifest, dependency queue, KPI dashboard. Never hand-edit one; the edit is lost at the next regeneration and nothing records that it existed. |
| Co-owned | this skill, inside one delimited region | Charter, season plan, bible pages. Rewrite the marked region only; everything outside it is protected material. |
| User-owned | the user | Script, briefs, rights records, supplied references. Read and cite; propose a change, never make one. |
| Append-only | this skill, at the tail | Run ledger, checkpoint log, decision log. A correction is a new entry naming the one it corrects, never a rewritten row. |

A derived view regenerated over a hand-written note deletes a production decision and leaves no trace that a decision was ever made, the same failure as a state entry dropped instead of retired in [assets-continuity-lineage.md](assets-continuity-lineage.md), one layer up.

## Completed, current, and reserved beat firewall

Keep a completed, current, and reserved beat firewall for every scene. Completed beats are accepted visible facts; the current beat is the next required delta; reserved beats are future work and must not be pre-completed by convenience.

If an accepted deviation completes a future beat, remove that beat from downstream work and recalculate the next delta. A rejected deviation is not canonical, even when it looks useful; it may inform diagnosis but cannot advance the schedule. [FP-06]

## Scene and coverage planning

The Scene level's scene card may already exist upstream: a screenplay developed with the `sw-*` skills emits one per scene. Adopt it instead of re-deriving it, and carry three of its fields into the shot manifest, because nothing downstream reconstructs them, **truth / audience knowledge / character knowledge**, without which dramatic irony cannot be stated in a shot contract at all; the **audience question**, which the coverage has to keep alive; and the **failure condition**, which becomes an acceptance gate, since a take can satisfy its prompt and still trip it.

For every scene establish:

- narrative purpose, start/end story state, story time and location state;
- load-bearing performance intent from the scene card, carried using the **Performance handoff** in [assets-continuity-lineage.md](assets-continuity-lineage.md); [FP-22]
- cast, wardrobe/injury, props/ownership, entrances/exits, geography, axis and eyelines;
- master/establishing view for spatial literacy;
- singles, two-shots, and over-the-shoulders for performance and eyelines;
- inserts and reactions for props, hands, information, time compression and edit cover;
- exits/transitions and handles for adjacent scenes;
- alternative coverage for identity, hand/contact, crowd, exact-text, dialogue, speed, or physics risks.

If a proposed shot contains several independent `and then` events, separate beats before deciding whether to split the shot.

## Shot contract

Every queued shot needs:

```text
Identity: film/sequence/scene/beat/shot ID, owner, risk, priority
Narrative: purpose, start state, one primary delta, end state
Performance when applicable: approved beat-record reference and incoming/outgoing obligations, including response timing and residue
Entities: required/forbidden and passport/state versions
Invariants: attributes that must hold constant for the whole interval and still match at the boundary with adjacent shots
Population: exact counts of people and continuity-critical props; whether the set is closed
Space: floor plan, landmarks, axis, screen direction, eyelines, entrance/exit
Camera: size, side/height, lens feel, movement, focus, cut/continuation, handles
Look: light, exposure, grade, palette, material, weather, VFX intent
Sound: speaker, exact dialogue/language, room tone, foley, music/silence, layer assignment
Inputs: reference IDs/hashes/roles/packet order/admitted and denied scope/inheritance exclusions/rights
Prompt and parameters: version, platform/model/task/aspect/duration/format/audio
Spec channels: which channel enforces ratio, duration, resolution, audio
Acceptance: hard gates, rubric, neighbor compatibility, route rules
Provenance: parent run, one change, output hash, reviewer, decision, actual time/cost
```

Two contract lines the delta model does not supply on its own:

- **Invariants** are inherited from scene state, not re-described as prose inside the action. A start state plus one delta says what changes; it never says which unchanged things were required to stay unchanged. Invariants are what the neighbor shot and QC compare at the interval boundary, and what a retry must preserve. Carry them as opaque identifiers that resolve to a state entry, never by restating the attribute in each shot, which is exactly how two shots drift apart. Pick invariant IDs that name a slot rather than its content, so a change to the pinned attribute is a version bump instead of an edit to every shot that inherits it.
- **Population** bounds quantity, which `required/forbidden` does not. Duplication, extra figures and silently added props are only detectable against a declared count and a closed/open flag. How a prompt phrases a count belongs to `video-shot-prompts`; the schedule is what makes the count inheritable across shots and checkable after the run.

Never assume one platform's request schema is portable. Keep prompt text and runtime parameters separate.

## Shot-to-job mapping

A generation job is not a shot. Decide and record the mapping for every queued shot:

- **one job, one shot**, the default; state in the request that the job runs continuously with no internal cut;
- **one job, several shots**, internal cuts written into one request. This buys cut-adjacent continuity and costs retry granularity: the job is the unit of re-run, so no internal shot can be redone alone. Choose it only where that coupling is worth paying for;
- **several jobs, one shot**, a split for risk, length, capacity, or coverage, reassembled in the edit.

Accounting stays per shot whatever the mapping. Record, for every job output, the shot IDs it delivers and their in/out points, so review, acceptance, retry counts, coverage, and cost attribute to shots rather than to jobs. A job carrying several shots is accepted per interval; one unusable interval does not approve the others.

Treat job capacity as a shot-design constraint. Record the platform's current per-job ceilings, clip length, reference slots, permitted cut structure, and which decisions have a runtime control at all, and check each shot's entity set and beat count against them at breakdown. A shot that exceeds capacity is a split or a pre-composite decision made before queueing, not after a failed run. Capacities are platform- and date-specific; re-read them at charter time.

Handles are bought, not assumed: head and tail exist only where a shot was requested longer than its cut length. Decide the allowance at breakdown, how much margin, and on which shots. Action, overlapping dialogue, and any cut the edit may still slide need it; locked-off inserts, plates and textures do not. A second of head and tail on an eight-second shot is a quarter of that shot's cost and lands in `waste_rate` and `cost_per_approved_second` as generated seconds that never enter the cut, so buy it knowingly per shot rather than as a blanket surcharge. How a request asks for the extra length belongs to `video-shot-prompts`; the allowance and its cost are production decisions.

## Spec channel of record

For every delivery spec, aspect and framing, duration, resolution, frame rate, audio presence, record which channel enforces it: a runtime parameter, a sentence in the prompt, or geometry drawn into the picture. They are not interchangeable, and only the runtime container binds delivery.

- Bars, mattes, or a wider ratio drawn inside the picture are content. They are baked in, they do not change the container, and conform, reframe, safe areas, and archive specs must be planned against both facts.
- Timing written into prompt text is editorial notation, not a render budget. Give each shot a target duration in the manifest, compare it with the delivered clip length in the ledger, and treat a systematic gap as a shot-design or coverage problem rather than a wording problem. How a prompt should phrase timing belongs to `video-shot-prompts`; the reconciliation is a production control.
- Where a decision could have been set by a runtime control but was written in prose instead, mark it unenforced in the shot contract. Nothing in the record will show whether the model honored it.
- Where both channels state the same spec, keep them equal deliberately and re-check both after any parameter change.

Requested picture geometry and in-text beat timing diverge from the delivered container and duration often enough to make reconciliation a standing duty rather than an assumption about model behavior.

## End-to-end gates

1. **Development**, charter, rights, format, budget, risks.
2. **Script/bible**, story and state machines; canonical hero assets approved.
3. **Breakdown/risk**, hierarchy, floor plans, entity schedules, coverage and fail routes; reserve position checked before anything is queued.
4. **Previz/anchors**, animatic/blockout; only necessary diagrams/storyboards/keyframes/clay.
5. **Blocking generation**, low-cost narrative and edit feasibility; an end-to-end rough cut exists.
6. **Final shot generation**, locked contracts; outputs enter incoming, never overwrite approved.
7. **Dailies/selects**, full-media review, fidelity before consistency, only approved memory promotion.
8. **Structure lock/pickups**, rough cut exposes missing coverage; downstream impact controlled.
9. **VFX/cleanup/conform/color/sound/subtitles**, normalize and finish rather than endlessly regenerate.
10. **Final QC/master/archive**, complete playback, technical/content/rights checks, independent approvals.

## Queue and dependency graph

Safe to parallelize:

- independent establishing, insert, reaction, cutaway, plate, and texture shots;
- scenes with locked canonical assets and no immediate handoff dependency;
- asset preparation and conditioning passes, which run in their own lane and never mutate approved state;
- review, sound spotting, VFX breakdown, or subtitle preparation that does not mutate the same truth.

Serialize:

- extension chains and continuous action;
- evolving wardrobe, injury, weather, and prop ownership;
- any next shot dependent on an approved prior last frame or motion vector;
- canonical or approved-memory promotion;
- hero close-ups before scene geography/blocking is approved.

Batch only compatible platform, model, task, ratio, resolution, format, reference-packet version, and rubric. Otherwise failures cannot be attributed.

Queue by the recorded shot-to-job mapping. A job carrying several shots is one unit of re-run and cannot be re-queued shot by shot, so its shots are scheduled, reviewed, and retried together.
