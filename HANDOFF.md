# HANDOFF — Cybeersym

Read this first. `CHANGELOG.md` has the version-by-version arc; `README.md` has
structure and run commands. This file is the *why* — the live decisions, the
non-obvious rationale, and the method discipline that the code alone can't convey.
Written at the end of a long design session, for whoever (human or model) picks this
up next.

---

## What this is, in one breath
Agent-based, stock-flow-consistent (SFC) sim for testing **structural** inflation
hypotheses. Wind tunnel, not crystal ball. Working commodity: **eggs** (2022-23 &
2024-25 US HPAI price spikes). Econometrics is the *referee* (out-of-sample
validation), never the engine.

## Current validated state (don't re-derive — build on this)
- **Conservation** holds to <1e-10 (money + egg residuals). This is the crown jewel.
  Every refactor must keep the asserts in `model.py:step()` green. If they ever fire,
  stop and fix — a leak invalidates everything downstream.
- **Timing validated out-of-sample.** Same model + same params reproduce BOTH the
  2022-23 (peak Jan 2023) and 2024-25 (peak Mar 2025) price peaks. The 2024-25 episode
  was never fit. This is the result that licenses trusting the mechanism.
- **Magnitude** bracketed by a single commodity-owned slope (egg pricer, linear in
  deficit, slope≈13 → ~13% price per 1% flock deficit). Both episodes lift together.
- **Distributional wedge** (the namesake) computed on the validated price path × real
  income/egg-share data: ~5.5× regressive (poorest quintile's personal egg-inflation
  vs richest).

## Non-obvious decisions and WHY (the stuff that isn't in the code)

1. **`replace_lag=12` is calibrated, NOT tuned — but it's the one soft spot.**
   It's the *effective* flock-recovery lag (6-mo pullet-maturation floor + slow/
   incomplete/re-culled replacement; flock ran ~5% below baseline for years). It's ONE
   physical scalar, independently data-supported, and the deficit *shape* comes from
   real cull dates — categorically better than the v0.3 hand-drawn bump. BUT it was
   chosen partly because it lands the peak. The clean validation is the real **NASS
   monthly layer-inventory series** (open thread #1), which needs no lag assumption.
   Until then, treat 12 as defensible-but-provisional. The out-of-sample 2024-25 pass
   is what currently vindicates it.

2. **The pricer slope is a COMMODITY property, not an engine constant.** It moved from
   `Params.supp_up` to `pricers.py:EGG_PRICING`. The engine is commodity-blind: a
   commodity names a pricer + carries its slope; the engine dispatches. This matters
   for the whole architecture — milk/microchips will register their own. Don't push
   pricing knobs back into the engine.

3. **"Convexity" was the wrong diagnosis.** Reality is ~LINEAR in the deficit (~13%/pt),
   mildly *saturating* at deep deficits — NOT convex. The earlier convex miss was an
   artifact of pricing off `flow_gap = 1/(1-deficit)`. Keying off the deficit directly
   fixed it. If you revisit magnitude, the residual is *saturation* (imports +2,040%,
   demand destruction at $6+ eggs), not convexity. Candidate: `markup = slope·deficit
   **alpha`, alpha≈0.65, with alpha as another egg-commodity property. DEFERRED — see #1;
   don't fit a 2-point curve while the 2024-25 deficit rests on estimated cull months.

4. **The wedge is a read-out, not the engine's households.** The engine's egg budget
   shares are stylised high (good for the price mechanism, wrong for distributional
   LEVELS). The honest wedge = validated price path × realistic Engel shares (BLS/ERS).
   The model *understates* real regressivity (compressed income range; substitution
   asymmetry — poor can't substitute, a 2nd regressive channel). Don't "fix" this by
   cranking engine household params; keep the read-out separate.

5. **The plugin seams are deliberate and they paid off.** `events.py` (adverse events
   as pure supply/demand path-transforms, multiplicative composition) and `pricers.py`
   (pricer registry) made each new test nearly free. Principle throughout: *rich
   interface, poor body; generalize on contact, not on spec; validate at the seam, not
   mid-loop.* New commodities/events/pricers slot in without touching the engine.

## The METHOD (this is the actual product — protect it)
Every version where an input got shaped to fit an output was **refuted by the next
version that fed real data** (v0.3's 0.86 was a beautiful lie; v0.4 caught it; v0.5
earned the same number honestly). Rules:
- Feed REAL series, never hand-drawn shapes. If you must stylize, flag it loudly and
  treat the result as provisional until real data replaces it.
- Validate **out-of-sample** (against episodes/facts not used in calibration). That is
  the only thing that licenses "reflects real-world dynamics."
- Determinism is a property to GUARD (same inputs → same outputs). If it breaks,
  that's a bug, not noise.
- Forecasting stance: **illustrative, not predictive.** Validate the *mechanism* across
  independent episodes, then run *counterfactuals* — not point forecasts.

## Open threads (named; most blocked on data, not cleverness)
1. **NASS monthly layer-inventory series** → retires the calibrated `replace_lag`, pins
   the 2024-25 deficit. Scattered across monthly Chickens-and-Eggs PDFs + Quick Stats
   API (`quickstats.nass.usda.gov`). Data archaeology, ~1hr. *Now doable from Claude
   Code with real network access.*
2. **Saturation term** in the egg pricer (after #1). An egg-commodity property.
3. **Cost-matrix / third channel** — real feed-cost / natural-gas series into structural
   cost accounting. Seam marked `### TODO(cost-matrix)` in `events.py`. base_cost
   stops being the constant 0.50 and becomes a path.
4. **Return to the distributional wedge** on any future engine changes (it's downstream
   of prices, so it inherits improvements for free, but re-validate).
5. **Distributed virtual economy** (the "Distributive" half of the repo title — a
   separate, larger project). Suppliers/stores as services; an **event-sourced ledger**
   as the conserved spine (= the MMT state balance sheet; this is where conservation
   lives once it's distributed); ensemble runs + **chaos measurement** (Lyapunov
   exponents, attractor dimension, bifurcation scans) as first-class tooling. Goal:
   render the MMT inflation mechanism ("pushes against real resource constraints") as a
   *measurable propagation through a conserved producer network*, validated against
   emergent stylized facts (fat tails, volatility clustering, bullwhip ratios) it wasn't
   tuned to. Minimal first brick: smallest producer-network that exhibits ONE measurable
   emergent phenomenon the equilibrium model can't produce (candidate: **bullwhip
   amplification in a 3-tier supply chain** — real, industry-measured, absent from
   equilibrium treatment), with the chaos-measurement instrument wrapped around it from
   day one. Prove the instrument on one phenomenon, then grow the economy around it.

## Suggested immediate next move
Pull the NASS layer-inventory series (#1). It's the one calibrated assumption left, it's
now reachable with real network access, and it either vindicates `replace_lag=12`
out-of-the-box (assumption retired, confidence way up) or teaches us something new.
Everything else (saturation, cost-matrix) sequences cleanly after it.

## Repo / run notes
- All code lives under `src/`. Engine modules (`model.py`, `pricers.py`, `events.py`)
  and `data/` import as siblings, so `cd src` and run `vNN_*.py` from there.
- `requirements.txt`: numpy, matplotlib only.
- GitHub: github.com/Goldcap/Cybeersym (public, MIT).
- Sandbox limitation that shaped the build (now lifted under Claude Code): the prior
  environment couldn't reach FRED/NASS APIs directly — real data was scraped via page
  fetches. With real network access, pull from source APIs instead.
