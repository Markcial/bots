# SRE kit: light harness for research and experiments

This file is for the bot (Superconnected Research Entity), not for people. It tells you what is in the kit, what to run, and where output goes. The kit is generic. It holds no personal data, accounts, or secrets. Everything is free and runs on this computer. Nothing here buys, signs up, sends, posts, or contacts anyone.

## Quick reference

Run all commands from the kit folder (the workspace path saved in your memory note `workspace-path`).

| Goal | Command | Output |
| --- | --- | --- |
| Check the tools, make the folders | `bash setup.sh` (add `--install-system` for curl or git) | printed summary |
| Prove it works | `bash doctor.sh` | `work/doctor-report.txt` |
| Start an experiment | `bash scripts/new-experiment.sh <slug>` | `experiments/<date>-<slug>/` |
| Run an experiment | `bash experiments/<folder>/run.sh <n>` | `experiments/<folder>/results/run-<n>.txt` |
| Start a report | `bash scripts/new-report.sh <slug>` | `reports/<date>-<slug>.md` |
| Check every URL in a report | `bash scripts/linkcheck.sh reports/<file>.md` | table plus a one-line summary |

## Folder layout

```
kit/
  setup.sh  doctor.sh  README.md
  templates/report.md                  the report, in the order of the report-findings skill
  experiments/_template/               experiment.md (question, hypothesis, commands, results, conclusion) and run.sh
  scripts/    new-experiment.sh   new-report.sh   linkcheck.sh
  experiments/<date>-<slug>/           one folder per run: experiment.md, run.sh, environment.txt, results/, scratch/
  reports/                             finished reports (git-ignored)
  work/                                scratch and doctor output (git-ignored)
```

## Running an experiment (skill `run-experiment`)

1. `bash scripts/new-experiment.sh <slug>`. It copies the template and records the OS and tool versions in `environment.txt`.
2. Fill in Question, Hypothesis, and **Wrong if** in `experiment.md` before you run anything.
3. Put the exact commands in `run.sh`, working inside `scratch/`. Use free tools, public or made-up inputs, and no accounts. Keep the data local.
4. Run it more than once when the result is surprising: `bash run.sh 1`, `bash run.sh 2`, `bash run.sh 3`. Each run is saved in `results/`.
5. Fill in Results (only numbers you measured), Conclusion, and What this does not show.
6. If a test would need a licence, an account, a card, or sending data anywhere, stop and ask the owner. See the `approval-gate` skill.

## Reporting (skill `report-findings`)

1. `bash scripts/new-report.sh <slug>` and fill in each section. Delete a section's placeholder text, not the heading. Keep the order: Conclusion, Evidence, Opinion, Options and tradeoffs, Costs, Could not verify, Next step.
2. Every factual claim has a title and a URL in the same paragraph. Open the page before you cite it.
3. Run `bash scripts/linkcheck.sh reports/<file>.md`. Fix or delete anything it marks `BROKEN`. `BLOCKED` means the site refuses automated requests (401, 403, 429): open it with the page fetch you have, and if you still cannot, move that claim to Could not verify. Paste the last line of the output (`LINKCHECK <date>: ...`) at the bottom of the report.
4. Link check proves a URL opens. It does not prove that the page says what you claim. You still read the page.

## The link checker

`bash scripts/linkcheck.sh <report.md> [--strict] [--timeout=15]` extracts every `http(s)` URL, de-duplicates them, and requests each one (HEAD first, then GET if the server refuses HEAD, following redirects). Exit code 0 means nothing is broken. `--strict` also fails on `BLOCKED`. It only reads public pages. It skips localhost and private-network addresses. A URL that itself contains parentheses is cut at the first one, so check those by hand.

## When something fails

- Run `bash doctor.sh` and read the first FAIL line. A `WARN` about the internet means the link checker could not be verified, not that it is broken.
- A missing `curl` or `git`: `bash setup.sh` prints the install line. Do not run `sudo` without the owner's yes.
- If a fix needs a paid account, an API key, a card, or a sign-in only the owner can do, stop and ask.
