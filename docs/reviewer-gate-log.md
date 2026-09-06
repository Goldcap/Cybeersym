# Reviewer-gate log — escaped defects & escalation

The honest error-rate record for the **reviewer gate** (see `CLAUDE.md` §"The reviewer gate",
spec **CYB-34**). Every "whoops / correction" is logged here — whether caught *at* the gate
(before merge) or *escaped* past it (found later by Andy or a downstream check). A recurring class
is the trigger to **climb the escalation ladder**, not to patch-and-move-on.

Columns: **when · what · where it had leaked · why the gate (nearly) missed it · the check that
caught / would catch it · gate outcome**. "Gate outcome" = *caught at gate* (fixed before merge)
or *escaped* (reached done/merge; the rows that should drive escalation).

---

## Entries

### 9 — 2026-09-06 · NAIRU v2 (matching-γ + expectations×NAIRU, `run_v2.py`) · **clean pass (cosmetic nit only) — positive signal**
- **What:** v2 micro-founds γ from a matching job-finding rate (γ=1−a) and composes the expectations
  channel with the NAIRU gap. A fresh reviewer re-derived γ=1−a and the composition closed form,
  independently confirmed the steepening, and — the two spots most likely to fail — verified (i) the v1
  **interpretation-inverted** bug (entry #8) did **NOT** recur (slack/tight labels correct), and (ii) the
  **sim-overflow transient trap was avoided**: the orthogonal borders and regime map are computed
  analytically, not from finite-horizon overflow (which the reviewer confirmed does overflow u-dependently
  below the true φ_e* — the transient the build refuses to present as the border). Only a cosmetic
  docstring nit (cost "rises with D" vs the ∝D actually used); fixed.
- **Check that caught it:** a fresh reviewer re-deriving both the matching→γ mapping and the composition
  from the sim's own map, and probing the sim for the transient artifact the build claims to avoid.
- **Outcome:** clean — no bug, no overclaim. **Escalation signal (positive):** the two recurring classes
  the gate has been climbing on (scope-overclaim #1–#3; interpretation-inverted #8) did not recur; the
  DMP simplification and the transient/steady-state distinction were both flagged honestly *by the
  builder* before the reviewer. The per-build fresh-reviewer cadence is holding; no ladder climb.

### 8 — 2026-09-06 · NAIRU v1 micro-foundation (CYB-20, `run_v1.py`) · **caught at gate — an inverted economic interpretation**
- **What:** v1 micro-founds the discipline function from Nash/McDonald–Solow bargaining and dials the
  outside-option convexity γ. The reviewer confirmed the load-bearing math — nesting (γ=1 ≡ v0 linear,
  matched to 1.1e-16, u\* exact), the closed form, the u\* decomposition, determinism, and the honest
  "relocates-not-removes" framing — but caught a **CONFIRMED BUG in the economic interpretation**: the
  γ-dial's slack/tight labeling was **inverted**. Since `|dπ/du| ∝ u^(γ−1)`, γ>1 is **flat at low u
  (TIGHT) / steep at high u (SLACK)** — it *flattens* near full employment; the runner and README
  claimed the reverse ("flat when slack, steep when tight") and mis-attributed "steepening near full
  employment" to γ>1 (it's γ<1). **The numbers and slopes were exactly right; only the words mapping
  curvature → market condition were backwards** — but that gloss is the section's load-bearing economic
  content and the stated *fingerprint direction*, so anyone taking it to data would match the wrong γ.
  Plus three NITs: "the objection evaporates" softened to "relocated, not removed"; `ω_e` was
  listed-but-not-swept (added to the decomposition output); the printed conservation residual came from
  an un-stepped economy (now read off the 400-step trajectory).
- **Check that caught it:** a fresh reviewer that **computed π(u) directly at low vs high u** (tight vs
  slack) rather than trusting the slope-label prose.
- **Outcome:** fixed before commit. Class = **interpretation-inverted** (a new class — the math is
  correct, the *economic gloss* is backwards). Escalation signal: this is exactly why the gate must
  re-derive the ECONOMICS, not just the arithmetic — here the arithmetic was flawless and the reading
  was reversed. Keep charging reviewers to attack the interpretation/prose, not only the numbers.

### 7 — 2026-09-06 · Two channel builds (expectations + NAIRU, CYB-20) · **caught at gate (NITs only) — positive signal**
- **What:** two new `src/` modules — `expectations/` (adaptive-expectations de-anchoring) and `nairu/`
  (the conflict/Kaleckian NAIRU) — each put through a fresh independent reviewer before commit. **Both
  headlines SURVIVED independent re-derivation:** for expectations the reviewer hand-derived the closed
  form *and* the 2×2 Jacobian (matched `linearize` to 2.85e-10) and confirmed a real +1-multiplier
  de-anchoring, stable throughout the physical range; for the NAIRU the reviewer re-derived
  `u*=(ω_w0−ω_f)/b`, confirmed the sim↔closed-form to 8.3e-17, and judged the (unavoidable) circularity
  objection *honestly owned, not hidden*. Only **NITs** found and fixed pre-commit: expectations — the
  real-vs-complex check ran at a single φ_e (→ swept and asserted), and "fold" overstated the evidence
  (→ "+1-multiplier / equilibrium escapes"); NAIRU — "~1e-17" undersold the 8.3e-17 error (→ "~1e-16"),
  and one polemical half-sentence ("used to justify recessions") tripped the descriptive/normative
  firewall (→ softened to the analytic policy corollary).
- **Check that caught it:** fresh reviewers re-deriving the math symbolically/numerically AND attacking
  the prose for overclaim (the NAIRU reviewer was charged specifically to flag preachy/oversold framing).
- **Outcome:** caught at the gate; fixed before the PRs. **Escalation signal (positive):** the
  *centerpiece-overclaim-about-our-own-results* class (entries #1–#3) did **not** recur — both new builds
  passed with only NITs, and the anti-overclaim net now catches *register-level* issues (the NAIRU
  polemic) before merge, not just numeric ones. No ladder climb; keep the fresh-reviewer-per-build cadence.
  Note the discovery discipline that fed these: a cheap probe found the expectations bifurcation was real
  (vs Fisher/recursion dead-ends) *before* the build — see the escaped-defect-avoidance in the probes.

### 6 — 2026-09-06 · CYB-39 pre-registration (v1 voided, v2 caught pre-lock) · **caught before lock → LADDER CLIMB**
- **What:** the second WID pre-registration (Keen breakdown-basin border) failed design review twice.
  **v1** was *locked* (PR #15) and then the **advisory review app** caught three substantive design
  flaws (a Spearman rank-correlation success criterion contradicting the doc's own anti-triviality
  guard; a **circular train/withheld split** selected on the outcome; a *"preferred ordinal"* mapping
  that cannot instantiate the **cardinal** `d − d₀*` border) → **VOIDED before merge** (no data touched,
  so clean). **v2** was redesigned (real leverage as the cardinal axis) and — per the escalation below —
  sent to a **fresh independent adversarial reviewer BEFORE locking**, which ran the model and found
  **two FATAL flaws**: the benchmark's `d₀*≈3.25–9.93` (uncalibrated `D/Y`) is **not commensurable** with
  real BIS leverage (~1–2.5), so the "zero-fit" border needs a normalization constant `k≈3–5` = **fitting**
  (the v1 cardinal flaw moved to the leverage axis), and the border sits **off the entire data cloud**
  (degenerate threshold, position dominated by `r`). Plus the distributional test collapsed to the known
  "inequality → crisis" claim. → **NEEDS REDESIGN; banked as a negative finding** (see
  `docs/solutions/frozen-model-borders-resist-zero-fit-empirical-instantiation.md`).
- **Where it had leaked:** the flaws were *in the pre-registration design itself* (locked-then-voided for
  v1; caught pre-lock for v2). No code shipped.
- **Why nearly missed:** the builder authored the pre-reg and the human design sign-off covered the
  *direction*, not the load-bearing internals (unit commensurability, split independence, ordinal↔cardinal).
- **Check that caught it:** v1 — the advisory code-review app on a *docs* file (beyond its nominal
  `src/**` scope, and valuable for it). v2 — a **pre-lock** fresh adversarial reviewer that *ran the
  model* to get `d₀*` magnitudes rather than trusting the prose.
- **Outcome / ESCALATION (the ladder climb):** pre-registration *design* flaws recurred (v1's three, tracing
  to the cardinal-mapping issue latent in CYB-38), so the gate escalated: **a pre-registration now gets a
  fresh independent adversarial review BEFORE it is locked, not after.** That pre-lock review is what
  caught v2. Class = *pre-registration-design-flaw* (recurring) → escalated one rung. The empirical arc is
  banked as a boundary result; the discipline caught both non-instantiable designs before any data.

### 5 — 2026-09-05 · Fisher α_p border, the WID prerequisite (CYB-38 §3, `run_v1.py`) · **caught at gate**
- **What:** the §3 finding — *the shipped Fisher α_p axis has no graded border; it's a hard corner
  at α_p=0* (which makes the locked WID test uninstantiable as written) — was sent to a **fresh,
  independent reviewer** (no builder context) charged specifically to **falsify** the headline. The
  headline **SURVIVED**: the reviewer pushed α_p to 1e-6 at n=100k, varied the classifier band and
  the grid, and confirmed the corner is a genuine n-stable singularity *consistent with* `run_v0`
  (evidence against a detector artifact — the failure mode that produced the retired Fisher
  "two-basin" headline). Two real defects were caught **beside** the verdict: (M) a **latent
  false-corner bug** in `border_alpha_p` — via the `last_div is None` path it would print "HARD
  CORNER at α_p=0" even where α_p=0 does *not* diverge (safe only because the tested φ∈{2,4,8} all
  diverge at 0); and (overclaim) **"interior kinks: 0 / monotone" was grid-fragile** — a finer grid
  turns limit-cycle sampling jitter into spurious reversals, so the literal integers held only on
  the coarse grid.
- **Where it had leaked:** the bug was latent (not on the live path); the grid-fragile claim was in
  `run_v1.py`'s printed Q2 line + docstring.
- **Why nearly missed:** the corner logic was not self-validating (no guard asserting α_p=0 actually
  diverges before declaring a corner); the "0 kinks" claim read the sign of raw successive diffs
  with no jitter tolerance.
- **Check that caught it:** a fresh reviewer that **re-ran with independent probes** (α_p→1e-6,
  n→100k, band and grid variations) rather than re-reading the printed output.
- **Outcome:** both fixed before the PR — `border_alpha_p` now returns an explicit
  `corner`/`graded`/`none` kind guarded on α_p=0 diverging (+ an assert for the tested φ), and the
  bounded-branch claim is now a **grid-robust** statement (no fixed-point region; net deepening;
  worst non-monotone wobble reported as a fraction of amplitude, < 0.2% = jitter). Verdict unchanged;
  byte-identical rerun; conservation ~1e-15. Class: *self-validating-guard-missing* (new) +
  *grid-fragile scope-overclaim* (a mild recurrence of the entry #1–#3 class, caught immediately).
  **Escalation signal (positive):** the gate did exactly its job on a headline-grade structural
  claim — an adversarial reviewer failed to break a true finding and found only side-defects; no
  ladder climb warranted.

### 4 — 2026-09-05 · Thesis document set, final gate (CYB-36) · **caught at gate**
- **What:** the whole 9-doc set's final reviewer gate — the **cleanest pass of the session**. The
  recurring *scope-overclaim about our own results* class (entries #1–#3) was **largely absent**: the
  CYB-33 "Hopf" and Fisher "small drift" traps were actively avoided, the class table matched the
  registry/modules, the descriptive/normative firewall held across all nine docs, every link resolved.
  One real catch — 02/07 asserted "the conserved ledger *is* the issuer's balance sheet," an
  **MMT-issuer attribution the shipped engine doesn't instantiate** (no currency-issuer sector; it's a
  private Godley–Lavoie circuit) — exactly what an MMT-literate skeptic would use to discount the rest.
  Plus a registry cross-reference lag (CYB-33 instances cited from the module README, not the frozen
  registry v0.1).
- **Check that caught it:** a fresh reviewer fact-checking every economics attribution against the
  engine source (`src/model.py`).
- **Outcome:** fixed before the PR. **Escalation signal (positive):** the overclaim-about-our-own-
  results class that recurred in #1–#3 did NOT recur this round — the earlier tightening (scope every
  claim; re-derive) appears to be catching it earlier. Keep watching; don't yet escalate the ladder.

### 3 — 2026-09-05 · Thesis flagship exhibit (CYB-36) · **caught at gate → DROPPED**
- **What:** the thesis set's flagship — a worked example meant to *show* our approach is "more
  informative than classical economics" — was built and reviewer-gated over two attempts, and
  **dropped**. (1) The originally-scoped smooth inflation→deflation time-series flip + a
  critical-slowing-down early-warning was caught **pre-build** as unsupported by the on-hand model
  (the Fisher dynamics are a violent bounded oscillation / abrupt collapse, not a slow ramp) —
  nothing was written. (2) The reshaped "structural-blindness" exhibit was built and green, but the
  gate ruled its strong claim **trivial/circular**: it re-illustrates the Lucas critique on a DGP we
  authored, mislabeled the CYB-30 bounded limit cycle as "deflation," and leaned on out-of-support
  regression extrapolation.
- **Where it had leaked:** the plan (KTD/U5) and my own status messages described a "more
  informative" *demonstration* before the gate ruled it out.
- **Why nearly missed:** the claim was exciting and the numbers were real; the flaw was in what the
  numbers *meant* (circular against an authored border), not in the code.
- **Check that caught it:** a fresh reviewer charged specifically to steelman the "just Lucas /
  regressions-don't-extrapolate / circular" reads and to re-derive the fit.
- **Outcome:** exhibit removed (`src/thesis_exhibit/` deleted); doc 04 reshaped to an honest
  *argument* (cites Lucas, owns the circularity); the real non-circular demonstration deferred to
  doc 08 (future work). Class = *scope-overclaim about our own results* (recurs — cf. entry #1); the
  reviewer now checks every "more/better than X" claim for circularity + triviality.

### 2 — 2026-09-05 · Goodwin–Keen v1 Hopf (CYB-35, PR #9) · **caught at gate**
- **What:** (M1) the *demonstrated* limit cycle was drawn on the economically **unphysical
  net-creditor branch** (ksharp=15.6 ⇒ `d*<0`), when a physical demo point (`d*>0`) existed just
  below threshold (ksharp≈17.3). (M2) the "Phillips-independent" claim was **overstated** — true of
  the Hopf's threshold *location* (φ′ cancels from `J₃₁`), but φ′>0 still sets the oscillation's
  existence and frequency. Plus three low: "three ways"→two independent objects, a stale taxonomy
  D1 row, a dead code idiom.
- **Where it had leaked:** README v1 section + `run_v1.py`/`model.py` docstrings + Fig 2.
- **Why nearly missed:** builder picked a demo `ksharp` without checking the equilibrium's `d*`
  sign; the "Phillips-independent" framing was clean and went unscoped. The *load-bearing* algebra
  (the `a₁a₂−a₃ = J₁₂·J₂₃·J₃₁` factorization) was, this time, correct.
- **Check that caught it:** a fresh reviewer that **re-derived the Routh–Hurwitz factorization
  symbolically** (sympy) and checked the demo equilibria for physicality (`d*` sign).
- **Outcome:** caught at the gate; fixed in `9ae7a1b` before merge. Class = *demo-on-an-unphysical-
  branch* + *scope-overclaim* (the latter recurs from entry #1 → reviewers now scope every
  "independent of X" claim). No false science: the headline (a genuine Neimark–Sacker Hopf,
  ksharp*=18.591 on flow and map) held under independent re-derivation.

### 1 — 2026-09-05 · Goodwin–Keen rung (CYB-33, PR #7) · **caught at gate**
- **What:** the stated *known answer* `Ω = √(A·C) = 0.3603` was wrong — the true value is
  **0.3602** (0.36021). The code always *printed* 0.3602; only the prose claim was off, which
  manufactured a phantom "measured-vs-known gap." Also: a dead `GKSystem` import, and a verdict
  that over-claimed the whole `src/chaos/` suite when only `linearize`+`lyapunov` were exercised.
- **Where it had leaked:** README + two module docstrings + the CYB-33 ticket + a prior status
  message — before the gate ran.
- **Why nearly missed:** builder-authored the "known answer" from memory instead of computing it;
  self-review re-read the same wrong number without recomputing √(A·C).
- **Check that caught it:** a fresh, independent reviewer that **re-derived the analytics** (not
  re-read the printed output) and checked every stated number against `run_v0.py` output.
- **Outcome:** caught at the gate; fixed in `676fc8d` before merge. Class = *stated-number-not-
  recomputed* + *scope-overclaim*. If this class recurs → escalate (make "recompute every cited
  constant independently" a standing reviewer check; it already is, as of this entry).

<!-- append new entries above this line; keep newest first within the numbered list -->
