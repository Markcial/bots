# Getting started

1. X in Grok Bot has two layers:
   - **Built-in public reads** (posts, users, search, trends, news) need no connection. Limits: 30 calls per minute, 1000 per day, at most 25 results per call.
   - **Your likes, bookmarks, accounts you follow, and home timeline** need the X plugin. Open Connectors or Plugins, choose X, and sign in as yourself.
   This bot never writes to X. It does not like, reply, follow, post, bookmark, or send a message, even when a write tool exists. It does not read direct messages. If a permission screen looks like it grants posting, stop and ask before you continue.
   Without the plugin, public reads still work. The bot says the private feed was not read and asks you for topics in text.
2. Ask for tomorrow's digest on one topic, or let the evening routine pick the strongest cluster from likes, bookmarks, and accounts you follow.

   First message to try: `Tomorrow's digest on <topic>.` or `Run evening study once.`

3. Check that every factual sentence has a title and a URL. Open two of them.
4. Name topics to skip. The bot should remember those skips as study preferences, not as a profile of you.
5. Evening study saves the digest as a memory note titled `digest-YYYY-MM-DD`, using the next day's date. Morning delivery reads that note. If the note is missing, it says so and offers to draft from topics you name.
6. Expect a short digest: a few sentences of context, three sources, and one practice task.
