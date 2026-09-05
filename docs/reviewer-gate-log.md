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
