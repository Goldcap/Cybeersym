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

## Project board & the conserved-network track (CYB-1…5)
The egg model (below) proved the **method**. The CYB tickets carry it onto the THESIS's
**recursion channel** — a conserved producer network — with chaos-measurement tooling
built alongside. *This section is the current front; the egg material below is the
still-valid foundation.* Specs are **canonical in Linear** (CYB-N, edited in place); the
**repo is canonical for code + committed results**; no duplicate spec files live in the
repo. Per-module detail: `src/bullwhip/README.md`, `src/chaos/README.md`,
`docs/empirical_grounding.md`, `docs/plans/`, `docs/solutions/`.

**Board.** CYB-1 ✅ recursion/bullwhip · CYB-2 ✅ deterministic chaos (nonsmooth onset) ·
CYB-3 ✅ empirical grounding · CYB-4 ✅ formal classification · CYB-5 (this) ✅ doc sync.
**Conflict layer = next mechanism, deliberately unspecced.**

**Validated reusable instrument suite** (model-agnostic — operate on a `step(state)→state`
callable + a flat state vector, knowing nothing about supply chains; every future mechanism
runs through these): `lyapunov` (largest Lyapunov, self-test → ln 2), `bifurcation`
(sweeper), `linearize` (finite-diff Jacobian + fixed-point finders, self-test → multiplier
2−r), `normal_form` (border-collision classifier, self-test on 3 documented 2-D cases).

**Key findings to date.**
- **Bullwhip amplification (CYB-1).** A 3-tier chain compounds order variance from
  demand-signal processing alone (local 36.6× → shared 10.9× → coordinated 2.9×): *seeing*
  true demand suppresses but does not flatten — only *acting* on it (echelon replenishment)
  flattens. The standalone **oracle** the integrated SFC version must later reproduce.
- **Deterministic chaos via a nonsmooth onset (CYB-2).** Sterman's anchoring rule + falling
  supply-line weight β → measured chaos (λ>0, bounded, deterministic, conserved). The
  equilibrium **never destabilizes** (|λ|≈0.91, never crosses 1); a constraint-riding
  attractor is born **coexisting** with it (**bistability**); the active border is **order
  non-negativity** (you can't un-order).
- **The conservation finding (CYB-4) — the deepest result so far.** Stock-flow consistency
  makes the equilibrium **non-hyperbolic for all parameters** (three exact λ=+1
  supply-line-conservation eigenvectors = a permanent center subspace). So the model's
  instabilities are **global** (coexisting attractors, bistability, hysteresis), *not*
  local smooth bifurcations. The rigor (conservation) is what puts the dynamics outside the
  standard local-bifurcation toolkit — a structural claim about SFC models as a class.
- **Empirical spine (CYB-3).** The β bias is measured-real (Sterman β≈0.34, near-universal,
  robust 35 yrs) and sits at the model's stable→turbulent edge; illustrative-not-predictive,
  with an honesty firewall on why direct chaos-detection in macro data fails.

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

**Conserved-network track (current front):**
- **Formal global-bifurcation proof.** The chaos onset is a nonsmooth fold of a
  *coexisting limit cycle*, not a local bifurcation of the equilibrium (CYB-4). Classifying
  / proving this rigorously — in a ~21-D piecewise-smooth, non-hyperbolic, conserved map —
  is the prime **external-mathematician validation** candidate (piecewise-smooth /
  nonsmooth-dynamics specialist). The honest limits are already documented (`docs/solutions/`).
- **Conflict layer** — the next inflation channel (social transmission; wage-price / share
  fight). Deliberately unspecced; the next mechanism ticket.
- **SFC integration of the bullwhip oracle** — fold CYB-1's standalone 3-tier chain into the
  conserved engine so the integrated model reproduces the measured amplification ratios.

**Egg model (mostly blocked on data, not cleverness):**
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
   *Status: the minimal first brick is built — CYB-1 (bullwhip amplification) and CYB-2
   (deterministic chaos) on a standalone conserved chain, with the Lyapunov / bifurcation /
   linearize / normal-form instrument suite (CYB-2/4) already validated and reusable.*

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
