---
name: cybeersym-research
description: >-
  Apply the Cybeersym collaboration protocol when working with the research notebook.
  Use when (1) capturing a GPT/Desktop/Claude conversation export into research/, (2) promoting
  a research idea across the boundary into a project (Linear ticket + code/docs), (3) recording
  how a claim is supported (typed support), or (4) running a review pass. Keeps the ideation
  notebook (research/), the compound-engineering repo (docs/ + code), and collaboration memory
  from forking. Triggers: "capture this conversation", "promote this idea", "file this into the
  notebook", "is this supported", "run a research review", "notebook provenance".
---

# Cybeersym research protocol

**The authority is `research/schemas/collaboration-protocol.md` (v0.1).** This skill is the
*procedure*; that doc is the *contract*. If they ever disagree, the doc wins — and fix the skill.

## The creed (orienting frame)

> Research proposes. Tickets authorize crossing the boundary. The repository tests. Evidence
> decides. The notebook remembers the path — including the failures.

## Three layers — know which one you're touching

- **`research/`** — ideation. Ideas, concepts, questions. The distilled notes/schemas/reviews are versioned in the repo; raw conversation exports (`conversations/`) and bulk/licensed data (`data/`) stay local & git-excluded.
- **`docs/` + code** — compound engineering (committed). The referee: real data decides here.
- **`memory/`** — collaboration continuity. Preferences/procedures/mechanics only.
  **Never evidence, never authority** — it says where to look and how to work, not what is true
  (only the repo) and not what may cross the boundary (only a ticket).

Authority is one-way: `research/` may inspire and reference, but must not shadow canonical
conclusions in `docs/`. Findings return upstream only as new questions/hypotheses/links.

---

## Procedure 1 — Capture a conversation export (immutable provenance)

When a GPT/Desktop/Claude conversation is exported and should be preserved:

1. Create `research/conversations/YYYY/<slug>/` and place the **as-received** export bytes there
   (e.g. the original `.zip` and/or extracted files). **Do not re-zip or edit them.**
2. Write an **immutable** `provenance.yaml` beside them:
   ```yaml
   source_file: <as-received filename>
   sha256: <sha256 of the as-received bytes>   # e.g. sha256sum <file>
   captured_at: <ISO timestamp>
   origin: <conversation / tool / model>
   immutable: true
   ```
   Take the hash over the delivered bytes (archives aren't byte-reproducible — never re-zip).
   Per-file hashes of the extracted set may ride alongside.
3. Write a **mutable, adjacent** `links.yaml` for forward references (this evolves; the export
   does not):
   ```yaml
   derived_notes: []
   canonical_successors: []   # e.g. docs/outreach/bifurcation-note.md
   ```
4. Optionally add a summary from `research/conversations/TEMPLATE.md` that links the source.
5. Promote durable claims/questions/people/models into `research/notes/` (as *ideas*, status-marked).

**Never** edit a frozen export to match later work. The `sha256` exists so silent rewriting is
detectable.

## Procedure 2 — Promote an idea (cross the boundary)

Exploration inside `research/` is free — no ticket for cheap conjectures. A **Linear ticket
(CYB-NN) is required only to alter the project's canonical implementation, plans, or validated
conclusions.** Lifecycle:

```
captured → investigated in research/ → selected for implementation/validation
        → promoted via CYB-NN → resolved in code/docs/artifacts → linked forward from research/
```

Steps:
1. Confirm the idea is `developing` and actually crossing into canonical work (touching `src/`
   or `docs/`). If it's still exploration, stay in `research/` — do not open a ticket.
2. Ensure a **Linear ticket `CYB-NN`** exists (Desktop specs it; the ticket is the boundary object).
3. Execute/validate/review in the repo. On completion, post the verdict to the ticket:
   **commit hash + regression-anchor pass/fail**.
4. Update the originating `research/` record: status → `supported`/`refuted`/`superseded`, with a
   **forward link** `[CYB-NN · commit · docs/solutions/…]`. Link — do **not** copy the result.

Enforceable check: any commit touching `src/`/`docs/` should reference its `CYB-NN`.

## Procedure 3 — Type a claim's support

`supported` is not one gate. Record a **support profile**; the repo-gate applies only where it
belongs.

```yaml
status: supported
support_type: empirical | computational | mathematical | documentary | mixed
evidence:
  - type:             # per strand
    path_or_citation:
    commit:           # MANDATORY for computational / repo-validated empirical
    artifact_hash:
    reviewed_in:
```

- **computational** / repo-validated **empirical** → `docs/solutions/` entry **and** commit are
  mandatory. No notebook-only declaration satisfies this class.
- **mathematical / documentary** (derivation, literature, historical evidence, conceptual
  clarification with no code) → citation or derivation; no commit required.
- **mixed** = more than one strand; inherits the **strictest** gate (any computational strand
  still needs its commit). `support_type` is a *derived summary* of the evidence list — it can't
  be declared to weaken it.
- **Negative experiments are support** — they justify `refuted`/`disputed` under the same typed
  evidence (a computational refutation still cites its commit).

## Procedure 4 — Run a review pass

Use `research/reviews/TEMPLATE.md`. Record: what changed, strongest supported claims, weak/
disputed claims, new questions, **contradictions and failed ideas (kept, not deleted)**, evidence
gaps, decisions/next experiments. Link the canonical results; don't copy them. Superseded ideas
are **relabelled**, not removed — the notebook remembers the failures.

---

## Invariants checklist (verify before finishing any of the above)

- [ ] Right layer? ideation→`research/`, validated→`docs/`, mechanics→`memory/`.
- [ ] Did I **link** the canonical artifact rather than **copy** it?
- [ ] Frozen exports untouched + `sha256` manifest present; links in the adjacent file.
- [ ] `supported` carries a support profile; computational/empirical strands cite commit + docs/solutions.
- [ ] Any canonical (`src/`/`docs/`) change traces to a `CYB-NN`.
- [ ] `memory/` used for state/how-to only — never cited as evidence or as authorization.
- [ ] Refuted/superseded material relabelled and still queryable, not deleted.
- [ ] Neo4j still deferred (Markdown canonical) unless a real traversal question demands it.

## Portability note

This skill uses the open agent-skills format and is discovered by multiple runtimes via a copy
at each runtime's path: **Claude Code** (`.claude/skills/`), **Claude Desktop**, and **OpenAI
Codex** operating in-repo (`.agents/skills/`). The two repo copies **must stay byte-identical** —
edit both or neither; `scripts/check-skill-sync.sh` (wireable as a pre-commit hook via
`githooks/`) fails the commit on drift.

A plain **ChatGPT conversation** can use the *contract* as context but cannot execute repository
procedures without connected tools — give it `research/schemas/collaboration-protocol.md` + the
notebook schemas (e.g. a ChatGPT Project). **Codex**, operating in-repo, *runs* this skill with
filesystem, Git, and Linear access — it executes capture / promotion / provenance / support-typing
/ review rather than describing them. A blocked operation is an authorization limit (e.g. missing
write scope), not an absence of runtime capability.
