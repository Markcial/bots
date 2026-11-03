---
name: audio-handoff
description: Use when a script or audio brief needs to become checked, delivered audio, such as narration, a song, a music bed or a sound effect, and the files must be handed to the requester with a report.
---

# Audio handoff

Use when someone gives Cap a script or a brief and expects finished audio.

## Steps

1. Get the input. For narration you need the script text, the platform (sets the loudness target) and the mood. For music you need mood, length and whether it has vocals. Stop and ask if any is missing.
2. Diagnose and plan. Write a short diagnosis (platform, mood, length, language, tools found, cost) and, for narration, a line-by-line emotion and pacing plan. Show both and wait for an explicit OK before you make anything. Silence is not approval. Do not change the script.
3. Make two takes with free tools (open TTS with emotion tags; the skill `make-song` for music). One take is enough for a short sound effect. If a tool is missing, say which and offer a free alternative. Anything paid needs a cost estimate and an explicit yes first.
4. Check each take:
   - Narration: transcribe with speech-to-text and compare with the script. Any changed, missing or added word fails the take.
   - Loudness: measure with ffmpeg loudnorm. Target about -14 LUFS integrated for social and YouTube, true peak at or below -1 dBTP.
   - Clipping: run ffmpeg volumedetect. Any clipping fails the take.
5. Mix if asked: duck music under the voice, normalise, and keep voice and music stems as separate files.
6. Write a handoff note next to the files: paths, durations, which take is recommended and why, the loudness and clipping numbers, the transcript match result, and the cost (zero if free).
7. Show the result to the requester. Hand it to a teammate only with SendToAgent, and only if the owner asked for that.

## Do not

- Hand over a take that failed a check, or hide a failure.
- Edit the script, clone a real person's voice, or make podcasts or live audio.
- Spend money, publish, or send anything outside the team without an explicit yes.
- Invent files, numbers or tool results.
