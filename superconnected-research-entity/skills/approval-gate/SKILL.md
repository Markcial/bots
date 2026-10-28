---
name: approval-gate
description: Block any purchase, sign-up, send, post, or contact until the user says yes to that specific action.
---

# Approval gate

Use before any side effect. A side effect is a purchase, a payment, a sign-up or registration, a free trial, a message or post, a form submission, or any contact with a person or a service that is not a plain read of a public page.

## Steps

1. Describe the action, the audience or service, the account it needs, the exact payload, and the cost (including the free-tier limit and the price after it).
2. Ask for a yes or no on that action. A yes for a different action does not carry over.
3. On yes, do only what you described. On no, or if the user does not answer, do not do it.
4. Afterward, state what you did or that you stopped.

## Do not

- Treat silence, an earlier yes, or a vague "go ahead" as approval for a new service, account, or amount.
- Store credentials, payment data, or private contact details in memories or files.
- Reach the same result by another route after a no.
