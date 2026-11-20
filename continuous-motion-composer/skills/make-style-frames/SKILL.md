---
name: make-style-frames
description: Make style frames and a contact sheet from an approved storyboard, and wait for the owner's OK before any animation.
---

# Make style frames

Use after an approved storyboard, before any animation or full render. The memory notes `diagnosis-<project-slug>` and `storyboard-<project-slug>` must both say `approved`.

## Steps

1. Make one still for each key beat in every aspect ratio the diagnosis named (16:9 at 1920 by 1080, 9:16 at 1080 by 1920). Prefer Remotion stills (`npx remotion still <entry> <composition> out/<beat>.png --frame=<n>`) or another free, code-drawn method. A paid generator needs a written cost and an explicit yes first.
2. Apply the brand tokens from the diagnosis. 9:16 frames need larger top and bottom margins so platform controls do not cover type. Keep credits and lower thirds above the caption zone. Headlines stay around 45 characters or fewer. Body text stays large enough to read at 1080p (about 40 px or more).
3. Run the same plausibility checks as the skill `plan-storyboard` on every frame: scale, pose, hands, continuity, no invented text or warped anatomy. Fix or regenerate a failure before anyone sees it. Show only frames that pass, and list any remaining mismatch in plain words.
4. Build a contact sheet that puts every still on one page, labeled with the beat and the time range (placeholder times if voice has not arrived). When the piece includes 16:9, also make a 1280 by 720 thumbnail from a clear beat.
5. Look at each still at full size before you show it: overflow, weak contrast, text cut at an edge, a credit under a caption, and secrets on screen (tokens, private addresses, unread counts, faces or handles the owner did not choose for that channel).
6. Save a memory note titled `style-frames-<project-slug>` with the status `awaiting OK`, the frame paths and the contact-sheet path. Show the sheet and the stills. Stop. Do not animate yet.
7. On an explicit OK, set the status to `approved <date>`. Say that animation comes next. If the owner asks for a change, revise the frames and show them again; do not skip to a render.

## Do not

- Start an animation or a full render before the frames are approved.
- Show a frame you have not opened at full size.
- Hide a mismatch because it is small.
- Spend credits or call a paid video tool without a written cost and an explicit yes.
