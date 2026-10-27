---
name: propose-bot
description: Draft a new bot in chat and give the user a bot-template link. Do not create the bot.
---

# Propose a bot

Use when triage found a recurring job and the catalog has no fit.

## Steps

1. Confirm that no catalog entry fits and that the job will recur. Fetch `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json`. If that fails, use the catalog the user pasted. A one-off stays with you.
2. Choose a three-word title: a buzzword (Perpetual, Distributed, Hyperconnected, Continuous, Superconnected, or a peer of those), a domain, and a role. The folder name is the kebab-case of that title.
3. Write the draft in the chat. Do not assume a local copy of `_template/`. Try the public files under `https://raw.githubusercontent.com/Markcial/bots/main/_template/` (`README.md`, `profile.md`, `getting-started.md`, `memories.md`, `routines.md`, `skills/example-skill/SKILL.md`). If that fetch fails, use the heading list below.
   The draft must include:
   - Profile: name, title, description, persona
   - Getting started: first steps for a new user
   - One skill, with YAML frontmatter `name` and `description`
   - Seed memories that are generic and contain no personal data
   - One routine with a schedule, a 5-field cron, a timezone note, a prompt, and where it delivers
   - A note that `media/` later holds the avatar and the motion video
   Leave the stage at `sketch`.
4. Show the draft. You cannot create the bot. Do not add it to `catalog.json`. Do not claim it exists.
5. After the user says yes to the proposal, give them the draft pack and the link `grokbot://app/v1/bot-template?id=<share id>`. If they already have a share id, put it in the link. If they do not, tell them that link is how Grok Bot opens a shared template, and that they create or import the bot. Do not invent a share id. Wait until they confirm the bot exists.
6. Carry these rules into the draft: nothing is sent, published, purchased, or contacted without an explicit yes, and a teammate is messaged only with `SendToAgent`.

## Do not

- Propose a title that duplicates an existing catalog entry.
- Silently create a bot, a folder, or a catalog row.
- Claim the bot exists before the user confirms.
