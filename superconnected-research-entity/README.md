# Superconnected Research Entity

Stage: **prepare**. The template text is in this repo. Nothing is published.

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

Identity and motion presentation live in [`media/`](media/). The avatars were approved by the owner on 2026-10-28. The brief they were made from is [`media/BRIEF.md`](media/BRIEF.md).

| Asset | Path |
| --- | --- |
| Avatar (1024 / 512 / 256 / 128 / 48 / 32) | [`media/avatar-1024.png`](media/avatar-1024.png) (and siblings) |
| Motion video 16:9 | [`media/sre-16x9.mp4`](media/sre-16x9.mp4) |
| Motion video 1:1 | [`media/sre-1x1.mp4`](media/sre-1x1.mp4) |
| Sample frame | [`media/sample-frame.png`](media/sample-frame.png) |

After merge to `main`, raw URLs look like `https://raw.githubusercontent.com/Markcial/bots/main/superconnected-research-entity/media/avatar-1024.png`. Bed music licence: [`LICENSE-music.md`](../LICENSE-music.md).

## Stage

`prepare`. Copy is done. The avatar and the motion presentation video are made and the avatars are approved, but the template text still needs the owner's final review before `ready`. No template link yet (`xai_template_url` stays null until `launch`).
