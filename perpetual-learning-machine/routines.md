# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine. These two runs are hours apart.

21:00 is outside the usual quiet hours on purpose. The digest is prepared overnight and stored in memory so the morning run can read it.

## Evening study

- **Schedule:** Every day at 21:00.
- **Cron:** `0 21 * * *`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user. Also saves a memory note the morning routine reads.
- **Prompt:** Build tomorrow's digest. Use the X plugin, read-only, for the user's likes, bookmarks, and accounts they follow. Derive topics of followed accounts from bios and recent posts. There is no topics tool. Public posts, users, search, trends, and news need no plugin. The home timeline needs the plugin. Read it only if the user has asked. Stay within 30 calls per minute, 1000 per day, and 25 results per call. Never write to X: do not like, reply, follow, post, bookmark, or send. Do not read direct messages. If the plugin is missing, say the private feed was not read and ask for topics in text. Do not invent a feed. Skip any topic the user has ruled out. Every factual claim needs a source title and URL. Include one practice task with a done-when line. If a claim has no source, omit it. Save the finished digest as a durable memory note titled `digest-YYYY-MM-DD`, using tomorrow's date. Deliver to the user in this chat. If there is nothing to report, say so in one line and stop.

## Morning delivery

- **Schedule:** Every day at 08:00.
- **Cron:** `0 8 * * *`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user.
- **Prompt:** Read the memory note `digest-YYYY-MM-DD` whose date is today. Deliver that digest. Keep each citation next to the claim it supports. If the note is missing, say so in one line and offer to draft one from topics the user names. Do not write to X and do not call the X plugin unless the user asks for a new draft and the private feed is required. Deliver to the user in this chat. If there is nothing to report, say so in one line and stop.
