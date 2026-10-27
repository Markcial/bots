---
name: delegate-task
description: Assign work to a teammate bot with SendToAgent after the user names that agent and says yes.
---

# Delegate a task

Use when another bot the user already runs should do the work.

## Steps

1. Name the target and the outcome. Use the display name and agent id the user gave you. If you have no id, ask for one. Do not guess an id.
2. If there is no teammate for this job, ask the user to add one or do the work yourself. Do not create a bot to fill the gap from this skill.
3. Learn what the teammate needs (inputs, files, constraints) before you assign the task. Asking is a message: show the question, then send it with `SendToAgent` only after the user says yes.
4. Write the assignment: outcome, inputs you have, inputs still missing, constraints, and how the result comes back.
5. Show the assignment to the user. Wait for an explicit yes, then send that assignment with `SendToAgent` to the id they named.
6. If the work also includes a send, publish, purchase, or contact outside that teammate message, get a separate yes for that action.
7. Repeat the decision in the reply. Do not claim the teammate finished until a reply comes back.

## Do not

- Assign work to a planned name that has no folder and no teammate id.
- Create a bot. A new bot is a chat draft plus `grokbot://app/v1/bot-template?id=<share id>`, from `propose-bot`, after the user says yes. Do not invent a share id.
- Call a teammate by any path other than `SendToAgent`.
- Fill missing inputs with guesses about the user's private life.
