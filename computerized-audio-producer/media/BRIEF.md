# Media brief: Computerized Audio Producer

Status: **avatar and motion video made, waiting for the owner's review**. The avatar set, the 16:9 and 1:1 videos and the sample frame are in this folder. Nothing is published.

## Family look

Match the other avatars in this repo. Each one is a single glass object with an inner glow, on a dark charcoal rounded square, lit from within, with soft bloom and a faint reflection below. One object, one colour, no text, no face, no mascot.

## Avatar (done)

- **Colour:** emerald. Accent `#34E39A`, with a deeper green for the glass and a near-white highlight. Background charcoal, the same rounded-square plate as the other avatars.
- **Motif:** five layered glass panes in a row, seen at a slight angle, with one glowing waveform line running through all of them. Small rings mark a few points on the line. A soft green pool of light sits under the object.
- **Concept in one line:** layers of glass with one emerald waveform passing through them, glowing on charcoal. The layers say "mixing", the waveform says "audio".
- **Sizes:** 1024, 512, 256, 128, 48, 32 (`media/avatar-1024.png` and siblings).

## Motion presentation (done)

Same format as the other videos in this repo: 1920×1080, 30 fps, h264 with AAC audio, 16:9, plus a 1:1 cut, about 30 to 36 seconds. Look: near-black background, a small numbered chip top left, the avatar on the left, a headline on the right in emerald and white, and a caption pill at the bottom that repeats the narration so the video works without sound. Built in code with the timings in data. Suggested beats:

1. One brief in, finished audio out.
2. Narration in a stock voice, checked against the script.
3. Songs, beds and sound effects, free tools first.
4. Two takes, and every take is checked against the script and for loudness.
5. Nothing is sent, published or bought without your explicit yes.
6. Ask Cap for a sound.

- **Narration:** normal spelling in captions, no phonetic respelling.
- **Music:** a soft procedural bed made in code, ducked under the voice, about -14 LUFS overall, with no sampled or third-party material (see [`LICENSE-music.md`](../../LICENSE-music.md)).
- **Deliverables:** `media/cap-16x9.mp4`, `media/cap-1x1.mp4`, `media/sample-frame.png`.
- **Tools:** free tools only. Any paid generation needs the owner's yes, with the cost stated first.

### How the video was made

Made with Cap's own kit, free tools only, no sampled or third-party audio.

- **Format:** `media/cap-16x9.mp4` (1920×1080) and `media/cap-1x1.mp4` (1080×1080), 30 fps, h264 with AAC audio, 34.9 s each, about 2.9 MB and 2.3 MB. `media/sample-frame.png` is the "Free tools first" beat.
- **Picture:** Remotion, in code, with the chips, headlines and caption timings generated from the narration manifest so a line can move without a re-edit.
- **Narration:** `kit/narrate.py` with Phonon 31M (Apache-2.0), the stock voice Easton, one line per beat. `kit/check_song.py --kind narration` heard 100% of the script words, also on the final mix.
- **Music:** a soft procedural bed made in code (NumPy synthesis, no samples), ducked under the voice.
- **Effects:** five whooshes from `kit/make_sfx.py`, one into each beat after the first.
- **Loudness:** whole mix at -14.0 LUFS integrated, true peak -1.5 dBFS (ffmpeg ebur128).
- **Checked by numbers, not by ear.** The owner listens before anything is published.
