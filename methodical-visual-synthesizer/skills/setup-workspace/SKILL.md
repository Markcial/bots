---
name: setup-workspace
description: First run: fetch this bot's own kit (the motion and image harness) from the public repo onto your computer, run setup and the self-check, show the owner the test output, and save the workspace path as a memory note.
---

# Set up the workspace

A template only carries text. The tools you need to make videos and images come as a kit: the folder `methodical-visual-synthesizer/kit/` in the public repo `github.com/Markcial/bots` (MIT). Do this once, before the first build. It is fine to do it before the diagnosis is approved, because it only prepares tools and designs nothing.

Skip to step 6 if the memory note `workspace-path` exists and `<path>/doctor.sh` is there. Then just run `bash doctor.sh` and report the result.

## Steps

1. Pick the folder: `$HOME/workspaces/methodical-visual-synthesizer`, unless the owner names another. If it already exists and is not empty, do not copy over it. Ask the owner whether to use a new folder name.
2. Tell the owner, in a few lines, what you are about to install, and ask for a yes before you run anything. State that all of it is free and needs no account:
   - Node.js 18+ and ffmpeg, if they are missing (a system package: needs `sudo` or Homebrew. Ask first, and say which).
   - npm packages (Remotion and React) and Remotion's headless Chrome, into the kit folder only.
   - Optional: `uv` (user-level) and the free Phonon voice, about 60 MB, for narration. Without it, narration is silent and captions still show.
   - Remotion is free only for individuals, non-profits, and for-profit organisations with up to 3 people. Ask whether the owner is eligible, and save the answer in `tool-notes` with the date. If not, stop and tell the owner that a company licence has a price. See `LICENSES.md` in the kit.
3. Fetch only the kit folder from the public repo (no other source):

   ```
   WS="$HOME/workspaces/methodical-visual-synthesizer"
   SRC="$(mktemp -d)"
   git clone --depth 1 --filter=blob:none --sparse https://github.com/Markcial/bots.git "$SRC"
   git -C "$SRC" sparse-checkout set methodical-visual-synthesizer/kit
   KIT_COMMIT="$(git -C "$SRC" rev-parse --short HEAD)"
   mkdir -p "$WS" && cp -R "$SRC/methodical-visual-synthesizer/kit/." "$WS/"
   ```

   If `git` is missing or the clone fails, use the tarball instead (main branch, then copy the kit folder only):

   ```
   mkdir -p "$WS" && curl -fsSL https://codeload.github.com/Markcial/bots/tar.gz/refs/heads/main \
     | tar -xz --strip-components=3 -C "$WS" --wildcards 'bots-main/methodical-visual-synthesizer/kit/*'
   ```

   If both fail (offline, 404 because the kit is not published yet, or a blocked network), say exactly what failed and ask the owner for another source, such as a zip of the folder. Do not rebuild the kit from memory.
4. Run `cd "$WS" && bash setup.sh`. Add `--install-system` only if the owner said yes to a system install, and `--with-tts` only if they said yes to the free voice. Read the printed summary. If something is MISSING, tell the owner what and the fix line it printed. Do not run `sudo` for anything the owner did not approve. Stop and ask if a step needs a paid account, an API key, a card, or a sign-in only the owner can do.
5. Run `bash doctor.sh`. If it fails, read the first FAIL line, fix what you may fix without a paid account or `sudo`, and run it again. Report what you could not fix.
6. Show the owner the doctor output (pass or fail, the timings) and the test files: view `out/doctor-avatar-sheet.png` and a frame of `out/doctor-clip.mp4`, and give the full paths. Say whether narration is spoken or silent.
7. Save a memory note titled `workspace-path` with: the folder path, the kit commit (`KIT_COMMIT`), the date, the doctor result, the narration engine (phonon or silent), and the Remotion licence answer. Read this note at the start of every build and `cd` into the folder. If you have since moved the folder, update the note.
8. Run `node scripts/brand-check.mjs` once (the doctor already did) and list `brand/`: `_template/` holds the brand book template. Each brand you keep gets its own `brand/<brand-slug>/` folder, which is the owner's private data and stays in the workspace (skill `brand-book`).
9. Read `README.md` in the workspace. It is the command reference for building videos and images.

## Do not

- Fetch anything but the one kit folder from `github.com/Markcial/bots`, or run a script you have not read from anywhere else. The one exception is the `uv` installer that `setup.sh --with-tts` runs, and only after the owner's yes.
- Install, sign up for, or pay for anything that needs an account, a card, or credits. Paid image generation is not part of the kit. It needs its own yes from the owner, with the cost stated first (skill `approval-gate`).
- Copy the owner's logos, images, or briefs into the public repo. They stay in the workspace's `assets/` folder.
- Overwrite an existing workspace. Updating the kit means fetching it into a new folder and comparing.
