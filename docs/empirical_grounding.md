# Empirical grounding — the behavioral foundation and field signatures

> **What this document is.** CYB-2 showed *in the mathematics* that the conserved
> 3-tier supply chain, given the documented anchoring-and-adjustment ordering rule,
> routes to deterministic chaos (bounded, aperiodic, λ>0) via a border-collision
> bifurcation. A referee's first question is the right one: *so what — is any of this
> real?* This is the answer, prepared in advance. It does **not** claim to detect
> chaos in the wild (see §3 — you can't, and we explain why). It anchors the
> *ingredients* (the behavioral bias that drives the bifurcation) and the
> *signatures* (amplification, persistent oscillation) in measured reality, and lets
> the model carry the inference. The framing this licenses: **the bias is established
> (Sterman/Croson); here is the instability the model rigorously illustrates given
> it.**
>
> This is the egg-model playbook (`THESIS.md`, "How to evaluate this") applied to the
> behavioral foundation: validate the components against data, validate the mechanism
> in the model, and keep the claim *illustrative, not predictive*.

**On verification.** Every empirical claim below is tagged against its primary
source. Tags: **[VERIFIED]** confirmed against the primary paper (or a faithful
working-paper rendering of it); **[VERIFIED-substance]** the finding is confirmed but
an exact quote was paraphrased from a paywalled body; **[needs-verification]** the
specific number/wording could not be confirmed to the source and is flagged, not
asserted. The flagged items are collected in the closing note. This is the same
discipline the egg model holds itself to — *flag what you can't verify rather than
assert it.*

---

## Section 1 — The behavioral bias is real (the keystone)

The control parameter that drives CYB-2's bifurcation, **β = supply-line weight**, is
not a modelling convenience. It is a *measured* feature of how humans manage
inventory under feedback delay — first estimated by Sterman, then shown
near-universal and robust across two decades of controlled experiments.

### Sterman (1989) — the rule and the headline number  [VERIFIED]

**Sterman, J. D. (1989). "Modeling Managerial Behavior: Misperceptions of Feedback in
a Dynamic Decision Making Experiment." *Management Science* 35(3): 321–339.**

Sterman fit an **anchoring-and-adjustment** ordering rule to the decisions of 44
subjects playing the Beer Distribution Game. The rule (his Eqs. 10–15):

```
O_t  = max(0, IO_t)
IO_t = Lᵉ_t + α_s·(S′ − S_t − β·SL_t)
```

where `Lᵉ` is an exponentially-smoothed demand anchor (smoothing parameter θ), `α_s`
is the stock-adjustment fraction, `S′` the desired stock, `SL` the supply line, and —
the load-bearing definition —

> **β = α_SL / α_s**, *"the fraction of the supply line taken into account by the
> subjects. If β = 1, the subjects fully recognize the supply line… If β = 0, orders
> placed are forgotten until they arrive."*

**Critical mapping — Sterman's (α_s, β, θ) ARE this model's (a_S, β, θ).** Our
`order = max(0, D̂ + a_S·(S* − S) + a_SL·(SL* − SL))` with `β = a_SL / a_S` is
Sterman's rule, name-for-name. **His β is our β.** This is the join that makes the
whole document load-bearing: the parameter we sweep to find chaos is the parameter he
*measured in people*.

Estimated parameters (Table 4, N = 44):

| parameter | meaning | mean | range |
|---|---|---|---|
| α_s | stock-adjustment fraction | **0.26** | 0.00 – 0.80 |
| **β** | **supply-line weight (= α_SL/α_s)** | **0.34** | 0.00 – 1.05 |
| θ | demand-anchor smoothing | 0.36 | (weakly identified; ⅔ of estimates n.s.) |

> Headline quote: *"The average value of [β] is just .34; only five subjects (11%)
> accounted for more than two-thirds of the supply line. The result is overordering
> and instability."*

So **39 of 44 subjects (89%) had β < ⅔**, against the stabilizing optimum β = 1. The
*mean* β = 0.34 is the number to remember — and §4 returns to where it lands on our
bifurcation axis.

*Precision note:* Sterman does not report a t-test count of "β significantly < 1," so
we cite the figure he *does* report (5 of 44 ≥ ⅔), not a manufactured significance
count.

### Croson & Donohue (2006) — the bias survives stripping out every operational cause  [VERIFIED]

**Croson, R. & Donohue, K. (2006). "Behavioral Causes of the Bullwhip Effect and the
Observed Value of Inventory Information." *Management Science* 52(3): 323–336.**

The control experiment. The classical (Lee et al. 1997) explanations of the bullwhip
are *operational* — order batching, price fluctuation, demand-signal forecasting,
shortage gaming. Croson & Donohue ran the 4-echelon beer game with all of them
**removed**: demand drawn from a **stationary, publicly-known** distribution
(U[0,8]), the chain **initialized at its order-up-to equilibrium**, no batching, no
price changes. The bullwhip persisted anyway.

> *"the bullwhip effect still exists when normal operational causes (e.g., batching,
> price fluctuations, demand estimation, etc.) are removed"* — and is *"explained to
> some extent by evidence that decision makers consistently underweight the supply
> line… first identified by Sterman (1989)."*

This is exactly CYB-2's deterministic-demand isolation, run in a lab: with the
operational/stochastic causes gone, the instability is **endogenous to the decision
rule**. Underweighting incidence in their data: **44/44 (100%)** of subjects
underweighted under known/stationary demand, **42/44 (~95%)** under the
inventory-information-sharing treatment (N = 44 per study).

*Caveat carried into the doc:* describe their demand as **stationary and
publicly-known (U[0,8])**, *not* "constant" — it was stochastic-but-stationary with
the chain started at steady state.

> **On the widely-quoted "98% of 172 players underweight the supply line."** That
> exact phrasing is **not** in Croson & Donohue. It appears in **Rong, Shen & Snyder**
> (*The Impact of Ordering Behavior on Order-Quantity Variability*), who use it as a
> *pooled summary* of Croson & Donohue's two studies (2006 ≈ 88 subjects + 2003 POS-
> data-sharing study ≈ 84 → ~172, ~169/172 ≈ 98%). The pooling arithmetic is
> plausible but **[needs-verification]** (the 2003 source is image-only). **We cite the
> primary fact — C&D's own 100% / ~95% at N=44/study — and attribute the "98% of 172"
> framing to Rong, Shen & Snyder, flagged, rather than to Croson & Donohue.**

### Croson, Donohue, Katok & Sterman (2014) — robust even when you hand subjects the answer  [VERIFIED]

**Croson, R., Donohue, K., Katok, E. & Sterman, J. (2014). "Order Stability in Supply
Chains: Coordination Risk and the Role of Coordination Stock." *Production and
Operations Management* 23(2): 176–196.**

Four experiments (baseline; common knowledge of the optimal policy; automated
partners following it; added on-hand coordination stock), 160 participants.

> *"the magnitude of the bullwhip can be mitigated, but … its behavioral causes
> appear robust"* — even after revealing the optimal policy and automating the other
> echelons, *"the large majority of participants continue to underweight the supply
> line."*

A modest "coordination stock" buffer lowers order variability, but **does not remove
the underweighting**. The bias is not an information deficit you can train away.

### Robustness sweep — underweighting survives visibility and is partly a cognitive trait

* **Wu & Katok (2006), "Learning, communication, and the bullwhip effect," *Journal of
  Operations Management* 24(6): 839–850.**  [VERIFIED citation; VERIFIED-substance]
  Knowledge/training *alone* does not reduce the bullwhip; only communication and
  coordination across echelons do. Making the supply line visible helps stabilize but
  does not eliminate underweighting.
* **Narayanan & Moritz (2015), "Decision Making and Cognition in Multi-Echelon Supply
  Chains: An Experimental Study," *Production and Operations Management* 24(8):
  1216–1234.**  [VERIFIED citation; VERIFIED-substance] The tendency to underweight the
  supply line tracks an individual's **cognitive reflection** — i.e. it is partly a
  stable cognitive trait, not merely an artifact of missing information.

Together: β < 1 holds under known demand, equilibrium start, supply-line visibility,
disclosed optimal policy, and automated partners. **Treating β as a structural
property of the chain (not a tunable artifact) is empirically warranted.**

### The chaos link is already in the literature — we sharpen it, not invent it

* **Mosekilde & Larsen (1988), "Deterministic Chaos in the Beer Production-
  Distribution Model," *System Dynamics Review* 4(1–2): 131–147.**  [VERIFIED] First
  showed the beer game routes to deterministic chaos.
* **Thomsen, Mosekilde & Sterman (1991), "Hyperchaotic Phenomena in Dynamic Decision
  Making,"** in *Complexity, Chaos, and Biological Evolution* (NATO ASI Series B, Vol.
  270, Plenum); journal version in *Systems Analysis – Modelling – Simulation* 9(2):
  137–156 (1992).  [VERIFIED] Found chaos *and hyperchaos* (two positive Lyapunov
  exponents) in regions of the decision-parameter space.
* **Macdonald, Frommer & Karaesmen (2013), "Decision making in the beer game and
  supply chain performance," *Operations Management Research* 6(3–4): 119–126.**
  [VERIFIED] Strong supply-line underweighting lengthens the *"period of chaos before
  the system reaches final stability."*

These established the *existence* of chaos in this class of model. **CYB-2's
contribution is to characterize it rigorously on a conserved ledger** — a *measured*
largest Lyapunov exponent on a verified-bounded attractor, and the route named by
direct linearization (a border-collision, not the period-doubling or smooth
Neimark–Sacker one might guess). We are making precise what this literature gestured
at.

---

## Section 2 — The field signatures are real (represented honestly, disconfirming evidence included)

The model predicts *intermediate* signatures on the way to chaos — amplification up
the chain, and persistent oscillation. Both are documented in real supply chains. The
discipline here (same as CYB-1's "information sharing suppresses but does not flatten,"
and the egg model's refusal to overclaim) is to report the **disconfirming** evidence
in the same breath.

### Amplification up real chains — real, but sector-dependent

* **Lee, Padmanabhan & Whang (1997)** — two companion papers. The analytical one,
  *"Information Distortion in a Supply Chain: The Bullwhip Effect," Management Science*
  43(4): 546–558  [VERIFIED], identifies the four operational causes. The practitioner
  one, *"The Bullwhip Effect in Supply Chains," Sloan Management Review* 38(3): 93–102
  [VERIFIED], opens with the **P&G Pampers** case: retail consumption of diapers is
  near-stable, yet P&G's orders to its suppliers swing far more — amplification up the
  chain made concrete. (Which paper "owns" the Pampers anecdote: the Sloan piece —
  [needs-verification] on exclusivity, both cite it.)
* **Bray & Mendelson (2012), "Information Transmission and the Bullwhip Effect: An
  Empirical Investigation," *Management Science* 58(5): 860–875.**  [VERIFIED]
  Firm-level Compustat data, **4,689 U.S. public firms, 1974–2008**: **about two-
  thirds of firms bullwhip** (mean bullwhip 15.8%, median 6.7% of total demand
  variability, both significantly positive).

* **The disconfirming caveat — Cachon, Randall & Schmidt (2007), "In Search of the
  Bullwhip Effect," *Manufacturing & Service Operations Management* 9(4): 457–479.**
  [VERIFIED citation; VERIFIED-substance findings] Using industry-level U.S. data,
  **wholesale industries do amplify, but retail and most manufacturing industries do
  not — they *smooth*.** So amplification is **real but not universal**: a
  sector-dependent property, not a law. We represent it as exactly that. (This
  sector-dependence maps directly onto CYB-2's *regime classification* — see §4.)

### Persistent oscillation — production more variable than sales

* **Blanchard (1983), "The Production and Inventory Behavior of the American Automobile
  Industry," *Journal of Political Economy* 91(3): 365–400.**  [VERIFIED-substance;
  exact pages [needs-verification]] The foundational empirical demonstration that auto
  *production* is more variable than *sales* — the production/inventory cycle is real,
  not a modelling artifact. Corroborated by the macro inventory-cycle literature
  (Blinder & Maccini 1991, "Taking Stock: A Critical Assessment of Recent Research on
  Inventories," *Journal of Economic Perspectives* 5(1): 73–96  [VERIFIED-substance]):
  the consensus that production is more variable than sales and inventory investment
  is procyclical.
* **The semiconductor "silicon cycle"** (the ~4-year boom-bust of capacity and memory
  prices) is widely documented in industry/trade analysis but **[needs-verification]**
  — we could not locate a single canonical *peer-reviewed* primary source in this
  pass. **We cite it only as industry-documented, not to an academic source**, until
  one is pulled. (Automotive, via Blanchard, is the solid academic oscillation cite.)

### Cost stakes (for motivation)

* **Metters (1997), "Quantifying the bullwhip effect in supply chains," *Journal of
  Operations Management* 15(2): 89–100.**  [VERIFIED — verbatim abstract] *"Given
  appropriate conditions, however, eliminating the bullwhip effect can increase
  product profitability by 10–30%."* We carry the qualifiers exactly: this is **product
  profitability**, **conditional** ("given appropriate conditions"), from an
  analytical/simulation study — *not* a measured across-the-board cost saving. The
  bullwhip is expensive enough to be worth understanding; that is all this number is
  asked to support.

---

## Section 3 — Epistemic stance (the honesty firewall — REQUIRED)

**We do not claim to detect chaos directly in macroeconomic or financial time series.
We can't, and here is why the attempt is the wrong move.**

In the 1980s–90s a research program imported the physicists' **correlation-dimension**
estimator (**Grassberger & Procaccia 1983, *Physica D* 9(1–2): 189–208** [VERIFIED])
to hunt for low-dimensional deterministic attractors in GDP, business cycles, and
asset returns. The early positive claim — **Scheinkman & LeBaron (1989), "Nonlinear
Dynamics and Stock Returns," *Journal of Business* 62(3): 311–337** [VERIFIED] —
reported a low correlation dimension in weekly CRSP returns, read at the time as
suggestive of deterministic chaos. **It did not survive.**

Two structural facts about economic data defeated the program:

1. **The series are too short.** The **Eckmann–Ruelle data-length bound** (**Ruelle
   1990, *Proc. R. Soc. A* 427: 241–248**; formalized in **Eckmann & Ruelle 1992,
   *Physica D* 56: 185–187** [VERIFIED citations; exact Ruelle wording
   [needs-verification], Eckmann–Ruelle 1992 is the machine-readable backup]) requires
   roughly **D < 2·log₁₀ N** for a credible dimension estimate D from N points.
   Economic series (hundreds to low thousands of points) cannot reliably resolve more
   than a tiny dimension — so a low estimate is *forced by the data length*, not
   discovered in the dynamics.
2. **The algorithm returns spurious low dimensions on noise.** **Ramsey, Sayers &
   Rothman (1990), "The Statistical Properties of Dimension Calculations Using Small
   Data Sets: Some Economic Applications," *International Economic Review* 31(4):
   991–1020** [VERIFIED citation] showed small-sample correlation-dimension estimates
   are biased and unreliable, and that the earlier low-dimension chaos claims were
   largely small-sample **artifacts**.

The reassessment was decisive. **Brock & Sayers (1988), "Is the business cycle
characterized by deterministic chaos?," *Journal of Monetary Economics* 22(1): 71–90**
[VERIFIED] found little evidence of chaos in U.S. macro aggregates (nonlinearity, yes;
low-dimensional chaos, no). **Hsieh (1991), "Chaos and Nonlinear Dynamics: Application
to Financial Markets," *Journal of Finance* 46(5): 1839–1877** [VERIFIED citation]
re-attributed financial-market nonlinearity to **ARCH-type conditional
heteroskedasticity** (nonlinear *stochastic* volatility) rather than chaos. And the
program's own headline tool, the **BDS test** (**Brock, Dechert, Scheinkman & LeBaron
1996, "A Test for Independence Based on the Correlation Dimension," *Econometric
Reviews* 15(3): 197–235** [VERIFIED]), is a test for **i.i.d./neglected nonlinearity**
— rejecting i.i.d. is equally consistent with nonlinear stochastic processes — and so
**is not a positive detector of deterministic chaos**. The authoritative retrospective,
**Barnett & Serletis (2000), "Martingales, Nonlinearity, and Chaos," *Journal of
Economic Dynamics and Control* 24(5–7): 703–724** [VERIFIED citation], reads the
question as unresolved-to-negative: available tests **cannot separate low-dimensional
chaos from high-dimensional / nonlinear-stochastic dynamics** in economic data.

**Therefore the claim is illustrative, not predictive** — exactly the THESIS stance.
We do not reconstruct the economy's attractor from its thermometer readings. We
validate the **ingredients** (the measured β < 1 bias, §1), validate the **signatures**
(amplification and oscillation, §2), and let the model demonstrate the **mechanism**
(the conserved chain's measured route to chaos, CYB-2). This is the **climate-model
analogy** made literal: nobody reconstructs the atmosphere's attractor from a network
of thermometers; they validate *mechanisms* inside models whose *ingredients* match
measured reality, and report the dynamics, not the trajectory.

The strongest honest claim available, stated as exactly that:

> **The economy is assembled from measured components that, placed on a conserved
> ledger and let run, generate endogenous bounded turbulence. Equilibrium is not the
> generic outcome — it is one regime among several, and not the one the measured
> parameters select.**

---

## Section 4 — Literature → model map

What a referee scans to see the model is anchored. Each empirical finding (left) and
the model element it grounds (right).

| empirical finding (source) | grounds this model element |
|---|---|
| Anchoring-and-adjustment ordering rule, fit to humans (Sterman 1989) | The exact ordering rule in `chaos/model.py` — `order = max(0, D̂ + a_S(S*−S) + a_SL(SL*−SL))`. **Same rule, same parameter names.** |
| **Mean supply-line weight β = 0.34**, β = α_SL/α_s (Sterman 1989) | **Our control parameter β.** His measured mean lands in the *low-β* region (see note below) where CYB-2 leaves the stable equilibrium — the measured human bias sits at the edge of the instability the model finds. |
| 89% of subjects β < ⅔; bias robust to visibility, training, disclosed optimum, automation (Sterman 1989; Croson–Donohue 2006; CDKS 2014; Wu–Katok 2006; Narayanan–Moritz 2015) | Justifies treating **β < 1 as a structural property**, not a tuned dial — we sweep a parameter people *actually exhibit*, not an arbitrary one. |
| Bullwhip persists with operational/stochastic causes removed (Croson–Donohue 2006) | CYB-2's **deterministic-demand isolation** (σ=0): the instability is endogenous to the decision rule, not the demand signal. Their lab control *is* our σ=0 condition. |
| Amplification real but **sector-dependent** — wholesale amplifies, retail smooths (Lee et al. 1997; Bray–Mendelson 2012; Cachon et al. 2007) | CYB-1's recursion channel (bounded amplification) **and** CYB-2's **regime classification** (stable / bounded-turbulence / runaway) — different parameterizations sit in different regimes, mirroring smoothing vs amplifying sectors. |
| Persistent production/inventory oscillation (Blanchard 1983; Blinder–Maccini 1991; silicon cycle [needs-verification]) | CYB-2's **bounded-turbulence regime** — the constraint-riding attractor born at the border-collision (invariant loop → strange attractor). **Not** a smooth Hopf/quasiperiodic torus (the spec's earlier guess); the measured route is a *border-collision*. |
| Chaos & hyperchaos already shown in beer-game models (Mosekilde–Larsen 1988; Thomsen et al. 1991; Macdonald et al. 2013) | CYB-2's **measured λ>0 on a verified-bounded, conserved attractor**, with the route **named by linearization** (border-collision) — the rigorous version of what this literature gestured at. |
| Direct chaos-detection in macro/financial series failed (Brock–Sayers 1988; Ramsey et al. 1990; Hsieh 1991; BDS 1996; Barnett–Serletis 2000) | Why the project is **illustrative, not predictive**: we validate ingredients + signatures + mechanism, and do **not** claim to fit an attractor to macro data. The firewall (§3) *is* a model element — it bounds the claim. |

> **The β-coincidence, stated honestly.** Sterman's measured mean β = 0.34 sits just
> above CYB-2's measured stable→turbulent boundary (β ≳ 0.30 at our canonical
> `a_S=0.7, L=3`), and his subjects' range (0.00–1.05) spans deep into our turbulent
> and runaway regimes. This is a **striking qualitative correspondence** — the bias as
> measured places real decision-makers right at the edge of the instability — but it
> is **not** a quantitative coincidence to lean on: the exact onset β depends on
> `a_S`, lead time `L`, and tier count, which differ from Sterman's fitted setup. We
> report the alignment of *regime* (measured β lands in/near the model's unstable
> region), not an exact numeric match. Pinning the boundary's dependence on `a_S`/`L`
> is a natural follow-up (and connects to CYB-4's formal classification).

---

## Closing note — items flagged [needs-verification]

Carried explicitly so they are never silently asserted:

1. **"98% of 172 players underweight"** — *not* a Croson & Donohue figure; it is Rong,
   Shen & Snyder's pooled summary of C&D's two studies. The primary, verified facts are
   C&D (2006)'s own **100% (44/44)** and **~95% (42/44)**. Cite those; attribute the
   pooled figure to Rong et al. if used at all.
2. **Semiconductor "silicon cycle"** — industry/trade-documented, no peer-reviewed
   primary source located. Cited as industry-documented only. (Automotive, via
   Blanchard 1983, is the solid academic oscillation cite.)
3. **Exact verbatim wording** of: Ruelle's (1990) statement of the 2·log₁₀N bound (use
   Eckmann–Ruelle 1992 as the machine-readable backup); the concluding sentences of
   Hsieh (1991) and Barnett & Serletis (2000); Wu–Katok (2006) and Narayanan–Moritz
   (2015) abstracts. Findings are confirmed in substance; treat the quotes as close
   paraphrase unless the publisher PDFs are pulled.
4. **Blanchard (1983) exact pages** (365–400) attributed from catalog metadata, not the
   article itself.
5. **Which 1997 Lee et al. paper "owns" the Pampers anecdote** — the Sloan piece, but
   exclusivity not confirmed (both reference it).

---

### Full reference list

* Barnett, W. A. & Serletis, A. (2000). Martingales, nonlinearity, and chaos. *Journal
  of Economic Dynamics and Control* 24(5–7): 703–724.
* Blanchard, O. J. (1983). The production and inventory behavior of the American
  automobile industry. *Journal of Political Economy* 91(3): 365–400.
* Blinder, A. S. & Maccini, L. J. (1991). Taking stock: a critical assessment of recent
  research on inventories. *Journal of Economic Perspectives* 5(1): 73–96.
* Bray, R. L. & Mendelson, H. (2012). Information transmission and the bullwhip effect:
  an empirical investigation. *Management Science* 58(5): 860–875.
* Brock, W. A. & Sayers, C. L. (1988). Is the business cycle characterized by
  deterministic chaos? *Journal of Monetary Economics* 22(1): 71–90.
* Brock, W. A., Dechert, W. D., Scheinkman, J. A. & LeBaron, B. (1996). A test for
  independence based on the correlation dimension. *Econometric Reviews* 15(3):
  197–235.
* Cachon, G. P., Randall, T. & Schmidt, G. M. (2007). In search of the bullwhip effect.
  *Manufacturing & Service Operations Management* 9(4): 457–479.
* Croson, R. & Donohue, K. (2006). Behavioral causes of the bullwhip effect and the
  observed value of inventory information. *Management Science* 52(3): 323–336.
* Croson, R., Donohue, K., Katok, E. & Sterman, J. (2014). Order stability in supply
  chains: coordination risk and the role of coordination stock. *Production and
  Operations Management* 23(2): 176–196.
* Eckmann, J.-P. & Ruelle, D. (1992). Fundamental limitations for estimating dimensions
  and Lyapunov exponents in dynamical systems. *Physica D* 56: 185–187.
* Grassberger, P. & Procaccia, I. (1983). Measuring the strangeness of strange
  attractors. *Physica D* 9(1–2): 189–208.
* Hsieh, D. A. (1991). Chaos and nonlinear dynamics: application to financial markets.
  *Journal of Finance* 46(5): 1839–1877.
* Lee, H. L., Padmanabhan, V. & Whang, S. (1997a). Information distortion in a supply
  chain: the bullwhip effect. *Management Science* 43(4): 546–558.
* Lee, H. L., Padmanabhan, V. & Whang, S. (1997b). The bullwhip effect in supply
  chains. *Sloan Management Review* 38(3): 93–102.
* Macdonald, J. R., Frommer, I. D. & Karaesmen, İ. (2013). Decision making in the beer
  game and supply chain performance. *Operations Management Research* 6(3–4): 119–126.
* Metters, R. (1997). Quantifying the bullwhip effect in supply chains. *Journal of
  Operations Management* 15(2): 89–100.
* Mosekilde, E. & Larsen, E. R. (1988). Deterministic chaos in the beer
  production-distribution model. *System Dynamics Review* 4(1–2): 131–147.
* Narayanan, A. & Moritz, B. B. (2015). Decision making and cognition in multi-echelon
  supply chains: an experimental study. *Production and Operations Management* 24(8):
  1216–1234.
* Ramsey, J. B., Sayers, C. L. & Rothman, P. (1990). The statistical properties of
  dimension calculations using small data sets: some economic applications.
  *International Economic Review* 31(4): 991–1020.
* Rong, Y., Shen, Z.-J. M. & Snyder, L. V. The impact of ordering behavior on
  order-quantity variability: a study of forward and reverse bullwhip effects.
  (*Flexible Services and Manufacturing Journal*; vol/issue/pages [needs-verification].)
* Ruelle, D. (1990). Deterministic chaos: the science and the fiction (Claude Bernard
  Lecture, 1989). *Proceedings of the Royal Society of London A* 427(1873): 241–248.
* Scheinkman, J. A. & LeBaron, B. (1989). Nonlinear dynamics and stock returns.
  *Journal of Business* 62(3): 311–337.
* Sterman, J. D. (1989). Modeling managerial behavior: misperceptions of feedback in a
  dynamic decision making experiment. *Management Science* 35(3): 321–339.
* Thomsen, J. S., Mosekilde, E. & Sterman, J. D. (1991). Hyperchaotic phenomena in
  dynamic decision making. In *Complexity, Chaos, and Biological Evolution* (NATO ASI
  Series B, Vol. 270), Plenum; journal version *Systems Analysis – Modelling –
  Simulation* 9(2): 137–156 (1992).
* Wu, D. Y. & Katok, E. (2006). Learning, communication, and the bullwhip effect.
  *Journal of Operations Management* 24(6): 839–850.
