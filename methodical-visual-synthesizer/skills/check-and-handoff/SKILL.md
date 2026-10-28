---
name: check-and-handoff
description: Review your own stills, videos, and files against the brief and the brand book with a concrete checklist, then hand over with the weak spots, the numbers, and the licences listed.
---

# Check and hand off

Use before you show or hand over any design file. Open every file. Do not judge from the config or from memory.

## Checklist

**Brief and diagnosis**
1. Compare the result with the approved diagnosis, line by line. Note any line that is not met.
2. Nothing from the owner's existing assets was changed. New files have new names.

**Brand book** (skill `brand-book`)
3. Run `node scripts/brand-check.mjs`. Every FAIL is fixed or reported. Read the WARN lines too.
4. Colours, type, logo size and clear space, and the tone of the copy match the book. List each deviation as: the rule, what the file does, a proposed fix. If the owner asked for the deviation, ask whether the book should change. Do not edit the book to make a file pass.

**Look (full size, then smallest size)**
5. Open each still at full size and at the smallest size it will be used at. Avatars: look at 48 and 32 pixels, and the 8 times enlargement of 32. The main shape or word still reads.
6. Contrast: text at least 4.5:1, large shapes and accent words at least 3:1.
7. Overlaps and alignment: nothing crosses something it should not (lines through parts, labels on artwork, credits under captions). Margins hold in every format you made (9:16 needs larger top and bottom margins).
8. Text: nothing under about 40 px at 1080p, headlines 45 characters or fewer, no text cut at an edge, no widows in the main headline.
9. Motion: look at a frame in the middle of each transition and at the moment a part is most hidden. Each idea stays on screen long enough to read it (3 seconds or more).

**Sound and captions (video)**
10. `node scripts/qa.mjs <file.mp4>`: expected size and 30 fps, an audio stream, about -14 LUFS, true peak at or below -1.5 dBTP.
11. Captions are the exact written text. Spoken respellings appear only in the voice text. Run a speech-to-text pass on the final mix if one is installed, and check that no sentence was dropped and each hard term was heard right. List the terms that needed a fix.
12. The music is the built-in bed or a credited open-licence track, and the licence note is next to the file.

**Delivery**
13. Fonts and tools used, each with its licence, and the date checked.
14. Cost: say that nothing cost money, or what did and who approved it.
15. A short status note: file paths, sizes and formats, duration, loudness, narration engine, and the exact commands to re-make each file.
16. A list of weak spots in plain words, including the small ones. Say what you could not fix.

Then ask for feedback. If the feedback changes the scope, go back to the diagnosis for that change. If it is a taste (too dry, too busy, too sleepy), offer to write it into the brand book as a do or don't, and wait for the owner's OK.

## Do not

- Say a piece is finished when you did not look at it.
- Hide a weak spot because it is small.
- Fix a problem by lowering a check or editing the brand book.
- Publish or send the files anywhere. That needs the user's yes to that exact action.
