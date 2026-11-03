# Cap kit

The tools behind the Computerized Audio Producer: make songs with [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) on **your own free Kaggle GPU**, read a script aloud with **Phonon 31M on your CPU**, synthesise simple **sound effects with ffmpeg**, then check every take before anyone hears it. Free by default: the only resource used is your weekly Kaggle GPU quota, and only for songs. Narration and sound effects need no account and no GPU. Nothing here publishes, sends, buys or contacts anyone.

Cap fetches this folder for you when you say `Set up your workspace`. You can also use it by hand.

## What you need

- A computer with a shell and internet: Linux, macOS, or Windows with WSL. A chat-only bot with no computer cannot run this kit.
- `python3` 3.11 or newer, `ffmpeg` (with `ffprobe`), `curl` and `git`.
- For songs only: a free [Kaggle](https://www.kaggle.com) account. **You create it and sign in yourself.** Cap never sees your password. Narration and sound effects work without it.
- For narration: about 60 MB of disk for the voice model, which downloads from Hugging Face on first use (no login), and the `ptts` command (`setup.sh` installs it into `.venv`; `uv` is the fallback).

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
bash setup.sh      # checks the tools, creates .venv with the Kaggle CLI, faster-whisper and ptts (--no-whisper, --no-tts skip those)
bash doctor.sh     # checks the login, GPU quota, kernel settings and network. Costs no GPU time.
```

`doctor.sh` prints PASS, WARN or FAIL lines. It also makes two test sound effects and dry-runs `narrate.py` (nothing is downloaded). It checks that the kernel will have the GPU on, internet on, a T4 and private (without those Kaggle silently runs on CPU with no network), that the pinned ACE-Step commit still exists, and how many GPU hours are left. Phone verification cannot be checked from the command line; if a push fails or runs without a GPU, check it in your Kaggle settings.

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

## Narrate a script

`narrate.py` reads a script file and renders it with Phonon 31M (`gradium/phonon-31m-en`, English only, Apache-2.0) on the CPU. The first run downloads the voice model (about 60 MB).

1. Write the script, one line per segment:

   ```
   # comments start with a hash
   Welcome to the show.
   [Easton] This line is read by Easton.
   [pause 1.5]
   And this one is read by the default voice again.
   ```

   `[Voice]` at the start of a line picks a stock voice for that line (Easton, Harper, Juniper, Imogen and more: `.venv/bin/python narrate.py --list-voices`). `[pause 1.5]` adds 1.5 seconds of silence. Write numbers as words if you want the word check to be exact.
2. Render two takes with two seeds:

   ```
   .venv/bin/python narrate.py --script script.txt --out out/narration-1 --voice Harper --seed 1 --normalize -14
   .venv/bin/python narrate.py --script script.txt --out out/narration-2 --voice Harper --seed 2 --normalize -14
   ```

   Each take writes `out/narration-N.wav` (or `.mp3` with `--format mp3`) and `out/narration-N.json`: the start, end, voice, seed and text of every segment, the model, its licence and `commercial_use`. Options: `--pause` (gap between segments, default 0.5 s), `--lead`, `--tail`, `--temperature`, `--normalize LUFS` (two-pass loudness normalisation, true peak -1.5 dBTP, which leaves room for MP3 encoding), `--keep-parts` (the per-segment WAV files), `--dry-run`.
3. Check each take: `.venv/bin/python check_song.py out/narration-1.wav --kind narration --manifest out/narration-1.json --target -14`.

What you control: the voice per line, the pauses, the seed and the temperature. **There is no emotion or style control per line.** Phonon has conditioners such as `duration_delta` that this kit does not expose.

A rendering takes a few seconds on a laptop CPU. Measured on one Linux box with 8 threads: three short lines (about 8 seconds of speech) rendered in about 2.5 seconds, including the model load for each line.

**Licence guard.** Phonon 31M is Apache-2.0 and is the default. The Phonon 40M models are CC BY-NC (non-commercial, and gated on Hugging Face): `narrate.py` refuses them unless you pass `--non-commercial`, and then the manifest says `commercial_use: false` and you must not publish or sell the audio. Any other model needs `--licence TEXT`, the licence you read on its model page; a non-commercial licence also needs `--non-commercial`. The licence is written into the manifest.

**No voice cloning.** Voices are stock names from the catalog. A path, a voice file or reference audio is refused. Do not use this kit to imitate a real person.

**Another engine** is your choice, not tested here: `--engine command --engine-cmd 'mytts --text {text} --voice {voice} --out {out}' --licence "Apache-2.0"`. The command must write a WAV file to `{out}`. Read the model's licence first, and do not use a voice-cloning model for a real person's voice.

## Sound effects

`make_sfx.py` synthesises effects from maths and noise with ffmpeg. There are no external assets, no network and no GPU.

```
.venv/bin/python make_sfx.py --list
.venv/bin/python make_sfx.py whoosh riser boom --out-dir out/sfx
.venv/bin/python make_sfx.py riser --duration 4 --pitch 150 --out-dir out/sfx --format mp3
.venv/bin/python check_song.py out/sfx/*.wav --kind sfx
```

| Preset | Sound | Default length | Default pitch |
| --- | --- | --- | --- |
| `whoosh` | pink noise swept up through a band-pass, bell-shaped volume (`--down` for a fall) | 0.8 s | 300 Hz |
| `riser` | rising tone plus building noise, cut off at the top | 3 s | 200 Hz |
| `boom` | impact: a sine that drops in pitch plus a low thump | 1.5 s | 140 Hz |
| `click` | very short noise tick | 0.04 s | 3000 Hz |
| `glitch` | gated, bit-crushed stutter; `--seed` changes the pattern | 0.6 s | 400 Hz |
| `sweep` | white noise through a swept band-pass (`--down` for a fall) | 2 s | 200 Hz |
| `beep` | one sine beep with a short fade | 0.2 s | 880 Hz |

`--duration` (0.01 to 60 s) and `--pitch` (20 to 8000 Hz, the base frequency) change a preset; the same preset, settings and seed always give the same file. Every file is peak-normalised to `--peak` (default -3 dBFS), so it cannot clip. `sfx-manifest.json` lists preset, duration, pitch, seed, peak and licence of each file. The sounds are simple building blocks, not studio sound design: listen before you use them.

**Sounds you provide.** `make_sfx.py --import-dir FOLDER --licence "CC0" --out-dir out/sfx` converts every audio file in the folder to the output format with the same peak normalisation, and records the licence you give in the manifest. Only CC0 or public-domain files: the script refuses a licence that says non-commercial or personal use. It does not download anything. Keep a `SOURCES.md` in the folder with one line per file (name, URL, author, licence) and read the licence on the page each file came from.

## What it costs

Measured on a Kaggle T4: setup about 4 minutes, model load about 2.5 minutes, then roughly one minute per song of one minute. A two-take test of 30 seconds each takes about 8 to 12 minutes, which is about **0.15 to 0.2 GPU hours** of your weekly quota. Read the weekly total from `make_song.py --quota`; do not assume it. A run that hits `--timeout` is killed, and the quota is wall-clock, so a long timeout is a long possible bill in hours, not in money.

## What `check_song.py` checks

`--kind song` (default), `--kind narration` or `--kind sfx`. Per file, with ffmpeg:

| Check | How | Result |
| --- | --- | --- |
| Duration | `ffprobe` against the requested length | FAIL if more than 5% off |
| Clipping | `volumedetect`, max volume at 0.0 dB | FAIL |
| Silence | mean volume below -50 dB, or over 3 s of silence inside the take | FAIL (silent takes are the known failure on a T4) |
| Loudness | `loudnorm` integrated LUFS and true peak against -14 LUFS and -1 dBTP | WARN, fixable by a normalise pass |
| Lyrics (optional, `--lyrics`) | `faster-whisper` on the CPU, words heard back against the lyrics, per section | PASS 85% or more, WARN 65 to 85%, FAIL below 65% |
| Words (`--kind narration`, with `--manifest` from `narrate.py` or `--lyrics script.txt`) | `faster-whisper` on the CPU, words heard back against the script, plus the count of extra words heard | PASS 95% or more, WARN 85 to 95% (or many extra words), FAIL below 85%. The words not heard are listed. |
| Sound effects (`--kind sfx`) | Duration, clipping and silence as above. The loudness target is skipped because effects are too short to measure | Peak must stay below 0 dB |

Speech-to-text under-hears singing, so the lyrics score is a guide, not a verdict. A whole section missing means the model skipped or replaced it. The script exits non-zero when every take fails, and it prints the preferred take. These are numbers, not listening: say so when you hand takes over. To normalise a take to the target afterwards:

```
ffmpeg -i take.mp3 -af loudnorm=I=-14:TP=-1:LRA=11 -ar 44100 take-normalised.mp3
```

## How the Kaggle kernel works

[`kernel/bootstrap.py`](kernel/bootstrap.py) runs on Kaggle's system Python: it installs `uv`, clones ACE-Step, checks out the pinned commit in [`ACE_STEP_REF`](ACE_STEP_REF), syncs its environment, and runs [`kernel/gen.py`](kernel/gen.py). `gen.py` loads the model once and generates every song in the job; one failing song never stops the batch. On a T4 (no native bfloat16) ACE-Step would pick float16, which gives NaN noise, so `gen.py` forces bfloat16, and if a take still comes out as NaN it retries once in float32 without the language model. The weights download from Hugging Face without a login. No token or credential is ever put into the kernel. Change the commit with `--ace-ref`, or edit `ACE_STEP_REF` after testing a newer one.

## Licences and limits

- ACE-Step 1.5 code and weights: MIT. The model card allows commercial use of the output but gives **no guarantee against similarity to existing works**. Say that the music is AI-generated whenever you publish it. See [`LICENSES.md`](LICENSES.md).
- Reference audio (timbre cloning) is deliberately not supported by this kit: no real person's voice.
- Narration: Phonon 31M is Apache-2.0 and the default; Phonon 40M models are CC BY-NC and refused without `--non-commercial`; no voice cloning. Check any other voice model's licence before commercial use (see `LICENSES.md`). Say that the speech is AI-generated whenever you publish it.
- Sound effects are synthesised by ffmpeg from maths and noise, so there is nothing to credit. Sounds you provide keep their own licence.
- Kaggle's terms apply to your account and your use of its free GPU. Read them.

## Troubleshooting

- `kaggle` crashes with `No module named 'six'`: run `bash setup.sh` again. It installs `six` next to the CLI.
- `doctor.sh` says the quota call failed: the token is missing or wrong. Redo the Kaggle setup above.
- A run finishes with no GPU or no internet: verify the phone number in your Kaggle settings.
- `narrate.py` says ptts is not found: run `bash setup.sh`, or install [uv](https://docs.astral.sh/uv/) so `uvx ptts` works. The first narration needs the internet once for the voice model.
- A take is silent or noise: look at `runs/RUN_ID/output/out/results.json` and the kernel log (`kaggle kernels logs YOUR_USERNAME/cap-make-song`).
