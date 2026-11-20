---
name: task-identifiers
description: >-
  Use when the user writes a task identifier such as /explainer <slug>,
  /youtube <slug>, /bot <name>, or /post <slug>: present that task's full
  proposal, with the full body of every post, before doing or sending anything.
---
# Task identifiers: /explainer /youtube /bot /post

When a message starts with `/<type> <slug>`, the user is naming a task. Reply with that task's **complete proposal** and wait for the user's OK. Present the full text, never a summary or "see file". Nothing is published, sent, created or charged until the user approves it.

1. **Find the task.** Look up `<slug>` in your project folders, other agents' shared workspaces, memory and earlier chat. If it does not exist yet, say so and propose it from scratch. If several match, ask which one in one short question.
2. **Present per type** (every text in full, in the language it will be posted in; add character counts where a limit applies):
   - `/explainer <slug>`: topic, audience, length and formats, scene-by-scene outline, full narration, visuals plan, X post and reply, LinkedIn post, YouTube title, description and tags, costs, timeline, and what you need from the user. Pipeline: `explainer-pipeline`.
   - `/youtube <slug>`: video file(s) and duration, title, full description (no angle brackets), tags, thumbnail, Short title and description, visibility, settings (not made for kids; AI-altered content yes if applicable).
   - `/bot <name>`: purpose, name, full instructions, connectors/skills, schedule if any, who it overlaps with. Do not create the bot or publish a template before the OK. Method: `design-bot`.
   - `/post <slug>`: platform(s), the **full body of every post** (each post of a thread numbered, article body in full), media, links, posting order and time. Emails go through a draft-for-approval step, direct messages are shown in chat first, and nothing is posted without the OK.
3. **State the cost and the risk** in one line (money, quota, anything irreversible). Prefer free options and flag every cost.
4. **Ask once** with the exact actions named (for example "publish these 3 posts to X now"). If the user edits a text, show the revised full text again.
5. **After the OK**, run the matching skill (`explainer-pipeline`, `publish-video-everywhere`, `design-bot`) and report links and results. If the scope changes mid-way, go back to step 2.

Add your own identifiers the same way: one line per type listing everything the proposal must show in full.
