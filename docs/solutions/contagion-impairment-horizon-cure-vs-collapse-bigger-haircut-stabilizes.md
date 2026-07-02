---
title: "Whether default cures a debt grind or detonates into contagion-collapse is a CONTEST between two feedbacks (impairment→risk-premium→more-Ponzi vs inflation-erodes-the-real-impairment), so the cure↔collapse frontier is genuinely ragged, not a clean line — and counterintuitively a BIGGER haircut (lower recovery) is MORE stabilizing because clearing more debt per default cures the borrower faster than the extra lender-impairment detonates; the collapse it produces is a hyper-INFLATIONARY risk-premium spiral (Engine 1, credit-quantity), which is NOT Fisher debt-deflation (Engine 2, gated) — and CYB-17's demand channel disinflates but never deflates, so Fisher needs a strengthened price channel, not a switch-on"
category: modeling
tags: [minsky, default, debt-deflation, impairable-rentier, contagion, risk-premium, recovery-rate, haircut, balance-sheet, godley-lavoie, capital-account, stock-flow-consistent, nested-regression, fisher, gated-engine, ragged-frontier, discipline-guard, method]
created: 2026-07-02
updated: 2026-07-02
severity: medium
component: src/contagion
problem_type: conceptual_insight
root_cause: outcome_is_a_contest_between_competing_feedbacks
tracking: CYB-23
---

# Default's cure-or-detonate is a contest; and a bigger haircut is more stabilizing

CYB-19 Phase 2 lets Phase 1's bounds-without-curing grind terminate in **default**, and makes the
rentier pool **impairable** (it stops passively absorbing losses). The build sweeps the
**impairment horizon** — how strongly the impaired lender feeds back — and finds four things worth
carrying forward.

## Finding 1 — cure-vs-collapse is a contest between two feedbacks, so the frontier is ragged

Default cures the borrower (clears the debt feeding the cost channel) but impairs the lender. Wire
the impaired lender's feedback as a risk premium on credit (`i_eff = i + ε·impairment/P`, Engine 1,
credit-quantity) and sweep `ε`:

- **ε=0** (passive absorber): CURE — the grind stays bounded, the rentier eats the losses.
- **ε high**: CONTAGION-COLLAPSE — premium → more Ponzi → more default → more impairment → higher
  premium → hyperinflationary blow-up.

Both reachable (not rigged). But the boundary is **ragged**, and for a real reason: **two feedbacks
compete** — the contagion loop (positive) versus a *self-cure* loop (negative): higher inflation
raises `P`, which shrinks `impairment/P`, which lowers the premium before it can detonate. Inflation
erodes the real impairment. So whether a given `(ε, recovery)` cell cures or collapses is a race,
and near the frontier tiny changes flip it. **Lesson: when an outcome is set by competing
feedbacks, expect (and report) a contested frontier — a clean bifurcation line would be the
suspicious result, not the ragged one.**

## Finding 2 — a BIGGER haircut (lower recovery) is MORE stabilizing (counterintuitive)

Naively, bigger write-offs = bigger lender losses = more contagion. The model says the opposite:
**lower recovery collapses LESS** (collapse fraction `recovery=0.30` → 5%, `recovery=0.90` → 62%).
Clearing more debt per default cures the borrower faster (lower `D` → lower interest → lower
cost-push → out of Ponzi), so fewer subsequent defaults accumulate less total impairment. A
**stingy** haircut barely clears, so the borrower keeps defaulting, and the drip of impairment
eventually ignites the premium spiral. **Bankruptcy that hurts the lender more *per event* can be
more stabilizing because it fixes the borrower** — a genuinely non-obvious policy-relevant result.

## Finding 3 — the collapse is hyper-INFLATIONARY (Engine 1), NOT Fisher debt-deflation (Engine 2)

Two mechanisms both get called "debt-deflation" and must not be conflated. Engine 1 (wired) is
credit-QUANTITY contagion via the risk premium — it blows up **inflation**. Engine 2 (gated off) is
the price-level **Fisher** loop (activity collapse → P down → real burden up) — it blows up
**deflation**. They are opposite in sign. Keeping Engine 2 gated means any collapse observed here is
honestly attributable to Engine 1. **Verification delivered:** CYB-17's demand channel damps
inflation toward 0 but never negative — it *disinflates, it does not deflate* — so Engine 2 needs a
*strengthened* price channel (a Phase-2b prerequisite), not a mere switch-on. **Lesson: when two
distinct mechanisms share a name, wire one and gate the other, and verify the gated one's
prerequisite before claiming it — don't let a same-named cousin borrow your result's credibility.**

## Finding 4 — the SFC payoff: the write-off is a STOCK event, and the capital account must close

Phase 1's conservation was a *flow* identity (shares sum to 1). A write-off is a **stock** event, so
Phase 2 upgrades to a full **capital-account reconciliation** (Godley–Lavoie: every financial asset
is someone's liability): `ΔD = borrowing − repayment − writeoffs`; rentier wealth ↓ by the
write-off; **borrower-liability-↓ ≡ lender-asset-↓**. The identity `rentier_wealth ≡ firm_debt`
closes to `≤ 4e-12` through the default/impairment transient *and* through collapses. This is the
criterion that makes the SFC spine earn its keep at the balance-sheet level, not just the flow level.

## A substrate caveat that shaped the design (worth remembering)

CYB-17's debt is a **revolving wage fund** (`D_next = W + capitalized`), so it does not accumulate a
persistent pile and a naive write-off reverts next period. Two consequences: (a) the default trigger
must be the pile in **real** terms (nominal is inflated away), and (b) "cure" is honest **loss
absorption that keeps the grind bounded**, NOT below-floor disinflation — clearing revolving debt has
no persistent disinflationary bite. Reported as an honest negation of the strong-cure claim (AC4).

## Why it's trustworthy

- **Nested regression byte-exact:** `recovery=1 ⇒ Phase 1` (`0.0`); `+crunch-off ⇒ CYB-17` (`0.0`).
  `CYB-17 ⊂ P1 ⊂ P2`, clean at each shell.
- **Capital-account identity `≤ 4e-12`** through defaults and collapses.
- **Determinism** — byte-identical reruns; **graceful runaway detection** (freeze at the blow-up,
  so collapse is observable, not a NaN crash).

## Takeaways (how to apply)

1. **Competing-feedback outcomes have contested (ragged) frontiers — report the raggedness.**
2. **Interrogate "obvious" sign intuitions.** Bigger loss ≠ more contagion here; the borrower-cure
   dominates. Sweep, don't assume.
3. **Same-named mechanisms: wire one, gate the other, verify the gate's prerequisite.**
4. **A write-off is a stock event — upgrade conservation to the capital account or the model lies.**

## References
- Code: `src/contagion/model.py` (`ContagionEconomy` — composes an unchanged `CrunchEconomy`; adds
  default + impairable rentier + the swept premium elasticity + gated Fisher + balance-sheet asserts);
  `src/contagion/run_v0.py`.
- Plan: [`../plans/2026-07-02-feat-contagion-v0-phase2-default-impairable-rentier-impairment-horizon-plan.md`](../plans/2026-07-02-feat-contagion-v0-phase2-default-impairable-rentier-impairment-horizon-plan.md).
- Parents: crunch Phase 1 [[crunch-bound-vs-fizzle-is-an-outcome-crunch-bounds-but-doesnt-cure]] (CYB-19);
  accommodation [[accommodation-runaway-was-full-accommodation-limit-rate-is-a-tug-of-war]] (CYB-17).
- Forward-links: Phase 2b (switch Engine 2 / Fisher on, after strengthening the price channel);
  Phase-2-on-coupled; unit-level / network default. Anchors: Minsky (FIH); Keen (Goodwin–Minsky);
  Fisher 1933 (Engine 2, gated); Bernanke–Gertler (financial accelerator); Godley–Lavoie (SFC).
