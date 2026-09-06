# CYB-38 — scoping the WID evaluation (the post-lock, model-first-then-correlate test)

> **Status: scoping (not the evaluation).** This document plans *how* to execute the LOCKED
> pre-registration `docs/preregistrations/2026-09-05-classifier-vs-wid.md` (locked in commit
> **`6338f3a`** on `main`). It **references** the lock; it **may not alter** anything above the
> lock line. Two design decisions in §4–§5 need Andy's sign-off, and one model-side prerequisite
> (§3) must be executed *blind to WID* before any evaluation. Nothing here touches the WID×outcome
> join — that is Phase C, and it stays sealed until the Phase-A pre-analysis plan is itself committed.

## 0. The one-sentence job

Take the **frozen** model (egg-validated params + the Fisher α_p border) and ask, without fitting:
does the model's **regime-border structure** track independent distributional data (WID) against an
**independent** crisis chronology — or does it not (a reportable null, like the egg magnitude
overshooting OOS)?

## 1. Frozen inputs (from the lock — restated, not re-decided)

- **Slow variable:** WID wealth concentration (top-10% / top-1% wealth share; β = wealth/income
  secondary), normalized vs a per-country *reference* baseline, never vs the outcome.
- **Border:** the Fisher markup-defense **α_p** tipping value from the model's own sweep
  (`src/fisher/`) — the **graded** tipping value, **not** the degenerate α_p→0 corner.
- **Model params:** the mechanism/egg-validated repo values, frozen.
- **Mapping:** preferentially **zero-fit ordinal**; at most **one** constant, calibrate-freeze-OOS.
- **Decision rule:** 2×2 contingency (above/below border × fragile/stable) + Spearman ρ on
  distance-to-border vs fragility; **test, margin, sign, min |ρ| fixed before data**.
- **Outcome labels:** an **independent external crisis chronology** (third leg; not WID, not model).
- **Forbidden:** fit the mapping; pick the threshold post-hoc; re-tune after seeing the withheld
  set; relabel "fragile"; swap the slow variable or metric after a null.

## 2. What already exists (build on it, don't re-derive)

- **WID data — staged and self-checked.** `research/data/wid/` holds all-country WID with an
  `INVENTORY.md` over **16 test countries** (US, FR, DE, JP, GB, SE, FI, NO, TH, ID, KR, MY, AR,
  VE, ZW, CN), coverage documented, instrument self-checked against published facts (US top-1%
  income 2024 = 20.7% ✓). Honest windows flagged: income shares dense ~1913+, **wealth** shares a
  hard **1980 wall** for FI/MY/VE/ZW. Deep-past developing-country shares are WID *imputation* —
  illustrative, not fitted.
- **The reproducibility banks** (`research/notes/concepts/natural-experiment-portfolio.md`) — the
  natural country-era clusters, and the inventory confirms WID covers each in its crisis window:
  - **Nordic banking crises, early 1990s** — SE, FI, NO
  - **Asian financial crisis, 1997** — TH, ID, KR, MY
  - **Latin American hyperinflations, 1980s–90s** — AR (+ others outside the WID-16)
  - plus isolated regime-eggs (VE 2016–19, ZW 2008, JP 1990, US/GB 2008).
- **The Fisher sweep** (`src/fisher/run_v0.py`) — the (α_p, φ) genuine-divergence map. **Grid:**
  `alpha_ps = linspace(0, 0.30, 13)` (step 0.025), `phis = linspace(0, 8, 17)`. Finding: genuine
  divergence occurs **only at α_p = 0.0**; α_p ≥ 0.025 is a bounded limit cycle at every φ.

## 3. PREREQUISITE (model-side, blind to WID) — locate the graded border

> **RESOLVED (2026-09-05, reviewer-gated): NO graded border exists on the shipped Fisher α_p axis.**
> `src/fisher/run_v1.py` fine-resolved the interval `run_v0` stepped over and found the deflation
> border is a **hard corner at exactly α_p=0** (n-stable to 100k under independent review), with the
> bounded regime a **smooth monotone gradient** (no fixed-point/Hopf onset, no interior tip;
> φ-flat; conservation ~1e-15). So the only "border" is the degenerate α_p→0 corner the lock
> **excluded**, and the bounded gradient *is* the smooth null the Option-A shape test must beat.
> **⇒ the WID test cannot be instantiated on this axis as pre-registered** — a reportable
> prerequisite result. Per the lock's forbidden moves we do **not** swap the slow variable or
> redefine the border. **Decision pending (Andy):** (1) report the null-of-feasibility and close the
> CYB-38 line, or (2) open a *new* pre-registration asking whether a graded border lives elsewhere in
> the stack (coupled/recursion — the CYB-22 territory `run_v0`/`run_v1` flag as the prime suspect).

**The border the lock commits to does not yet exist at usable resolution.** The current sweep has
one grid point below 0.025 (namely 0.0), so it resolves a **corner at α_p→0** and a **wall at
α_p ≥ 0.025** — but *not* a graded tipping value in between. Two things must happen first, and both
are **pure model computation, blind to WID** (blind-safe — no outcome data touched):

1. **Fine α_p sweep in (0, 0.025]** (e.g. `linspace(0, 0.025, N)` at fixed representative φ, plus a
   2-D refinement), classifying **not just divergence** (−1/0/+1) but the **qualitative character**
   of the bounded regime (limit-cycle amplitude / period, or a Neimark–Sacker–type onset). The
   "graded border" is the α_p where the regime *character* changes, even if outright divergence
   stays pinned at 0.
2. **Feasibility verdict.** If a genuine interior graded tipping α_p exists → that is the border,
   `distance-to-border = |effective α_p − α_p*|`. **If the transition is a true hard corner at
   α_p=0 with no interior structure** → the lock's committed border is *unsatisfiable as written*;
   that is itself a **reportable finding** (we do not move the goalposts — we report that the
   graded-border test cannot be instantiated on the shipped model and say why).

Output: `src/fisher/` fine-sweep script + figure + a one-paragraph verdict. This is a normal
`src/**` change → it will be the **first PR the code-review app actually reviews.**

## 4. DECISION 1 (load-bearing) — how the border becomes testable without triviality or fitting

> **RESOLVED (2026-09-05): Option A — the shape/threshold test.** The primary test is
> threshold-beats-smooth-monotone OOS; the smooth "inequality → crises" relation is the *null we
> must beat*. Zero-fit, no WID↔α_p scale, egg-CYB-14 discipline (defended by rejection).

The knot: the border lives in **α_p units**; WID lives in **concentration units**. To place the
border on the data you must relate them — and the lock forbids fitting *and* disavows the trivial
"more inequality → more crises." Candidate resolutions (Andy picks; I recommend **A**):

- **A — Shape/threshold test (CHOSEN; egg-CYB-14–consistent).** The model's *distinctive*
  claim is a **regime change** (a step) in concentration→fragility, not a smooth gradient. Test
  whether a **threshold** model beats a **smooth-monotone** model out-of-sample. The smooth
  "inequality correlates with crises" relation is the **null we must beat** — the model earns its
  keep only if there is a *step*. Directly mirrors CYB-14 (linear-vs-concave, defended by
  rejection). No WID→α_p scale needed; the border is *qualitative* (step exists / doesn't).
- **B — One-constant ordinal placement.** Calibrate a single WID↔α_p scale on **one** declared
  training bank (e.g. Nordic), freeze it, place the border, validate OOS on the withheld banks
  (Asian, LatAm). Egg-slope discipline (calibrate-freeze-OOS-report). Costs one parameter.
- **C — Pure rank correlation only.** Spearman(concentration-rank, fragility-rank). **Rejected as
  primary** — this *is* the trivial test the lock disavows; keep only as a context statistic.

## 5. DECISION 2 — the independent crisis chronology (the third leg)

> **RESOLVED (2026-09-05): Laeven–Valencia, IMF Systemic Banking Crises Database.** The named,
> fixed chronology source. Exact country-era rows get pinned in the Phase-A analysis lock.

Must be **named and fixed before data** (the load-bearing anti-circularity guard). Candidates
(recommend **Laeven–Valencia**):

- **Laeven–Valencia, IMF Systemic Banking Crises Database (recommended).** Standard, well-documented,
  covers 1970–2017, includes every reproducibility bank (Nordic '91–'93, Asian '97, LatAm). Clean
  start-year dating.
- **Reinhart–Rogoff** banking/debt-crisis chronology — deeper history, the pre-reg's named example;
  messier dating, weaker post-1970 for some countries.
- **Baron–Verner–Xiong** bank-equity-crash dates — market-based, narrower.

## 6. Staged plan (each stage gated; the join stays sealed until Phase A is committed)

- **Phase A — Pre-analysis plan (blind, committed before any WID×outcome join).** With §3's border
  in hand and §4/§5 decided, pin the *exact numbers the lock deferred*: the border α_p* value; the
  chronology source + the exact country-era list and windows (dense-window rule from INVENTORY); the
  training/withheld split by the coverage rule; the exact statistical test + margin + ρ sign +
  min |ρ|. Commit — this is the **second lock** (analysis lock), referencing `6338f3a`. Still no
  outcome join.
- **Phase B — Data assembly (numpy only).** Thin `load_series(iso, var, pct) -> (years, values)`
  loader over `research/data/wid/extracted/`; normalize each series vs its per-country reference
  baseline; assemble the chronology table. Outcome labels kept in a **separate module**, not joined
  to the border computation.
- **Phase C — Frozen evaluation (the sealed join).** Compute per-era distance-to-border and the §4
  test against the §5 outcomes on the **withheld** set. Run once. No re-tuning.
- **Phase D — Reviewer gate + honest report.** Fresh independent reviewer (builder≠reviewer,
  CYB-34): re-run for determinism, re-derive every stated number, attack the headline, confirm the
  join was sealed until Phase A. Write the results doc (`docs/`), **report a null as a finding.**

## 7. Deliverables

- `src/fisher/` fine-sweep script + figure + border verdict (§3).
- `src/classifier/` (or `src/wid_test/`): loader, normalizer, border-distance, the §4 test, figures
  — numpy + matplotlib only, deterministic (σ=0), one script per stage.
- Phase-A pre-analysis plan (committed, referencing `6338f3a`) and the Phase-D results doc.
- A reviewer-gate-log entry.

## 8. Honest caveats (pre-stated, inherited from the lock)

- **Small-N.** Few clean country-eras; pre-registration is the only defence against fooling
  ourselves — hence the two-stage lock (design lock `6338f3a` → analysis lock in Phase A).
- **The mapping is the bet.** If distributional slow variables are not the ones that move the
  border, the probe fails honestly — itself the CYB-28 finding.
- **WID comparability** across a century + 16 countries (Piketty's own caveat); gate every test on
  the *dense* window, never the nominal span (INVENTORY finding #3–#4).
- **Scope:** a domain-of-validity check of a frozen model against independent data — **not** a
  forecast-superiority claim (that bar is still doc 08).

## Related
Lock: `docs/preregistrations/2026-09-05-classifier-vs-wid.md` (`6338f3a`) ·
`research/data/wid/INVENTORY.md` · `research/notes/concepts/natural-experiment-portfolio.md` ·
`src/fisher/` · thesis doc 08 (future-work roadmap) · CYB-28 / Q-2026-005.
