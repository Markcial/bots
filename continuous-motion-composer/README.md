# Continuous Motion Composer

Stage: **sketch**. The template text is in this repo. Nothing is published. There is no install link and no avatar or motion video yet.

Composes short motion pieces from a brief, a script and any characters or assets you already have. A written diagnosis, an approved storyboard and style frames come before any animation. Remotion and other free, code-first tools are the default. Motion has rhythm and a story, not a slideshow of stills. It flags the cost of any paid video tool before suggesting one, and it never publishes, sends or buys anything without your explicit yes.

## Use cases

- Turn an approved script and character designs into a timed storyboard, style frames and a motion cut in 16:9, 9:16, or both.
- Make a short motion sting or explainer visual in Remotion, synced to voice timings when they exist.
- Check a cut for overflow, legibility and secrets on screen, and hand over the files with the commands to re-make them.
- Hand back script writing, character design, original narration or songs, brand-book work, and any publish or paid-generation request until the owner says yes.
- Refuse: skipping the diagnosis or the style-frame OK, slideshows of screenshots, cloning a living person's likeness, and spending credits without a written cost.

## Tools it uses

All free by default.

| Job | Tool | Status |
| --- | --- | --- |
| Motion (default) | [Remotion](https://www.remotion.dev) (code-first; free for individuals, teams of up to three, and non-profits — [licence FAQ](https://www.remotion.dev/docs/license/faq)) | Direct: the bot writes a Remotion project on the owner's computer |
| Stills, contact sheets, loudness | `ffmpeg` and `ffprobe` | Direct |
| Real 3D | [Blender](https://www.blender.org) (GPL) when it is installed | Optional, free |
| Voice, songs, original beds | An audio teammate such as [Computerized Audio Producer](../computerized-audio-producer) | Handed in; this bot muxes, ducks and checks the picture mix |
| Paid image-to-video or text-to-video | Owner's choice | Never the default; written cost and an explicit yes first |

This sketch has no kit folder. One may be added at `prepare`. Until then the bot uses Remotion and ffmpeg directly, and says so if a tool is missing.

## Install

There is no published template yet. To try the words: create the bot from `profile.md`, add each skill with its YAML frontmatter, paste `memories.md` as seed knowledge, and schedule every routine with its 5-field cron in the user's timezone.

You need a **computer with a shell** (Linux, macOS, or Windows with WSL): Node.js, ffmpeg and Remotion run there. A bot with no computer can plan a storyboard but cannot render.

## Media

Identity and a motion presentation video belong in `media/` at the `prepare` stage. This sketch has none.

## For contributors: when you copy this

- Every `SKILL.md` has YAML frontmatter with `name` (the folder slug) and `description`.
- Every routine has a 5-field cron, the user's timezone, and a delivery line.
- An installed bot cannot see this repo on disk. Skills use full URLs and real tool names, with a fallback when a fetch or plugin is missing.

## Stage

`sketch`. Advance only when the exit criteria in the repository README are met. Do not publish at this stage.
