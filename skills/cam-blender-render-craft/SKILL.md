---
name: cam-blender-render-craft
description: "Blender 5.0 render craft for the camera department when a film is built and rendered in Blender from Python: why a render looks flat, gray or noisy and how to fix it (AgX looks, key-to-fill ratios, a dark room with one dominant motivated light, color temperature in Kelvin, Cycles sampling and OpenImageDenoise passes, grain judged only at delivery size), lens and sensor fit in a vertical 9:16 frame, push-in versus zoom, depth of field on a focus object, keyframes and F-curves under 5.0's layered actions, and a value-first critique (thumbnail, grayscale, flip, reference). Every setting was checked against Blender 5.0.1. Use when a Blender render or draft looks amateur, flat, gray, washed out or noisy, when choosing render settings, a lens or a camera move for a built film, or when reviewing a built frame."
---

# Blender render craft (5.0)


## First: measure the frame, then name the fault

Before changing a light, read the frame's values. Convert to luma (Rec. 709 weights) and take the 1st, 50th and 99th percentiles, then compare with the look book's targets.

| What you see | Usual cause | First fix |
| --- | --- | --- |
| Everything mid-gray, p50 near 0.5 to 0.6, nothing dark, nothing bright | Too much fill: a bright world, a big soft source facing the subject, or the window acting as fill instead of key | Lower the fill until the key-to-fill ratio is at the target; let the room go dark |
| Flat but not gray | Key-to-fill ratio too low, no separation | Raise the ratio; darken what is behind the subject or add a rim |
| Low contrast after the lights are right | View transform look too soft | Step the AgX look up one contrast level and judge in grayscale |
| Dark areas crushed to featureless black | Ratio too high, or no bounce | A small fill from the camera's side, or one more diffuse bounce |
| Shimmering noise in flat areas in motion | Too few samples for per-frame denoising, or grain drawn too large | More samples or a lower adaptive threshold; judge grain only at delivery size |
| "Videogame" look | Hard shadows everywhere, sharp edges | Larger area sources, bevels on edges |

Fix one bad light before adding another. More lights usually means flatter.

## Light ratios and the dark room

- Key to fill: 2:1 is high-key (commercial), 4:1 is medium (portrait), 8:1 or more is low-key (dramatic). A dark room lit by one window or one projector is low-key.
- When a light in the scene is the story (a window, a lamp, a projector), it must dominate: world strength about 0.1 to 0.2 or less, the usual fill and rim reduced or removed, and at most one small, weak fill from the camera's direction so dark objects keep their shape.
- Bounces decide how much light fills the shade. Raising them lifts shadows; do not raise them to cure a dark frame, and do not lower them below what keeps the shade readable.
- Aim lights at the subject from their position (point the light's -Z axis at the target, for example with `Vector.to_track_quat('-Z', 'Y')`), never with copied Euler angles.

## Color temperature

Use Kelvin, not typed RGB. Checked: `Light.use_temperature` and `Light.temperature` (default 6500 K) exist in 5.0.1, and the Blackbody shader node is available for emitters. Direct sun is warm-neutral, about 5000 to 5800 K; open skylight through a window is cool; a tungsten lamp is about 2700 to 3200 K. A cool blue "sun" is a mistake.

## View transform and contrast

Checked: in 5.0.1 the AgX looks are None, AgX - Punchy, AgX - Greyscale, AgX - Very High Contrast, AgX - High Contrast, AgX - Medium High Contrast, AgX - Base Contrast, AgX - Medium Low Contrast, AgX - Low Contrast, AgX - Very Low Contrast. Base Contrast is neutral, not punchy. A low-key film usually wants Medium High or High Contrast; choose it by comparing two renders of the same frame in grayscale, and record the choice in the camera plan so every render uses it. Never use the Standard view transform for photographic output; it clips highlights. Exposure in `view_settings.exposure` is a global shift and does not fix a ratio.

## Noise

Checked in 5.0.1: `cycles.denoiser = 'OPENIMAGEDENOISE'`, `denoising_input_passes` in RGB, RGB_ALBEDO, RGB_ALBEDO_NORMAL, `denoising_prefilter` ACCURATE, `denoising_quality` HIGH, adaptive sampling on with threshold 0.01. There is no temporal denoiser (`denoising_use_animation` does not exist), so each frame is denoised alone and low-sample animation can shimmer in flat areas even when a still looks clean.

- Use RGB_ALBEDO_NORMAL passes with the ACCURATE prefilter for kept renders.
- For animation, judge noise in motion, not on a still. If flat areas boil, raise samples or lower the adaptive threshold before anything else.
- A low-resolution draft is for timing and layout. Judge noise and grain only at delivery resolution, because added grain drawn on a small frame is coarser relative to the picture and reads as dirt.
- As a starting range: scenes lit mostly by direct light converge at 64 to 128 samples; indoor scenes with lots of bounce need about 512; glass, caustics and subsurface need more. Denoising helps a lot but does not replace samples.

## Lens and sensor in a vertical frame

Checked: with `sensor_fit = 'AUTO'` the sensor width applies to the longer side of the frame. In a 1080 x 1920 frame with a 36 mm sensor and a 35 mm lens, AUTO gives about 54 degrees vertically and 32 degrees horizontally, like a full-frame camera turned on its side and cropped to 9:16. With `sensor_fit = 'HORIZONTAL'` the same 35 mm spans 54 degrees across and 85 degrees up and down, a much wider picture. When a focal length is quoted in a plan, say which side the sensor spans, or the number means two different lenses.

| Focal length (full frame) | Feel |
| --- | --- |
| 14 to 24 mm | Very wide, exaggerated perspective, spaces |
| 28 to 35 mm | Wide, documentary, environments |
| 50 mm | Neutral |
| 85 mm | Intimate, flattering close-ups |
| 100 mm and up | Isolated subjects, compressed space |

## Focus

Checked: `camera.dof.focus_object` and `aperture_fstop` exist. Prefer a focus object (an empty on the subject) to a typed distance when the camera moves. f/1.2 to 2 is razor thin, f/2.8 shallow, f/4 moderate, f/5.6 to 8 medium deep, f/11 and up deep. Keep the explained subject sharp; very shallow focus on a small subject makes it look like a miniature. Check what units the scene uses before trusting an f-stop: the depth of field depends on the scene's scale.

## Camera moves

- A push-in moves the camera; a zoom changes the focal length. A push-in changes perspective and reads as cinematic; a zoom flattens and reads as news or surveillance.
- Move with intent: a dolly toward what matters, a reveal, a track along the subject. Constant drift with no reason reads as filler.
- Checked: in 5.0.1, `Action.fcurves` no longer exists. Keyframes go into layered actions with slots. Read or edit curves through `bpy_extras.anim_utils.action_get_channelbag_for_slot(action, obj.animation_data.action_slot).fcurves`. New keys default to BEZIER with AUTO easing.
- A keyframe's interpolation governs the segment that follows it. Setting an easing on the last key does nothing.

## Critique, every time a frame is shown

1. Squint, or view at phone-thumbnail size: does the composition still read?
2. Grayscale: do the values work without color? Values first, color second.
3. Flip horizontally: awkward balance shows at once.
4. Compare side by side with the reference at the same size.
5. Leave it for a while and look again.

## Claims in the source that did not hold in Blender 5.0.1

`action.fcurves.find` (removed in 5.0); a Cycles temporal denoiser (`denoising_use_animation`, not present); EEVEE `use_gtao`, `use_bloom`, `use_ssr` (not present in 5.0's EEVEE); a cool blue color for direct sun (wrong); "256 samples plus denoising equals 4096 raw samples" (an overstatement); framing math that assumed the sensor spans the frame's height (wrong for AUTO in a vertical frame); a warning that Euler rotation flips past 180 degrees (it does not for a single-axis spin).
