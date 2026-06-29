---
title: "Chaos in the conserved beer game routes via Hopf/quasiperiodicity, not a clean period-doubling cascade — and how to keep yourself honest"
category: modeling
tags: [chaos, lyapunov, bifurcation, beer-game, anchoring-and-adjustment, supply-line-underweighting, instrument-validation, method]
created: 2026-06-28
severity: medium
component: src/chaos
problem_type: conceptual_pitfall
root_cause: spec_modeling_assumption
tracking: CYB-2
---

# Chaos in the conserved beer game routes via Hopf/quasiperiodicity, not a clean period-doubling cascade

Building CYB-2 (deterministic chaos in the 3-tier supply chain) surfaced several
traps the project's standing discipline — *measure the claim; let real behaviour
refute the spec; the correction is the finding* — caught before they became false
results. Recording them so they don't recur on the next mechanism.

## Problem

The spec predicted a **pristine logistic-style period-doubling cascade** (fixed
point → period-2 → period-4 → … → chaos) as the control parameter `β = a_SL/a_S`
(supply-line weighting) falls. Built faithfully, the conserved 3-tier
anchoring-and-adjustment model does **not** do that. As β crosses onset the
fixed-point amplitude grows **continuously from zero with the largest Lyapunov
exponent λ ≈ 0** — the marginal signature of a **supercritical Hopf bifurcation to
a two-frequency torus** (quasiperiodicity), *not* a flip to period-2. Only as the
torus breaks down (frequency-locking + embedded period-doubled windows) does λ
lift clearly positive into genuine chaos.

Two further traps nearly produced *false positives* along the way:

### Trap A — a positive Lyapunov on an UNBOUNDED trajectory is not chaos
The deep-underweighting corner (β→0 at aggressive `a_S`) gives λ>0 — but the
trajectory **runs away to ±thousands** (vs demand 100) before the hard
nonlinearities clamp it, then freezes. That is transient exponential *growth*, not
chaos. Chaos requires a **bounded** aperiodic attractor. λ>0 must be read together
with a boundedness check (amplitude stabilizes; late-window range ≈ early-window
range), or you will certify a blow-up as chaos.

### Trap B — an absolute conservation tolerance trips on scale, not on leaks
The CYB-1 conservation assert used an absolute `residual < 1e-9`. In a runaway
regime the goods totals reach millions and float round-off pushes the *absolute*
residual just over 1e-9 — a *precision artifact*, not a leak (relative residual
~1e-13). Reported as a "GOODS LEAK" it looks like a bug in the physics.

## Root cause

* **High-dimensional delay systems generically lose stability via Hopf, not a
  flip.** The state is 3 tiers × (4 + L) ≈ 21 dimensions with lead-time delays;
  the first instability of such a system is almost always a complex eigenvalue pair
  crossing the unit circle (oscillatory → torus), giving quasiperiodicity. A clean
  period-doubling cascade is characteristic of *low-dimensional* maps (the logistic
  map). Expecting the logistic picture from a delay network is the modeling
  assumption that was wrong.
* The runaway-vs-chaos confusion is the literal "complication is not chaos" trap
  the spec warned about, made concrete: the same diagnostic (λ>0) means different
  things on bounded vs unbounded sets.

## Solution

1. **Validate the instrument before trusting its verdict** (the load-bearing move,
   mirroring CYB-1's frozen-forecast regression). The largest-Lyapunov estimator
   reads the logistic map at r=4 as **λ = 0.69315 = ln 2** to five digits and λ<0
   in periodic windows; the bifurcation sweeper reproduces the logistic cascade
   (1→2→smear). Only then point them at the unknown system. An instrument that
   can't read a known chaotic map cannot certify an unknown one.
2. **Report the real route.** Supercritical Hopf → quasiperiodic → chaos, with
   embedded periodic/period-doubled windows. This is exactly what **Mosekilde &
   Larsen (1988)** document for the beer game (torus dynamics, frequency-locking,
   *and* period-doubling) — richer than, and more faithful than, the spec's first
   framing. The load-bearing claim survives intact: bounded + aperiodic + λ>0 +
   deterministic + conserved = deterministic chaos, measured. Canonical regime
   `a_S=0.7, L=3, θ=0.25`: λ turns positive near β≈0.26, up to +0.054 nats/step.
3. **Check boundedness alongside λ.** Pick a regime where the attractor amplitude
   *stabilizes* (growth ratio ≈ 1) and report λ>0 there — not the runaway corner.
4. **Make the conservation tolerance relative to scale:**
   `residual < 1e-9 * max(1, |injected|, |goods_in_system|)`. Stays at machine
   precision (~5e-15 here) regardless of regime; only a real leak trips it.

## Takeaways (how to apply)

1. **Don't expect a logistic cascade from a high-dimensional delay system.** Its
   first bifurcation is most likely Hopf (→ quasiperiodicity), with period-doubling
   showing up as *windows* inside a richer structure. Plan the bifurcation diagram
   and the narrative for that, not for a clean staircase.
2. **λ>0 is necessary but not sufficient for chaos — always pair it with a
   boundedness check.** Exponential divergence of an unbounded orbit is a blow-up,
   not chaos. This is the operational form of "complication is not chaos".
3. **Validate any dynamical-systems instrument on a closed-form case first**
   (logistic r=4 → ln 2). Bake the self-test into the module so it runs every time.
4. **Conservation tolerances should be relative when magnitudes can vary by orders
   of magnitude.** An absolute floor reports precision noise as a physics bug.
5. **β (supply-line weighting), not a_S, is the destabilizing control** — at high β
   even aggressive inventory adjustment stays stable. The behavioural story
   (underweighting the pipeline) *is* the bifurcation parameter; confirm which knob
   actually crosses the boundary before sweeping the wrong one.

## References
- Code: `src/chaos/` (`lyapunov.py` + `bifurcation.py` self-tests; `model.py`
  anchoring rule + `step_vector`; `run_v0.py` the three figures).
- Plan: [`../plans/2026-06-28-feat-chaos-v0-deterministic-chaos-instrument-plan.md`](../plans/2026-06-28-feat-chaos-v0-deterministic-chaos-instrument-plan.md).
- Prior learning this rhymes with: [`bullwhip-seeing-is-not-acting.md`](bullwhip-seeing-is-not-acting.md)
  (a spec predicting an idealized outcome, refuted into a sharper result).
- Sterman, J. D. (1989), *Modeling managerial behavior*, Management Science 35(3):321–339.
- Mosekilde, E. & Larsen, E. R. (1988), *Deterministic chaos in the beer
  production–distribution model*, System Dynamics Review 4(1–2):131–147.
