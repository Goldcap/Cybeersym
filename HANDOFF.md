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

## Project board & the conserved-network track (CYB-1…15)
The egg model (below) proved the **method**. The CYB tickets carry it onto the THESIS's
**recursion channel** — a conserved producer network — with chaos-measurement tooling
built alongside. *This section is the current front; the egg material below is the
still-valid foundation.* Specs are **canonical in Linear** (CYB-N, edited in place); the
**repo is canonical for code + committed results**; no duplicate spec files live in the
repo. Per-module detail: `src/bullwhip/README.md`, `src/chaos/README.md`,
`docs/empirical_grounding.md`, `docs/plans/`, `docs/solutions/`.

**Board.** CYB-1 ✅ recursion/bullwhip · CYB-2 ✅ deterministic chaos (nonsmooth onset) ·
CYB-3 ✅ empirical grounding · CYB-4 ✅ formal classification · CYB-5 ✅ doc sync ·
CYB-6 ✅ conflict layer · CYB-7 ✅ retire replace_lag (real NASS flock) · CYB-9 ✅ recalibrate
pricer slope · CYB-10 ✅ recursion×conflict coupling · CYB-14 ✅ saturation tested→rejected ·
CYB-15 ✅ doc sync · CYB-17 ✅ accommodation (the first *sustaining* channel; the rate as a
three-channel tug-of-war) · CYB-18 ✅ accommodation on the coupled stack (distributional
exhaustion deferred; recursion pins an inflation floor; rate gates ignition both ways) ·
CYB-19 ✅ Minsky credit-crunch cascade Phase 1 (bounding-vs-fizzle is an outcome; the crunch
bounds but doesn't cure; Fisher/debt-deflation basin deliberately unwired). **Gated:** CYB-13 🔒
formal global-bifurcation proof (external mathematician, post-July-6 — do NOT solo-build);
CYB-16 🔒 the monetarism critique (normative; external buy-in). **Live next:** CYB-19 Phase 2
(default + impairable rentier → the debt-deflation/Fisher basin) · CYB-19-on-coupled (the crunch
on the egg stack) · CYB-20 reflexivity / expectations (the other sustaining channel) · CYB-21
supply-chain financing (the rate's 4th channel). **Parked seed:** CYB-8 austerity. Nearer-term:
the CYB-10 follow-ups (H2 chaos-leakage characterization; bidirectional coupling).

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
- **Conflict layer (CYB-6) — the second transmission channel, dynamically OPPOSITE to
  recursion.** Wage-price conflicting claims over a conserved pie (wage share + profit
  share = 1). The real wage share is a **stable node**; the instability lives entirely in
  the **nominal price level** (a sustained spiral) — the mirror image of recursion's bounded
  *real* chaos. Steady rate matches the Rowthorn–Lavoie closed form `π*=(α_w·α_p/(α_w+α_p))·g`
  to 6e-17. The **nominal-wage floor** (downward rigidity) breaks the otherwise-symmetric
  inflation/deflation mechanism and is what makes gap=0 a genuine transmission threshold —
  a real constraint as the switching manifold, echoing CYB-2's order-non-negativity border.
- **Super-additive ignition (CYB-10) — the channels compose.** Couple recursion→conflict
  one-way (chain scarcity `d(t)` raises the aspiration gap: `g(t)=g0+κ·d(t)`) and a
  *subthreshold* shock that neither channel alone would ignite lights a sustained wage-price
  spiral. Emergence is real, not plumbing: the **κ=0 decoupling regression reproduces CYB-2
  and CYB-6 byte-for-byte**. Sharpened mechanism: recursion's *endogenous* instability is a
  **persistent-scarcity generator** — a transient shock dissipates, only the self-sustaining
  bullwhip holds `g>0` — so recursion **sustains, doesn't merely amplify**; and the real
  chaos leaks into the nominal path (π aperiodic; a positive answer to the H2 preview). Both
  conservation laws hold simultaneously through the ignited regime.
- **Accommodation — the first *sustaining* channel (CYB-17), and it on the coupled stack
  (CYB-18).** Finance the wage bill at a policy rate `i`; the rate acts through **three
  channels at once** (cost +, symmetric-demand −, distributional −) — a **tug-of-war whose
  winner is a parameter, not a verdict**. CYB-6's "unbounded" runaway was the **full-
  accommodation limit** hiding as a law. On the coupled stack the distributional channel
  **stops self-exhausting** (recursion re-loads its target every period) but also **never
  wins**: recursion pins a positive inflation floor `≈k·κ·⟨d⟩` **no rate can reach** → the
  rate turns *redistributive, not stabilising*; and the rate **gates super-additive ignition
  both ways** (cost-push lowers the coupling threshold, disinflation raises it). Composition
  proven by **two** byte-exact anchors (`κ=0`→CYB-17; full-accommodation→CYB-10); three
  nonsmooth borders live at once, the **solvency ceiling dominating and pre-empting the wage
  floor**. The Minsky crunch off that solvency border is CYB-19 (below).
- **Minsky credit-crunch cascade — Phase 1 (CYB-19).** Fire the solvency border: a financing-
  regime classifier (hedge→speculative→Ponzi, from CYB-17's *existing* flows — **Ponzi ≡ CYB-17
  capitalizing uncovered interest**, renamed not new) + a deleveraging-rate cascade armed at
  **Ponzi ∧ border**. Headline: **bound vs fizzle is an OUTCOME the parameters pick** — fast/early
  deleveraging bounds the spiral (→12% of baseline), slow/late fizzles (→85%), above the rate-set
  baseline leverage it never fires. But the crunch **bounds without curing** (only via a grinding
  **limit cycle at the border**, never to zero), and **leverage-at-trigger is set by the policy
  rate** (hiking tips you into Ponzi). The **Fisher/debt-deflation basin is deliberately UNWIRED**
  (no default/impairment) — that's Phase 2; do NOT read Phase 1 as "the crunch stabilizes."
  Crunch-off recovers CYB-17 byte-exact; conservation `≤1e-16` through the deleveraging transient.

## Current validated state (don't re-derive — build on this)
- **Conservation** holds to <1e-10 (money + egg residuals). This is the crown jewel.
  Every refactor must keep the asserts in `model.py:step()` green. If they ever fire,
  stop and fix — a leak invalidates everything downstream.
- **Timing validated out-of-sample — and now data-driven.** Same model + same params
  reproduce BOTH the 2022-23 (peak Jan 2023) and 2024-25 (peak Mar 2025) price peaks; the
  2024-25 episode was never fit. As of CYB-7 the timing is driven by the **real NASS
  flock-inventory deficit** with **no fitted timing parameter** at all (`replace_lag`
  retired) — the timing improved (ep1 lands exactly on Jan 2023). This is the result that
  licenses trusting the mechanism.
- **Magnitude** bracketed by a single commodity-owned slope (egg pricer, linear in the
  real deficit). Recalibrated against the real NASS deficit to **≈24 %/pt** (CYB-9,
  `EGG_PRICING["slope"]=24.1`); the old ≈13 was calibrated off a synthetic deficit ~2×
  too large (a compensating-error pair — CYB-7 fixed the deficit, CYB-9 the slope). A
  linear-vs-concave OOS model comparison (CYB-14) found no generalizing curvature → the
  pricer stays **linear** (one parameter, earned).
- **Distributional wedge** (the namesake) computed on the validated price path × real
  income/egg-share data: ~5.5× regressive (poorest quintile's personal egg-inflation
  vs richest).

## Non-obvious decisions and WHY (the stuff that isn't in the code)

1. **`replace_lag` is RETIRED (CYB-7) — the one soft spot is gone.** It was the
   *effective* flock-recovery lag, defensible-but-provisional because it was chosen
   partly to land the peak. It is now superseded: the model is driven by the **real
   USDA-NASS monthly table-egg layer-inventory series** (`data/nass_layers.py`,
   deseasonalized vs the 2020-21 pre-outbreak normal), which needs no lag assumption.
   Timing survived and *improved* (both peaks land; ep1 exact). `hpai_culls`'s
   `replace_lag` path is kept only for the `v09` side-by-side. The committed fixture was
   verified byte-for-byte against a live QuickStats pull (`fetch_live`, needs
   `NASS_API_KEY`); the model path stays deterministic (no live call at import).

2. **The pricer slope is a COMMODITY property, not an engine constant.** It moved from
   `Params.supp_up` to `pricers.py:EGG_PRICING`. The engine is commodity-blind: a
   commodity names a pricer + carries its slope; the engine dispatches. This matters
   for the whole architecture — milk/microchips will register their own. Don't push
   pricing knobs back into the engine.

3. **"Convexity" was the wrong diagnosis; "saturation" was tested and also rejected.**
   Reality is ~LINEAR in the deficit — NOT convex (the convex miss was an artifact of
   pricing off `flow_gap = 1/(1-deficit)`; keying off the deficit directly fixed it). A
   mild *concavity* at the two peaks then looked like a candidate egg property (a
   saturating `markup = slope·deficit**alpha`), but CYB-14 tested it honestly — a
   linear-vs-concave **model comparison on the full monthly path, OOS on ep2** — and the
   curvature did **not** generalize (the free power exponent landed at α≈1.03, not
   concave; the forced-concave form was worse). It lives only *between* the two peaks and
   is within-noise at the path level. Verdict: **keep the linear pricer**; don't carry an
   unearned second parameter. The `power_deficit`/`saturating_deficit` forms remain in the
   registry as the documented comparison harness (not adopted).

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
- **Formal global-bifurcation proof — GATED (CYB-13).** The chaos onset is a nonsmooth fold
  of a *coexisting limit cycle*, not a local bifurcation of the equilibrium (CYB-4). It is
  the prime **external-mathematician validation** candidate (piecewise-smooth specialist),
  and it is explicitly **gated on human expert review — do NOT solo-build** (the standard
  normal-form reduction is not even a theorem here; unsupervised it produces confident
  error). Hand-off brief + first technical move (center-manifold reduction) are on CYB-13;
  the honest limits are documented (`docs/solutions/`).
- **Sustaining channels — the next mechanisms.** Both *transmission* channels (recursion,
  conflict) are built and coupled (CYB-6/10). Next is **reflexivity** (expectations /
  indexation) then **accommodation** (money/credit ratifying the nominal runaway — the seed
  CYB-16 frames it as the monetarism critique; needs math + econ buy-in). Accommodation is
  what would *bound* conflict's nominal spiral.
- **CYB-10 follow-ups.** H2 — *characterize* the chaos-leakage (the binary is answered:
  the nominal path inherits the real chaos; open question is spectra / partial filtering).
  And **bidirectional** coupling (inflation → nominal ordering), vs the current one-way.
- **SFC integration of the bullwhip oracle** — fold CYB-1's standalone 3-tier chain into the
  conserved engine so the integrated model reproduces the measured amplification ratios.

**Egg model (mostly blocked on data, not cleverness):**
1. ~~**NASS monthly layer-inventory series** → retires `replace_lag`.~~ **DONE (CYB-7).**
   Pulled from Quick Stats (`CHICKENS, LAYERS, TABLE - INVENTORY`, national, monthly);
   cached deterministically in `data/nass_layers.py`, verified == live API.
2. ~~**Saturation term** in the egg pricer.~~ **DONE (CYB-14) — tested & rejected.** No
   generalizing curvature on the OOS path; keep the linear pricer.
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
The egg foundation is on real data end-to-end (NASS flock + linear pricer, both episodes
OOS-clean); both transmission channels are built and coupled (CYB-6/10); and the first
**sustaining** channel — accommodation — is built on bare CYB-6 (CYB-17) and on the coupled
stack (CYB-18), and the **Minsky crunch Phase 1** (CYB-19) fires that solvency border. The
natural next moves: (a) **CYB-19 Phase 2** — default + an impairable rentier pool → the
debt-deflation / Fisher basin, closing the loop Phase 1 deliberately left open (the genuine
extension of CYB-17's balance sheet); (b) **CYB-19-on-coupled** — the crunch on the egg stack,
where CYB-18 showed it's central; (c) **CYB-20** — reflexivity / expectations, the other
sustaining channel; (d) **CYB-21** — supply-chain financing (the rate's 4th channel); or (e) a
**CYB-10 follow-up** (H2 chaos-leakage spectra / bidirectional coupling). The formal proof
(CYB-13) and the monetarism critique (CYB-16) wait on external buy-in — do not pick them up solo.

## Repo / run notes
- All code lives under `src/`. Engine modules (`model.py`, `pricers.py`, `events.py`)
  and `data/` import as siblings, so `cd src` and run `vNN_*.py` from there.
- `requirements.txt`: numpy, matplotlib only.
- GitHub: github.com/Goldcap/Cybeersym (public, MIT).
- Sandbox limitation that shaped the build (now lifted under Claude Code): the prior
  environment couldn't reach FRED/NASS APIs directly — real data was scraped via page
  fetches. With real network access, pull from source APIs instead.
