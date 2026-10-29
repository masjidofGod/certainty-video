---
name: sb-cinematic-explainer
description: "Cinematic explainer craft for animated films that teach something (a count, a mechanism, a process): every narrated line shows a real change in the scene, not a camera drift over a still; a shot table with start state, driver, middle state and end state per line; a hook that states the question big and shows the first surprise within 5 seconds; narration that only says what the picture shows, in cause-then-effect order; the recorded voice as the timing master; one full-resolution approval frame before any motion is rendered; a frame-triplet motion check; and a physical-plausibility and anti-toy-look gate. Use when boarding, scripting, lighting, animating or reviewing an explainer or educational animation, when a section plays as talk over a still page, when an animation looks amateur, flat or like a slideshow, or before rendering a full sequence."
---

# Cinematic explainer craft


An explainer is cinematic when the thing being explained moves, changes and causes something on screen, in the order the voice explains it. A beautiful still with a voice over it is a slideshow, whatever the light or the lens.

## The law: every narrated line shows a change in the subject

- Each spoken sentence gets one dominant visual action that happens in the scene itself: a letter lifts off the line, a mark detaches, a slot of light opens, a page turns, a row reassembles. Ask: would the change still be visible if the camera were locked off? If not, it is not the action.
- Camera moves, push-ins, Ken Burns pans, rack focus, a light sweep and crossfades can support the action. They never are the action.
- A still hold is allowed only to establish where we are, to land an emphasis, or to give the viewer a silence to count in. It never carries an explanation. A run of narration over an unchanging picture is the first thing to fix in any animatic.
- Show the cause before the effect. The viewer sees what is about to happen, then sees it happen, then hears what it means.
- End each shot on a visibly different state that sets up the next one.

## Shot table: one row per spoken line

Write this before boarding motion. A row with no subject change is a row to rewrite, merge or cut.

| Field | What goes in it |
| --- | --- |
| Line | The spoken words, verbatim |
| Teaching objective | The one thing the viewer knows after this line that they did not before |
| Claim status | verified, inferred or conceptual (`references/evidence-and-explanation.md`) |
| Orientation and scale | Where we are and how big things are at the start |
| Start state | The subject before the change |
| Driver | What causes the change |
| Middle state | The frame that proves the change is happening |
| End state | The subject after, visibly different |
| Camera | Supporting move, if any, and why |
| Literal or conceptual | Whether the motion could be mistaken for something real |
| Exit | What this end state hands to the next line |

Shots of about 6 to 12 seconds teach well; a 30 to 60 second film runs about 8 to 14 of them. If you cannot say what a shot proves, cut it.

Pick one primary pattern from `references/story-patterns.md` (for a count: "how it works" or "cause and effect"; for a hidden structure: "inside the system") and at most two supporting ones.

## The hook

- The opening line promises what is coming. Say the question big, then show the first surprise within 5 seconds. A small title that undersells the film loses people before the good part.
- If the first 3 seconds would not stop your own thumb, rebuild them before building anything else.
- The first frame already looks like a film, not a slide: depth, a motivated light, something moving.

## Narration

- Narrate only what the viewer can see, or what the picture has clearly set up. Cut any claim whose object, step or cause is not on screen.
- Prefer "because" and "therefore" over lists. For each thing shown: what is it, what changes, what causes the change, why it matters.
- Say "looks like" rather than "is" when the evidence only shows a resemblance. Every spoken fact has a source in the film's claim ledger before it goes in the script.
- The recorded voice, at its natural speed, is the timing master. Never speed up, slow down or stretch the voice to fit a shot. If it does not fit, rewrite and record again, then retime the picture and the captions to the waveform. (In this project a scratch voice may time an animatic; the board is retimed when the real voice arrives.)
- The voice sits on top of the mix. If the effects compete, the effects come down.

## Approval frame before motion

Before any sequence is rendered at full quality, render one frame at delivery resolution that holds the hardest material, the finest detail that must read, the darkest region, the brightest highlight, the intended depth of field and one sample caption. Inspect it at 100% and at phone-thumbnail size. It goes to the user through the art department's frame review. No motion render until it is approved. Approval covers the look only, never the motion or the pacing. Details: `references/visual-quality.md`.

## Motion check after every render

For each narrated shot, pull an entry, a middle and an exit frame and read them as a sequence, not as one contact-sheet still. Pass only if the subject changes without the camera's help, the cause comes before the effect, and the end state prepares the next shot. A shot that is a still, a repeated frame, a pan, a zoom, an orbit, a crossfade or a light change alone fails.

## The amateur look, and what fixes it

From `references/visual-quality.md`, the points that most often separate a professional frame from an amateur one:

- Light for form: a controlled key that rakes the surface, readable shadows, highlights that roll off, and the subject separated from the background. A frame lit evenly from everywhere reads as gray and flat.
- Keep detail in the darks; avoid featureless black and avoid lifting everything to mid-gray.
- Break perfect uniformity with roughness and surface variation before adding color noise or grain.
- Avoid heavy saturation, bloom, glow and miniature-looking depth of field. Use focal length and distance for perspective.
- Deliberate camera moves (a dolly, a top-down reveal, a track along the subject), not constant drift.
- Every visible object has a real counterpart at a plausible scale, or is clearly shown as conceptual.

Motion principles worth borrowing from motion design (charlie947 `motion-effects`): change one object's shape instead of crossfading between two objects; leave a faint ghost of the start state while the new state forms; stagger related elements by a beat in reading order; keep one small thing alive during a hold so the frame never freezes.

## Reject before calling it done

Any narrated process shown only by a camera move over a still, repeated frames, a slideshow or a crossfade montage; any unsupported claim or invented detail; misleading scale; an unreadable or clipped caption; an unexplained abstraction; a black frame; a color-tag error; audio drift; a decode failure.

## References

- `references/story-patterns.md`: seven explanation patterns and the shot design template (source text).
- `references/evidence-and-explanation.md`: the claim ledger, four kinds of accuracy, causal narration (source text).
- `references/visual-quality.md`: hierarchy, the toy look, the plausibility gate, light, camera, readable change, the approval frame (source text, approval paragraph adapted).
