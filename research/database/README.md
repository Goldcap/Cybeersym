# Rebuildable Database Plan

Markdown is canonical. Database files and Neo4j imports are derived and may be deleted and rebuilt.

## Phase 1: local index

Parse YAML front matter and Markdown links into a small SQLite database for full-text search, stable IDs, backlinks, tags, and provenance. Keep the database untracked under this directory.

Suggested tables: `records`, `links`, `tags`, `citations`, `claims`, `review_events`, and `build_runs`.

## Phase 2: Neo4j projection

Export normalized CSV files into `neo4j-import/`:

- `nodes.csv`: `id:ID`, `label:LABEL`, `title`, `status`, `source_path`
- `relationships.csv`: `:START_ID`, `:END_ID`, `:TYPE`, `evidence`, `source_path`

Candidate labels: `Conversation`, `Claim`, `Question`, `Hypothesis`, `Model`, `Dataset`, `Person`, `Paper`, `Concept`, `Experiment`, `Figure`, `Issue`, `Commit`, and `Review`.

Candidate relationships: `MENTIONS`, `SUPPORTS`, `CONTRADICTS`, `REFUTES`, `DERIVED_FROM`, `TESTED_BY`, `SUPERSEDES`, `RELATED_TO`, `IMPLEMENTED_IN`, and `REVIEWED_IN`.

## Build rules

1. Validate every Markdown record against the schemas.
2. Reject duplicate IDs and broken internal links.
3. Preserve source path, source hash, and extraction timestamp.
4. Treat inferred relationships as proposals until reviewed.
5. Generate databases and CSVs atomically; never edit them as canonical data.

