# Editorial, finishing, and final QC

Read this file when planning rough cut, pickups, post-production, delivery, or archive.

## Start editorial early

An accepted-looking isolated shot may still fail the film. Build a complete blocking cut early to reveal:

- coverage holes and absent story beats;
- repeated or slow beats;
- missing masters, reactions, inserts, exits, and transition handles;
- axis/eyeline/action mismatches;
- shots that are impressive but unusable in rhythm;
- where a cheaper edit/VFX route beats regeneration.

Rolling assembly was repeatedly described in project briefs, but no controlled study proved the ideal overlap. Treat it as a strong production starting policy, not a causal guarantee.

## Dailies and selects

- Review the complete clip, not its thumbnail.
- Inspect opening, middle, ending, cuts/transitions, and high-risk action/audio timecodes.
- Gate intra-shot quality, prompt/entity fidelity, cross-shot continuity, then neighbor edit.
- Keep incoming, rejected, selects, and approved memory distinct.
- Only accepted takes enter the edit; rejected takes remain in the ledger for diagnosis and never become identity truth.

## Rough cut and pickups

Cut for story and performance rather than sunk generation cost. Track:

- approved in/out and handles;
- temp VFX, reframes, speed-change intent and audio placeholders;
- missing coverage and prioritized pickups;
- downstream impact of each structure change.

For performance-bearing cuts, watch the exchange at normal speed before inspecting individual frames. Keep the listener's opportunity to register information, the partner's response and any continuing effort or tension from the Performance handoff. A technically matched pose can still reset the person. Moving a reaction earlier can give a character knowledge they did not have; cutting a hesitation short can turn reluctance into consent. Record these as story changes, not only timing adjustments. An intentional time jump or subjective edit may change the state, but must follow the approved scene contract. [FP-22]

Do not conceal dialogue retiming or continuity damage with undocumented time-stretch. Structure lock requires a change request for new shots or reordered state.

## Cleanup, VFX, and conform

Route defects deliberately:

- regenerate when the core shot contract is wrong but remains model-suitable;
- local AI edit or traditional paint/roto/key when a defect is bounded;
- reframe/cutaway/split when editorially recoverable;
- composite exact text/logo/UI instead of endlessly regenerating spelling;
- use simulation/3D/practical/live action for persistent physics/contact limits.

Normalize codec, frame rate, duration, color tags, audio channels and filenames into the project master. Preserve source media and transformations. Upscale/interpolate only with a defined need and inspect ghosting, edge distortion and texture crawl.

Conform against the delivered container, not against geometry drawn into the picture: bars, mattes, or a wider ratio inside the frame are content and travel with it. Reconcile each shot's target duration against the delivered clip length before conform, and route a systematic gap back to shot design instead of absorbing it in the timeline.

## Baked-in versus separable layers

Decide before shooting which elements are baked into the generated take and which are delivered as separate layers. Anything baked in cannot be re-timed, translated, remixed, or removed without rejecting the take, so the layer assignment is a production decision made at breakdown, not a preference discovered later in the mix.

- **Sound.** Assign every audio element to a layer before the first request. Shots ask only for the in-world sources belonging to that space and moment, drawn from the location and prop passports. Anything the mix must stay free to change, score, any non-diegetic element, anything whose timing, language or licensing is unsettled, is deferred to the mix and kept out of the request. Baking a musical or non-diegetic element into a take is a legitimate choice when the production wants it; record it as a decision with its cost noted, because changing it afterwards means re-running the shot.
- **On-screen text.** Keep a per-scene inventory of the text allowed to be visible in the delivered picture, each item with its source: in-world graphic, composited artwork, or none. Anything else the generator renders, captions, provider marks, invented signage, subtitle-like overlays, is a defect in an otherwise acceptable frame, because burned text cannot be conformed, translated, or re-timed and collides with any separate caption deliverable.
- **Picture.** The look is baked in with the frame: exposure, black level, grade and palette, halation and bloom, grain, day-for-night, and in-frame atmospherics. Decide at breakdown how much of it the generation carries. A neutrally exposed take that holds detail in the blacks stays gradeable in finishing; a look driven into the take fixes the film's color before the first cut and cannot be pulled back without re-running the shot. Baking a look in is a legitimate choice where it is the point of the scene, record it as a decision with its cost, and hold it as a passport state so neighboring shots match it.
- The hard gate tests conformance to this plan, not the presence or absence of music: an accepted take carries no rendered text outside that scene's inventory and no audio outside its declared layer assignment.
- Picture-accepted and sound-rejected is a route, not an automatic re-run: mute and re-voice, or replace the audio layer, before spending a retry. Muting removes that shot's ambience and room tone along with its defect, so rebuild the bed from the location passport; otherwise the shot leaves a hole in a bed the neighboring shots carry.

The prompt clauses that carry these restrictions belong to `video-shot-prompts`; the layer assignment, the inventory, and the gate are production decisions.

## Color and sound

Color checks: shot match, motivated light, skin/material fidelity, day/weather state, gradients/banding, legal range and calibrated playback. A container or `4k` badge does not identify generation resolution, bit depth or color pipeline.

Sound checks: exact dialogue, speaker/voice identity, pronunciation, lip-sync, perspective, room tone across cuts, action-linked foley, music motif, silence, loudness, channels and delivery. Generated sound may guide timing but does not replace professional cleanup/mix.

Use ADR/dubbing when picture is usable and model speech is not. Keep voice rights and pronunciation dictionary in the passport.

## Subtitles

Time subtitles from the final video's actual audio, never from prompt milestones. Verify language, speaker, transcription, punctuation, line breaks, reading speed, safe area, occlusion, cross-cut behavior, and burned-versus-sidecar delivery. Plan the accessibility deliverables here too: SDH carries speaker labels and significant non-speech sound, and audio description needs its gaps reserved in the mix rather than found after the sound lock.

## Final QC and archive

Use at least one full uninterrupted master playback plus targeted checks of every edit, VFX, subtitle and audio transition.

Technical QC:

- duration, aspect, resolution, frame rate, codec/container and color tags;
- duplicate/drop/freeze/black frames and compression artifacts;
- audio channels, sync, clipping/peaks/loudness;
- subtitle format/timing/safe area;
- delivery naming and checksum.

Content QC:

- story and required beats;
- identity, wardrobe/injury, prop/location/weather continuity;
- anatomy, motion, physics/contact, camera and text;
- dialogue/sound/music/subtitles;
- rights, policy, disclosure and watermark requirements.

Archive master/mezzanine, stems, subtitle files, project/timeline files, prompt/reference/state/run ledgers, approved/rejected decisions, tool/model/platform/doc versions, hashes, approvals, waivers and rollback checkpoints. Never archive signed media queries or credentials.
