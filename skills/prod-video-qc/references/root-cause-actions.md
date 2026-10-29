# Root causes, minimal actions, and stopping rules

Read this file after recording direct evidence. Do not jump from a symptom to a fix without a bounded hypothesis.

## Locate the defect before choosing its level

A defect's distribution is diagnostic and is cheaper to establish than any hypothesis about its cause. Test three axes:

1. **Across takes**, compare existing runs made with identical text, inputs, and recorded parameters before proposing another sample. Repeated failure supports a repeatability finding, not proof that wording caused it; changing outcomes supports sample sensitivity, not immunity of the contract from defects. Record sample count and uncontrolled conditions, rank input/contract/model hypotheses, and propose a bounded control only if it can distinguish them. A text contradiction can be established from the contract itself without a new render.
2. **Across the clip**, a defect confined to an interval is a repair, insert or trim candidate. A defect present in every frame may require a longer repair or an upstream change; temporal persistence alone identifies neither its cause nor whether spatial repair is possible.
3. **Across the frame**, a defect confined to a region is a repair, cutaway or composite candidate. A defect present everywhere in the rectangle is not.

Record the distribution in the finding. `Change only: nothing (control run, N samples)` is a valid action packet entry, and the ceiling that bounds it is a take budget, not a rewrite budget. [QC-25]

## Check candidate degeneration against the contract

An apparent degeneration signature can arise from the contract, inputs, lineage or sample variation. Inspect the
contract and existing evidence before naming the hypothesis; a familiar symptom does not establish which cause
produced it. The cost of an unsupported diagnosis is a retry that leaves the actual defect untouched.

Candidate signatures, only when the contract did not ask for them; their presence alone does not establish a cause:

- motion that cycles instead of progressing: the same few steps, a gesture restarting rather than completing, a camera move that resets;
- a tail that stops advancing before the stated duration while the frame keeps running, a still with drifting grain, or a held pose under continuing ambience;
- prompt material rendered in frame: instruction words, bracketed direction, a caption of the brief, an unrequested slate or label card;
- the audio equivalents, a loop point in room tone, a line restarting mid-word, an ambience that begins and never resolves.

Two exclusions before filing one. A contract that declared the artifact, a looping cycle, a freeze-frame ending, an on-screen title, is scored against what it declared rather than for the artifact's presence. [QC-29] And the finding names a run, never a model, a version or a generator: the signature describes the state this lineage reached and says nothing about what produced it.

**Choose a new lineage only when the evidence supports that hypothesis.** Check the contract first: copied planning text or an overloaded schedule can explain an apparent signature and route to a contract repair. A signature that worsens through successive continuations from one parent supports a lineage hypothesis; a defect that clears on an unchanged re-fire supports sample sensitivity. Neither comparison alone proves the cause. When the lineage hypothesis is the strongest remaining one, propose `regenerate` from the last clean parent with the contract fixed, a diagnostic signal, and a ceiling; do not pile on unsupported texture or wording fixes.

**Set a lineage ceiling separate from the take budget.** Close the candidate lineage at the project ceiling. If the same signature survives a bounded comparison from another clean parent, stop repeating that test and reconsider the shot, inputs, or repair route. Report which alternatives remain unresolved rather than conclude that the contract or model is proven responsible. A proposed re-render is a route, never authorization to generate. [QC-30]

## Diagnose in order

1. **Task/runtime**, wrong task family, asset role, prompt verb, hint, aspect/duration/format, model/platform assumption; text and parameters disagreeing on timing, length or take structure, or a schedule that over-books the requested runtime. [QC-24]
2. **Reference conflict**, test the binding before the inheritance: an asset may be unused, misbound to the wrong entity, conflated with another, or correctly bound but over-inherited. Then audit inheritance channel by channel, since leakage usually appears on a channel the reference was never granted. Ambiguous mapping, redundant/conflicting asset, and weak state reference sit under the same step.
3. **Entity/state**, wrong count/identity, mixed wardrobe/injury/weather/prop state, ownership or end-state omission.
4. **Space/camera**, missing first-frame occupation, landmarks, axis, eyelines, directions, or competing movement.
5. **Physics/action**, too many state changes, no contact causality, impossible body/material burden, camera masking action.
6. **Acting**, unclear purpose or partner stimulus, unavailable knowledge, mistimed response, redundant cues, unreadable framing, lost performance register or a state reset. Infer causes cautiously; an emotion label alone is not a complete diagnosis. [QC-32]
7. **Audio/text**, speaker/language/timing ambiguity, generated text burden, missing real audio evidence.
8. **Neighbor edit**, end state, action/camera vector, light or room-tone mismatch.

Higher upstream failures invalidate lower-level polish work.

## Symptom-to-action matrix

| Symptom | First minimal action | If repeated | Final route |
|---|---|---|---|
| Wrong task/error | Align one mismatched role/verb/hint/parameter from current docs | endpoint probe | stop until runtime contract is known |
| Missing/extra entity | Add exact count/required/forbidden line | cleaner single-role asset, reduce cast | split/composite |
| Identity/wardrobe drift | Return to one approved state-specific canonical asset | shorten shot or isolate character | identity composite/2D/3D/live action |
| Reference leakage | Name the channel that leaked, then add allowed/excluded inheritance for the offending asset on that channel | remove or rebuild that asset | separate roles across shots |
| Spatial/axis failure | Add first-frame occupation, landmarks, camera side and end positions | use floor plan/diagram/master | reframe/cutaway/new coverage |
| Hands/contact | Lock camera and keep one interaction | keyframe/blockout, split into inserts/reactions | traditional VFX/3D/practical |
| Wrong physics/material | State contact→force→inertia/material→result | state asset or blockout | simulation/composite/redesign |
| Flat or mechanical acting | Locate whether intent, partner stimulus, timing or cue readability failed; change that one cause | reaction coverage or a clearer playable tactic | writer/director review or editorial performance reconstruction |
| Excessive or generic expression | Remove a redundant cue sequence while preserving the approved register and event | compare a different character-specific carrier | director review; do not automatically turn heightened acting into restraint |
| Reaction too early or performance resets at a cut | Restore the information boundary or incoming residue that failed | review both shots and the proposed edit point | pickup or scene/coverage repair |
| Edit spill | State sole master, A→B, exact scope and preserve list | use only approved changed interval | roto/paint/key/composite |
| Extension drift | Return to last approved checkpoint + canonical context | shorten continuation | independent hard-cut shot |
| Wrong dialogue/lip | One speaker, exact language/line, silent others | picture-only generation | ADR/dubbing/lip tool |
| Text/subtitle failure | Isolate short static requirement | clean plate + tracking | graphic/subtitle composite |
| Audio seam | Match room tone/perspective/level intent | crossfade/mix | replace generated soundtrack |
| Neighbor mismatch | Repair the one end-state/vector/light/level mismatch | insert/reaction/cutaway | pickup/re-edit |
| Unrequested damage or feature appearing where the contract bounded it by number | Restate the bound as the object, the place on it, and the surface that stays whole | Give each object its own sentence naming its state | Isolate the object in its own shot or insert |
| Defect on an attribute the contract appears to forbid | Read that clause standing alone before charging the model | Resolve every pointer in it to a literal value | Contract rewrite, not another take |
| Candidate degeneration signature: looping motion, a frozen tail, prompt text or a slate in frame | Inspect existing run distribution and rule out an explicit contract cause | If supported, propose a bounded clean-parent comparison with contract fixed | Stop the comparison at its ceiling; reconsider inputs, repair, or shot design |

**An inert clause is a contract defect, not a take failure.** Before filing a prohibition as violated, read it by itself with nothing else in view. A clause that points at a document not submitted with it, *the listed items*, *the rest*, *that area*, *the master*, never bound anything, because nothing at the other end of the pointer reached the generator; report it the way a contract that over-books its own runtime is reported, as a defect of the text routed to a rewrite, and expect no number of retries to change it. A clause that bounds a diffuse feature by how many there are, *no second one*, *only one of them*, carries a weaker warrant: it rests on an uncontrolled observation of such a bound leaving the feature free, not on a controlled comparison, so record it as suspected inert, restate the bound as a place and an edge, and say in the finding that the rewrite is precautionary. Either way, charging the clause to the model before reading it alone is a misdiagnosis that spends the take budget on nothing. [QC-28]

Edit spill is diagnosed only after the job has been inspected as a differential against its source; see the delta-edit dimension in the inspection rubric. [QC-27]

## One-variable action packet

```text
Observed defect and evidence:
Defect distribution across takes / clip / frame:
Root-cause hypothesis:
Alternative hypothesis:
Change only:
Hold fixed:
Expected diagnostic signal:
Pass/fail condition:
Next route if failed:
```

Changing prompt, reference, duration, resolution and shot design simultaneously destroys attribution. Preserve the last working prompt and parent run.

## Choose the route

- **Accept** when all hard gates pass and residual defects are inside the agreed floor.
- **Edit/repair** when the approved performance/state is usable and the defect is local, bounded and cheaper to fix.
- **Regenerate** when the model-suitable core contract failed and one testable upstream change remains, or a lineage hypothesis justifies a bounded parent comparison with text held fixed.
- **VFX/composite** for persistent text, hands/contact, local identity, keying, geometry, physics or cleanup problems.
- **Redesign/split** when shot architecture overloads the model or retries oscillate.

Do not use “regenerate” as a default. Compare expected loss, human time and continuity risk.

## Stop conditions

The project sets numeric ceilings; research heuristics such as 10–15 retries are not universal.

Stop generation when:

- the same blocking defect survives isolated relevant retries;
- solving one critical requirement repeatedly breaks another;
- budget/time ceiling is reached;
- further progress requires a rejected or drifted frame as truth;
- rights, policy, platform or delivery cannot pass;
- a mature edit/VFX/ADR/graphics route has lower expected cost/risk;
- the loop has converged: the last controlled change moved no finding in class or severity.

A retry counts as isolated only where it was controlled. State how many samples were taken and whether the text and parameters were unchanged; an uncontrolled retry sequence cannot support the repeated-defect stop condition. [QC-25]

**Declare the termination condition before the first re-render.** End when the defect clears, the ceiling is reached,
or the bounded comparison produces no useful change in the finding. An unchanged outcome is insufficient signal
in those samples, not proof that the variable cannot matter. Report the sample scope, unresolved alternatives and
next route. A metric moving between takes does not establish that the defect moved; do not spend toward a score
without an observable acceptance change. [QC-16] [QC-25]

Record last approved checkpoint, observed defects, tested hypotheses, spent time/cost and next route.
