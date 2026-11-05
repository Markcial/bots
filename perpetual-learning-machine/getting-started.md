# Getting started

1. X in Grok Bot has two layers:
   - **Built-in public reads** (posts, users, search, trends, news) need no connection. Limits: 30 calls per minute, 1000 per day, at most 25 results per call.
   - **Your likes, bookmarks, accounts you follow, your own posts and replies, and home timeline** need the X plugin. Open Connectors or Plugins, choose X, and sign in as yourself.
   This bot never writes to X. It does not like, reply, follow, post, bookmark, or send a message, even when a write tool exists. It does not read direct messages. If a permission screen looks like it grants posting, stop and ask before you continue.
   Without the plugin, public reads still work. The bot says the private feed was not read and asks you for topics in text. Topics already in its backlog stay there.
2. The bot keeps a topic backlog in `backlog.json` in its working folder. Each study run merges new likes, bookmarks, replies, your posts, and topics from accounts you follow. A bookmark, a reply, or a post of yours counts more than a like. A single like or bookmark with something to learn is kept. Only memes, jokes, link-only posts with nothing to study, crypto spam, and similar noise are set aside.
3. Ask for tomorrow's digest on a topic you name, or let the evening routine pick the strongest open topic from that backlog. It will not repeat a topic it taught in the last three digests. Every other open topic is listed at the end.

   First message to try: `Tomorrow's digest on <topic>.` or `Run evening study once.`

4. Check that every factual sentence has a title and a URL. Open two of them. A radar line with no source stops after the triggering post. It does not invent a link.
5. Name topics to skip. The bot marks those `dropped` in the backlog and remembers the skip as a study preference. It does not bring them back unless you explicitly un-skip one, and it does not treat the list as a profile of you.
6. Evening study saves the digest as a memory note titled `digest-YYYY-MM-DD`, using the next day's date, and marks the main topic taught in the backlog. Morning delivery reads that note, including the radar. If the note is missing, it says so and offers to draft from topics you name.
7. Expect a short deep dive: a few sentences of context, three sources, and one practice task with a done-when line. Then an "Also on your radar" section: every other open topic, strongest first, up to eight lines, each with its signal count, since when, the post that triggered it, and one source when one was found. If more are open, the section says how many are still waiting.
