---
name: study-topic
description: Study the strongest open backlog topic from citable sources and write notes for the next digest.
---

# Study a topic

Use when the digest needs sourced notes. The deep dive is one topic. Every other open topic stays on the backlog for the radar.

## Steps

1. Read `backlog.json` (skill `scan-interests`). Pick the open entry with the highest strength across the backlog, including signals merged today. A bookmark, a reply, or an own post weighs 3. A like or a follow weighs 1. Break ties by `signal_count`, then by the earliest `first_seen`, then by the order already in the file. Do not pick a topic with status `dropped`, or a topic still `taught` from one of the last three digests (`taught_on` is one of the three most recent `digest-YYYY-MM-DD` notes). If the user named a topic that is not dropped, study that topic even if it was taught recently. If it is not in the backlog, add it with every count at 0, `signal_count` 0, `status` `open`, `taught_on` null, and no invented URLs, then write the file back. If they named a `dropped` topic, leave it dropped, say that it stays skipped, and study it only after they explicitly un-skip it.
2. Collect a small set you can cite: a definition or primary document, one deeper piece, and one opposing or limiting view when it exists. Use the web and built-in public X reads (posts, users, search, trends, news). This skill does not need the X plugin.
3. Stay within 30 calls per minute, 1000 per day, and 25 results per call when a source is on X.
4. Write notes the digest can reuse: what it is, why it matters, what is still contested, and what a 25-minute practice looks like.
5. Attach a source title and URL to every factual claim. If you cannot cite a claim, leave it out.
6. Leave the other open topics on the backlog. You may attach one source you already found for a later radar line. If you have no source, leave that line without one.

## Do not

- Copy long passages. Summarize.
- Fill a gap with an unsourced number or quotation.
- Write to X.
- Deep-study every open topic. One main topic gets the notes. The radar lists the rest.
- Drop a one-time like, bookmark, reply, or own post that has learning content. It stays `open` until it is taught or the user skips it.
