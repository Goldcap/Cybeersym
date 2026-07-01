---
title: "feat: Recursion × conflict coupling v0 — super-additive ignition"
type: feat
status: done
date: 2026-07-01
tracking: CYB-10
canonical_source: "Linear CYB-10 (https://linear.app/techno87/issue/CYB-10)"
depends_on: [CYB-2, CYB-6]
---

# feat: Recursion × conflict coupling v0 — super-additive ignition

> **Canonical spec lives in Linear (CYB-10)** (design forks resolved in chat). Mirror
> into version control. Shipped outcome at the bottom.

## Goal

Couple the two *transmission* channels minimally — recursion (CYB-1/2 supply chain)
and conflict (CYB-6 wage–price claims) — and test **H1, super-additive ignition**: can
the chain's amplification push a shock that *neither channel alone* would ignite across
the conflict layer's `g=0` threshold into a sustained wage–price spiral?

## Design resolution (forks closed in chat)

- **Direction:** one-way, recursion → conflict (bidirectional is a follow-up).
- **Coupling:** `ω_f(t) = ω_f0 − κ·d(t)` ⇒ `g(t) = g0 + κ·d(t)` — the chain's deficit
  `d(t)` raises conflict's control parameter `g` (firms want more margin when scarce).
  `ω_w` held fixed; `κ=0` decoupled.
- **Headline:** H1 (super-additive ignition). H2 (chaos-leakage) and bidirectional are
  follow-ups.
- **Structure:** single good; two separate conservation asserts (don't pre-specify a
  combined law); nonsmooth-border dominance measured, not pre-specified.

## Acceptance criteria

1. Super-additive ignition characterized (map `(shock/β, κ)`; coupled vs conflict-alone
   vs recursion-alone) — report whether the coupled threshold is genuinely lower.
2. Both conserved substrates green simultaneously (goods; shares) `< 1e-9`, incl. ignited.
3. Decoupling regression: `κ=0` reproduces CYB-2 and CYB-6 exactly.
4. Dynamics characterized empirically (instruments); which nonsmooth border dominates.
5. Determinism.

---

## Outcome (shipped)

Delivered `src/coupling/{model.py, run_v0.py, README.md, figures/}`. All five criteria met.

1. **Super-additive ignition — YES.** With the conflict layer subthreshold (`g0=−0.05`):
   conflict alone (`κ=0`) dissipates; recursion alone has no nominal channel; a stable
   chain (`β≳0.30`) never ignites (`d≈0`). The **coupled** system ignites for `β≲0.30,
   κ≳0.10`, `π*` up to `0.9 %/step` — inflation emergent from a pair whose parts don't
   inflate. Mechanism shown explicitly: `d(t)` drives `g(t)=g0+κ·d(t)` repeatedly across 0.
2. **Both substrates conserved** to `< 2e-15` throughout, including the ignited/chaotic regime.
3. **Decoupling regression byte-identical** (`κ=0` reproduces CYB-2 + CYB-6 to `0.0`).
4. **Dynamics:** coupled `λ=+0.039` = chain-alone `λ` (real chaos pervades — one-way
   coupling); `π(t)` aperiodic (H2 preview: chaos **does** leak into the nominal path,
   the opposite of standalone conflict's stable node); both nonsmooth borders live
   (wage floor 59%, chain stockout 26%).
5. **Determinism** — σ=0, pure functions, byte-identical reruns.

**Spec refinement (surfaced):** ignition is set by the amplification **regime (β)**,
not the shock size — the sustained rate is ~invariant across a 20× shock range, because
the bullwhip deficit is a self-sustaining attractor. A *transient* amplified shock
dissipates; only recursion's **endogenous instability** supplies the *persistent*
scarcity that holds `g>0`. So the ignition axis is `(β, κ)`, a measured refinement of
the spec's `(shock, κ)`.

Learning: [`../solutions/coupling-super-additive-ignition-persistent-not-transient.md`](../solutions/coupling-super-additive-ignition-persistent-not-transient.md).
