---
title: "CYB-6's 'unbounded' runaway was the full-accommodation limit hiding as a law; and once you finance the wage bill the policy rate is a three-channel tug-of-war (cost feeds, demand cools symmetrically, distribution cools by breaking labor) whose winner is a parameter, not a foregone conclusion"
category: modeling
tags: [accommodation, endogenous-money, horizontalism, conflict, interest-rate, channel-decomposition, cost-channel, distribution, solvency-ceiling, switching-manifold, hidden-assumption, decoupling-regression, discipline-guard, method]
created: 2026-07-01
updated: 2026-07-01
severity: medium
component: src/accommodation
problem_type: conceptual_insight
root_cause: unnamed_limit_assumption
tracking: CYB-17
---

# The unbounded runaway was a hidden limit; the financed rate is a tug-of-war

CYB-17 adds the first *sustaining* channel — money/credit accommodation — to the bare CYB-6
conflict spiral, with a policy rate `i`. Two findings, both of the "reveal the hidden
assumption" kind the project keeps producing.

## Finding 1 — "unbounded" was never a law; it was the full-accommodation limit

CYB-6's marquee result was an **unbounded** nominal runaway for aspiration gap `g > 0`. But
CYB-6 has **no money and no credit**: nothing had to be financed, so nothing could choke.
The unboundedness was therefore not a property of the conflict mechanism — it was an
**unnamed assumption** sitting at a corner of parameter space: the **full-accommodation
limit**, where financing the spiral is costless and unconstrained. Name the constraint
(finance the wage bill at a rate `i`, with a finite creditworthiness ceiling) and the
runaway becomes **conditional**.

This is the same move as every prior module: the load-bearing feature was a hidden
constraint — order non-negativity (CYB-2), the conservation clamp (CYB-4), the wage floor
(CYB-6), and now the **financing constraint**. A result that looks like a law is often a
limit; find the corner it lives at and name the assumption that put it there.

## Finding 2 — the financed rate is a three-channel tug-of-war, not a lever

Once the wage bill is financed, the policy rate acts through **three channels at once**, and
they pull in **opposite directions**:

- **Cost** (inflationary): interest is a cost of production; firms defend margin *net of
  interest*, so a higher rate raises the effective gap → `π*` up (neo-Fisherian / cost-push).
- **Demand** (disinflationary, *symmetric*): the rate's slack damps both sides' claim
  adjustment equally → `π*` down, but the distribution `ω*` unchanged. Orthodoxy's mechanism.
- **Distributional** (disinflationary, *asymmetric*): the same slack breaks the *workers'*
  side (unemployment lowers `ω_w`) → `π*` down AND `ω*` toward capital. The thesis's mechanism.

The decomposition turns on **symmetry**: demand cools both sides, distribution breaks one.
Only the distributional channel drives `π*` cleanly to **zero** (it closes the gap); demand
merely scales the rate down; cost feeds. The **net is a tug-of-war whose winner is set by the
relative strengths** — free parameters. The disciplined result is not "the rate is
distributional/perverse"; it is that the model *can* produce any of the three and reports
which dominates for given strengths. Building fewer than three channels would have rigged the
answer (a pamphlet in one direction or the other).

## Why it's trustworthy (the validations)

- **Full-accommodation-limit regression byte-identical.** At `i→0`, cost off, `D_max→∞` the
  composed module reproduces CYB-6 (W, P) to `0.0`, *including* the unbounded runaway — so the
  financing loop is provably the only new thing (same anchoring role `κ=0` played in CYB-10;
  there is no closed form for the financed system, so the limit is the ground truth).
- **Extended conservation.** The identity grows from `wage + profit = 1` to
  `wage + interest + retained = 1` (retained is the residual, now after wages *and* interest),
  holding with the debt bookkeeping (`ΔD = borrowing − repayment`; rentier asset = firm debt)
  to `≤ 2e-16` throughout the spiral and the choke.
- **The solvency ceiling completes the switching-manifold set** (order non-negativity → wage
  floor → solvency), and is literally *ridden* (bind/release each step, echoing CYB-2's border).

## Takeaways (how to apply)

1. **A result that looks like a law may be a limit — find the corner and name the assumption.**
   "Unbounded" was true *at the full-accommodation corner*; the interesting physics is what
   happens when you leave it. Ask of any strong result: what unmodeled constraint is set to
   its costless/infinite value here?
2. **When a policy tool has multiple channels, build ALL of them or you rig the verdict.** The
   honest question is "which dominates," which is only askable if each is present and tunable.
   A one-channel model answers a question you baked in.
3. **"There is always a restraint" ≠ "the restraint always binds."** Require the model to be
   able to produce a restraint-present-but-insufficient region (here: cost-dominant, the rate
   feeds the spiral). If your mechanism *always* eventually chokes, you've smuggled in the
   conclusion — exactly the error the thing-being-critiqued makes.
4. **Distinguish "the orthodox tool is misaimed" from "heterodox tools work better."** This
   build only characterizes what the rate does; the normative claim is a separate, gated build
   (CYB-16). Keeping them apart is what lets the descriptive result be trusted by either side.

## References
- Code: `src/accommodation/model.py` (`AccommodationEconomy`, composes bare CYB-6 + the
  financing loop; three channels; solvency + monetarist clamps; extended conservation);
  `src/accommodation/run_v0.py` (regression → decomposition → H1a → boundary → solvency/monetarist).
- Plan: [`../plans/2026-07-01-feat-accommodation-v0-credit-ratification-channel-decomposition-plan.md`](../plans/2026-07-01-feat-accommodation-v0-credit-ratification-channel-decomposition-plan.md).
- The substrate it finances: conflict channel [[conflict-channel-is-nominal-level-instability-not-real-chaos]] (CYB-6).
  The composition-anchor pattern: [[coupling-super-additive-ignition-persistent-not-transient]] (CYB-10's `κ=0`).
- Endogenous money / horizontalism (Moore 1988; Kaldor; Lavoie); circuit theory (Graziani);
  cost channel (Barth & Ramey 2001); conflicting claims (Rowthorn 1977; Lavoie). Normative
  consumer: the monetarism critique (CYB-16), gated.
