# bots
Versioned source of my Grok Bot templates.

Templates for Grok bots: description, skills, seed memories, routines, and a getting-started note. `catalog.json` is the machine-readable list a coordinator bot reads when it picks or recommends a template. Installed bots fetch it at `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json`. If that fetch fails, they ask for a paste or another URL. They do not invent entries. Text here is generic. It holds no personal memories, contact details, or secrets.

## Use a template

1. Copy `_template/` to a new folder. The folder name is the kebab-case form of the bot's three-word title (buzzword, domain, role), for example `distributed-workforce-router`.
2. Replace every placeholder in `profile.md`, `getting-started.md`, `memories.md`, `routines.md`, and `skills/`.
3. Add an object to `catalog.json` and a row to the catalog table below. Leave `xai_template_url` null until launch.
4. Keep the stage at `sketch` until that stage's exit criteria are met.
5. This repo is the source of truth for the words. To install a shared template in Grok Bot, open `grokbot://app/v1/bot-template?id=<share id>`. How a share id is created is confirmed at launch. Until then, create the bot from `profile.md`, add each skill with its YAML frontmatter, paste `memories.md` as seed knowledge, and schedule every routine with its 5-field cron in the user's timezone. The routine delivers in that chat. Put the avatar and the motion presentation video in `media/` during `prepare`.
6. At `launch`, publish the Grok Bot template once, with that avatar and motion video. The result is a shareable `grokbot://app/v1/bot-template?id=<share id>` link. Set `xai_template_url` to that link. A bot does not create another bot. It hands the user a draft and, when they have a share id, that same link.

Planned names in the table have no folder. Do not assign work to them and do not add them to `catalog.json`.

## Kits

A Grok Bot template carries only prose: the profile, seed memories, skill text, routines, and a getting-started note. It cannot carry files or scripts. So a bot that needs tools gets a **kit**: a `kit/` folder inside its template folder, in this public repo (MIT).

1. **Template plus kit.** The template installs the bot. The kit holds the harness the bot needs on its own computer: `setup.sh` (checks for or installs the toolchain and prints what is missing), `doctor.sh` (a self-check that proves the toolchain works), a `README.md` written for the bot, and whatever scripts or starter projects the job needs.
2. **First run.** Step 1 of every kit bot's getting-started note is "set up your workspace". The skill `setup-workspace` makes the bot fetch only its own `<folder>/kit` from this repo (a sparse git checkout, or a tarball of `main`), copy it to a workspace folder, run `setup.sh` and then `doctor.sh`, show the owner the test output, and save the folder path in the memory note `workspace-path`. It asks before it installs anything, and it stops if a step needs a paid account.
3. **Rules.** A kit is generic: no personal data, no accounts, no secrets, no owner files. It is free to run by default. Anything paid is optional, needs the owner's explicit yes with the cost stated first, and is never the default path. Every third-party tool and its licence is listed in the kit (`LICENSES.md`). `setup.sh` is idempotent. Nothing in a kit publishes, sends, buys, or contacts anyone.
4. **Updating.** Kits are versioned with the repo. The bot records the commit it fetched in `workspace-path`. To update, it fetches into a new folder and compares, so it never overwrites the owner's work.
5. **Adding a kit to a bot.** Create `<folder>/kit/` with `setup.sh`, `doctor.sh`, and `README.md`. Add a `setup-workspace` skill (copy one from an existing kit bot and change the folder name), make setting up step 1 of `getting-started.md`, and mention the workspace in `profile.md` and `memories.md`. Test from a clean copy in a temporary folder: `setup.sh` then `doctor.sh` must pass.

| Bot | Kit | What it holds |
| --- | --- | --- |
| Methodical Visual Synthesizer | [`methodical-visual-synthesizer/kit`](methodical-visual-synthesizer/kit) | Remotion project (16:9 video from one JSON config, code-drawn avatar still), free narration with silent fallback, built-in music bed with ducking, brand book template with contrast and licence check, video QA script (size, loudness), doctor clip and still |
| Superconnected Research Entity | [`superconnected-research-entity/kit`](superconnected-research-entity/kit) | Experiment scaffold, report template, link checker, doctor |

## Pipeline

A bot moves one way: sketch, prepare, ready, launch. It launches only once, by publishing the Grok Bot template: a shareable `grokbot://app/v1/bot-template?id=<share id>` link, together with its identity (avatar) and a motion presentation video.

| Stage | What is true | Exit criteria |
| --- | --- | --- |
| sketch | The template text is in this repo. Nothing is published. | Profile, getting-started, skills, memories, and routines describe one bot and agree with each other. |
| prepare | The text is stable. Avatar and motion presentation video are being made. | Both files are in `media/` and have been reviewed. |
| ready | Template, avatar, and motion video are finished. Still unpublished. | Someone can publish without writing new copy. |
| launch | The Grok Bot template is published as a shareable `grokbot://app/v1/bot-template?id=<share id>` link, with that avatar and motion video. | `xai_template_url` is set to that link. This happens once. |

`catalog.json` fields: `id`, `title`, `stage`, `summary`, `folder`, `xai_template_url` (or null), `chains_with` (ids of templates that follow this one in a known sequence).

## Catalog

| Name | Stage | One-liner | Template |
| --- | --- | --- | --- |
| Distributed Workforce Router | launch | Does a task itself, recommends a catalog template, or proposes a new bot, and asks what the other bot needs before assigning work. Nothing is sent, published, purchased, or contacted without an explicit yes. | [Open template](https://x.ai/bot/79dGJd9FqqNXZZ773YhX8) |
| Perpetual Learning Machine | launch | Reads X likes, bookmarks, and follow topics, studies them, and prepares a cited digest for the next day. Never likes, replies, follows, or posts. | [Open template](https://x.ai/bot/PsppjjXTB3Ggf0YmCTlNO) |
| Superconnected Research Entity | sketch | Researches a question, compares the options (free first), runs small experiments, and reports the tradeoffs with a cited source for every claim. Flags any cost. Buys, signs up, sends, or contacts no one without an explicit yes. | not published yet |
| Methodical Visual Synthesizer | sketch | Helps you create and track your brand (a living brand book) and designs on top of it: avatars, images, social visuals, motion videos, explainers. A mandatory diagnosis (brief, audience, existing assets, constraints, references) and your OK come before any design. Free tools and code first. Title is a proposal. | not published yet |
| Programmer bot (title not set) | planned | Careful sketch. A mandatory diagnosis phase comes before any code change. No folder yet. | not published yet |
| Perpetual Narrative Weaver | planned | Scripts and storyboards. First step of the creative chain. No folder yet. | not published yet |
| Distributed Character Sculptor | planned | Characters for those scripts. No folder yet. | not published yet |
| Continuous Motion Composer | planned | Motion design for those characters. No folder yet. | not published yet |
| Hyperconnected Audio Producer | planned | Audio and voice for that motion. No folder yet. | not published yet |
| Animation bot (name TBD) | planned | Turns the chain into a finished piece. Name not chosen. No folder yet. | not published yet |

The creative block, once those templates exist, runs in this order: Perpetual Narrative Weaver, Distributed Character Sculptor, Continuous Motion Composer, Hyperconnected Audio Producer, then the animation bot. Each hands its output to the next. They are not in `catalog.json` until they have folders.
