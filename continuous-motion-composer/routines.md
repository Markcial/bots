# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine. Keep two routines at least 5 minutes apart. These two run on different days.

Both routines read memory notes. If the notes do not exist yet, the routine says so in one line and stops.

## Open motion review

- **Schedule:** Mondays at 10:00.
- **Cron:** `0 10 * * 1`
- **Timezone:** The user's local timezone. Set it when creating the routine.
- **Delivers:** In this chat, to the user. Reads the memory notes `diagnosis-<project-slug>`, `storyboard-<project-slug>` and `style-frames-<project-slug>`.
- **Prompt:** Read every memory note titled `diagnosis-<project-slug>`, `storyboard-<project-slug>` and `style-frames-<project-slug>`. List the diagnoses that are still `awaiting OK`, the storyboards and style-frame sets that are waiting for a review, and any approved piece that has no render or whose last QA found a problem. For each, name the one decision or file that is needed from the user. Do not start any motion work, and do not change a status. Do not publish, send, purchase or spend credits. Deliver to the user in this chat. If nothing is open or there are no notes, say so in one line and stop.

## Monthly tool and licence check

- **Schedule:** The first day of each month at 10:15.
- **Cron:** `15 10 1 * *`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user. Reads and updates the memory note `tool-notes`.
- **Prompt:** Read the memory note `tool-notes`. Open the licence and price pages for each tool listed there, including Remotion at https://www.remotion.dev/docs/license/faq. Report any change to the licence, the terms of use, or the free-tier limits, with a title and a URL for each change, and flag anything that now costs money. Do not buy, sign up, register, publish, send or spend credits. Update the dates in the note. Deliver to the user in this chat. If nothing changed or the note is missing, say so in one line and stop.
