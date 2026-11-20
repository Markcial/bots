---
name: design-bot
description: >-
  Use when the user wants a new Grok Bot designed or an existing bot tightened
  up: one job, anti-jobs, voice and wake, written as a bot description,
  checked, then verified after creation.
---
# Design a bot

Create the bot directly. Don't make a shareable template unless the user asked for one. A bot can't be deleted from a tool, so only create a bot for a real job, and only after the user's explicit OK to create it.

## 1. A bot is four fields, in this order
1. **One job.** One sentence: what it does every time it wakes.
2. **Anti-jobs.** What it never does, even if asked. Adjacent work belongs to another bot.
3. **Voice.** A few words. Match the user or a named character, never a generic assistant.
4. **Wake.** On-demand chat, a standing routine, or both. It stays quiet when there's nothing to report.

Keep the name short. The description carries all four fields. No leftover tools, no model essays, no "I can also help with...".

## 2. Intake (preference questions only)
Ask only what no experiment can settle, and skip anything already answered:
- the one job
- voice and name, if they care
- standing routine or on-demand
- who it talks to (only the user, other bots, or an outside channel like Slack, X or email)

Don't ask about tools, plugins or the model when a working sibling bot can be copied. Don't ask about reversible details like colour or nickname: pick one and say what you picked. For a fuzzy idea, run the `grill-me` skill first.

## 3. Coding bots
Put these in the description:
- one job and explicit anti-jobs
- short, plain replies with no filler
- repo work goes to a cloud coding agent, never a local clone on the user's computer
- slash-skills are live files, not app commands
- copy the current model rule from an existing coding bot unless the user names one
- verify before claiming done

## 4. Non-coding bots
Put these in the description:
- the ONLY job, named in the first sentence
- stays quiet when there's nothing to report, with no "(no change)" filler
- never does the adjacent verb: a mentions scout doesn't post, a drafter doesn't send, a researcher doesn't publish
- the concrete how: which API, inbox, channel or connector, never "use whatever tools you have"
- no coding instructions unless the job is hybrid and the split is explicit

## 5. Tool trimming
Name only the tools and connectors the job needs. Every tool in the persona maps to the one job.

## 6. Description template (a new bot takes only a name and a description)
```
<Name> is <user>'s <role>. Its only job: <one sentence>.
Never: <anti-job 1>, <anti-job 2>, <anti-job 3>. Adjacent work goes to <other bot>.
How: <concrete connector/inbox/channel/schedule>.
Voice: <few words, language>.
Wakes: <on-demand | routine name + schedule>. Stays quiet when there's nothing to report.
Nothing goes out (posts, sends, purchases) without <user>'s explicit OK.
```
Add the user's house rules from memory when they're relevant, such as task identifiers, where source code lives, and which inbox the bot uses for signups. If the bot later stages a public template, the template description must be its full live description.

## 7. Checklist before creating it
- [ ] the job is one sentence and real
- [ ] no existing teammate already does it (extend rather than create)
- [ ] anti-jobs listed, including the adjacent verb
- [ ] voice and language set
- [ ] wake decided, and quiet-when-empty stated
- [ ] concrete how named
- [ ] no leftover tools or padding
- [ ] approval gate for anything external
- [ ] coding bot: the coding bar applied

## 8. After creating it
1. Read the new bot's live profile back and check that the name and description match what was approved.
2. Tell the user the name and the one-job line, and how they can delete it from the app if they change their mind.
3. If it needs a standing routine and you can't write another bot's routines, message the new bot right away with the exact routine to create (name, prompt, schedule or trigger), and confirm to the user you did.
