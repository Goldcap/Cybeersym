---
title: "feat: Credit-crunch on the coupled substrate — CYB-19 Phase 1 crunch on the CYB-18 egg stack; does the grind worsen when recursion reloads?"
type: feat
status: done
date: 2026-07-02
tracking: CYB-22
canonical_source: "Linear CYB-22 (https://linear.app/techno87/issue/CYB-22)"
depends_on: [CYB-18, CYB-19]
---

# feat: Credit-crunch on the coupled substrate

> **Canonical spec lives in Linear (CYB-22).** Pure inheritance build (no new mechanism, no
> forks). Mirror into version control; shipped outcome at the bottom.

## Goal

Drop CYB-19 Phase 1's credit-crunch (coverage-ratio classifier + deleveraging-rate cascade)
**unchanged** onto CYB-18's coupled recursion×conflict+financing substrate. Headline question:
does the crunch's "bounds-without-curing" grind get **worse** when recursion keeps reloading the
gap (`g=g0+κ·d`) against the border?

## The composition (one inherited interaction)

Hold a `ChaosChain` + a `CrunchEconomy` (CYB-19 P1); each step reload the crunch's inner
accommodation base gap by `κ·d` (the CYB-18 coupling), then run the unchanged crunch tick.

## Acceptance criteria (all met — see outcome)

1. Crunch-under-coupling (headline): choke floor / limit-cycle amplitude coupled vs bare.
2. TWO byte-exact anchors: crunch-off → CYB-18; κ=0 → CYB-19 Phase 1.
3. All conservation green through the crunch transient (< 1e-9).
4. Border dynamics under coupling vs CYB-18's static 73%.
5. Determinism.

## Discipline guard

Report whether the grind worsens — don't assume it. Reuse the parent modules unchanged.

---

## Outcome (shipped)

Delivered `src/crunch_coupled/{model.py, run_v0.py, README.md, 3 figures}`. All five met.

1. **The grind WORSENS under reloading.** Baseline bare +3.30 → coupled +4.09 %/step; best
   achievable choke (min over δ) bare 7% → coupled 12% of baseline; limit-cycle amplitude
   1.02 → 2.93 %/step. Recursion re-ignites the spiral in the crunch's recover phase, so the
   floor rises and the crunch is uniformly less effective at every δ. Bounds-without-curing,
   now with a higher floor.
2. **Both anchors byte-exact** (`0.0`): crunch-off → CYB-18; κ=0 → CYB-19 Phase 1.
3. **All conservation green** (goods + three-way income + debt bookkeeping), worst `1e-15`.
4. **Border dynamics:** solvency/crunch border binds 73% (bare) → 63% (coupled) — dominant on
   both; coupling makes the spiral hotter between binds, so each bind chokes less.
5. **Determinism** — byte-identical reruns.

Learning: [`../solutions/crunch-coupled-grind-worsens-recursion-reignites-in-the-recover-phase.md`](../solutions/crunch-coupled-grind-worsens-recursion-reignites-in-the-recover-phase.md).
