---
title: "The conflict channel is a NOMINAL-level instability over a STABLE real equilibrium — the opposite dynamical signature from the recursion channel's chaos — and the nominal-wage floor is what makes g=0 a transmission threshold"
category: modeling
tags: [conflicting-claims, wage-price-spiral, inflation, conservation, piecewise-smooth, nominal-wage-floor, border, instrument-reuse, lyapunov, linearize, bifurcation, method]
created: 2026-06-30
updated: 2026-06-30
severity: medium
component: src/conflict
problem_type: conceptual_insight
root_cause: model_structure
tracking: CYB-6
---

# The conflict channel: a nominal-level instability over a stable real equilibrium

CYB-6 isolated the **conflict** transmission channel (wage–price conflicting
claims) the way CYB-1/2 isolated **recursion**. The spec's central discipline guard
was *do not pre-judge the dynamics — run the instruments and let them tell us*. They
told us something cleaner than expected, and the opposite of CYB-2.

## What the dynamics are (measured, not assumed)

The minimal conflict model is two backward-looking claim-adjustment rules over one
conserved pie (`wage_share + profit_share = 1`). The reused CYB-2 instrument suite
(`lyapunov`, `linearize`, `bifurcation`, imported unchanged from `../chaos`) reads
the pure 1-D map of the wage share `ω = W/P`:

- `linearize`: the multiplier at the conflict equilibrium stays in `[0.57, 0.81]`
  for all `g` — never near `|mult| = 1`. A **stable node**, monotone approach.
- `bifurcation` over the aspiration gap `g`: a **single branch**. No
  period-doubling, no smear.
- `lyapunov`: `λ < 0` everywhere.

So the **real wage share is a clean stable equilibrium**. The instability is entirely
in the **nominal price level**: at equilibrium `ω` sits still while `P` (and `W`)
grow at the constant rate `π*` — a ray of sustained inflation. This is the **opposite
signature from CYB-2**: recursion makes the *real* quantities bounded-but-chaotic;
conflict makes the *nominal* level unstable while the real quantity is calm. Two
transmission channels, two opposite dynamical characters — worth stating as a result.

## Why this is the right reading (the validations)

- **Closed form to machine precision.** The steady rate matches the conflicting-
  claims result `π* = (α_w·α_p/(α_w+α_p))·g` (Rowthorn 1977; Lavoie) to
  `max |error| = 6e-17` across 36 `(g, α_w, α_p)` combinations. The "instability" is
  an exact analytic ray, not numerical drift.
- **Conserved shares.** Profit is the residual claimant on a conserved unit of value
  added; `wage_share + profit_share = 1` to `0.0` every step, mid-spiral included.
  Conservation is load-bearing again (cf. CYB-4).

## The nominal-wage floor is load-bearing — and it makes g=0 a nonsmooth border

The spec's criterion 1 says "`g ≤ 0` dissipates." The **smooth** symmetric model does
NOT do this: with no floor, `g < 0` produces steady *deflation* (the signed mirror of
`g > 0` inflation). What delivers dissipation-to-zero is the **nominal-wage floor**
`ŵ = max(0, α_w·(ω_w − ω))` (wages are downward-rigid):

- `g > 0` (incompatible): at `ω* < ω_w` the floor is **slack** — never binds —
  so `π*` is unchanged. Transmits.
- `g ≤ 0` (compatible): the floor **binds**, wages stop falling at `ω_f`, and
  inflation dissipates to **exactly 0** (not negative).

So the floor *creates* `g = 0` as a genuine **piecewise-smooth transmission border**
— a kink in the multiplier at `g = 0`. This rhymes with CYB-2's order-non-negativity
border: a clamp that looks like numerical hygiene is the structural feature. The
criterion-1 behaviour is *produced by* the floor — flagged back to the canonical
spec as a finding, not silently absorbed.

## Takeaways (how to apply)

1. **"Instability" can live in the nominal level while the real state is a stable
   node.** Don't assume an inflation mechanism needs chaotic or oscillatory real
   dynamics. Linearize the *reduced* state (here the ratio `ω`, not the growing
   `(W,P)`) — the right fixed point is in the ratio.
2. **The reduced map is where the fixed point is.** A model whose levels grow has no
   fixed point in the levels; find the stationary combination and hand the
   instruments *that* pure map. (Same lesson as CYB-4's center subspace, gentler.)
3. **A downward rigidity (floor) can BE the threshold.** Before reaching for a
   bifurcation to explain an on/off boundary, check whether a one-sided clamp
   produces it. Here the dissipation/transmission switch is a floor binding, not a
   smooth instability crossing zero.
4. **Build instruments model-agnostic and they pay off across mechanisms.** The
   CYB-2 suite read a supply chain and a distributional-conflict model unchanged —
   the first cross-module reuse, the reason they were built on a callable + flat
   vector in the first place.

## References
- Code: `src/conflict/` — `model.py` (the rules, conserved-shares assert, floor,
  `omega_map`), `run_v0.py` (threshold + closed form + dynamics + figures).
- Instruments reused: `src/chaos/{lyapunov,linearize,bifurcation}.py` (self-tested
  before use).
- Plan: [`../plans/2026-06-30-feat-conflict-v0-conflicting-claims-channel-plan.md`](../plans/2026-06-30-feat-conflict-v0-conflicting-claims-channel-plan.md).
- Sibling finding (the contrast): the recursion channel routes to chaos via a
  piecewise-smooth border-collision —
  [[chaos-route-is-border-collision-not-smooth-hopf]] — and conservation forces a
  non-hyperbolic equilibrium there
  ([[conserved-map-equilibrium-is-non-hyperbolic-so-border-collision-normal-form-doesnt-apply]]).
- Rowthorn, R. E. (1977), *Conflict, inflation and money*, Cambridge J. Econ.
  1(3):215–239. Lavoie, M., *Post-Keynesian Economics: New Foundations*.
- The symmetry-breaker (downward nominal wage rigidity): Tobin, J. (1972),
  *Inflation and unemployment*, Am. Econ. Rev. 62(1):1–18 ("greasing the wheels");
  Akerlof, G., Dickens, W. & Perry, G. (1996), *The macroeconomics of low inflation*,
  Brookings Papers on Economic Activity 1996(1):1–76.
- Weber, I. & Wasner, E. (2023), *Sellers' inflation, profits and conflict*,
  Rev. Keynesian Econ. (empirical anchor for the later grounding ticket).
