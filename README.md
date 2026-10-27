# bots
Versioned source of my Grok Bot templates.

Templates for Grok bots: description, skills, seed memories, routines, and a getting-started note. `catalog.json` is the machine-readable list a coordinator bot reads when it picks or recommends a template. Text here is generic. It holds no personal memories, contact details, or secrets.

## Use a template

1. Copy `_template/` to a new folder. The folder name is the kebab-case form of the bot's three-word title (buzzword, domain, role), for example `distributed-workforce-router`.
2. Replace every placeholder in `profile.md`, `getting-started.md`, `memories.md`, `routines.md`, and `skills/`.
3. Add an object to `catalog.json` and a row to the catalog table below. Leave `xai_template_url` null until launch.
4. Keep the stage at `sketch` until that stage's exit criteria are met.
5. On x.ai, create the bot from `profile.md`, add each skill, paste `memories.md` as seed knowledge, and schedule every routine. Put the avatar and the motion presentation video in `media/` during `prepare`.
6. Publish once, at `launch`, and only with that identity and motion video. Then set `xai_template_url`.

Planned names in the table have no folder. Do not assign work to them and do not add them to `catalog.json`.

## Pipeline

A bot moves one way: sketch, prepare, ready, launch. It launches only once, when its template is published on x.ai with its identity (avatar) and a motion presentation video.

| Stage | What is true | Exit criteria |
| --- | --- | --- |
| sketch | The template text is in this repo. Nothing is published. | Profile, getting-started, skills, memories, and routines describe one bot and agree with each other. |
| prepare | The text is stable. Avatar and motion presentation video are being made. | Both files are in `media/` and have been reviewed. |
| ready | Template, avatar, and motion video are finished. Still unpublished. | Someone can publish without writing new copy. |
| launch | Published on x.ai with that avatar and motion video. | `xai_template_url` is set. This happens once. |

`catalog.json` fields: `id`, `title`, `stage`, `summary`, `folder`, `xai_template_url` (or null), `chains_with` (ids of templates that follow this one in a known sequence).

## Catalog

| Name | Stage | One-liner | x.ai |
| --- | --- | --- | --- |
| Distributed Workforce Router | sketch | Does a task itself, recommends a catalog template, or proposes a new bot, and asks what the other bot needs before assigning work. Nothing is sent, published, purchased, or contacted without an explicit yes. | not published yet |
| Perpetual Learning Machine | sketch | Reads X likes, bookmarks, and follow topics, studies them, and prepares a cited digest for the next day. Never likes, replies, follows, or posts. | not published yet |
| Superconnected Research Entity | planned | Research and experiments. No folder yet. | not published yet |
| Designer bot (title not set) | planned | Careful sketch. A mandatory diagnosis phase comes before any design. No folder yet. | not published yet |
| Programmer bot (title not set) | planned | Careful sketch. A mandatory diagnosis phase comes before any code change. No folder yet. | not published yet |
| Perpetual Narrative Weaver | planned | Scripts and storyboards. First step of the creative chain. No folder yet. | not published yet |
| Distributed Character Sculptor | planned | Characters for those scripts. No folder yet. | not published yet |
| Continuous Motion Composer | planned | Motion design for those characters. No folder yet. | not published yet |
| Hyperconnected Audio Producer | planned | Audio and voice for that motion. No folder yet. | not published yet |
| Animation bot (name TBD) | planned | Turns the chain into a finished piece. Name not chosen. No folder yet. | not published yet |

The creative block, once those templates exist, runs in this order: Perpetual Narrative Weaver, Distributed Character Sculptor, Continuous Motion Composer, Hyperconnected Audio Producer, then the animation bot. Each hands its output to the next. They are not in `catalog.json` until they have folders.
