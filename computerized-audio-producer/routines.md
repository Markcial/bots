# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine.

## Weekly free-GPU budget check

- **Schedule:** Mondays at 09:00.
- **Cron:** `0 9 * * 1`
- **Timezone:** The user's local timezone. Set it when creating the routine.
- **Delivers:** In this chat, to the user.
- **Prompt:** Read the memory note `workspace-path` and run `.venv/bin/python make_song.py --quota` in that folder, and report the GPU hours used and left this week. Then read the memory note `cap-jobs` (one line per run: run id | kernel | status | date | output folder) and run `.venv/bin/python make_song.py --list --refresh` to see live status. List every job whose status is `pushed` or `running`, with its run id and expected folder. Do not start, fetch or push any job, do not spend money, and do not message anyone. If no job is unfinished, say so in one line and stop. If the workspace or the Kaggle login is missing, say that in one line and stop. Deliver to the user in this chat.
- **Where jobs are recorded:** the skill `make-song` adds a line to the memory note `cap-jobs` when it pushes a run and updates it when the run is fetched or fails. The kit also keeps `runs/RUN_ID/state.json` in the workspace.
