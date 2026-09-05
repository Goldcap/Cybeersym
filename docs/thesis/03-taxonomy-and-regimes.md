# 03 — Taxonomy & regimes: diagnose the class, not the point

*Part of the [Cybeersym thesis set](00-index.md). The full registry lives in the research notebook
([`taxonomy.md`](../../research/notes/concepts/taxonomy.md) + its
[principles](../../research/notes/concepts/taxonomy-principles.md)); this doc is its thesis-facing
summary. Bounded by [05 — limits & honesty](05-limits-and-honesty.md).*

## The move

Stop identifying *points* ("the equilibrium," "is r>g," "where is the Phillips curve") and start
identifying **regimes**: what dynamical class an economy is in, and how close it sits to a border.
Meteorology classifies weather systems before forecasting rain; medicine diagnoses before treating;
macro argues *treatment* with no shared diagnosis. The classifier is meant to supply that missing
**diagnostic layer** — and, framed defensibly, its first job is to **certify the domain of validity
of equilibrium methods**: "near-equilibrium, linearization safe" is *one labelled regime*; elsewhere
it flags multiple basins, hysteresis, finite-amplitude transitions ([04](04-augmenting-the-discipline.md)).

## The registry, and the honesty rule built into it

The [class registry](../../research/notes/concepts/taxonomy.md) defines classes by **mathematical
behaviour** (invariant sets, boundedness, basin structure, transition type) *before* any historical
case is assigned — a class states the observables and decision rule that assign or reject membership.
Every class is marked `validated-instance` / `benchmark` / `candidate`, so *demonstrated* and
*aspirational* are never blurred. The registry itself is **hypothesis-status**: the frame is under
test; its *instances* sit at the reproducibility levels [05](05-limits-and-honesty.md) records.

A compressed view of the classes and where the project's own worked instances sit:

| Class | What it is | Instance in this project |
|---|---|---|
| **A1** stable / linearization-safe | equilibrium methods are correct here | the labelled "safe" regime (concession in 04) |
| **A2** structurally non-hyperbolic | a conserved center subspace, ∀ parameter | conserved chain (CYB‑2/4); Goodwin centre (CYB‑33) — *numerical* |
| **B1** bounded limit cycle | endogenous, self-limiting oscillation | Fisher on the markup-defense (CYB‑30) — *structural* |
| **C1** bistability / coexisting attractors | history selects the fate; hysteresis | finite-amplitude turbulence (CYB‑2/4); Keen bistability (CYB‑33) |
| **D1** local (smooth) bifurcation | eigenvalue crosses smoothly | *tested-and-rejected* as the chaos-core onset; a genuine Hopf is the unmerged CYB‑35/v1 work |
| **D2** global / border-collision | contact with an active constraint | CYB‑2/4 (numerical; formal proof gated, CYB‑13) |
| **E1 / E2** escape (nominal / real-burden) | hyperinflation / debt-deflation runaway | contagion Engine‑1 (CYB‑23); Fisher at α_p→0 (CYB‑30) |
| **E3** bounded grind / choke | bounded but pathological | the Minsky crunch (CYB‑19) |

The debt-dynamics rows are one coherent story on a single substrate — a distress signal that floors
into a cycle, ignites past a threshold, and escapes upward (nominal) or downward (real) by the
stabiliser balance. **All of this is structural-or-below** — a map of the classes a debt economy can
occupy, not a claim that a *real* economy is in one of them.

## Why it can't be a local-linearization exercise

The A2 result — conservation pins the equilibrium non-hyperbolic ∀ parameter — is the mathematical
reason a classifier built on this substrate cannot be a local eigenvalue check: the interesting
transitions are *global* (D2), which is exactly the open problem gated on an external mathematician
([08](08-future-work-roadmap.md), CYB‑13).

## Open threads

- **Assigning a *real* economy to a class is not done.** The registry is populated by our own models
  (structural), plus benchmarks. The empirical classification — pre-registered signatures on
  withheld data — is the trophy in [08](08-future-work-roadmap.md).
- **Honest gap: B2 (torus) is uninstantiated;** and some classes are observationally equivalent in
  short, noisy data (the registry's own F1 "unresolved" class is the honest output there).
- **The same series can fit multiple mechanisms.** Separating *math behaviour* from *measurement
  artifact* from *historical narrative* is the identifiability problem the whole classifier arc has
  to beat.

---

*Sources: the registry + principles (`research/notes/concepts/`); the module READMEs and
`CHANGELOG.md` for each cited instance; [04](04-augmenting-the-discipline.md), [08](08-future-work-roadmap.md).*
