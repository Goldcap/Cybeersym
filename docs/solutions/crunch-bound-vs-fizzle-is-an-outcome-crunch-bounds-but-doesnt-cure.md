---
title: "The Minsky credit-crunch's 'bound vs fizzle' is an outcome the model discovers, not a design choice — and on the CYB-17 substrate the crunch BOUNDS but does not CURE: even a hard, fast deleveraging only chokes the wage-price spiral via a grinding limit cycle at the solvency border (never to zero), and leverage-at-trigger turns out to be set by the policy rate, not a free lever; the Ponzi regime IS just CYB-17 capitalizing uncovered interest, renamed"
category: modeling
tags: [minsky, credit-crunch, deleveraging, financing-regime, hedge-speculative-ponzi, coverage-ratio, solvency-ceiling, switching-manifold, limit-cycle, accommodation, endogenous-money, bounding-vs-fizzle, debt-deflation, phasing, discipline-guard, regression-anchor, method]
created: 2026-07-02
updated: 2026-07-02
severity: medium
component: src/crunch
problem_type: conceptual_insight
root_cause: outcome_left_to_parameters_not_designed_in
tracking: CYB-19
---

# The crunch's outcome is discovered, not designed — and it bounds without curing

CYB-19 Phase 1 fires the solvency border CYB-17 built and CYB-18 showed is central (the coupled
system rides it 73% of steps): the *static* credit ceiling becomes a dynamic **credit-crunch
cascade**. One new mechanism on the bare CYB-17 substrate — a Minsky financing-regime classifier
+ a deleveraging-rate cascade — and three findings, all of the project's recurring "let the model
discover it" and "reveal what was already there" kinds.

## Finding 1 — "bound vs fizzle" is an outcome the parameters pick, not a wiring choice

The temptation is to wire the bounding path (credit contracts → wage bill cut → spiral choked)
and declare crunches stabilizing — a financial-stability pamphlet. The discipline (same as
CYB-17's three channels): wire the mechanism *neutrally* and let the outcome fall out. Over
(leverage-at-trigger `L_trig`, deleverage rate `δ`) at `i=0.60`:

- **fizzle** (fire late / contract slowly): the crunch fires, self-corrects mildly, inflation
  stays ~85% of baseline;
- **bound** (fire early / contract fast): the contraction chokes the spiral to ~12%;
- **no-op**: above the (rate-set) baseline leverage the crunch never fires.

Both reachable ⇒ not rigged. The boundary is diagonal — you must fire *early* AND contract *fast*
to bound. The lesson transports: **when a policy/structural intervention can help or hurt, wire it
so both are reachable and report the boundary; a model that only ever stabilizes has smuggled in
the conclusion.**

## Finding 2 — the crunch BOUNDS but does not CURE (and the honesty guard that keeps it true)

Even a hard, fast crunch only cuts inflation to ~12%, never cleanly to zero, and does so via a
**grinding limit cycle at the border**: fire → contract credit → force the wage bill down →
coverage recovers → credit heals → the spiral re-levers → fire again. The solvency border, a
*static clamp* in CYB-17/18, is now a border that **fires and recurs** — dynamic, not static.

This is only trustworthy because the dangerous basin is **deliberately unwired**: Phase 1
contracts *new* credit and forces repayment but does **not** default, impair, or write off (the
rentier pool stays passive), so the **Fisher debt-deflation** basin (falling `P·Y` raises the real
burden ⇒ more deleveraging) is unreachable *by construction*. The guard: characterize
bound-vs-fizzle, but do **not** conclude "the crunch is stabilizing" — the genuinely
destabilizing outcome is the Phase-2 direction (default + impairable rentier → the Fisher loop).
The general method point: **when you deliberately leave out the failure mode, say so loudly and
refuse the reassuring reading the truncated model invites.**

## Finding 3 — the Ponzi regime was already in CYB-17; and leverage-at-trigger is rate-set

Two "reveal what was there" observations:

- **Ponzi ≡ CYB-17 capitalizing interest.** Minsky's Ponzi unit ("income can't cover interest, so
  debt grows to service itself") is *exactly* CYB-17's `capitalized = max(0, interest − margin) >
  0`. The financing-regime classifier didn't add dynamics — it *named* a switch the accommodation
  model already had. Look for the phenomenon you're about to build already implicit in the
  substrate's existing arithmetic.
- **Leverage-at-trigger is not a free lever — the policy rate delivers you to Ponzi.** Debt `D/P`
  is pinned near a fixed ratio set by `i` (0.65 at low `i` → 0.75 at `i=0.70`), and the coverage
  ratio `CR = margin/interest` falls through 1 as the rate rises (hedge `i≲0.51` → speculative
  `≈0.53` → Ponzi `≥0.55`). So *the crunch lives in the high-rate regime* — hiking to fight the
  spiral is what tips the aggregate into the financing fragility that fires the crunch (pure
  Minsky, and consistent with CYB-17/18's "the rate is the load-bearing conditioning variable").

## Why it's trustworthy (the validations)

- **Regression anchor byte-exact.** Crunch-off (trigger disabled) reproduces CYB-17 (`W,P,D`) to
  `0.0` — the classifier + cascade are provably the only new thing.
- **Conservation through the deleveraging transient.** Three-way income identity + debt
  bookkeeping `≤ 1e-16` *including mid-crunch* — contracting credit leaks no accounting.
- **Determinism** — byte-identical reruns.

## Takeaways (how to apply)

1. **Wire interventions neutrally; make both good and bad outcomes reachable; report the boundary.**
   A crunch (or rate, or policy) that only ever helps is rigged.
2. **When you leave out the failure mode, say so and refuse the reassuring reading.** Phasing is
   legitimate; using a truncated model to claim safety is the pamphlet failure.
3. **The mechanism you're about to build may already be implicit in the substrate's arithmetic —
   name it before you add machinery.** (Ponzi was CYB-17's interest capitalization.)
4. **"Bounds" ≠ "cures."** A stabilizer that only works via a grinding limit cycle at a border,
   never to zero, is a materially weaker claim than "it stabilizes" — state the weaker, true one.

## References
- Code: `src/crunch/model.py` (`CrunchEconomy` — composes an unchanged `AccommodationEconomy` +
  the Minsky regime classifier + the deleveraging-rate cascade); `src/crunch/run_v0.py`
  (regression → regime tipping → bounding/fizzle map → border dynamics).
- Plan: [`../plans/2026-07-02-feat-crunch-v0-minsky-credit-crunch-phase1-bounding-vs-fizzle-plan.md`](../plans/2026-07-02-feat-crunch-v0-minsky-credit-crunch-phase1-bounding-vs-fizzle-plan.md).
- The substrate it fires: accommodation [[accommodation-runaway-was-full-accommodation-limit-rate-is-a-tug-of-war]] (CYB-17);
  the border shown central: [[accommodation-coupled-distributional-exhaustion-deferred-recursion-pins-a-floor]] (CYB-18).
- Anchors: Minsky (hedge/speculative/Ponzi); Keen (dynamic Goodwin–Minsky); Fisher 1933
  (debt-deflation — the **Phase 2** mechanism); endogenous money (Moore; Lavoie). Forward-links:
  CYB-19 Phase 2 (default / Fisher basin); CYB-19-on-coupled; CYB-21 (supply-chain financing).
