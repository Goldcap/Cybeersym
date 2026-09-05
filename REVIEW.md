# REVIEW.md — how automated code review must behave in this repo

This is a research repo: an agent-based, stock-flow-consistent economic simulation (numpy +
matplotlib only). **Automated review here is an ADVISORY, low-severity net for *mechanical* issues
only.** The load-bearing check is the human/domain reviewer gate (`CLAUDE.md` §"The reviewer gate",
`docs/reviewer-gate-log.md`) — a fresh reviewer that re-derives the math and fact-checks the
economics. Do **not** attempt that scientific review here: if a claim seems to need it, note in one
line "may warrant the domain gate" and move on — do not adjudicate math or economics.

## What "important" means here

- Flag only issues that **break behavior**, **break determinism (σ=0)**, or **break a
  conservation / byte-exact-nesting assert**.
- Style, naming, and structure are **Nit at most**. Report **at most 5 Nits** per review, then say
  "plus N similar items". Prefer silence to noise.

## Respect the repo's deliberate constraints — do NOT suggest against them

These are choices, not oversights. Suggesting against them is noise:

- **numpy + matplotlib ONLY.** Never suggest adding scipy, pandas, statsmodels, scikit-learn, or any
  dependency. A pure-numpy OLS/VAR or a hand-rolled routine is intentional.
- **Parsimony is a value.** Do not suggest adding parameters, features, abstractions, generality, or
  "flexibility." The project actively rejects unearned complexity (e.g. CYB-14 tested a second
  pricer parameter and *rejected* it).
- **Determinism and conservation asserts are intentional.** Flag them only if a change *breaks* one.
- **The `importlib` `_load(...)` cross-module pattern** (loading a sibling module by path) is
  intentional — scripts run from inside `src/` with no `sys.path` shims. Not a smell.
- **One analysis script per version** (`vNN_*.py`, `run_v0.py`, etc.) each regenerating its figure
  is the established shape — do not suggest consolidating them.

## Do NOT review as code (skip entirely)

- `docs/**`, `THESIS.md`, `CHANGELOG.md`, `HANDOFF.md`, `README.md` — prose; the domain gate owns
  these, and prose lint is pure noise.
- `research/**` — the ideation notebook.
- `**/figures/**` — generated artifacts (deterministic outputs, not source).
- `.github/**` and CI config already reviewed here.

## Scope

Review `src/**/*.py` for **behavior / correctness bugs** and genuine mechanical defects (real dead
code, an actual bug, a missing test for new behavior). Keep every review short, humble, and
advisory. A green run means "no mechanical smell found" — never "this is correct."
