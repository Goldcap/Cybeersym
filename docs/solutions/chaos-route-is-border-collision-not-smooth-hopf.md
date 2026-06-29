---
title: "The conserved beer game routes to chaos via a border-collision (piecewise-smooth), not period-doubling and not a smooth Neimark–Sacker — and how to tell"
category: modeling
tags: [chaos, lyapunov, bifurcation, jacobian, border-collision, piecewise-smooth, neimark-sacker, beer-game, supply-line-underweighting, instrument-validation, method]
created: 2026-06-28
updated: 2026-06-29
severity: medium
component: src/chaos
problem_type: conceptual_pitfall
root_cause: spec_modeling_assumption
tracking: CYB-2
---

# The conserved beer game routes to chaos via a border-collision, not period-doubling and not a smooth Neimark–Sacker

Building and *closing out* CYB-2 (deterministic chaos in the conserved 3-tier
supply chain) refuted **two** successive framings of the route to chaos — the
second one handed over by the other agent (Claude Desktop, via Linear). Each
refutation came from a direct measurement, not an argument. The standing discipline
— *measure the claim; let the data refute the framing; the correction is the
finding* — held even when the framing was a confident, well-reasoned hypothesis.
Recording the full arc so the next mechanism doesn't repeat any leg of it.

## Problem — three framings, two refuted by measurement

1. **"Pristine period-doubling cascade" (the original spec, criterion 1).** Refuted:
   the onset is not a gentle flip to period-2; the cascade staircase never appears.
2. **"Supercritical Neimark–Sacker / discrete Hopf to a quasiperiodic torus" (the
   close-out hypothesis).** The amplitude appearing to grow from zero with λ≈0 at
   onset *looked* like a supercritical Hopf to a torus, so the close-out asked to
   confirm it via the eigenvalue crossing. Direct measurement refuted it too.
3. **Border-collision bifurcation of a piecewise-smooth map (what the measurements
   actually show).** This is the honest mechanism.

Plus two near-miss *false positives* the discipline caught earlier (still worth
keeping):

- **λ>0 on an UNBOUNDED trajectory is not chaos.** The deep-underweighting corner
  (β→0, aggressive a_S) gives λ>0 but the orbit runs away to ±thousands then
  freezes — transient growth, not chaos. Always pair λ>0 with a boundedness check.
- **An absolute conservation tolerance trips on scale, not on leaks.** At large
  magnitudes the absolute residual exceeds 1e-9 by float round-off (relative ~1e-13).
  Make the tolerance relative to the goods scale.

## Root cause — why it's a border-collision, and how we know

The model is a **piecewise-smooth** map: `order = max(0, …)` and
`ship = min(inventory, backlog)` are kinks (switching manifolds). Three independent
measurements distinguish a *smooth* bifurcation from a *border-collision*:

- **(a) Eigenvalues at the *physical* fixed point never reach the unit circle.**
  Linearize the one-step map (finite-difference Jacobian, `linearize.py`) at the
  *attracting* equilibrium (found by iteration) and track the leading complex pair as
  β falls: it stays at **|λ|≈0.91 (∠≈40°)** clean through the onset region and
  **never reaches |λ|=1**. The equilibrium undergoes **no smooth local bifurcation**.
  *Load-bearing pitfall avoided:* a Newton solve found a root with |λ|=1.13 — but
  that was a **virtual** equilibrium on the *linear extension* of a piece, outside
  its region of validity (negative supply line). Mistaking it for real would have
  *falsely confirmed* a Neimark–Sacker. Find the physical fixed point by **iteration
  in the stable regime**, and check feasibility/branch-validity on any Newton root.
- **(b) Onset is a hard jump with bistability — and the equilibrium is NOT
  destroyed.** Amplitude jumps **0 → ~525 over Δβ≈0.003** (discontinuous), and the
  turbulent attractor **coexists** with the still-stable equilibrium (verified by
  running from small vs large initial conditions): a constraint-riding attractor is
  **born alongside** the stable fixed point, not in place of it. Supercritical Hopf =
  continuous-from-zero and no coexistence; we see the opposite. The coexistence is
  **endogenous path-dependence / hysteresis** — same parameters, calm or turbulent
  depending on history (an anti-equilibrium-uniqueness result).
- **(c) Which border, and geometry.** Instrumenting the developed attractor: the
  dominant active constraint is **order non-negativity** (`max(0, order)`, "you can't
  un-order" — manufacturer orders zero **42–56 %** of steps), with the **stockout**
  floor (`min`-ship) secondary (~24–27 %). Delay-embedded phase portraits show
  frequency-locked points → a **closed invariant loop** (flat segments riding the
  `order≥0` border — the piecewise-smooth fingerprint) → a **strange attractor**.
  FFT: a single sharp line → a **subharmonic at f/2** → broadband.

The structural reason the original logistic cascade never shows up: this is a ~21-D
**piecewise-smooth delay** system. Clean period-doubling cascades are a
low-dimensional-*smooth*-map phenomenon; high-D delay systems with hard constraints
generically transition via Hopf-like or border-collision mechanisms — and when the
constraints bite at onset (as here), border-collision wins.

## Solution

1. **Validate every dynamical instrument on a closed-form case before trusting its
   verdict** (the discipline guard). `lyapunov.py` → logistic r=4 gives λ=ln 2 to 5
   digits; `bifurcation.py` → reproduces the logistic cascade; `linearize.py` →
   recovers the logistic multiplier 2−r and fixed point 1−1/r exactly, and a known
   complex pair. Only then read the supply chain.
2. **Name the bifurcation from the linearization + onset character, not the
   trajectory's appearance.** Eigenvalue-never-crosses-1 + hard jump + bistability =
   border-collision. Reported as such (Zhusubaliyev & Mosekilde, *Bifurcations and
   Chaos in Piecewise-Smooth Dynamical Systems*).
3. **Report the regime classification** (stable / bounded turbulence / runaway), and
   note the forward-link: the inflation thesis's accommodation/reflexivity channels
   are what would *remove the bound* and turn bounded turbulence into a runaway
   spiral — so the bounded-vs-runaway boundary is load-bearing for later tickets.

## Takeaways (how to apply)

1. **A trajectory that *looks* like a torus is not proof of a Neimark–Sacker.** The
   loop can be born by a border-collision instead. Confirm the *birth* mechanism
   with eigenvalues at the fixed point + onset character (jump vs continuous,
   coexistence vs none), not just the phase portrait.
2. **Find the PHYSICAL fixed point (iterate in the stable regime); check feasibility
   on any Newton root.** Piecewise-smooth maps have virtual equilibria on
   extrapolated branches that will mislead the eigenvalue analysis.
3. **In piecewise-smooth systems, treat the clamps as first-class dynamics.** The
   `max(0,·)`/`min(·)` saturations are not numerical hygiene — they can BE the
   bifurcation mechanism (the orbit literally rides them).
4. **λ>0 ⇒ chaos only on a bounded attractor.** Pair it with a boundedness check;
   exponential divergence of an unbounded orbit is a blow-up.
5. **Conservation tolerances should be relative when magnitudes span orders of
   magnitude.** An absolute floor reports precision noise as a physics bug.
6. **The other agent's framing gets the same skeptical measurement as the spec's.**
   The close-out's Neimark–Sacker hypothesis was well-argued and wrong; the
   eigenvalue/bistability measurements said so, and the cross-agent channel (Linear)
   is where that refutation is surfaced and reconciled — not silently overridden.

## References
- Code: `src/chaos/` — `lyapunov.py`, `bifurcation.py`, `linearize.py` (all
  self-tested); `model.py` (`step_vector`); `run_v0.py` (proves the chaos);
  `run_route.py` (names the route: eigenvalues + bistability + phase portraits + FFT).
- Plan: [`../plans/2026-06-28-feat-chaos-v0-deterministic-chaos-instrument-plan.md`](../plans/2026-06-28-feat-chaos-v0-deterministic-chaos-instrument-plan.md).
- Prior learning this rhymes with: [`bullwhip-seeing-is-not-acting.md`](bullwhip-seeing-is-not-acting.md)
  (a spec predicting an idealized outcome, refuted into a sharper result).
- Sterman, J. D. (1989), *Modeling managerial behavior*, Management Science 35(3):321–339.
- Mosekilde, E. & Larsen, E. R. (1988), *Deterministic chaos in the beer
  production–distribution model*, System Dynamics Review 4(1–2):131–147.
- Zhusubaliyev, Zh. T. & Mosekilde, E. (2003), *Bifurcations and Chaos in
  Piecewise-Smooth Dynamical Systems*, World Scientific.
