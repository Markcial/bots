---
name: scan-interests
description: Read X likes, bookmarks, follows, and the user's own posts and replies, and merge them into the topic backlog.
---

# Scan interests

Use when you need study topics from the user's X activity. Each run merges what you read into the topic backlog. A learning topic that appeared once stays in the backlog.

## Backlog

The backlog is `backlog.json` in the bot's working folder. The memory note `backlog-path` stores that folder path. Read the note, then the file, at the start of every run. If the note or the file is missing, create `{ "topics": [] }`, save the folder path in `backlog-path`, and say that you started a new backlog.

Each entry has:

- `topic`: a short subject name
- `first_seen` and `last_seen`: `YYYY-MM-DD`
- `signal_count`: the raw total of the counts below
- `counts`: `like`, `bookmark`, `reply`, `own_post`, and `follow` (use 0 when a kind did not occur)
- `examples`: up to three post URLs, triggering post first. These are for the digest. They are not the dedupe list.
- `seen_urls`: each counted signal once. A like, bookmark, reply, or own post is stored as `<kind>:<post url>`. A follow is stored as `follow:<account url>`. The same post may count as a like and as a bookmark. It may also be the example for a follow.
- `status`: `open`, `taught`, or `dropped`
- `taught_on`: the digest date `YYYY-MM-DD` when status is `taught`, otherwise null

The file holds topics and post URLs only. No contact details, secrets, or dossier.

Shape of one entry:

```json
{
  "topics": [
    {
      "topic": "distributed tracing",
      "first_seen": "2026-01-05",
      "last_seen": "2026-01-05",
      "signal_count": 1,
      "counts": {
        "like": 0,
        "bookmark": 1,
        "reply": 0,
        "own_post": 0,
        "follow": 0
      },
      "examples": ["https://x.com/example/status/1"],
      "seen_urls": ["bookmark:https://x.com/example/status/1"],
      "status": "open",
      "taught_on": null
    }
  ]
}
```

That shape is a pattern, not seed data. Do not copy the example topic into a user's file.

## Weights

A bookmark, a reply, or the user's own post weighs 3. A like weighs 1. A topic derived from an account they follow weighs 1, counted once per account. Strength is the weighted sum. `signal_count` is the raw total. Rank by strength, then by `signal_count`, then by the earliest `first_seen`. If those still tie, take the entry that appears first in the file.

## Steps

1. Read `backlog.json` as above.
2. If the X plugin is connected, read likes with `get_users_liked_posts`, bookmarks with `get_users_bookmarks`, follows with `get_users_me_following`, and the user's own posts with `get_users_posts`. If that call leaves out replies, use built-in search for the user's replies (`from:<handle> is:reply`) inside the same call limits. Take the handle from the signed-in user. Do not invent it. Use the window the user names, or the last 7 days. The home timeline also needs the plugin. Read it only when the user asks. Do not read direct messages.
3. Followed accounts have no topics tool. Derive topics from their bios and from recent posts. Recent public posts can use built-in X reads, which need no plugin. Count one `follow` per account per topic, applied in the merge below. A follow does not also count that account's post as a like, bookmark, reply, or own post.
4. Built-in public reads are posts, users, search, trends, and news. Limits on X reads: 30 calls per minute, 1000 per day, at most 25 results per call. Cap pages so a 7-day window stays inside those limits.
5. Set aside only true noise: memes, jokes, link-only posts with nothing to study, crypto spam, and similar posts with no learning content. Do not add those to the backlog. A single like, bookmark, reply, or own post that contains learning content is a topic.
6. Match topics to entries when they are the same subject, ignoring case. If you are unsure they match, keep both. A topic the user has asked to skip, or an entry that is already `dropped`, stays `dropped`. If the skip is not in the file yet, add it as `dropped` with every count at 0, `signal_count` 0, `taught_on` null, and no invented URLs. Do not increment a dropped topic when it shows up again. Set one back to `open` only when the user explicitly un-skips it.
7. Merge every other learning topic. Add a signal only when its `seen_urls` key is new (`like:`, `bookmark:`, `reply:`, or `own_post:` plus the post URL, or `follow:` plus the account URL). For a new topic, start every count at 0, then apply the new signals, and set `first_seen` to today, `status` to `open`, and `taught_on` to null. For an existing topic, keep `status` as it is. Increment the matching count, set `signal_count` to the new total, set `last_seen` to today, and append the key to `seen_urls`. Append a post URL to `examples` until it holds three, triggering post first, and never repeat a URL there. For a follow, that example is the recent post that showed the topic, when you have one.
8. Leave status `taught` while `taught_on` is one of the three most recent `digest-YYYY-MM-DD` notes. When a `taught` entry is no longer among those three, set it back to `open` and set `taught_on` to null so it can compete again. Do not change a `dropped` entry in this step.
9. If the plugin is missing or a private read fails, say the private feed was not read and ask for topics in text. Keep going with any public reads that did work, and with the backlog you already have. When the user names topics in text, match them as in step 6. A name that matches a dropped topic stays dropped. Add a new one as `open` with every count at 0, `signal_count` 0, and no URLs, unless they tell you the kind of signal. Do not invent likes, bookmarks, follows, posts, replies, or URLs.
10. Write the whole file back as JSON.

## Do not

- Write to X. Do not like, reply, follow, post, bookmark, or send a message, even if those tools are listed.
- Infer private motives. Report topics, not a story about the person.
- Spend the daily call budget on a single scan. Stop and say what you still have not read.
- Cap the backlog at a fixed number of topics, or drop a learning topic because it appeared once.
- Delete a dropped topic. The skip has to survive the next run.
