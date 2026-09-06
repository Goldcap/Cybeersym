# Pre-registration #2 — does the Keen breakdown-basin border track WID wealth concentration?

> **Status: LOCKED (2026-09-06).** Written **blind to the WID series** — no WID values were examined
> in composing it — and its a-priori commitments (concentration → Keen breakdown-basin leverage
> border, threshold-not-smooth discriminator, ordinal zero-fit mapping, independent crisis
> chronology) were signed off by Andy **before** this commit. **The commit that adds this file IS the
> lock:** nothing above the lock line may change hereafter. The WID evaluation is a *separate,
> subsequent* commit that references this one by hash and may not alter the rule; a change to the
> locked content voids the pre-registration.
>
> **Why a second pre-registration.** The first (`2026-09-05-classifier-vs-wid.md`, locked `6338f3a`,
> CYB-38) named the **Fisher α_p** border. Its §3 prerequisite (`src/fisher/run_v1.py`, reviewer-
> gated) found that axis has **no graded border** — genuine divergence is a hard corner at exactly
> α_p=0, and the bounded regime is a smooth-monotone gradient — so that test is **uninstantiable as
> written**. Per the lock's forbidden moves we did **not** edit CYB-38 to rescue it. This is a
> **new, independent** pre-registration against a border that IS graded and already exists in the
> repo. It does not alter CYB-38; it supersedes it only as the *live* CYB-28 slow-manifold probe.

## The discipline (literal, from the egg solve — we do NOT fit functions to data)

Mirrors, move for move, how the egg problem was solved without fitting (identical to CYB-38):

- **The fitted parameter was removed, not tuned** (egg: CYB-7 retired `replace_lag`; real NASS series
  drives timing). → *Here: the slow-variable driver is a real measured WID series; the border is
  frozen from the Keen model's mechanism. Neither is fit to the outcome data.*
- **At most one constant, calibrate-freeze-validate-OOS, never re-tuned** (egg: CYB-9 slope). → *Here:
  the mapping is preferentially zero-constant (ordinal); any unavoidable scale is calibrated on
  declared training country-eras, frozen, validated OOS, mismatch reported.*
- **Model shape defended by rejection, not fitting** (egg: CYB-14 rejected saturation). → *Here: the
  border structure is the model's; we add no degrees of freedom to make the data fit.*

---

## H — The hypothesis, stated a priori (the CYB-28 bet)

**A slowly-drifting distributional variable is the slow manifold that walks the fast model's
regime-parameter across its border.** Committed before data:

- **Slow variable (the driver):** a real measured **WID wealth-concentration** series (top-10% /
  top-1% **wealth** share; secondarily the **capital–income ratio β = wealth/income**, which WID
  covers deep and dense, 1800–2025 for the major economies) — normalized against a per-country
  *reference* baseline (mirroring the egg's 2020-21 normal), NOT against its own outcome.
- **Model regime border it maps to:** the **Keen debt-deflationary breakdown-basin boundary** —
  the critical initial leverage **d₀\*** separating Keen's stable "good" equilibrium from the
  debt-deflationary breakdown basin (d→∞, ω→0, λ→0), as computed by the frozen model in
  `src/goodwin_keen/` (`_critical_d0`, `_outcome`; the (r, d₀) basin map). This is a **global**
  basin boundary (taxonomy C1→E), and a higher interest rate **r** shrinks the good basin.
- **Direction (a-priori sign, no free magnitude):** higher wealth concentration ⇒ **larger rentier
  debt-claims ⇒ higher effective economy leverage d (and/or higher effective r) ⇒ a smaller good
  basin ⇒ closer to / across the breakdown boundary ⇒ more crisis-prone.** This is Keen's own
  Minsky mechanism. *It is the a-priori bet; it can be false, and a null falsifies it.*

## The anti-triviality guard (READ THIS FIRST — it is load-bearing)

"Higher leverage → more crises" is **exactly what Minsky/Keen already argue** and what the mainstream
half-concedes. A smooth monotone concentration→fragility correlation would therefore be **trivial and
would NOT count as the model being right.** The model's specific, testable, non-trivial content is its
**border STRUCTURE**, and success is defined only against it:

1. **A THRESHOLD, not a gradient.** The breakdown basin is a *step*: below d₀\* the economy survives,
   above it collapses. The primary discriminator is **threshold-beats-smooth-monotone out-of-sample**
   (the Option-A shape test, egg-CYB-14 discipline). A smooth "more leverage → more crisis" fit is the
   **null we must beat** — beating it is the only thing that licenses "more informative than the
   standard leverage story."
2. **The interest-rate interaction.** The model predicts the basin **shrinks as r rises** (d₀\* falls).
   A secondary, pre-registered check: among high-concentration eras, the fragile ones should be
   disproportionately the **high-real-rate** ones — an interaction the trivial story does not predict.

## F — What is FROZEN (from the Keen model, not from WID)

- **The border** is the critical leverage **d₀\*(params)** and the basin map r ↦ d₀\*(r), read from
  the frozen `src/goodwin_keen/` model (KEEN defaults), **calibrated to no macro dataset**.
  **Distance-to-border** = the frozen model's `d − d₀*` (how far an era's mapped leverage sits from
  the survival threshold).
- **The model parameters** are the repo's benchmark Keen values, frozen.
- Nothing in F is (re)estimated from WID or from the outcome labels.

## M — The a-priori mapping (egg-slope-disciplined)

- **Preferred — zero-fit (ordinal).** Compare the model's frozen distance-to-border **ranking** of
  country-eras against the observed fragility ranking; and test the **threshold** (§guard 1) against
  the smooth-monotone null. No constant estimated from WID.
- **Only if a scale is unavoidable — one constant, egg-discipline.** Calibrate a single
  concentration↔leverage scale on a **declared training** set of country-eras (chosen by a coverage
  rule, *not* by their values), freeze it, validate OOS on the withheld set, and **report the mismatch
  honestly** even if it fails. Never re-tune.

## D — The decision rule (pre-registered — what counts as the model being right)

- **Primary (the threshold test):** a threshold model (fragility jumps as the mapped slow-variable
  crosses the frozen border) must **beat a smooth-monotone model out-of-sample** on the withheld
  country-eras by a pre-stated margin (exact model-comparison statistic + margin fixed in the Phase-A
  analysis lock, before the withheld set is opened).
- **Secondary (contingency):** a 2×2 over the withheld eras — *(WID slow-variable above / below the
  frozen border) × (independent fragile / stable outcome)* — beating chance by a pre-stated margin.
- **Tertiary (the r-interaction):** among above-border eras, fragility concentrates in the
  high-real-rate ones (sign fixed here).
- **Secondary rank check:** Spearman ρ between distance-to-border and the fragility ordering (sign +
  min |ρ| fixed in the analysis lock).
- All are **frozen before the withheld set is opened.**

## Outcome labels — INDEPENDENT of both WID and the model (no circularity)

"Fragile outcome" (a crisis / regime shift in a country-era) comes from the **Laeven–Valencia IMF
Systemic Banking Crises Database** (systemic banking-crisis start years) — named and fixed here,
**not** from WID and **not** from the model. This is the load-bearing anti-circularity guard: the
border is the model's, the driver is WID, the *outcome* is a third, independent source.

## S — The data split (fixed blind to WID values)

- **Training country-eras** (only if the one-constant calibration is used): a small declared set
  chosen by a *coverage/availability* rule, listed in the Phase-A analysis lock before any values are
  seen. Candidate reproducibility banks (from the natural-experiment portfolio): **Nordic 1990s**
  (SE, FI, NO), **Asian 1997** (TH, ID, KR, MY), **Latin America 1980s–90s** (AR).
- **Withheld / validation set:** all remaining country-eras with adequate WID + Laeven–Valencia
  coverage — **untouched until the analysis lock is committed.**

## The forbidden moves (we refuse these explicitly)

1. Fitting the mapping function to WID. 2. Choosing the border threshold post-hoc to maximize the
match. 3. Re-tuning anything after seeing the withheld result. 4. Relabeling "fragile" after the fact.
5. Swapping the slow variable, the border, or the metric after a null. 6. Declaring victory on a
smooth monotone "leverage → crisis" correlation (that is the null, per the anti-triviality guard).
Any of these voids the pre-registration.

## What a NULL result means (stated before the data)

If the frozen Keen border + a-priori mapping does **not** beat the smooth-monotone null on the
withheld set, the **CYB-28 slow-manifold hypothesis is falsified for this border** (or the border is
mis-placed) — a real, reportable result, exactly like the egg magnitude overshooting OOS, and exactly
like CYB-38 §3's null-of-feasibility. We report it and do **not** tune to rescue it. A null here is
worth more than a fitted "success."

## Honest caveats (pre-stated)

- **The triviality trap is the main risk.** If the model only reproduces "leverage → crisis," it has
  added nothing; the threshold + r-interaction tests exist precisely to hold that line, and a
  smooth-only result is reported as a (partial) null.
- **Small-N.** Few clean country-eras; pre-registration is the only defence against fooling ourselves
  — hence the two-stage lock (this design lock → the Phase-A analysis lock → the sealed join).
- **The mapping is the bet.** If distributional slow variables are not the ones that move the border,
  the probe fails honestly — itself the CYB-28 finding.
- **WID comparability** across a century + countries (Piketty's own caveat); gate every test on the
  *dense* window, never the nominal span (INVENTORY findings #3–#4).
- **Benchmark scope.** `src/goodwin_keen/` is a benchmark instrument (its larger orbits are not
  economically bounded); this test uses its **basin-boundary structure**, not a claim that the
  benchmark's numbers are a calibrated economy. Scope: a *correlation* of a frozen model's border
  against independent data — a domain-of-validity check, **not** a forecast-superiority claim.

---

<!-- LOCK LINE — nothing above this line may change after the commit that locks this pre-registration.
     The WID evaluation is a separate document/commit that references this one by hash. -->
