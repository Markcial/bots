---
name: make-narration-sfx
description: Use when the user wants narration read from a script, or simple sound effects (whoosh, riser, boom, click, glitch, sweep, beep), made for free on the CPU with the kit, then checked with ffmpeg and speech-to-text before delivery.
---

# Narration and sound effects for free (kit, CPU only)

Narration uses Phonon 31M (English only, Apache-2.0) through the kit's `narrate.py`. Sound effects are synthesised by ffmpeg through `make_sfx.py`. Neither needs a GPU, a Kaggle account or any paid service.

## Before you start

- You need the kit workspace. Read the memory note `workspace-path`. If it does not exist, run the skill `setup-workspace` first. Run every command from that folder, with `.venv/bin/python`.
- Run `bash doctor.sh`. The "sound effects and narration scripts" lines must PASS. If `ptts` is missing, run `bash setup.sh` again.
- The first narration downloads the Phonon 31M voice model (about 60 MB) from Hugging Face, no login. Tell the owner before the first run.
- Licence rule: `narrate.py` refuses Phonon 40M models (CC BY-NC) unless `--non-commercial` is passed, and refuses any other model until you pass `--licence` with the licence you read on the model page. Never pass `--non-commercial` for audio the owner will publish or sell. See `kit/LICENSES.md`.
- No voice cloning: voices are stock catalog names only (Easton, Harper, Juniper, Imogen and more: `.venv/bin/python narrate.py --list-voices`). No reference audio, no voice files. Say so if asked.
- What you can control: the voice per line, pauses, the sampling seed, and the temperature. There is no emotion or style control per line. Do not promise one.

## Narration

1. Get the script from the owner or the writer bot. Do not edit it. Write numbers as words if the check should be exact, and ask the owner before you change any wording.
2. Save it as a text file: one line per segment, `[Voice] text` for a line in another voice, `[pause 1.5]` for extra silence, `#` for comments. Show the owner the voice and the pacing plan (line by line) and wait for an explicit OK.
3. Two takes with two seeds:

   ```
   .venv/bin/python narrate.py --script script.txt --out out/narration-1 --voice Harper --seed 1 --normalize -14
   .venv/bin/python narrate.py --script script.txt --out out/narration-2 --voice Harper --seed 2 --normalize -14
   ```

   Use `--normalize -16` for podcasts, `--pause` to change the gap between segments, and `--format mp3` for MP3. Each take writes the audio and a JSON manifest with the start, end and text of every segment (useful for captions).
4. Check each take: `.venv/bin/python check_song.py out/narration-1.wav --kind narration --manifest out/narration-1.json --target -14`. It checks duration, clipping, silence, loudness and the words heard back against the script (95% or more passes, 85 to 95% warns, below 85% fails). Speech-to-text can miss names and numbers, so read the "not heard" words before you judge.
5. Hand over the better take with the numbers, the voice, seed and date (all in the manifest), and say you have not listened to it. Say that the speech is AI-generated whenever it is published.

## Sound effects

1. Ask what the effect is for and how long it should be. List the presets with `.venv/bin/python make_sfx.py --list`.
2. Make it: `.venv/bin/python make_sfx.py whoosh riser boom --out-dir out/sfx` (add `--duration SECONDS`, `--pitch HZ`, `--seed N`, `--down`, `--format mp3`). Every file is peak-normalised to -3 dBFS and listed in `out/sfx/sfx-manifest.json`.
3. Check: `.venv/bin/python check_song.py out/sfx/*.wav --kind sfx`. One take is enough for a short effect.
4. Sounds the owner provides (CC0 or public domain only): `make_sfx.py --import-dir FOLDER --licence "CC0" --out-dir out/sfx`. Ask for the page each file came from, read its licence, and keep a `SOURCES.md` in that folder. Never download sound libraries yourself, and never import CC BY-NC or "free for personal use" files.

## Do not

- Use a non-commercial model or sound for anything the owner will publish or sell.
- Clone or imitate a real person's voice.
- Hand over a take that failed a check, or claim an emotion control the kit does not have.
- Spend money, publish or send anything without an explicit yes.
