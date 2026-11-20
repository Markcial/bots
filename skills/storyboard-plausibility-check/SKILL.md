---
name: storyboard-plausibility-check
description: >-
  Use before showing ANY storyboard panel, generated still or video frame: locks
  continuity and physical plausibility (scale, poses, how bodies and hands
  actually perform each action) and regenerates failures first.
---
# Storyboard plausibility check

Run this every time, for every panel, before anyone sees it. Image generators get the look right but not physics, so never trust a quick look.

## 1. Before generating
1. Write `continuity.md` for the scene: set layout, props (position, real size, material), lighting, character look (clothes, accessories, which sleeve state), and the camera for each panel.
2. For EVERY action in the scene, write its real-use geometry: where the body is, which side the limbs/wrists come from, the palm direction, the thumb side, the contact point, and what is near and far relative to the body (e.g. at a keyboard: the player sits facing the keys, the forearms come from the bench side, the palms face down, the fingers point away from the player, the black keys are on the far side of the white keys, the stop knobs are pulled toward the player).
3. Write real-world dimensions: furniture, people's heights, instrument and object sizes.

## 2. Blockout
1. Build a real-scale 3D blockout (any renderer; a simple numpy/PIL box renderer is fine) of the set AND the body in its pose, including simple hand/forearm boxes for close-ups.
2. Render it from each panel's camera, and use those renders plus a master set image as references for generation.

## 3. Generate, then supervise each panel
Compare every panel with its blockout (a 50% overlay) and answer each question explicitly. Any "no" means regenerate.
- Could a real person do this pose/action from this camera? Where is their body relative to the frame, and do the limbs enter from that side?
- Are hands, palms, thumbs and fingers oriented as in the use geometry?
- Are sizes and proportions real (furniture height vs. body, objects vs. hands)?
- Does it match continuity.md: same set, the same props in the same places, nothing missing, the same character look?
- Does the shot type match what was asked (a close-up is truly tight, a wide is truly wide)?
- Is there no invented text, extra limbs or warped anatomy?

## 4. Report
Show only panels that pass. List any remaining mismatches honestly, in plain words, and keep the rejected versions with names that say why they failed.
