---
name: setup-workspace
description: First run: fetch this bot's own kit (experiment scaffold, report template, link checker) from the public repo onto your computer, run setup and the self-check, show the owner the test output, and save the workspace path as a memory note.
---

# Set up the workspace

A template only carries text. The small tools you need for experiments and reports come as a kit: the folder `superconnected-research-entity/kit/` in the public repo `github.com/Markcial/bots` (MIT). Do this once, before the first experiment or report.

Skip to step 6 if the memory note `workspace-path` exists and `<path>/doctor.sh` is there. Then just run `bash doctor.sh` and report the result.

## Steps

1. Pick the folder: `$HOME/workspaces/superconnected-research-entity`, unless the owner names another. If it already exists and is not empty, do not copy over it. Ask the owner whether to use a new folder name.
2. Tell the owner, in a few lines, what you are about to do, and ask for a yes before you run anything. All of it is free and needs no account. The kit needs only `curl` and `git`, which most computers have. If one is missing, say so and ask before installing it with the system package manager (that needs `sudo` or Homebrew). `python3`, `node`, and `jq` are optional and are installed only if an experiment needs them, with the owner's yes.
3. Fetch only the kit folder from the public repo (no other source):

   ```
   WS="$HOME/workspaces/superconnected-research-entity"
   SRC="$(mktemp -d)"
   git clone --depth 1 --filter=blob:none --sparse https://github.com/Markcial/bots.git "$SRC"
   git -C "$SRC" sparse-checkout set superconnected-research-entity/kit
   KIT_COMMIT="$(git -C "$SRC" rev-parse --short HEAD)"
   mkdir -p "$WS" && cp -R "$SRC/superconnected-research-entity/kit/." "$WS/"
   ```

   If `git` is missing or the clone fails, use the tarball instead (main branch, then copy the kit folder only):

   ```
   mkdir -p "$WS" && curl -fsSL https://codeload.github.com/Markcial/bots/tar.gz/refs/heads/main \
     | tar -xz --strip-components=3 -C "$WS" --wildcards 'bots-main/superconnected-research-entity/kit/*'
   ```

   If both fail (offline, 404 because the kit is not published yet, or a blocked network), say exactly what failed and ask the owner for another source. Do not rebuild the kit from memory.
4. Run `cd "$WS" && bash setup.sh`. Add `--install-system` only if the owner said yes to a system install. Read the printed summary. If something is MISSING, tell the owner what and the fix line it printed. Do not run `sudo` for anything the owner did not approve. Stop and ask if a step needs a paid account, an API key, a card, or a sign-in only the owner can do.
5. Run `bash doctor.sh`. If it fails, read the first FAIL line, fix what you may fix without a paid account or `sudo`, and run it again. A `WARN` about the internet means the link checker could not be verified. Say so.
6. Show the owner the doctor output (pass or fail, the timings, any WARN).
7. Save a memory note titled `workspace-path` with: the folder path, the kit commit (`KIT_COMMIT`), the date, and the doctor result. Read this note at the start of every experiment or report and `cd` into the folder. If you have since moved the folder, update the note.
8. Read `README.md` in the workspace. It is the command reference for experiments, reports, and the link check.

## Do not

- Fetch anything but the one kit folder from `github.com/Markcial/bots`, or run a script you have not read from anywhere else.
- Install, sign up for, or pay for anything that needs an account, a card, or credits.
- Put the owner's questions, reports, or data into the public repo. They stay in the workspace.
- Overwrite an existing workspace. Updating the kit means fetching it into a new folder and comparing.
