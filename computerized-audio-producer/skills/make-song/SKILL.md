---
name: make-song
description: Use when the user wants a song, instrumental or music bed made for free: write and agree the lyrics, generate two takes with ACE-Step on a free Kaggle GPU, check the sung words with speech-to-text, and deliver both takes with the scores.
---

# Make a song for free (ACE-Step on Kaggle, with a lyric check)

Use for songs with vocals, instrumentals and music beds. Everything here is free. The only resource is the owner's free weekly Kaggle GPU quota, shown in their Kaggle account. Never use a paid music service or credits for this without a cost estimate and the owner's explicit yes (see the skill `approval-gate`).

## Before you start

- ACE-Step is MIT-licensed: https://github.com/ace-step/ACE-Step-1.5. Read its README for the current install and run commands, and say what you used. If the page cannot be opened, say so and ask the owner for another source. Do not guess the commands.
- A Kaggle GPU needs the owner's own Kaggle login (https://www.kaggle.com), phone-verified, with internet turned on in the notebook. Signing in is something only the owner can do. Ask them to do it and never store or print their credentials. If there is no login, offer CPU-only short beds, or say the job has to wait.
- Check the remaining GPU quota in their account and tell them the cost in GPU hours before a long run.

## Steps

1. **Lyrics first.** Draft lyrics in the owner's language and show them. Let the owner tweak until they say go (rhyme scheme, tone, facts). Keep them under 4096 characters, with section tags `[Intro] [Verse 1] [Chorus] [Bridge] [Outro]`. No real artist names and no copyrighted lyrics. If the lyrics use real history or people, keep every fact accurate. Avoid regionalisms that do not fit the owner's dialect. Instrumentals and beds skip this step.
2. **Style tags.** One line under 512 characters: genre, mood, instruments, voice, tempo (for example "playful soft pop, female vocals, ukulele, 100 bpm"). Ask for the voice if the owner did not say.
3. **Batch of two takes.** Make a small job list with two different seeds for the same song, and run both in one notebook session, because installing and loading the model is most of the cost. Write repeated choruses out in full. Aim for 30 to 60 seconds for a test and 150 to 180 seconds for a full song.
4. **Run.** Start the session, wait or check back later, and tell the owner the expected ready time. On a T4 GPU, float16 can produce silent or noisy output, so use bfloat16, and retry once in float32 without the language model if a take is silent. Keep the seeds, the prompt, the date and the ACE-Step version next to the files.
5. **Check the words (free, CPU).** Transcribe each take with a speech-to-text model such as faster-whisper (https://github.com/SYSTRAN/faster-whisper) and compare it with the lyrics word by word. Report a score per take and per section: 85% or more is a pass, 65 to 85% is a warning, below 65% is a fail. Speech-to-text under-hears sung vocals, so treat the score as a guide. A whole section missing means the model skipped or replaced it.
6. **Check the sound.** Measure loudness and clipping with ffmpeg as in the skill `audio-handoff`.
7. **If both takes fail** or an important line is missing, tell the owner what was missed, offer one tweak (shorter lines, simpler words, other tags or seeds) and one more batch. Do not loop silently: each retry costs GPU hours.
8. **Deliver.** Hand over both takes with the check scores, the lines worth listening to, the quota used and left, and which take the check prefers. Say that you have not listened to them yourself. Say that the music is AI-generated whenever it is published.
9. **Next.** Ask which take the owner wants before it is used anywhere.

## Do not

- Start a run before the owner has agreed the lyrics and the cost.
- Hand over a take that failed a check, or hide a failure.
- Use real artist names or copyrighted lyrics in a prompt.
- Store the owner's Kaggle credentials anywhere.
