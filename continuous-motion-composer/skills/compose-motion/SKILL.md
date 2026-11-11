---
name: compose-motion
description: Build and render real motion in Remotion (or free 3D when needed) from approved style frames, with timings, captions and a loudness-checked mix.
---

# Compose motion

Use after the owner has approved the style frames. The memory note `style-frames-<project-slug>` must say `approved`. Motion is code-driven by default.

## Steps

1. **Confirm the gates.** If any of `diagnosis-<project-slug>`, `storyboard-<project-slug>` or `style-frames-<project-slug>` is missing or still `awaiting OK`, stop and go back to that skill.
2. **Source of truth.** Put copy, brand tokens and scene times in data, including a `timings.json` (scene ids, and word times when voice exists). 16:9 and 9:16 compositions read the same data so they do not drift. Build only the ratios the diagnosis named.
3. **Real motion.** Animate the idea: a value filling, a lock closing, a shape becoming another shape, a character turning on the beat. Do not cut between static screenshots and call it motion. Match the rhythm of the storyboard. Each idea stays on screen long enough to read (about 3 seconds or more).
4. **Voice and music.**
   - If an audio teammate or the owner has provided voice and word timings, sync the picture to those times. Prefer voice that has not already been loudness-normalised, so this bot can duck and master the mix.
   - If voice is still coming, keep placeholder timings and do not call the piece finished unless the owner asked for a silent or temporary cut.
   - When a music bed is present, duck it under speech. Record the title, author, URL and licence next to the file. Do not use music whose licence you cannot state.
   - Captions match the written script. Spoken respellings stay in the voice text only and are never shown.
5. **Layout check before any full render.** Render stills for each scene, including a frame in the middle of each transition (`npx remotion still <entry> <composition> out/<name>.png --frame=<n>`). Look for overlaps, weak contrast, text too small at 1080p, and anything hiding behind something else. Fix, and look again.
6. **Render.** Check free memory and that no other heavy job (a voice run, another render) is going. Then render at one process:
   `npx remotion render <entry> <composition> out/<slug>.mp4 --concurrency=1`
   Typical sizes: 16:9 at 1920 by 1080 and 30 fps; 9:16 at 1080 by 1920 and 30 fps, with larger top and bottom margins. If Remotion is missing, say so and offer to install it after the owner's yes. If the owner is not eligible for the free licence, stop and report the company-licence cost from https://www.remotion.dev/docs/license/faq.
7. **Other free tools.** For real 3D (a camera around geometry, materials, lights), Blender is the free path when it is installed: run it headless with a script, one process at a time. If the owner asks to grade existing footage, do it with deterministic code (curves, a LUT), not a generative restyle, and show a before-and-after grid.
8. **Paid tools.** A paid image-to-video or text-to-video service is never the default. Describe the action, the cost (including the free-tier limit and the price after it) and wait for an explicit yes. On no, stay on the free path.
9. **Measure the final file** with the skill `qa-frames` before you call it done.

## Do not

- Render before the style frames are approved.
- Run a full render at a concurrency higher than 1, or next to another heavy job, on a shared computer.
- Use music or footage whose licence you cannot state.
- Show a phonetic respelling in a caption, a title or the script you hand over.
- Invent on-screen code, errors or numbers.
- Publish or send the file. That needs the skill `approval-gate`.
