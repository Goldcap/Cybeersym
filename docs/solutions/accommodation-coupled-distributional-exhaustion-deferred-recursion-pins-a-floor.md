---
title: "On the coupled substrate the distributional rate-channel no longer self-exhausts (recursion re-loads its target every period) — but it also never wins: recursion pins a positive inflation floor k·κ·⟨d⟩ the rate can't reach through any channel, so the rate turns redistributive-not-stabilising; and the rate gates super-additive ignition both ways (cost-push lowers the coupling threshold, disinflation raises it)"
category: modeling
tags: [accommodation, coupling, recursion, conflict, endogenous-money, channel-decomposition, distributional-channel, cost-channel, ignition, super-additive, inflation-floor, solvency-ceiling, switching-manifold, decoupling-regression, inheritance-build, discipline-guard, method]
created: 2026-07-02
updated: 2026-07-02
severity: medium
component: src/accommodation_coupled
problem_type: conceptual_insight
root_cause: substrate_changes_a_self_limiting_mechanism_into_a_floored_one
tracking: CYB-18
---

# The distributional channel stops self-exhausting under reloading — and stops winning too

CYB-18 is an **inheritance build**: CYB-17's accommodation machinery (finance the wage bill at
a rate `i`; three rate-channels; a solvency ceiling) dropped *unchanged* onto CYB-10's coupled
recursion×conflict substrate, where a conserved supply chain amplifies a deficit `d(t)` that
re-loads the aspiration gap `g(t)=g0+κ·d(t)`. Two findings, both about how **a substrate change
converts a self-limiting mechanism into a floored one** — and both of the "reveal what was
load-bearing" kind the project keeps producing.

## Finding 1 — the distributional channel's self-exhaustion was a property of the *static* substrate

On bare CYB-6 (CYB-17) the **distributional** channel drove `π*` cleanly to **zero**: it lowers
workers' target `ω_w` by `distrib_a·slack`; once that covers the static gap `g0`, the gap is
closed, labor's claim is broken, `g` stops responding, and the channel's marginal disinflation
**decays to 0**. That decay is what let the **cost** channel take over at high `i` (the
restraint-insufficient / cost-flip region).

Change the substrate and the mechanism changes character. Recursion re-supplies the gap **every
period** via `κ·d(t)`, so the distributional channel never runs out of gap to work on — the
exhaustion is **deferred**. But it also **never wins**: it can neutralise the static `g0`, never
the recursively-reloaded portion. Its clean zero is replaced by a **positive inflation floor**

> **floor ≈ k·κ·⟨d⟩** (here 0.91 %/step) — inflation the rate cannot reach through *any* channel.

Measured, channel-isolated at `i=0.20` (where the bare channel is fully exhausted): bare
**−0.00 %/step** (→0) vs coupled **+0.93 %/step** (≈ `k·κ·⟨d⟩`). And the restraint-insufficient /
cost-flip region **survives and is hotter** — recursion lifts the whole `π*(i)` surface
(baseline +1.50→+2.43 %/step), so a cost-dominant mix runs hotter and **no rate drives inflation
to zero**. The disciplined read: on the faithful stack the rate is **even less a stabiliser and
more a redistributive tool** — you can cool the spiral but not extinguish it while recursion
keeps re-supplying scarcity. The single most transportable lesson: **a mechanism that
self-limits on one substrate can become floored (never-zero) on a richer one — re-test every
"it decays away" result when you change what feeds it.**

## Finding 2 — the rate gates super-additive ignition, both ways

CYB-10's headline was super-additive ignition (a subthreshold conflict layer ignites only once
the chain's amplification `κ ≥ κ*` pushes `g` past 0). Financing moves the threshold `κ*(i)`,
and the direction is set by the channel mix — the **same tug-of-war as Finding 1, at the
ignition margin**:

- **rate off** → `κ* = 0.10`, flat: **exactly the CYB-10 baseline** (a clean check that the rate
  acts *only* through its three channels).
- **cost-leaning** → `i` **lowers** `κ*` (0.10 → 0.00): cost-push self-ignites the spiral with
  **no coupling at all**.
- **disinflation-leaning** → `i` **raises** `κ*` (0.10 → 0.17): you can **choke ignition at the
  financing stage**.

So "does accommodation gate ignition?" has no single answer — it gates it in whichever direction
the dominant channel points. Build fewer than all three channels and you'd have manufactured a
one-directional verdict.

## Why it's trustworthy (the validations)

- **TWO byte-exact decoupling anchors, one per composition axis.** `κ=0` reproduces CYB-17
  (`W,P,D` to `0.0`); `i→0, D_max→∞, cost-off` reproduces CYB-10 (chain ⊕ conflict to `0.0`,
  including the ignited regime). Two axes of composition, one anchor each → nothing leaked
  beyond the two already-validated interactions. (Getting `κ=0` byte-exact required *skipping*
  the reload when decoupled — recomputing `gap0 = ω_w0 − ω_f0` re-rounds `0.10` by 1 ULP; the
  honest expression of "κ=0 is fully decoupled" is to not touch the base at all.)
- **All three conservation laws green simultaneously** — goods (chain) + three-way income
  `wage+interest+retained=1` + debt bookkeeping — worst residual `1e-15` in the
  ignited/coupled/financed regime.
- **The solvency ceiling completes the switching-manifold set live (three borders at once)** and
  **pre-empts** the wage floor: it caps the wage push first (73% of steps) so the floor rarely
  binds (6%); stockout (26%) is the ever-present recursion substrate. The borders **interact**.

## Takeaways (how to apply)

1. **A self-limiting result is a property of the substrate, not the mechanism — re-test it when
   you change the substrate.** "The distributional channel exhausts to zero" was true on bare
   CYB-6 and false (deferred + floored) the moment recursion re-loaded the gap. Ask of any
   "it decays away / saturates / self-corrects" finding: what was holding the driver still?
2. **When a policy tool has multiple channels, its *gating* direction is also a tug-of-war.**
   Ignition-gating, like the steady-state decomposition, flips sign with the channel mix; report
   which dominates rather than picking one.
3. **Two composition axes ⇒ two anchors.** An inheritance build that merges two validated models
   should recover *each* parent in *its* decoupling limit, byte-exact. One anchor proves half.
4. **Byte-exactness can hinge on not re-deriving an invariant.** If a quantity is unchanged in a
   limit, leave it literally untouched rather than recomputing it through algebra that re-rounds.

## References
- Code: `src/accommodation_coupled/model.py` (`AccommodationCoupledEconomy` — composes
  `ChaosChain` + `AccommodationEconomy` unchanged via the CYB-10 reload `g=g0+κ·d`);
  `src/accommodation_coupled/run_v0.py` (two anchors → coupled decomposition → ignition-vs-rate
  → three borders).
- Plan: [`../plans/2026-07-02-feat-accommodation-coupled-v0-distributional-exhaustion-under-reloading-plan.md`](../plans/2026-07-02-feat-accommodation-coupled-v0-distributional-exhaustion-under-reloading-plan.md).
- The two parents: accommodation [[accommodation-runaway-was-full-accommodation-limit-rate-is-a-tug-of-war]] (CYB-17);
  coupling [[coupling-super-additive-ignition-persistent-not-transient]] (CYB-10). Substrate:
  conflict [[conflict-channel-is-nominal-level-instability-not-real-chaos]] (CYB-6).
- Forward-links: the Minsky crunch off the solvency border (CYB-19); reflexivity / expectations
  (CYB-20). Endogenous money / horizontalism (Moore; Kaldor; Lavoie); circuit theory (Graziani);
  cost channel (Barth & Ramey 2001); conflicting claims (Rowthorn 1977; Lavoie).
