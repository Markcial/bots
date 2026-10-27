# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine. Keep two routines at least 5 minutes apart.

## Routine name

- **Schedule:** When it runs, in words.
- **Cron:** `0 9 * * 1-5`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user. Name any memory note a later routine must read.
- **Prompt:** The instruction the scheduler sends. Repeat what the bot must not do. Deliver to the user in this chat. If there is nothing to report, say so in one line and stop.
