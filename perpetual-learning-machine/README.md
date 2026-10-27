# Perpetual Learning Machine

Stage: **ready**. Template, avatar, and motion presentation video are finished. Still unpublished.

Also called Continuous Learning Coach.

Studies what you already pay attention to on X and turns it into material for the next day. Public posts, users, search, trends, and news need no connection. Your likes, bookmarks, follows, and home timeline need the X plugin. It never writes to X: it does not like, reply, follow, post, or bookmark. Every factual claim in the digest cites a source. Evening study saves the digest to memory. Morning delivery reads that note.

## Use cases

- Turn recent bookmarks into a short study list for tomorrow.
- Go deeper on one topic that keeps showing up in likes and follows.
- Produce a daily digest: what the topic is, three sources, one thing to practice.
- Keep a trail of titles and URLs so you can check the work.

## X access

Built-in public reads work immediately, with limits of 30 calls per minute, 1000 per day, and 25 results per call. Likes, bookmarks, following, and the home timeline wait on the X plugin (Connectors or Plugins, then X, then sign in). Without that plugin the bot asks you to name a topic. It does not invent a feed, and it does not read direct messages.

## Media

Identity and motion presentation live in [`media/`](media/):

| Asset | Path |
| --- | --- |
| Avatar (1024 / 512 / 256 / 128 / 48 / 32) | [`media/avatar-1024.png`](media/avatar-1024.png) (and siblings) |
| Motion video 16:9 | [`media/plm-16x9.mp4`](media/plm-16x9.mp4) |
| Motion video 1:1 | [`media/plm-1x1.mp4`](media/plm-1x1.mp4) |
| Sample frame | [`media/sample-frame.png`](media/sample-frame.png) |

After merge to `main`, raw URLs look like `https://raw.githubusercontent.com/Markcial/bots/main/perpetual-learning-machine/media/avatar-1024.png`. Bed music licence: [`LICENSE-music.md`](../LICENSE-music.md).

## Stage

`ready`. Copy, avatar, and motion presentation video are done and reviewed. Someone can publish the Grok Bot template without writing new copy. No template link yet (`xai_template_url` stays null until `launch`).
