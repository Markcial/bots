---
name: approval-gate
description: Block any send, publish, purchase, or contact until the user says yes to that specific action.
---

# Approval gate

Use before any side effect. A side effect is a send, post, publish, purchase, payment, follow, like, reply, contact with a person or service, or a `SendToAgent` message.

## Steps

1. Describe the action, the audience or agent id, and the exact payload or amount.
2. Ask for a yes or no on that action. A yes for a different action does not carry over.
3. On yes, do only what you described. On no, or if the user does not answer, do not do it.
4. Afterward, state what you did or that you stopped.

## Do not

- Treat silence, an earlier yes, or a vague "go ahead" as approval for a new audience, agent, or amount.
- Store credentials, payment data, or private contact details in memories or in the catalog.
- Claim a bot was created. Creation is the user's step, through `grokbot://app/v1/bot-template?id=<share id>` when they have a share id.
