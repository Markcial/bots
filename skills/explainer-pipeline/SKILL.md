---
name: explainer-pipeline
description: >-
  Use when the user writes /explainer <slug> or asks for a short explainer
  video: script, verified facts, Remotion visuals, narration, post texts, a PR
  to the user's explainers repo, approval, publishing, merge and cleanup.
---
# /explainer <slug> pipeline

The slug is the folder name (kebab-case). If the user keeps past explainers in a repo, read a few as examples (clone into a scratch folder, never over their work). Use Remotion for visuals. If other bots own motion or copy, delegate to them only after the user said yes. Nothing is published, sent, merged or deleted without the user's explicit OK.

1. **Frame it.** Topic, audience and length (16:9 about 60-70 s, plus a 9:16 Short). Present the full proposal first (see `task-identifiers`): hook, scene list, narration draft, X post and reply, LinkedIn post, YouTube title/description/tags in full. Get the OK on the plan.
2. **Script and facts.** Write the narration and `sources.md`. Verify every claim you can (run the code; for TypeScript `tsc --noEmit --strict`, outputs kept in `src-verify/`); cite only sources you opened. No phonetic spellings in narration text (voice-only spelling variants go in a separate `variants.json`; captions keep the real spelling).
3. **Visuals.** Remotion project (compositions per aspect ratio, `src/timings.json`, tokens/fonts), `render.sh` (`--concurrency=1`), `still.sh` (1280x720 thumbnail), a contact sheet to eyeball frames. Check for overflow, legibility and secrets on screen.
4. **Narration.** Generate voice sentence by sentence, verify with speech-to-text that the words match, build timings from word times, add a music bed with ducking (licence noted), master to about -14 LUFS.
5. **Post texts** in `posts.md` and, once final, `published/` (x-post, x-reply, linkedin, youtube-title, youtube-description, youtube-tags, short-title). Check X character counts; no angle brackets in YouTube descriptions.
6. **Review package.** Renders stay in the working folder (not the repo); write `STATUS.md`. Show the videos, thumbnail and full texts. Batch every requested change into one new render rather than exporting each tweak. **Stop for feedback.**
7. **PR to the explainers repo.** One PR per explainer: branch `explainer/<slug>`, one folder `<slug>/`, a row in the README table. **No renders** (no video, audio, images or files over 2 MB), no node_modules or venvs, no secrets. Open the PR and share the link. Do not merge yet.
8. **Approval, then publish** with `publish-video-everywhere`. Verify the links.
9. **Merge and clean up.** Merge the PR **once the explainer is live** and the user confirms, after updating the README row with links. Remove local working files **only after the user's explicit yes**, listing what would be deleted and its size first.
