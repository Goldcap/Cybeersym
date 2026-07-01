---
title: "Recalibrating the egg pricer slope on real deficits (13→24): a compensating-error pair split into two correct values, and a single linear slope calibrated on ep1 OVERSHOOTS ep2 out-of-sample — the saturation, finally measured not fudged"
category: modeling
tags: [calibration, out-of-sample, real-data, egg-pricer, slope, saturation, concavity, compensating-error, honesty-firewall, single-parameter, method]
created: 2026-07-01
updated: 2026-07-01
severity: medium
component: src/pricers.py
problem_type: calibration_assumption
root_cause: parameter_calibrated_against_wrong-scale_input
tracking: CYB-9
---

# Recalibrating the egg pricer slope on real deficits: two correct values replace a compensating-error pair, and the OOS overshoot finally measures the saturation

CYB-9 is the second half of CYB-7, deliberately split so the `replace_lag` retirement stayed
honest. CYB-7 replaced the ~2×-too-large synthetic flock deficit with the real NASS deficit;
with the frozen slope (~13) the model then undershot. CYB-9 recalibrates the ONE parameter —
the egg pricer's price-per-deficit slope — against the real deficit, out-of-sample.

## The compensating-error pair (why 13 was "right" for the wrong reasons)

The old slope ~13 was calibrated against the synthetic cull-reconstruction deficit, which was
~2× too large. Too-big deficit × too-small slope ≈ the right price — a **compensating-error
pair**. It validated, but on two errors that cancelled. CYB-7 fixed the deficit (real, ~half);
CYB-9 fixes the slope (~24.1). **Two independently-correct values replace a pair that only
looked right multiplied together.** The recalibrated slope (24.1, from numerically calibrating
the model on ep1) independently lands on the ~24 %/pt CYB-7 estimated from the raw
deficit-price ratio — a satisfying cross-check.

## The finding: a single linear slope calibrated on ep1 OVERSHOOTS ep2 (OOS)

Calibrate the slope on ep1 (2022-23) → freeze → validate on ep2 (2024-25):
- ep1 (in-sample): **+188%**, by construction.
- ep2 (**out-of-sample**): model **+316% vs real +272%** — overshoots by ~16pp of the rise.

The real per-point slope falls with depth: **24.7 %/pt** at ep1's 7.6% deficit, **22.5 %/pt**
at ep2's 12.1% deficit. So a single *linear* slope fit on the shallow episode overshoots the
deep one. This is mild **concavity/saturation** — at extreme scarcity the price response
flattens (demand destruction at $6+ eggs; the Jan–Mar 2025 egg-import surge, +2,040% YoY). The
`pricers.py TODO(saturation)` predicted exactly this; CYB-7's real deficit now pins both
episodes down, so the concavity is **measured, not within-noise**.

**We did not fix it.** CYB-9's whole point (as a split from CYB-7) was to move ONE parameter and
report what breaks. Adding a saturation exponent `alpha` to absorb the ep2 overshoot would have
recreated the multi-parameter fit the split existed to avoid. The overshoot is reported; a
saturating pricer (`slope·deficit**alpha` or `A(1−e^{−k·deficit})`) is filed as its own thread.

## Takeaways (how to apply)

1. **A parameter is only meaningful relative to the scale of its input.** The slope wasn't
   "wrong" at 13 — it was calibrated against a 2×-inflated deficit. When you fix an input's
   scale, every parameter calibrated against it must be re-derived, or a compensating error hides.
2. **Calibrate on one episode, validate on the other — even for a single parameter.** The OOS
   overshoot is the entire value here: it turned "the model fits" into "the model fits ep1 and
   reveals a real concavity on ep2." Fitting both episodes would have recovered a nicer number
   and learned nothing.
3. **When you retire/repair one number, freeze everything else and report the residual.** The
   residual (here, the ep2 overshoot) is often a genuine finding — it *measured* the saturation
   that was previously dismissable as within-noise. Don't let a second parameter silently eat it.
4. **Preserve superseded artifacts by pinning, not deleting.** Changing the `EGG_PRICING` default
   would have silently broken the pre-CYB-7 historical scripts (`v05`–`v08`) that used the
   synthetic path; pinning them to `slope=13` keeps their frozen figures reproducible without
   re-tuning anything live.

## References
- Code: `src/v10_pricer_recal.py` (calibrate-on-ep1 / validate-on-ep2 + figure);
  `src/pricers.py` (`EGG_PRICING["slope"]=24.1`, empirical-basis + `TODO(saturation)` notes);
  pinned historical scripts `src/v05_seasonal_fit.py`, `v06_oos_test.py`, `v07_pricer_fix.py`,
  `v08_wedge.py`.
- Real deficit: `src/data/nass_layers.py` (CYB-7). Price: `data/eggs_fred.py` (FRED APU0000708111).
- Plan: [`../plans/2026-07-01-feat-recalibrate-egg-pricer-slope-real-deficits-plan.md`](../plans/2026-07-01-feat-recalibrate-egg-pricer-slope-real-deficits-plan.md).
- Direct predecessor (the deficit fix + epistemic shift): [`replace-lag-retired-timing-was-in-the-flock-data.md`](replace-lag-retired-timing-was-in-the-flock-data.md).
