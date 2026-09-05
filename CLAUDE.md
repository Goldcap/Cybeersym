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

## The reviewer gate (builder ≠ reviewer) — run before calling anything done
No build or analysis is **done** — not reported to the user, not committed to a PR — until a
**fresh, independent reviewer** has signed off: a separate subagent with *none* of the builder's
context (or the `ce-code-review` / `ce-doc-review` skills). Self-review does not count — the
builder's blind spots are exactly what it misses (the Fisher "two-basin" headline was a detector
artifact that read as *done* until rechecked). From a clean state the reviewer must:
1. **Re-run** the code; confirm determinism (byte-identical rerun).
2. **Check every stated number** — report, README, commit message, Linear ticket — against actual
   output. No claim without a matching output line. (First catch: a stated `Ω=√(A·C)=0.3603` that
   was really `0.3602` — CYB-33.)
3. **Attack the headline** — "lift the detectors": re-derive independently, try to break it.
4. **Guards green AND not vacuous** — conservation `< tol` on a *real* trajectory (not sitting at
   the fixed point), byte-exact nesting, σ=0 determinism.
5. **Reconcile docs ↔ code** — README/figures/claims match; no stale refs or phantom imports.
Resolve every finding before presenting. If a fork can't be resolved, **HOLD and surface it** in
one sentence — never silently ratify (`../tandem`'s rule: *if unsure, HOLD*).

**The gate is a floor, not a ceiling — measure and escalate.** Log every whoops found *after*
"done" (the escaped-defect record). When a class keeps escaping, climb the ladder: 1 reviewer →
two independent / cross-model → adversarial red-team (must *falsify* the headline) → full
`../tandem` fresh-clone loop → external expert (CYB-13). And **label what can't be self-verified**
(out-of-sample empirical, formal proof) rather than let a green gate imply coverage it lacks —
name the highest reproducibility level actually demonstrated. Full spec + rationale: **CYB-34**.

## Next move & open threads (see HANDOFF.md for full detail)
Done: `replace_lag` retired via the real NASS flock series (CYB-7); egg pricer slope
recalibrated to ~24/pt on real deficits (CYB-9); **saturation tested & rejected** (CYB-14 —
concavity within-noise at the path level, keep linear); **recursion × conflict coupling**
built (CYB-10 — super-additive ignition); **accommodation** — the first *sustaining* channel —
built on bare CYB-6 (CYB-17 — the rate is a three-channel tug-of-war; the distributional
channel *self-exhausts*) and on the coupled stack (CYB-18 — under recursion's reloading the
distributional exhaustion is deferred and recursion pins an inflation floor the rate can't
reach; the rate gates ignition both ways; two byte-exact anchors); **Minsky credit-crunch
cascade Phase 1** (CYB-19 — bounding-vs-fizzle is an outcome the params pick; the crunch bounds
but doesn't cure; Ponzi ≡ CYB-17 capitalizing interest); **Phase 2** (CYB-23 — default +
impairable rentier → the impairment horizon; Engine-1 credit-quantity contagion is
hyper-inflationary, NOT Fisher); and **Phase 2b** (`src/fisher/` — the genuine Fisher
debt-deflation loop → **the markup-defense is a structural price floor**: composed on the conflict
layer the Fisher loop is a *bounded limit cycle*, and genuine `D/P→∞` debt-deflation appears only
on the `α_p→0` edge (stabilizer suppressed); the isolated Fisher map is always unstable so the
stabilizer, not φ, is the pivot; the **"inflationary, not Fisher" result is STRUCTURAL**, not a
refutation of the canon. This **supersedes an artifactual first cut** — a "two-basin / φ*≈1.63"
map that was a detector artifact (a −25%/step tripwire freezing a bounded oscillation)).
Open threads: the **formal global-bifurcation proof** is **gated** on an external
mathematician (CYB-13, post-July-6, now parked after Dr Hu declined — do NOT solo-build);
**Phase-2b-on-coupled** and **CYB-19-on-coupled** are the live crunch follow-ups; **reflexivity /
expectations** (CYB-20, the other sustaining channel); **supply-chain financing** (CYB-21, the
rate's 4th channel); **H2 chaos-leakage characterization** and **bidirectional coupling** (CYB-10
follow-ups); the monetarism critique (CYB-16) stays gated; then cost-matrix third channel → the
distributed virtual economy. Pull real data from source APIs (FRED/NASS) directly now — a NASS QuickStats
key is required (env `NASS_API_KEY`).

## Conventions
- Public repo, MIT: github.com/Goldcap/Cybeersym.
- Keep the conservation asserts green on every change. New commodities/events/pricers slot in
  at the registries without touching the engine.
