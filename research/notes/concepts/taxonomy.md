---
id: concept-taxonomy
status: hypothesis
tags: [classification, dynamics, macroeconomics, registry, bifurcation, minsky, keen]
created: 2026-08-03
updated: 2026-09-05
derived_from: >
  conversations/2026/chaotic-economic-models/ (Andy + GPT, 2026-08-03);
  Claude Code synthesis 2026-09-05 (registry v0.1 populated from the validated CYB modules)
---

# Taxonomy of Economic Dynamics — the class registry

## Working idea

Classify economic models and observed episodes by **qualitative dynamical behavior** — fixed
points, cycles, multiple attractors, bifurcations, escape — rather than only by school or equation
family. The [principles note](taxonomy-principles.md) is the constitution (how a class may be
defined and validated); **this note is the registry** (the classes themselves). Class definitions
come before historical cases; each class states the observables and decision rule that assign or
reject membership.

This is the classifier's payload: [phase-space-macroeconomics](phase-space-macroeconomics.md) says
*diagnose the regime, not the point*; the [four-layer control structure](parameterization-and-control-structure.md)
says *find the low-dimensional handles*; the registry says *here are the regimes, and here is how
you tell which one you are in*.

## Why now / the Keen-facing point

Steve Keen's program is the natural home for this: endogenous money, Goodwin–Minsky debt dynamics,
and the insistence that macro is a **global dynamical** problem, not a local expansion around
equilibrium. The taxonomy operationalizes exactly his narrow question — *which phenomena require a
global description rather than local analysis around a steady state?* — and, crucially, it is **not
vaporware**: the egg/inflation arc has already built and validated worked instances of a whole
debt-dynamics corner of the registry (a bounded debt-cycle, threshold ignition, two opposite-sign
escapes on one distress signal), and the chaos arc has instantiated the hard mathematical corner (a
structurally non-hyperbolic equilibrium, coexisting attractors, a global border-collision). The
registry below marks each class `validated-instance` / `benchmark` / `candidate` so the difference
between *demonstrated* and *aspirational* is never blurred.

## Registry entry schema

Each class carries, per the principles' Next-step 1:

- **Defining property (necessary).** The mathematical condition — invariant-set / boundedness /
  basin / transition structure. Not a narrative label.
- **Diagnostic (sufficient evidence).** The measurement + instrument + threshold that assigns it,
  and (for our instances) the conservation/accounting check that keeps it honest.
- **Exclusions.** What the class is *not*, and the observation that rejects membership.
- **Observational equivalence.** What it can be confused with in short, noisy data → an
  equivalence set, not false precision.
- **Instance(s).** Worked example(s): a CYB module (with ticket + the highest reproducibility level
  reached), a canonical benchmark, or an honest `candidate` placeholder.

All instances **link** canonical results (CYB-NN · commit · `docs/`/`src/`) — they do not copy
them (notebook rule). Status of a *class* ≠ status of its *instance*: the registry is a hypothesis;
the instances it cites may be independently validated.

---

## A. Equilibrium classes (rest states)

### A1 — Stable hyperbolic equilibrium (linearization-safe)
- **Defining property.** An attracting fixed point whose Jacobian spectrum lies strictly inside the
  unit circle (map) / left half-plane (flow); perturbations decay; no switching manifold nearby.
- **Diagnostic.** Dominant `|λ| < 1` with margin; no active constraint within the perturbation
  neighborhood; return-to-rest after a shock. This is the regime that *certifies the domain of
  validity of equilibrium/DSGE methods* — one labelled class, not the whole space.
- **Exclusions.** A single eigenvalue on the unit circle (→ A2); a nearby border (→ T2/T3).
- **Observational equivalence.** A slowly-decaying stable node vs a long-period cycle can look
  alike in a short window; separate by AC(1)/variance trend and phase structure.
- **Instance.** `benchmark` — near-baseline conflict economy (CYB-6) at low adjustment speeds,
  wage share near its floor target. (Illustrative; not the project's headline.)

### A2 — Structurally non-hyperbolic equilibrium (permanent center subspace)
- **Defining property.** One or more eigenvalues pinned **exactly** on the unit circle *by
  construction* (a conservation functional), for **all** parameter values — the equilibrium is
  non-hyperbolic ∀β, not at isolated bifurcation points.
- **Diagnostic.** A conserved quantity ⇒ left/right eigenvector at `λ = 1`; verified numerically
  (spectrum shows the pinned unit eigenvalue that never moves under β).
- **Exclusions.** A center that appears only at a critical parameter (that is an ordinary local
  bifurcation, A1↔C3 via T1) — not this class.
- **Observational equivalence.** Indistinguishable from a marginally-stable system over short data;
  the *structural* claim needs the model's conservation law, not the series.
- **Instance.** `validated-instance` — the conserved 3-tier chain (**CYB-2/CYB-4**); the pinned
  `λ=1` is why standard local bifurcation theory does not close the onset (the reduction is the
  gated formal-proof question, **CYB-13**). This class is the mathematical reason the classifier
  cannot be a local-linearization exercise.

## B. Cyclic classes (bounded oscillation, no rest)

### B1 — Bounded limit cycle (endogenous, self-limiting)
- **Defining property.** An attracting periodic orbit; trajectories neither rest nor escape; the
  amplitude is **non-secular** (running extrema stationary over long horizons).
- **Diagnostic.** A stable closed orbit; running-min/running-max of the log-state byte-identical
  across early vs late windows over a long run (the operational non-secular test).
- **Exclusions.** A transient swing that later escapes (→ E-classes) or decays (→ A1); reject by
  the long-horizon secular check.
- **Observational equivalence.** A limit cycle vs forced/noisy oscillation vs low-order chaos —
  separate by return maps, recurrence, and spectral concentration.
- **Instance.** `validated-instance` — **Fisher Phase 2b (CYB-30)**: composed on the conflict
  layer's markup-defense the Fisher price-cut is a *bounded deflationary limit cycle* at the
  shipped stabilizer (non-secular for every φ up to 20). `benchmark` — the **Goodwin** cycle
  (employment × wage share), the instrument self-test rung ([control-structure note](parameterization-and-control-structure.md)).

### B2 — Quasiperiodic / torus
- **Defining property.** Two (or more) incommensurate frequencies; motion dense on an invariant
  torus; no frequency locking.
- **Diagnostic.** Two independent basic frequencies in the spectrum; a closed-curve Poincaré
  section that does not collapse to points.
- **Instance.** `candidate` — **not yet instantiated** in a CYB module. Placeholder pending a
  two-slow-frequency substrate (a target of the slow–fast build, CYB-28 territory).

## C. Multi-attractor classes (basin structure)

### C1 — Bistability / coexisting attractors (finite-amplitude birth, hysteresis)
- **Defining property.** ≥2 attractors coexist at the **same** parameters; the realized state is
  history/initial-condition dependent; a control sweep shows a hysteresis loop; a new attractor is
  born at **finite amplitude** (not by a small-amplitude local bifurcation).
- **Diagnostic.** Measured coexistence + hysteresis under up/down parameter sweeps; a basin
  boundary separating outcomes; onset amplitude bounded away from zero.
- **Exclusions.** A unique global attractor reached from all initial conditions (→ A/B); reject by
  failure to find a second basin.
- **Observational equivalence.** Bistability vs a single attractor under a shifting slow variable
  can mimic each other — the slow–fast separation is what distinguishes them.
- **Instance.** `validated-instance` — **CYB-2/CYB-4**: turbulence appears as a coexisting attractor
  born at finite amplitude with measured hysteresis. `related` — the contagion **impairment
  horizon** (CYB-23) is a *parameter-space* basin map (cure vs contagion-collapse both reachable on
  a ragged frontier), the outcome-map cousin of coexistence.

## D. Transition classes (how the state moves between A–C — bifurcation type)

### D1 — Local (smooth) bifurcation
- **Defining property.** A qualitative change produced by an eigenvalue crossing the stability
  boundary **smoothly** (fold / Hopf–Neimark–Sacker / period-doubling).
- **Diagnostic.** The dominant spectrum crosses the unit circle at the border; a normal form applies.
- **Instance.** `benchmark` — logistic period-doubling (self-test). **Tested-and-rejected as the
  mechanism** in CYB-2/4: the hyperbolic spectrum tops out at `|λ|≈0.92` and **never crosses** while
  chaos exists — a *negative result* (support for `refuted`, per the principles), and the reason the
  onset is not this class.

### D2 — Global / nonsmooth bifurcation (border collision, active constraint)
- **Defining property.** A qualitative change produced by trajectory **contact with a switching
  manifold** (a real constraint going active) rather than a local eigenvalue crossing — a
  border-collision, here of a *cycle* on a non-hyperbolic substrate.
- **Diagnostic.** Onset at finite amplitude; a constraint activates at the transition; no spectral
  crossing accompanies it; classified with the border-collision instrument (`src/chaos/`).
- **Exclusions.** Any transition with a clean smooth eigenvalue crossing (→ D1).
- **Observational equivalence.** Hard to separate from D1 or from noise-induced tipping in data
  alone; needs the model's constraint set. **This is the classifier's mathematical core and the
  gated open problem** (CYB-13; the reduction past the non-hyperbolic wall).
- **Instance.** `validated-instance` (numerically) — **CYB-2/CYB-4**; formal rigor **gated** (CYB-13).
  The economy-wide analogue is the switching-manifold through-line: order non-negativity → wage
  floor → solvency ceiling → capitalized-interest tipping.

### D3 — Threshold ignition (control-parameter crossing to a self-reinforcing loop)
- **Defining property.** A control parameter crosses a value beyond which a positive feedback
  dominates its stabilizer, flipping a bounded regime to escape (→ E). The pivot is the balance of
  a destabilizing loop against a **structural stabilizer**, not the loop's raw strength.
- **Diagnostic.** A swept control parameter with a located boundary between bounded and escape;
  both sides reachable (or it's rigged); the stabilizer identified (removing it moves the threshold).
- **Exclusions.** A transition that stays bounded on both sides (→ D1/D2, or none).
- **Observational equivalence.** The pre-ignition bounded regime can look benign; critical slowing
  down (rising AC(1)+variance) is the model-free early-warning candidate (Q-2026-003).
- **Instance.** `validated-instance` — **Ponzi ignition** (crunch, CYB-19); the **impairment→premium
  elasticity ε** (contagion, CYB-23, Engine-1 threshold); the **Fisher φ vs markup-defense α_p**
  boundary (CYB-30) — genuine debt-deflation ignites *only* as the stabilizer α_p→0, the cleanest
  statement that the threshold is set by the stabilizer, not the loop.

## E. Escape / unbounded classes (no invariant bounded set)

### E1 — Hyperinflationary runaway (nominal escape, upward)
- **Defining property.** The price level diverges (`log P → +∞`) via a self-reinforcing
  premium/cost or credit-quantity spiral; secular, not a bounded swing.
- **Diagnostic.** Unbounded, monotone-secular `log P`; the driving loop identified; distinguished
  from a bounded high-inflation grind by the secular test.
- **Instance.** `validated-instance` — **contagion Engine 1 (CYB-23)**: impaired-rentier risk
  premium → dearer credit → more Ponzi → hyperinflationary collapse. (Cf. Q-2026-002: hyperinflation
  as *escape*, not a high-inflation equilibrium.)

### E2 — Debt-deflation runaway (real-burden escape; nominal accounting exact)
- **Defining property.** The **real** debt burden diverges (`D/P → ∞`, `P → 0`) via Fisher's
  "the more they pay, the more they owe," while the **nominal** capital-account identity stays
  exact (it is P-independent). Escape is a real-burden phenomenon, not an accounting failure.
- **Diagnostic.** Unbounded `D/P`, `P → 0`; conservation residual at machine precision throughout
  (the SFC signature that separates a real runaway from a numerical blow-up).
- **Exclusions.** A bounded (if depressed) limit cycle floored by the markup-defense (→ B1); reject
  by the secular / D/P-blowup test. This exclusion is load-bearing: **it is the mistake the
  first-cut Phase 2b made** (a −25%/step swing detector misread a bounded cycle as this class).
- **Observational equivalence.** E1 and E2 share **one** distress signal and point in **opposite**
  sign; which one fires is set by the stabilizer balance (D3) — a headline taxonomy fact, not a
  contradiction.
- **Instance.** `validated-instance` — **Fisher Phase 2b (CYB-30)**, on the α_p→0 edge; conservation
  holds to 1e-16 through `D/P: 1 → 1.4×10⁶`.

### E3 — Bounded grind / choke (bounded, pathological, no cure)
- **Defining property.** A bounded attractor that is neither healthy rest (A1) nor a clean cycle
  (B1): the system is held from escape but grinds at a pathological floor it cannot leave without a
  structural change.
- **Diagnostic.** Bounded trajectory pinned above/below a floor; the binding constraint identified;
  removing/relaxing it (a *cure*) changes the floor.
- **Instance.** `validated-instance` — the **Minsky crunch Phase 1 (CYB-19)**: the deleveraging
  cascade *bounds without curing*, choking to a ~12% grind floor; default (CYB-23) is the structural
  event that can cure it — or, via impairment, tip it to E1.

## F. Meta-class

### F1 — Observationally-equivalent / unresolved
- **Defining property.** Finite, noisy, non-stationary observation cannot separate two or more
  candidate classes at the stated evidence threshold.
- **Diagnostic (honest output).** Report the **equivalence set** or explicit non-classification —
  never false precision (principles: "the honest output is an equivalence set"). This is a
  first-class result, not a failure (Q-2026-006).

---

## Worked instances already in hand (the "what's next is partly already here" table)

| Class | What it is | Instance | Ticket | Repro level reached |
|---|---|---|---|---|
| A2 | structurally non-hyperbolic equilibrium | conserved 3-tier chain | CYB-2/4 | numerical; formal gated (CYB-13) |
| B1 | bounded (deflationary) limit cycle | Fisher on markup-defense | CYB-30 | structural (α_p, φ sweep) |
| C1 | coexisting attractors, hysteresis | finite-amplitude turbulence | CYB-2/4 | numerical |
| D1 | local bifurcation — **rejected** here | spectrum never crosses | CYB-2/4 | numerical (negative result) |
| D2 | global border-collision | cycle border-collision | CYB-2/4 | numerical; formal gated |
| D3 | threshold ignition | Ponzi / ε / φ-vs-α_p | CYB-19/23/30 | structural |
| E1 | nominal (hyperinflation) escape | credit-quantity contagion | CYB-23 | structural |
| E2 | real-burden (debt-deflation) escape | Fisher at α_p→0 | CYB-30 | structural |
| E3 | bounded grind / choke | Minsky crunch | CYB-19 | structural |

The debt-dynamics rows (B1, D3, E1, E2, E3) are one coherent story on a **single** substrate — a
distress signal that, depending on the stabilizer balance, floors into a cycle (B1), ignites past a
threshold (D3), and escapes either upward in nominal terms (E1) or downward in real terms (E2). That
is the artifact to put in front of a Minsky/Keen-orbit reader: not a claim to have *reproduced*
debt-deflation, but a **map of the classes a debt economy can occupy and the borders between them**,
each with a reproducible signature and an exact balance sheet.

## Candidate defining dimensions (the axes a class is cut along)

State variables / observables · bounded vs unbounded · stability & basin structure · endogenous vs
exogenous regime change · sensitivity to initial conditions & parameters · contact with switching
manifolds · local vs global bifurcation mechanism · empirical signatures & falsifiability.

## Open issues

- The same observed series may fit multiple mechanisms (Q-2026-001, Q-2026-006): a class must
  separate **mathematical behavior** from **measurement artifact** from **historical narrative**.
- Class assignment from short macro data is the hard part; the [wind-tunnel method](phase-space-macroeconomics.md)
  (model-based indirection, data as calibration + out-of-sample referee) is the intended escape
  from reading Lyapunov exponents off one series.
- Which distinctions survive high-dimensional nonsmooth slow–fast systems is gated on the same math
  as D2/CYB-13.

## Next steps

1. **Version this registry.** Freeze v0.1 (this note); each future edit is a numbered revision with
   a dated rationale, so class definitions have provenance the way the code does.
2. **A standard diagnostic report** per class: inputs, transient handling, numerical checks,
   uncertainty, sensitivity, the class decision, and the failure conditions that would reject it.
3. **Self-test each diagnostic** on a closed-form/benchmark system with a known class before
   trusting it on the substrate (logistic → Goodwin → Goodwin–Keen → the coupled SFC system).
4. **Pre-register** one signature set + one decision rule before the first empirical validation
   portfolio (natural-experiment portfolio; withheld countries/episodes).
5. Fill the honest gaps: instantiate **B2 (torus)** or record why the substrate does not produce it.

## Related

[Taxonomy principles](taxonomy-principles.md) · [Phase-Space Macroeconomics](phase-space-macroeconomics.md) ·
[Parameterization and control structure](parameterization-and-control-structure.md) ·
[Natural-experiment portfolio](natural-experiment-portfolio.md) · [Inflation](inflation.md) ·
[Hyperinflation](hyperinflation.md) · [Open questions](../../indexes/questions.md).
Canonical results linked: CYB-2/4 (chaos, `src/chaos/`, `docs/outreach/`), CYB-19 (`src/crunch/`),
CYB-23 (`src/contagion/`), CYB-30 (`src/fisher/`).

## Provenance

Working idea from the Chaotic Economic Models conversation
(`../../conversations/2026/chaotic-economic-models/`, 2026-08-03). Registry v0.1 populated
2026-09-05 (Claude Code) by reading the qualitative behavior back out of the **validated** CYB
modules and organizing it under the [principles](taxonomy-principles.md). A hypothesis-status
registry to attack and revise, not an established classification — the *instances* are validated at
the repro levels stated; the *taxonomy* is a frame under test.
