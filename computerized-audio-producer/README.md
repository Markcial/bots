# Computerized Audio Producer

Stage: **prepare**. The template text and the avatar set are made. The motion presentation video is still pending. The template is not published yet.

Cap is the audio desk for a team of bots. It turns finished scripts into narration with emotion, and makes songs, instrumentals, music beds and sound effects, then mixes and normalises the result. It is free-only by default and checks every take before handing it over, with two takes per deliverable. It does not write scripts, make podcasts, clone real people's voices or handle live audio, and it never sends, publishes or buys anything without an explicit yes.

## Use cases

- Turn a script into narration with a chosen emotion per line.
- Make a song, an instrumental or a music bed from a short brief.
- Mix voice and music, duck the music under speech, and normalise loudness for social and YouTube.
- Hand back: writing or editing the script (the writer bot does that).
- Refuse: cloning a real person's voice, podcasts, live audio.

## Tools it uses

All free by default: an open text-to-speech model with emotion tags, ACE-Step (https://github.com/ace-step/ACE-Step-1.5) on a free Kaggle GPU, ffmpeg for loudness and clipping checks, and a speech-to-text model such as Whisper to compare narration with the script. If one is missing, the bot says which and offers a free way to add it. The template carries only text and has no kit yet, so the bot sets these tools up with the owner's yes.

## Media

Identity and motion presentation live in [`media/`](media/). The brief is [`media/BRIEF.md`](media/BRIEF.md).

| Asset | Path |
| --- | --- |
| Avatar (1024 / 512 / 256 / 128 / 48 / 32) | [`media/avatar-1024.png`](media/avatar-1024.png) (and siblings) |
| Motion video 16:9 | pending |
| Motion video 1:1 | pending |

After merge to `main`, raw URLs look like `https://raw.githubusercontent.com/Markcial/bots/main/computerized-audio-producer/media/avatar-1024.png`.

## When you copy this

- Every `SKILL.md` has YAML frontmatter with `name` (the folder slug) and `description`.
- The routine has a 5-field cron, the user's timezone, and a delivery line.
- An installed bot cannot see this repo on disk. Skills use full URLs and real tool names, with a fallback when a fetch or plugin is missing.

## Stage

`prepare`. The text is stable and the avatar is made. The motion presentation video is still to be made and reviewed before `ready`. No template link yet (`xai_template_url` stays null until `launch`).
