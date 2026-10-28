---
name: run-experiment
description: Settle a question with the smallest free test, run in a scratch folder, and report exactly what ran and what happened.
---

# Run an experiment

Use when an opinion is not enough and a small test can answer the question. Work in the kit folder saved in the memory note `workspace-path` (if the note is missing, run the skill `setup-workspace` first).

## Steps

1. State the hypothesis and what result would prove it wrong.
2. Choose the smallest test: one script, one benchmark, one trial of an open-source tool. Use free tools only, and no accounts.
3. Run `bash scripts/new-experiment.sh <slug>` and work in that folder's `scratch/`. Fill in `experiment.md` and keep the commands in `run.sh`. Do not touch the user's files or services.
4. Save the commands, the versions, and the raw output next to a short log: what you ran, what you saw, and what you changed between runs.
5. Run it again if the result is surprising. Say how many times you ran it and how much the results varied.
6. Report the result with the log. Say what the test does not show.

## Do not

- Install something that needs a licence, an account, or a card.
- Report a result you did not run, or round a number you did not measure.
- Send data from the test anywhere. Keep it local.
