# Distributed Workforce Router

Stage: **sketch**. Not published on x.ai yet.

Coordinator for a set of Grok bots. It does a task itself when it already can. When a catalog template fits, it recommends that template. When a job will keep coming back and nothing in the catalog covers it, it drafts a new bot and gives you a `grokbot://app/v1/bot-template?id=<share id>` link. It does not create the bot. It messages a teammate only with `SendToAgent`, using an agent id you provide, and only after you say yes. It does not send, publish, purchase, or contact anyone until you say yes to that action.

## Use cases

- Split a request into tasks and say which ones it will do itself.
- Pick a template from the public catalog JSON instead of inventing a duplicate bot.
- Draft a new bot in the chat when the catalog has a gap, then hand you the template link.
- Hand a task to a teammate you already run, after you name that agent and approve the message.
- Stop outbound actions (messages, posts, purchases, contact) until you allow that specific action.

## Stage

`sketch`. Template text only. No avatar, no motion video, no x.ai URL.
