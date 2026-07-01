# What Cybeersym is actually claiming

This document is the conceptual statement of purpose — the *why*, separate from the
code (`README.md` for structure, `CHANGELOG.md` for the build history, `HANDOFF.md`
for the working state). If you're new here and wondering "what is this, what is it
trying to say, and how would I know if it's wrong" — this is for you.

---

## The one-sentence claim

**Inflation is a transmission phenomenon, not a single cause** — and a conserved
production network is the right instrument for modelling it, because it can host every
inflation channel at once and let data decide which dominates in which regime.

That sentence is doing careful work. Read on for what it includes and, just as
importantly, what it refuses to say.

## The argument

A supply shock in one place — avian flu culling egg-laying hens — is, by itself, a
**relative price change**, not inflation. Eggs got expensive *relative to everything
else*. That is the price system working correctly: signalling scarcity. It is not a
rising general price level.

The real question, the one most inflation talk skips, is what converts a relative-price
shock into **inflation** (a sustained rise in the *level*). A shock becomes general
inflation only if it is both **transmitted** to other prices and **sustained** rather
than reversed. Each of those has more than one channel (see the taxonomy below) — but
the headline point is structural:

So the precise thesis: **a trigger (e.g. a supply constraint) is necessary but not
sufficient; whether it becomes inflation rather than a relative-price blip is determined
by how the economy *transmits* the shock and whether it *sustains* it.** The trigger is
the part everyone argues about; the transmission-and-sustaining is the part nobody has
modelled mechanistically. This project is a transmission model. "Pushes against real
resource constraints" names the trigger and is silent on the transmission — which is
exactly the gap.

## The channels — a working taxonomy

Transmission and sustaining each split in two, giving four channels (plus a damping
dual). This is **scaffolding for deciding what to instrument next, not a periodic table
of inflation** — the boundaries blur, the channels interact, and there are almost
certainly interactions we have not named. Treat it as a map of the terrain to model one
region at a time.

**Transmission — how a local shock spreads to the general level**

- **Recursion (technical transmission).** Propagation through input-output linkages.
  Eggs feed bakeries feed restaurants; energy feeds nearly everything. A localized shock
  becomes general only if the network *transmits and amplifies* it through the pipes of
  production. Whether it propagates or dampens is a structural property of the network,
  and it is measurable. *This is the cleanest channel and the first to instrument —* it
  has no expectations confound. **Bullwhip amplification** (a 3-tier supply chain
  over-ordering from local information and lags) is its sharpest, industry-measured,
  equilibrium-impossible demonstration.

- **Conflict (social transmission).** The shock also spreads through a *fight over
  income shares*, not through pipes. When prices rise, workers seek wage catch-up to
  restore real income; firms defend or widen margins. The relative shock becomes a
  general spiral via strategic interaction — the wage-price / "sellers' inflation"
  dynamic (Rowthorn, Lavoie, Weber). This is distinct from recursion (not technical
  linkage) and from expectations (not anticipation). It connects directly to this
  repo's namesake: the **wedge measures who *bears* inflation; conflict is what happens
  when people *refuse* to bear it and shove it onto someone else.** Distribution is not
  only the *outcome* of inflation — it can be a *driver*.

**Sustaining — whether a transmitted shock persists or reverses**

- **Reflexivity / expectations (expectational sustaining).** The accommodation switch in
  agents' heads. The same propagated shock either gets *built in* (firms reprice ahead,
  workers price in catch-up, it becomes a level spiral) or stays *contained*
  (expectations anchored, treated as transitory, it washes out). 2021-23 is the natural
  experiment: the shock propagated but expectations mostly held, so it did not spiral
  like the 1970s. This is the channel orthodox macro leans on hardest — and it is real —
  but it is one of four, not the whole story. *Reflexivity is also where the
  weather-analogy breaks: unlike air parcels, agents read the forecast and act on it,
  which changes the system (the Lucas critique). Model agent adaptation as a tested
  hypothesis, never a free realism dial.*

- **Accommodation (financial sustaining).** A sustained rise in the *nominal* level must
  be *financed*. Credit and money have to expand to validate higher prices; if they do
  not, real balances fall, demand contracts, and the shock reverses itself instead of
  becoming inflation. This is the endogenous-money / MMT point (and the kernel of truth
  monetarism mangled): inflation must be *ratified* by the financial system. In a
  stock-flow-consistent model this is partly automatic (loans create deposits), but
  *whether* accommodation happens is a genuine switch, distinct from expectations.

**The damping dual**

- **Buffering / absorption.** Slack, inventories, imports, spare capacity — a shock can
  be *absorbed* rather than propagated. This is the off-switch on recursion, not a
  separate pillar. The candidate here was the egg price's apparent *saturation* at deep
  deficits — the +2,040% import surge and demand destruction at $6 eggs plausibly capping
  the price. Honestly tested, though, that curvature did **not** survive an out-of-sample
  model comparison on the full price path (CYB-14): it shows only between the two episode
  peaks and is within-noise at the path level, so the linear pricer is kept. If buffering
  bent the egg response, two episodes cannot yet resolve it — a plausible mechanism is a
  hypothesis until the data earns it. Every transmission channel still has a corresponding
  absorption that can null it; this one is noted, not claimed.

**The 2×2, at a glance**

```
                 TRANSMISSION                      SUSTAINING
            (spread to other prices)        (persist vs. reverse)
         ┌──────────────────────────┬──────────────────────────┐
technical│  RECURSION               │                          │
/financial│  input-output pipes      │  ACCOMMODATION           │
         │  (bullwhip)              │  credit/money ratifies   │
         ├──────────────────────────┼──────────────────────────┤
social   │  CONFLICT                │  REFLEXIVITY             │
/expect. │  wage-price, share fight │  expectations built in   │
         │  (the wedge as cause)    │  or anchored             │
         └──────────────────────────┴──────────────────────────┘
   damping dual (all cells): BUFFERING — slack, inventory, imports absorb the shock
```

**Why this is a roadmap, not just a list.** The convincing demonstration is never "the
model produces inflation." It is "the *same* trigger dissipates or cascades depending on
which cells are active and what state the network is in." That is the *"and when"*
question — the one orthodox framing leaves to judgment — rendered as a controllable
experiment. The build order follows the table: isolate **recursion** first (bullwhip —
clean, measured, equilibrium-impossible), prove the instrument detects and characterizes
it, *then* add **conflict** (a wage-setting layer), *then* couple the two, and only after
that reach for the sustaining channels (**reflexivity**, then **accommodation**). One
mechanism at a time, each validated before the next — the same discipline that built the
egg model, never the whole tangle at once.

Both transmission channels are now built and, as of the coupling, the "and when" is no
longer a promissory note — the same subthreshold trigger provably dissipates or ignites
depending on which cells are live. The next section is what that build taught us.

## From map to mechanism — what building the channels revealed

The taxonomy above is a map. Building its first region has begun to turn it into a
mechanism, and the discoveries came in a definite order, each riding the one
non-negotiable below all of them: the conserved ledger. That ledger is not bookkeeping
hygiene. It is load-bearing, and the first thing it taught us is that a stock-flow-consistent
economy *does not lose stability the way the textbook says* — its equilibrium is
non-hyperbolic by construction, so its instabilities are global rather than local (the
conservation result, CYB-4, detailed under "Why a conserved network" below). Everything
that follows inherits that fact.

**The two transmission channels are dynamical opposites.** Built as isolated modules,
recursion and conflict did not turn out to be two flavors of the same instability — they
destabilize orthogonal halves of the economy. Recursion — the input-output supply chain
(CYB-1/2) — destabilizes the **real** side: given the documented supply-line-underweighting
bias it generates bounded, deterministic *quantity* chaos while goods stay conserved to
machine precision, and prices are not yet even in the story. Conflict — the wage-price
share fight (CYB-6, `015f6e7`) — destabilizes the **nominal** side: the real distribution
settles to a *stable node* (the realized wage share sits still, strictly between what
workers and firms each claim) while the price *level* runs away, a sustained spiral whose
rate matches the Rowthorn–Lavoie conflicting-claims closed form, `π* = (α_w·α_p/(α_w+α_p))·g`,
to machine precision. Same conserved-ledger discipline, opposite dynamical character. That
is a structural dichotomy, not two labels on a list — and it is the fact the coupling later
turns to account.

**Every channel rides a real economic constraint as its switching manifold.** In each
module, the feature that generates the interesting dynamics is not a smooth nonlinearity
but a hard constraint — something agents institutionally *cannot* do — acting as a
switching border. Recursion's chaos rides order non-negativity: you cannot un-order, and
that clamp (not any smooth term) is the active border at the onset (CYB-2). Conflict's
inflationary *bias* rides downward nominal wage rigidity: strip it and the mechanism is
symmetric — inflation for a positive aspiration gap, equal-and-opposite deflation for a
negative one — and it is precisely the floor (wages don't fall) that suppresses the
deflation side, converting the symmetric law into a dissipate-below / transmit-above
*threshold* at gap zero (CYB-6). And CYB-4's non-hyperbolicity rides the conservation
clamp itself. The pattern is consistent enough to state as a claim: **the constraints ARE
the dynamical structure.** The economics is not decoration on the mathematics; the
institutional facts about what agents can't do are exactly where the mathematics lives.

**Real data grounded the egg model — and unmasked an error we hadn't seen.** While the
channels were being built, the egg foundation was pushed the other way, from model to
data, and the data returned the favor. Retiring the model's one fitted timing parameter —
the flock-replacement lag — against the real USDA-NASS monthly layer-inventory series
*improved* the peak timing with **zero** free timing parameters (CYB-7, `591b364`): the
timing had been in the flock stock all along. But the same swap exposed something the
old, apparently-good fit had hidden. The magnitude had been matched by **two canceling
~2× errors** — a synthetic flock deficit roughly twice too large, multiplied by a pricer
slope roughly half what the data demands. Feeding the real (smaller) deficit made the
undershoot visible; recalibrating the slope against it (CYB-9, `c21b2d6`) replaced the
lucky pair with two independently-correct numbers. A model with many free parameters would
have silently re-fit and buried the cancellation. The **few-meaningful-parameters-on-a-
conserved-substrate** design is exactly what let the error surface — and when we then asked
whether the residual concavity at the two peaks was real, an out-of-sample model comparison
on the full price path *declined* the extra parameter as within-noise (CYB-14). The
discipline cuts both ways: it made us fix a hidden error and it stopped us from inventing
structure the data doesn't support. Parsimony here is not an aesthetic preference; it is
the property that lets the data refute you.

**The channels compose super-additively — the payoff.** Coupling the two transmission
channels (CYB-10, `109c998`) is where the taxonomy stops being a catalog. Held apart,
neither ignites a subthreshold shock: the supply chain has no nominal channel at all, and
the conflict layer, started below its gap threshold, dissipates. Coupled through a single
link — the chain's scarcity raising firms' target margin, which widens the distributional
gap — they ignite a *sustained* wage-price spiral in a region where **neither channel alone
produces any inflation**. The emergence is not an artifact of gluing two models together:
at zero coupling the composed system reproduces each part *byte-for-byte* (the decoupling
regression), so the inflation that appears at positive coupling is genuinely a property of
the interaction, not of the plumbing. And the mechanism is sharper than "amplification." A
transient amplified shock, however large, dissipates; only recursion's **endogenous**
instability — the self-sustaining bullwhip attractor — holds the distributional gap open
long enough to ignite the spiral. Recursion doesn't merely amplify the trigger, it
**sustains** it; its bounded real chaos is a *persistent-scarcity generator*, and conflict
is the machine that converts persistent real scarcity into sustained nominal inflation. The
real chaos even leaks into the nominal path — the resulting inflation is itself aperiodic.
The taxonomy's promise — *the same trigger dissipates or cascades depending on which cells
are live* — is, in the coupled model, a measured fact rather than a hope.

**How these were found, and where the discipline stops.** None of the above was the prior
we started with. Each finding arrived as the model *refuting* a confident framing — the
chaos onset was expected to be a period-doubling cascade, then a smooth Hopf, and measured
to be a nonsmooth border-collision; the coupling was framed as shock-amplification and
measured to be endogenous sustaining; the pricer was expected to saturate and measured to
be linear. Every refutation moved the same direction — from *external* to *endogenous*,
from *local* to *global*, from *smooth* to *nonsmooth* — which is itself a result about
where the interesting structure of a conserved economy lives. The model tells us; our
priors don't. And the discipline knows its own boundary: the single genuinely hard formal
claim — rigorously classifying the global bifurcation on a ~21-dimensional, non-hyperbolic,
conserved piecewise-smooth map, where the standard normal-form reduction is not even a
theorem — is **gated for external expert review** (CYB-13), not ground out unsupervised.
The honesty firewall below is not a disclaimer bolted on at the end; it is how the work was
done.

## What this is NOT claiming (the disclaimers that keep it honest)

- **Not** "inflation IS a supply constraint." That is cost-push monocausality, the same
  error as demand-pull monocausality from the other side. Eggs are *one validated
  channel*. The framework is channel-plural by design: demand-pull, cost-push, sectoral
  propagation, and distributional conflict are all hostable on the same conserved
  substrate.
- **Not predictive. Illustrative.** A chaotic dynamical system cannot be point-forecast
  in principle (sensitive dependence). The claim is never "eggs will be $X in March."
  It is "*this* is how a shock propagates through *this* structure." Think climate
  model, not weather forecast: correct and illuminating about the dynamics, silent on
  the specific trajectory.
- **Not** a proof that economies are chaotic *because the output looks turbulent*.
  Complication is not chaos. Chaos is a specific, measurable claim (positive Lyapunov
  exponent, sensitive dependence, a characterizable attractor) and must be *measured*,
  not asserted.
- **Not** a claim that any single number (a correlation, a fitted slope) validates the
  model. See "how to evaluate," below.

## Why a conserved network, and not the standard tools

Equilibrium economics studies *fixed points* — it solves *for* the equilibrium. But an
economy has no fixed point; it has trajectories, attractors, sensitive dependence. The
choice of linear/algebraic models was not a simplification of a simple thing; it was a
retreat forced by a method (solve-for-equilibrium) that cannot represent heterogeneous
agents interacting out of equilibrium. The profession's own Sonnenschein-Mantel-Debreu
result showed rational agents do not aggregate to a well-behaved economy; the
representative-agent fix "solves" aggregation by deleting the heterogeneity that
produces the interesting dynamics.

The phenomena that matter for inflation — propagation, amplification, regime switches,
crises — are *emergent and out-of-equilibrium*. They are definitionally excluded from
equilibrium models as "exogenous shocks." Here they are endogenous behaviours of the
structure.

Two non-negotiable properties make this rigorous rather than a pretty machine:

- **Conservation.** Stock-flow consistency (Godley-Lavoie). Money and goods are
  conserved to machine precision (<1e-10). The chaos rides on a conserved substrate —
  exactly as numerical weather prediction rides on conservation of mass/energy. This is
  also where the model meets MMT: the conserved ledger *is* the issuer's balance sheet;
  money is entries on it.
- **Determinism.** Same inputs → same outputs, guarded as a property. If it breaks, that
  is a bug, not noise.

### What conservation forces — the deepest result so far (CYB-4)

The conserved network's first structural result falls straight out of the conservation
pillar above, and it is sharper than expected. Stock-flow consistency makes the
**equilibrium non-hyperbolic by construction, for every parameter value**: the conserved
supply-line quantities are *exact* left-eigenvectors of the linearized step map with
eigenvalue +1 (one per tier) — a permanent center subspace that no parameter choice
removes. The consequence generalizes beyond the toy chain: **a conserved-ledger economy
does not lose stability the textbook way.** There is no smooth local bifurcation of the
equilibrium — no eigenvalue drifting out through the unit circle as a parameter turns.
Instead the instabilities are **global**: a turbulent attractor is *born at finite
amplitude alongside* the still-stable equilibrium, and the system can jump to it. The very
rigor that makes the model honest (conservation) is what places its dynamics outside the
standard local-bifurcation toolkit — a structural claim about SFC models as a *class*, not
a quirk of one chain. (Measured, and shown inapplicable to the Nusse–Yorke normal form, in
the chaos module; see `src/chaos/` and `docs/solutions/`.)

This delivers, mechanically, a result the equilibrium tradition assumes away: **bistability
⇒ endogenous path-dependence.** Same parameters, two coexisting fates — calm equilibrium or
turbulent attractor — with *history* selecting which. Hysteresis and
anti-equilibrium-uniqueness that the model *produces* rather than postulates (a
Keynesian-flavored multiplicity, here earned from the structure).

And the ingredient is **measured, not assumed** (the empirical grounding, CYB-3): the
supply-line-underweighting bias that drives the instability is a real, near-universal human
behaviour (Sterman's mean β≈0.34, robust across thirty-five years of beer-game
experiments), and the measured bias sits right at the model's stable→turbulent edge — a
*qualitative regime correspondence*, not a fitted coincidence (the exact onset β depends on
the adjustment rate and lead time). The bias is established by others; what the model
contributes is the instability that bias *implies*. Consistent with the stance throughout:
validate the ingredients and the mechanism, stay illustrative-not-predictive, and do **not**
claim to detect chaos in macro data directly — the honesty firewall, and why that 1980s–90s
detection program failed, is documented in `docs/empirical_grounding.md`.

## How to evaluate this (the part a skeptic should hold us to)

The honest worry about any rich simulation: *with enough agents and parameters you can
produce any behaviour, so producing a plausible crash proves nothing.* Flexibility is
not validation. We accept that bar. The model earns trust only by:

1. **Out-of-sample reproduction.** Reproducing episodes / stylized facts it was *not*
   tuned on, with the *same* parameters. (Done for eggs: the 2024-25 HPAI episode was
   never fit; the model reproduced its price-peak timing with the calibration frozen.
   That, not the in-sample fit, is the result that counts.)
- 2. **Mechanism, not curve-fit.** A finding survives only if it holds across independent
   episodes for a structural reason — not because a coefficient was fit to one history.
   (The price-deficit slope is the same across both egg episodes; that consistency, not
   the fit to either alone, is the claim.)
3. **Emergent stylized facts, for the network version.** The forthcoming distributed
   model will be judged on reproducing emergent signatures it wasn't tuned to — fat
   tails in return distributions, volatility clustering, measured supply-chain bullwhip
   ratios — across regimes. Until it does, "reflects real-world dynamics" is a goal,
   not a claim.

If the model reproduces what it wasn't shown, it is illustrative science. If it only
reproduces what it was tuned to, it is a painting. The difference is the entire point,
and it is the standard this repo holds itself to.

## Lineage

Stock-flow consistency (Godley & Lavoie). Endogenous instability (Minsky; Keen's
existence proofs that crises arise from internal structure, not outside shocks).
Complexity / out-of-equilibrium economics (Santa Fe; Arthur; Farmer & Foley). Money as
balance-sheet entries (MMT — Mosler, Kelton, Mitchell, Fullwiler). Data as dispositive
(Keen: neoclassical theory lacks foundational data because the data would refute it).
Chaos modelled honestly as illustrative-not-predictive (the numerical-weather-prediction
tradition — Lorenz, ensemble forecasting).

Cybeersym aims to supply the half these traditions point at but have not built: the
**mechanistic, validated transmission model** that turns the accounting truths (which
MMT has right) into the *dynamics* (which everyone is thin on). Keen's models prove the
instability *can* arise; the aim here is to show a structurally-realistic economy
*reproduces the specific signatures* of real instability, out-of-sample. Same lineage,
next rung.
