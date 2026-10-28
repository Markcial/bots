# MVS kit: free local harness for motion video and images

This file is for the bot (Methodical Visual Synthesizer), not for people. It tells you what is in the kit, what to run, and where output goes. The kit is generic. It holds no personal data, accounts, or secrets. Everything runs on this computer with free tools. Nothing here publishes, sends, buys, or spends credits.

Use the kit only after the diagnosis is approved (see the `diagnose-brief` skill). Setting it up is fine before that.

## Quick reference

Run all commands from the kit folder (the workspace path saved in your memory note `workspace-path`).

| Goal | Command | Output |
| --- | --- | --- |
| Install and check the toolchain | `bash setup.sh` (add `--install-system` for Node and ffmpeg, `--with-tts` for the free voice) | printed summary |
| Prove it works | `bash doctor.sh` | `out/doctor-clip.mp4`, `out/doctor-avatar-*.png`, `out/doctor-report.txt` |
| Layout check of a video, no render | `node scripts/make.mjs configs/<name>.json --stills` | `work/<slug>/stills/scene-NN.png` |
| Make a 16:9 video | `node scripts/make.mjs configs/<name>.json` | `out/<slug>.mp4` |
| Make a video with silent narration | add `--engine=none` | captions still show |
| Check the brand book and configs | `node scripts/brand-check.mjs` (or `... brand/<slug>/brand.json configs/<name>.json`) | contrast of palette pairs, font licences, change log, configs that drift from the book |
| Measure a finished video | `node scripts/qa.mjs out/<slug>.mp4` | size, fps, duration, LUFS, true peak (exit 1 on a hard miss) |
| Make an avatar set | `node scripts/still.mjs --out=out/<name> --motif=ring --glow="#FF5FA8" ...` | `out/<name>-{1024,512,256,128,48,32}.png`, `-check32.png`, `-sheet.png` |
| Narration test | `node scripts/narrate.mjs "A sentence." --voice=Harper` | `work/narration-test.wav` |
| Music bed | `node scripts/music.mjs --out=work/bed.wav --duration=40 --mood=soft` | WAV |

## Folder layout

```
kit/
  setup.sh  doctor.sh  README.md  LICENSES.md
  package.json  tsconfig.json  remotion.config.ts
  configs/    _template.json (copy it per project)   doctor.json (used by doctor.sh)
  brand/      _template/ (brand.json + BRAND.md: copy to brand/<slug>/ for each brand; the owner's brand files stay in the workspace)
  scripts/    make.mjs (one command, config to MP4)   narrate.mjs   music.mjs   mix.mjs   render.mjs   still.mjs   brand-check.mjs   qa.mjs   lib.mjs
  src/        Remotion project: Video (16:9 scenes, captions, closing card), Avatar (1024 px square still), Background, Captions, theme
  assets/     put the owner's logos and images here (never commit them back to the public repo)
  out/        finished files (git-ignored)      work/<slug>/  intermediates: props.json, timeline.json, voice clips, mix.wav, silent.mp4
```

Keep each project's files in its own config and slug. Save new files under new names. Never overwrite the owner's existing files.

## The brand book (one folder per brand)

Copy `brand/_template/` to `brand/<brand-slug>/` and fill `brand.json` and `BRAND.md` (skill `brand-book`). Keep the status `draft` until the owner says OK, then `approved <date>`. Change it only after the owner's yes, bump `version`, and add a dated line to `changelog`.

- In a video config, add `"brand": "brand/<brand-slug>/brand.json"`. `make.mjs` then takes the palette, the heading and body fonts, and the avatar colours from the book, and the book wins over any value in the config. It warns if the book is not approved.
- `node scripts/still.mjs --brand=brand/<brand-slug>/brand.json` draws the avatar in the book's colours.
- `node scripts/brand-check.mjs` checks every pair in `pairs` (contrast of the palette tokens), that each font has an open licence, that the change log is filled in, that configs point at the book, that text and accent colours are readable on the background, and that the Remotion source takes colours from the theme. Run it before every handoff. Never change the book to make a check pass. Report the deviation.

## The video config (one JSON per project)

Copy `configs/_template.json` to `configs/<project>.json` and edit it.

- `project`, `slug`: name shown in the eyebrow, and the output name.
- `brand` (optional): path to the brand book, for example `brand/my-brand/brand.json`. Palette, fonts, avatar colours, and spoken respellings come from it.
- `palette`: `primary`, `accent`, `background`, `ink` as `#hex` (optional: `surface`, `onPrimary`, `primaryText`). Take the values from the approved diagnosis. Do not invent a brand's colours.
- `fonts`: `heading`, `body` (a family installed on this computer, else the stack falls back to Inter, then a generic sans-serif), `headingWeight`. Record the font and its licence in `tool-notes`.
- `avatar`: default avatar props for scenes that use `"visual": {"type": "avatar"}` (same fields as `still.mjs`).
- `voice`: `engine` (`auto`, `phonon`, or `none`), `name` (a Phonon voice, default `Harper`), `seed` (same seed gives the same take).
- `music`: `mood` (`soft`, `warm`, `night`, `upbeat`), `gainDb` (default -9; use -12 for quieter), `seed`. Or `file` plus `credit` (see Music).
- `pronounce`: spoken-only respelling, for example `{"Brand": "Bran d"}`. Captions keep the real spelling.
- `subtitles`: `true` (default) or `false`.
- `scenes`: each has `headline` (45 characters or fewer), `narration` (one or two short sentences), and optionally `eyebrow`, `accentWords` (words of the headline painted in the primary colour, matching exactly), `support`, and `visual`: `{"type":"none"}`, `{"type":"avatar","props":{...}}`, or `{"type":"image","src":"assets/file.png"}`.
- `closing`: the closing card. `headline`, `accentWords`, `support`, `narration`, `cta`.

Scene length follows the narration length. Captions are timed to the narration and split at about 44 characters.

## Typical flow for a motion piece

1. Write the storyboard and get it approved (skill `build-motion`).
2. Write `configs/<project>.json` from the storyboard.
3. `node scripts/make.mjs configs/<project>.json --stills`. Look at each PNG at full size with the image reader. Fix overlaps, weak contrast, and text that is too small.
4. `node scripts/make.mjs configs/<project>.json`. The last line prints `DONE <path>`. Then run `node scripts/qa.mjs out/<slug>.mp4`: it measures the final file (size, 30 fps, audio, loudness, true peak). The target is about -14 LUFS and -1.5 dBTP or lower. It exits with 1 if the loudness is more than 1.5 LU off or the peak is above -1.0 dBTP.
5. Run `node scripts/brand-check.mjs`. Report the file path, duration, loudness, narration engine, the brand check result, and what is weak.

Measured on an 8-core Linux box: a 2 second doctor clip takes about 5 s end to end, and a 15 second, 3 scene video with narration takes about 17 s (Remotion render about 12 s). A 60 second video takes about a minute. Use `--concurrency=1` or `2` if memory is tight. Do not run two heavy renders at once, and do not run a voice job while a render is going. Check free memory first (`free -m`).

## Narration (free)

- Default engine: Phonon 31m through `uvx ptts` (Apache-2.0, runs on the CPU, no account, about 60 MB of model downloaded once into `.cache/hf`). Set up with `bash setup.sh --with-tts`.
- One clip per sentence, cached by text, voice and seed in `work/<slug>/tts/`. Change a line and only that clip is re-made. `--fresh` ignores the cache.
- List voices: `uvx ptts --list-voices`. Do not select a 40m model (non-commercial weights).
- Silent fallback: if `uvx` is missing or Phonon fails, the step continues with silent clips timed at 2.6 words per second and a warning. The captions still show. Say so in your report. If the owner wants a spoken track and the free voice is not available, ask them for a recording or for a decision. Do not sign up for a paid voice service on your own.
- A word is mispronounced: add it to `pronounce`, re-run, and check by ear or with a speech-to-text pass if you have one. Voice text only: captions keep the real spelling. A word at the start of a clip that loses its first syllable gets a leading ellipsis in the respelling (`"Parse": "... Parse"`) or goes in the previous line. Two fused words get a comma. See `../LESSONS.md`.
- Loudness is off on a sparse voice track: the mix uses one loudness pass, so run `qa.mjs`, and if it is more than 1.5 LU off, normalise the mix again (`ffmpeg -i work/<slug>/mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=11 ...`) and mux it again.

## Music (free and copyright-safe only)

1. **Default, preferred: the built-in bed.** `scripts/music.mjs` synthesizes a soft chord bed from code. No samples, no third-party material, no attribution. The licence is in `LICENSES.md`. This is what `make.mjs` uses unless the config names a file.
2. **Public domain / CC0 tracks**, only if the owner wants a different sound. Sources that publish CC0 or public-domain music: the CC0 filter on [Free Music Archive](https://freemusicarchive.org/), CC0 tracks on [OpenGameArt](https://opengameart.org/), and public-domain items on the [Internet Archive](https://archive.org/). Open the item page and read the licence before you download. Do not trust a search snippet.
3. **Anything that needs attribution** (CC BY, for example) or comes with a custom licence (for example the [Pixabay Content License](https://pixabay.com/service/license-summary/), which has limits on redistribution) needs the owner's yes first. State the terms.
4. Never use commercial music, music from a video or a streaming service, or AI music that needs credits or an account.
5. For a file, put it in `assets/` and set `music.file` and `music.credit` (`title`, `author`, `url`, `license`). `make.mjs` refuses to run without the credit, and writes it to `work/<slug>/music-credits.json`. Add the credit to the handoff note.
6. Ducking is automatic. The bed drops under the voice (sidechain compressor, about 0.6 s release) and comes back. With silent narration the bed plays alone. The final mix is normalised to about -14 LUFS and -1.5 dBTP.

## Images (free default: code-drawn)

- `scripts/still.mjs` draws an avatar in SVG through a Remotion still: a dark rounded plate and one glass object with a glow. Motifs: `triangle-arc`, `ring`, `lattice`, `beam`, `monogram`. Add a motif in `src/Avatar.tsx` (`Motif`) when the direction needs a new shape.
- It renders the master at 1024 px and renders 512, 256, 128, 48, and 32 px natively (not by resizing), with fewer fine details at 64 px and below. Look at `-check32.png` (the 32 px render enlarged 8 times) and `-sheet.png` (real-size row) before you hand over anything.
- Need another still (a banner, a card)? Add a `<Still>` to `src/Root.tsx` and render it with `npx remotion still <id> out/<name>.png`.
- **Paid image generation is optional and never the default.** Say what it costs and which account it needs, and wait for the owner's yes to that exact step. See the `approval-gate` skill.

## When something fails

- Run `bash doctor.sh` and read the first FAIL line.
- `Remotion could not get a headless browser` or a missing shared library: `setup.sh` prints the `apt-get install` line for Linux. Do not run `sudo` without the owner's yes.
- A render runs out of memory: `--concurrency=1`.
- A font looks wrong: the family name must match what is installed (`fc-list : family | grep -i <name>`), else Inter is used.
- Narration is silent when it should not be: `uvx --version`, then `bash setup.sh --with-tts`.
- If a fix needs a paid account, an API key, a card, or a sign-in only the owner can do, stop and ask.
