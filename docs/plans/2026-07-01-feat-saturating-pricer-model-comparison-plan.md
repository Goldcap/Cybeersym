---
title: "feat: Saturating (concave) egg pricer — linear-vs-concave model comparison, OOS-on-path-shape"
type: feat
status: done
date: 2026-07-01
tracking: CYB-14
canonical_source: "Linear CYB-14 (https://linear.app/techno87/issue/CYB-14)"
depends_on: [CYB-7, CYB-9]
---

# feat: Saturating egg pricer — a model-selection question, not "add a term"

> **Canonical spec lives in Linear (CYB-14).** Mirror into version control. Outcome at bottom.

## Goal

Determine whether the egg pricer's deficit→price mapping has **real, generalizing
curvature**, or whether the mild concavity CYB-9 surfaced at the two peaks is
within-noise. Framed as **linear-vs-concave model comparison on OOS path error — NOT
"add a saturation term."** Either answer is a finding.

## The methodological fork

Two HPAI episodes + a 2-parameter concave fit = zero out-of-sample episode (fits both
peaks, breaks the OOS discipline). Escape it two ways together:
1. Validate on the **full monthly path** (dozens of `(d_t, price_t)` pairs), not the peaks.
2. **Model comparison, not a fit:** calibrate linear AND concave on ep1's full path,
   freeze, validate OOS on ep2's full path. Concave earns its extra parameter only if it
   beats linear OOS.

## Acceptance criteria

1. Fit both forms on ep1's full path (linear `slope·d`; ≥1 concave form).
2. OOS on ep2's full path — RMSE + peak, split stated. The decisive metric.
3. Honest verdict either way (concave beats → adopt; else keep linear, don't carry an
   unearned 2nd parameter).
4. Conservation intact (pricer analysis only).
5. Honesty firewall (model-selection framing; narrow claim; link CYB-3/7/9).
6. Determinism.

---

## Outcome (shipped)

Delivered `src/v11_saturation.py` (comparison harness + figure) and the concave pricer
forms `power_deficit` (`slope·d^α`, nests linear at α=1) and `saturating_deficit`
(`A(1−e^{−k·d})`, robustness) in `pricers.py`. **Verdict: concavity NOT supported → keep
the linear pricer.** All six criteria met.

- **OOS path RMSE (calibrate ep1 / validate ep2):** linear **0.425**, power **0.423**,
  saturating **0.436**.
- The power form's best exponent lands at **α ≈ 1.03 — not in the concave region at all**
  (marginally convex, indistinguishable from linear); its OOS tie with linear is ~0.3%
  (grid noise). The dedicated **forced-concave** saturating form is strictly **worse**.
- **The peak-level concavity does not generalize to the path** — it lives only between the
  two peaks; on the full monthly path it's swamped by the shoulder months (a concave curve
  overshoots low-deficit prices), so the data prefers α=1 (linear). Within-noise → **keep
  the linear pricer; don't carry an unearned second parameter.** `EGG_PRICING` unchanged.
- **2015 HPAI (bonus):** not available — the NASS layer series (`data/nass_layers`) starts
  2020, so the 2015 real deficit can't be computed without a separate pull. Noted, not gated.
- Conservation leak `2e-10` (substrate untouched); deterministic.

Note: v11 uses a **path-RMSE** linear calibration (slope≈17.8) *internally* for the fair
form comparison; the committed `EGG_PRICING["slope"]=24.1` (CYB-9's **peak** calibration)
is a different, intentional target and is left unchanged.

Learning: [`../solutions/saturation-tested-concavity-doesnt-generalize-keep-linear.md`](../solutions/saturation-tested-concavity-doesnt-generalize-keep-linear.md).
