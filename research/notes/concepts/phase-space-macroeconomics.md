---
id: concept-phase-space-macroeconomics
status: hypothesis
tags: [classification, dynamics, macroeconomics, regimes, slow-fast, bifurcation, method]
created: 2026-08-01
derived_from: conversations/2026/chaotic-economic-models/ ; Claude Code synthesis 2026-08-01
---

# Phase-Space Macroeconomics — an economy-state classifier

## North-star (one line)

Stop identifying *points* ("the equilibrium", "is r>g", "where is the Phillips curve") and start
identifying **regimes**: what dynamical class an economy is in, and how close it sits to a
transition.

## Purpose — a domain-of-validity / state-estimation layer (an *addition* to DSGE, not a replacement)

Economics lacks a shared **diagnostic layer**. Meteorology classifies weather systems before
forecasting rain; medicine diagnoses before treating; macro argues *treatment* with no shared
diagnosis. The classifier supplies it.

Framed defensibly (and crank-proof): the classifier's first job is to **certify the domain of
validity of equilibrium methods**. "Near-equilibrium, linearization safe" is *one* labelled
regime; elsewhere it flags multiple basins, hysteresis, finite-amplitude transitions, path
dependence — where DSGE's local assumptions break. This is exactly what the Hu bifurcation note
does one scale down ("the standard normal form applies *here* and provably *not there*"). The
classifier generalizes it: **map where standard methods hold vs. fail across the macro state
space.** So the Hu / CYB bifurcation-classification work is the mathematical *core*, not a side
quest.

Output = a **diagnosis, not a forecast**: regime label + distance-to-nearest-border + basin
membership + what moves it across. Illustrative / counterfactual, never point-predictive.

## Method — model-based indirection (the wind tunnel)

You **cannot** read a Lyapunov exponent / attractor off one short, non-stationary macro series
(cf. `../../../docs/empirical_grounding.md` — we do NOT claim chaos-detection in macro data). So:

1. **Mechanistic substrate** — a conserved, stock-flow-consistent coupled system (Marx
   accumulation + Minsky finance + MMT operations as ONE SFC system). Its regime boundaries are
   **real economic constraints** — the *switching-manifold through-line* (order non-negativity →
   wage floor → solvency ceiling → capitalized-interest tipping). Classification = locating the
   economy relative to its *active constraints*.
2. **Classify with the validated instruments** — `src/chaos/` (Lyapunov, bifurcation sweep,
   linearization, border-collision classifier), each self-tested on a closed-form case first.
   Classes get *falsifiable signatures*.
3. **Data as calibration + referee, never as the trajectory** — real series (FRED, NASS,
   Piketty/WID) calibrate the mechanism and validate **out-of-sample** (as the 2024-25 egg
   episode did).
4. **Diagnosis output** — regime + distance-to-border + basin + what crosses it.

## The core problem, and the fix: non-stationarity IS the slow variable

Accepted regime narratives ("1929", "postwar boom", "Weimar") are **not measurements** — they are
stories (window + causal plot + salient events). Treating them as ground truth is the
"beautiful lie" one level up. The fix:

- **Don't classify the narrative; measure the transition.** Model-free signatures exist:
  **critical slowing down** (rising AC(1) + variance, flickering before a basin crossing — Scheffer
  et al.), **bounded vs. escape**, **which constraint went active**. The narrative becomes a
  *hypothesis under test*, not the thing fit.
- **Slow–fast decomposition.** Fast variables (inflation, output, spreads) live on a basin whose
  shape is set by slowly-drifting structural variables (leverage, wealth concentration,
  institutions). Minsky *is* this. So **non-stationarity = the slow variable, and it is
  measurable** — not noise to remove.
- **Piketty/WID is the slow manifold** — a century-long, cross-country measurement of the
  distributional slow variables; the background parameter that walks the fast system across
  bifurcation borders.

## Piketty's datasets — the distributional out-of-sample bank

Steal GPT's reframed question verbatim: **"Can Piketty's historical dataset distinguish among
different classes of nonlinear macroeconomic dynamics?"** WID's cross-country panel = multiple
independent realizations of "the same" regime → the reproducibility test: a *real* dynamical
class's signature reproduces across countries; a *narrative* won't. `r` and `g` become
**state-dependent observables**, not drivers — `r>g` demoted from law to a projection that holds
in one basin (the same move already made on the Phillips curve). See
[natural-experiment-portfolio](natural-experiment-portfolio.md).

## Honest limits

- **Identifiability** ([taxonomy](taxonomy.md)'s open issue): the same series fits multiple
  mechanisms; classes must separate math behavior / measurement artifact / historical narrative.
- **Small N**: few instances per event type; early-warning indicators are noisy (false positives).
- **Data comparability** across a century + countries ([Piketty](../people/piketty.md)'s caveat).
- **High-D nonsmooth classification is an open math frontier** — the coupled system is exactly the
  "no sanctioned reduction" wall in the Hu note; the classifier's rigor is *gated on the same
  mathematics*.
- **Circularity is the killer**: pre-register signatures, test out-of-sample on withheld
  countries/episodes.

## Related

[Taxonomy](taxonomy.md) · [Hyperinflation](hyperinflation.md) · [Inflation](inflation.md) ·
[Piketty](../people/piketty.md) · [Natural-experiment portfolio](natural-experiment-portfolio.md) ·
[Open questions](../../indexes/questions.md). Math core: the bifurcation-classification work (Hu
outreach, `docs/outreach/`, CYB-25) + the switching-manifold through-line (`docs/../THESIS.md`).

## Provenance

Derived from the GPT conversation (`../../conversations/2026/chaotic-economic-models/` — the DSGE /
phase-space / Piketty threads) and a Claude Code synthesis, 2026-08-01. A framing to attack, not
an established result.
