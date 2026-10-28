---
name: propose-directions
description: After an approved diagnosis, offer two or three directions, each tied to the diagnosis, and let the user choose before building.
---

# Propose directions

Use only when the memory note `diagnosis-<project-slug>` says `approved`. If it does not, run the diagnose-brief skill first.

## Steps

1. Offer two or three directions at most. Few, careful options beat many rough ones.
2. For each direction give a name, the colour and the motif in a sentence, the type, and the line in the diagnosis it answers.
3. Show each as a simple frame or sketch made in code, not as a finished piece. If a brand book exists, every direction stays inside it, and any step outside it is marked as a proposed change to the book (skill `brand-book`), which needs the owner's OK. If there is no book, the chosen direction becomes the draft of one.
4. Say which one you would pick and why, and mark that as your opinion.
5. Say what each direction would cost to build, and flag anything that needs money.
6. Ask the user to choose one or to ask for a change. Stop.

## Do not

- Offer a direction that ignores a constraint or an asset that must stay.
- Copy another brand's identity or a living person's likeness.
- Start the full build before the user chooses.
