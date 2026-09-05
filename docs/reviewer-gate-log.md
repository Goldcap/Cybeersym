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
