---
title: "feat: Retire replace_lag — drive the egg model with real NASS flock-inventory data"
type: feat
status: done
date: 2026-07-01
tracking: CYB-7
canonical_source: "Linear CYB-7 (https://linear.app/techno87/issue/CYB-7)"
depends_on: []
---

# feat: Retire replace_lag — drive the egg model with real NASS flock-inventory data

> **Canonical spec lives in Linear (CYB-7).** This file mirrors the spec into version
> control. Spec changes happen in Linear first, then sync here. Shipped outcome at the bottom.

## Goal

Replace the egg model's one calibrated assumption — `replace_lag=12`, the fitted
flock-replacement lag that made the *cull-flow*-derived synthetic deficit peak near the
observed price peak — with **real measured flock dynamics** from USDA NASS monthly
table-egg layer-inventory data, and test whether the out-of-sample validation **survives
the swap**. Turns "validated against price data with one fitted timing parameter" into
"driven by real flock data with no free timing parameter."

> **⚠ Scope:** the **egg model** (recursion/supply substrate + pricer), NOT the conflict
> layer (CYB-6). Separate workstream, separate commits.

> **⚠ Epistemic shift — clean-room → observational.** Everything prior (bullwhip, chaos,
> conflict) was validated against closed forms / controlled experiments: provably correct.
> Observational data is noisy, revised, confounded — plausibility, not proof. Claim stays
> **"the mechanism reproduces the episode with real ingredients," NOT "the model predicts
> egg prices."** (CYB-3 honesty firewall.)

## Acceptance criteria

1. **Data provenance verified + pinned.** Exact series (monthly table-egg layer inventory —
   not annual/all-chickens/broilers/hatching/total-incl-hatching); documented query, units,
   pull date; cached in-repo; reproducible/deterministic (no live call on the model path);
   suppressed/withheld cells + gaps handled explicitly.
2. **`replace_lag` retired** — replacement driven by observed inventory, not the fitted lag.
3. **OOS re-run with real data, reported honestly** — timing (peak ~Mar 2025) and magnitude
   bracket. **If the fit degrades, that's a FINDING — report it, do NOT re-tune to compensate.**
4. **Conservation still holds** (substrate unchanged; data only drives the flock deficit).
5. **Honesty firewall active** — document the epistemic shift; precise claim; link CYB-3.

## Deliverables

Cached NASS dataset (query + pull date + units); reproducible ingestion (pull → cache →
feed the model), no live calls in the deterministic path; the OOS comparison
(`replace_lag=12` vs real-data-driven) with the honest verdict; provenance + retirement +
epistemic-shift docs.

---

## Outcome (shipped)

Delivered `src/data/nass_layers.py` (cached fixture + `real_flock_deficit_path` +
`fetch_live` reproducer) and `src/v09_real_flock.py` (OOS comparison + figure). All five
criteria met.

1. **Provenance.** Series `CHICKENS, LAYERS, TABLE - INVENTORY`, NATIONAL, unit HEAD,
   FIRST-OF-MONTH; query + pull date (2026-07-01) documented; committed fixture verified to
   reproduce the live API exactly (**78/78 months, 0 mismatches**); **no gaps / no withheld
   cells** over 2020-01..2026-06 (documented, with a guard note against silent-zero months).
2. **`replace_lag` retired.** The model is driven by the real inventory deficit
   (deseasonalized vs the 2020-21 pre-outbreak normal — same calm-years method as the demand
   seasonality). No fitted timing parameter. `hpai_culls`'s lag path retained only for the
   side-by-side.
3. **OOS verdict — reported both ways.**
   * **Timing SURVIVES and improves:** real deficit peaks **2023-01** and **2025-03** (both
     price peaks) with zero timing parameters; the synthetic lag=12 path peaked 2022-12 for
     ep1 (a month early). Model, fed the real deficit, lands both price-peak months. Robust
     to the normal-year choice at the model level (ep2 exact everywhere; ep1 Jan/Feb-2023).
   * **Magnitude DEGRADES — not re-tuned:** real deficits are ~half the synthetic (ep1 7.6%
     vs 13.0%, ep2 12.1% vs 23.0%), so the frozen v0.6 pricer undershoots the peaks worse
     (ep1 +101% vs real +188%; ep2 +168% vs +272%) and the real-data price-per-deficit slope
     ~doubles (~13 → ~24 %/pt). Pricer slope left untouched by design; recalibration is a
     separate open thread.
4. **Conservation** — substrate unchanged; `model.step()` asserts stayed green through the run.
5. **Honesty firewall** — epistemic shift + precise claim (mechanism reproduces episodes with
   real ingredients; not price prediction) documented in `v09` and `nass_layers.py`; CYB-3 linked.

Learning: [`../solutions/replace-lag-retired-timing-was-in-the-flock-data.md`](../solutions/replace-lag-retired-timing-was-in-the-flock-data.md).
