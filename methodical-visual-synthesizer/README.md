# Methodical Visual Synthesizer

Stage: **launch**. The Grok Bot template is published: [open the template](https://x.ai/bot/g7lZEZtIgQspQ4uQvkXhf). The avatars were approved by the owner on 2026-10-28. The title is a proposal. Alternatives are listed in [`media/BRIEF.md`](media/BRIEF.md).

Careful designer that helps you create and keep track of your brand, then designs on top of it: avatars, palettes, type, logos, social visuals, motion videos, and explainers. It keeps a living brand book that it only changes with your OK and checks every new piece against. A mandatory diagnosis comes before any design. It asks about the brief, the audience, your existing assets, the constraints, and your references, writes the diagnosis down, and waits for your OK. Only then does it propose a few directions and build one. It works in code and free tools first (Remotion for motion), checks its own frames before it shows them, and flags any cost before suggesting it. It does not publish, send, purchase, or spend credits without your explicit yes.

## Use cases

- Start a brand book (palette with contrast pairs, type with licences, logo and avatar rules, voice, motion rules, do and don't, change log), or record the one you already have and flag its gaps.
- Check a new image, avatar, or video against the brand book and list each deviation.
- Create an avatar set and a small identity (colour, type, motif) for a project, bot, or channel.
- Turn an existing logo and a few references into a consistent kit.
- Make a short motion presentation or explainer in Remotion from an approved storyboard, with matching captions and a measured loudness.
- Review an existing identity and write down what to keep and what to fix, without redrawing it.
- Hand back a request that has no brief, and run the diagnosis first.

## Diagnosis first

No design work starts until you have said OK to the written diagnosis. That means no sketches, no generated images, no palettes, and no video. The diagnosis covers five things: the brief, the audience, the assets you already have, the constraints, and the references. If the scope changes later, it runs the diagnosis again for the change.

## Brand book

The bot keeps one living brand book per brand: a memory note `brand-book-<brand-slug>` plus a kit file `brand/<brand-slug>/brand.json` and a readable `BRAND.md` (start from [`kit/brand/_template/`](kit/brand/_template/)). It holds the palette with hex, roles and contrast pairs, type with licences, logo and avatar rules with the smallest size, voice and tone, motion rules, do and don't, references, and a dated change log. It changes only after your explicit yes. A video config with `"brand": "brand/<brand-slug>/brand.json"` takes its palette, fonts, and avatar colours from the book, and `node scripts/brand-check.mjs` measures the contrast of the palette pairs, checks the font licences and the change log, and reports configs that drift from the book. The skill is `brand-book`. Your brand files are your private data: they stay in your workspace and never go back to the public repo.

## Lessons

[`LESSONS.md`](LESSONS.md) lists what earlier design jobs taught (voice fixes in the voice text only, loudness on the final file, small-size legibility, overlaps, tokens, speed on shared machines). The skills `build-identity`, `build-motion`, and `check-and-handoff` apply them.

## Kit

The template carries only text, so the tools come as a kit: [`kit/`](kit/) holds a free local harness for motion and images (a Remotion project with one config-driven 16:9 video and a code-drawn avatar, free narration with a silent fallback, a built-in music bed with ducking, a brand book template with a contrast and licence check, a video QA script for size and loudness, `setup.sh` and `doctor.sh`). On the first run the bot fetches only that folder from this repo, runs the setup and the self-check, and saves the path (skill `setup-workspace`). See the repository README, section Kits.

## Media

Identity and motion presentation live in [`media/`](media/). The avatars were approved by the owner on 2026-10-28. The brief they were made from is [`media/BRIEF.md`](media/BRIEF.md).

| Asset | Path |
| --- | --- |
| Avatar (1024 / 512 / 256 / 128 / 48 / 32) | [`media/avatar-1024.png`](media/avatar-1024.png) (and siblings) |
| Motion video 16:9 | [`media/mvs-16x9.mp4`](media/mvs-16x9.mp4) |
| Motion video 1:1 | [`media/mvs-1x1.mp4`](media/mvs-1x1.mp4) |
| Sample frame | [`media/sample-frame.png`](media/sample-frame.png) |

After merge to `main`, raw URLs look like `https://raw.githubusercontent.com/Markcial/bots/main/methodical-visual-synthesizer/media/avatar-1024.png`. Bed music licence: [`LICENSE-music.md`](../LICENSE-music.md).

## Stage

`launch`. The template is published once, with its avatar and motion presentation video, at https://x.ai/bot/g7lZEZtIgQspQ4uQvkXhf. `xai_template_url` in `catalog.json` holds that link.
