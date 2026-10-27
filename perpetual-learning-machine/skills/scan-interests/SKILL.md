---
name: scan-interests
description: Read X likes, bookmarks, and follows for study topics, and ask for topics if the X plugin is missing.
---

# Scan interests

Use when you need study topics from the user's X activity.

## Steps

1. If the X plugin is connected, read the private surfaces with `get_users_liked_posts`, `get_users_bookmarks`, and `get_users_me_following`. Use the window the user names, or the last 7 days. The home timeline also needs the plugin. Read it only when the user asks. Do not read direct messages.
2. Followed accounts have no topics tool. Derive topics from their bios and from recent posts. Recent public posts can use built-in X reads, which need no plugin.
3. Built-in public reads are posts, users, search, trends, and news. Limits on X reads: 30 calls per minute, 1000 per day, at most 25 results per call. Cap pages so a 7-day window stays inside those limits.
4. Cluster what you actually read into at most five topics. Count how they showed up, and name the kind of signal (like, bookmark, or follow). Drop topics the user has asked to skip.
5. If the plugin is missing or a private read fails, say the private feed was not read and ask for topics in text. Keep going with any public reads that did work. Do not invent likes, bookmarks, or follows.

## Do not

- Write to X. Do not like, reply, follow, post, bookmark, or send a message, even if those tools are listed.
- Infer private motives. Report topics, not a story about the person.
- Spend the daily call budget on a single scan. Stop and say what you still have not read.
