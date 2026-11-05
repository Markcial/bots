# Perpetual Learning Machine

Stage: **launch**. The Grok Bot template is published: [open the template](https://x.ai/bot/PsppjjXTB3Ggf0YmCTlNO).

Also called Continuous Learning Coach.

Studies what you already pay attention to on X and turns it into material for the next day. It keeps a topic backlog in `backlog.json` in its working folder, teaches the strongest open topic, and lists every other open topic at the end of the digest. A bookmark, a reply, or a post of yours weighs more than a like. A single like or bookmark with something to learn stays on the backlog. Only memes, jokes, link-only posts with nothing to study, crypto spam, and similar noise are set aside. Topics you skip stay skipped. Public posts, users, search, trends, and news need no connection. Your likes, bookmarks, follows, posts, replies, and home timeline need the X plugin. It never writes to X: it does not like, reply, follow, post, or bookmark. Every factual claim in the digest cites a source. A radar line leaves the source off when none was found. Evening study saves the digest to memory and updates the backlog. Morning delivery reads that note, radar included.

## Use cases

- Turn a bookmark, a like, a reply, or a post of yours into a topic that is still there tomorrow, even if it showed up once.
- Go deeper on the open topic with the strongest signal, and skip anything taught in the last three digests.
- Produce a daily digest: what the main topic is, three sources, one thing to practice, then "Also on your radar" for every other open topic.
- Keep a trail of titles and URLs so you can check the work.

## X access

Built-in public reads work immediately, with limits of 30 calls per minute, 1000 per day, and 25 results per call. Likes, bookmarks, following, your own posts and replies, and the home timeline wait on the X plugin (Connectors or Plugins, then X, then sign in). Without that plugin the bot asks you to name a topic and keeps using the backlog it already has. It does not invent a feed, and it does not read direct messages.

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

`launch`. The template is published once, with its avatar and motion presentation video, at https://x.ai/bot/PsppjjXTB3Ggf0YmCTlNO. `xai_template_url` in `catalog.json` holds that link.
