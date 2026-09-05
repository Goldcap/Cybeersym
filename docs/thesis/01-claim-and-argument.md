# 01 — The claim, and the argument for it

*Part of the [Cybeersym thesis set](00-index.md). The single-file long-form of this argument is
[`THESIS.md`](../../THESIS.md); this doc is its navigable, dual (defense + open-threads) distillation.
Everything here is bounded by [05 — limits & honesty](05-limits-and-honesty.md).*

## The one-sentence claim

**Cybeersym is a wind tunnel, not a crystal ball:** an agent-based, stock-flow-consistent simulation
for testing whether a *structural* hypothesis about inflation survives contact with real data — where
econometrics is the **referee** (out-of-sample validation), never the engine. The longer-range aim
is a **regime / domain-of-validity classifier**: not "where is the equilibrium," but "what dynamical
class is this economy in, and how close does it sit to a border."

## What the claim is, precisely

- **Structural, not reduced-form.** We model behavioural rules (how a firm raises price under
  scarcity, how a household cuts per point of debt) whose composition *produces* the aggregate
  relationships — rather than fitting the aggregates directly. Fitting hand-drawn macro shapes was
  always the "beautiful lie" the project's own history keeps refuting.
- **Mechanism validated out-of-sample, then counterfactual — never point-forecast.** The licence to
  say "reflects real-world dynamics" comes only from reproducing episodes/facts *not* used in
  calibration. (Done, narrowly: the 2024‑25 egg episode's peak *timing* from a frozen calibration it
  was never fit to — an **empirical** result, one commodity; see [05](05-limits-and-honesty.md).)
- **Conservation-disciplined.** Money and goods are conserved to machine precision (< 1e‑10); every
  composed module reproduces its parent byte-exact. This is the rigor that separates the work from an
  untestable parameter zoo.

## The argument in four moves

1. **Equilibrium methods solve *for* a fixed point; economies have trajectories, attractors, borders.**
   The phenomena that matter for inflation — propagation, amplification, regime switches — are
   emergent and out-of-equilibrium, and are excluded from equilibrium models as "exogenous shocks."
   Here they are endogenous behaviours of the structure. (The mainstream head-to-head, honestly
   bounded, is [04](04-augmenting-the-discipline.md).)
2. **A conserved, stock-flow-consistent substrate makes that rigorous, not decorative.** The
   accounting can't lie; the chaos rides on a conserved ledger, exactly as numerical weather
   prediction rides on conservation of mass/energy.
3. **The commodity is eggs, on purpose.** A validated working example (the 2022‑23 and 2024‑25 HPAI
   price spikes) on *real* series (FRED, USDA/NASS) keeps the method honest before it is pointed at
   harder targets.
4. **The channels compose.** Conflict → accommodation → crunch → contagion → Fisher (CYB‑6/17/19/23/30)
   are hosted on one conserved substrate, each nesting the previous byte-exact — a *class* of results
   about how a debt economy behaves, at **structural** reproducibility (see [02](02-method.md),
   [03](03-taxonomy-and-regimes.md)).

## What the claim is **not**

Not predictive; not "inflation *is* a supply constraint"; not a policy verdict; not a demonstration
that we out-forecast anyone. The full disclaimer set is [05](05-limits-and-honesty.md), and it is not
optional reading — it is where the claim's boundary lives.

## Open threads

- **The single most load-bearing bet is that structure-first buys something a reduced form can't** —
  argued in [04](04-augmenting-the-discipline.md), but only *demonstrated* once the empirical program
  in [08](08-future-work-roadmap.md) runs. Until then this is a representational claim.
- **Eggs are narrow.** One commodity, two episodes. Whether the method generalises is the open
  empirical question, not a settled result.

---

*Sources (linked, not copied): [`THESIS.md`](../../THESIS.md) (long-form); `CHANGELOG.md` (the arc);
the module READMEs under `src/`. Support levels per [05](05-limits-and-honesty.md).*
