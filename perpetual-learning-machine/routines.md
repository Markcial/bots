# Routines

Cron is five fields: minute, hour, day of month, month, day of week. Interpret it in the user's local timezone, and set that timezone when you create the routine. These two runs are hours apart.

21:00 is outside the usual quiet hours on purpose. The digest is prepared overnight and stored in memory so the morning run can read it. The topic backlog lives in `backlog.json` in the working folder recorded in the memory note `backlog-path`, so topics carry from one evening to the next.

## Evening study

- **Schedule:** Every day at 21:00.
- **Cron:** `0 21 * * *`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user. Also saves a memory note the morning routine reads, and updates `backlog.json`.
- **Prompt:** Build tomorrow's digest. Use the skills scan-interests, study-topic, cite-sources, and prepare-digest, in that order. Read `backlog.json` in the working folder recorded in the memory note `backlog-path`. If the note or the file is missing, start `{ "topics": [] }` in the working folder and save the path. Merge today's signals into that file. Use the X plugin, read-only, for the user's likes, bookmarks, accounts they follow, and their own posts and replies. Derive topics of followed accounts from bios and recent posts. There is no topics tool. Public posts, users, search, trends, and news need no plugin. The home timeline needs the plugin. Read it only if the user has asked. Stay within 30 calls per minute, 1000 per day, and 25 results per call. Never write to X: do not like, reply, follow, post, bookmark, or send. Do not read direct messages. If the plugin is missing, say the private feed was not read and ask for topics in text. Do not invent a feed. Keep the backlog you already have. A bookmark, a reply, or the user's own post weighs 3. A like or a follow weighs 1. signal_count is the raw total. A single like, bookmark, reply, or own post with learning content is a topic. Set aside only memes, jokes, link-only posts with nothing to study, crypto spam, and similar noise. Do not add noise to the backlog. Topics the user has ruled out stay status dropped and are not reopened unless the user explicitly un-skips one. Pick the main topic by strength across the open backlog, including today. Do not repeat a topic taught in the last three digests. If the user named a topic that is not dropped, that topic is the main one. Study it with three cited sources, one practice task with a done-when line, and a citation on every claim. If a claim has no source, omit it. End the digest with an "Also on your radar" section that lists every other open topic, strongest first, one line each, with signal count, since when, the triggering post, and one checkable source if you found one. Never invent a source. Show at most eight lines, then say how many more are waiting. Mark the main topic taught, with taught_on set to tomorrow's date, and write `backlog.json` back. Save the finished digest as a durable memory note titled `digest-YYYY-MM-DD`, using tomorrow's date. Deliver it to the user in this chat, radar included. If the backlog is empty and the user named no topic, say so in one line and stop.

## Morning delivery

- **Schedule:** Every day at 08:00.
- **Cron:** `0 8 * * *`
- **Timezone:** The user's local timezone.
- **Delivers:** In this chat, to the user.
- **Prompt:** Read the memory note `digest-YYYY-MM-DD` whose date is today. Deliver that digest in full, including the "Also on your radar" section. Do not drop open topics from it, and do not rewrite `backlog.json` unless the user asks for a new draft. Keep each citation next to the claim it supports. If the note is missing, say so in one line and offer to draft one from topics the user names. Do not write to X and do not call the X plugin unless the user asks for a new draft and the private feed is required. Deliver to the user in this chat. If there is nothing to report, say so in one line and stop.
