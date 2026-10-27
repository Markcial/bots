---
name: triage-request
description: Classify a new request as do-it-yourself, a catalog template, a new bot, or a clarifying question.
---

# Triage a request

Use when a request arrives and you have not yet decided who does the work.

## Steps

1. Restate the outcome in one sentence.
2. Choose one: do it yourself, recommend a catalog template, propose a new bot, or ask a clarifying question.
3. Do it yourself when the task is one answer, draft, summary, or plan that does not need another bot.
4. Recommend a template only after `consult-catalog` fetches `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json` (or the user has pasted it) and an entry's summary covers the job.
5. Propose a new bot only when the job will recur and no entry fits. Draft it in the chat. Do not create it.
6. Stop and ask when the outcome, the deadline, or the audience is ambiguous.

## Do not

- Start a send, publish, purchase, contact, or `SendToAgent` call from this skill.
- Treat a planned README name as a bot you can assign.
