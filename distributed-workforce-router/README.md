# Distributed Workforce Router

Stage: **launch**. The Grok Bot template is published: [open the template](https://x.ai/bot/79dGJd9FqqNXZZ773YhX8).

Coordinator for a set of Grok bots. It does a task itself when it already can. When a catalog template fits, it recommends that template. When a job will keep coming back and nothing in the catalog covers it, it drafts a new bot and gives you a `grokbot://app/v1/bot-template?id=<share id>` link. It does not create the bot. It messages a teammate only with `SendToAgent`, using an agent id you provide, and only after you say yes. It does not send, publish, purchase, or contact anyone until you say yes to that action.

## Use cases

- Split a request into tasks and say which ones it will do itself.
- Pick a template from the public catalog JSON instead of inventing a duplicate bot.
- Draft a new bot in the chat when the catalog has a gap, then hand you the template link.
- Hand a task to a teammate you already run, after you name that agent and approve the message.
- Stop outbound actions (messages, posts, purchases, contact) until you allow that specific action.

## Media

Identity and motion presentation live in [`media/`](media/):

| Asset | Path |
| --- | --- |
| Avatar (1024 / 512 / 256 / 128 / 48 / 32) | [`media/avatar-1024.png`](media/avatar-1024.png) (and siblings) |
| Motion video 16:9 | [`media/router-16x9.mp4`](media/router-16x9.mp4) |
| Motion video 1:1 | [`media/router-1x1.mp4`](media/router-1x1.mp4) |
| Sample frame | [`media/sample-frame.png`](media/sample-frame.png) |

After merge to `main`, raw URLs look like `https://raw.githubusercontent.com/Markcial/bots/main/distributed-workforce-router/media/avatar-1024.png`. Bed music licence: [`LICENSE-music.md`](../LICENSE-music.md).

## Stage

`launch`. The Grok Bot template is published: [Open template](https://x.ai/bot/79dGJd9FqqNXZZ773YhX8).
