# Lessons from earlier design jobs

Generic lessons from real avatar, still, and explainer-video jobs made with this kind of harness (Remotion, free local voice, code-made music). No names, handles, or private details. The skills apply them. The bot reads this file before a motion job, and adds a line when a job teaches something new (with the owner's OK to save it in the repo).

Each lesson: what went wrong or what worked, then the rule.

## Voice and captions
1. **A hard word came out wrong** (a product name read as "Skonfig", a name read as "Ralo"). Test every hard term alone and inside its real sentence, hear it, and fix it in the voice text only (a respelling, letters spaced out, or a comma for a pause). Captions, titles, and the written script keep the real spelling. Never show a phonetic respelling.
2. **A word at the start of a clip lost its first syllable** ("Parse, don't validate" lost "Parse"; "Coerce" became "coarse"). Start that clip with an ellipsis in the voice text, or merge it with the line before so the first syllable has a lead-in.
3. **Two words fused** ("calling getTime throws" became "call and get time"). A comma in the voice text separates them. A swallowed ending ("parsed JSON" heard as "parse JSON") also gets a comma.
4. **A speech-to-text pass on the final mix catches dropped sentences.** It is noisy on odd terms, so judge the terms by ear and use the pass to check that every sentence is present. Keep a short table: term, what it said first, the fix that worked.
5. **Captions match the narration** because they are timed per sentence from the measured clip lengths and split at about 44 characters, not guessed. A caption shows the exact text of the script.

## Sound
6. **Loudness is measured on the final MP4**, not on the mix before it was muxed. Target about -14 LUFS with true peak at or below -1.5 dBTP. A sparse voice track can miss the target in one pass, so run the loudness step again on the final mix. `scripts/qa.mjs` reports it.
7. **Ducking:** the bed sits about 8 to 9 dB down before ducking, drops 18 to 22 dB under speech, attack about 50 ms, release about 400 to 600 ms. Keep the bed's energy under 1 kHz so consonants stay clear. A bed that is a little bland under narration is the right bed.
8. **Music rights:** a bed made in code from synthesis (no samples) has no third-party claim. Say so in a licence note next to the video. Any other track needs the owner's yes, an open licence, and a credit.

## Look
9. **Small-size legibility.** An avatar that is good at 1024 can be mush at 48 and 32. Render each size natively, drop fine detail at 64 and below, and keep one bright element. Look at the 32 px render enlarged 8 times.
10. **Hidden parts change the shape.** A part tucked behind another can read as a different shape for a second (a piston read as a hollow U near the top of its stroke). Look at the frames where a part is most hidden, not only the first and last.
11. **Overlaps hide in the busiest moment.** A dimension line crossed a part in the intro, and a credit sat under the caption until it was raised. Keep labels in fixed columns, never on top of artwork. Keep credits and lower thirds above the caption zone. Check a mid-transition frame.
12. **Dense scenes fail.** A scene with two code panels was too dense. Split it, or show one thing at a time. Headlines of 45 characters or fewer, text of 40 px or more at 1080p.
13. **Contrast is a number.** Text 4.5:1, large shapes and accent words 3:1. A light brand colour that fails on white gets a darker text-safe variant (`primaryText`). `scripts/brand-check.mjs` measures it.
14. **Thumbnails are separate pieces.** Design them at their real size (for example 1280 by 720) and look at them small. A long title wraps, so make the one key word big.
15. **Flat tones can be right.** Crisp flat colour with one light direction looks mature and renders fast. Say honestly that it is less rich than hand illustration, and let the owner choose.
16. **The metaphor must match the job.** An avatar for a drawing tool should show a drawing tool (a canvas and a pencil), not rulers and compasses, which read as arithmetic. Check the object against what the bot does.
17. **Feedback in plain words is a rule to save.** "A bit dry" meant "add a second thing happening and a person in motion". "Avoid the sleepy look" meant "awake, relaxed". Turn such feedback into a proposed do or don't, and ask whether it joins the brand book.

## Tokens and type
18. **One tokens file, no hard-coded colours.** Every component reads the palette, type, and stroke weights from tokens. Then a palette swap is one prop, and a brand book can supply the tokens.
19. **Fonts:** only SIL OFL or Apache-2.0, installed on this computer, name matched exactly (`fc-list : family | grep -i <name>`), licence written in a short `FONTS-LICENSE` note.
20. **Icons and shapes are drawn for the piece.** Original SVG avoids a licence question. If a library is used, record its licence.
21. **A contact sheet before motion.** One image with the palette (hex and role), type specimens, the shape system, and a few key frames. The owner reacts to stills before any animation is built.

## Process and speed
22. **Stills first.** `--stills` shows every scene in seconds, and a full render takes about a minute per minute of video. Fix on stills, then render once.
23. **Cache and re-run cheaply.** Narration is cached per sentence, so a changed line re-makes one clip. Keep timings in data and the whole piece follows a changed line.
24. **Shared machines run out of memory.** Check free memory, use `--concurrency=1` or `2`, and never run a voice job and a render, or two renders, at the same time.
25. **Formats come from one source.** Make the 16:9 master, then 1:1 or 4:5, then 9:16 (bigger top and bottom margins) from the same composition. Do not redraw each one.
26. **Ask which sign-off goes on which channel.** A signature or handle that is right on one channel may not be wanted on another. The owner decides, and the answer goes in the brand book.
27. **Write a status note with every deliverable:** paths, size, duration, loudness, narration engine, the term table, the licences, the weak spots, and the exact commands to re-make each file.
28. **Hand over honestly.** Name the weak spots, including the small ones, and re-render after a fix. Do not say finished before you look.
29. **Nothing is published or sent** until the owner says yes to that exact action, and a paid image generator needs the cost stated first.
