---
title: "The credit-crunch's 'bounds-without-curing' grind gets strictly WORSE on the coupled egg stack: recursion re-ignites the spiral in the crunch's recover phase, so the achievable choke floor rises (7%→12% of baseline) and the crunch is uniformly less effective at every deleverage rate — the same border stays dominant but chokes less per bind because the spiral is hotter between binds"
category: modeling
tags: [minsky, credit-crunch, coupling, recursion, limit-cycle, deleveraging, solvency-ceiling, bounds-without-curing, inheritance-build, decoupling-regression, two-anchors, method]
created: 2026-07-02
updated: 2026-07-02
severity: low
component: src/crunch_coupled
problem_type: conceptual_insight
root_cause: reloading_forcing_defeats_a_recover-and-relever_stabilizer
tracking: CYB-22
---

# The crunch bounds even less when recursion keeps reloading the gap

CYB-22 is a pure inheritance build: CYB-19 Phase 1's credit-crunch (coverage classifier +
deleveraging cascade) dropped **unchanged** on CYB-18's coupled recursion×conflict+financing
substrate. The question is inheritance-specific — it can't be asked on bare CYB-17.

## The finding — a recover-and-re-lever stabilizer is defeated by reloading forcing

Phase 1 found the crunch **bounds without curing**: it turns a runaway into a grinding limit
cycle (fire → cut credit → coverage recovers → spiral re-levers), choking only to ~12% of
baseline. That mechanism depends on a *quiet recover phase* between cuts. On the coupled
substrate recursion reloads the gap **every period** (`g=g0+κ·d`), so the recover phase is no
longer quiet — the spiral re-ignites before the next cut lands. Result, measured:

- baseline spiral hotter: bare +3.30 → coupled +4.09 %/step (recursion reloads the gap);
- **achievable choke floor rises**: best-over-δ bare **7%** → coupled **12%** of own baseline;
- **limit-cycle amplitude ~3×**: tail σ(π) 1.02 → 2.93 %/step (clean regular cycle → chaotic);
- the crunch is **uniformly** less effective at every deleverage rate δ, and the bounding/fizzle
  boundary shifts toward "harder to bound."

The transportable lesson: **a stabilizer that works by cut-then-recover is undermined by
persistent reloading forcing.** When you validate a damping/bounding mechanism on a substrate
with a *static* disturbance, re-test it against a substrate that *continuously re-supplies* the
disturbance — the mechanism can degrade even though nothing about it changed. (Same shape as
CYB-18's distributional channel: a mechanism that "exhausts / bounds" on the static substrate
merely "floors / bounds-less" once recursion re-supplies its input.)

## The border stays dominant but chokes less per bind

The solvency/crunch border binds 73% (bare) → 63% (coupled) of steps — still **dominant** on
both (CYB-18's static ceiling also rode 73%). So coupling doesn't dethrone the border; it makes
the spiral hotter *between* binds, so each bind achieves less. The effectiveness loss is about
what happens off the border, not a change in which border rules.

## Why it's trustworthy

- **Two byte-exact decoupling anchors, one per composition axis** (coupling × crunch): crunch-off
  ⇒ CYB-18 (`0.0`); κ=0 ⇒ CYB-19 Phase 1 (`0.0`). Nothing leaked but the interaction.
- **All conservation laws green through the crunch transient** (goods + three-way income + debt
  bookkeeping), worst `1e-15`.
- **Determinism** — byte-identical reruns.

## Takeaways (how to apply)

1. **Re-test bounding/damping mechanisms against reloading substrates.** A stabilizer validated
   against a one-shot disturbance can degrade when the disturbance is continuously re-supplied.
2. **"Dominant border" and "effective border" are different questions.** The same constraint can
   keep binding just as often yet accomplish less, because the action is off-border.
3. **Two composition axes ⇒ two anchors.** Recover each parent in its own decoupling limit.

## References
- Code: `src/crunch_coupled/model.py` (`CrunchCoupledEconomy` — `ChaosChain` + `CrunchEconomy`
  unchanged, via the CYB-18 reload); `src/crunch_coupled/run_v0.py`.
- Plan: [`../plans/2026-07-02-feat-crunch-coupled-v0-does-the-grind-worsen-under-reloading-plan.md`](../plans/2026-07-02-feat-crunch-coupled-v0-does-the-grind-worsen-under-reloading-plan.md).
- Parents: crunch Phase 1 [[crunch-bound-vs-fizzle-is-an-outcome-crunch-bounds-but-doesnt-cure]] (CYB-19);
  coupled accommodation [[accommodation-coupled-distributional-exhaustion-deferred-recursion-pins-a-floor]] (CYB-18).
- Forward-link: Phase-2-on-coupled (default/contagion on the egg stack) — the eventual full combination.
