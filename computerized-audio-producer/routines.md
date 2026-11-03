# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine.

## Weekly free-GPU budget check

- **Schedule:** Mondays at 09:00.
- **Cron:** `0 9 * * 1`
- **Timezone:** The user's local timezone. Set it when creating the routine.
- **Delivers:** In this chat, to the user.
- **Prompt:** Check how many free Kaggle GPU hours are left this week and list any queued or unfinished audio jobs. Report the hours left and the queue in a few lines. Do not start any job, do not spend money, and do not message anyone. If nothing is queued, say so in one line and stop. If the Kaggle login is missing, say that in one line and stop. Deliver to the user in this chat.
