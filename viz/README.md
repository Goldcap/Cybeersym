# viz/ — the illustration layer (CYB-42)

Interactive, parametric visualisations of the Cybeersym models — "move the dials, watch
the patterns change," in the spirit of Steve Keen's Minsky/Ravel. These are an
**illustration layer**, not the engine of record: the numpy models under `src/` remain
authoritative, and each page carries a **fidelity self-check** that re-derives known
numpy reference points in-browser on load (and shows the max deviation).

- `index.html` — **Goodwin–Keen Regime Map**. Every point in the interest-rate ×
  investment-sensitivity plane is one economy, coloured by its fate (stable / limit cycle /
  breakdown). Pick a point → the phase portrait and debt path redraw for that economy. The
  **Hopf boundary** (local bifurcation) is anchored in the map; the **d₀** dial (the global
  debt basin, deliberately kept *off* the map) reshapes the breakdown region — so the map
  visibly cannot see the thing d₀ does. This is the CYB-40/41 local-vs-global distinction,
  made spatial. A faithful JS RK4 port of `src/goodwin_keen/model.py` (verified to
  max Δ ≈ 5×10⁻¹¹ against numpy over 10 checkpoints).

Deterministic (σ=0). Served at `cybeersym.motormeme.com` (Caddy static + basic auth, behind
the ALB). Not "done" until a fresh reviewer gate signs off the fidelity + eigenvalue logic.
