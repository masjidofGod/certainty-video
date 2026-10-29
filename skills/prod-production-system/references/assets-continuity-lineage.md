# Assets, continuity, lineage, and rollback

Read this file when building the creative bible, asset registry, scene state, shot handoffs, generation ledger, or recovery plan.

## Before creating a project scaffold

Verify preconditions before writing a multi-file production project, and if any fails write nothing at all.

- The charter decisions this skill cannot invent are present, platform and displayed model, aspect and master specs, rights position, delivery surface, and a script or treatment exists at the agreed stage.
- Distinguish missing from present-but-empty, and say which it was. An empty passport, an empty ledger and an empty state file all satisfy a file check and none of them is usable.
- On failure, name the exact missing path or decision and the step that produces it. A half-written scaffold is worse than none: it reads as a project, so the next run treats its gaps as state and plans on top of them.
- A read-only request, a critique, a cost estimate, a routing question, a look at an existing plan, never requires scaffolding. Only a request that writes production state does, and creating a project in order to answer a question is an unrequested write.

These preconditions govern a production scaffold, not a bounded asset proposal. If the user authorizes free design within a stated scope, write a finite named draft roster with design assumptions and continue the authorized planning; do not repeatedly request nonexistent character sheets or pretend the proposal is approved. Unsettled runtime facts stay unknown and block only the step that needs them. Free design grants neither unlimited scope nor paid media generation. [FP-20]

## Creative-bible passports

Every passport has a stable ID, version, owner, rights status, `draft/approved/retired` state, approval date, and hashes.

`rights_status` is a cleared/not-cleared decision, not a label. Where an asset carries a real person's likeness or voice, a photograph used as an identity reference, a recording used as a voice reference, establish before it enters the bible who the person is, who obtained their consent for synthetic generation across this project's uses, territories and duration, and what they excluded; record that, its date and its expiry on the passport. An asset whose consent cannot be established stays out of the bible and out of every input packet: it is not a risk to manage downstream, because every shot generated from it inherits the same defect and no finishing pass removes it. [FP-03]

### Character and voice

- face/hair/skin/build/posture/handedness/gait and stable identifying traits;
- approved views, framing scales, and expression references selected for the film's actual structural and performance needs;
- voice language/accent/register/timbre/tempo/pronunciation dictionary and rights;
- relevant established behavior: working tempo, use of space and objects, posture/gait, partner-specific gaze and speech, and responses under pressure; distinguish stable traits from scene-local proposals rather than assigning stock gestures by age or culture;
- closed wardrobe and accessories, plus state-specific wet/damaged/injured/aged versions;
- forbidden drift and recurring blocking/eyeline relationships.

### Location, prop, and look

- location floor plan, entrances/exits, axis, camera positions, landmarks, materials, light direction, weather/time states, room tone;
- prop geometry/scale/material/moving parts, owner/hand, appearance/disappearance and state machine;
- exact graphics as clean artwork for post when text fidelity matters;
- camera grammar, style/material contract, color script, VFX grammar, sound bible and subtitle style.

A new wardrobe, injury, weather, lighting, or prop state is a new asset/version. Do not overwrite the base state or combine conflicting states in one sheet.

## Performance handoff [FP-22]

For a beat whose meaning depends on a performance, keep one compact record alongside its scene state. This section owns the planning field meanings; it is not a runtime API, a new state engine or a second character bible. An insert with no performance obligation needs no record. Consume the writer's approved intent; where it is absent, use the user's brief and label scene-local proposals rather than inventing canon.

| Field | What survives into each consuming shot |
|---|---|
| `intent` | Character, recipient, current pursuit/tactic and knowledge boundary; what is concealed from whom if that matters. |
| `baseline` | The established habit, physical condition and performance register needed to distinguish this response; reference the existing passport, not a competing biography. |
| `trigger` | The available word/event/contact that permits the response, or the reason a response is withheld. |
| `response` | The authored action or visible/audible change and partner response that carry the beat; preserve ambiguity where intended. |
| `exit_residue` | Attention, support/contact, unfinished action, tension or recovery that remains, the shot that inherits it, and any elapsed time/event permitting a change. |
| `acceptance` | The observable wrong timing, wrong tactic, lost register or reset that would break this beat, and the evidence needed to judge it. |

Record only load-bearing fields; leave an unknown unknown and omit irrelevant cue detail. The prompt director composes the actual expression, gaze, body and breath instructions; the plan does not pre-animate every muscle. One causal response may contain several coordinated actions and a pause. Choose coverage to preserve that response, including the receiver's reaction; split contact only with a readable bridge for the story event.

Planned response and observed response stay separate. Approved evidence amends the existing scene/character state through the promotion protocol; a frame can establish posture but not breath phase or response timing. Do not promote a reviewer interpretation into objective inner truth. Match the incoming performance state at a direct cut, including ongoing exertion or a still-incomplete response; after an authorized time gap, use the state the story now warrants. Never pin an emotion permanently as an identity invariant.

Example of a prospective record, not rendered evidence:

```yaml
performance:
  intent: courier completes the handoff without revealing that she needs this job
  baseline: practiced handling; still recovering from the stairs; restrained register
  trigger: shopkeeper says the closing date; courier had no prior knowledge
  response: supported parcel transfer completes after the date; courier does not answer
  exit_residue: next reaction shot inherits incomplete breathing recovery and attention on parcel
  acceptance: no early release, replayed revelation or unsupported reset; inspect both clips and sound
```

Carry the record's approved obligations into the shot manifest and the receiving prompt brief. At selects, compare the performance in context with its neighbor, not only identity and prop position. If a kept take changes a downstream obligation, amend the record explicitly and identify affected shots; do not quietly substitute the latest take.

## Film asset views and delivery [FP-20]

Use this section only when a film asset task requests independent views or needs a scoped design roster. Standalone still prompts and still-image inspection remain with `certainty:studio`; this section owns the film registry and delivery contract, not image generation or a new packaging service.

1. **Bound the roster.** Record each included entity, asset purpose, design assumption, and approval state. Whole characters, independently designed creatures, and core props needing structural explanation can justify complete view sets. Ordinary coats, trousers, belts, or shoes remain part of wardrobe unless the user gives them an independent structural purpose. Request a useful detail close-up when evidence is insufficient; splitting accessories into full sets is not progress.
2. **Lock the requested view set.** Use the user's confirmed angles and count; five views are not a universal definition. For a request specifying front, right, back, left, and overhead, keep those five. Define right/left as subject-relative or camera-relative before writing the contracts. Overhead places the camera above the subject rather than making the subject bow; allow physically plausible foreshortening and occlusion. Do not demand impossible simultaneous visibility.
3. **Keep output units independent.** Each entity × view gets one self-contained submission producing one image of that specified view. An independent five-view request is five such submissions, never one contact sheet, multi-panel turnaround, or a larger image cropped to masquerade as independent generations. Keep roster notes, filenames, ZIP instructions, and batch counts outside the picture description.
4. **Carry the authorized reference.** Attach the actual input in every submission and state its authority for identity, wardrobe, geometry, material, light, or style, with exclusions. A previous message, `same as above`, or a generation ID is not an attachment. Pixels govern only the dimensions granted to them; text supplies the view and necessary visibility changes without competing descriptions of the same property. Unseen design details remain named assumptions until approved. If an attachment is missing, the packet is prepared but not submission-ready; do not silently switch to generation from scratch.
5. **Preserve approval and purpose.** Keep the original approved image, derivative candidates, and rejected versions distinct. A candidate does not automatically become the next view's identity master; promotion requires the existing approval gate [FP-05]. Approval of a natural casting or wardrobe reference carries its stated purpose and visual quality target into the batch. Batch size does not authorize CGI, game-model display, or promotional styling, and quality approval does not approve new designs or new entities.
6. **Reconcile delivery.** ZIP is a packaging layer. For N included entities and five requested independent views, the gate expects exactly 5 × N qualified image files, organized by entity folder and view filename. Reconcile roster, actual files, decoded image validity, angles, duplicate hashes and visually repeated views, missing items, and failed items before claiming completion. Empty directories, duplicate images, text files, and failed candidates do not fill a slot. If files were not produced or inspected, record delivery as `not_run` or incomplete rather than claim a finished archive.

This is a planning and acceptance policy, not a guarantee of pixel or identity preservation across generated views. Stop expansion at the scoped roster and stop delivery approval at the first unresolved required slot; return the exact missing or failed items instead of filling them with substitutes.

## Retirement

An asset version, a state entry, or an invariant slot leaves the system only when it is retired by name. Record who retired it, what stands in its place, and the story position from which it no longer applies; leave the entry in the registry as `retired`, because the registry is a history and not an inventory. [FP-13]

Omission is never deletion. A wardrobe state dropped from a sheet is indistinguishable from one that was never written, so every shot inheriting that slot keeps resolving it and nobody can name the moment the constraint was lost.

Retire forward only. A decision that was wrong from the start is an amendment with a new version and a change record, not a retirement: a retirement backdated into a scene where it did not happen makes the lineage unreadable, and the lineage is what a rollback trusts.

Retiring an asset does not retire the takes made from it. Approved shots keep the version they were generated against and stay valid, retirement bars future use, it does not invalidate the past.

## Reference authority

Name, for each attribute class the film must hold, identity, wardrobe, geometry, material, palette, grade, voice, motion, the single authority of record: an approved asset, or the prompt text. Record it in the bible. Never specify the same class in both channels; when they disagree, no record can say which one the take obeyed. A class established in pixels during asset preparation is thereafter carried by reference and dropped from prompt text.

- Scope a reference's authority to named classes, per use, and scope it by default: an asset confers no camera position, framing, composition, or crop unless the shot contract grants it. Keep that exclusion in the registry entry, not only in the prompt.
- One asset may be admitted on one channel and barred on the rest, its picture but not its sound, its geometry but not its light. Register admitted and denied channels per use, because the same asset can hold different authority in different shots.
- Where the interface binds references by position rather than by name, attachment order is part of the contract. Record the ordered packet and reproduce it exactly on retry, or the runs are not comparable.
- The provider's asset record is not the registry. Its category may be machine-assigned, its description empty, its name whatever the uploader typed; none of that is evidence of what the asset may govern, and some projects register no assets with the provider at all. Class, role, admitted channels, version, and rights live in the production registry and are restated in the input packet.

## Prompt blocks as versioned assets

Long shot prompts are assembled, not written. Any constraint block that recurs across shots is an asset: stable ID, version, owner, state, hash, and the passport version it was derived from. A shot's submitted text is a composition, an ordered list of block versions plus that shot's own delta text. Which categories of block a project keeps, and what they say, is the project's business; only the way blocks are identified, versioned and recorded is general.

- Record the composing block IDs and versions in the run ledger beside the prompt hash. Without them, one changed variable cannot be audited inside a long prompt, and two runs differing by one line read as two unrelated texts.
- Editing a block creates a new block version and marks every shot composed from the previous version stale. Decide per stale shot: re-render, or keep the approved take and pin it to the block version it actually used.
- When a shot must depart from a standing block, write the departure as an explicit precedence declaration that names the rule it supersedes, rather than as a contradicting line appended to the tail. A named supersession is auditable and survives recomposition; a bare contradiction leaves a hash describing text the run never honored.
- Fold a correction back into the block once it stops being a one-shot exception and starts recurring. A block that has accumulated per-shot patches has lost its authority as an invariant.
- A block rewritten in another authoring language is a language variant of the same block ID. Any count or audit that scans prompt text must be language-aware; do not trust a platform-supplied language field, which may report a single language for a mixed-language project.
- A block states values, never citations. Where the authority of record for an attribute class is the prompt text, the block carries that class's literal values and never refers to the passport, to another block, or to what an earlier block already said: a citation is legible to whoever maintains the registry and to nothing downstream, so a bound expressed as a citation binds nothing once the composition is submitted. Where the authority of record is an approved asset, the class stays out of the block entirely under **Reference authority**, resolving it into text there would put the same class on two channels. The derivation itself lives in the block's metadata, never in the text that gets sent.
- Blocks carry project vocabulary, not craft rules. Version them with the bible and keep them inside the project.

Block composition is a production hygiene control for attribution and rollback. No controlled evidence links it to output quality; do not present it as a quality lever.

## Three distinct continuity stores

### Canonical bank

Human-approved identity, location, prop, voice, style, and state truth. A generation can never replace it automatically.

### Approved memory

A small set of high-information frames or clips promoted from accepted shots only after:

- correct identity/entity/location fidelity;
- no disqualifying artifact or motion blur for its intended use;
- prompt/story adherence and cross-shot compatibility;
- source shot/timecode/crop/use boundary recorded.

### Local handoff

Transient neighbor state: last approved pose/frame or action tail, positions, screen direction, camera velocity, light/color, prop owner, and room tone. It serves adjacent continuity and never overrides canonical truth.

These stores are an external production design inspired partly by long-video research; they are not claimed as Seedance internals. `return_last_frame`, where documented, is only transport. A last frame must pass QC before promotion.

### Conditioning before promotion

A candidate may need a bounded conditioning pass before it can serve as approved memory: removing an overlay, badge, or incidental marking the generator added, cropping to the usable region, or repairing one local defect. Conditioning is neither editing nor re-authoring:

- the conditioned asset is a new version whose parent is the accepted source, with the single operation recorded;
- it is bounded to the named operation and may not touch identity, wardrobe, state, or geography; a candidate needing more than that fails promotion instead;
- the unconditioned source is retained, because it, not the repair, is what the run produced.

Run asset preparation as its own lane, with its own queue, ceiling, and reviewer. Preparation is many short single-operation commands against existing images, a register quite distinct from long shot specifications; mixing the two makes cleanup register as shot retries and inflates the shot ledger.

### Amending canonical state from an approved take

Planning states what should be true; the accepted take states what is. Where an approved take's observed state has departed from the passport it was generated against, an injury that healed differently, a sleeve that stayed rolled, a prop that ended in the other hand, and the take is kept, the passport is now wrong for every shot after it and must be amended. [FP-19]

- the amendment is a new immutable asset version whose parent is the previous version and whose evidence is the accepted take's shot ID, timecode and hash; it never edits the version already used;
- it carries the same human approval as any canonical entry and lands at a scene or checkpoint boundary, listing the downstream shots whose invariant slots now resolve to the new version;
- shots already approved against the earlier version keep it: re-render or pin, decided per shot, exactly as for a stale prompt block.

This is the only path from a generated result into canonical truth, and it does not soften the firewall, only an approved take may be promoted, a rejected one never becomes identity truth [FP-05], and nothing is promoted automatically. A bible that is never amended stops describing the film that was actually made.

## Asset versions across episodes

In series work an asset's versions form a chain read by **story position**, not by registry recency. Every version records the earliest season, episode and scene at which it becomes canonical, and a shot resolves its invariant slots to the latest version effective at its own position. [FP-04]

- Production order is not story order. An episode generated late can precede one generated early, and a registry read as "newest wins" dresses that shot in an injury it has not received yet, a defect no per-shot review catches, because the take is internally correct.
- Standing classes, base identity, standing wardrobe, a recurring location's default state, camera and color grammar, live at the season level and are inherited. An episode may add a state-specific version; it may not silently redefine a standing class. A redefinition is a season-bible amendment carrying the list of episodes it restates. [FP-19]
- Re-verify a returning asset against the canonical bank after an absence of several episodes. Each approved step in a long version chain passes on its own; their sum is a different character, and nothing inside a per-episode review is positioned to see it.
- Approved memory serves the episode it came from unless its use boundary says otherwise. A promoted frame carries that episode's light, wardrobe state and room tone, so a handoff across an episode boundary imports all three.

## Continuation relation and accepted-state firewall

Choose one continuation relation before preparing inputs: same-shot seamless, intentional next shot, bridge known states, repair tail, or reanchor drift. The relation names editorial intent; it does not imply a provider feature. [FP-15]

Use same-shot seamless only inside the same scene when geography and open motion genuinely continue. A scene boundary defaults to an intentional next shot, which may preserve story continuity without promising frame continuity.

An accepted source carries its existing state. Prompt text describes only the delta required after that accepted state, rather than replaying the full source contract. A rejected output is diagnostic evidence only and never becomes canonical, approved memory, or a handoff source. [FP-05]

Do not put a numeric retry, chain, work-slice, or review-cycle ceiling into the production deliverable unless the user or project provided it. Internal agent execution defaults stay outside the deliverable. When the production ceiling is absent, keep it unknown and request it only when it changes the plan. [FP-14]

## Continuity state and entity schedule

```yaml
scene_id: SC-023
story_time: "Day 4 / dawn"
location_state: LOC-007-dawn-rain-v02
screen_axis: door-to-window
characters:
  CHAR-001:
    position: frame-left beside table
    wardrobe: WARD-001-wet-v03
    injury: INJ-001-cheek-cut-v01
    gaze: CHAR-002
    held_props: [PROP-014-letter-open]
props:
  PROP-014:
    state: open
    owner: CHAR-001
    hand: right
lighting: LIGHT-SC023-window-left-v02
audio: SOUND-SC023-rain-roomtone-v02
invariant_slots:  # what a shot's invariant IDs resolve to
  WARDROBE-A@v3: WARD-001-wet-v03
  KEYLIGHT-SC023@v2: LIGHT-SC023-window-left-v02
```

```yaml
shot_id: SH-023-040
required: [CHAR-001, CHAR-002, PROP-014, LOC-007]
forbidden: [CHAR-003, PROP-014-letter-sealed]
invariants: [WARDROBE-A@v3, KEYLIGHT-SC023@v2]
population: {people: 2, key_props: 1, closed: true}
start_state: CHAR-001 holds the open letter in the right hand
primary_delta: PROP-014 transfers to table center
end_state: both characters remain seated; letter lies open at table center
entrance_exit: nobody enters or exits
```

Each shot reads the prior approved state and submits exactly its approved delta. Scene rollback replays only accepted deltas from the checkpoint.

## Registry and run ledger

Asset registry fields:

```text
asset_id, entity_id, state, version, owner, rights_status, source_paths,
allowed_attributes, excluded_attributes, status, approval, sha256
```

Run ledger fields:

```text
run_id, parent_run, shot_id, timestamp, platform, native_tool, connector,
requested_model, returned_model_label, verified_backend_model, document_version,
prompt text/hash, prompt_block_ids/versions, parameters,
reference IDs/hashes/roles, one changed variable, retry_class,
delivered_shot_ids/in-out, output path/hash/duration/spec,
queue/generation/review/human time, billed cost,
hard gates, scores, timecoded defects, reviewer, decision, route
```

For each historical field retain its evidence source and status: directly inspected, `reported`, or `unknown`. A wrapper label is not a verified backend model; a generation ID is only a source identifier, not a seed, retrieval URL, reproducible recipe, or identity lock. Record hashes and dimensions only from files actually read. An original user request is not the verified submitted prompt, and missing invocation or post-processing records establish no negative claim about what occurred. Preserve unknowns instead of completing a plausible history. [FP-21]

Record a changed provider, requested/returned model, native tool or connector, or reference handling as a process change with the known before/after facts. Keep it out of unchanged-condition comparisons. Later derivative runs cannot establish an earlier image's origin. One accepted result supports a scoped quality decision, not a model ranking, success rate, or causal finding about the prompt or skills. [FP-21]

Input packet fields:

```text
reference_id, version, packet_order, role, allowed_attributes, excluded_attributes,
sha256, rights
```

Never retain credentials, cookies, session material, signed media queries, or private URLs. If provider task/URLs expire, ingest the authorized output promptly, hash it, and retain a sanitized source identifier.

## Stable IDs and filenames

```text
FILM-ORCHID
SEASON-02
EP-02-005
SQ-030
SC-030-012
BT-030-012-04
SH-030-012-040
CHAR-003 / LOC-007 / PROP-014
```

IDs are never reused because editorial order changes. Status metadata is authoritative; `APPROVED` in filenames is only a readable aid.

In series work the episode segment prefixes every unit ID below it, and every run-ledger row carries it. Scene and shot numbers repeat in every episode, and a manifest that cannot tell one episode's `SC-030-012` from another's attributes a retry, a cost and an approval to the wrong hour, after which no per-episode budget, waste rate or coverage count means anything.

Example:

```text
FILM-ORCHID_SH-030-012-040_take-003_run-r017_prompt-p004_ref-r006_model-full-id_720p_v001.mov
FILM-ORCHID_CHAR-003_wardrobe-rain_v005_APPROVED.png
FILM-ORCHID_SC-030-012_continuity-state_v012.yaml
```

## Checkpoints and rollback

Create immutable checkpoints after bible lock, previz/anchor lock, approved-shot lock, picture structure lock, sound/color lock, and final master. Save script/bible versions, state snapshot, approved hashes, timeline/EDL, open defects/routes, budget, tool/model/platform/doc versions and approvals.

Rollback rules, including the extension-chain boundary [FP-15]:

- retry from the parent approved run, never a rejected child;
- if state/axis/wardrobe was corrupted, return to scene-start checkpoint and replay approved deltas;
- after structure lock, require a change record listing downstream VFX/sound/subtitle/color impacts;
- test a model/platform update as a new branch and regression suite; never overwrite approved renders.
