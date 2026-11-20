---
name: plan-storyboard
description: Write a storyboard after an approved diagnosis, with one strong change per beat and only what the chosen tools can actually do, then wait for the owner's OK.
---

# Plan the storyboard

Use after an approved diagnosis, before any style frame or render. The memory note `diagnosis-<project-slug>` must say `approved`.

## Steps

1. Read the approved diagnosis and the script, characters and assets named in it. If the note is missing or still `awaiting OK`, go back to the skill `diagnose-motion`.
2. Write one row per beat:
   - time range (use placeholder times if voice has not arrived)
   - the one thing that changes (the viewer should be able to name it when the beat ends)
   - what is on screen (headline of 45 characters or fewer, any caption line)
   - the narration line, if there is one
   - how it moves
3. **One strong change per beat.** If two ideas compete, split the beat. Give each idea enough time to read: about 3 seconds or more, and more when the type is dense. Time long explainers to the narration, not to a fixed metronome.
4. **Only what the tools can do.**
   - Remotion (the default): transforms, masks, typed text, code-drawn shapes, sequenced stills that then move, simple layered characters. Not photoreal fluid, not unseen physics, not a feature-film camera in one prompt.
   - Blender (free, when installed and the brief needs real 3D): real cameras, lights and geometry. Still plan poses and scale that a body can hold.
   - A paid image-to-video or text-to-video service: not in the plan unless the diagnosis already recorded the cost and the owner said yes.
5. **Plausibility.** Before anyone sees a panel, check continuity and physical sense. For a body, a hand or a real object, write the real-use geometry: where the body is, which side the limbs enter from, the palm and thumb side, the contact point, and real sizes relative to the frame. Ask, and answer, whether a real person could do this from this camera. Reject a beat that needs extra limbs, warped anatomy, invented on-screen text, or a move the toolchain cannot produce. Keep rejected versions with names that say why they failed, and do not show them as the proposal.
6. On-screen code, errors and numbers come from a real command or from a file the owner provided. Do not invent them to look technical.
7. Save the storyboard as a memory note titled `storyboard-<project-slug>` with the status `awaiting OK`, and show it to the user. Stop.
8. On an explicit OK, set the status to `approved <date>`. Say that style frames come next.

## Do not

- Draw final frames or start a render before the storyboard is approved.
- Pile two dense panels into one beat.
- Plan a slideshow of screenshots. The idea itself has to move.
- Show a phonetic respelling in a caption or a title.
- Put a handle, a signature or a link on a piece the owner did not choose for that channel.
