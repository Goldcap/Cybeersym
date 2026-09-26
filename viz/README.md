# viz/ — the illustration layer (CYB-42)

Interactive, parametric visualisations of the Cybeersym models — "move the dials, watch the
patterns change," in the spirit of Steve Keen's Minsky/Ravel. An **illustration layer**, not the
engine of record: the numpy models under `src/` remain authoritative, and CI re-derives the numpy
reference and checks the deployed JS against it on every change.

## `index.html` — Four Models, Three Shocks (a comparative document)

A **coverage comparison**: four models of the business cycle, arranged left→right as a ladder where
each *adds a mechanism the one before it lacks* — **Lucas (RBC)** → **Mankiw (NK, +sticky prices)** →
**Goodwin (+endogenous distribution)** → **Keen (+finance)**. Pick a model, watch it run, then hit it
with the same three shocks — **Productivity · Demand · Financial**. Where a model has the machinery it
responds (real model output); where it doesn't, it sits **blind**, with a one-line reason — and *the
blind spots are the point* (e.g. fire **Financial** at Lucas/Mankiw/Goodwin: no debt state, nothing to
shock — the flat line is why the mainstream models couldn't represent a 2008).

- **Capability strip:** the selected model's "bits" (endogenous cycle · supply · demand · distribution
  · finance) shown as ✓ / ~ / ✗ — read across = the ladder, read down = the blind spots.
- **The response matrix** (real numpy output in ✓/~, honest flat-line in ✗):
  - **Lucas** — Productivity ✅ (RBC IRF: efficient, near-monotone recovery). Demand ✗ (money neutral).
    Financial ✗ (no debt state).
  - **Mankiw** — Demand ✅ (inefficient gap, policy closes it). Productivity ✅ (cost-push **tradeoff**:
    output↓ inflation↑, policy tightens). Financial ✗ (no debt state).
  - **Goodwin** — Productivity / Demand ~ (a perturbation to the endogenous cycle; Goodwin has no
    supply/demand *distinction*). Financial ✗ (no debt).
  - **Keen** — Financial ✅ (a debt overhang tips it over the global basin into debt-deflation, no
    warning). Productivity / Demand ~ (perturbation, damps back at prudent settings).
- **Orthodox responses** are the real numpy DSGE IRFs (`src/orthodox/`), baked in and CI-pinned,
  shape-normalized for display (magnitudes not comparable across models — topological). **Goodwin/Keen**
  responses compute live from the in-page Goodwin–Keen RK4 engine.
- **The regime map** (interest rate r × investment sensitivity k_sharp; local-stability colour + Hopf
  line + d₀-driven breakdown basin) is shown **only for Goodwin/Keen** — the models with a debt state
  that live on it; orthodox models have no such map. It remains the local-tipping-vs-global-basin view:
  the Hopf edge is a **forecastable** local bifurcation (CSD-visible), the basin crossing is **blind**.

### `src/orthodox/` — the real orthodox foils (the special-case-then-diverge story, runnable)

- **`rbc.py`** — a log-linearised Real-Business-Cycle model (Kydland–Prescott; King–Plosser–Rebelo;
  Campbell 1994). Solved two independent ways (stacked-time + Blanchard–Kahn saddle path) that agree
  to ~5e-15. Signature: an adverse TFP shock → efficient, **near-monotone** recovery, consumption
  smooth, no output gap, no policy role.
- **`nk.py`** — the canonical 3-equation New-Keynesian model with an inertial Taylor rule
  (Clarida–Galí–Gertler; Woodford; Galí 2015), with `kind='demand'|'supply'`. **Demand** shock → an
  **inefficient output gap + disinflation** that policy eases to close (the gap **troughs on impact
  and decays, NOT hump-shaped** — the hump is a medium-scale-DSGE habit/adjustment-cost feature;
  building the real model corrected an earlier hand-drawn viz curve that wrongly implied a hump).
  **Supply** (cost-push) shock → the **inflation-output tradeoff**: output falls but inflation *rises*
  and policy tightens (the NK feature RBC lacks).
- Each has a `_selftest()` pinning its qualitative signature; both run in CI.
- **Glossary + conclusions** below: what every dial/axis means, and the load-bearing division of
  labour (k_sharp sets the local Hopf; r and d₀ govern the global basin).

## Fidelity & CI (`.github/workflows/viz.yml`)

A faithful JS RK4 port of `src/goodwin_keen/model.py`, guarded by three CI jobs:
- **`fidelity`** (self-hosted tweedledum runner): extracts the model block from `index.html` and
  checks its RK4 against the numpy reference — **max Δ ≈ 5×10⁻¹¹ over 7 checkpoints**.
- **`verify_display`**: asserts the illustration actually *shows* its thesis — both regime bands
  present, the Hopf contour has segments, and the breakdown overlay fires and grows with d₀ (added
  after the 2026-09-07 reviewer gate found the earlier map's d₀ demo was inert).
- **`reference-drift`** (hosted, has numpy): pins `fidelity-reference.json` to `model.py`; also
  runs the `src/orthodox/` self-tests and `gen_ortho.py --check` (the baked RBC/NK IRFs in
  `index.html` must still match the numpy models).

Deterministic (σ=0). Reviewer-gated 2026-09-07: the math (fidelity, eigenvalue classification, Hopf
locus, local-vs-global) was independently re-derived in numpy and holds; the display defects it
found are fixed and now CI-guarded. Served at `cybeersym.motormeme.com` (Caddy + basic auth, ALB).
