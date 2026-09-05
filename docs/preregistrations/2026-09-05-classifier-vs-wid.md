# Pre-registration — does the frozen model's regime structure track the WID distributional data?

> **Status: LOCKED (2026-09-05).** This document was written **blind to the WID series** — no WID
> values were examined in composing it — and its a-priori commitments (concentration → Fisher `α_p`,
> graded tipping-border, ordinal zero-fit mapping, independent crisis chronology) were signed off by
> Andy **before** this commit. **The commit that adds this file IS the lock:** nothing above the lock
> line may change hereafter. The WID evaluation is a *separate, subsequent* commit that references
> this one by hash and may not alter the rule; a change to the locked content voids the pre-registration.
>
> Companion to the thesis roadmap ([`docs/thesis/08-future-work-roadmap.md`](../thesis/08-future-work-roadmap.md))
> and the classifier arc (CYB-26…29). Governs the first honest test of the CYB-28 slow-manifold bet.

## The discipline (literal, from the egg solve — we do NOT fit functions to data)

This pre-registration mirrors, move for move, how the egg problem was solved without fitting:

- **The fitted parameter was removed, not tuned** — CYB-7 retired `replace_lag` and let the **real
  measured NASS flock series** drive timing (deseasonalized vs a *reference* period, the 2020-21
  normal); timing became **zero-parameter**. → *Here: the slow-variable driver is a real measured WID
  series; the model's regime border is frozen from mechanism. Neither is fit to the outcome data.*
- **At most one constant, calibrate-freeze-validate-OOS, never re-tuned** — the egg slope was
  calibrated on ep1, frozen, validated OOS on ep2, and its overshoot **reported honestly**
  (CYB-9). → *Here: the mapping is preferentially zero-constant (ordinal); if a scale is unavoidable
  it is calibrated on declared training country-eras, frozen, validated OOS, mismatch reported.*
- **Model shape defended by rejection, not fitting** — CYB-14 tested and **rejected** a saturation
  parameter (keep linear). → *Here: the border structure is the model's; we do not add degrees of
  freedom to make the data fit.*

---

## H — The hypothesis, stated a priori (the CYB-28 bet)

**Slowly-drifting distributional variables are the slow manifold that walks the fast model's
regime-parameter across its border.** Concretely, and committed before data:

- **Slow variable (the driver):** a real measured **WID wealth-concentration** series (top-10% /
  top-1% wealth share; secondarily the capital–income ratio) — normalized against a per-country
  *reference* baseline (mirroring the egg's 2020-21 normal), NOT against its own outcome. A
  *distributional* driver, matched on purpose to a *distributional* border (below), not to aggregate
  leverage.
- **Model regime-parameter it maps to:** the **markup-defense stabiliser `α_p`** of the
  conflict/Fisher stack (CYB-30) — the wage-price restoration mechanism that floors the price level
  and, when suppressed, opens the Fisher deflation channel.
- **Direction (a-priori sign, no free magnitude):** higher wealth concentration ⇒ **weaker
  wage-price restoration ⇒ lower effective `α_p` ⇒ closer to the Fisher deflation edge** (the 1930s
  intuition — concentrated, rentier-heavy economies lose the wage floor and turn debt-deflation-prone).
  *This mapping is the a-priori bet; it can be false, and a null falsifies it — see below.*

## F — What is FROZEN (from mechanism, not from WID)

- **The border** is the **`α_p` at which the CYB-30 sweep *tips*** from the bounded/inflationary
  regime toward the deflationary one — read from the model's own `α_p`-sweep (`src/fisher/`), **not**
  the degenerate `α_p→0` runaway corner (a corner, not a graded testable border), and **calibrated to
  no macro dataset**. **Distance-to-border** = distance in *effective* `α_p` to that tipping value.
- **The model parameters** are the mechanism/egg-validated values already in the repo, frozen.
- Nothing in F is (re)estimated from WID or from the outcome labels (below).

## M — The a-priori mapping (egg-slope-disciplined)

- **Preferred — zero-fit (ordinal).** Compare *ranks*: does a country-era's WID slow-variable rank
  (leverage/concentration) order the same way as the model's frozen distance-to-border predicts the
  fragility rank? No constant is estimated from WID; a rank/ordinal comparison cannot be "fit."
- **Only if a scale is unavoidable — one constant, egg-discipline.** Calibrate a single scale on a
  **declared training** set of country-eras (chosen by a coverage rule, *not* by their values),
  freeze it, validate OOS on the withheld set, and **report the mismatch honestly** even if it fails.
  Never re-tune.

## D — The decision rule (pre-registered — what counts as the model being right)

**Not** the trivial "more leverage → more crises" (which Minsky/Keen already argue and mainstream
half-concedes). The test is the model's **specific border structure**:

- **Primary metric:** a 2×2 contingency over the withheld country-eras — *(WID slow-variable
  above / below the model's frozen border) × (independent fragile / stable outcome)* — pre-registered
  to "succeed" only if above-border eras are the fragile ones at a rate that beats chance by a
  pre-stated margin (exact test + margin fixed here, before data).
- **Secondary metric:** rank correlation between the model's **distance-to-border** and the observed
  fragility ordering (Spearman ρ), with the sign and a minimum |ρ| fixed here.
- Both are **frozen before the withheld set is opened.**

## Outcome labels — INDEPENDENT of both WID and the model (no circularity)

"Fragile outcome" (a crisis / regime shift in a country-era) comes from a **pre-specified external
crisis chronology** (e.g. a Reinhart–Rogoff-style banking/debt-crisis list, named and fixed here),
**not** from WID and **not** from the model. This is the load-bearing anti-circularity guard: the
border is the model's, the driver is WID, the *outcome* is a third, independent source.

## S — The data split (fixed blind to WID values)

- **Training country-eras** (only if Option-B calibration is used): a small declared set chosen by a
  *coverage/availability* rule, listed here before any values are seen.
- **Withheld / validation set:** all remaining country-eras with adequate WID + chronology coverage —
  **untouched until D is locked.**

## The forbidden moves (we refuse these explicitly)

1. Fitting the mapping function to WID. 2. Choosing the border threshold post-hoc to maximize the
match. 3. Re-tuning anything after seeing the withheld result. 4. Relabeling "fragile" after the fact.
5. Swapping the slow variable or the metric after a null. Any of these voids the pre-registration.

## What a NULL result means (stated before the data)

If the frozen model + a-priori mapping does **not** track the independent outcomes on the withheld
set, the **CYB-28 slow-manifold hypothesis is falsified** (or the border is mis-placed) — a real,
reportable result, exactly like the egg magnitude *overshooting* OOS. We report it and do **not**
tune to rescue it. A null here is worth more than a fitted "success."

## Honest caveats (pre-stated)

- **Small-N.** Few clean country-eras; the reproducibility test is weak, and pre-registration is the
  only defence against fooling ourselves.
- **The mapping is the bet.** If distributional slow variables are *not* the ones that move the
  border, the probe fails honestly — which is itself the CYB-28 finding.
- **WID comparability** across a century + countries (Piketty's own caveat).
- **Scope:** this is a *correlation* of a frozen model against independent data — a domain-of-validity
  check, **not** a forecast-superiority claim (that bar is still [08](../thesis/08-future-work-roadmap.md)).

---

<!-- LOCK LINE — nothing above this line may change after the commit that locks this pre-registration.
     The WID evaluation is a separate document/commit that references this one by hash. -->
