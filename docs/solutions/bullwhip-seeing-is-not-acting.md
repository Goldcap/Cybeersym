---
title: "Bullwhip: a known-mean forecast gives no amplification, and seeing ≠ acting"
category: modeling
tags: [bullwhip, supply-chain, recursion-channel, order-up-to, echelon-base-stock, method]
created: 2026-06-28
severity: medium
component: src/bullwhip
problem_type: conceptual_pitfall
root_cause: spec_modeling_error
tracking: CYB-1
---

# Bullwhip: a known-mean forecast gives no amplification, and seeing ≠ acting

Two modeling traps surfaced while building the bullwhip v0 module (`src/bullwhip`),
both caught by the project's standing discipline — *let real behavior refute the
spec; the correction is the finding.* Recording them so neither recurs.

## Problem

### Trap 1 — "fixed forecast" produces NO bullwhip (the spec's first framing)
The original spec asked for bullwhip from a 3-tier chain with a **constant**
order-up-to level `S` ("fixed forecast only"), expecting lead time alone to
amplify. Built exactly as written, it gives **ratio = 1.000 at every tier** — a
null. With a *known, stationary* mean, order-up-to passes demand through
one-for-one (`order_{t+1} = D_t`) for any lead time `L`. This is the textbook
result (Lee et al. 1997; Chen et al. 2000): base-stock with a known mean has no
bullwhip. The amplification *requires* demand-signal processing — each tier
**estimating** the demand mean from observed orders (a moving-average forecast),
which makes `S_t` move and double-respond to a demand blip.

### Trap 2 — "information sharing flattens the chain" (the spec's second framing)
The corrected spec then predicted: if every tier forecasts off **true consumer
demand** (`shared_info`), compounding goes **flat ≈ r**. The model refuted this
too — `shared` only *suppressed* compounding (~3×), it did not flatten it
(cumulative still rose 2.9 → 6.3 → 10.9).

## Root cause

There are **two** channels carrying distortion upstream, and sharing the forecast
fixes only one:

- **Forecast / information channel** — what a tier *sees* and forecasts from.
- **Physical replenishment channel** — a tier's order ≈ `received_orders + ΔS`.
  Even with a smooth, true-demand `ΔS`, the tier still physically replenishes the
  **distorted orders it received** from downstream (its installation inventory
  position is depleted by them). That variance passes straight through regardless
  of the forecast.

**Seeing true demand ≠ acting on it.** This is exactly the installation- vs
echelon-base-stock distinction in the inventory literature.

## Solution

Model **three** modes that turn each channel off in turn (separating *seeing* from
*acting*):

| mode | forecast from | replenish against | result |
|------|---------------|-------------------|--------|
| `local` | distorted received orders | installation position (distorted) | full compounding — **36.6×** |
| `shared` | true demand `D_t` | installation position (distorted) | suppressed, not flat — **10.9×** |
| `coordinated` | true demand `D_t` | echelon position depleted by true `D_t` | flat — **2.9×** |

The three-way contrast **decomposes** the bullwhip into a forecast channel
(`local→shared`, ~3.3×) and a physical channel (`shared→coordinated`, ~3.7×) —
comparable in size. `coordinated` lands at the single-stage Chen ratio (2.92),
flat across the chain: the compounding is gone. Implementation: order against
`coord_pos` where `coord_pos -= D_t; order = max(0, S_t - coord_pos); coord_pos
+= order`.

## Takeaways (how to apply)

1. **A model has no bullwhip without a forecast that updates.** If a supply-chain
   sim shows ratio ≈ 1, check whether the order-up-to target is constant — that's
   the `p → ∞` null, and it's a useful regression test (assert it stays ~1).
2. **Distinguish information from coordination.** "Share the data" (a forecast
   fix) and "change the policy" (an echelon-replenishment fix) are different
   interventions with comparable, separable effects. Don't collapse them.
3. **When a spec predicts an idealized outcome ("flat ≈ r"), report what the model
   actually does, not the prediction.** Here the refutation produced a sharper,
   more publishable result (a clean two-channel decomposition) than the original
   binary would have. Flag the divergence as a *question*, not a forced ✅.
4. The forecast-channel math to keep handy — Chen et al. (2000), single stage,
   MA window `p`, lead time `L`: `ratio = 1 + 2L/p + 2L²/p²` (use `L+1` to match a
   target that includes the review period).

## References
- Code: `src/bullwhip/` (`model.py` modes, `run_v0.py` three-way report).
- Plan: [`../plans/2026-06-28-feat-bullwhip-v0-recursion-channel-plan.md`](../plans/2026-06-28-feat-bullwhip-v0-recursion-channel-plan.md).
- Chen, Drezner, Ryan & Simchi-Levi (2000), *Quantifying the Bullwhip Effect in a
  Simple Supply Chain*, Management Science 46(3):436–443.
- Lee, Padmanabhan & Whang (1997), *The Bullwhip Effect in Supply Chains*, Sloan
  Management Review (the P&G Pampers case).
