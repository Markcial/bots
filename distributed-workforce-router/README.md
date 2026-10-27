# Distributed Workforce Router

Stage: **sketch**. Not published on x.ai yet.

Coordinator for a set of Grok bots. It does a task itself when it already can. When a catalog template fits, it recommends that template. When a job will keep coming back and nothing in the catalog covers it, it proposes a new bot. Before it assigns work, it asks what the other bot needs. It does not send, publish, purchase, or contact anyone until you say yes to that action.

## Use cases

- Split a request into tasks and say which ones it will do itself.
- Pick a template from `catalog.json` instead of inventing a duplicate bot.
- Draft a new bot from `_template/` when the catalog has a gap.
- Hand a task to a bot you already run, after the inputs and your approval are clear.
- Stop outbound actions (messages, posts, purchases, contact) until you allow that specific action.

## Stage

`sketch`. Template text only. No avatar, no motion video, no x.ai URL.
