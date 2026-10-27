# Consult the catalog

Use when you are about to recommend a template or claim that none exists.

## Steps

1. Read `catalog.json` in this repository. Ignore README rows marked planned; they have no folder.
2. Match the job to `summary` and `title`. When two entries fit, prefer the later pipeline stage: launch, then ready, then prepare, then sketch.
3. Report `id`, `title`, `stage`, `folder`, and `xai_template_url`. If the URL is null, say "not published yet".
4. Mention `chains_with` when the job is a sequence those ids already name.
5. If nothing fits, say so. Do not stretch a template past its summary.

## Do not

- Invent catalog entries.
- Describe a null URL as a live x.ai template.
