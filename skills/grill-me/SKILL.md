---
name: grill-me
description: >-
  Use when the user says "grill me" or wants a plan, bot design, decision or
  idea stress-tested through a relentless round-by-round interview before
  anything is built.
---
Adapted from the `grilling` skill in [mattpocock/skills](https://github.com/mattpocock/skills), MIT License, Copyright (c) 2026 Matt Pocock.

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled: the questions you can ask now without guessing at answers you haven't heard yet. Ask the whole frontier in one round: number each question and give your recommended answer. Then wait for the user's answers before the next round.

Format a round like so:

```
❓ **Q1** - **<question title>**: <question body, may include multiple choices>

➡️ <your recommended answer>

---

❓ **Q2** - **<question title>**: <question body>

➡️ <your recommended answer>
```

Word each question so "yes" accepts your recommended answer.

Each round of answers reshapes the tree: settled decisions push the frontier outward and unblock questions that depended on them. Recompute the frontier and ask the next round. A question whose answer depends on another question still open in this round belongs to a later round.

Finding facts is your job, never the user's. When a question needs a fact from the environment (files, tools, connectors, the web), look it up yourself, in the background if it is slow; don't ask the user for anything you could find. Don't block on it: only the questions downstream of a running lookup wait; ask the rest now. The decisions are the user's: put each to them and wait.

The session is done when the frontier is empty: every branch visited, nothing silently assumed. Then restate the full plan in your own words and do not act on it until the user confirms you share the same understanding.
