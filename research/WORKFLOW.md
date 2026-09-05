# Research → repo PR workflow (the review contract)

*Converted from the original `WORKFLOW.txt` (Windows-1252 smart quotes cleaned; `?`
placeholders left verbatim as authored). This is the process doc for how a claim-change
crosses from research into the repo — the PR-review side of the collaboration protocol.
See also `schemas/collaboration-protocol.md`.*

## A clean workflow

- Claude or I create a branch for one revision round.
- The draft and review ledger change together.
- Open a PR with a narrow title, for example:
  - `CYB-25: initial bifurcation note draft`
  - `CYB-25: tighten conservation and spectrum claims`
  - `CYB-25: incorporate external mathematical review`

You tell the other reviewer: "Check PR #xx." The reviewer reads the actual diff, not a
pasted copy.

Comments are classified as:

- CORRECTNESS
- RIGOR
- CLARITY
- STYLE
- OPEN QUESTION

The author addresses comments in the branch. Merge only when substantive objections are
either resolved or explicitly logged as open.

**The key rule:** one PR should represent one coherent claim-change set. Don't mix
mathematical corrections, prose cleanup, regenerated figures, and unrelated repository work
in the same PR. Small diffs make hostile review much more effective.

## Keep these files together

- `docs/outreach/bifurcation-note.md`
- `docs/outreach/review-ledger.md`
- `docs/outreach/figures/`

## Use the PR description as a compact review contract

```
## Purpose
Create the first mathematician-facing draft for CYB-25.

## Claims changed
- Defines the 21-D map directly from implementation.
- Separates proved, numerical, and conjectural statements.
- Recasts the onset as an open global nonsmooth classification problem.

## Review requested
- Verify recurrence against `src/chaos/model.py`.
- Challenge the conservation ? ?=1 argument.
- Challenge use of "attractor," "invariant," and "bifurcation."
- Identify every claim exceeding numerical evidence.

## Out of scope
- Economics interpretation
- Email copy
- New simulations
```

That lets either model begin reviewing immediately and keeps us from reviewing different
mental versions of the paper.
