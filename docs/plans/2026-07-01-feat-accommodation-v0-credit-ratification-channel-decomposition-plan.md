---
title: "feat: Accommodation channel v0 — credit ratification of the nominal spiral + the rate's channel decomposition"
type: feat
status: done
date: 2026-07-01
tracking: CYB-17
canonical_source: "Linear CYB-17 (https://linear.app/techno87/issue/CYB-17)"
depends_on: [CYB-6]
---

# feat: Accommodation channel v0 — credit ratification + the rate's channel decomposition

> **Canonical spec lives in Linear (CYB-17)** (forks resolved in chat). Mirror into
> version control. Shipped outcome at the bottom.

## Goal

The first **sustaining** channel. Add money/credit accommodation to the bare CYB-6 conflict
spiral, with a **policy rate `i`** as the conditioning parameter, and test two things
neutrally: **H1a** — once the wage bill must be financed, is CYB-6's unbounded runaway still
unconditional, or does a high enough `i` bound it? **H1b** — when `i` moves inflation,
through which channel (cost / demand / distributional)? The **channel decomposition** is the
headline; every outcome is a legitimate finding.

## The reframe

CYB-6's unbounded runaway was produced with no money/credit — it was the **full-accommodation
limit** (financing costless & unconstrained), a hidden assumption, not a law. Financing the
wage bill at a rate names that constraint. (The same move as CYB-2 order non-negativity,
CYB-4 conservation clamp, CYB-6 wage floor: reveal the hidden switching manifold.)

## Design resolution (forks closed)

Bare CYB-6 substrate; horizontalist money regime (rate lever, quantity endogenous) + a
monetarist `μ`-cap comparison switch; working-capital / wage-fund finance; **all three rate
channels** (cost / symmetric-demand / distributional-asymmetric) with tunable strengths + a
decomposition; passive rentier-bank pool with extended three-way flow conservation; a
solvency ceiling `D/P ≤ D_max` as the nonsmooth border (Minsky cascade deferred).

## Acceptance criteria (all met — see outcome)

1. H1a characterized; boundary in `(i, g)`. 2. H1b channel decomposition (headline). 3. A
restraint-insufficient region reachable (explicit). 4. Full-accommodation limit recovers
CYB-6 exactly. 5. Extended conservation throughout. 6. Solvency ceiling as border; border
dominance. 7. Monetarist-knob comparison. 8. Determinism.

## Discipline guard

Restraint present ≠ restraint sufficient — the model MUST reach a spiral that outruns the
rate. Do NOT spec toward "the rate is distributional." Keep "orthodox tool misaimed" distinct
from "heterodox tools work better" (not built here).

---

## Outcome (shipped)

Delivered `src/accommodation/{model.py, run_v0.py, README.md, 4 figures}`. All eight met.

1. **Full-accommodation-limit regression byte-identical** (`i→0`, cost off: `0.0` vs CYB-6,
   incl. the unbounded runaway; costless steady state = Rowthorn–Lavoie `π* = k·g`).
2. **Channel decomposition (headline).** The three channels pull in **opposite directions**
   (at `i=0.10`, base π*=1.5%/step): cost **+2.5** (feeds), demand **+1.05** (cools
   symmetrically), distributional **+0.75** (cools by breaking labor, → 0). The net is a
   **tug-of-war set by the relative strengths** — not rigged toward any winner. Only the
   distributional channel closes the gap; demand only scales the rate; cost feeds.
3. **H1a — the runaway is conditional.** A high `i` bounds it **only if disinflation
   dominates cost**. Restraint-insufficient region reached explicitly (cost-dominant, `i=0.20`:
   π* = +3.07%/step — the spiral outruns the rate).
4. **Extended conservation** `wage + interest + retained = 1` and `ΔD = borrowing − repayment`
   to `≤ 2e-16`, mid-spiral and mid-choke.
5. **Solvency ceiling completes the switching-manifold set** (order non-negativity → wage
   floor → solvency); binds when the financeable wage share is capped (ridden bind/release,
   echoing CYB-2). Governs a different region than the wage floor.
6. **Monetarist knob: inert as a lever, real as a crunch.** Capping money growth *does* bound
   the cost-fed spiral (2.5 → 0.5%/step) — but only via **rationing** (a credit crunch), not
   a clean nominal lever. The horizontalist point, shown not asserted.
7. **Determinism** — byte-identical reruns.

Learning: [`../solutions/accommodation-runaway-was-full-accommodation-limit-rate-is-a-tug-of-war.md`](../solutions/accommodation-runaway-was-full-accommodation-limit-rate-is-a-tug-of-war.md).
