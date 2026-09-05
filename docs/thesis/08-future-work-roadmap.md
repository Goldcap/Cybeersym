# 08 — Future work: the roadmap from *representational* to *empirical*

*Part of the [Cybeersym thesis set](00-index.md). This doc is the honest home of the ambition: the
claims we would *love* to make and the exact work each requires before we may. Nothing here is
claimed as done — the [limits doc](05-limits-and-honesty.md) governs what is.*

The project today is a **representational and methodological** contribution: it can *build* and
*characterise* dynamics (endogenous debt cycles, opposite-sign escapes on one distress signal,
structurally non-hyperbolic equilibria) that models linearised around a unique equilibrium cannot
represent, and it can *argue* — see [04](04-augmenting-the-discipline.md) — that a good local fit is
blind to its own domain-of-validity border. What it has **not** done is show, on data it did not
author, that this buys a decision a working macroeconomist would pay for. This page is the path from
the first thing to the second.

---

## What is actually in hand (the honest inventory)

- **Egg arc** — a mechanism reproducing the 2024‑25 HPAI price-peak *timing* it was never fit to
  (empirical, narrow); the distributional wedge as a read-out over the validated path.
- **The channel stack** (CYB‑6 conflict → CYB‑17 accommodation → CYB‑19 crunch → CYB‑23 contagion →
  CYB‑30 Fisher) — structural results, byte-exact nested, conservation < 1e‑10: the rate as a
  three-channel tug-of-war; the crunch that bounds-without-curing; two opposite-sign escapes on one
  distress signal; the markup-defense as a structural price floor.
- **The instruments** (`src/chaos/`: Lyapunov, bifurcation, linearisation, border-collision) —
  self-tested on the logistic map and now on the **Goodwin–Keen rung** (CYB‑33/35: a conservative
  centre and a genuine local Hopf recovered against analytic answers).
- **The [taxonomy registry](../../research/notes/concepts/taxonomy.md)** — classes A1–F1 with
  worked instances, each labelled by the level it has reached.

That is a validated *toolkit and a class registry*. It is not yet a validated *diagnosis of a real
economy*.

---

## The trophy we do not yet have — and exactly what would earn it

**Goal:** a genuinely non-circular demonstration that the approach is *more informative* than the
standard local toolkit — the thing [04](04-augmenting-the-discipline.md) currently only argues.

**Why we can't claim it now.** The honest version cannot be shown on a model we authored: if *we*
define the regime border (a parameter in our own DGP) and then note a reduced-form fit can't see it,
the demonstration is circular (this is precisely why the first flagship exhibit was built,
reviewer-gated, and **dropped** — see [`docs/reviewer-gate-log.md`](../reviewer-gate-log.md)).

**What would earn it (the test we'd have to pass, pre-registered before we look):**
1. A **real regime classifier** — the instruments applied to produce a regime label + distance-to-
   border + basin membership from *data*, not from sweeping our own parameter.
2. Applied to **independent / held-out data where the border is not authored** — cross-country panels
   (the WID/Piketty slow manifold, `research/data/wid/`), or withheld historical episodes
   ([natural-experiment portfolio](../../research/notes/concepts/natural-experiment-portfolio.md)).
3. A **pre-specified signature set + decision rule**, frozen before the withheld cases are examined,
   that a classical baseline (a Markov-switching model, a small VAR) does **not** provide — e.g. a
   regime-boundary warning that replicates across independent realisations of "the same" regime.
4. Passing means: the diagnosis survives cases it was not built on. Only then may "reflects
   real-world dynamics" be said, and only at that level.

Until (1)–(4), the claim stays where [05](05-limits-and-honesty.md) puts it: **argued, not demonstrated.**

---

## The next arc: the phase-space classifier (CYB‑26 → CYB‑29)

The substrate the GK-validated instruments are meant to run on
([phase-space macro](../../research/notes/concepts/phase-space-macroeconomics.md);
[four-layer control structure](../../research/notes/concepts/parameterization-and-control-structure.md)):

- **CYB‑26 — state-space axes** (the fast coordinates: inflation, output, spreads, …).
- **CYB‑27 — the vector field** (the parameters; the distinguished control/bifurcation parameters).
- **CYB‑28 — endogenous slow variables** (leverage, wealth concentration — Piketty as the slow
  manifold that walks the fast system across borders; the reflexivity that makes macro
  history-dependent). The hardest, most novel layer.
- **CYB‑29 — thresholds** (the switching manifolds: real constraints going active — the border a
  transition *is*).

These are **design-first seeds** (definitions + selection criteria, not yet a running model). The
classifier that *consumes* all four — a slow–fast conserved SFC substrate with a thin WID loader —
is the build that could support the empirical trophy above.

---

## Signals we'd want but cannot honestly show yet

- **Critical slowing down** (rising lag-1 autocorrelation + variance before a basin crossing —
  Scheffer et al.). A model-free early-warning that would make the "diagnosis, not forecast" claim
  concrete. **Aspirational:** our current models collapse too *abruptly* to exhibit a slow variance
  ramp (the honesty gate caught an attempt to show it on the Fisher model). It needs a genuine
  slow–fast substrate (CYB‑28) with a graded approach to the border.
- **Cross-country reproduction** of a regime's dynamical signature (a *class* vs a *narrative*) —
  the reproducibility test on WID's panel.

---

## Gated on outside expertise (do not solo-build)

- **CYB‑13 — the formal global-bifurcation proof.** The conserved substrate is non-hyperbolic ∀β, so
  the onset sits outside the standard local-bifurcation toolkit; making the classification rigorous
  needs a piecewise-smooth-dynamics specialist (the `docs/outreach/` bifurcation note is the
  calling-card). Parked after the first outreach declined; do not solo-build.
- **CYB‑16 — the monetarism critique.** The normative reading of the rate results; gated on external
  economic buy-in and firewalled from the descriptive work (see [05](05-limits-and-honesty.md)).

---

## The staging, in one line

**Representational + methodological (now) → structural robustness across the classifier arc (next) →
empirical, on withheld data, with a pre-registered rule (the trophy).** Each rung is only claimed
once its own bar is cleared — and the reviewer gate is what stops the next rung's excitement from
being written as if it were done.

## Open threads

- **Is the WID slow-manifold hypothesis (CYB‑28) right — do distributional slow variables actually
  walk the fast system across borders?** It's the load-bearing bet of the whole classifier arc, and
  it is unproven.
- **Small-N is the killer for the empirical trophy** — few instances per regime type; early-warning
  signals are noisy; the pre-registration discipline is the only defence against fooling ourselves.
- **The classifier might not add over a Markov-switching baseline.** If a pre-registered run can't
  beat regime-switching econometrics on withheld data, the honest conclusion is that the value stays
  representational — and [05](05-limits-and-honesty.md) already reserves that possibility.

---

*Sources (linked, not copied): the classifier-arc tickets CYB‑26…29; `phase-space-macroeconomics.md`,
`parameterization-and-control-structure.md`, `natural-experiment-portfolio.md`; `research/data/wid/`;
CYB‑13 / CYB‑16 (gated); the [reviewer-gate log](../reviewer-gate-log.md).*
