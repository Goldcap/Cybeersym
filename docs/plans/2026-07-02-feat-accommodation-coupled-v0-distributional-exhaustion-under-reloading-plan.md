---
title: "feat: Accommodation on the coupled substrate v0 — the CYB-17 channel decomposition on the CYB-10 egg stack, and the fate of the distributional-exhaustion flip"
type: feat
status: done
date: 2026-07-02
tracking: CYB-18
canonical_source: "Linear CYB-18 (https://linear.app/techno87/issue/CYB-18)"
depends_on: [CYB-10, CYB-17]
---

# feat: Accommodation on the coupled substrate v0

> **Canonical spec lives in Linear (CYB-18).** Inheritance build — design resolved by
> inheritance (all forks closed in CYB-17/CYB-10). Mirror into version control; shipped
> outcome at the bottom.

## Goal

Take CYB-17's accommodation machinery (credit ratification of the wage bill at a policy rate
`i`; the three rate-channels; the solvency ceiling) **unchanged** and drop it on CYB-10's
coupled recursion×conflict substrate instead of the bare CYB-6 conflict layer. Two questions
only the coupled substrate can answer:

1. **Q1 (headline).** On bare CYB-6 the distributional channel *self-exhausts* (drives `π*`
   to 0 once labor's static gap is closed) — that decay produced the cost-flip /
   restraint-insufficient region. When recursion keeps re-loading `g` via `κ·d(t)`, does the
   exhaustion **survive / defer / erase**?
2. **Q2.** Does the rate **gate** CYB-10's super-additive ignition — raise the threshold
   (choke ignition at the financing stage) or, via cost-push, lower it (rate helps ignite)?

## The composition (one new line)

CYB-17 drives a conflict layer off a fixed base gap; CYB-10 drives that base gap with
recursion (`g(t)=g0+κ·d(t)`). So reload accommodation's base each step from the chain deficit
(lower ω_f0 by κ·d, hold ω_w0), then let the unmodified accommodation step run on top. Reuse
`ChaosChain` and `AccommodationEconomy` unchanged; the coupling is the inherited CYB-10 map.

## Acceptance criteria (all met — see outcome)

1. Coupled channel decomposition + fate of the distributional decay term (headline).
2. Ignition-vs-rate map against the CYB-10 `(shock,κ)` baseline.
3. **TWO** byte-exact regression anchors: `κ=0`→CYB-17, full-accommodation→CYB-10.
4. All three conservation laws green at once (< 1e-9).
5. Three nonsmooth borders live at once — dominance report.
6. Determinism.

## Discipline guard

Do NOT pre-judge Q1/Q2. Reuse the parent modules unchanged (compose, don't rewrite). Finance
the wage bill ONLY (supply-chain financing is a deferred new mechanism). Minsky crunch
(CYB-19) and reflexivity (CYB-20) stay out.

---

## Outcome (shipped)

Delivered `src/accommodation_coupled/{model.py, run_v0.py, README.md, 3 figures}`. All six met.

1. **Both anchors byte-exact** (`0.0`): `κ=0`→CYB-17 (financed spiral, all channels);
   `i→0,cost-off`→CYB-10 (ignited coupled model). Two composition axes, one anchor each.
2. **Q1 — the distributional exhaustion is DEFERRED, and its clean zero becomes a
   recursion-pinned floor.** Bare distributional → 0 at `i=0.20` (exhausts); coupled floors at
   `≈ k·κ·⟨d⟩ = 0.91 %/step` — recursion re-supplies the gap every period, so the channel never
   runs out but also never wins. The **restraint-insufficient / cost-flip region survives and
   is hotter** (recursion lifts the whole `π*(i)` surface; baseline +1.50→+2.43 %/step): **no
   rate drives inflation to zero.** The rate becomes more redistributive, less stabilising.
3. **Q2 — the rate gates ignition both ways.** Rate-off `κ*=0.10` = CYB-10 baseline;
   cost-leaning **lowers** `κ*` (0.10→0.00, cost-push self-ignites with no coupling);
   disinflation-leaning **raises** it (0.10→0.17, chokes ignition). Same tug-of-war as Q1.
4. **All three conservation laws green** — goods + three-way income + debt bookkeeping, worst
   residual `1e-15` in the ignited/coupled/financed regime.
5. **Three borders live at once**; the **solvency ceiling dominates** (73%) and **pre-empts the
   wage floor** (rare, 6%) by capping the wage push first; stockout (26%) the ever-present
   recursion substrate. They interact, not just coexist.
6. **Determinism** — byte-identical reruns.

Learning: [`../solutions/accommodation-coupled-distributional-exhaustion-deferred-recursion-pins-a-floor.md`](../solutions/accommodation-coupled-distributional-exhaustion-deferred-recursion-pins-a-floor.md).
