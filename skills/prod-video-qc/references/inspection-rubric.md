# Inspection rubric and report schema

Read this file when auditing a generated clip or multi-shot sequence.

## Evidence intake

Record exactly what is available:

- original prompt and runtime platform/model/version/parameters if visible;
- reference assets and intended roles;
- full video and actual audio, or only a subset of frames/screenshots;
- opening, representative middle, ending, every transition, and high-risk action/dialogue/text timecodes;
- neighboring shot/end-state requirements;
- delivery, rights and acceptance criteria.

If evidence is incomplete, continue with bounded findings and label uncovered dimensions unknown. Do not turn the user's failure description into a direct visual observation.

Evidence-resolution rules:

- a screenshot can prove visible state only at that frame;
- spaced frames can suggest but not prove continuous motion, stability, physics or lip-sync;
- an unmuted/player icon proves player state, not audio presence or quality;
- actual audio, decode/waveform/ASR or human listening is needed for audio claims;
- automatic metrics and thumbnails are secondary diagnostics, not approval evidence;
- one qualifying frame settles a presence requirement, but no finite sampling settles a prohibition: report every absence result as bounded by the interval covered and the frame area actually inspected, never as proven absence;
- coverage has a spatial axis as well as a temporal one: a single frame or a single region breaks a suppression requirement, so partial coverage never clears one; [QC-21]
- a reduced-tier run and a delivery-spec run of the same contract are not interchangeable evidence.

Keep original user requirements, inspected media features, reported user approval, and inferred causes in separate fields. A single accepted result is not an ablation, a success rate, or a comparison of models or skills. Record native tool, connector, requested model, returned label, and verified backend separately when provenance matters; mark uninspected history `reported` and hidden values `unknown`. A missing invocation or post-processing record is not proof that the step never happened, and a generation ID is not a seed or an attached image. Photographic appearance establishes neither camera capture nor detector performance. [QC-02]

A run at lower resolution, shorter duration or a draft quality setting can settle coarse adherence, entity presence and count, blocking, action and beat order, gross camera behavior, obvious prohibition violations. It cannot clear fine artifacts, small or short-lived characters, finger and contact anatomy, grain and texture, edge quality, or lip-sync. Say which dimensions the reduced-tier evidence cleared, and label the rest unknown at delivery spec. A pass earned at a probe tier never transfers to the delivery master: the master is re-inspected on exactly the dimensions the tier could not settle, and the verdict names both scopes. [QC-26]

**Reconcile the declaration surfaces, then test satisfiability.** Timing, length, format and take structure may be declared in the prompt text, in the runtime parameters, or in both, and where both carry the same spec the two can disagree. Some contracts state none of this in text and leave it entirely to the parameters; that silence is a drafting choice, not a defect, and there is nothing to reconcile. Where the text does declare any of it, check before scoring adherence that the contract was satisfiable as issued:

- does the written schedule fit inside the requested runtime;
- do the declared take structure and the requested duration and format agree;
- can the number of state changes asked for occur in the time available.

If the contract over-books its own runtime, the missing material is a contract defect. It routes to a contract fix, not to a regeneration, and charging it to the model is a misdiagnosis that no number of retries will correct. Record it as a finding against the contract, quoting both declared values and naming the surface each came from.

Where the surfaces agree, score them separately: against any written schedule, each beat's presence, order and realized time; against the parameters and the delivered file, total length, aspect, format and take structure. A beat that occurred but landed materially off its scheduled time is an adherence finding with an editorial consequence, not a cosmetic one. [QC-24]

## Hard gates

Fail before averaging if any material gate is unmet:

1. rights, safety, policy, delivery or required media specification;
2. correct required entities/identity/reference roles, with no critical extra entity;
3. required story beat and causal action result;
4. correct continuity-critical wardrobe/injury/prop/location/direction/end state;
5. no uneditable structural failure, severe artifact, wrong text/subtitle, or broken audio;
6. an editorially usable interval/transition or an approved repair route.

A beautiful but wrong character, missing prop, wrong end state, or unusable cut remains a failure. Where the reconciliation step under Evidence intake shows the contract was not satisfiable as issued, the resulting gap is reported as a contract defect and routed to a contract fix rather than counted as a gate failure of the take. [QC-24]

### Gates declared by the contract

Before applying the default gate list, harvest the gates the contract already states. Two forms occur: a named condition the contract declares sufficient on its own to reject the shot, and a block carrying a precedence or severity marker that the contract asserts governs where its own clauses conflict. Both are gates for this review, checked by name and reported individually.

An author-declared precedence is not silently replaced by the default one. A defect on a constraint the contract declared rejecting is a gate failure even where the default list would rate it Minor; a defect on a constraint the contract marked preferred rather than absolute is reported as a score, not as a blocker. Where the two orderings disagree, report both readings and state which one the verdict used.

When the contract declares no precedence, state the gate list applied before scoring, so the user can correct it rather than infer it from the verdict. [QC-19]

## Dimensions

Use pass/fail for acceptance and optionally 1–5 for comparison. Every score cites timecoded evidence.

### Prompt adherence

- exact entity counts and required/forbidden presence;
- reference identity/role fidelity;
- start state, action order, direction, contact/result and end state;
- camera, light/style, audio/dialogue/subtitle requirements.

**Check prohibitions one at a time.** Collect every exclusion the contract states, in whatever form it takes: a labeled exclusion section, a rider attached to one shot or panel, a positive requirement stated together with the counter-case it rejects, or an inventory the contract declares complete. For each, record the prohibited observable, the scope it binds (whole delivery, one shot, one interval, one entity), the evidence actually examined, and a verdict of pass / violated / not checkable. Never collapse the set into a single "no violations found".

A prohibition can bar anything the contract is able to name, not only entities. Whenever the contract negates something, restate that negation as a test another reviewer could run on the same evidence and reach the same verdict; where you cannot, record it as not checkable and say what evidence would settle it. Negated camera behavior, negated editorial events, negated color, negated legibility of lettering or captions, and negated styles all convert this way. Treat that as illustration, not as the list to check, the list to check is whatever this contract negates.

Separate two failures that look alike. A prohibition you cannot restate as a test another reviewer could run is *not checkable*, a limit on the review. A prohibition the generator could not have executed reading it alone is *inert*, and its violation is a finding against the contract rather than against the take. Inertness is established where the clause points at a document that was not submitted with it, since nothing at the other end of the pointer reached the generator; it is only suspected where the clause bounds a diffuse feature by how many there are, a reading that rests on an uncontrolled observation rather than a controlled comparison. Record which of the two applies and, for an inert clause, whether the inertness is established or suspected; they route differently. [QC-28]

Where the contract declares a list complete, the burden inverts: anything present in the evidence but absent from the list is a finding in its own right, independent of how well it is rendered. Report unlisted additions and unmet requirements as two separate lists, because they have different causes and different repairs. [QC-20]

**Reference audit.** Test the binding before judging fidelity, and record each result as its own finding class:

- *unused*, an asset was supplied but none of its declared attributes is visible; the roster and the output disagree about what was in play;
- *misbound*, a supplied attribute landed on a different element than the one it was assigned to;
- *conflated*, two distinct references resolved into one blended entity, or one reference split across two;
- *over-inherited*, the asset contributed on a channel it was not granted.

Then audit inheritance per channel. For each reference, record which channels the contract granted it, identity, geometry, material, palette, light, motion, voice, and check each granted channel for under-inheritance and each ungranted channel for leakage. Extend the check to the channels a contract usually leaves unnamed: an asset's own framing, camera position and lighting can arrive alongside the attribute that was actually wanted, so inspect them even when the contract says nothing about them.

Where the contract grants no channels and addresses a pile of assets collectively, say so. Adherence is then unscorable per asset; only the aggregate result can be judged, and "which asset caused this" stays unknown rather than being guessed. [QC-22]

### Multi-unit generations [QC-23]

Some generations declare more than one internal unit: the prompt segments itself into ordered parts, each carrying directions of its own, however that segmentation happens to be marked. When it does, evaluate the unit structure before the unit content:

- how many units were declared, in what order, and where each boundary actually landed in the result;
- whether a boundary required to be a discrete change of setup is one, rather than being served by a blended or uninterrupted substitute, a morph, a dissolve, a camera move that carries through, and whether any boundary appeared that was never declared;
- each unit against only the clauses that bind it.

Bind every clause to its declared scope before scoring. A clause stated for the whole generation is checked in every unit; a clause stated inside one unit is charged only against that unit. A later unit may legitimately contradict an earlier one: when the declaration itself holds an attribute fixed in one unit and calls for it to change in the next, the change is compliance, not a continuity failure. A finding filed against the wrong unit is a reporting error, not a lenient call.

Report per unit, then per job. A job whose units are each acceptable can still fail on structure, and one failed unit does not condemn the rest when its boundary is cuttable.

### Continuity

- identity/face/hair/build and voice;
- wardrobe, accessories, wet/damaged/injury/age state;
- prop geometry/count/state/owner/hand;
- location geometry/landmarks/weather/time/light;
- blocking, axis, screen direction, eyeline, entrance/exit;
- action/camera velocity, room tone and neighbor edit.

Verify fidelity to the correct entity before measuring self-consistency. A consistently wrong person does not pass continuity.

### Temporal stability and anatomy

- unrequested flicker, morphing, texture crawl, popping/disappearance;
- face/body/limb/finger topology and contact anatomy;
- object permanence, duplication and reflection copies;
- short-lived text/UI errors, motion blur and edge artifacts.

A contract may name one of these artifacts as part of the intended look, exposure flicker, a frame-to-frame brightness jump, a head-switching tear. Where it does, that artifact is scored not for its presence but against the character it was declared with: the right kind, in the right place, at the right strength and rate. An instance the contract did not name remains a defect, and so does a declared artifact that swallows a required beat, a face or a line of text. [QC-29]

Sampling density must match the risk. Sparse frames are insufficient for fast fingers, short text, transitions or lips.

Prohibitions drive sampling density rather than inheriting it: choose the interval and rate from the prohibition list, not from the action. Cover the frame as well as the timeline, a scene-wide exclusion, a suppression requirement or a closed inventory can be broken anywhere in the rectangle, so inspect periphery and corners, background population, reflective and out-of-focus areas, and any surface able to carry marks or characters, not only the subject. State the covered interval and the inspected areas in the verdict, alongside the evidence modality. [QC-21]

### Physics and action [QC-08]

- trajectory, speed/acceleration and gravity;
- visible contact before response;
- weight, momentum/inertia, follow-through and balance;
- material deformation, liquid/particle response and stable result;
- coherence between camera motion and subject motion.

Describe visible failure directly; label its cause as hypothesis.

### Camera and optics [QC-10]

- shot size, camera side/height/angle and intended lens feel;
- movement type/direction/speed, stability and focus target;
- axis/eyeline and transition/cut function;
- whether camera complexity hides or causes action unreadability.

### Observable acting [QC-09]

For character-led beats, read the declared performance intent and incoming/outgoing state before judging the cues. When no intent is supplied, assess observable adherence and technical coherence, state the missing dramatic basis and make only provisional interpretations. Do not invent a character motive in order to pass or fail a take. [QC-32]

| Check | Inspect and report |
|---|---|
| Stimulus and knowledge | What the character could hear, see or know before responding; the relevant word/event and response onset. A response during a line can be correct. An early reaction without a story basis is not rescued by an expressive face. |
| Tactic and relationship | How behavior serves the declared pursuit toward this partner, including a meaningful refusal or stillness. Does the partner notice, resist, accept or misread what happened? Preserve intended ambiguity rather than demand a uniquely readable emotion. |
| Expression and gaze | Target and changes of attention, onset/hold/release where meaningful, and whether the face remains coherent with the body and words. Eye/head order and blinks are checked only when specified or materially wrong for the event, never as universal acting laws. |
| Body and contact | Support, posture, effort, grip and release, with initiation and the recipient's response. Test the role's established behavior and current condition, not stereotyped movement for an age, culture or disability. |
| Breath and voice | Visible recovery, mouth behavior, phrase timing and any authorized breath sound. Check an unexplained reset or mismatch against effort and the handoff. Audio quality and continuous respiratory timing require moving/audio evidence. |
| Register and cue economy | The approved scale of performance, including broad comedy or exuberance. Redundant grimaces, sighs or gestures may flatten a beat; low motion is not by itself poor acting. Do not prefer the variant with more facial movement. |
| Readability and cut | Whether the chosen cue can be read at delivery size and whether the reaction's onset, unfinished action and residue survive the neighboring cut. Do not grade an invisible facial detail in a wide shot. |

Separate the observation from the interpretation: “the hand releases before the closing date is spoken” can be inspected; “she has already accepted the loss” is a reading against the story. A gaze direction, smile, breath or facial action is not proof of a real person's emotion, truthfulness or diagnosis. A still cannot establish listening, response delay, breath phase or deliberate stillness. Sparse logs remain reported evidence.

Use the contract's failure condition for severity. A missing load-bearing response or an early reaction that reveals unavailable knowledge can block the beat even when entity/prop gates pass. Cosmetic variation in a nonessential cue need not fail it. If all written cues occurred but the intended beat still does not read, report the contract/coverage gap and route it to the writer, director or producer; do not certify the performance from cue counts. Deliberate ambiguity, unresolved feeling and an absence of escalation can pass.

### Text and subtitles [QC-11]

- exact string, language, spelling, glyph stability and placement;
- timing, speaker, punctuation, line break, safe area and occlusion;
- consistency across frames/cuts and burned/sidecar requirement.

### Audio, dialogue and lip-sync

- audio stream/decode integrity;
- exact words/language/accent, speaker attribution, voice identity/naturalness;
- speech timing, mouth movement and phoneme-level sync when evidence permits;
- mouth movement in figures the contract lists as carrying no line;
- jaw, dentition or mouth-shape deformation at syllable peaks, reported against the identity gate rather than against sync;
- SFX causal alignment, room-tone/ambience continuity, music and level/seam;
- no unrequested dialogue, BGM, subtitles or silence.

Do not generalize a coarse mouth-motion correlation to exact dialogue or phoneme sync.

### Editorial usability

- complete usable interval, clean in/out, handles, and a stable ending except where the shot was specified to exit mid-movement;
- match to neighboring pose/state/direction/eyeline/camera/light/audio, and motion continuity across the cut, limb and body vector, subject and camera speed, and the phase of the movement at the out-point against the neighbor's in-point;
- where the generation declares internal units, whether a failed unit is cuttable without losing the rest;
- whether a local repair, insert, cutaway, reframe or VFX route preserves the shot;
- whether a delivered flicker, strobe or rapid luminance alternation clears the delivery route's photosensitivity requirement, a delivery gate an intentional look does not exempt, so look the applicable standard up rather than assume one; [QC-29]
- manual fix cost/time versus regeneration/redesign.

### Delta edits against a supplied source [QC-27]

When the job is a scoped change to a supplied image, frame or clip rather than a fresh render, inspect it as a differential:

- did the requested change occur, within the scope stated;
- what else changed. Enumerate every difference outside the declared change scope; each is a finding regardless of whether it is attractive. Where the contract names no preserve set, everything outside the named change is the preserve set by default.

Unchanged-ness cannot be judged from memory or from a description of the source. It requires the source and the output inspected together, aligned frame to frame, and across the same interval for a moving source. Without the source in hand, out-of-scope drift is unknown, not absent, and the verdict says so.

Report the change and the drift as separate findings. They route differently: a correct change riding on unrequested drift may still be unusable, and re-issuing the edit is not the same action as re-scoping it.

First establish the operation. A video generated from an identity reference at a new angle is judged for its granted identity/wardrobe/material dimensions and requested perspective, not for unchanged source pixels. Neither exact retention nor universal impossibility of viewpoint editing follows from the task name. If a close-up becomes a wider view, assess facial detail at its actual visible scale; do not demand invented pores or sharpening to simulate close-up evidence. Standalone still outputs route to `certainty:studio`.

## Keep three questions apart

A QC pass answers three questions that fail in different ways, and every line of the report belongs to exactly one of them:

1. **Was the inspection completed?** Which dimensions were opened, over which interval and which frame areas, at which evidence modality and quality tier. A record of what was done, settled by the log rather than by judgement.
2. **Does the work meet its contract?** The gate results and the scores.
3. **Is the report defensible?** Every claim carrying a timecode, an observation/inference/unknown label, and a stated bound on any absence.

Conflating one and two is how coverage turns into taste: a dimension nobody opened gets written up as clean because the clip looked good, and the master ships with a defect the report says was checked. Conflating two and three produces the mirror failure, a scrupulously hedged document that never says whether the shot can be cut. [QC-02]

**Every dimension carries a recorded disposition**, and the three ways of not scoring one stay apart:

- `pass` / `fail`, inspected and judged;
- `n/a`, the contract was read and this dimension does not bind here: no dialogue, no on-screen text, no neighboring shot;
- `not checkable`, it binds and the available evidence cannot settle it; the finding takes severity `Unknown`, and says what evidence would settle it;
- `not inspected`, nobody looked.

Never leave a dimension off the list to mean any of these. An omission reads as `n/a` to the next person, which silently promotes an unexamined dimension to a cleared one; and a genuine `n/a` read as an omission buys a second inspection of a shot that has no dialogue in it. [QC-31]

## Severity

| Severity | Meaning |
|---|---|
| Critical | Wrong version attribution, fabricated capability/parameter/evidence, rights/data leak, missing primary entity/reference role/end state, or structurally unusable required beat |
| Major | Blocks approval/cut but has a plausible regeneration/redesign/VFX route |
| Moderate | Material deviation requiring local repair or pickup |
| Minor | Cosmetic defect that does not break meaning, continuity or delivery |
| Unknown | Evidence cannot support pass or fail |

## Finding schema [QC-18]

```text
Finding ID / dimension / severity / acceptance impact
Evidence modality and exact timecode/frame
Direct observation:
Defect distribution across takes / clip / frame:
Inference or root-cause hypothesis:
Unknown / missing evidence:
Minimal next action:
Route: accept / edit / repair / regenerate / VFX / redesign
Changed variable:
Fixed invariants:
Stop condition:
```

## Verdict

Return `PASS`, `FAIL`, or `CONDITIONAL` only for the reviewed evidence scope. Summarize blockers separately from numeric scores. A high mean never clears a failed hard gate.

**Open the report with its own scope line.** One line, inside the artifact: evidence modality, the interval and frame areas inspected, the quality tier of that evidence, the platform/model/version as the user stated it or `unknown`, and every dimension standing at `not checkable` or `not inspected`. It belongs in the artifact rather than in the message delivering it, because the artifact is what gets forwarded, pasted into a tracker and read a month later by someone who never saw the message, and a verdict read without its bounds is read as a general one. The same line states what this report does not do: it judges the media against its contract, it does not name who or what generated the clip, and it predicts nothing about reception. [QC-02] [QC-21] [QC-31]
