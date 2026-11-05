---
name: prepare-digest
description: Assemble next-day learning material, list every other open topic on the radar, and save the digest as a memory note the morning routine can read.
---

# Prepare the digest

Use when it is time to shape next-day learning material.

The digest teaches one main topic in depth, then lists every other open backlog topic under `Also on your radar`. A topic the user liked, bookmarked, replied to, or posted about, or that you derived from an account they follow, stays visible until it is taught or they skip it.

## Steps

1. Read `backlog.json` (skill `scan-interests`). The main topic is the one `study-topic` just studied. If you have not studied one yet, pick it with the same rule: the open entry with the highest strength, including signals merged today. A bookmark, a reply, or an own post weighs 3. A like or a follow weighs 1. Break ties by `signal_count`, then by the earliest `first_seen`, then by the order already in the file. Skip `dropped` entries, and skip a topic still `taught` from one of the last three digests. If the user named a topic that is not dropped, that topic is the main one. A `dropped` topic stays dropped until they explicitly un-skip it.
2. Write the deep dive from the study notes: a title, five to twelve sentences, three cited sources, one practice task with a done-when line, and an optional "skip this if" line.
3. Put each citation in the same paragraph as the claim it supports. End the deep dive with a source list of titles and URLs.
4. End the digest with `Also on your radar`, using the format below. List every `open` topic except the main topic, strongest first. `taught` and `dropped` topics stay off the list.
5. For each radar line you will show, add one checkable source when you found one: a page you opened, or a source already attached to that signal. One lookup per shown line is enough. Stay inside the call limits from `study-topic`. If you find no source, end the line after the triggering post. Never invent a title or a URL.
6. Mark what you could not verify. Leave it out rather than guessing.
7. If you are replacing a digest note for the same date and the previous main topic is different, set that previous entry back to `open` when its `taught_on` is that same date.
8. Set the main topic's status to `taught` and `taught_on` to the digest date (tomorrow's date). Write the whole `backlog.json` back.
9. Save the digest as a durable memory note titled `digest-YYYY-MM-DD`, using the next day's date. Morning delivery reads that note and delivers it in full, including the radar. If a note for that date already exists, replace it with this draft and say that you replaced it.
10. Deliver the digest in this chat as well, including the radar.

If the backlog has no open topic and the user named none, say so in one line and stop. An empty scan today still produces a digest when older open topics are in the file.

## Digest format

```
# <title>

<five to twelve sentences. Each claim sits with its citation.>

Practice: <one task>
Done when: <a check the user can apply>
Skip this if: <optional>

Sources
- <title> — <url>
- <title> — <url>
- <title> — <url>

## Also on your radar

- <topic> — signal count <signal_count>, since <first_seen>. Triggered by <post url>. Source: <title> — <url>
- <topic> — signal count <signal_count>, since <first_seen>. Triggered by <post url>.
```

Radar rules:

- The heading is exactly `Also on your radar`.
- One line per open topic that is not the main topic. Strongest first.
- Show at most eight lines. When more open topics remain, add one line: `<N> more open topics are waiting.`
- `since` is `first_seen`. The signal count is the raw `signal_count` from the backlog.
- The triggering post is the first URL in `examples`. When `examples` is empty and `seen_urls` has a `follow:` entry, write `From a followed account: <account url>` using the URL after `follow:`. When no URL is stored, write `No triggering post stored.` Do not invent a URL, and do not print the `follow:` prefix.
- The source is optional. Include `Source: <title> — <url>` only when you found a real one. Otherwise stop after the triggering post.
- When no other topic is open, the section is one line: `Nothing else is open.`

## Do not

- Post, send, or schedule the digest anywhere except this chat and that memory note.
- Leave the digest only in the evening conversation. A later run cannot see that conversation.
- Turn the digest into a log of the user's activity. Lead with the topic. The radar names topics, not a story about the person.
- Omit an open topic because its signal was a single like or bookmark, or because the list is long. Past eight, name the count that is still waiting.
- Write to X.
