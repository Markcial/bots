---
name: qa-frames
description: Review stills and rendered frames on a contact sheet for overflow, legibility and secrets on screen, then hand over with the weak spots and the commands to re-make the files.
---

# Check frames and hand over

Use before you show or hand over any motion file. Open every file. Do not judge from the config or from memory.

## Checklist

**Brief and gates**
1. Compare the result with the approved diagnosis, storyboard and style frames, line by line. Note any line that is not met.
2. Nothing from the owner's existing assets was changed. New files have new names.

**Look (contact sheet, then full size)**
3. Build or refresh a contact sheet from the render (a frame every half second is enough for a short piece). Open the sheet and then open the weak frames at full size, including a frame in the middle of each transition and the moment a part is most hidden.
4. Overflow and alignment: nothing crosses something it should not (a label on artwork, a credit under a caption, type cut at an edge). Margins hold in every format you made (9:16 needs larger top and bottom margins).
5. Legibility: text contrast at least 4.5:1, large shapes at least 3:1. Nothing under about 40 px at 1080p. Headlines 45 characters or fewer. Each idea stays on screen long enough to read (about 3 seconds or more).
6. Secrets on screen: no API tokens, passwords, private addresses, unread notification counts, other people's faces, or handles, signatures and links the owner did not choose for that channel. If you find one, cover or remove it and say what you found, without repeating the secret.

**Sound and captions**
7. Probe the file: `ffprobe -v error -show_entries format=duration,size -of default=nw=1 FILE`. Expect the requested size and frame rate, and a duration within a small margin of the plan (say why if the narration is longer than the brief).
8. Loudness: `ffmpeg -hide_banner -i FILE -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -` and read `input_i` and `input_tp`. Target about -14 LUFS integrated for social and YouTube, true peak at or below -1 dBTP, no clipping. If a tool cannot run, say so and do not invent numbers.
9. Captions are the exact written text. Spoken respellings appear only in the voice text. If a speech-to-text tool is installed, run it on the final mix and check that no sentence was dropped.

**Delivery**
10. Cost: say that nothing cost money, or what did and who approved it.
11. A short status note: file paths, sizes and formats, duration, loudness, which compositions you rendered, and the exact commands to re-make each file (including `--concurrency=1`).
12. A list of weak spots in plain words, including the small ones. Say what you could not fix.

Then ask for feedback. If the feedback changes the scope, go back to the diagnosis for that change.

## Do not

- Say a piece is finished when you did not look at it.
- Hide a weak spot because it is small.
- Repeat a secret you found on screen; describe the kind of secret and where it was.
- Publish or send the files anywhere. That needs the user's yes to that exact action.
