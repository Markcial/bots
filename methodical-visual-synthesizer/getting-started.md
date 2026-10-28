# Getting started

This bot is a sketch. It diagnoses first, then builds in code with free tools. It cannot publish, spend, or contact anyone for you.

1. **Set up its workspace (first run only, a few minutes).** A template carries only text, so the bot fetches its own tool kit from the public repo (`github.com/Markcial/bots`, folder `methodical-visual-synthesizer/kit`) onto its computer.

   First message to try: `Set up your workspace.`

   It tells you what it will install and asks for your yes first. Everything is free and needs no account: Node.js, ffmpeg, Remotion, and optionally a free local voice for narration. It will ask whether you may use Remotion for free (individuals, non-profits, and companies of up to 3 people can). It runs a self-check, then shows you a 2 second test clip and a test avatar. It saves the folder in the memory note `workspace-path`. If a step would need a paid account, it stops and asks.
2. **Describe the project** in a line or two, and say where the files should go.

   First message to try: `I need an avatar and a 30 second motion intro for <project>.`

3. **Answer its five questions.** It does not design yet. If it already keeps a brand book for you, it reads it first and skips what the book answers. It asks about the brief, the audience, the assets you already have, the constraints, and the references you like and dislike. Share files or links if you have them.
4. **Approve the diagnosis.** Read the written diagnosis it sends back. Say OK, or say what to change. Silence is not an OK. It saves the diagnosis as the memory note `diagnosis-<project-slug>` with the status `awaiting OK`, then `approved <date>` after your yes.
5. **Start your brand book.** Say `Start a brand book for <brand>`, or accept its offer after the diagnosis. It writes a draft: palette with hex and contrast pairs, type with licences, logo and avatar rules, voice and tone, motion rules, do and don't, references, and a dated change log. It saves the summary as the memory note `brand-book-<brand-slug>` and the file `brand/<brand-slug>/brand.json` in its workspace, and shows you the contrast results. Approve it or change it. After your OK it only changes with your yes, and every new piece is checked against it. If you only want to track a brand you already have, hand it your colours, fonts, and logo, and it records them and flags gaps.
6. **Pick a direction.** It proposes two or three, each tied to a line in the diagnosis. Choose one, or ask for a change.
7. **It builds.** Avatars are drawn in code, with the colours from your brand book. Motion is made in Remotion, with free narration (or captions only), a quiet music bed that ducks under the voice, and a closing card. If a step would cost money, such as paid image generation, credits, or a paid font, it says so first and waits for your yes.
8. **Check the result.** It runs a checklist: the brand check, its own stills and frames at full size and at 32 pixels, loudness of the video, and captions against the script. It hands over the files with the paths, the commands to re-make them, and a note on what is weak and where it deviates from the book. Look at the avatar at the smallest size yourself.
9. **If the scope changes**, it diagnoses the change before it builds it.
10. **Optional routines.** Keep your projects as diagnosis notes, your brands as brand-book notes, and list your tools and fonts in the note `tool-notes`. The Monday review and the monthly licence check read those notes.
