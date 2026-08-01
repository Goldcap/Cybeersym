# Review ledger — bifurcation note (CYB-25)

The note (`bifurcation-note.md`) and this ledger change **together**, one PR per coherent
claim-change set. Reviewers read the **diff**, not a pasted copy, so everyone reviews the
same version of the paper. Merge a PR only when every substantive objection is either
**resolved** or **explicitly logged here as OPEN**.

## Comment classification

Every review comment is tagged with exactly one type:

- **CORRECTNESS** — the stated claim is false / the map or invariant is misstated.
- **RIGOR** — the claim exceeds its evidence; a proved/numerical/conjectural row is
  mis-tiered (§6 of the note).
- **CLARITY** — the claim is right but ambiguously or misleadingly stated.
- **STYLE** — presentation, notation, wording.
- **OPEN QUESTION** — a genuine unknown surfaced for the record (not a defect).

## How a row moves

A CORRECTNESS or RIGOR comment on a claim `Pn / Nn / Cn` (the §6 ledger IDs) either
(a) gets the note edited and the row updated, or (b) is logged OPEN below with a one-line
rationale. Nothing merges with an unlogged substantive objection outstanding.

---

## Round 1 — initial draft (PR: CYB-25 initial bifurcation note draft)

Reviewers: Prof. Hu (external) · Claude (referee proxy) · Desktop.

| # | Reviewer | Type | Target (§/claim) | Comment | Status |
|---|----------|------|------------------|---------|--------|
| _ | _ | _ | _ | _(none yet — draft just opened)_ | — |

### Open questions carried forward

_(none yet)_

### Resolved this round

_(none yet)_

---

*Standing invitations to the reviewer, from the note §0/§6: (1) verify the §2 recurrence
against `src/chaos/model.py`; (2) challenge the §3 conservation / center-subspace argument
(claim N6 / C4); (3) challenge every use of "attractor / invariant / chaos /
border-collision / bifurcation"; (4) adjudicate the §5 open classification problem
(claim C2 / C5); (5) move any §6 row between tiers, or refute it.*
