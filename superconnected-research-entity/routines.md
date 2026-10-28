# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine. Keep two routines at least 5 minutes apart. These two run at different times of the month.

Both routines read a memory note. If the user has not created it yet, the routine says so in one line and stops.

## Weekly watch

- **Schedule:** Mondays at 09:00.
- **Cron:** `0 9 * * 1`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user. Reads the memory note `watch-list`.
- **Prompt:** Read the memory note `watch-list`. For each topic, search for what changed since the date noted there. Use public sources only. Report only real changes, each with a title and a URL, and say what the change means for the decision the user noted. Mark what you could not verify. Do not buy, sign up, register, send, post, or contact anyone. Update the date in the note after the report. Deliver to the user in this chat. If nothing changed or the note is missing, say so in one line and stop.

## Monthly price and free-tier check

- **Schedule:** The first day of each month at 09:30.
- **Cron:** `30 9 1 * *`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user. Reads and updates the memory note `tool-shortlist`.
- **Prompt:** Read the memory note `tool-shortlist`. Open each tool's price page and docs again. Report any change to the price, the free-tier limits, or the terms, with a title and a URL for each change, and flag anything that now costs money. Do not buy, sign up, register, send, post, or contact anyone. Update the dates in the note. Deliver to the user in this chat. If nothing changed or the note is missing, say so in one line and stop.
