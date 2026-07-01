---
title: "feat: Conflict module v0 — wage-price conflicting-claims inflation (the social transmission channel)"
type: feat
status: done
date: 2026-06-30
tracking: CYB-6
canonical_source: "Linear CYB-6 (https://linear.app/techno87/issue/CYB-6)"
depends_on: [CYB-1, CYB-2]
---

# feat: Conflict module v0 — wage-price conflicting-claims inflation

> **Canonical spec lives in Linear (CYB-6).** This file mirrors the spec into
> version control. Spec changes happen in Linear first, then sync here. The
> shipped outcome / final numbers are at the bottom.

## Goal

Isolate the **conflict** channel — inflation as a distributional struggle
(wage–price conflicting claims) — on its own minimal substrate, the way CYB-1
isolated recursion. Demonstrate the **transmission threshold**: a one-off price
trigger *dissipates* when distributional claims are compatible but *transmits* into
sustained inflation when they are incompatible. Conserved substrate: **wage share +
profit share = 1** — realised shares always sum to one; conflict is the fight over a
conserved pie, and inflation is the symptom of an unresolvable fight over a conserved
total.

> **Taxonomy placement.** Recursion (CYB-1/2, technical/input–output) and Conflict
> (this, social/distributional) are the two *transmission* channels. Conflict is
> where **distribution becomes a cause** of inflation, not just the outcome the egg
> model measured. Accommodation and reflexivity (the *sustaining* channels) come
> after both transmission channels are in.

> **⚠ Discipline guard — do NOT pre-judge the dynamics.** v0's job is the
> transmission threshold + the conserved-shares structure. Then run the existing
> instrument suite and let it tell us what the dynamics *are*. The model tells us,
> not our priors.

## The minimal substrate

Single sector, single good. Two classes (workers, firms). State: nominal wage `W`,
price `P`; realised wage share `ω = W/P`. Workers' target `ω_w`; firms' implied
target `ω_f = 1/(1+m)`; aspiration gap `g = ω_w − ω_f`. Backward-looking claim
adjustment:

```
ŵ = max(0, α_w·(ω_w − ω))      # nominal-wage floor: wages downward-rigid
p̂ = α_p·(ω − ω_f)
W ← W·(1 + dt·ŵ);  P ← P·(1 + dt·p̂);  π = p̂
```

The pure 1-D map of the wage share, `ω ↦ ω·(1+dt·ŵ)/(1+dt·p̂)`, is what the reused
instruments iterate (`ω*` is a genuine fixed point of it; the full `(W,P)` state is
not — both grow at the common rate `π*`).

## Acceptance criteria (all met — see outcome)

1. Order parameter (amended): report BOTH curves. The **pure mechanism is symmetric**
   — `π* = k·g` through the origin (`g<0` → sustained *deflation*, not dissipation).
   The **nominal-wage floor breaks the symmetry**, suppressing the deflation side —
   which is what *creates* the dissipate-below/transmit-above threshold, the
   inflationary bias, and the piecewise-smooth `g = 0` border. The floor is a named,
   load-bearing feature (downward nominal wage rigidity; Tobin, Akerlof–Dickens–Perry),
   not a silent default.
2. Conserved shares: wage + profit = 1 (`< 1e-9`, scale-relative), incl. mid-spiral.
3. Steady rate matches the closed form `π* = (α_w·α_p/(α_w+α_p))·g`.
4. Dynamics characterized empirically (`linearize`/`bifurcation`/`lyapunov`), not
   assumed — including any nonsmoothness from the nominal-wage floor.
5. Determinism + reproducibility guarded.

## Scope (v0 excludes)

Isolated module (no supply-chain coupling yet); backward-looking adjustment in,
forward-looking indexation out (reflexivity, later); no money/credit (accommodation,
later); constant targets.

## Empirical anchor (note, don't build)

Rowthorn (1977); Lavoie (Post-Keynesian conflicting-claims tradition); 2021–23
"sellers' inflation" revival (Weber & Wasner 2023; ECB/IMF unit-profit
decompositions). Verify against source in the later grounding ticket.

---

## Outcome (shipped)

Delivered `src/conflict/{model.py, run_v0.py, README.md, figures/}`. All five
criteria met:

1. **Transmission threshold** — at `ω_f=0.65`, `α_w=α_p=0.30`: `g=−0.10` dissipates
   (`π*=0.000`), `g=+0.10` transmits (`π*=+0.015`); the order parameter `π*(g)`
   crosses zero exactly at `g = 0`.
2. **Conserved shares** — residual `0.0` every step.
3. **Closed form** — measured `π*` matches `(α_w·α_p/(α_w+α_p))·g` to
   **max |error| = 6e-17** across 36 `(g, α_w, α_p)` combinations.
4. **Dynamics, measured** — the multiplier of the wage-share map stays in
   `[0.57, 0.81]` (`|·|<1`), `λ < 0` everywhere, bifurcation is a single branch:
   a **stable node in the real wage share — the instability lives in the nominal
   price level**, the opposite signature from CYB-2's bounded chaos. The
   **nominal-wage floor** is load-bearing: it converts the symmetric model's `g<0`
   *deflation* into *dissipation to zero*, making `g = 0` a genuine **nonsmooth
   transmission border** (a kink in the multiplier) — the criterion-1 behaviour is
   delivered by the floor, a finding flagged back to the spec.
5. **Determinism** — byte-identical trajectories.

First **cross-module reuse** of the CYB-2 instrument suite (`lyapunov`,
`linearize`, `bifurcation`) — imported unchanged, self-tested before use.

Learning: [`../solutions/conflict-channel-is-nominal-level-instability-not-real-chaos.md`](../solutions/conflict-channel-is-nominal-level-instability-not-real-chaos.md).
