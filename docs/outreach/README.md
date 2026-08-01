# Outreach — external mathematical review (CYB-25)

The mathematician-facing artifact and its review apparatus. The goal is a small, honest,
diffable note that hands an external dynamicist (Prof. Hu) a single, well-posed
bifurcation-classification question — **not** the economics, and **not** a proof we don't
have.

## Contents

- **`bifurcation-note.md`** — the note itself (~3 pp): *Finite-Amplitude Onset of a
  Coexisting Attractor in a Conserved Piecewise-Smooth Map*. Defines the 21-D map, states
  what is **proved** vs **numerical** vs **conjectural**, records the four successive
  (and refuted) classifications, and poses the reduction/classification question.
- **`review-ledger.md`** — the typed-comment ledger. One PR per coherent claim-change set;
  reviewers read the diff; nothing merges with an unlogged substantive objection.
- **`emails/cover-01…05.md`** — cover-letter options for the cold outreach (drafts).
- **`figures/`** — figures referenced by the note (copied from `src/chaos/figures/`).

## Workflow (from `WORKFLOW.txt`)

1. One revision round = one branch = one PR with a **narrow** title (`CYB-25: …`).
2. The PR description is the review contract: Purpose / Claims changed / Review requested /
   Out of scope.
3. Comments are typed (CORRECTNESS / RIGOR / CLARITY / STYLE / OPEN QUESTION) and logged in
   the ledger.
4. Do **not** mix mathematical corrections, prose cleanup, regenerated figures, and
   unrelated repo work in one PR. Small diffs make hostile review effective.

## Referee target

The claims are all reproducible from `src/chaos/` (MIT, `Goldcap/Cybeersym`). Each
instrument is self-validated on a closed-form case before it is trusted on the model:
`lyapunov.py` (logistic → ln 2), `linearize.py` (logistic multiplier 2−r), `normal_form.py`
(three documented 2-D border-collision cases), `bcb_classify.py` (the 21-D spectrum + the
one-sided-Jacobian probe). `run_v0.py` proves the chaos; `run_route.py` names the route.
