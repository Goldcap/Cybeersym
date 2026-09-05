# Cybeersym Research Notebook

This is the durable research record (the ideation layer) for Cybeersym. Its distilled notes,
schemas, indexes, and reviews are **versioned here in the repo** for shareability; the **raw
ideation stays local and git-excluded** — source-conversation exports and correspondence
(`conversations/`) and bulk/licensed data (`data/`, regenerable from `data/wid/PROVENANCE.md`).
See `../.gitignore` for exactly what is held back.

## Working model

- Markdown is the canonical, human-readable source.
- `conversations/` preserves source discussions and extracted summaries.
- `notes/` holds durable concepts, people, models, and open questions.
- `artifacts/` holds generated figures, datasets, notebooks, and other outputs.
- `reviews/` records periodic synthesis and challenge.
- `bibliography/` tracks sources and reading notes.
- `indexes/` provides navigation across the notebook.
- `database/` contains rebuildable indexes and graph imports, never the sole copy of knowledge.
- `schemas/` defines metadata and graph conventions.

## Suggested workflow

1. Save a source conversation under `conversations/YYYY/YYYY-MM-DD-slug/`.
2. Create a summary from `conversations/TEMPLATE.md` and link the source material.
3. Promote durable claims, questions, people, or models into `notes/`.
4. Update `indexes/questions.md`, `indexes/timeline.md`, and `indexes/glossary.md`.
5. Record citations in `bibliography/bibliography.md`.
6. Run a review using `reviews/TEMPLATE.md`.
7. Rebuild derived database files from Markdown when needed.

## Naming and links

Use lowercase kebab-case filenames, ISO dates (`YYYY-MM-DD`), relative Markdown links, and stable IDs from the schemas. Mark uncertain material explicitly as `hypothesis`, `question`, or `needs-source`.

## Methodological foundations

- [Principles for a reproducible taxonomy of economic dynamics](notes/concepts/taxonomy-principles.md)
