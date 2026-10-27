---
name: consult-catalog
description: Read the shared bots catalog JSON and recommend a matching template, or say none fits.
---

# Consult the catalog

Use when you are about to recommend a template or claim that none exists.

## Steps

1. Fetch `https://raw.githubusercontent.com/Markcial/bots/main/catalog.json`. If the fetch fails, ask the user for an updated catalog URL or a paste of the JSON. Do not invent entries. A catalog they already pasted into seed memory is valid until they replace it.
2. Ignore README rows marked planned. They have no folder. Recommend only JSON objects whose `folder` is a non-empty string.
3. Match the job to `summary` and `title`. When two entries fit, prefer the later pipeline stage: launch, then ready, then prepare, then sketch.
4. Report `id`, `title`, `stage`, `folder`, and `xai_template_url`. If the URL is null, say "not published yet".
5. Mention `chains_with` when the job is a sequence those ids already name.
6. If nothing fits, say so. Do not stretch a template past its summary.

## Do not

- Invent catalog entries.
- Describe a null URL as a live template.
- Assume this repository is on the local filesystem.
