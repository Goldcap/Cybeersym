# Frozen structural-SFC model borders resist zero-fit empirical instantiation

**A methodological boundary result — two pre-registered attempts, both refuted at the design stage,
before any data was touched.** This is a negative finding worth as much as a positive one: it maps the
edge of what the wind-tunnel method can honestly claim, and it is the pre-registration discipline doing
exactly its job (stopping a validation that would have been a units/structure sleight-of-hand).

## The ambition (CYB-28 slow-manifold / Q-2026-005)

A distributional slow variable (WID wealth concentration) is hypothesized to be the **slow manifold**
that walks a fast SFC model across a **regime border**. The trophy: validate a **frozen** model border
against **independent** data, **zero-fit**, and show the approach is *more informative than the standard
leverage/inequality story* — the non-circular, model-first-then-correlate test staged as the empirical
payoff in the thesis roadmap (doc 08). Two borders were tried; each was pre-registered and each was
**refuted at design**, for a common root reason.

## Attempt 1 — the Fisher α_p border (CYB-38, pre-reg locked `6338f3a`)

The pre-registration committed the border to a **graded tipping α_p** from the Fisher sweep, explicitly
NOT the degenerate α_p→0 corner. Its §3 prerequisite (`src/fisher/run_v1.py`, reviewer-gated) resolved
the α_p interval the shipped grid had stepped over and found:

- The deflation-side border is a **hard corner at exactly α_p=0** (n-stable to 100k), not a graded tip.
- The bounded regime is a **smooth-monotone gradient** — i.e. the very null a threshold test must beat.

So the committed graded border **does not exist**; the test is uninstantiable as written. Per the lock's
forbidden moves it was **not** rescued (no swapping the variable, no redefining the border). Reportable
null-of-feasibility.

## Attempt 2 — the Keen breakdown-basin border (CYB-39)

A border that IS graded and already exists: the Keen debt-deflationary breakdown-basin boundary
`d₀*(r)` from `src/goodwin_keen/`. Two rounds:

- **v1 (locked, then VOIDED before merge).** The advisory review caught three substantive design flaws:
  a Spearman rank-correlation *success criterion* that contradicts the doc's own anti-triviality guard;
  a **circular train/withheld split** (the training set was the famous crisis banks — selecting on the
  outcome); and a **"preferred ordinal" mapping that cannot instantiate the cardinal border** (a
  rescaling-invariant ranking can't place an era relative to a cardinal `d₀*`). No data was touched, so
  the void was clean.
- **v2 (redesigned, PRE-LOCK adversarial review — never locked).** v2 moved the cardinal axis to **real
  measured leverage** (`distance = d_real − d₀*(r_real)`), demoted Spearman to context, and de-circularized
  the split. A fresh reviewer ran the model first and found the fatal problem: the benchmark's border is
  **`d₀* ≈ 3.25–9.93`** in its own *uncalibrated* `D/Y` units, while real BIS private-leverage runs
  **~1.0–2.5**. They are **not commensurable** — the whole real-data cloud sits below the border, so the
  threshold indicator is **degenerate** (predicts ~zero breakdowns, including at every actual crisis), and
  bridging the units needs a normalization constant `k≈3–5` — which **is fitting the border to the data**:
  the v1 cardinal-mapping flaw reborn on the leverage axis. The "zero-fit" claim was therefore false.
  Additionally the border's position is dominated by `r` (swings ~6.7 units of `D/Y` over a 3-pt rate
  change vs ~1 unit of cross-country leverage variation), and the distributional test collapsed to the
  known Kumhof–Rancière / Minsky **"inequality → crisis"** claim without the frozen border doing any work.

## The root cause (why both failed, and why it generalizes)

**Structural / benchmark SFC model borders live in the model's own units and structure.** Instantiating
one against real data requires *either*:

1. a border that is simultaneously **graded** AND in **commensurable units** with a real observable —
   the Fisher border failed the first (a corner), the Keen border failed the second (uncalibrated units);
   *or*
2. a **calibration constant** bridging model↔real units — which **is fitting the model to the data**, the
   one thing the method forbids (every prior version that shaped an input to fit an output got refuted).

And the escape hatch — testing only the model's *dimensionless structural predictions* (a threshold
exists; it moves with rates; it moves with concentration) — tends to **collapse to already-known macro
claims** (leverage/inequality → crisis), so it fails to secure "more informative than the standard story."

## Implication / scope

- The empirical **trophy** — a zero-fit validation of a frozen structural-model border against real
  distributional data, *demonstrably more informative than the standard story* — is **not cleanly
  achievable with the current benchmark models.** It remains **future work** (doc 08), contingent on
  either (a) a **calibrated** model (accepting explicit egg-discipline calibrate-freeze-OOS fitting, a
  departure from the zero-fit ideal), or (b) a genuinely dimensionless, **model-specific** structural
  prediction that does not reduce to a known macro correlation — which we tried and could not design.
- **What is NOT in doubt:** the model borders themselves are real and characterized (the Fisher hard
  corner; the Keen graded basin `d₀*(r)`). This finding is only about their **empirical instantiation**,
  not their internal validity. The wind-tunnel method remains productive for **counterfactuals** (its
  actual product); the empirical-validation ambition is what hit the wall.
- **The discipline worked.** Pre-registration + the reviewer gate caught **both** non-instantiable designs
  *before any data was examined* — no fooling-ourselves validation shipped. This is the single strongest
  demonstration in the project so far that the method protects against self-deception.

## Escalation recorded (the gate climbed a rung)

Because pre-registration *design* flaws recurred (CYB-39 v1's three flaws, tracing to the same
cardinal-mapping issue latent in CYB-38), the gate escalated: a pre-registration is now put through a
**fresh independent adversarial review BEFORE it is locked**, not after. That pre-lock review is exactly
what caught v2's two fatal flaws here. See `docs/reviewer-gate-log.md` entry #6.

## Related
`src/fisher/run_v1.py` (Fisher corner) · `src/goodwin_keen/` (the Keen basin) ·
`docs/preregistrations/2026-09-05-classifier-vs-wid.md` (CYB-38, locked) · CYB-39 (voided/banked) ·
`docs/thesis/08-future-work-roadmap.md` · `research/notes/concepts/phase-space-macroeconomics.md` ·
Q-2026-005 / CYB-28.
