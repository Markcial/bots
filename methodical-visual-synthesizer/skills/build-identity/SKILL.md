---
name: build-identity
description: Build the chosen identity (avatar set, palette, type, simple logo) from the brand book, with free tools and open-licence fonts, and export it at the right sizes.
---

# Build the identity

Use after the user has chosen a direction from an approved diagnosis. Work in the kit folder saved in the memory note `workspace-path` (if the note is missing, run the skill `setup-workspace` first).

## Steps

1. **Brand book first.** If the memory note `brand-book-<brand-slug>` exists, read it and build from it. If it does not, create a draft with the skill `brand-book` and get the owner's OK on it before you build. Tokens (palette with hex and roles, type with its licence, spacing, corner radius) live in the book, and nothing in the build hard-codes a colour.
2. Build the master in code at 1024 by 1024 with `node scripts/still.mjs --brand=brand/<brand-slug>/brand.json` (see the kit README for the motifs, and `src/Avatar.tsx` to add one). Keep one object, one main colour, and no text inside an avatar. Choose a motif that says what the brand does: a drawing tool for a drawing brand, not a ruler.
3. **Show a contact sheet before you animate anything.** One image with the palette and its hex values and roles, the type specimens, the logo and avatar at several sizes, and the rules that make it consistent. Stills first, motion after the owner has seen them.
4. **Small sizes.** `still.mjs` renders 1024, 512, 256, 128, 48, and 32 pixels natively (it does not shrink the big one) and simplifies the motif at 64 and below. Look at `-sheet.png` and `-check32.png`. If the shape stops reading at 48 and 32, remove detail until one bright element is left. Parts that hide behind other parts can read as the wrong shape, so check the mid-sizes too, not only the first and last.
5. Check the master against the diagnosis (audience, existing assets, constraints) and against the brand book (skill `check-and-handoff`).
6. Write a short note with the tokens, the fonts and their licences, the file names, and the commands that re-make each file. Add the tools and fonts, with licence links and the date checked, to the memory note `tool-notes`.
7. If the owner has a style reference (a picture or a past piece), keep it in `assets/` and say which of its features you matched. If a generated image is used, say so, and say what it cost.
8. Paid image generation is optional and never the default. If a paid step would help (a generator, stock, a paid font), say what it costs and which account it needs, and wait for a yes. Do not spend credits otherwise.
9. Thumbnails, covers, and banners are separate pieces. Design each at its real size (for example a 1280 by 720 thumbnail) and look at it small: the main word must be readable at the size of a feed card.

## Do not

- Use a font or an asset without recording its licence. Prefer fonts under the SIL Open Font License or Apache-2.0, and write the licence in a small `FONTS-LICENSE` note next to the files.
- Ship an avatar that is only readable at full size.
- Redraw the owner's logo by hand. Use their original file, or a plain wordmark.
- Add a colour, font, or rule that is not in the brand book without asking the owner (skill `brand-book`).
- Overwrite the user's existing files. Save new files under new names.
