---
id: concept-parameterization-and-control-structure
status: hypothesis
tags: [parameterization, control-structure, dynamics, slow-fast, reflexivity, classifier, method, design]
created: 2026-08-02
derived_from: Claude Code session 2026-08-02 (Andy + Claude brainstorm; extends concept-phase-space-macroeconomics)
promoted_to: [CYB-26, CYB-27, CYB-28, CYB-29]
---

# Parameterizing the economy-state classifier — the four-layer control structure

The design frame under the classifier ([phase-space-macroeconomics](phase-space-macroeconomics.md)):
**how do you parameterize an economic system without drowning in its vastness?** Answer:
you don't parameterize "the economy." You find the low-dimensional **control structure** —
the handful of objects whose values organize the *qualitative* behavior — and everything
else is detail that doesn't move the phase portrait. Same move as the egg (one pricing
slope) and the CYB-2 chaos map (one knob, β).

**Promoted 2026-08-02** to four separated-but-coupled tickets: **CYB-26** (axes) ·
**CYB-27** (parameters) · **CYB-28** (endogenous slow variables) · **CYB-29** (thresholds).
Natural order **26 → 27 → {28, 29}**; separated as *work*, coupled as *design*.

## The four layers

1. **State variables — the axes** (CYB-26). The *fast* things that move moment-to-moment
   (inflation, output, spreads, inventories). These are the coordinates of the phase space;
   you don't parameterize them, they're what *moves*. Choosing the axis set is open by
   design — the brainstorm layer.
2. **Parameters — the vector field** (CYB-27). The *constants* that set the shape of the
   landscape (markup slope, adjustment speeds, propensities, leverage ceiling). Turn one →
   the phase portrait deforms. A distinguished few are **control (bifurcation) parameters** —
   the β-analogue whose sweep reorganizes everything.
3. **Slow variables — endogenous outcomes** (CYB-28). Parameters that *drift* so slowly the
   fast system treats them as fixed (wealth concentration, leverage, β). **This is Piketty.**
4. **Thresholds — switching manifolds** (CYB-29). The regime *borders*: real constraints
   going active (order non-negativity → wage floor → solvency ceiling → capitalized-interest
   tipping). A regime transition = a manifold crossing.

## The load-bearing insight: slow variables are *almost outcomes* (Andy)

The tidy story treats layer 3 as exogenous dials that happen to drift. That's wrong. Wealth
concentration, leverage, β are **produced by the system's own accumulation** and then feed
*back* as parameters reshaping the fast landscape. `r > g` is not a law imposed from outside;
it's an *outcome* of how returns and growth interact, and that outcome becomes an *input*.

So layers 2 and 3 are **the same substance on two different clocks.** Freeze the slow clock
and β is a fixed dial (a parameter); run the slow clock and β is a state variable with a
feedback loop. That thawing-of-the-freeze **is the reflexivity** that makes macro
history-dependent — hysteresis, path dependence, Minsky fragility as accumulated-outcome
turned regime-parameter. It is the hardest and most novel layer (CYB-28), kin to
[CYB-20 reflexivity] and the Minsky work (CYB-17/CYB-19).

## Three principles that tell you *which* numbers matter

1. **Parameterize mechanisms, not aggregates.** Parameters are behavioral rules ("how a firm
   raises price under scarcity", "how much a household cuts per point of debt"); the macro
   aggregates *emerge*. Fitting hand-drawn macro shapes was always "a beautiful lie".
2. **Follow the constraints to find the knobs.** The switching manifolds (CYB-29) tell you
   which parameters matter — the ones that move the system relative to an *active* constraint.
   Don't guess; follow the seams.
3. **Separate timescales.** Freeze the slow variable → understand the fast phase portrait →
   let the slow variable drift → watch the portrait deform across a border. Non-stationarity
   stops being noise and becomes the mechanism.

## The entry rung — Goodwin–Keen as instrument self-test (not the model)

Smallest nonlinear macro system with real dynamics: **Goodwin** (2 vars: employment × wage
share → a limit cycle) → **Keen's Minsky extension** (+ debt → can tip to breakdown; that tip
is a bifurcation). It is **not the destination** — the real target is the coupled SFC
substrate. Its role is the **instrument self-test rung**: prove the classifier machinery
detects a bifurcation it already knows is there, exactly as the CYB-2 instruments self-test
on the logistic map's λ=ln2 before being trusted on the 21-D system. Pass G–K → then aim at
the full substrate.

## Honest status

A design frame to attack, not a result. The four tickets are **design-first seeds** — the
deliverable of each is a defensible definition + candidate set + selection criteria, not yet
a running model. Building the thing that *consumes* all four (the slow–fast substrate, with
its thin WID numpy loader) is downstream of CYB-28.

## Related

[Phase-Space Macroeconomics](phase-space-macroeconomics.md) ·
[Natural-experiment portfolio](natural-experiment-portfolio.md) ·
[WID data](../../data/wid/INVENTORY.md) · [Taxonomy](taxonomy.md) ·
[Hyperinflation](hyperinflation.md) · [Piketty](../people/piketty.md) ·
[Open questions](../../indexes/questions.md).
Promoted: CYB-26 · CYB-27 · CYB-28 · CYB-29.
