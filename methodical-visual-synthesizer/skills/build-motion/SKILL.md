---
name: build-motion
description: Build a short motion piece or explainer in Remotion from an approved storyboard and the brand book, with timings in data, captions that match the narration, and a bed that ducks under the voice.
---

# Build motion

Use after an approved diagnosis and a chosen direction, when the user wants a short motion piece or explainer. Motion is code-driven. Work in the kit folder saved in the memory note `workspace-path` (if the note is missing, run the skill `setup-workspace` first), and read its `README.md` for the commands.

## Steps

1. **Brand book.** Read `brand-book-<brand-slug>`. The config points at it with `"brand": "brand/<brand-slug>/brand.json"`, so the palette, fonts, and avatar colours come from the book and cannot drift. If there is no book, create a draft first (skill `brand-book`).
2. **Storyboard first.** One row per scene: time range, on-screen headline (45 characters or fewer), the narration line, and what moves. Aim for 30 to 45 seconds for a short piece. Give each idea at least 3 seconds, and more when it has to be read. Long explainers are timed to the narration, not to a fixed beat. Ask the user to approve it.
3. Copy `configs/_template.json` to `configs/<project>.json` and fill it from the storyboard. Scene timings follow the narration, so a line can change without a re-edit.
4. **Narration.**
   - Write it in normal spelling. Test each hard term (names, acronyms, code words) alone in a short sentence and again inside its real sentence, and listen, or run a speech-to-text pass if one is installed.
   - Fix a bad word in the voice text only: add it to `pronounce` (a respelling such as `Ray low`, or letters spaced out, or a comma for a pause). Captions, on-screen text, and the written script keep the real spelling, and no phonetic spelling is ever shown.
   - A word that opens a clip can lose its first syllable: start that clip with an ellipsis in the voice text only, or merge it with the line before. A word fused with the next one (`call and get time`) usually needs a comma.
   - Keep a small table of the terms, what the voice said at first, and the fix that worked. Put it in the handoff.
5. **Music.** Use the kit's built-in bed (code-generated, no samples). It sits at about -9 dB before ducking, drops 18 to 22 dB under speech, and the whole mix lands at about -14 LUFS and -1.5 dBTP. Another track needs the owner's yes, an open licence, and a `music.credit` with title, author, URL, and licence. Keep the music licence note next to the video.
6. **Layout check before any render.** Run `node scripts/make.mjs configs/<project>.json --stills` and look at each scene still at full size, including a frame in the middle of a transition. Look for overlaps (a dimension line across a part, a label on top of artwork, a credit under the caption), weak contrast, text too small at 1080p, a part that hides behind another and changes shape, and scenes with two dense panels (split them). Keep credits and lower thirds above the caption zone. Fix, and look again.
7. **Render.** `node scripts/make.mjs configs/<project>.json` gives 16:9 at 1920 by 1080 and 30 fps. Before it, check free memory and that no other heavy job (a voice run, another render) is going, and use `--concurrency=1` or `2` on a shared computer. A 1:1 or 9:16 cut is not in the kit: say so, and add a composition to `src/Root.tsx` from the same source only if the user wants one. For 9:16, use bigger top and bottom margins. A thumbnail is its own piece (skill `build-identity`, step 9).
8. **Measure the final file.** `node scripts/qa.mjs out/<slug>.mp4` reports size, frame rate, duration, loudness, and true peak of the MP4 itself. If a sparse voice track misses -14 LUFS, run the loudness step again on the final mix before you mux. If a sentence could have been dropped, run a speech-to-text pass on the final mix and compare it with the script.
9. Run `node scripts/brand-check.mjs` and the checklist in the skill `check-and-handoff`. Say what is weak. Report the file paths, the duration, the loudness, the narration engine, and the commands that re-render each file.

## Do not

- Render before the storyboard is approved.
- Use music or footage whose licence you cannot state.
- Show a phonetic respelling in a caption, a title, or the script you hand over.
- Put signatures, handles, or links on a piece that the owner did not choose for that channel. Ask which sign-off goes on which channel.
- Leave a heavy render running on a shared machine without checking what else is running.
