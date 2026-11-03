---
name: setup-workspace
description: First run: fetch this bot's own kit (song maker, take checker, doctor) from the public repo onto your computer, run setup and the self-check, tell the owner what is left to do for Kaggle, and save the workspace path as a memory note.
---

# Set up the workspace

A template only carries text. The tools Cap needs come as a kit: the folder `computerized-audio-producer/kit/` in the public repo `github.com/Markcial/bots` (MIT). Do this once, before the first song.

Cap needs a computer with a shell and internet access. If you have none, say so and stop: you can still plan, draft lyrics and write briefs, but you cannot make or check audio.

Skip to step 6 if the memory note `workspace-path` exists and `<path>/doctor.sh` is there. Then just run `bash doctor.sh` and report the result.

## Steps

1. Pick the folder: `$HOME/workspaces/computerized-audio-producer`, unless the owner names another. If it already exists and is not empty, do not copy over it. Ask the owner whether to use a new folder name.
2. Tell the owner, in a few lines, what you are about to do, and ask for a yes before you run anything. It installs the Kaggle command line and faster-whisper into a `.venv` inside that folder, nothing system-wide, and costs nothing. It needs `python3` 3.11 or newer, `ffmpeg`, `curl` and `git`. If one is missing, say so and give the fix line `setup.sh` prints. Do not use `sudo` or install system packages unless the owner says yes.
3. Fetch only the kit folder from the public repo (no other source):

   ```
   WS="$HOME/workspaces/computerized-audio-producer"
   SRC="$(mktemp -d)"
   git clone --depth 1 --filter=blob:none --sparse https://github.com/Markcial/bots.git "$SRC"
   git -C "$SRC" sparse-checkout set computerized-audio-producer/kit
   KIT_COMMIT="$(git -C "$SRC" rev-parse --short HEAD)"
   mkdir -p "$WS" && cp -R "$SRC/computerized-audio-producer/kit/." "$WS/"
   ```

   If `git` is missing or the clone fails, use the tarball (main branch, kit folder only):

   ```
   mkdir -p "$WS" && curl -fsSL https://codeload.github.com/Markcial/bots/tar.gz/refs/heads/main \
     | tar -xz --strip-components=3 -C "$WS" --wildcards 'bots-main/computerized-audio-producer/kit/*'
   ```

   If both fail (offline, 404 because the kit is not published yet, or a blocked network), say exactly what failed and ask the owner for another source. Do not rebuild the kit from memory.
4. Run `cd "$WS" && bash setup.sh`. Read the printed summary. If something is MISSING, tell the owner what and the fix line it printed.
5. Run `bash doctor.sh`. A FAIL on the Kaggle login or the quota is expected on a first run: give the owner the numbered Kaggle steps from `kit/README.md` ("Kaggle setup") as a short list and ask them to do them in their own browser and terminal. They create the account, verify the phone, generate the token and save it where the Kaggle command line reads it. Never ask them to paste the token into the chat, and never read or print the token file. When they say it is done, run `bash doctor.sh` again.
6. Show the owner the doctor output (pass or fail, any WARN).
7. Save a memory note titled `workspace-path` with: the folder path, the kit commit (`KIT_COMMIT`), the date, and the doctor result. Do not put any credential in it. Also create the memory note `cap-jobs` if it does not exist, with the header line `run id | kernel | status | date | output folder`. Read `workspace-path` at the start of every job and `cd` into the folder.
8. Read `README.md` in the workspace. It is the command reference.

## Do not

- Fetch anything but the one kit folder from `github.com/Markcial/bots`, or run a script you have not read from anywhere else.
- Ask for, read, print or store the owner's Kaggle token or password.
- Sign up for, or pay for, anything.
- Overwrite an existing workspace. Updating the kit means fetching it into a new folder and comparing.
