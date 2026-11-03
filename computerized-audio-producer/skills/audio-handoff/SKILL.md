---
name: audio-handoff
description: Use when a script or audio brief needs to become checked, delivered audio, such as narration, a song, a music bed or a sound effect, and the files must be handed to the requester with a report.
---

# Audio handoff

Use when someone gives Cap a script or a brief and expects finished audio.

## Steps

1. Get the input. For narration you need the script text, the platform (it sets the loudness target: YouTube and social about -14 LUFS, podcasts about -16) and the mood. For music you need mood, length and whether it has vocals. Stop and ask if any is missing.
2. Diagnose and plan. Write a short diagnosis (platform, mood, length, language, tools found, cost) and, for narration, a line-by-line pacing plan, and an emotion plan only for the controls the chosen model really has. Show both and wait for an explicit OK before you make anything. Silence is not approval. Do not change the script.
3. Make two takes with free tools. Music: the skill `make-song`. Narration: an open text-to-speech model that the owner chose. Before you use a voice model, read its licence on its model page and say whether it allows commercial use (see `kit/LICENSES.md`). Do not use a model marked non-commercial (for example CC BY-NC) for anything the owner will publish or sell. Emotion comes only from the model's own style or instruction control, if it has one; do not promise per-line emotion otherwise. Use stock or synthetic voices only, or the owner's own recording for the owner's own narration. Sound effects: simple ones synthesised with ffmpeg (for example `ffmpeg -f lavfi -i "sine=f=880:d=0.2" -af afade=t=out:st=0.1:d=0.1 beep.wav`, or `anoisesrc` plus filters), or CC0 or public-domain sounds the owner provides. One take is enough for a short sound effect. If a tool is missing, say which and offer a free alternative. Anything paid needs a cost estimate and an explicit yes first.
4. Check each take. For songs, `kit/check_song.py` runs all of these. For anything else run them by hand:
   - Narration: transcribe with speech-to-text and compare with the script. Any changed, missing or added word fails the take.
   - Duration: `ffprobe -v error -show_entries format=duration -of csv=p=0 FILE`. It must be within 5% of the requested length.
   - Loudness: `ffmpeg -hide_banner -i FILE -af loudnorm=I=-14:TP=-1:LRA=11:print_format=json -f null -` and read `input_i` and `input_tp`. Target about -14 LUFS integrated for social and YouTube, true peak at or below -1 dBTP. To fix a take: `ffmpeg -i FILE -af loudnorm=I=-14:TP=-1:LRA=11 OUT`.
   - Clipping: `ffmpeg -hide_banner -i FILE -af volumedetect -f null -`. Fail if `max_volume` is 0.0 dB or `mean_volume` is below -50 dB.
   - Silence: `ffmpeg -hide_banner -i FILE -af silencedetect=n=-50dB:d=3 -f null -`. Fail on silence longer than 3 seconds in the middle of a take.
5. Mix if asked: duck music under the voice, normalise, and keep voice and music stems as separate files.
6. Write a handoff note next to the files: paths, durations, which take is recommended and why, the loudness and clipping numbers, the transcript match result, and the cost (zero if free).
7. Show the result to the requester. Hand it to a teammate only with SendToAgent, and only if the owner asked for that.

## Do not

- Hand over a take that failed a check, or hide a failure.
- Edit the script, clone a real person's voice, or make podcasts or live audio.
- Spend money, publish, or send anything outside the team without an explicit yes.
- Invent files, numbers or tool results.
