# 04 — Augmenting the discipline: what a regime view adds to the standard toolkit

*Part of the [Cybeersym thesis set](00-index.md). Bounded by [05 — limits & honesty](05-limits-and-honesty.md);
the demonstration it defers to lives in [08 — future-work roadmap](08-future-work-roadmap.md).*

**The claim, stated honestly first.** This is an **argument**, not a demonstration. We argue that a
regime / domain-of-validity view *augments* the standard local toolkit by answering a question that
toolkit cannot pose about itself. We do **not** claim to forecast better, and — importantly — we do
**not** ship a worked example that "proves" it (see *Why we argue rather than demonstrate*, below).
The value asserted here is **representational and diagnostic**; the empirical superiority a skeptic
would (rightly) demand is [future work](08-future-work-roadmap.md), not a result.

---

## Where the mainstream is right (concede it cleanly)

Credibility starts with the concession, so make it plainly:

- **On forecasting a specific series, the standard tools win, and we don't compete.** A supply-shock
  model with a pass-through elasticity reproduces the 2022–23 egg-CPI spike at least as well as our
  SFC model, with far fewer researcher degrees of freedom. Our own record says it: *illustrative,
  not predictive.*
- **In the linearization-safe regime, equilibrium methods are not just adequate — they are correct.**
  "Near-equilibrium, linearization safe" is a *labelled regime* in our own taxonomy
  ([A1](../../research/notes/concepts/taxonomy.md)). Inside that basin, a Phillips curve and a
  well-specified DSGE are the right tools, and we agree.

If a regime view added nothing where local methods already work, it would be noise. The claim is
narrower and only about the boundary of that domain.

---

## The argument: a fitted relationship is *local by construction*

An estimated Phillips curve (or a small VAR) is a linearization around an operating point — a
relationship fit on a window of data. By construction it cannot tell you four things **about
itself**:

1. whether there is **more than one regime** the economy could be in;
2. **how far** the current state is from a border where the relationship changes or breaks;
3. whether a shock will **decay or ignite** a self-reinforcing move;
4. whether an observed "structural break" is a **regime transition** or an estimation artifact.

This is not a tuning gap — it is what *local* means. A regime view is exactly a map of the state
space *outside* the fitted window: which regimes exist, where their borders are, and how close you
sit to one. That is a different object than a fitted curve, and it is the thing we claim is worth
adding.

The sharpest illustration in our own work is the two-engine result: the *same* debt-distress signal
routes to inflation **or** deflation depending on a structural parameter, not on the shock (see
`src/fisher/README.md`, `docs/solutions/`, and [08](08-future-work-roadmap.md) for where this can and
cannot be pushed). A relationship fitted while the economy is in one basin has no representation of
the fact that a structural change *suppressing the markup-defense stabiliser* (the `α_p→0` edge)
flips the sign of its response — while at shipped parameters the same distress signal stays a
**bounded cycle**, not a runaway (the honest statement of the result; see [05](05-limits-and-honesty.md)).

---

## This is the Lucas critique — and a constructive corollary

None of the above is new, and pretending otherwise would be the fastest way to lose a serious
reader. **Robert Lucas (1976)** made exactly this point: estimated reduced-form relationships are
not structural — their parameters shift when policy or structure changes — so extrapolating them
across a regime change is unsafe. The Phillips curve's own history (its 1970s breakdown) is the
canonical case.

Our contribution is not to rediscover Lucas; it is a **constructive corollary**. Lucas is a
*warning* ("don't trust the reduced form across a regime change"). A regime view attempts the
*positive* version: a systematic, mechanism-grounded, **conservation-consistent** way to *map where
the regimes are and how close you sit to a border* — a **domain-of-validity certificate** for the
local method, rather than only the knowledge that one exists. Whether that map, built our way,
actually beats the tools that already try to detect regimes (below) is the open empirical question,
not something asserted here.

---

## Why we argue rather than demonstrate (the honest part)

We tried to *show* this on our own model — fit a classical baseline to a Cybeersym scenario and
exhibit its blindness to a regime border — and we **dropped the exhibit** after it was built and
independently reviewed. The reason is worth stating publicly, because it is the discipline the whole
project runs on:

> A demonstration on a model *we authored* is **circular**. If we define the regime border (a
> parameter in our own data-generating process) and then observe that a reduced-form fit can't see
> it, we have engineered the gap. Reduced to essentials, such a demo restates the Lucas critique on
> a toy plus the generic motivation for structural modeling — no new capability. (The build,
> review, and drop are logged in [`docs/reviewer-gate-log.md`](../reviewer-gate-log.md).)

A genuinely non-circular demonstration requires the border to live in **data we did not author** —
a real classifier applied to independent or held-out episodes. That is exactly the empirical program
in [08](08-future-work-roadmap.md), and it is *not done*. So this doc argues; it does not claim the
trophy.

---

## The real competitor is the frontier, not the textbook

A fair reader will note that the mainstream is already moving into this territory, and the honest
competitor is not Mankiw's undergraduate Phillips curve. It is:

- **regime-switching econometrics** (Markov-switching models) that detect regime changes from data;
- **central-bank agent-based and complexity models** (e.g. work at the Bank of England, the OFR);
- **occasionally-binding-constraint and financial-accelerator DSGE**, which reach for the nonlinear
  cases the linear core can't hold;
- **post-Keynesian stock-flow-consistent modeling** (Godley–Lavoie), the tradition our accounting
  discipline sits inside.

And economists who work the nonlinear cases by hand — multiple equilibria, self-fulfilling crises,
liquidity traps — are already doing *this kind* of analysis, one clever model at a time. The honest
positioning is therefore **not** "the mainstream can't do this." It is: *"we are trying to make that
analysis systematic, measurable, and accounting-consistent — a standing diagnostic layer rather than
a bespoke model per crisis — and here is a falsifiable signature program to test whether it earns
its keep."* Our edge over the frontier, *if* it holds up empirically, is the conservation/SFC rigor
(accounting that can't lie) plus instruments self-tested on known answers — not a claim to see what
they can't.

---

## The honest boundary (what this doc is allowed to conclude)

- **In scope, now:** we can *represent* — and *argue* the value of — a domain-of-validity map that a
  locally-fitted relationship cannot produce about itself; and we can be precise that a good local
  fit's very confidence *in-regime* is why it gives no warning near a border.
- **Not in scope, now:** any claim that our classifier beats regime-switching econometrics
  out-of-sample, or that a real economy sits near a border we've identified. Those require the
  [08](08-future-work-roadmap.md) empirical work; until then the ceiling is [05](05-limits-and-honesty.md)'s
  *representational*, not *forecast-superiority*.

The claim that survives cross-examination is modest and true: **a regime view is a different and
complementary object to a fitted relationship — it maps the boundary the fit is structurally blind
to — and making that map systematic and testable is the contribution; proving it more informative on
real data is the work still ahead.**

---

## Open threads (where we're unsure / roads not taken)

- **Is the constructive corollary more than Lucas + "use a structural model"?** Honestly, on paper
  it is close; the daylight only appears if the *systematic, measurable, cross-episode-reproducible*
  version (08) works. If it doesn't, this doc is a well-argued restatement of a known critique, and
  we should say so.
- **The dropped exhibit is a scar worth keeping.** It is tempting to rebuild a slicker version; the
  honest block is the authored-DGP circularity, which no amount of polish removes — only real data
  does.
- **"False confidence at a border" vs "a model without parameter X can't represent X."** The former
  is the non-trivial reading; the latter is trivial. The distinction is real but rhetorically
  fragile, and a hostile reader can collapse it. We keep the claim at the level the argument
  actually supports.

---

*Sources (linked, not copied): Lucas (1976), *Econometric Policy Evaluation: A Critique*;
[`THESIS.md`](../../THESIS.md); the taxonomy [registry](../../research/notes/concepts/taxonomy.md)
and [principles](../../research/notes/concepts/taxonomy-principles.md); `docs/solutions/` (the
two-engine / Fisher results); [`docs/reviewer-gate-log.md`](../reviewer-gate-log.md) (the dropped
exhibit).*
