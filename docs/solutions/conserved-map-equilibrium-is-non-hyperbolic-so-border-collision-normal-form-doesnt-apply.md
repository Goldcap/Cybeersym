---
title: "A stock-flow-consistent map's equilibrium is non-hyperbolic, so the Nusse–Yorke border-collision normal form does not apply — and the dimension reduction you'd reach for isn't a theorem"
category: modeling
tags: [chaos, border-collision, normal-form, nusse-yorke, banerjee-grebogi, jacobian, non-hyperbolic, stock-flow-consistency, dimension-reduction, piecewise-smooth, instrument-validation, method]
created: 2026-06-29
updated: 2026-06-29
severity: medium
component: src/chaos
problem_type: conceptual_pitfall
root_cause: theory_domain_of_applicability
tracking: CYB-4
---

# A conserved map's equilibrium is non-hyperbolic, so the border-collision normal form does not apply

CYB-2 named the conserved beer game's route to chaos a **border-collision** (four
empirical ways). CYB-4 set out to *formalize* it via the Nusse–Yorke piecewise-linear
normal form — compute the two one-sided Jacobians `J_L`, `J_R` at the collision and
name the type from theory. The honest result, earned by measurement, is that the formal
normal form **does not apply** — and saying *why*, rigorously, is the finding. It both
sharpens CYB-2 and is a reusable caution for every later mechanism on the conserved
ledger.

## Problem — the clean 2-D theory has a domain of applicability this system sits outside

The Nusse–Yorke / Banerjee–Grebogi normal form classifies a **hyperbolic fixed point
that crosses the switching manifold** as a parameter varies (`μ` through 0). Reaching
for it here looked natural after CYB-2. Three measurements show it cannot be applied:

1. **No boundary equilibrium.** The physical equilibrium never reaches a switching
   manifold. At the FP every tier orders exactly μ (flow balance — far from the
   `order≥0` border) and the stockout margin stays ≈129 (far from the ship border), for
   **all β through onset**. The FP is robustly *interior* to both manifolds. (Earlier
   intuition that "the FP loses feasibility / collides with the manifold" — in CYB-2's
   first-pass docstring — was imprecise; the careful measurement is interiority.)
2. **The equilibrium is non-hyperbolic, at every β.** The *full* 21-D spectrum (CYB-2
   tracked only the leading complex pair) carries **three eigenvalues pinned exactly at
   λ=+1**, eps-robust (identical at finite-difference step 1e-4/1e-6/1e-8). Their left
   eigenvector is the per-tier functional `on_order − Σ(in-transit)`: the **supply-line
   conservation law**. Stock-flow consistency shows up as a permanent 3-D **center
   subspace**. Everything else tops at |λ|≈0.92 and never crosses the unit circle. A
   non-hyperbolic FP has no border-collision normal form (and no smooth NS/flip/fold —
   nothing crosses).
3. **The N-D → 2-D reduction is not a theorem.** Projecting the ~21-D map onto a
   "dominant eigenplane" and applying the 2-D classification is *not* sanctioned —
   especially with a **complex** dominant pair (Simpson et al., *Phys. Lett. A* 2025:
   the only rigorous N-D robust-chaos reduction is to a 1-D skew tent map, and needs a
   dominant **real** eigenvalue). The probe makes it concrete: `J_L` and `J_R` differ in
   only two rows — the manufacturer's `on_order` (the λ=1 conservation direction) and
   its newest transit slot (a λ=0 deadbeat). The **oscillatory plane is identical across
   the border** (|λ|=0.945 ∠40° on both), so a 2-D normal form on the active mode sees
   *no* collision; a naive dominant-modulus reduction locks onto the λ=1 conservation
   mode and returns a degenerate, spurious verdict.

## Root cause — conservation is the obstruction

The very property that makes the model rigorous — **stock-flow consistency** — gives its
equilibrium neutral (conserved) directions, so the equilibrium is non-hyperbolic and
falls outside the standard piecewise-smooth classification. The conservation law is
load-bearing twice: it certifies the physics (goods conserve to <1e-9), and it places
the bifurcation beyond the boundary-equilibrium normal form. The onset is therefore a
**global, nonsmooth** event — a constraint-riding attractor born at finite amplitude,
**coexisting** with the still-stable equilibrium (bistability/hysteresis): a
border-collision (nonsmooth fold) **of the limit cycle**, not of the fixed point. This
is consistent with — and sharper than — CYB-2's settled "equilibrium stays stable, the
attractor coexists." See [[chaos-route-is-border-collision-not-smooth-hopf]].

## Solution

1. **Validate the formal classifier before pointing it at the model** (the discipline
   guard, as for `lyapunov.py` / `linearize.py`). `normal_form.py` reproduces three
   documented 2-D border-collision verdicts — robust chaos `(1.7,0.5,−1.7,0.5)`,
   period-doubling `(−1.43,0.5,−1.52,0.5)`, closed invariant curve `(0.3,0.5,0.5,1.5)` —
   before classifying anything.
2. **Track the *full* spectrum, not just the leading complex pair.** The λ=1 conservation
   triple is invisible if you only follow the oscillatory mode; it is the whole story.
3. **Find the equilibrium by iteration in the stable regime; use Newton continuation to
   follow it below onset, and check feasibility.** It stays feasible and interior below
   onset — iteration fails only because the basin collapses (the bistability), not
   because the FP is destroyed. (Same virtual-vs-physical-FP discipline as CYB-2.)
4. **State the domain of applicability honestly.** An accurate "the formal normal form
   does not apply here, for these three measured reasons" beats a forced 2-D fit. The
   spec explicitly licensed this, and the literature (Simpson 2025) independently backs
   the no-reduction point.

## Takeaways (how to apply)

1. **Check the theorem's hypotheses, not just its conclusion.** The border-collision
   normal form needs a hyperbolic boundary equilibrium. Verify *boundary* (is the FP on
   the manifold?) and *hyperbolic* (full spectrum off the unit circle?) before naming a
   type — both failed here.
2. **A conserved/SFC system is generically non-hyperbolic at its equilibrium.** Expect a
   center subspace (λ=1 per conservation law). This recurs for every Cybeersym mechanism
   on the conserved ledger — it will shape how each one bifurcates.
3. **Dimension reduction for border-collisions is mostly *not* available.** Do not
   project onto a dominant eigenplane and apply 2-D theory as if it were rigorous —
   especially with a dominant complex pair. Flag any such reduction as a heuristic.
4. **The onset of a coexisting attractor is not a local bifurcation of the equilibrium.**
   Bistability + a hard amplitude jump + an equilibrium that never destabilizes = a
   global/nonsmooth (cycle border-collision / nonsmooth fold), not a boundary-equilibrium
   event.

## References
- Code: `src/chaos/normal_form.py` (reusable classifier, self-tested); `bcb_classify.py`
  (the CYB-4 analysis: FP interiority + non-hyperbolicity + the one-sided-Jacobian probe);
  `linearize.py` (Jacobian / fixed-point finders); `model.py` (`step_vector`).
- Plan/spec: Linear CYB-4; builds on [[chaos-route-is-border-collision-not-smooth-hopf]].
- Nusse, H. E. & Yorke, J. A. (1992), *Border-collision bifurcations including "period
  two to period three"…*, Physica D 57(1–2):39–57; (1995) Int. J. Bifurcation & Chaos
  5(1):189–207.
- Banerjee, S. & Grebogi, C. (1999), *Border collision bifurcations in two-dimensional
  piecewise smooth maps*, Phys. Rev. E 59(4):4052–4061.
- Banerjee, S., Yorke, J. A. & Grebogi, C. (1998), *Robust Chaos*, Phys. Rev. Lett.
  80(14):3049–3052.
- di Bernardo, M., Budd, C. J., Champneys, A. R. & Kowalczyk, P. (2008),
  *Piecewise-smooth Dynamical Systems: Theory and Applications*, Springer (AMS 163).
- Simpson, D. J. W. (2016), *Border-collision bifurcations in ℝᴺ*, SIAM Review
  58(2):177–226; Simpson et al. (2025), *Three forms of dimension reduction for
  border-collision bifurcations*, Physics Letters A.
- Zhusubaliyev, Zh. T. & Mosekilde, E. (2003), *Bifurcations and Chaos in
  Piecewise-Smooth Dynamical Systems*, World Scientific (Series A, vol. 44).
