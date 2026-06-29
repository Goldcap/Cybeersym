# Chaos — v0 (standalone)

CYB-1 proved **amplification** — a stationary demand blip rings *louder* up the
chain (linear, bounded). Amplification is not chaos. This module asks the sharper,
*measurable* question and answers it: does the same conserved 3-tier supply chain,
given a realistic **nonlinear** ordering rule, generate **deterministic chaos**
endogenously — bounded aperiodic trajectories with **sensitive dependence on
initial conditions** and a **positive largest Lyapunov exponent** — as one
behavioural parameter varies?

It does. **This is measured chaos, not complication.** A complicated model
producing wiggly output proves nothing; chaos is a specific claim, defined by
λ > 0 on a bounded attractor, and it is *measured* here with an instrument that is
itself validated against a map of known exponent first.

```bash
cd src/chaos
python3 lyapunov.py      # instrument self-test: logistic r=4 -> λ = ln 2
python3 bifurcation.py   # instrument self-test: logistic period-doubling cascade
python3 run_v0.py        # the supply-chain result + the three figures
```

## The nonlinearity (the chaos generator)

CYB-1's near-linear order-up-to rule is replaced by the documented
**anchoring-and-adjustment** ordering heuristic (Sterman 1989), per tier each step:

```
D_hat   <- D_hat + θ·(received - D_hat)              # adaptive demand forecast
S       =  inventory - backlog                        # current NET stock
SL      =  on_order                                   # current supply line (in pipeline)
SL_star =  L · D_hat                                  # desired supply line
order   =  max(0, D_hat + a_S·(S_star - S) + a_SL·(SL_star - SL))
```

The behavioural control parameter is the **supply-line weight**

```
β = a_SL / a_S
```

* **β = 1** — the decision-maker fully credits orders already in the pipeline;
  does not re-order for gaps already on the way → **stable**.
* **β < 1** — **supply-line underweighting**, the documented human bias (Sterman's
  subjects systematically ignored the pipeline): the tier re-orders for gaps it
  has *already addressed*, over-corrects, oscillates. As β falls → **chaos**.

The `max(0, ·)` (orders can't be negative) is a genuine nonlinearity; combined
with the lead-time delays and the feedback it is what makes chaos *possible*. A
purely linear rule can only decay or blow up — it cannot sustain a bounded
aperiodic attractor.

**β is THE knob.** At high β even an aggressive inventory-adjustment `a_S=1.3`
stays stable; `a_S` alone does not destabilize the chain. Underweighting the
supply line is what tips it over — the behavioural story, made measurable.

## The result

`a_S=0.7, L=3, θ=0.25`, demand noise **OFF** (σ=0), perturbed off the fixed point
by a one-time initial-condition offset. Sweep β downward (← stable, → more
underweighting):

![route to chaos](figures/cybeersym_chaos_v0_bifurcation_lyapunov.png)

* **Top — bifurcation diagram.** A single fixed point (net stock ≈ 135) holds for
  β ≳ 0.30, loses stability near β ≈ 0.29 into a narrow band, and broadens into a
  **chaotic smear** as β falls. The attractor stays **bounded** the whole way (it
  does not run away).
* **Bottom — the load-bearing measurement.** The largest Lyapunov exponent is
  **λ ≈ 0 in the stable/quasiperiodic regime and turns robustly positive
  (λ up to +0.054 nats/step) below β ≈ 0.26.** The sign change *locates* the onset
  of chaos. Chaos is *defined* by this, not by the picture looking busy.

![sensitive dependence](figures/cybeersym_chaos_v0_sensitive_dependence.png)

* **Sensitive dependence (the butterfly).** Two runs whose initial conditions
  differ by ε = 1e-6: in the chaotic regime (β=0.15) the gap **grows
  exponentially** (×10⁵ over ~200 steps — a straight line on the log axis, the
  visual signature of λ>0); in the stable regime (β=0.32) the same gap **decays**
  back toward the fixed point (→ 1e-11). Same model, opposite verdict, set only by β.

## The route we actually measured (a spec correction the model earned)

The spec's criterion 1 predicted a *pristine logistic-style period-doubling
cascade* (fixed point → period-2 → period-4 → … → chaos). The model refuted the
"pristine" part and produced something richer and **more faithful to the
literature**: a **supercritical Hopf → quasiperiodic → chaos** transition. As β
crosses onset the fixed-point amplitude grows *continuously from zero* with
**λ ≈ 0** (the marginal signature of a Hopf bifurcation to a two-frequency torus,
not a flip to period-2), and only as the torus breaks down — via frequency-locking
and embedded period-doubled windows — does λ lift clearly positive into chaos.

This is exactly what **Mosekilde & Larsen (1988)** report for the beer game:
quasiperiodicity, torus dynamics, frequency-locking *and* period-doubling — a rich
bifurcation structure, not a single clean cascade. Period-doubled and periodic
windows *do* appear (e.g. period-2/4 bands near onset, and a narrow periodic window
embedded in the chaotic band — the supply-chain analogue of the logistic period-3
window); they are not the *global* route. Reported as the finding, per the
project's method — same discipline as CYB-1's "information sharing suppresses but
does not flatten": let the data refute the spec, and the correction is the result.

The **load-bearing claim is unaffected**: bounded + aperiodic + λ>0 + deterministic
+ conserved = deterministic chaos, measured. The route to it is just more
interesting than the first framing.

## Why it's real and not a bug (the validations)

1. **The instrument is validated before its verdict is trusted** (the discipline
   guard, mirroring CYB-1's frozen-forecast regression). The largest-Lyapunov
   estimator reads the **logistic map x→r·x·(1−x) at r=4 as λ = 0.69315**, matching
   the exact analytic value **ln 2 = 0.69315** to five digits, and returns λ<0 in
   periodic windows. The bifurcation sweeper reproduces the textbook logistic
   cascade (1 → 2 → smear). An instrument that cannot read a known chaotic map is
   not allowed to certify an unknown one.
2. **Determinism (chaos ≠ noise).** Demand noise is OFF; the step map is a pure
   function of the state vector. Identical initial conditions → **byte-identical
   trajectory**. The aperiodicity is endogenous, generated by the dynamics — *that
   is why the noise is off*: with noise on you cannot tell chaos from randomness.
3. **Conservation holds in the chaotic regime.** Goods are created only by the
   external supplier, destroyed only by consumption; the invariant
   `injected − consumed == Σ inventories + Σ in-transit` holds to **4.9e-15**
   (relative) every step *while the trajectory is unpredictable*. Chaos rides on a
   conserved substrate — the numerical-weather-prediction analogy: the trajectory
   is unpredictable, the mass is conserved. A conservation break would be a bug,
   never "chaos".
4. **Boundedness is checked, not assumed.** A positive λ on an *unbounded* (blowing
   up) trajectory is not chaos. The deep-underweighting corner (β→0 at aggressive
   a_S) does run away to ±thousands; the reported regime (a_S=0.7) stays bounded —
   amplitude stabilizes, growth ratio ≈ 1 — so its λ>0 certifies genuine chaos.

## The instruments (the real, reusable deliverable)

These are model-agnostic on purpose — every future mechanism (conflict, the full
economy) gets run through the *same* tooling. They operate on a `step(state)→state`
callable and a flat state vector, knowing nothing about supply chains.

* **`lyapunov.py`** — largest Lyapunov exponent, Benettin two-trajectory method:
  evolve a reference + a twin a tiny distance d0 away; each step accumulate
  `log(d/d0)` and renormalize the twin back to d0 along the separation direction
  (so it keeps sampling the *local* stretching rate). `λ = mean(log(d/d0))` after a
  discarded transient. Renormalizing along the separation vector converges to the
  *largest* exponent.
* **`bifurcation.py`** — for each control value: run long, discard the transient
  (we want the attractor, not the approach), record the asymptotic local maxima of
  one observable; scatter (control, samples). period-1 → one point; period-2 → two;
  chaos → a vertical smear.
* **`model.py`** — the CYB-1 conserved 3-tier flow with the anchoring-and-adjustment
  ordering rule and deterministic demand. Exposes `get_state` / `set_state` /
  `step_vector` so the instruments can drive it as a pure map.
* **`run_v0.py`** — instrument self-test → determinism+conservation → bifurcation →
  λ-vs-β → sensitive dependence → the two figures.

## Literature

* **Sterman, J. D. (1989), *Modeling managerial behavior: misperceptions of
  feedback in a dynamic decision making experiment*, Management Science 35(3):
  321–339.** The anchoring-and-adjustment ordering rule and the empirical finding
  that decision-makers **underweight the supply line** — the β<1 bias that drives
  the instability here.
* **Mosekilde, E. & Larsen, E. R. (1988), *Deterministic chaos in the beer
  production–distribution model*, System Dynamics Review 4(1–2): 131–147.** Showed
  the beer game routes to deterministic chaos; documents the **quasiperiodic /
  torus / frequency-locking** structure we reproduce, not merely a clean cascade.

## Scope (v0 deliberately excludes)

Deterministic demand only (noise OFF — chaos must be endogenous; the stochastic
CYB-1 bullwhip is a *separate regime*, not to be conflated). One control parameter
(β) for the primary diagram; the β×a_S map is a later nicety. Still **3 tiers**,
still the **conserved physical flow** from CYB-1 — only the ordering rule changed.
The instruments are built general so the next mechanism reuses them unchanged.
