---
name: report-findings
description: Write the report with the conclusion first, facts apart from opinion, tradeoffs, costs, and what could not be verified.
---

# Report findings

Use when research or an experiment is finished and the user needs the result. Start from `bash scripts/new-report.sh <slug>` in the kit folder saved in the memory note `workspace-path` (if the note is missing, run the skill `setup-workspace` first). The template follows the steps below.

## Steps

1. Open with the conclusion in one or two sentences, and the decision it supports.
2. Give the evidence: each claim with its title and URL, in the same paragraph. Put facts and opinion in separate sections, and label the opinion.
3. List the tradeoffs of the options that are still open.
4. State every cost: what is free, what is not, and what an account or a sign-up would involve.
5. List what you could not verify, with the reason (page blocked, source missing, figure disputed).
6. End with one next step. If it needs money, an account, or contact with a person, say that it waits for the user's yes.
7. Keep it short. Link longer material in a file instead of pasting it.
8. Run `bash scripts/linkcheck.sh <report>` before you hand it over. Fix or delete every broken URL, check blocked ones another way or move the claim to what you could not verify, and paste the summary line at the bottom. A link check shows that a URL opens, not that the page supports the claim.

## Do not

- Bury the conclusion under the method.
- Present an opinion as a finding.
- Pad the report with sources you did not use.
