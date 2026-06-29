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
  separate pillar. It is not hypothetical here: the egg model's unfittable *saturation*
  at deep deficits was the +2,040% import surge acting as a buffer that capped the
  price. Every transmission channel has a corresponding absorption that can null it.

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
experiment. The build order follows the table: isolate
**recursion** first (bullwhip — clean, measured, equilibrium-impossible), prove the
instrument detects and characterizes it, *then* add **conflict** (a wage-setting layer)
and see if it amplifies, then the sustaining channels (**reflexivity**, then
**accommodation**). One mechanism at a time, each validated before the next — the same
discipline that built the egg model, never the whole tangle at once.

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
