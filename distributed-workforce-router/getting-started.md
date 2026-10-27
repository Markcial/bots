# Getting started

This coordinator is in prepare. It can plan and draft. It cannot publish, spend, or contact anyone on your behalf, and it cannot create another bot.

1. It reads the catalog by fetching `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json`. If that fetch fails, paste the JSON into a seed memory or give it another URL. It must not invent entries. Until this file is on `main`, the fetch returns not found, so the paste is the way through.
2. Name every teammate bot it may message: display name and agent id. It reaches a teammate only with `SendToAgent` and that id. If you have no teammates, say so. It will do the work itself or propose a template.
3. Give it one real task. Ask it to answer "I'll do this" or "this belongs to a template" before it expands the plan.

   First message to try: `I need someone to make a promo video. What can you do yourself, what is already in the catalog, and would this need a new bot?`

4. When it recommends a template, check the stage in the catalog. A null `xai_template_url` means not published yet. A sketch is text only. Planned names in the README have no folder. It must not assign work to them.
5. When it wants to message a teammate, post, buy, or contact someone, answer yes or no for that action. Silence is not approval. `SendToAgent` counts as a message.
6. When it proposes a new bot, it puts a draft in the chat. It does not create the bot. After you say yes, it offers `grokbot://app/v1/bot-template?id=<share id>` if you already have a share id, together with the draft pack. You create or import the bot, then tell it the bot exists. It must not claim that before you confirm. How a share id is minted in the Grok Bot UI is confirmed at launch.

You should get a short triage, a named next step, and a stop whenever an outbound action needs you.
