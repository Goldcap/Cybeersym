---
id: review-2026-08-01-collaboration-protocol-v0.1
date: 2026-08-01
period: single-session design exchange
reviewer: Andy Madsen (mediating), GPT, Claude Code
status: complete
tags: [collaboration, protocol, provenance, knowledge-architecture, governance, meta]
outcome: collaboration-protocol v0.1 accepted
canonical_result: ../schemas/collaboration-protocol.md
---

# Research review — Collaboration Protocol v0.1

The origin record of `../schemas/collaboration-protocol.md`. Captures the design exchange
that produced it: a Claude Code proposal, GPT's amendments, and the accepted v0.1. Per the
protocol's own "derived notes link, don't copy" rule, the canonical protocol is **not**
reproduced here — see `../schemas/collaboration-protocol.md`; this record holds the
*negotiation*.

## What changed

GPT scaffolded the `research/` notebook (nodes, graph model, record schema, templates,
indexes) — formalizing the notebook's *internals*. It asked to "formalize our interactions."
Claude Code contributed the missing layer: the **cross-system boundary** (how `research/`,
`docs/`+code, and `memory/` relate) and the **multi-agent protocol**. GPT amended it. The two
converged on **v0.1**.

## The proposal (Claude Code, v0 spine)

1. **Three layers, one direction of flow:** `research/` (ideation) → *pulled over* → `docs/`
   (compound engineering); `memory/` = collaboration continuity. Authority one-way.
2. **The pull-over:** a Linear ticket (CYB-NN) is the boundary object; a `Claim` reaches
   `supported` only by citing `docs/solutions/` + commit.
3. **Defer Neo4j** (YAGNI); Markdown canonical.
4. **Immutable conversation exports**; derived notes link forward, don't copy.

## GPT's amendments (accepted)

1. **Typed support, not one universal gate.** Replace bare `supported` with a `support_type`
   (empirical | computational | mathematical | documentary | mixed) + evidence profile. The
   `docs/solutions/` + commit gate is mandatory **only** for computational / repo-validated
   empirical claims — not for literature, derivation, historical evidence, or conceptual
   clarification. *Fixes a real flaw: v0 forced every true proposition into the shape of a
   software change.*
2. **Promotion marks commitment, not curiosity.** Exploration in `research/` is free; a ticket
   is required only when an idea crosses into canonical implementation / plans / conclusions.
   Invariant: *"No research idea may alter the project's canonical implementation, plans, or
   validated conclusions without a promotion event linked to a Linear ticket."* More
   enforceable than "the moment an idea becomes work," because crossing the boundary is
   observable (a git event) while "work" is ambiguous.
3. **Hash-based provenance for frozen exports.** A `provenance.yaml` manifest (`source_file`,
   `sha256`, `captured_at`, `origin`, `immutable: true`) makes silent rewriting *detectable*;
   mutable forward-links (`derived_notes`, `canonical_successors`) live in an adjacent
   `links.yaml` so the export bytes stay untouched.
4. **`memory/` is never evidence.** It may hold preferences, procedures, hazards, and mechanics,
   but cannot establish what is true. "Memory can tell an agent where to look or how to work;
   it cannot establish what is true."

## Claude Code's riders (folded into v0.1)

- `support_type` is a **derived summary of the evidence list**, not an independent field — so
  `mixed` can't be declared to slip a computational claim past its commit (consistent with the
  graph model's "derived, not asserted").
- The promotion invariant is **mechanizable**: commits touching `src/`/`docs/` already reference
  their `CYB-NN`, so the boundary is greppable, not just observable.
- The `sha256` is over the **as-received bytes** (archives aren't byte-reproducible; don't
  re-zip); per-file hashes may ride alongside.
- The memory boundary is extended: `memory/` is neither **evidence** nor **authority** — it
  cannot establish truth (only the repo can) and cannot authorize a crossing (only a ticket can).

## Decisions

- **collaboration-protocol v0.1 accepted.** Live, and held to the same review terms as code.
- Adopted GPT's closing line as the protocol's epigraph:
  > *Research proposes. Tickets authorize crossing the boundary. The repository tests. Evidence
  > decides. The notebook remembers the path — including the failures.*

## Contradictions / failed ideas (kept, per the refuted-stays-queryable rule)

- **v0's single `supported` gate** (docs/solutions + commit for *all* claims) — **superseded**
  by typed support. Recorded, not deleted.
- **v0's "the moment an idea becomes work"** promotion trigger — **superseded** by the
  narrow, observable "crossing into the canonical record" trigger.

## New questions / follow-ups

- Implement the `provenance.yaml` / `links.yaml` pair for the existing
  `conversations/2026/chaotic-economic-models/` export (retrofit the frozen origin).
- Decide the concrete YAML location for `support_type` / `evidence` in `research-record.schema.md`
  (align the schema doc with this decision).
- Revisit Neo4j only when a traversal question defeats ordinary Markdown search + indexes.

## Notes reviewed

- `../schemas/collaboration-protocol.md` (v0.1 — the canonical result)
- `../schemas/graph-model.md`, `../schemas/research-record.schema.md`
- `../conversations/2026/chaotic-economic-models/` (the source export that prompted the notebook)
