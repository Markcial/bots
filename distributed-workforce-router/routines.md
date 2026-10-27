# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine. These two runs are 15 minutes apart.

## Morning triage

- **Schedule:** Weekdays at 09:00.
- **Cron:** `0 9 * * 1-5`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user.
- **Prompt:** List open commitments you were given. For each one, say whether you will do it, which catalog template fits, or that you are blocked on approval. Read the catalog from `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json`. If that fetch fails, use a catalog the user pasted, or say you could not read the catalog. Do not send, publish, purchase, contact anyone, or call `SendToAgent`. Do not create a bot. End with a numbered list of decisions that need a yes or no today. Deliver to the user in this chat. If there is nothing to report, say so in one line and stop.

## Catalog gap check

- **Schedule:** Mondays at 09:15.
- **Cron:** `15 9 * * 1`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user.
- **Prompt:** Fetch `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json`. If that fails, use a catalog the user pasted, or say you could not read the catalog and stop. From the tasks discussed in the last week, name any recurring job that no entry covers. Propose at most one new bot title, with the folder name and a one-line summary. Do not create the bot. The install link, only after the user agrees and only if they have a share id, is `grokbot://app/v1/bot-template?id=<share id>`. Deliver to the user in this chat. If there is nothing to report, say so in one line and stop.
