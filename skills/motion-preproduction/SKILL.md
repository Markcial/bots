---
name: motion-preproduction
description: >-
  Use when the user asks for a motion, animation or video (new one-off job or a
  known format) before any voice, frames or render are produced: builds the
  plan, mood, storyboard, beats and material list and gets the user's OK first.
---
# Motion preproduction

Nothing is produced (voice, frames, renders, paid generations) until the user approves this preproduction.

## 1. Classify the job
- **Known format** (an existing series with defined mood, template and plan, e.g. a recurring short-video format): reuse its mood, visual template and plan skeleton. Still work the **script** and the **storyboard** for this piece. Skip steps 3 and 5 unless the user asks for a change of style.
- **New / specific job** (no defined format, or the user did not specify the style): do every step below.
- If the user already gave mood, references or a script, use them and only fill the gaps.

## 2. Plan
Goal, audience, duration, platforms and aspect ratios, deadline, call to action, constraints (brand, rights, budget, free-tier limits).

## 3. Mood (new jobs)
3-6 references: real public-domain or licensed images, or properly generated images. Note palette, typography, motion style, music and voice tone. Never crude sketches or block figures; if a reference is missing use an obvious placeholder box labeled "PLACEHOLDER: X goes here".

## 4. Script and beats
Hook, development and payoff split into beats; each beat has its line of narration or on-screen text, an estimated duration and the emotional intent.

## 5. Storyboard
4-8 shots (more for long pieces), each with: visual description, on-screen text, voice line, transition or motion, estimated duration, and the reference image or a PLACEHOLDER box. Run the `storyboard-plausibility-check` skill before showing panels.

## 6. Material list
Everything the production needs: images and their source and license, footage, music, SFX, voice (engine and voice), fonts, data, characters, and which agent or tool produces each item. Flag anything that costs money with its price.

## 7. Present and wait
Show plan, mood, script with beats, storyboard and material list in one message. Wait for the user's explicit OK or changes. After the OK, voice and frames start in parallel and the user gets them together for a single review.

## 8. Quality before delivery
Each producer checks its own part before handing it over. Then the whole piece gets two reviews: a full-context check against brief, approved script and storyboard (consistency between parts), and a fresh-eyes check with no context, as a viewer in the feed would see it (clarity, hook, anything odd).
