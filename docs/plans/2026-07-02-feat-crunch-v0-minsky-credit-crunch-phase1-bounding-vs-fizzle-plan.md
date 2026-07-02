---
title: "feat: Minsky credit-crunch cascade Phase 1 — dynamic deleveraging off the solvency border, the bounding-vs-fizzle outcome map"
type: feat
status: done
date: 2026-07-02
tracking: CYB-19
canonical_source: "Linear CYB-19 (https://linear.app/techno87/issue/CYB-19)"
depends_on: [CYB-17]
---

# feat: Minsky credit-crunch cascade — Phase 1

> **Canonical spec lives in Linear (CYB-19).** Phased build (Phase 1 here; Phase 2 = default /
> Fisher basin, separate ticket). Mirror into version control; shipped outcome at the bottom.

## Goal

Fire the solvency border CYB-17 built and CYB-18 showed is central: turn the *static* credit
ceiling into a dynamic **credit-crunch cascade**, and let **bound vs fizzle** be an outcome the
model discovers, not a design choice. One new mechanism on the bare CYB-17 substrate: a
**financing-regime classifier** (hedge/speculative/Ponzi, from existing flows) + a
**deleveraging-rate cascade** fired at Ponzi∧border.

## The reframe

"Bound vs debt-deflate" is an OUTCOME, not a choice — wire the feedbacks and let parameters pick
the basin. **Phase 1 wires the bounding path only** (credit contracts → wage bill cut → spiral
choked) and maps **bound vs fizzle**. The Fisher/debt-deflation basin needs default + an
impairable rentier pool — **deliberately unwired here (Phase 2)**. Honesty guard: may
characterize the bounding path; may NOT conclude "the crunch is stabilizing."

## Acceptance criteria (all met — see outcome)

1. Crunch fires from a regime shift (coverage ratio), not a level breach — characterized.
2. Bounding-vs-fizzle outcome map over (leverage-at-trigger, deleverage rate) — both reachable.
3. Regression anchor byte-exact: crunch-off → CYB-17 (`0.0`).
4. Conservation through the deleveraging transient (< 1e-9).
5. Border interaction under the crunch vs CYB-18's static picture.
6. Determinism.

## Discipline guard

Both outcomes must be reachable (a crunch that always bounds is as rigged as one that always
collapses). Do NOT extend to a bound-vs-deflate claim — deflate is unwired. Reuse CYB-17
unchanged; one new mechanism only.

---

## Outcome (shipped)

Delivered `src/crunch/{model.py, run_v0.py, README.md, 3 figures}`. All six met.

1. **Regime tipping characterized.** The coverage ratio `CR = margin/interest` falls through 1
   as the rate rises: hedge (`i≲0.51`) → speculative (`i≈0.53`) → Ponzi (`i≥0.55`). The crunch
   arms at Ponzi∧border. A finding: **leverage-at-trigger is set by the policy rate**, not a free
   lever (echoing CYB-17/18).
2. **Bounding-vs-fizzle map (headline).** Over (`L_trig`, `δ`) at `i=0.60` (baseline +3.30%/step):
   **fizzle** (`L_trig=0.66, δ=0.05`) → +2.82%/step (85%); **bound** (`L_trig=0.61, δ=0.90`) →
   +0.38%/step (12%); **no-op** above the rate-set baseline leverage (`L_trig≳0.69`). Boundary is
   diagonal — must fire early AND contract fast to bound. Even a hard bound only cuts to ~12% via
   a grinding limit cycle — bounds but does not cure.
3. **Regression byte-exact.** Crunch-off reproduces CYB-17 (`W,P,D`) to `0.0`.
4. **Conservation through the transient.** Three-way income + debt bookkeeping `≤ 1e-16`,
   including mid-crunch.
5. **Border dynamics.** The solvency border, static in CYB-17/18, now **recurs as a limit cycle**
   (fire→cut→recover→re-lever); binds 73% of steps, wage floor 0% — still dominates, now dynamic.
6. **Determinism** — byte-identical reruns.

Learning: [`../solutions/crunch-bound-vs-fizzle-is-an-outcome-crunch-bounds-but-doesnt-cure.md`](../solutions/crunch-bound-vs-fizzle-is-an-outcome-crunch-bounds-but-doesnt-cure.md).
