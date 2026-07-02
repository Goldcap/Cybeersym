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

## v0.9 — real flock stock retires `replace_lag`  ·  `v09_real_flock.py`, `data/nass_layers.py`  ·  `591b364` (CYB-7)
Replaced the model's one fitted timing parameter with the **real USDA-NASS monthly
table-egg layer-inventory series** (`CHICKENS, LAYERS, TABLE - INVENTORY`, national),
deseasonalized against the 2020-21 pre-outbreak normal. The deficit peaks land **2023-01
and 2025-03 — both real price peaks — with zero timing parameters**, and fed through the
model reproduce both peak months; ep1 is now *exact* (the synthetic lag path peaked a
month early). The committed fixture was verified byte-for-byte against a live Quick Stats
pull. Crossing from clean-room to observational data (the CYB-3 honesty firewall now
load-bearing); claim stays *mechanism reproduces the episode*, not price prediction.

## v0.10 — recalibrate the pricer slope on real deficits  ·  `v10_pricer_recal.py`  ·  `c21b2d6` (CYB-9)
The real deficits are ~half the synthetic ones, so the frozen slope now undershot. The
honest split (calibrate on ep1, freeze, validate OOS on ep2): slope **13 → 24.1**, which
independently matches the raw deficit-price ratio. **Timing survives; magnitude degrades
honestly and is NOT re-tuned** — the single linear slope overshoots ep2 OOS (+316% vs
+272%). Framed as a **compensating-error pair split into two correct values**: CYB-7 fixed
the ~2×-too-large deficit, CYB-9 the ~2×-too-small slope. The pre-CYB-7 scripts (v05-v08)
are pinned to slope=13 to preserve their historical figures.

## v0.11 — does the pricer saturate? (model comparison)  ·  `v11_saturation.py`  ·  `8deba75` (CYB-14)
The ep2 overshoot hinted mild concavity at the two peaks. Tested honestly as a
**linear-vs-concave model comparison** — calibrate both on ep1's full monthly *path*,
freeze, validate OOS on ep2's path. Verdict: **concavity does NOT generalize → keep
linear.** The nested power form's free exponent lands at α≈1.03 (not concave); the
forced-concave saturating form is worse OOS. The curvature lives only *between* the two
peaks, within-noise at the path level. Parsimony as a positive result: the data supports
one pricer parameter, not two. (The 2015 bonus point wasn't available — NASS series starts 2020.)

---

## Module track — conserved-network instruments & channels (CYB-1…10)

The egg model proved the **method** on a validated commodity. This track carries it onto
the THESIS recursion channel: a conserved producer network with chaos-measurement tooling
wrapped around it from day one. Standalone modules (`src/bullwhip/`, `src/chaos/`), same
conservation + determinism discipline. Specs are canonical in Linear (CYB-N); per-module
READMEs, `docs/plans/`, and `docs/solutions/` carry the detail.

### CYB-1 — recursion / bullwhip v0  ·  `src/bullwhip/`  ·  `bc8946e`
A 3-tier chain amplifies order variance from demand-signal processing alone: chain ratio
**local 36.6× → shared 10.9× → coordinated 2.9×**. The finding — *seeing true demand is
not enough; you have to act on it*: sharing the forecast only **suppresses** compounding;
only echelon replenishment against true end-demand **flattens** it. Validated against Chen
et al. (2000) to ~1%, frozen-forecast regression = 1.000, conservation 3.4e-11. (Spec
earned a correction: two modes → three.)

### CYB-2 — deterministic chaos, nonsmooth onset  ·  `src/chaos/`  ·  `fb5440d`
Swap the order-up-to rule for Sterman's anchoring-and-adjustment heuristic (noise OFF) and
sweep the supply-line weight β: the same conserved chain generates **deterministic chaos**
— positive largest Lyapunov exponent (λ up to +0.054) on a bounded attractor, sensitive
dependence, byte-deterministic, goods conserved (4.9e-15 rel). The route is a **nonsmooth /
border-collision onset**, not a smooth Hopf: the equilibrium stays linearly stable
(|λ|≈0.91, never crosses 1) while a constraint-riding attractor is born **coexisting** with
it (bistability); the active border is **order non-negativity**. Reusable instruments:
`lyapunov` (self-test ln2), `bifurcation`, `linearize`. (Two framing corrections earned:
period-doubling → Neimark–Sacker → border-collision.)

### CYB-3 — empirical grounding  ·  `docs/empirical_grounding.md`  ·  `d01d522`
The behavioral spine, every claim source-verified: the supply-line-underweighting bias
driving β is real and measured (Sterman 1989 mean β=0.34, his β=α_SL/α_s **is** our β;
robust across Croson–Donohue and 35 years), field signatures (amplification, oscillation)
reported with their disconfirming caveats, and an honesty firewall on why direct
chaos-detection in macro series failed (so the claim is illustrative, not predictive).

### CYB-4 — formal border-collision classification  ·  `src/chaos/normal_form.py`  ·  `4511b50`
A reusable, self-tested Nusse–Yorke / Banerjee–Grebogi classifier, and the structural
finding it produced: the boundary-equilibrium normal form **does not apply** — the
equilibrium is interior to both switching manifolds and **non-hyperbolic for all β** (three
eigenvalues pinned at λ=+1, the supply-line conservation law / stock-flow consistency as a
permanent center subspace). So the onset is a **global nonsmooth event** (a border-collision
of the coexisting cycle), not a local bifurcation of the equilibrium. **Conservation is the
obstruction — load-bearing twice.**

*(CYB-5 ✅ doc-sync propagated CYB-1…4 into HANDOFF/THESIS/CHANGELOG. CYB-13 🔒 the formal
global-bifurcation proof is gated for an external mathematician — not a Claude Code build.)*

### CYB-6 — conflict layer, the second transmission channel  ·  `src/conflict/`  ·  `015f6e7`
Wage-price conflicting claims over a conserved pie (wage share + profit share = 1). The
**real wage share is a stable node; the instability is purely nominal** (a sustained
price-level spiral) — the *opposite* dynamical character to CYB-2's bounded real chaos.
Steady rate matches the Rowthorn–Lavoie closed form `π*=(α_w·α_p/(α_w+α_p))·g` to 6e-17.
The pure mechanism is symmetric (inflation/deflation ∝ gap); the **nominal-wage floor**
(downward rigidity) breaks the symmetry, creating the dissipate-below / transmit-above
threshold at gap=0 — a real constraint as the switching manifold, echoing CYB-2's border.
First cross-module reuse of the CYB-2 instrument suite, self-tested before use.

### CYB-10 — recursion × conflict coupling, super-additive ignition  ·  `src/coupling/`  ·  `109c998`
Couple the two transmission channels one-way (chain scarcity `d(t)` raises the aspiration
gap: `g(t)=g0+κ·d(t)`). A *subthreshold* shock that neither channel alone ignites lights a
**sustained wage-price spiral** — inflation emergent from a pair whose parts don't inflate.
The **κ=0 decoupling regression reproduces CYB-2 and CYB-6 byte-for-byte**, so the emergence
is real, not a composition artifact. Sharpened mechanism: recursion's *endogenous*
instability is a **persistent-scarcity generator** — a transient shock dissipates, only the
self-sustaining bullwhip holds `g>0`, so recursion **sustains, doesn't just amplify**; the
real chaos leaks into the nominal path (π aperiodic — a positive H2 preview). Both
conservation laws hold simultaneously through the ignited regime (<2e-15).

### CYB-17 — accommodation: credit ratification + the rate's channel decomposition  ·  `src/accommodation/`  ·  `64fe816`
The first **sustaining** channel. Finance the wage bill at a policy rate `i` (working-capital
finance); the rate acts through **three channels at once** — cost (+, feeds), symmetric-demand
(−), distributional (−, breaks labor). Two findings: CYB-6's "unbounded" runaway was the
**full-accommodation limit** hiding as a law (name the financing constraint and it becomes
*conditional*); and the financed rate is a **tug-of-war whose winner is a parameter, not a
verdict** — only the distributional channel drives `π*` to zero (it *exhausts* once labor's
gap is closed → cost then dominates → the restraint-insufficient region). Solvency ceiling
completes the switching-manifold set. `i→0`, cost-off regression reproduces CYB-6 byte-exact.

### CYB-18 — accommodation on the coupled substrate  ·  `src/accommodation_coupled/`
CYB-17's machinery **unchanged** on the CYB-10 coupled stack (recursion re-loads the gap
`g=g0+κ·d`). Inheritance build, **two** byte-exact anchors (`κ=0`→CYB-17; full-accommodation
→CYB-10). Headline: the distributional channel **no longer self-exhausts** (recursion re-supplies
its target every period) — but it also **never wins**: recursion pins a positive inflation floor
`≈k·κ·⟨d⟩` the rate can't reach through any channel, so the rate turns **redistributive, not
stabilising** (no rate drives `π` to 0; the cost-flip region survives and is hotter). The rate
also **gates super-additive ignition both ways** (cost-push lowers the coupling threshold `κ*`,
disinflation raises it). Three nonsmooth borders live at once — the **solvency ceiling dominates
and pre-empts the wage floor**. All three conservation laws green (<1e-15).

### CYB-19 (Phase 1) — Minsky credit-crunch cascade  ·  `src/crunch/`
Fire the solvency border (static in CYB-17/18): a financing-regime classifier
(hedge→speculative→Ponzi, from CYB-17's existing flows) + a deleveraging-rate cascade that
arms at **Ponzi ∧ border**. Headline: **bounding vs fizzle is an OUTCOME the parameters pick,
not a design choice** — over (leverage-at-trigger, deleverage rate δ), fast/early deleveraging
**bounds** the spiral (→12% of baseline), slow/late **fizzles** (→85%), above the rate-set
baseline leverage it never fires. But the crunch **bounds without curing** — even a hard crunch
only chokes via a grinding **limit cycle at the border**, never to zero. Two "reveal what was
there" notes: **Ponzi ≡ CYB-17 capitalizing uncovered interest** (renamed, not new), and
**leverage-at-trigger is set by the policy rate** (hiking tips the aggregate into Ponzi). The
**Fisher debt-deflation basin is deliberately UNWIRED** (no default/impairment) — Phase 2. Crunch-
off recovers CYB-17 byte-exact; conservation `≤1e-16` through the deleveraging transient.

### CYB-22 — the credit-crunch on the coupled egg stack  ·  `src/crunch_coupled/`
Pure inheritance: CYB-19 Phase 1's crunch on CYB-18's coupled substrate. **The
bounds-without-curing grind gets WORSE under reloading** — recursion re-ignites the spiral in
the crunch's recover phase, so the achievable choke floor rises (bare 7% → coupled 12% of
baseline), the limit-cycle amplitude ~3×s (1.02 → 2.93 %/step), and the crunch is uniformly
less effective. The solvency border stays dominant (73%→63%) but chokes less per bind. TWO
byte-exact anchors (crunch-off → CYB-18; κ=0 → Phase 1); conservation `1e-15` through the transient.

### CYB-23 (CYB-19 Phase 2) — default + impairable rentier: the impairment horizon  ·  `src/contagion/`
Let Phase 1's grind terminate in **default**, and make the rentier pool **impairable**. Headline:
the **impairment horizon** — sweep the impairment→premium elasticity ε — **cure ↔ contagion-
collapse, both reachable, a RAGGED frontier**: two feedbacks compete (impairment→risk-premium→more-
Ponzi contagion vs inflation→P↑→impairment/P↓ self-cure). **Counterintuitive: a bigger haircut
(lower recovery) is MORE stabilizing** (collapse 5% vs 62%) — clearing more debt per default cures
the borrower faster than the extra impairment detonates. The collapse is a hyper-INFLATIONARY
premium spiral (Engine 1, credit-quantity), **NOT Fisher debt-deflation** (Engine 2, gated OFF; and
CYB-17's demand channel disinflates but never deflates → Fisher needs a strengthened price channel,
Phase 2b). The SFC payoff: write-offs as **STOCK events**, capital-account identity (rentier asset ≡
firm liability, Godley–Lavoie) closes `≤4e-12` through defaults AND collapses. Nested `CYB-17 ⊂ P1 ⊂
P2` byte-exact at each shell.

### CYB-24 — doc-sync: THESIS.md re-woven for the accommodation→crunch arc  ·  `THESIS.md`
Successor to CYB-15 (which stopped at CYB-10). Extends the "From map to mechanism" narrative
through CYB-14 (concavity rejected — the null result, kept), CYB-17/18/19/22/23 as one continuous
argument, and **states the switching-manifold through-line explicitly as the meta-thesis**: order
non-negativity → wage floor → full-accommodation limit → solvency ceiling → capitalized-interest/
Ponzi — *the real constraint is the load-bearing switching feature, hiding in plain sight*. The
descriptive/normative firewall is reinforced (report what the rate does; the monetarism/CYB-16
conclusion stays out; "orthodox tool is distributional" kept apart from "heterodox tools work
better"). Narrative, not changelog; cross-refs each module README.

---

## Current stable engine (unversioned — the validated core)
- `model.py`   — SFC engine, conservation asserts, 5 income quintiles, supplier/store,
                 seasonal-demand hook, commodity-pricer dispatch.
- `pricers.py` — commodity pricer registry; `EGG_PRICING` (linear_deficit, slope **24.1**,
                 real-deficit-calibrated, CYB-9); `power_deficit`/`saturating_deficit` are
                 the CYB-14 comparison forms (concavity tested, not adopted).
- `events.py`  — adverse-event plugin layer: pure supply/demand path-transforms,
                 multiplicative composition, registry, load-time validation.
- `data/`      — real fixtures: FRED prices, **NASS monthly layer inventory** (the flock
                 stock, CYB-7), USDA culls + flock transform, seasonality.
- `conflict/`, `coupling/` — the two transmission-channel modules (CYB-6, CYB-10),
                 standalone; reuse the `chaos/` instrument suite unchanged.
- `accommodation/`, `accommodation_coupled/` — the sustaining channel (CYB-17) and it
                 on the coupled stack (CYB-18); compose the above modules unchanged.
- `crunch/`    — the Minsky credit-crunch cascade, Phase 1 (CYB-19); fires the CYB-17
                 solvency border; composes `accommodation/` unchanged.
- `crunch_coupled/` — the Phase-1 crunch on the coupled egg stack (CYB-22); composes
                 `chaos/` + `crunch/` unchanged via the CYB-18 reload.
- `contagion/` — CYB-19 Phase 2 (CYB-23): default + impairable rentier; the impairment horizon;
                 composes `crunch/` unchanged; capital-account (balance-sheet) reconciliation.

## Open threads (named, mostly blocked on data, not cleverness)
1. ~~**NASS layer-inventory series** → retire `replace_lag`.~~ **DONE (CYB-7, v0.9).**
2. ~~**Saturation term** in the egg pricer.~~ **DONE (CYB-14, v0.11) — tested & rejected;
   keep linear.**
3. **Formal global-bifurcation proof (CYB-13)** — 🔒 GATED for an external mathematician
   (post-July-6); do NOT solo-build.
4. **Sustaining channels** — accommodation (money/credit) **DONE** on bare CYB-6 (CYB-17)
   and on the coupled stack (CYB-18); the **Minsky credit-crunch cascade Phase 1** (CYB-19)
   **DONE** (bounding-vs-fizzle); the **crunch on the coupled egg stack** (CYB-22) **DONE** (the
   grind worsens under reloading); **CYB-19 Phase 2 = CYB-23** (default + impairable rentier → the
   impairment horizon: cure vs contagion-collapse; a bigger haircut stabilizes; Fisher gated) **DONE**.
   Live next: **CYB-24** (THESIS re-weave, gated on 22+23), **Phase 2b** (switch Engine-2/Fisher on,
   after strengthening the price channel), **Phase-2-on-coupled**, and **reflexivity / expectations**
   (CYB-20). Seeds: **CYB-21** supply-chain financing (the rate's 4th channel). The monetarism
   critique (CYB-16) stays gated. Plus the **CYB-10 follow-ups**: H2 chaos-leakage spectra,
   and bidirectional coupling.
5. **Cost-matrix / third channel** — real feed-cost / natural-gas series into
   structural cost accounting (seam marked in `events.py`).
6. **Distributed virtual economy** — the "Distributive" half of the repo title:
   suppliers/stores as services, an event-sourced ledger as the conserved spine
   (= the MMT state balance sheet), ensemble runs + chaos measurement (Lyapunov,
   attractor stats) for *illustrative-not-predictive* validation. A separate project;
   today proved the *method*.
