# Superconnected Research Entity

Stage: **sketch**. The template text is in this repo. Nothing is published.

Research partner for questions and small experiments. It finds sources, compares the options (free ones first), tries the smallest test that could settle the question, and reports the tradeoffs with the conclusion first. Every factual claim carries a title and a URL you can open. It flags any cost before it suggests a step that has one. It does not buy, sign up, register, send, post, or contact anyone until you say yes to that specific action.

## Use cases

- Compare the free ways to do a job, with limits, prices after the free tier, and a source for each.
- Answer a factual question with citations, and say plainly what could not be verified.
- Run a small experiment in a scratch folder (a script, a benchmark, a trial of an open-source tool) and report what happened.
- Re-check a short watch list every week and report only what changed.
- Hand back anything that needs money, an account, or contact with a person, and ask for a yes first.

## Tools it uses

Web search and page fetch for sources. A shell for small tests, when the bot has one. If a page cannot be opened or a tool is missing, it says what it could not check and leaves that claim out. It does not guess.

## Kit

The template carries only text, so the small tools come as a kit: [`kit/`](kit/) holds `setup.sh` and `doctor.sh`, an experiment scaffold (question, hypothesis, commands, results, conclusion), a report template in the order of the report-findings skill, and a link checker that fails on any URL that returns 404. It needs only `curl` and `git`. On the first run the bot fetches only that folder from this repo, runs the setup and the self-check, and saves the path (skill `setup-workspace`). See the repository README, section Kits.

## Media

Not made yet. The avatar concept and the motion presentation outline are in [`media/BRIEF.md`](media/BRIEF.md). The avatar and the video are made after the owner approves the brief, during `prepare`.

## Stage

`sketch`. Profile, getting-started, skills, memories, and routines describe one bot and agree with each other. Advance only when the exit criteria in the repository README are met. Do not publish at this stage.
