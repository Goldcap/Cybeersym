---
title: "Retiring the one fitted parameter (replace_lag) with real NASS flock data: the TIMING was in the data all along (and improved), but the MAGNITUDE gap doubled — reported, not re-tuned"
category: modeling
tags: [empirical-validation, out-of-sample, real-data, nass, provenance, determinism, deseasonalization, honesty-firewall, epistemic-shift, replace-lag, eggs, method]
created: 2026-07-01
updated: 2026-07-01
severity: medium
component: src/data
problem_type: calibration_assumption
root_cause: fitted_parameter_proxying_for_real_data
tracking: CYB-7
---

# Retiring replace_lag with real flock data: timing was in the data; magnitude degraded honestly

CYB-7 removed the egg model's single fitted assumption — `replace_lag=12`, the
flock-replacement lag that made the *cull-flow*-derived synthetic deficit peak near the
observed price peak — by driving the model with the **real** USDA NASS monthly table-egg
layer-inventory series. This is the project's first crossing from clean-room (closed forms,
controlled experiments — provably correct) into **observational** data (noisy, revised,
confounded — plausible at best). The result splits cleanly, and the split is the finding.

## Problem — a fudged number where real data now exists

The cull data (a flow) peaks spring 2022, but the egg price peaked Jan 2023. The model
bridged that with `replace_lag=12`: cull now, replacement matures 12 months later, so the
reconstructed deficit peaks ~Jan 2023. It worked, but it was a fitted timing parameter —
the one soft spot. NASS publishes the flock **stock** directly, so the deficit needs no
reconstruction and no lag: the timing is already in the data.

## Root cause / method — deseasonalize against the pre-outbreak normal, then let it talk

Layer inventory has a strong recurring seasonal cycle (summer laying-drop + fall molt), so a
flat-baseline deficit reads every normal summer dip as a "shortage." The HPAI signal is the
shortfall **below the seasonal-normal flock**, where the normal is the pre-outbreak years
(2020-21, layers untouched) averaged by calendar month — the same detrend-calm-years method
the demand seasonality already uses. This also makes the real deficit structurally
comparable to the synthetic one (both are pure HPAI supply signals with seasonality removed;
seasonality enters the model only via demand).

## Solution / verdict (reported both ways — the point of the ticket)

- **TIMING survives and IMPROVES.** The deseasonalized real deficit peaks **2023-01** and
  **2025-03** — both real price peaks — with zero timing parameters; the synthetic lag=12
  path peaked 2022-12 for ep1 (a month early). Fed through the model (frozen params), both
  price-peak months land. Robust to the normal-year choice at the model level (ep2 exact
  everywhere; ep1 Jan/Feb-2023). `replace_lag` retired.
- **MAGNITUDE degrades — and we do NOT re-tune.** Real deficits are ~half the synthetic
  (ep1 7.6% vs 13.0%, ep2 12.1% vs 23.0%). With the frozen v0.6 pricer the model undershoots
  the peaks worse (ep1 +101% vs real +188%; ep2 +168% vs +272%), and the real-data
  price-per-deficit slope ~doubles (~13 → ~24 %/pt — the old ~13 was computed off the
  ~2x-too-large synthetic deficits). The pricer slope is left untouched; recalibrating it is
  a separate thread. **Retiring one fitted parameter is worthless if another silently absorbs
  the slack.**

## Takeaways (how to apply)

1. **A fitted parameter is often a proxy for data you don't have yet. Go get the data.** When
   `replace_lag` was retired against the real flock stock, the timing it was fitting for turned
   out to be genuinely present in the data — and more accurately than the fit. Prefer the real
   series over any calibrated stand-in for it.
2. **When you retire a fitted parameter, freeze everything else and report what breaks.** The
   honest verdict is split (timing↑, magnitude↓). If we had nudged the pricer slope to keep
   the magnitude looking good, the whole exercise would have been a wash. A
   degraded-but-honest result beats a preserved-but-fudged one.
3. **Real observational series need deseasonalizing against a pre-event normal before the
   anomaly is legible.** Use the same calm-years method already in the codebase; don't invent
   a new baseline per data source.
4. **Pin observational data for determinism.** NASS *revises* releases, so a live API call
   would silently break same-inputs→same-outputs. Cache the pull in-repo with query + units +
   pull date; keep a `fetch_live` reproducer that is verified against the cache (here: 78/78
   months, 0 mismatches) but never on the model path. Handle gaps/withheld cells explicitly —
   a missing month becoming a silent zero reads as a 100% flock deficit.
5. **Name the epistemic shift when you cross into the real world.** Clean-room results are
   provably correct; observational ones are plausible. State the claim narrowly — *the
   mechanism reproduces the episodes with real ingredients*, not *the model predicts prices*
   (the CYB-3 honesty firewall, now load-bearing rather than decorative).

## References
- Code: `src/data/nass_layers.py` (cached fixture + `seasonal_normal` + deseasonalized
  `real_flock_deficit_path` + `fetch_live` reproducer); `src/v09_real_flock.py` (OOS
  comparison + figure). Superseded soft spot: `src/data/hpai_culls.py` (`replace_lag`).
- Data: USDA NASS QuickStats, `CHICKENS, LAYERS, TABLE - INVENTORY`, national, HEAD,
  first-of-month; retrieved 2026-07-01. Price: FRED `APU0000708111` (`data/eggs_fred.py`).
- Plan: [`../plans/2026-07-01-feat-retire-replace-lag-real-nass-flock-plan.md`](../plans/2026-07-01-feat-retire-replace-lag-real-nass-flock-plan.md).
- Honesty firewall / illustrative-not-predictive stance: CYB-3 empirical grounding
  ([`bullwhip-seeing-is-not-acting.md`](bullwhip-seeing-is-not-acting.md) rhymes — a spec's
  idealized prediction refuted into a sharper, honest result).
