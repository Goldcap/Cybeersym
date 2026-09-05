# Verification answer — CYB-23: is the "inflationary, not deflationary" collapse *conditional*?

**Short answer: YES — the reconstruction holds on the first two points, and Phase 2b now answers
the third more precisely (and more usefully) than first thought.** The CYB-23 headline was
Engine-1-only and honest; and having built the genuine Fisher price channel (Phase 2b), we can
tell a Minsky/Keen-orbit economist exactly *why* debt-deflation does not spontaneously ignite in
this model — a **structural** reason, not a swept-under-the-rug one. We did **not** ignore the
Fisher condition.

> **Correction note.** An intermediate Phase-2b write-up claimed a clean "two-basin map" with a
> deflation threshold φ\*≈1.63. On the proper-proof pass that turned out to be a **detector
> artifact** (the −25%/step tripwire freezing a bounded oscillation and calling it collapse). The
> corrected finding below is stronger and is what should go into any outreach.

## The three points, checked against the code

**1. Was the Fisher / price-level engine gated OFF in the CYB-23 headline runs? — YES.**
`ContagionParams.fisher_on` defaults to `False` (`src/contagion/model.py:67`), and the
impairment-horizon map never sets it. So the entire CYB-23 headline is **Engine 1 only** —
credit-quantity, the impaired rentier's risk premium `i_eff = i + ε·(impairment/P)`.

**2. Was the demand/price channel verified too weak to pull the price level negative? — YES,
exactly, and for a structural reason.** CYB-17's demand channel is a *symmetric multiplicative
damper* — `damp = max(0, 1 − demand_b·slack)` scales **both** `α_w` and `α_p` toward zero. It can
shrink the spiral to nothing but cannot flip its sign, so π approaches 0 **from above**. Deflation
was **unreachable by construction** in CYB-23, not merely unobserved.

**3. Does a genuine, strengthened Fisher price channel produce debt-deflation? — Only when the
conflict-layer stabilizer is suppressed.** This is the corrected, load-bearing result.

## What Phase 2b actually shows (`src/fisher/`)

Phase 2b replaces the crude switch with a genuine Fisher loop — distress (`D/P > b_ref`) →
distress selling cuts `P` → the cut **raises** the real burden next period → more selling. Then we
attacked it the way a skeptic must: **lift the collapse detectors and ask whether `P` actually
runs away.** Findings (all from `src/fisher/run_v0.py`; conservation ≤ 1e-16; determinism
byte-exact; `fisher_phi=0` ⇒ byte-exact CYB-23):

- **At the shipped configuration it is a BOUNDED LIMIT CYCLE, not a runaway.** With detectors
  lifted, the running-min `log P` is byte-identical across the first and last 1000 steps of a
  5000-step run **for every φ up to 20** (non-secular ⇒ no divergence). A falling `P` raises
  `ω = W/P`, so the conflict layer's markup-defense pushes `P` back up — it is a **structural
  price floor**. The earlier "φ\*≈1.63 threshold" was just where the cycle's down-swing first
  crosses −25%/step; unfrozen, φ=1.8 sits at `P≈0.9` forever.
- **Genuine Fisher debt-deflation exists, but requires the stabilizer OFF.** Over the `(α_p, φ)`
  plane (α_p = markup-defense strength), genuine divergence (`D/P → ∞`, `P → 0`) appears **only on
  the `α_p → 0` edge** (there for `φ ≳ 2`); for any working markup layer (`α_p ≥ 0.025` tested) it
  is bounded at every φ. The isolated Fisher map is *always* unstable
  (`u ← u·(1+φ·b_ref)`), so the markup-defense is the *only* thing preventing runaway — **the
  stabilizer, not φ, is the pivot.**
- **The genuine divergence is the LOOP, not the cut.** A frozen-leverage regression stays bounded
  at α_p=0, φ=2,4,8 where the live self-reinforcing loop diverges.
- **The SFC point.** Conservation holds to **1e-16 through a genuine deflationary runaway**
  (`D/P: 1 → 1.4×10⁶`), because the nominal capital-account identity is *P-independent*.
  Debt-deflation is a **real-burden runaway** under an *exact* balance sheet — a clean, defensible
  SFC framing.

## The single most honest one-sentence characterization

> The genuine Fisher debt-deflation loop, composed on a conflict/markup economy, does **not**
> produce a runaway at the shipped configuration — the wage-price markup-defense (a falling `P`
> raises `ω=W/P`, so firms push `P` back up) acts as a **structural price floor**, leaving a
> bounded (if severely depressed) limit cycle; genuine `D/P → ∞` debt-deflation opens only as that
> stabilizer is suppressed (`α_p → 0`), so *"inflationary, not Fisher"* is a **structural property
> of the conflict economy, not a weak-price-channel accident and not a refutation of
> debt-deflation.**

## Bottom line for the outreach

This is *safer and stronger* than a "we reproduced Fisher" claim. The Fisher condition is engaged
head-on: we wired the loop, tried hard to ignite it, and found a **structural** reason it doesn't
run away in a conflict economy — with a mapped `(α_p, φ)` boundary and SFC balance-sheet
consistency holding through a genuine divergence. Nothing overclaims; a reviewer who lifts the
detectors will find exactly what we report.

*(Filing note: mirror this on CYB-23 in Linear, and file Phase 2b as its own ticket linking
`src/fisher/`. Linear MCP was unreachable at write time, so this lives in the repo for now.)*
