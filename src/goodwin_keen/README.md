# Goodwin–Keen — the classifier arc's instrument self-test rung ("the hydrogen atom")

> **Verdict: our `src/chaos/` diagnostics (`linearize` + `lyapunov`) recover the KNOWN answers of a
> benchmark whose classes are analytically settled — so they are trusted before we point them at the
> coupled SFC substrate.** (The 3rd instrument, the bifurcation sweeper, is self-tested in its own
> module on the logistic cascade; this rung exercises the two its self-tests require.) This is the
> macro-dynamics analogue of the chaos suite's logistic λ=ln2 check, and it is **Steve Keen's own
> model**, so it doubles as the concrete debt-dynamics artifact.

The [taxonomy principles](../../research/notes/concepts/taxonomy-principles.md) (Next-step 3) require
every diagnostic to be self-tested on a benchmark with a known class before the substrate. The
[registry](../../research/notes/concepts/taxonomy.md) names the classes. This module instantiates
several of them against ground truth and checks the instruments read them correctly.

```bash
cd src/goodwin_keen
python3 run_v0.py     # nested → conservation → eigenvalues → Lyapunov → Keen bistability → determinism
```

## The model

State `s = [ω, λ, d]` — wage share, employment rate, debt ratio `D/Y`.

```
π  = 1 − ω − r·d                 g  = κ(π)/ν − δ
ω̇ = ω·(φ(λ) − α)                 λ̇ = λ·(g − α − β)                ḋ = κ(π) − π − d·g
φ(λ) = −γ + ρλ (linear Phillips)   κ(π) = π (Goodwin)  |  bounded sigmoid (Keen)
```

**Goodwin** (`keen=False`, `r=δ=0`, `d≡0`) is the classic 2-D predator–prey system — a
*conservative centre*. **Keen** adds debt and a bounded investment appetite: a stable "good"
equilibrium that coexists with a debt-deflationary breakdown.

## What the instruments recover (all from `run_v0.py`)

| # | Self-test | Result | Known answer |
|---|---|---|---|
| 0 | nesting (regression guard) | max\|Δ(ω,λ,d)\| = **0.0** | Keen(κ=id,r=δ=0,d₀=0) ≡ Goodwin, byte-exact by construction (same `_rhs` at d=0) |
| 1 | conservation | worst \|ΔH\| = **4.4e-14** | Lotka–Volterra invariant H is constant (on a real ~19% orbit, not the fixed point) |
| 2 | eigenvalues (`jacobian`/`eigs`) | \|μ\| = **1.000000**, Ω = **0.3602** | centre; Ω = √(A·C) = **0.3602**; 3rd (real) d-eig ≈ 0.9996 contracts |
| 3 | Lyapunov (`largest_lyapunov`) | λ = **−0.00000**/step | conservative centre → 0 (vs logistic ln2) |
| 4 | Keen bistability | good eq stable (\|μ\|<1); d₀* = **9.9 → 3.2** as r: 0.02→0.05 | stable good eq + breakdown basin; r shrinks it |
| 5 | determinism | **byte-identical** | σ=0 |

![Goodwin centre](figures/cybeersym_goodwin_keen_v0_goodwin_centre.png)

*The larger orbits reach ω, λ > 1 (wage share / employment above 100%) — illustrative Lotka–Volterra
math orbits, not economically bounded. This is a mathematical benchmark for the instruments, not an
economic claim (see "not empirical" below).*

## Mapping onto the taxonomy registry (the point of the rung)

- **A2 — structurally non-hyperbolic equilibrium.** Goodwin's equilibrium is a *centre*: the
  (ω,λ) Jacobian has zero trace **for any** linear-Phillips config, so the continuous eigenvalues
  are pure-imaginary and `|μ|=1` (marginal, ∀ parameters — exact for the continuous centre; the
  finite-difference RK4 *map* our `jacobian`/`eigs` see returns 1.0000005, i.e. |μ|=1 to 6 digits).
  The conserved `H` is the reason — the same conservation-⇒-non-hyperbolic story as the chaos core
  (CYB-2/4), one dimension down.
- **B1 — bounded limit cycle.** The closed orbits around the centre (the figure); largest Lyapunov
  ≈ 0 confirms neutral stability (neither the chaotic λ>0 nor the damped λ<0 of the logistic
  self-tests).
- **A1 — stable equilibrium.** Keen's good equilibrium is a genuine (if slow: e-folding ~108 time
  units) spiral sink, `|μ|<1` — recovered by `fixed_point_newton` + `eigs`.
- **C1 → E — bistability to escape.** A debt-deflationary breakdown basin (d→∞, ω→0, λ→0)
  coexists with the good basin; **initial leverage decides survival**, and a higher interest rate
  **shrinks the good basin** (d₀* falls). Crucially the breakdown is reached by crossing a
  finite-amplitude **basin boundary — a *global* event, not a local eigenvalue crossing** — the
  same distinction (D2 global vs D1 local) the taxonomy draws and the chaos core exhibits.

![Keen bistability](figures/cybeersym_goodwin_keen_v0_keen_breakdown.png)

## Honest notes / scope

- **Minimal, not canonical-Keen.** The linear Phillips curve makes the (ω,λ) block a structural
  centre, so this Keen good equilibrium is only *weakly* damped and its debt-deflation is a
  basin/global phenomenon rather than a local Hopf. A convex Phillips curve and an output-gap
  investment term (the natural v1) would give a stronger focus and richer local structure — but
  they are not needed for the instrument self-test, which is this module's whole job.
- **Not empirical.** This is a benchmark with analytic answers (structural reproducibility), not a
  claim about any real economy. Empirical validation is the withheld-episode work still ahead.
- **Entry rung only.** Passing here licenses the instruments for the next rung — the coupled,
  conserved SFC substrate (CYB-26…29 territory), where the classes are *not* known in advance.

## Files

- `model.py` — `GKParams`; the RK4 map `gk_step` (the `StepFn` the chaos instruments consume); the
  independent 2-D Goodwin step (nesting); `conserved_H`; analytic `goodwin_equilibrium` /
  `goodwin_frequency`.
- `run_v0.py` — the six self-tests + 2 figures; loads `../chaos/{linearize,lyapunov}.py` unchanged
  (read-only). (The bifurcation sweeper is self-tested in its own module — the logistic cascade.)
- `figures/` — the Goodwin centre (closed orbits on H); the Keen (r, d₀) basin + survival-vs-breakdown.

## Anchors

Goodwin (1967, the growth cycle). Keen (1995, *Finance and economic breakdown* — the Minsky debt
extension). Lotka–Volterra (the conserved centre). Instruments: `src/chaos/` (CYB-2/4); the taxonomy
registry (`research/notes/concepts/taxonomy.md`). Descriptive only — no policy/normative content.
