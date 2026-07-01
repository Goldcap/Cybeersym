---
title: "Coupling recursion × conflict: inflation is super-additive (emergent from a pair whose parts don't inflate), and ignition needs recursion's ENDOGENOUS instability — a transient amplified shock dissipates; only persistent scarcity holds the threshold"
category: modeling
tags: [coupling, integration, super-additive, emergence, recursion, conflict, ignition-threshold, persistent-vs-transient, decoupling-regression, conservation, lyapunov, chaos-leakage, method]
created: 2026-07-01
updated: 2026-07-01
severity: medium
component: src/coupling
problem_type: conceptual_insight
root_cause: model_structure
tracking: CYB-10
---

# Coupling recursion × conflict: super-additive ignition, and it needs *persistent* scarcity not a transient shock

CYB-10 is the first integration of two previously-isolated channels — recursion (the
CYB-1/2 supply chain) and conflict (the CYB-6 wage–price layer) — coupled one-way
through `d → ω_f → g`: the chain's scarcity `d(t)` lowers firms' target wage share,
raising the conflict aspiration gap `g(t) = g0 + κ·d(t)`. Two findings, both cleaner
than expected.

## Finding 1 — inflation is super-additive (emergent from the pair)

With the conflict layer held **subthreshold** (`g0 = −0.05`, dissipates on its own):

- **conflict alone** (`κ=0`): dissipates — no inflation.
- **recursion alone** (the chain, no conflict): amplifies goods flows, but has no
  nominal channel — no inflation.
- **coupled** (`κ ≳ 0.1`, chain in its amplifying regime): a **sustained wage–price
  spiral**, `π*` up to ~0.9 %/step.

So the coupled system inflates in a region where *neither ingredient does*. The
combined ignition threshold is strictly lower than either channel's alone —
**super-additivity**. Inflation here is not "present in one channel and amplified by
the other"; it is **emergent from the interaction**. This is the sharpest realization
of the project thesis: a cost shock, amplified through the chain, igniting a spiral it
could not have lit alone.

## Finding 2 — it needs recursion's ENDOGENOUS instability, not a big shock

Ignition is controlled by the amplification **regime** (β, the supply-line weight),
**not** by the shock size: the sustained rate barely moves (`≈0.33–0.38 %/step`) across
a 20× range of initial shock. The reason is structural — the bullwhip deficit is a
**self-sustaining attractor**, not a decaying transient. Consequences:

- A **stable** chain (β high) produces `d≈0` in steady state → **no ignition at any κ**.
  A one-off amplified shock rings and dies; the conflict wage floor dissipates it.
- An **unstable** chain (β low, the bullwhip/chaos regime) supplies **persistent**
  scarcity that holds `g>0` much of the time → ignition.

So recursion doesn't merely *amplify* the trigger — it **sustains** it. The
super-additive story is really "endogenous instability provides persistent forcing;
the threshold nonlinearity rectifies it into a spiral." (This refined the spec's
`(shock, κ)` framing to `(β, κ)` — surfaced to the spec author, not silently absorbed.)

## Why it's trustworthy (the validations)

- **Decoupling regression is byte-identical.** At `κ=0` the coupled model reproduces
  CYB-2 (chain subspace) and CYB-6 (conflict subspace) to `0.0`. With no closed form
  for the interaction, the two decoupling limits ARE the ground truth — and they hold
  exactly, so the composition introduced nothing but the intended coupling. *This is
  the single most important check when integrating two validated modules.*
- **Two conservation laws hold at once**, `< 2e-15`, through the chaotic ignited
  regime — goods (recursion) and wage+profit share (conflict) simultaneously.
- **Instruments confirm the character:** coupled `λ = chain-alone λ = +0.039` (real
  chaos pervades, as one-way coupling predicts), and `π(t)` is aperiodic — the chain's
  real chaos **leaks into the nominal inflation path** (a preview of the H2 ticket),
  the opposite of standalone conflict's clean stable node.

## Takeaways (how to apply)

1. **When integrating two validated modules, the decoupling regression is the spine.**
   Prove the composition reproduces each part exactly at zero coupling before trusting
   anything about the interaction. Byte-identical or bust — a near-miss means a leak.
2. **Emergence is worth isolating as its own claim.** "Neither alone, but coupled yes"
   is a stronger and more surprising result than "one channel amplifies the other."
   Design the baselines (each channel solo) so the emergence is unambiguous.
3. **Distinguish amplification from persistence.** A channel that amplifies a transient
   is not the same as one that *sustains* forcing. Threshold mechanisms downstream care
   about persistence, not peak — a big transient that decays won't cross a rectifying
   threshold into a self-sustaining regime; a smaller persistent one will.
4. **Let the coupling variable be the downstream control parameter, not an additive
   forcing.** Routing `d` into conflict's *gap* `g` (a bifurcation parameter) tests
   ignition; routing it as an additive cost-push into the price would only have injected
   exogenous inflation without testing the threshold. Couple into the knob that decides
   the regime, if you want to test a regime change.

## References
- Code: `src/coupling/model.py` (`CoupledEconomy`, one-way `d → ω_f → g`, both asserts
  live); `src/coupling/run_v0.py` (decoupling regression → ignition map → mechanism →
  shock-independence → dynamics). Reuses `src/chaos/*` (unchanged) + `src/conflict/*`
  (unchanged) + the CYB-2 instrument suite.
- Plan: [`../plans/2026-07-01-feat-coupling-v0-recursion-conflict-super-additive-ignition-plan.md`](../plans/2026-07-01-feat-coupling-v0-recursion-conflict-super-additive-ignition-plan.md).
- The two coupled channels: recursion route-to-chaos
  [[chaos-route-is-border-collision-not-smooth-hopf]]; conflict nominal-vs-real
  [[conflict-channel-is-nominal-level-instability-not-real-chaos]]. H2 (chaos-leakage)
  and bidirectional coupling are the flagged follow-ups.
- Sterman (1989); Mosekilde & Larsen (1988); Rowthorn (1977); Lavoie; Weber & Wasner (2023).
