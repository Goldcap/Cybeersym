# CLAUDE.md

Guidance for Claude Code working in this repo. Read `HANDOFF.md` first (the *why* and
live decisions), then `CHANGELOG.md` (the version-by-version arc — each version is one
finding). This file is the operational layer: how to run things, the layout reality, and
the discipline that must not be violated.

## What this is
Agent-based, stock-flow-consistent (SFC) simulation for testing **structural** inflation
hypotheses. A wind tunnel, not a crystal ball. Working commodity: **eggs** (2022-23 &
2024-25 US HPAI price spikes). Econometrics is the *referee* (out-of-sample validation),
never the engine. numpy + matplotlib only.

## Layout — run from inside `src/`
All code lives under `src/`. The scripts import siblings directly (`from model import …`,
`from data.hpai_culls import …`) with no `sys.path` shims, so they only resolve when run
from **inside `src/`**:
```bash
pip install -r requirements.txt        # numpy, matplotlib
cd src
python3 v06_oos_test.py                # out-of-sample validation (both episodes)
python3 v08_wedge.py                   # the distributional wedge
```

## Architecture (the seams are the point — validate *at* them, not mid-loop)
- `src/model.py`   — SFC engine. Conservation asserts (money + egg residuals < 1e-10) are
  the crown jewel; 5 income quintiles; supplier→store→household pipeline; seasonal-demand
  hook; commodity-pricer dispatch. The engine is **commodity-blind**.
- `src/pricers.py` — commodity pricer registry. A pricer is a PURE function
  `(flow_gap, prev_markup, *, deficit, **knobs) -> markup`. `EGG_PRICING` = `linear_deficit`,
  slope ≈ 13. The price-vs-scarcity **slope is a commodity property, not an engine
  constant** — never push pricing knobs back into the engine.
- `src/events.py`  — adverse-event plugin layer: pure supply/demand path-transforms,
  multiplicative composition, registry, load-time validation. `### TODO(cost-matrix)` seam.
- `src/data/`      — real fixtures: FRED egg prices, USDA culls + flock transform, seasonality.
- `src/vNN_*.py`   — one analysis script per version; each regenerates `src/figures/cybeersym_vNN_*.png`
  and prints its result.

## Validated state — build on this, don't re-derive
- **Conservation** holds to <1e-10. If the `model.py:step()` asserts ever fire, STOP and
  fix — a leak invalidates everything downstream.
- **Timing validated out-of-sample**: same model + same params reproduce both the 2022-23
  (peak Jan 2023) and 2024-25 (peak Mar 2025) peaks. 2024-25 was never fit.
- **Magnitude** bracketed by the single egg slope, ~linear and mildly *saturating* — NOT
  convex (that was an artifact of pricing off `1/(1-deficit)`). Slope recalibrated against
  the **real** NASS deficit: **~24%/pt** (`EGG_PRICING["slope"]=24.1`, CYB-9), calibrated on
  ep1 (2022-23). The old ~13 was calibrated off the ~2×-too-large *synthetic* deficit — a
  compensating-error pair (too-big deficit × too-small slope); CYB-7 fixed the deficit,
  CYB-9 the slope. **OOS finding:** the single linear slope *overshoots* ep2 (+316% vs real
  +272%) — a mild **concavity at the two peaks** (ep1 24.7%/pt → ep2 22.5%/pt). **CYB-14
  tested it and it does NOT generalize:** a linear-vs-concave model comparison on the full
  monthly path (OOS on ep2) found the free power exponent lands at α≈1.03 (not concave) and
  the forced-concave form is worse → within-noise at the path level → **keep the linear
  pricer** (don't carry an unearned 2nd parameter). The saturation thread is closed.
- **Distributional wedge**: ~5.5× regressive (poorest vs richest quintile), as a *read-out*
  over the validated price path × real income/egg-share data — not the engine's households.

## The METHOD — this is the actual product; protect it
- Feed **REAL series**, never hand-drawn shapes. If you must stylize, flag it loudly and
  treat the result as provisional. (Every version that shaped an input to fit an output got
  refuted by the next version that fed real data — v0.3's 0.86 was "a beautiful lie.")
- Validate **out-of-sample** — against episodes/facts not used in calibration. That is the
  only thing that licenses "reflects real-world dynamics."
- **Determinism is guarded**: same inputs → same outputs. If it breaks, that's a bug.
- Forecasting stance: **illustrative, not predictive.** Validate the *mechanism* across
  independent episodes, then run *counterfactuals* — not point forecasts.
- `replace_lag` is **retired** (CYB-7): the egg model is now driven by the **real NASS
  monthly table-egg layer-inventory** deficit (`data/nass_layers.py`, deseasonalized vs the
  2020-21 pre-outbreak normal) — no fitted timing parameter. Timing survived and improved
  (both peaks land, ep1 exact); magnitude *degraded* honestly (see the slope note above).
  `hpai_culls.flock_deficit_path(replace_lag=…)` remains only for the v09 side-by-side.

## Next move & open threads (see HANDOFF.md for full detail)
Done: `replace_lag` retired via the real NASS flock series (CYB-7); egg pricer slope
recalibrated to ~24/pt on real deficits (CYB-9); **saturation tested & rejected** (CYB-14 —
concavity within-noise at the path level, keep linear); **recursion × conflict coupling**
built (CYB-10 — super-additive ignition). Open threads: the **formal global-bifurcation
proof** is **gated** on an external mathematician (CYB-13, post-July-6 — do NOT solo-build);
**H2 chaos-leakage characterization** and **bidirectional coupling** (CYB-10 follow-ups);
then cost-matrix third channel → **accommodation / reflexivity** (the sustaining channels;
accommodation seed CYB-16) → the distributed virtual economy. Pull real data from source APIs
(FRED/NASS) directly now — a NASS QuickStats key is required (env `NASS_API_KEY`).

## Conventions
- Public repo, MIT: github.com/Goldcap/Cybeersym.
- Keep the conservation asserts green on every change. New commodities/events/pricers slot in
  at the registries without touching the engine.
