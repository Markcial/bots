# Cap kit

The tools behind the Computerized Audio Producer's songs: make songs with [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) on **your own free Kaggle GPU**, then check every take before anyone hears it. Free by default: the only resource used is your weekly Kaggle GPU quota. Nothing here publishes, sends, buys or contacts anyone.

Cap fetches this folder for you when you say `Set up your workspace`. You can also use it by hand.

## What you need

- A computer with a shell and internet: Linux, macOS, or Windows with WSL. A chat-only bot with no computer cannot run this kit.
- `python3` 3.11 or newer, `ffmpeg` (with `ffprobe`), `curl` and `git`.
- A free [Kaggle](https://www.kaggle.com) account. **You create it and sign in yourself.** Cap never sees your password.

## Kaggle setup (once, by you)

1. Create a free account at https://www.kaggle.com and **verify your phone number** in the account settings. Kaggle only gives GPU and internet to phone-verified accounts.
2. Open https://www.kaggle.com/settings/api and press **Generate New Token**.
3. Put the token where the Kaggle command line reads it. Pick one:
   - run `.venv/bin/kaggle auth login` in your terminal (after `setup.sh`), which signs in through your browser; or
   - save the token as the file `~/.kaggle/access_token`, or the legacy file `~/.kaggle/kaggle.json` (from "Create Legacy API Key"), then run `chmod 600` on it; or
   - set `KAGGLE_API_TOKEN` (or `KAGGLE_USERNAME` and `KAGGLE_KEY`) in your shell.

The rule: **you put the token there yourself. Cap never asks for it in chat, never prints it, never writes it into a memory note, a log or a repository.** Cap only runs `kaggle` and the scripts below, which read the token from that location. `.gitignore` already blocks `.kaggle/`, `kaggle.json` and `access_token`.

## Install and check

```
bash setup.sh      # checks the tools, creates .venv with the Kaggle CLI and faster-whisper
bash doctor.sh     # checks the login, GPU quota, kernel settings and network. Costs no GPU time.
```

`doctor.sh` prints PASS, WARN or FAIL lines. It checks that the kernel will have the GPU on, internet on, a T4 and private (without those Kaggle silently runs on CPU with no network), that the pinned ACE-Step commit still exists, and how many GPU hours are left. Phone verification cannot be checked from the command line; if a push fails or runs without a GPU, check it in your Kaggle settings.

## Make a song

1. Write a jobs file. Start from [`examples/jobs.example.json`](examples/jobs.example.json): a list of songs, each with `id`, `caption` (style tags, under 512 characters), `lyrics` (under 4096 characters, with `[Verse 1]`, `[Chorus]` tags; leave out for instrumentals), `duration` (10 to 600 seconds), `seed`, `language`, optional `bpm` and `"instrumental": true`. Make **two takes of a song with two different seeds in one file**: setup is most of the cost.
2. Dry run (builds and checks the kernel, pushes nothing):

   ```
   .venv/bin/python make_song.py --jobs my-jobs.json --out out --dry-run
   ```

3. Run. It pushes a private kernel named `cap-make-song` to your Kaggle account with a hard time limit, waits, downloads, checks that the output belongs to this run, and copies the audio to `out/`:

   ```
   .venv/bin/python make_song.py --quota                          # GPU hours used and left this week
   .venv/bin/python make_song.py --jobs my-jobs.json --out out    # add --timeout 900 to cap the GPU time
   ```

   For a long job use `--no-wait`, then `make_song.py --fetch RUN_ID` later, and `make_song.py --list --refresh` to see runs that are not finished.
4. Check the takes:

   ```
   .venv/bin/python check_song.py out/*.mp3 --results runs/RUN_ID/output/out/results.json --lyrics lyrics.txt --language en --json out/report.json
   ```

The output lands in `out/` and the seed, timings, GPU and ACE-Step commit of each run in `runs/RUN_ID/output/out/results.json`. Keep the seed, prompt and date with the files.

## What it costs

Measured on a Kaggle T4: setup about 4 minutes, model load about 2.5 minutes, then roughly one minute per song of one minute. A two-take test of 30 seconds each takes about 8 to 12 minutes, which is about **0.15 to 0.2 GPU hours** of your weekly quota. Read the weekly total from `make_song.py --quota`; do not assume it. A run that hits `--timeout` is killed, and the quota is wall-clock, so a long timeout is a long possible bill in hours, not in money.

## What `check_song.py` checks

Per take, with ffmpeg:

| Check | How | Result |
| --- | --- | --- |
| Duration | `ffprobe` against the requested length | FAIL if more than 5% off |
| Clipping | `volumedetect`, max volume at 0.0 dB | FAIL |
| Silence | mean volume below -50 dB, or over 3 s of silence inside the take | FAIL (silent takes are the known failure on a T4) |
| Loudness | `loudnorm` integrated LUFS and true peak against -14 LUFS and -1 dBTP | WARN, fixable by a normalise pass |
| Lyrics (optional, `--lyrics`) | `faster-whisper` on the CPU, words heard back against the lyrics, per section | PASS 85% or more, WARN 65 to 85%, FAIL below 65% |

Speech-to-text under-hears singing, so the lyrics score is a guide, not a verdict. A whole section missing means the model skipped or replaced it. The script exits non-zero when every take fails, and it prints the preferred take. These are numbers, not listening: say so when you hand takes over. To normalise a take to the target afterwards:

```
ffmpeg -i take.mp3 -af loudnorm=I=-14:TP=-1:LRA=11 -ar 44100 take-normalised.mp3
```

## How the Kaggle kernel works

[`kernel/bootstrap.py`](kernel/bootstrap.py) runs on Kaggle's system Python: it installs `uv`, clones ACE-Step, checks out the pinned commit in [`ACE_STEP_REF`](ACE_STEP_REF), syncs its environment, and runs [`kernel/gen.py`](kernel/gen.py). `gen.py` loads the model once and generates every song in the job; one failing song never stops the batch. On a T4 (no native bfloat16) ACE-Step would pick float16, which gives NaN noise, so `gen.py` forces bfloat16, and if a take still comes out as NaN it retries once in float32 without the language model. The weights download from Hugging Face without a login. No token or credential is ever put into the kernel. Change the commit with `--ace-ref`, or edit `ACE_STEP_REF` after testing a newer one.

## Licences and limits

- ACE-Step 1.5 code and weights: MIT. The model card allows commercial use of the output but gives **no guarantee against similarity to existing works**. Say that the music is AI-generated whenever you publish it. See [`LICENSES.md`](LICENSES.md).
- Reference audio (timbre cloning) is deliberately not supported by this kit: no real person's voice.
- Narration and sound effects are not in this kit yet. Check any voice model's licence before commercial use (see `LICENSES.md`).
- Kaggle's terms apply to your account and your use of its free GPU. Read them.

## Troubleshooting

- `kaggle` crashes with `No module named 'six'`: run `bash setup.sh` again. It installs `six` next to the CLI.
- `doctor.sh` says the quota call failed: the token is missing or wrong. Redo the Kaggle setup above.
- A run finishes with no GPU or no internet: verify the phone number in your Kaggle settings.
- A take is silent or noise: look at `runs/RUN_ID/output/out/results.json` and the kernel log (`kaggle kernels logs YOUR_USERNAME/cap-make-song`).
