---
title: "feat: Recalibrate the egg pricer slope against real deficits (~24%/pt) — OOS-validated"
type: feat
status: done
date: 2026-07-01
tracking: CYB-9
canonical_source: "Linear CYB-9 (https://linear.app/techno87/issue/CYB-9)"
depends_on: [CYB-7]
---

# feat: Recalibrate the egg pricer slope against real deficits — OOS-validated

> **Canonical spec lives in Linear (CYB-9).** Mirror into version control; spec changes
> happen in Linear first. Shipped outcome at the bottom.

## Goal

The second half of CYB-7, split out to keep the `replace_lag` retirement honest
(recalibrating in place would have let the slope silently absorb the deficit correction).
CYB-7 halved the deficit (synthetic → real); the frozen v0.6 slope (~13, calibrated off the
too-large synthetic deficit) then undershot. Recalibrate the ONE parameter — the egg
pricer's price-per-deficit slope — against the real deficit, and re-validate out-of-sample.

## Acceptance criteria

1. Recalibrate **only** the pricer slope, against real NASS-driven deficits. No other
   parameter moves; no new free parameters.
2. **OOS discipline (load-bearing):** calibrate the slope on **one** episode (ep1, 2022-23),
   freeze, validate **out-of-sample** on the other (ep2, 2024-25). State the split. Do NOT
   fit both episodes.
3. Report timing + magnitude both episodes.
4. Conservation intact (substrate untouched).
5. Honesty firewall: single-parameter calibration against measured data, narrow claim
   (mechanism reproduces episodes with real ingredients; not price prediction). Link CYB-3, CYB-7.

## Deliverables

Recalibrated pricer slope; OOS calibrate-on-one/validate-on-other with the split stated,
timing + magnitude both episodes; figure (real vs modeled, both episodes); doc.

---

## Outcome (shipped)

Delivered `src/v10_pricer_recal.py` (calibrate/validate + figure) and updated
`src/pricers.py` (`EGG_PRICING["slope"] 13 → 24.1`, empirical-basis + saturation notes).
All five criteria met.

1. **Only the slope moved.** `EGG_PRICING["slope"] = 24.1`, calibrated on ep1 by bisection to
   the real ep1 peak. `hi` and every other parameter unchanged; timing is data-driven (CYB-7).
2. **OOS discipline honored.** Calibrate on ep1 (2022-23) → freeze → validate on ep2 (2024-25),
   in one continuous run. Split stated explicitly in the script + figure.
3. **Timing + magnitude:**
   - Timing clean (both peaks land 2023-01, 2025-03 — data-driven).
   - ep1 (in-sample): **+188%** by construction (matches real).
   - ep2 (**out-of-sample**): model **+316% vs real +272%** — **overshoots** by ~16pp of the
     rise. The single linear slope calibrated on the shallow ep1 deficit overshoots the deeper
     ep2 deficit (real per-point slope 24.7%/pt at ep1's 7.6% → 22.5%/pt at ep2's 12.1%). This
     is the mild **saturation/concavity** the pricer's `TODO(saturation)` predicted, now
     **measured against real data** rather than within-noise. **Not fixed here** — CYB-9 fit
     one parameter and reported the overshoot rather than adding `alpha` to absorb it.
4. **Conservation** leak ~2e-10 (substrate untouched).
5. **Honesty firewall:** documented as a single measured-parameter calibration; narrow claim kept.

Also **pinned the pre-CYB-7 historical scripts** (`v05`–`v08`) to `slope=13` explicitly, so
their frozen figures still reproduce after the `EGG_PRICING` default changed (preserving the
arc; not re-tuning). The old {synthetic deficit × slope 13} was a compensating-error pair;
{real deficit × slope 24} is two independently-correct values.

Learning: [`../solutions/egg-pricer-slope-recalibrated-single-slope-overshoots-oos.md`](../solutions/egg-pricer-slope-recalibrated-single-slope-overshoots-oos.md).
