# viz/ — the illustration layer (CYB-42)

Interactive, parametric visualisations of the Cybeersym models — "move the dials, watch the
patterns change," in the spirit of Steve Keen's Minsky/Ravel. An **illustration layer**, not the
engine of record: the numpy models under `src/` remain authoritative, and CI re-derives the numpy
reference and checks the deployed JS against it on every change.

## `index.html` — Goodwin–Keen Regime Map

Read the same economy two ways, side by side:

- **The space (left):** the (interest rate r × investment sensitivity k_sharp) plane. The base
  colour is **local stability** — the sign of the good equilibrium's leading eigenvalue: *stable*
  (Re<0, spirals home) vs *unstable* (Re≥0, self-driven cycles); this is exact, cheap, and
  **d₀-independent**. The **Hopf line** (the stable⇄unstable boundary, ~horizontal because it is
  r-independent) is drawn as a contour scanned on both axes. A **breakdown overlay** (diagonal
  hatch) marks cells that collapse from the *current* initial debt d₀ — the **global basin**, which
  grows as you raise d₀ while the base colour and the Hopf line stay put.
- **Over time (right):** the phase portrait (ω↔λ, the dynamical-systems view) **plus** the same run
  as a **time-series** (employment λ, wage share ω, debt d vs time) **plus** an **impulse-response**
  panel — a +2% debt shock and employment's return, with a **shock half-life** readout that
  lengthens toward the Hopf. This is critical slowing down in a macroeconomist's native grammar.
- **The Keen A→B demonstration** across the top: classical self-correction → relax investment
  prudence → endogenous cycles → the debt-basin collapse you *can't* see coming.
- **Glossary + conclusions** below: what every dial/axis means, and the load-bearing division of
  labour (k_sharp sets the local Hopf; r and d₀ govern the global basin).

## Fidelity & CI (`.github/workflows/viz.yml`)

A faithful JS RK4 port of `src/goodwin_keen/model.py`, guarded by three CI jobs:
- **`fidelity`** (self-hosted tweedledum runner): extracts the model block from `index.html` and
  checks its RK4 against the numpy reference — **max Δ ≈ 5×10⁻¹¹ over 7 checkpoints**.
- **`verify_display`**: asserts the illustration actually *shows* its thesis — both regime bands
  present, the Hopf contour has segments, and the breakdown overlay fires and grows with d₀ (added
  after the 2026-09-07 reviewer gate found the earlier map's d₀ demo was inert).
- **`reference-drift`** (hosted, has numpy): pins `fidelity-reference.json` to `model.py`.

Deterministic (σ=0). Reviewer-gated 2026-09-07: the math (fidelity, eigenvalue classification, Hopf
locus, local-vs-global) was independently re-derived in numpy and holds; the display defects it
found are fixed and now CI-guarded. Served at `cybeersym.motormeme.com` (Caddy + basic auth, ALB).
