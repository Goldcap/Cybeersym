---
title: "The egg pricer's peak-level concavity does NOT generalize: a linear-vs-concave OOS model comparison on the full path picks linear — a nested 2-param model whose free curvature collapses to α≈1 is the cleanest way to decline a parameter"
category: modeling
tags: [model-selection, out-of-sample, overfitting, saturation, concavity, egg-pricer, nested-model, path-vs-peaks, parsimony, honesty-firewall, method]
created: 2026-07-01
updated: 2026-07-01
severity: medium
component: src/pricers.py
problem_type: model_selection
root_cause: two-point_feature_did_not_generalize
tracking: CYB-14
---

# The egg pricer's concavity doesn't generalize: test it as a model comparison, then decline the parameter

CYB-9 found the linear egg pricer overshoots ep2 out-of-sample and that the per-point
price/deficit slope falls with depth (24.7 %/pt at ep1's 7.6% deficit → 22.5 %/pt at
ep2's 12.1%) — mild concavity **at the two peaks**. CYB-14 asked the disciplined
question: is that curvature *real and generalizing*, or a two-point artifact? Answer:
it does not generalize — **keep the linear pricer.**

## The trap, and the escape

Two HPAI episodes and a 2-parameter concave curve = fits both peaks with **zero
out-of-sample episode left**. Fitting the two peaks and declaring "saturation confirmed"
would be textbook overfitting. Two moves together escape it:

1. **Validate on the full monthly path, not the peaks.** The pricer is evaluated every
   month, so each episode is *dozens* of `(deficit, price)` points — enough degrees of
   freedom for an honest OOS test of a 2-parameter curve.
2. **Frame it as a model comparison, not a fit.** Calibrate BOTH a linear and a concave
   pricer on ep1's full path, freeze, validate OOS on ep2's full path. The concave form
   earns its extra parameter **only if it beats linear out-of-sample.**

## The result — concavity is a two-peak artifact

OOS path RMSE (calibrate ep1 / validate ep2): **linear 0.425, power 0.423, saturating
0.436.** Two things make the verdict unambiguous:

- The **nested power form** `markup = slope·d^α` (α=1 IS linear) was given free rein and
  its best exponent landed at **α ≈ 1.03 — not concave at all** (marginally convex). When
  a 2-parameter model that *contains* the 1-parameter model puts its extra parameter at
  the no-op value, the data is telling you it doesn't want the parameter. Its ~0.3% OOS
  edge is grid noise.
- The **forced-concave** saturating form `A(1−e^{−k·d})` (which *must* bend the intended
  way) is strictly **worse** OOS.

Why the peak-level concavity vanishes on the path: it lives only *between the two peaks*.
On the full monthly path it's swamped by the shoulder months — a concave curve
(`d^α`, α<1, gives `d^α > d` for `d<1`) *overshoots* the many low-deficit months. The two
peaks hinted a bend; the cloud of all months does not support it.

## Takeaways (how to apply)

1. **A feature seen at 2 points is a hypothesis, not a finding — test it where it has to
   generalize.** The peak-level concavity was real *at the peaks* and still failed to
   generalize. Resist reading structure into the extremes of a small sample.
2. **Use a NESTED model to decline a parameter cleanly.** Let the richer model contain the
   simpler one (`α=1` recovers linear) and fit the extra parameter freely; if it drifts to
   the no-op value, that *is* the model-selection verdict — cleaner than an AIC/BIC
   argument and impossible to hand-wave.
3. **Also run a forced-direction form as a check.** The nested form can tie by going the
   wrong way (here α>1); a form that *must* bend concave (the exponential) failing OOS
   confirms the direction, not just the magnitude.
4. **The parsimonious answer is a real result, not a null.** "The data supports 1 parameter,
   not 2" is publishable and protects the model's credibility. Carrying an unearned second
   parameter is the actual failure mode.
5. **Distinguish calibration TARGETS.** CYB-9 calibrated the committed slope on the ep1
   *peak* (the headline magnitude); CYB-14 calibrates on the ep1 *path* for a fair form
   comparison. Different legitimate targets — don't silently overwrite one with the other
   (`EGG_PRICING` stays on CYB-9's peak calibration).

## References
- Code: `src/v11_saturation.py` (linear-vs-concave OOS comparison + figure);
  `src/pricers.py` (`power_deficit`, `saturating_deficit` — the comparison forms, NOT
  adopted; `RESOLVED(saturation)` note). Real deficit: `data/nass_layers.py`; price: `data/eggs_fred.py`.
- Plan: [`../plans/2026-07-01-feat-saturating-pricer-model-comparison-plan.md`](../plans/2026-07-01-feat-saturating-pricer-model-comparison-plan.md).
- Direct predecessors: [[replace-lag-retired-timing-was-in-the-flock-data]] (CYB-7),
  [[egg-pricer-slope-recalibrated-single-slope-overshoots-oos]] (CYB-9, which surfaced the
  peak concavity and correctly declined to bolt on a term in-place).
