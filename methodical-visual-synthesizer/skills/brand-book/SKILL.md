---
name: brand-book
description: Create and keep a living brand book (palette with contrast pairs, type, logo and avatar rules, voice, motion rules, do and don't, references, change log) as a memory note plus a kit file, change it only after the owner's OK, and check every new deliverable against it.
---

# Brand book

The brand book is the one place where the owner's brand is written down, so every image, avatar, and video comes out consistent. It is a memory note `brand-book-<brand-slug>` (the summary you read at the start of each job) and, once the workspace is set up, the file `brand/<brand-slug>/brand.json` plus a readable `BRAND.md` in the kit folder (the copy the scripts read). The two must match. If they differ, say so and ask which one is right.

Use it when the owner wants to create or track a brand, when `diagnose-brief` finds no brand book, before any build that touches colour, type, logo, voice, or motion, and whenever a deliverable is checked.

## Create it (after an approved diagnosis)

1. Start from the approved diagnosis `diagnosis-<project-slug>` and the owner's existing assets. Do not invent a brand's values. If the owner already has colours, fonts, or a logo, those go in as they are.
2. Copy `brand/_template/` in the kit folder to `brand/<brand-slug>/` and fill `brand.json` and `BRAND.md`. Sections: palette with hex and a role for each colour; contrast pairs; type with licence and source; logo and avatar rules with the smallest size; voice and tone with words to use, words to avoid, and spoken respellings; motion rules (formats, pacing, captions, music, loudness); do and don't; references the owner likes and dislikes; change log.
3. Fonts must be open licence (SIL OFL or Apache-2.0) and installed on this computer. Record the licence, the source link, and the date you checked. A paid font needs the owner's yes with the cost stated first.
4. Run `node scripts/brand-check.mjs brand/<brand-slug>/brand.json`. Fix every FAIL before you show the book: a pair under its contrast limit (4.5 for text, 3 for large shapes and accent words), a font with no licence, an empty change log. If the owner's own colours fail a pair, do not change them. Report the pair and the ratio, and offer a text-safe variant (`primaryText`) as a proposal.
5. Save the memory note `brand-book-<brand-slug>` with the status line `draft`, the version, the date, and a short summary: colours with hex, fonts, the smallest avatar size, the tone in one line, and the path of `brand.json`. Do not put contact details, accounts, or secrets in it.
6. Send the owner the book, with the contrast results and the weak spots. Ask for an OK or changes. Silence is not approval. On an explicit OK, set `status` to `approved <date>` in both places and add the first change log line.

## Keep it current

- **Only change it after the owner's OK.** Describe the change (what, why, which deliverables it affects), ask, and wait. On a yes, edit `brand.json` and `BRAND.md`, bump `version`, set `updated`, add a change log line with the date, the change, and `approvedBy: owner`, and update the memory note. A no or silence leaves the book as it is.
- **Learn from feedback.** When the owner reacts to a deliverable ("too dry", "this blue is off", "too busy"), write the reaction down as a proposed do or don't, and ask whether it becomes part of the book. Do not add it on your own.
- **Track what exists.** Keep a short list of the deliverables made under each version in the memory note, so a later change shows what it touches.
- **Monthly.** The tool and licence check also re-reads the fonts listed in the book.

## Check every deliverable against it

Before you show or hand over any image, avatar, or video, run the brand check in the skill `check-and-handoff`:

1. `node scripts/brand-check.mjs` for the palette pairs, the licences, and whether the video config uses the brand book (`"brand": "brand/<brand-slug>/brand.json"` makes the palette, fonts, and avatar colours come from the book).
2. Look at the file against each rule in the book: colours used, type, logo size and clear space, avatar legibility at its smallest size, tone of the copy, motion pacing, caption rules.
3. Report each deviation as a line: the rule, what the file does, and a proposed fix. Fix what is yours to fix. If the file breaks a rule because the owner asked for it, say so and ask whether the book should change. Never edit the book to make a deliverable pass.

## Do not

- Change the book, add a colour, or swap a font without the owner's explicit yes to that change.
- Copy another brand's identity, or a living person's likeness, into the book.
- Put the owner's private files, logos, or contact details in the public repo. They stay in the workspace's `assets/` folder.
- Say a deliverable follows the brand book when you did not run the check and look at it.
