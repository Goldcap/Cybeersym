# Graph Model

## Identity

Each node is keyed by the stable `id` in front matter. The source Markdown path is provenance, not identity.

## Node labels

`Conversation`, `Claim`, `Question`, `Hypothesis`, `Model`, `Dataset`, `Person`, `Paper`, `Concept`, `Experiment`, `Artifact`, and `Review`.

## Relationship policy

Relationships must be directional, typed, and traceable to a source record. Store `source_path`, `evidence`, `confidence`, `created_at`, and `review_status` when the edge is inferred rather than explicit.

## Validation invariants

- IDs are globally unique.
- Every relationship endpoint exists.
- Every derived record links to at least one source.
- Refuted and superseded material remains queryable.
- Rebuilding produces the same graph for unchanged sources.

