# Collaboration Protocol

> **Research proposes. Tickets authorize crossing the boundary. The repository tests.
> Evidence decides. The notebook remembers the path — including the failures.**

The cross-system layer above the notebook's node/graph schemas: **who does what, where truth
lives, and how an idea becomes validated work.** The other schemas (`graph-model.md`,
`research-record.schema.md`) formalize the notebook's *internals*; this formalizes its
*boundaries* — its relationship to the engineering repo, to Linear, to `memory/`, and to the
several minds (human and model) working the problem.

*Status: v0.1 consensus (2026-08-01). Drafted by Claude Code; amended by GPT (typed support,
narrow-promotion invariant, hash-based provenance, the memory/evidence boundary). Open for
continued review on the same terms as code.*

## Three layers, one direction of flow

Knowledge lives in three systems. They are not competitors; they are **stages**.

1. **`research/` — ideation (this notebook).** Thoughts, ideas, inspirations, source
   conversations, concepts, people, open questions. *Upstream.* Speculative by default, every
   record status-marked. Where things **incubate**. The distilled notes, schemas, indexes, and
   reviews are **versioned in the repo** (public, for shareability); the **raw ideation stays
   local & git-excluded** — source-conversation exports and correspondence (`conversations/`) and
   bulk/licensed data (`data/`), which are regenerable or private and must not be published.
2. **`docs/` + code — compound engineering (the repo).** The operational record of work done:
   `docs/plans/`, `docs/solutions/` learnings, `CHANGELOG`, `HANDOFF`, `THESIS`, committed code
   and artifacts. *Downstream, and the referee* — real data decides here.
3. **`memory/` — collaboration continuity (Claude Code).** Preferences, procedures, recurring
   hazards, collaboration mechanics. *How* the work runs — not *what* it concluded.

**Authority flows one way:** `research/` may inspire and reference, but must not *shadow*
canonical conclusions in `docs/`. Findings return upstream only as new questions, hypotheses,
or links — never as duplicate validated records.

## The pull-over (crossing the boundary)

Exploration is free inside the notebook; **promotion is the narrow event where an idea crosses
into the project's canonical record.** Cheap conjectures live and die in `research/` without
ceremony — the ticket marks *commitment*, not curiosity.

```
captured idea
  → investigated in research/                      (free; no ticket)
  → selected for implementation or formal validation
  → promoted via a Linear ticket (CYB-NN)          ← the boundary object
  → resolved in code / docs / artifacts
  → linked forward from research/
```

**Promotion invariant (enforceable):**

> No research idea may alter the project's canonical implementation, plans, or validated
> conclusions without a promotion event linked to a Linear ticket.

This is *observable* — crossing into the repo is a git event — where "the moment an idea becomes
work" was not. It is already mechanizable via the standing convention that commits touching
`src/` or `docs/` reference their `CYB-NN`.

## Typed support (how a Claim earns `supported`)

`supported` is **not one gate**. A Claim carries a **support profile** naming *how* it is
supported; the hard repo-gate applies to the class that needs it, not to every true proposition.

```yaml
status: supported
support_type: empirical | computational | mathematical | documentary | mixed
evidence:
  - type:             # one of the above, per strand
    path_or_citation:
    commit:           # MANDATORY for computational / repo-validated empirical
    artifact_hash:
    reviewed_in:
```

- **computational** and repo-validated **empirical** — a `docs/solutions/` entry **and** a
  commit are **mandatory**. No notebook-only declaration can satisfy this class. (This is the
  original hard boundary, now scoped to where it belongs.)
- **mathematical / documentary** — derivation, primary literature, historical evidence, or
  conceptual clarification that produces no code — supported by citation or derivation; no
  commit required.
- **mixed** inherits the **strictest** applicable gate: any computational or repo-empirical
  strand still carries its commit. `support_type` is a *summary of the evidence list*, not a
  declaration that can weaken it — the evidence list is canonical (derived, not asserted).
- **negative experiments are support too**: they justify `refuted` / `disputed` under the same
  typed evidence — a computational refutation still cites its commit.

## Immutable provenance (frozen exports + a manifest)

Conversation exports under `research/conversations/` are **immutable provenance** — they record
what was said *then*. A convention is not enough; each frozen export carries a **manifest** so
that silent rewriting is *detectable*:

```yaml
# provenance.yaml  (immutable, lives beside the frozen export)
source_file: source-package.zip
sha256: <hash of the as-received bytes>
captured_at: <ISO timestamp>
origin: <the conversation / tool / model>
immutable: true
```

The `sha256` is taken over the **as-received bytes** (do not re-zip — archive formats are not
byte-reproducible; treat the delivered artifact as the frozen blob; per-file hashes of the
extracted set may be added). The evolving forward-links live in a **separate adjacent file** so
the export and its manifest stay untouched:

```yaml
# links.yaml  (mutable, adjacent)
derived_notes: []
canonical_successors: []   # e.g. docs/outreach/bifurcation-note.md
```

## The memory boundary

`memory/` may describe preferences, procedures, recurring hazards, and collaboration mechanics.
It **must never serve as evidence for a research claim, nor authorize a boundary crossing.**
Memory can tell an agent *where to look* or *how to work*; it cannot establish *what is true*
(only the repo can) and it cannot *promote* an idea (only a Linear ticket can). Recalled memory
reflects what was true when written and is verified against source, never cited as an authority.

## Roles and handoff

| Agent | Role | Primary home |
|---|---|---|
| **Andy** | decides, owns, sends, sets direction | everywhere; final authority |
| **GPT (ChatGPT)** | ideation, scoping, the broad program (taxonomy), literature, first-draft outreach | `research/` |
| **Claude Desktop** | spec author — turns a matured idea into a resolved ticket | Linear |
| **Claude Code** | executes, validates, referees; figures, docs, git | repo (`docs/`, `src/`) |

**Bus and contract:** **Linear** is the exchange bus (specs in, verdicts out — on completion,
post commit hash + regression-anchor pass/fail). **`WORKFLOW.txt`** is the review contract (one
PR = one coherent claim-change set; read the *diff*, not a pasted copy; typed comments:
CORRECTNESS / RIGOR / CLARITY / STYLE / OPEN QUESTION). Every agent's framing — including
Claude Code's and GPT's — gets the same skeptical measurement; refutation is surfaced on the
bus, never silently overridden.

## Node types, pinned to the flow

| Node | Is | Home of record |
|---|---|---|
| `Conversation` | a model/Andy session (an export) | `research/conversations/` (immutable + manifest) |
| `Concept` / `Person` / `Paper` | durable idea, thinker, source | `research/notes/`, `bibliography/` |
| `Question` / `Hypothesis` | a matured idea → **Linear ticket** on promotion | `research/` ↔ Linear |
| `Experiment` | a ticket executed | `docs/plans/` + `docs/solutions/` + commit |
| `Review` | referee pass / `review-ledger` / code-review | `docs/` + the ledger |
| `Model` | an SFC / pricer / mechanism | `src/` + `docs/` |
| `Artifact` | figure, PDF, dataset | committed path |

## Boundary rules (invariants), collected

- **Authority is one-way:** `research/` inspires and references; it never shadows canonical
  `docs/` conclusions.
- **Archival sources are frozen + hashed:** exports are immutable, carry a `sha256` manifest,
  and evolve their links only in an adjacent file.
- **Derived notes link, they don't copy:** cite the canonical path; never hold a second,
  drifting copy.
- **Typed support:** `supported` requires a support profile; computational / repo-empirical
  strands require `docs/solutions/` + commit.
- **Promotion is required to cross into the repo:** no canonical change without a `CYB-NN`.
- **`memory/` is neither evidence nor authority.**
- **Refuted stays queryable:** superseded material is relabelled, not deleted (mirroring
  `CHANGELOG`'s one-finding-per-version arc and the project's kept refutations).
- **Defer the database:** Markdown is canonical; build the Neo4j import only when an actual
  traversal question defeats ordinary Markdown search and indexes. The DB is never the sole copy.

## Claude Code's standing responsibilities here

- Maintain the **forward links** (research `Claim` → `CYB-NN` → commit → `docs/solutions/`) and
  the frozen-export manifests, so the systems never fork.
- Run **Review** passes and log them (as with the CYB-25 referee pass and its `review-ledger`).
- Keep **`memory/`** current on collaboration *state* — never citing it as evidence.
- Treat this protocol as a diffable proposal: challenge it, log the objection, revise or record
  it as open — the same terms as code.
