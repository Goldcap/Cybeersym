# 05 — Limits & honesty: what Cybeersym does *not* claim

*Part of the [Cybeersym thesis set](00-index.md). Front door: [`THESIS.md`](../../THESIS.md). This
doc is the boundary of every other doc — read it before trusting any claim in the set.*

The project's one non-negotiable: **name the highest level of support a claim actually has, and
never borrow a stronger word.** This page is where we do that out loud. It exists because the
failure mode we most fear is a confident claim that is wrong in a way the reader can't see — so we
make the boundary a first-class artifact, not a footnote.

---

## The reproducibility ladder — and where each result actually sits

From the [taxonomy principles](../../research/notes/concepts/taxonomy-principles.md). The levels are
nested; passing one does **not** imply the next, and a claim must name the highest it has *actually*
reached:

1. **Computational** — published code + seeds recreate the reported tables/figures.
2. **Numerical** — the result survives reasonable changes of solver, precision, step size, transient
   length, and diagnostic implementation.
3. **Structural** — the qualitative class persists across a stated neighbourhood of model
   specifications, parameters, and initial conditions (not a property of one construction).
4. **Empirical** — pre-specified signatures replicate on **new** episodes/countries/data **not used
   to build or tune** the model.

Where the project's results honestly sit today:

| Result | Highest level reached | Note |
|---|---|---|
| Egg **timing** — both HPAI peaks from the real NASS flock series (2024‑25 never fit) | **Empirical** (narrow) | The project's strongest empirical foothold: a mechanism reproducing an *unfit* episode. One commodity. |
| Egg **magnitude** — the single linear price–deficit slope | **Structural** | Honestly *degrades* out-of-sample (overshoots ep2); reported, not re-tuned. |
| The channel stack — conflict / accommodation / crunch / contagion / Fisher (CYB‑6/17/19/23/30) | **Structural** | Behaviours persist across parameter sweeps; byte-exact nesting; conservation < 1e‑10. **Not** validated against real debt-dynamics data. |
| Goodwin–Keen instrument rung (CYB‑33/35) | **Numerical / Structural** | A benchmark self-test on analytic answers, not an economy. |
| Chaos core (CYB‑2/4) — border-collision on a non-hyperbolic substrate | **Numerical** | A formal *proof* is the gated open problem (CYB‑13). |
| The taxonomy [registry](../../research/notes/concepts/taxonomy.md) | **Hypothesis** | The frame is under test; its *instances* sit at the levels above. |
| "Our approach is **more informative** than classical macro" | **Not demonstrated** | Argued (see [04](04-augmenting-the-discipline.md)); a non-circular demonstration is [future work](08-future-work-roadmap.md). |

**The headline no one should miss:** outside the narrow egg-timing result, **nothing in the
debt-dynamics or classifier arc has reached empirical reproducibility.** Those results are
structural — real properties of the model class — but they are not yet claims about a real economy.

---

## What this project is *not* claiming

- **Not predictive — illustrative.** A chaotic / limit-cycling system cannot be point-forecast in
  principle. The claim is never "eggs will be $X in March," it is "*this* is how a shock propagates
  through *this* structure." Climate model, not weather forecast.
- **Complication is not chaos.** Chaos is a *measured* claim (positive Lyapunov exponent, sensitive
  dependence, a characterisable attractor), never asserted from turbulent-looking output. Where the
  measurement said *not* chaos (the conflict channel is nominal-level instability, not real chaos;
  the Fisher loop on the shipped stabiliser is a **bounded limit cycle, not a debt-deflation
  runaway**), we say so.
- **No single number validates a model.** A correlation or a fitted slope is exploratory evidence,
  never sufficient. The bar is out-of-sample + mechanism-not-curve-fit (see [06](06-evaluation.md)).
- **Not "inflation *is* a supply constraint."** Eggs are *one validated channel*. The framework is
  channel-plural by design; monocausality from either side is the error.
- **We do not detect chaos in real macro data directly.** The 1980s–90s detection programme failed
  for good reasons ([`docs/empirical_grounding.md`](../empirical_grounding.md)); we validate the
  *mechanism* and stay illustrative, and treat historical regime narratives as hypotheses under
  test, not ground truth.

---

## The descriptive / normative firewall

The models characterise **what the interest rate / the mechanism *does*** — that the rate acts
through three offsetting channels, that on the coupled substrate it reads redistributive more than
stabilising, that firing the financing border bounds without curing, that a conflict economy's
markup-defense structurally floors the price level. **That is descriptive and in scope.**

The **normative** reading — "the rate is misaimed / punitive," the monetarism critique — is a
*separate* claim, held behind a firewall. Its build (**CYB‑16**) is **gated on external economic
buy-in and is not made here.** "The orthodox tool is distributional rather than allocative" (which
the models can illuminate) is kept strictly apart from "heterodox tools work better" (a different,
unbuilt model this project does *not* imply). The descriptive results persuade *because* they are
refutable and do not depend on the normative conclusion.

---

## The honesty machinery (so the boundary isn't just a promise)

- **The reviewer gate** ([`CLAUDE.md` §"The reviewer gate"](../../CLAUDE.md)): no result is *done*
  until a fresh, independent reviewer re-runs it and re-derives its claims. Builder ≠ reviewer.
- **The escaped-defect log** ([`docs/reviewer-gate-log.md`](../reviewer-gate-log.md)): every
  "whoops" is recorded, and a recurring class escalates the checks. The gate has already caught
  centerpiece-grade overclaims *before* publication (a stated constant off by a digit; a would-be
  flagship exhibit whose strong claim was trivial/circular — dropped, not shipped).
- **Byte-exact nesting + conservation asserts:** every composed module must reproduce its parent
  exactly and keep money/goods conserved to machine precision, or a change is rejected.

---

## Open threads (where the boundary itself is uncertain)

- **Is "structural reproducibility" enough to interest an economist, or only an empirical result?**
  We suspect the honest answer is: the structural results are a *representational* contribution, and
  the empirical bar is the one that earns "reflects real-world dynamics." We have not crossed it.
- **The egg empirical foothold is narrow (one commodity, two episodes).** Whether the method
  generalises is exactly the withheld-episode work in [08](08-future-work-roadmap.md).
- **The firewall is a discipline, not a theorem.** A reader who wants the normative conclusion can
  read it into the descriptive results; we can only refuse to *make* it, and flag where the
  temptation lives.

---

*Sources (linked, not copied): [`THESIS.md`](../../THESIS.md) · taxonomy principles
(`research/notes/concepts/taxonomy-principles.md`) · `docs/empirical_grounding.md` ·
`docs/reviewer-gate-log.md` · `CHANGELOG.md`. Support-level labels follow the ladder above.*
