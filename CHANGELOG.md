# Cybeersym — version history

The egg model, version by version. Each version is one **finding**, with the script
that produced it (`vNN_*.py`) and its figure (`figures/cybeersym_vNN_*.png`).

The through-line: **let real data refute the model, repeatedly.** Every version where
we let ourselves shape an input to fit an output got caught by the next version that
fed real data. The number we ended on (corr 0.86) is the same number a stylized fit
gave at v0.3 — but the v0.3 version was a *beautiful lie* and the v0.5+ version is
*earned*. The epistemics are the whole point; the correlation is incidental.

---

## v0 — plumbing  ·  `v00_eggs_demo.py` → `figures/cybeersym_v0_eggs.png`
Stock-flow-consistent (SFC) engine. Two-account money circuit (households ↔ firm),
supplier → store → household pipeline, perishable inventory. **Conservation asserts**
(money & egg residuals < 1e-6) established as the crown jewel — held green through
every later refactor. Initial pricing was rockets-and-feathers (sticky markup).

## v0.3 — first calibration vs FRED  ·  `v03_calibrate.py`, `v03_calib_fig.py` → `cybeersym_v03_calibration.png`
Calibrated against the real 2022-23 FRED egg series. Three findings: (1) **rockets-
and-feathers is wrong for eggs** — eggs are a commodity (price falls fast too), not a
branded good; (2) a **stockout deadzone** — pricing off lagging realized inventory
can't anticipate scarcity; fix = price off the *flow gap* (leading indicator);
(3) **proportional, not integral** cost-pass-through — an accumulating markup peaks at
the *end* of a shortage; proportional peaks *with* it. Got corr 0.86 — **but on a
hand-shaped cull bump.** (The lie v0.4 exposes.)

## v0.4 — real cull data refutes the fit  ·  `v04_real_vs_stylized.py` → `cybeersym_v04_realdata.png`
Fed the **real USDA APHIS depopulation series**. The 0.86 collapsed to ~0: the model
peaked July 2022, reality peaked Jan 2023. The stylized bump had been *shaped to the
answer* (peak Dec, deep 64%); the real flock deficit peaks summer, ~9.5% deep. The
data exposed two missing first-order mechanisms: **seasonal demand** (every egg peak
is winter, independent of cull timing) and **convexity** (a ~9.5% deficit → +188%
price). This is the Keen "data is dispositive" lesson, applied to our own model.

## v0.5 — timing solved from real inputs  ·  `v05_seasonal_fit.py` → `cybeersym_v05_seasonal.png`
Added (1) **seasonal demand** extracted from calm-year (2016-21) prices, and (2) a
**12-month effective flock-replacement lag** (the 6-mo pullet-maturation floor plus
slow/incomplete/re-culled replacement — the flock ran ~5% below baseline for years).
Peak now lands **Jan 2023, corr 0.856** — from real culls + real seasonality + one
physical lag constant. Magnitude still undershoots (+78% vs +188%): convexity open.

## v0.6 — out-of-sample validation  ·  `v06_oos_test.py` → `cybeersym_v06_oos.png`
Ran the **2024-25 HPAI episode the model was never fit to** (one continuous run, same
params). **Timing validated**: peak March 2025, `replace_lag=12` untouched → the lag
is *structural*, not timestamp-tuned. The "uniform convexity" hypothesis was
*falsified* (capture differed 42% vs 73%), but normalizing by deficit depth revealed
the real relationship is **consistent and ~linear: ~13% price per 1% flock deficit**
across both episodes (mildly saturating, not convex). The model was the convex one.

## v0.7 — pricer becomes a commodity property  ·  `v07_pricer_fix.py`, `pricers.py` → `cybeersym_v07_pricer.png`
The price-deficit slope was an *engine constant* (`Params.supp_up`) — wrong place. It's
an **egg property** (egg demand's inelasticity). Built the `pricers.py` registry: a
commodity names a pricer + carries its slope; the engine stays commodity-blind.
Egg pricer = **linear in deficit at slope ≈ 13**. A single egg slope lifts *both*
episodes together (+175% / +324% vs real +188% / +272%). Residual: reality mildly
**saturates** at deep deficits (imports +2,040%, demand destruction) — the next egg
property, deferred until the real NASS inventory series pins the 2024-25 deficit.

## v0.8 — the distributional wedge (namesake)  ·  `v08_wedge.py` → `cybeersym_v08_wedge.png`
The regressive incidence, computed on the **validated price path** × **real income/
egg-share data** (USDA-ERS food shares, BLS CE egg lines). At peak, eggs alone add
**+1.10 pts** to the poorest quintile's personal inflation vs **+0.20** to the
richest — a **5.5× regressive ratio**, opening during both validated shocks. Honest
caveats: eggs alone are a small absolute burden (but proxy the food-at-home basket,
33% of the poorest's income); the model *understates* real regressivity (compressed
income range; substitution asymmetry — the poor can't substitute, a second regressive
channel on top of the budget-share one).

---

## Current stable engine (unversioned — the validated core)
- `model.py`   — SFC engine, conservation asserts, 5 income quintiles, supplier/store,
                 seasonal-demand hook, commodity-pricer dispatch.
- `pricers.py` — commodity pricer registry; `EGG_PRICING` (linear_deficit, slope 13);
                 `### TODO(saturation)` for the next egg property.
- `events.py`  — adverse-event plugin layer: pure supply/demand path-transforms,
                 multiplicative composition, registry, load-time validation.
- `data/`      — real fixtures: FRED prices, USDA culls + flock transform, seasonality.

## Open threads (named, mostly blocked on data, not cleverness)
1. **NASS monthly layer-inventory series** — would retire the calibrated `replace_lag`
   and pin the 2024-25 deficit (data archaeology: scattered monthly PDFs + a host the
   sandbox can't reach directly).
2. **Saturation term** — egg pricer `markup = slope·deficit**alpha` (alpha≈0.65), once
   (1) lands. An egg-commodity property like `slope`.
3. **Cost-matrix / third channel** — real feed-cost / natural-gas series into
   structural cost accounting (seam marked in `events.py`).
4. **Distributed virtual economy** — the "Distributive" half of the repo title:
   suppliers/stores as services, an event-sourced ledger as the conserved spine
   (= the MMT state balance sheet), ensemble runs + chaos measurement (Lyapunov,
   attractor stats) for *illustrative-not-predictive* validation. A separate project;
   today proved the *method*.
