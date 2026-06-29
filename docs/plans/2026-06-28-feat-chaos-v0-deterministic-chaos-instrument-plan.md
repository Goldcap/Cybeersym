---
title: "feat: Chaos module v0 — deterministic chaos + Lyapunov/bifurcation instrument"
type: feat
status: done
date: 2026-06-28
tracking: CYB-2
canonical_source: "Linear CYB-2 (https://linear.app/techno87/issue/CYB-2)"
depends_on: CYB-1
---

# feat: Chaos module v0 — deterministic chaos + Lyapunov/bifurcation instrument

> **Canonical spec lives in Linear (CYB-2).** This file mirrors the spec into
> version control. Spec changes happen in Linear first, then sync here. The
> shipped outcome / final numbers are at the bottom.

## Goal

Show that the conserved 3-tier supply chain (CYB-1), once given a realistic
**nonlinear** ordering rule, transitions into **deterministic chaos** as a single
behavioural parameter varies — and build the **measurement instrument** (largest
Lyapunov exponent + bifurcation diagram) that proves it is chaos and not merely
complication. The THESIS rests on economies being chaotic dynamical systems, not
equilibrium machines; this is that claim earned on the simplest substrate.

> **Why this is the right next step:** CYB-1 proved *amplification* (linear,
> bounded). Amplification is not chaos. Chaos is a specific, measurable claim —
> bounded aperiodic trajectories with sensitive dependence on initial conditions
> and a positive largest Lyapunov exponent (Sterman 1989; Mosekilde & Larsen 1988
> — deterministic chaos in the beer game).

> **Discipline guard (the trap to avoid):** complication is not chaos. A
> complicated model producing wiggly output proves nothing. Chaos must be
> *measured* (positive Lyapunov, bifurcation structure) and it must be
> *deterministic* — so the stochastic demand from CYB-1 is turned **OFF**. Any
> aperiodicity must come from the dynamics, not from random input.

## The nonlinearity to add (the chaos generator)

Replace CYB-1's near-linear order-up-to rule with the documented
**anchoring-and-adjustment** ordering heuristic (Sterman 1989):

```
order_t = max(0, D_hat + a_S*(S_star - S) + a_SL*(SL_star - SL))
```

* `D_hat` — adaptive demand forecast (exponential smoothing, param θ)
* `S`, `S_star` — current vs desired inventory (net stock); `a_S` = inventory-gap fraction
* `SL`, `SL_star` — current vs desired supply line; `SL_star = L * D_hat`; `a_SL` = supply-line fraction

Control parameter: `beta = a_SL / a_S` (supply-line weighting). `beta=1` →
fully credits the pipeline (stable); `beta<1` → **supply-line underweighting**
(the documented human bias) → over-correction → oscillation → chaos. The
`max(0, ·)` is the genuine nonlinearity that makes a bounded aperiodic attractor
possible.

## Acceptance criteria

1. **Period-doubling cascade.** Deterministic demand (σ=0, perturbed off
   equilibrium), a bifurcation diagram over the control parameter shows the route
   to chaos.
2. **Positive Lyapunov in the chaotic regime.** λ<0 stable/periodic, λ>0 chaotic;
   the sign change locates onset. **Load-bearing** — chaos is defined by λ>0.
3. **Sensitive dependence, shown directly.** ε-separated runs diverge exponentially
   in chaos, stay close when stable (the butterfly).
4. **Determinism preserved (chaos ≠ noise).** Identical IC → byte-identical run.
5. **Conservation holds (<1e-9) even in chaos.** Goods conserve while the
   trajectory is unpredictable.
6. **Literature match (qualitative).** Reproduces Sterman/Mosekilde:
   supply-line underweighting routes a beer-game chain to deterministic chaos.

## Scope discipline (v0 excludes)

* Deterministic demand only (noise OFF). The stochastic CYB-1 bullwhip is a
  separate regime; do not conflate.
* One control parameter (β) for the primary diagram; β×a_S map is a later nicety.
* Still 3 tiers, still the conserved physical flow from CYB-1 — swap only the
  ordering rule.
* The instruments (`lyapunov`, `bifurcation`) are **reusable deliverables** — build
  them clean and model-agnostic, not bolted to this one model.

## Instruments (the real deliverable)

* **Largest Lyapunov** — Benettin two-trajectory: evolve reference + perturbed,
  renormalize separation to `d0` each step, average `log(d/d0)` after transient.
  `λ>0 ⇒ chaos`.
* **Bifurcation diagram** — per control value: run long, discard transient, record
  asymptotic local maxima of a state variable; scatter control-vs-values.

## Implementer notes

* Deterministic demand (σ=0); perturb off the fixed point with a nonzero initial
  condition so the dynamics have something to evolve.
* Long runs + discard transients for both instruments (want the attractor, not the
  approach).
* **Required instrument self-test** (same discipline as CYB-1's frozen-forecast
  guard): logistic map at r=4 → λ ≈ ln 2 ≈ 0.693; period-doubling onsets near the
  Feigenbaum points. Trust the instrument before trusting its verdict.

## Deliverables

* `src/chaos/model.py` — CYB-1 chain + anchoring-and-adjustment rule (deterministic)
* `src/chaos/lyapunov.py` — largest-Lyapunov estimator (reusable)
* `src/chaos/bifurcation.py` — bifurcation-diagram sweeper (reusable)
* `src/chaos/run_v0.py` — bifurcation diagram, λ-vs-parameter, sensitive-dependence plot
* `src/chaos/figures/` — those figures
* conservation assert live in the chaotic regime
* `src/chaos/README.md` — the route to chaos, the λ sign-change, literature, and the
  explicit "measured chaos, not complication" statement

## Validation targets

* **Instrument self-test:** logistic r=4 → λ ≈ ln 2 ≈ 0.693; cascade reproduced.
* **Literature:** Sterman (1989) Management Science 35(3); Mosekilde & Larsen
  (1988) System Dynamics Review 4(1–2). Qualitative match is the bar.

---

## Outcome (shipped 2026-06-28)

All load-bearing criteria met; criterion 1 **earned a spec correction** (below).

Canonical regime: `a_S=0.7, L=3, θ=0.25`, σ=0, control = β swept 0.34→0.08.

| measurement | result |
|---|---|
| instrument self-test (logistic r=4) | λ = **0.69315** = ln 2 to 5 digits; period-2 window λ<0 |
| determinism | identical IC → **byte-identical** trajectory |
| conservation (chaotic regime) | relative residual **4.9e-15** (< 1e-9) |
| λ vs β | λ≈0 for β≳0.30; turns **positive near β≈0.26**, up to **+0.054 nats/step** |
| sensitive dependence | ε=1e-6 → **×10⁵** in chaos (β=0.15); **decays to 1e-11** when stable (β=0.32) |
| boundedness | attractor amplitude stabilizes (growth ≈ 1.0) — λ>0 on a *bounded* set |

- **β is the destabilizing control**, exactly as the behavioural story predicts:
  at high β even aggressive `a_S=1.3` stays stable; underweighting the supply line
  is what tips the chain over.
- **Route to chaos (named rigorously in `run_route.py`):** a **border-collision
  bifurcation of a piecewise-smooth map** (Zhusubaliyev & Mosekilde) — the
  equilibrium collides with the order/shipping saturation manifold while still
  linearly stable (leading complex pair tops out at |λ|≈0.91 ∠40°, never reaching
  the unit circle); a frequency-locked invariant loop is born (a hard jump, with
  bistability), then frequency-locks / period-doubles into a bounded strange
  attractor (λ>0).

### Route confirmations (criterion 6, added at close-out)
| confirmation | result |
|---|---|
| (a) eigenvalues at physical fixed point | leading complex pair \|λ\|≈0.83→0.91 ∠~40°, **never crosses 1**; FP loses feasibility at β≈0.294 → border collision, not Neimark–Sacker |
| (b) onset character | amplitude jumps **0 → ~525 over Δβ≈0.003**; **bistable** window β∈[0.295,0.298] (cycle coexists with stable FP) → hard / hysteretic, not soft Hopf |
| (c) geometry | delay embedding: frequency-locked points → **closed invariant loop** (riding the order≥0 constraint) → **strange attractor**; FFT: single line → subharmonic at f/2 → broadband |

**Two spec corrections this build earned.** Criterion 1 predicted a clean
period-doubling cascade (refuted). The close-out then predicted a smooth
**Neimark–Sacker** (discrete Hopf) — *also* refuted by direct measurement: the
eigenvalue pair never reaches |λ|=1 and the onset is a hard, bistable jump. The
honest mechanism is a **border-collision** in a piecewise-smooth map. The
load-bearing chaos claim (bounded + aperiodic + λ>0 + deterministic + conserved) is
unaffected; the route is sharper and more citable than either framing. See
[`../solutions/chaos-route-is-border-collision-not-smooth-hopf.md`](../solutions/chaos-route-is-border-collision-not-smooth-hopf.md).
