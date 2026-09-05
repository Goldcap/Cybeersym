---
id: concept-taxonomy-principles
status: hypothesis
tags: [classification, dynamics, methodology, reproducibility, validation, falsifiability]
created: 2026-08-03
derived_from: conversations/2026/chaotic-economic-models/ (Andy + GPT discussion, 2026-08-03)
---

# Principles for a reproducible taxonomy of economic dynamics

## Purpose

Construct a mathematically defined taxonomy of economic dynamical behavior that is based on
explicit system structure, supported by reproducible evidence, independently testable, robust to
reasonable numerical and modeling choices, and empirically meaningful without being retrofitted
to individual historical episodes.

The project is not primarily a critique of DSGE, equilibrium theory, or any school of economics.
Existing frameworks may remain useful within their domains of applicability. The narrower
question is:

> Which classes of economic phenomena require a global dynamical description rather than—or in
> addition to—local analysis around an equilibrium or steady state?

The taxonomy should classify what a system is doing before prescribing why it is doing it or what
policy should follow. Its first obligation is auditability: another researcher should be able to
inspect the definitions, validate the mathematics, reproduce the diagnostics, and attempt to
falsify the assignment.

## Separation of taxonomy vs. theory

A **taxonomy** identifies mathematically distinguishable classes of behavior. A **theory** explains
why a system enters, remains in, or exits one of those classes. A **policy analysis** asks how an
intervention alters the system's state, parameters, basin geometry, or class membership.

The intended order is:

\[
\text{observation} \rightarrow \text{classification} \rightarrow \text{mechanism}
\rightarrow \text{policy}.
\]

Class definitions must not depend on prior commitment to a school of economic thought, a favored
historical narrative, or a desired policy conclusion. Competing theories may generate the same
dynamical class; the taxonomy should make that overlap visible rather than erase it.

## Mathematical class definitions

Classes should be defined before historical cases are assigned to them. Candidate defining
properties include:

- invariant sets and their stability;
- fixed points, periodic orbits, quasiperiodicity, and chaotic attractors;
- Lyapunov spectra and other independently checkable stability diagnostics;
- basin number, geometry, and boundary structure;
- hysteresis, path dependence, and finite-amplitude transitions;
- bounded trajectories versus escape or blow-up;
- contact with switching manifolds and active constraints;
- local versus global bifurcation mechanisms;
- robustness over stated parameter and initial-condition neighborhoods.

A class definition must state the observables and decision rule needed to assign or reject class
membership. Labels such as "1970s inflation," "Argentina-like," or "Minsky moment" may describe
episodes or interpretations, but they cannot define mathematical classes.

Where finite, noisy observations make two classes observationally equivalent, the honest output is
an equivalence set or unresolved classification—not false precision.

## Model construction

Models generate candidate mechanisms and testable signatures; they do not confer truth merely by
reproducing a trajectory. Every model used for classification should publish:

- equations or update rules, state variables, parameters, constraints, and units;
- initial conditions, boundary conditions, random seeds, and numerical tolerances;
- conservation or accounting identities and the assertions used to verify them;
- diagnostic algorithms and thresholds used to assign a class;
- parameter ranges and their rationale;
- known failure modes, non-identifiabilities, and domains of validity.

Model complexity should be earned. Begin with the smallest system that exhibits the proposed
class, self-test each diagnostic on a system with a known result, and add structure only when it
changes a falsifiable implication or resolves a documented failure.

## Empirical validation

Data validate or reject a proposed classification; they do not define the classes after the fact.
The empirical question is:

> Does an observed economy exhibit enough pre-specified signatures of a mathematical class to
> support assignment, and does that assignment survive withheld cases?

Prefer signatures that are harder to manufacture than visual agreement with one time series:

- recurrence and persistence structure;
- phase relationships and lag patterns;
- spectral features across defensible windows;
- hysteresis and response asymmetry;
- constraint activation and regime-transition indicators;
- boundedness, escape, or basin-switching evidence;
- cross-country or cross-episode replication;
- out-of-sample responses to measured shocks.

Parameter estimation is permissible when separated from class definition and validation. Estimate
on declared training data; freeze the class rule, model specification, and admissible parameter
procedure; then evaluate on withheld episodes, countries, or time windows. Historical narratives
remain hypotheses under test, not ground-truth labels.

## Reproducibility levels

Reproducibility is layered. Passing one level does not imply the next.

1. **Computational reproducibility.** Published code, environment, inputs, seeds, and commands
   recreate the reported tables, figures, and class assignments.
2. **Numerical reproducibility.** Results survive reasonable changes in solver, precision, step
   size, tolerances, transient length, sampling interval, and diagnostic implementation. Numerical
   artifacts are explicitly tested and reported.
3. **Structural reproducibility.** The qualitative class persists across a stated neighborhood of
   model specifications, parameters, initial conditions, and defensible alternative mechanisms.
   Otherwise the result is a property of one construction rather than a robust class.
4. **Empirical reproducibility.** Pre-specified signatures and decision rules replicate on new
   episodes, countries, datasets, or later observations not used to build or tune the model.

Claims should name the highest level actually demonstrated. "Reproducible" without a level is too
ambiguous for this project.

**Applied to the [v0.1 registry](taxonomy.md).** These levels are already operative, not
aspirational. Every worked instance the registry cites has reached at least **structural**
reproducibility (the qualitative class survives a stated parameter/spec neighborhood): the Fisher
bounded limit cycle and debt-deflation escape (CYB-30) over an (α_p, φ) sweep; the crunch grind
(CYB-19) and contagion escapes (CYB-23) over their horizon maps. The chaos-core classes (CYB-2/4:
structural non-hyperbolicity, coexistence, border-collision) hold at **numerical** reproducibility,
with the step to a *proof* being the gated open problem (CYB-13). **No instance yet claims
empirical reproducibility** — that is the withheld-episode work still ahead, and the registry says
so plainly rather than borrowing the word early.

## Anti-curve-fitting principles

- Define classes, diagnostics, thresholds, and exclusion criteria before assigning historical
  cases.
- Separate calibration, estimation, classification, and validation datasets and document every
  reuse.
- Prefer measured shocks, conserved quantities, institutional constraints, and mechanism-owned
  parameters over hand-shaped latent inputs.
- Never tune a forcing path solely to recover the target output trajectory.
- Report failed specifications, negative controls, sensitivity ranges, and alternative mechanisms.
- Use the same decision rule across comparable cases; deviations require a reason recorded before
  results are known.
- Treat a good visual fit as exploratory evidence, never as sufficient validation.
- Penalize complexity and researcher degrees of freedom; add a parameter only with a mechanism,
  identifiable role, and falsifiable consequence.
- Withhold episodes or countries early, and keep them untouched until the class rule is frozen.
- Prefer predictions of qualitative structure and response over point forecasts the model was
  tuned to reproduce.

"Not fitted to data" therefore does not mean "data-free" or "no estimated parameters." It means
that empirical information cannot silently redefine the class, its diagnostics, or its success
criteria after results are visible.

## Open questions

- What is the minimum sufficient set of observables for each candidate class?
- Which mathematical distinctions remain identifiable in short, noisy, non-stationary macro data?
- How should uncertainty in class membership be represented: probabilities, equivalence sets, or
  explicit non-classification?
- What robustness neighborhood is sufficient for structural reproducibility?
- Which diagnostics remain trustworthy in high-dimensional, nonsmooth, slow–fast SFC systems?
- How should switching-manifold contact and institutional constraints enter class definitions?
- Can a common pre-registered rule reproduce across independent countries and episodes without
  erasing historically relevant structure?
- What evidence would falsify the taxonomy itself, rather than only one model within it?

## Next steps

1. ~~Turn the candidate behaviors in [Taxonomy](taxonomy.md) into a versioned class registry with
   necessary conditions, sufficient evidence, exclusions, and unresolved equivalences.~~
   **Started — [registry v0.1](taxonomy.md)** (2026-09-05): classes A1–F1 defined and populated
   from the validated CYB modules. Remaining: version each future edit with a dated rationale; fill
   the honest gaps (e.g. B2/torus not yet instantiated).
2. Define a standard diagnostic report: inputs, transient handling, numerical checks, uncertainty,
   sensitivity, class decision, and failure conditions.
3. Select closed-form or canonical benchmark systems for computational and numerical self-tests.
4. Pre-register one empirical signature set and one decision rule before examining the first
   validation portfolio.
5. Divide available episodes and countries into mechanism development, calibration, and untouched
   validation sets.
6. Publish a minimal replication bundle and ask an independent reader to reproduce both a positive
   and a negative classification.

## Related

[Taxonomy](taxonomy.md) · [Phase-Space Macroeconomics](phase-space-macroeconomics.md) ·
[Parameterization and control structure](parameterization-and-control-structure.md) ·
[Natural-experiment portfolio](natural-experiment-portfolio.md) ·
[Open questions](../../indexes/questions.md)

## Provenance

Derived from the Chaotic Economic Models conversation
(`../../conversations/2026/chaotic-economic-models/`), especially the 2026-08-03 discussion of
evidence-based, non-retrofitted, independently reproducible taxonomy design. This note is a
methodological constitution to test and revise, not an established result.
