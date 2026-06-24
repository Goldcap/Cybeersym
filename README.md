# Wind Tunnel

*An agent-based, stock-flow-consistent simulation framework for testing **structural** hypotheses in macroeconomics — beginning with inflation.*

**Status:** v0.1 — problem statement & theoretical commitments. Not yet a model. A statement of intent precise enough to be wrong.

> *Working title. The metaphor is the spec: this is not a crystal ball that predicts the future, it is a wind tunnel that shows you the structural response to a shock you supply. A wind tunnel that cannot forecast storms is still how you learn whether the bridge falls down.*

---

## 1. The problem

The headline inflation rate is a single scalar laundering two realities it is structurally built to hide:

- **A sectoral reality.** Inflation is almost never general. It is eggs, lumber, used cars, semiconductors — specific clogs in specific supply pipes — averaged into one number that is then treated as if one lever (the interest rate) should address it.
- **A distributional reality.** "5% inflation" may be 9% for the bottom income decile (whose spending is weighted toward inelastic staples) and 2% for the top. The aggregate index erases the regressive incidence of a supply-driven price shock.

The two dominant tool-kits cannot see either reality:

- **Econometrics** is curve-fitting disciplined by historical data. It can tell you what *correlated*; it cannot tell you what happens if you do something never done before, because there is no data for the thing that has not happened. It is a rear-view mirror told the road is straight — and the [Lucas Critique](#citations) is the field's own admission that the estimated relationships change when the policy regime does.
- **DSGE / representative-agent models** have no sectors, no bottlenecks, no balance-sheet plumbing that can clog in one place while running dry in another. They therefore *cannot represent* supply-driven inflation as anything but an exogenous "cost-push shock" — an intruder relabeled, the same move Real Business Cycle theory makes when it redefines a recession as an optimal response to a technology shock.

The consequence: the **Modern Monetary Theory** account of inflation — *nominal demand meeting real, sectoral resource constraints* — is inherently disaggregated, and is therefore **unmodellable in the dominant formalism**. There exists no substrate on which it can be made to either reproduce real price dynamics or fail to. This project builds that substrate.

## 2. The wager

The classical objection to disaggregated simulation — and to economic planning generally — was the **calculation problem** (Hayek): no central process can gather and compute dispersed local knowledge fast enough. That was a *technological* constraint, not a law of nature, and it has measurably weakened. Amazon and Walmart run continent-scale planned allocation internally, with no internal price system, and it works. The calculation objection is spent.

What remains is **not** calculation but **validation**: an agent-based model is *too* free. The space of models that *look* plausible vastly exceeds the space that is *true*. The binding discipline of this project is therefore out-of-sample empirical validation — and that is where the synthesis lives:

**The simulation provides what regression cannot — mechanism and counterfactual. Statistics provides what simulation cannot — the cold, data-grounded check that the wind tunnel's airflow matches the real sky. Econometrics is not the engine. It is the referee.**

## 3. Theoretical commitments

1. **Agent-based / bottom-up.** Aggregate behavior *emerges* from heterogeneous local agents. Crises are endogenous (Minsky), not injected as exogenous shocks.
2. **Stock-flow consistent by construction.** A double-entry invariant (Godley) is asserted every tick: every flow has a source and a sink; all stocks reconcile; **money cannot leak**. The simulation halts if the books do not balance. This single constraint is what separates a model from a plausible lie, and it operationalizes the MMT insistence that money is not a veil over barter.
3. **Endogenous, reflexive preferences.** Wants are socially coupled and shift in response to provisioning and to other agents' behavior (fads, runs, keeping-up-with-the-Joneses). This is non-negotiable: stable exogenous preferences would *assume the conclusion* and rig the planning question. The model must test whether a feedback-driven allocator can stay ahead of a preference landscape that moves *because* it is being allocated to.
4. **Real supply capacity.** Finite, lagged, sticky inventory; replenishment lead times; an upstream input that can shock. **Inflation is an output, not a parameter** — prices rise in a category exactly when local demand outruns the replenishment rate faster than the chain can respond.
5. **Income heterogeneity + Engel-curve consumption.** Poorer agents spend a larger share on inelastic staples, so *distributional inflation* — the wedge between top-decile and bottom-decile experienced inflation — emerges as an observable rather than an assumption.
6. **Two measures of inflation, by design.** Compute both a *simulated CPI* (with substitution/hedonic machinery, calibrated to the official artifact) **and** a *true cost-of-maintaining-welfare* from agents' actual consumption. The **gap between them is a finding**, not an error.

## 4. First target: eggs

A single perishable staple. Inelastic demand (~−0.1). Real shelf life, real expenditure-survey income shares, real price history. The validation test: inject a supply shock and check whether the model reproduces the *shape* of a real egg-price episode **it was not fit to**.

If a stock-flow-consistent ABM reproduces a real egg-price shock from mechanism alone, the architecture has earned its first receipt — and the rest of this document stops being a manifesto and becomes documentation of a thing that runs.

> **Methodological commitment (real vs. abstract).** Seed with **real commodities as fixtures**, against a **general schema** (`Good(shelf_life, elasticity, income_share, lead_time, …)`). Real stuff brings bundled validation data and constrains the degrees of freedom that otherwise produce a beautiful lie; the general schema keeps eggs from being hardcoded into the bones, so lumber, used cars, or an abstract control good can be swapped in later. We do not choose between real and abstract — real is the first fixture; abstract generality is the architecture.

## 5. Price formation: the one open fork

The single design decision that the economics — not the engineering — must settle: **how do prices form?**

- **(A) Markup-over-replacement-cost, inventory-adjusted (sticky).** Stores post prices as a margin over replacement cost and nudge them as inventory runs hot or cold. Realistic, sticky, MMT-friendly.
- **(B) Market-clearing each tick.** Cleaner, more neoclassical, easier to validate, less true.

*Current lean: (A). To be resolved before first build.*

---

## Citations

- Hayek, F. A. (1945). "The Use of Knowledge in Society." *American Economic Review.* — the calculation/knowledge problem.
- Beer, S. *Brain of the Firm*; Project **Cybersyn** (Chile, 1971–73). — cybernetic planning; the road not taken.
- Godley, W. & Lavoie, M. (2007). *Monetary Economics.* — stock-flow-consistent modelling; the Godley table.
- Minsky, H. (1992). "The Financial Instability Hypothesis." Levy Institute WP 74.
- Keen, S. *Debunking Economics*; **Minsky / Ravel** software. — endogenous financial instability; double-entry dynamics.
- Farmer, J. D. & Foley, D. (2009). "The economy needs agent-based modelling." *Nature* 460. — the methodological case.
- Phillips, L. & Rozworski, M. (2019). *The People's Republic of Walmart.* — existing large-scale private planning as feasibility proof.
- Wray, L. R. (2012). *Modern Money Theory*; Mitchell, Wray & Watts (2019). *Macroeconomics.* — MMT; inflation as real-resource constraint.
- Lucas, R. (1976). "Econometric Policy Evaluation: A Critique." — why estimated coefficients aren't structural constants.
- Fisher, M. (2009). *Capitalist Realism.* — why the alternative is permitted in the journals and quarantined from policy.
- Varoufakis, Y. (2023). *Technofeudalism.* — cloud rent; algorithmic centralized allocation in the wild.

---

*v0.1 — written to be attacked. Every section above is a claim that the eggs build can falsify.*
