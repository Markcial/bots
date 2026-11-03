# Computerized Audio Producer

Stage: **prepare**. The template text, the avatar set and the song kit are made. The motion presentation video is still pending. The template is not published yet.

Cap is the audio desk for a team of bots. It turns finished scripts into narration with an open text-to-speech model, makes songs, instrumentals and music beds with ACE-Step on a free Kaggle GPU, makes simple sound effects, then mixes and normalises the result. It is free-only by default and checks every take before handing it over, with two takes per deliverable. It does not write scripts, make podcasts, clone real people's voices or handle live audio, and it never sends, publishes or buys anything without an explicit yes.

## Use cases

- Turn a script into narration. How much emotion and pacing control you get depends on the open voice model you pick.
- Make a song, an instrumental or a music bed from a short brief.
- Mix voice and music, duck the music under speech, and normalise loudness for social and YouTube.
- Hand back: writing or editing the script (the writer bot does that).
- Refuse: cloning a real person's voice, podcasts, live audio.

## Tools it uses

All free by default. What is built in and what is your choice:

| Job | Tool | Status |
| --- | --- | --- |
| Songs, instrumentals, beds | [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5) (MIT) on your own free Kaggle GPU | Built in: the [`kit/`](kit/) has the scripts, a pinned version and the T4 fix |
| Checks | `ffmpeg` (duration, loudness, clipping, silence) and [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for the lyrics | Built in: `kit/check_song.py` |
| Narration | An open text-to-speech model that you choose, for example Phonon 31M (English, Apache-2.0), Qwen3-TTS (Apache-2.0) or Chatterbox (MIT) | Your choice. Cap reads the model's licence page before any commercial use ([`kit/LICENSES.md`](kit/LICENSES.md)). Not in the kit yet. |
| Sound effects | Cap synthesises simple ones with ffmpeg (tones, noise, filters), or uses CC0 or public-domain sounds you provide | Your choice. Not in the kit yet. |

If a tool is missing, Cap says which and offers a free way to add it.

## Install

You need a **computer with a shell and internet access** (Linux, macOS, or Windows with WSL): Cap runs `ffmpeg`, Python and the Kaggle command line there. A bot with no computer can plan and write lyrics but cannot make audio.

1. **Create the bot.** Not published yet, so until launch: in Grok Bot create a bot from [`profile.md`](profile.md), add each folder under [`skills/`](skills/) as a skill (with its frontmatter), paste [`memories.md`](memories.md) as seed knowledge, and create the routine in [`routines.md`](routines.md) with its cron in your timezone. After launch you open the template link from `catalog.json` (`xai_template_url`). See "How a template works" in the [root README](../README.md).
2. **Say `Set up your workspace.`** Cap tells you what it will install, asks for your yes, fetches only its [`kit/`](kit/) from this repo, runs `setup.sh` and `doctor.sh`, and shows you the result.
3. **Kaggle (songs only), done by you.** A free account with a verified phone number, an API token from https://www.kaggle.com/settings/api, saved where the Kaggle command line reads it (`kaggle auth login`, or `~/.kaggle/access_token`, or `~/.kaggle/kaggle.json` with `chmod 600`, or the `KAGGLE_API_TOKEN` or `KAGGLE_USERNAME` and `KAGGLE_KEY` variables). Cap never asks for the token in chat and never stores it. Details: [`kit/README.md`](kit/README.md). Without Kaggle, Cap does narration and short sounds only and says so.

## Media

Identity and motion presentation live in [`media/`](media/). The brief is [`media/BRIEF.md`](media/BRIEF.md).

| Asset | Path |
| --- | --- |
| Avatar (1024 / 512 / 256 / 128 / 48 / 32) | [`media/avatar-1024.png`](media/avatar-1024.png) (and siblings) |
| Motion video 16:9 | pending |
| Motion video 1:1 | pending |

After merge to `main`, raw URLs look like `https://raw.githubusercontent.com/Markcial/bots/main/computerized-audio-producer/media/avatar-1024.png`.

## For contributors: when you copy this

- Every `SKILL.md` has YAML frontmatter with `name` (the folder slug) and `description`.
- The routine has a 5-field cron, the user's timezone, and a delivery line.
- An installed bot cannot see this repo on disk. Skills use full URLs and real tool names, with a fallback when a fetch or plugin is missing.

## Stage

`prepare`. The text is stable and the avatar is made. The motion presentation video is still to be made and reviewed before `ready`. No template link yet (`xai_template_url` stays null until `launch`).
