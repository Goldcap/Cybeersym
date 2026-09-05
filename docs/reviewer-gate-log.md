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

### 2 — 2026-09-05 · Thesis flagship exhibit (CYB-36) · **caught at gate → DROPPED**
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
- **NB** numbering reconciles at merge (the `goodwin-keen-v1-hopf` branch carries its own entry #2).

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
