# Research Record Schema

Every durable note should provide YAML front matter with:

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | Stable, unique lowercase identifier. |
| `status` | yes | `captured`, `developing`, `hypothesis`, `supported`, `disputed`, `refuted`, `superseded`, or `archived`. |
| `tags` | yes | Lowercase topical labels. |
| `date` | for events | ISO date of the conversation, review, or experiment. |
| `source` | when applicable | Relative path or durable external identifier. |

## Provenance fields

Where useful, add `derived_from`, `reviewed_in`, `supersedes`, `authors`, `created`, and `updated`. Claims should distinguish quotation, paraphrase, inference, and original hypothesis.

## Link semantics

Ordinary Markdown links remain readable. A future builder may optionally parse typed links written as `relationship: target-id`, but typed relationships must cite the note or evidence that justifies them.

