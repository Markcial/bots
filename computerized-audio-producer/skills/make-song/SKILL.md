---
name: make-song
description: Use when the user wants a song, instrumental or music bed made for free: write and agree the lyrics, generate two takes with ACE-Step on the owner's free Kaggle GPU through the kit, check the takes with ffmpeg and speech-to-text, and deliver both takes with the scores.
---

# Make a song for free (ACE-Step on Kaggle, with checks)

Use for songs with vocals, instrumentals and music beds. Everything here is free. The only resource is the owner's free weekly Kaggle GPU quota. Never use a paid music service or credits for this without a cost estimate and the owner's explicit yes (see the skill `approval-gate`).

## Before you start

- You need the kit workspace. Read the memory note `workspace-path`. If it does not exist, run the skill `setup-workspace` first. Run every command below from that folder, with `.venv/bin/python`.
- ACE-Step 1.5 is MIT-licensed, code and weights (https://github.com/ace-step/ACE-Step-1.5, https://huggingface.co/ACE-Step/Ace-Step1.5). The model card allows commercial use of the output but gives no guarantee against similarity to existing works, so say that when it matters. The weights download from Hugging Face without a login. Run the kit; do not rewrite the install. `make_song.py` pins a tested ACE-Step commit (`ACE_STEP_REF`) and forces bfloat16 on the T4. If a newer ACE-Step is needed, pass `--ace-ref` and say so.
- Run `bash doctor.sh` first. It checks the Kaggle command line, the login, the weekly GPU quota and the kernel settings. Anything it reports as missing goes to the owner as a short numbered list.
- The owner does these three things themselves, in their own browser and terminal: (1) create a free Kaggle account at https://www.kaggle.com and verify the phone number (Kaggle gives GPU and internet only to phone-verified accounts); (2) open https://www.kaggle.com/settings/api and generate a token; (3) put it where the command line reads it: `kaggle auth login`, or the file `~/.kaggle/access_token`, or `~/.kaggle/kaggle.json` with `chmod 600`, or the variable `KAGGLE_API_TOKEN` (or `KAGGLE_USERNAME` and `KAGGLE_KEY`). **Never ask for the token in chat, and never print it or write it to a memory note, a log or a repository.** You only run `kaggle` and the kit scripts, which read it from that location.
- The kernel must be private, with the GPU on and internet on. Without those flags Kaggle runs on CPU with no network. The kit sets them and `doctor.sh` checks them.
- There is no reference audio or voice cloning in this skill. Use text prompts only.

## Steps

1. **Lyrics first.** Draft lyrics in the owner's language and show them. Let the owner tweak until they say go (rhyme scheme, tone, facts). Keep them under 4096 characters, with section tags `[Intro] [Verse 1] [Chorus] [Bridge] [Outro]`. No real artist names and no copyrighted lyrics. If the lyrics use real history or people, keep every fact accurate. Avoid regionalisms that do not fit the owner's dialect. Instrumentals and beds skip this step.
2. **Style tags.** One line under 512 characters: genre, mood, instruments, voice, tempo (for example "playful soft pop, female vocals, ukulele, 100 bpm"). Ask for the voice if the owner did not say.
3. **Batch of two takes.** Write `jobs.json`: a list of `{"id","caption","lyrics","duration","seed","language","bpm","instrumental"}` (see `examples/jobs.example.json`), with two different seeds for the same song, in one file. Setup is most of the cost. Write repeated choruses out in full. Aim for 30 to 60 seconds for a test and 150 to 180 seconds for a full song. Measured on a Kaggle T4: setup about 4 minutes, model load about 2.5 minutes, then about one minute per minute of audio, so a two-take test is about 8 to 12 minutes, roughly 0.15 to 0.2 GPU hours.
4. **Dry run, quota, estimate.** `.venv/bin/python make_song.py --jobs jobs.json --out OUT --dry-run`, then `.venv/bin/python make_song.py --quota`. Tell the owner the expected GPU hours and the hours left this week before a run. Do not start before the owner has agreed the lyrics and the cost.
5. **Run.** `.venv/bin/python make_song.py --jobs jobs.json --out OUT` (add `--timeout SECONDS` to cap the GPU time). It pushes a private kernel with `kaggle kernels push --accelerator NvidiaTeslaT4 -t TIMEOUT`, polls `kaggle kernels status`, downloads with `kaggle kernels output`, checks that the output belongs to this run, and copies the audio to `OUT`. For a long job add `--no-wait`, tell the owner the expected ready time, and fetch later with `--fetch RUN_ID`. If a take is silent or noise, read `runs/RUN_ID/output/out/results.json` and the kernel log.
6. **Record the job.** When a run is pushed, add one line to the memory note `cap-jobs`: `run id | kernel | status | date | output folder` (the script prints this line after `--no-wait`; `--list` prints it for any unfinished run). Update the line when the run is fetched (`fetched`) or fails (`failed`). The weekly routine reads this note.
7. **Check the takes.** `.venv/bin/python check_song.py OUT/*.mp3 --results runs/RUN_ID/output/out/results.json --lyrics lyrics.txt --language CODE --json OUT/report.json`. It checks duration, clipping, silence and loudness with ffmpeg (the exact commands are in the skill `audio-handoff`), and the sung words with faster-whisper: 85% or more is a pass, 65 to 85% a warning, below 65% a fail, per take and per section. Speech-to-text under-hears singing, so treat the score as a guide. A whole section missing means the model skipped or replaced it. A loudness warning is fixed with a normalise pass (command in `kit/README.md`).
8. **If both takes fail** or an important line is missing, tell the owner what was missed, offer one tweak (shorter lines, simpler words, other tags or seeds) and one more batch. Do not loop silently: each retry costs GPU hours.
9. **Deliver.** Hand over both takes with the check scores, the lines worth listening to, the quota used and left (from `make_song.py`), and which take the check prefers. Say that you have not listened to them yourself. Keep the seed, prompt, date and ACE-Step commit next to the files (they are in `results.json`). Say that the music is AI-generated whenever it is published.
10. **Next.** Ask which take the owner wants before it is used anywhere.

## Do not

- Start a run before the owner has agreed the lyrics and the cost.
- Hand over a take that failed a check, or hide a failure.
- Use real artist names or copyrighted lyrics in a prompt.
- Ask for, read, print or store the owner's Kaggle token anywhere in chat, memory notes, logs or a repository.
