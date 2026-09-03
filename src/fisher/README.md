# Phase 2b — the genuine Fisher debt-deflation loop: the two-basin map

> Ticket: **CYB-19 Phase 2b** (Linear ticket number to be assigned; referenced here as Phase 2b).
> Successor to CYB-23 (Phase 2). Standalone; **reuses CYB-23 (`contagion/`) unchanged**
> (`fisher_phi=0` ⇒ byte-exact CYB-23 ⇒ Phase 1 ⇒ CYB-17).

CYB-23 wired **Engine 1** (credit-quantity contagion — the impaired rentier's risk premium →
dearer credit → more Ponzi → **hyper-INFLATIONARY** collapse) and **gated Engine 2 (the
price-level Fisher loop) OFF** — honestly, with evidence. CYB-23's AC6 verified that CYB-17's
demand channel is a *symmetric multiplicative damper* (`damp = max(0, 1 − demand_b·slack)` scales
**both** `α_w` and `α_p` toward zero), so it drives inflation toward 0 **from above** and can
never flip sign (min tail π = **−0.000%/step** even at `demand_b=10`). Deflation was therefore
**unreachable by construction**, and CYB-23 said so: *"Engine 2 needs a strengthened price
mechanism (Phase 2b), not a simple switch-on."* This module is that strengthened mechanism, and
it answers the question CYB-23 deferred: **is the "inflationary, not Fisher" result conditional?**

```bash
cd src/fisher
python3 run_v0.py   # nested regression → φ* threshold → two-basin map → loop anchor → conservation → resolution
```

## The one new mechanism — a genuine, self-reinforcing Fisher loop

Everything else is CYB-23, reused unchanged. The crude fixed-decrement `fisher_on` switch that
`ContagionEconomy` carries stays **OFF**; Phase 2b supersedes it with a real feedback loop keyed
off the **real debt burden**:

```
pressure = max(0, leverage − b_ref)      # excess real debt burden D/P = distress
P ← P · (1 − φ · pressure)               # distress selling cuts the price level
# next period: leverage = D/P rises (D nominal, unchanged) ⇒ pressure rises ⇒ a bigger cut
```

That is Fisher 1933's *"the more they pay, the more they owe"* — a closed, self-reinforcing loop,
not a mechanical decrement. The pivot is `φ` (Engine-2 price-channel strength); `φ=0` recovers
CYB-23 byte-for-byte.

## The headline — two engines on one signal, opposite sign (the two-basin map)

![two-basin map](figures/cybeersym_fisher_v0_two_basin_map.png)

A falling `P` does **two opposite things at once**:

* **Engine 2 (φ, deflationary):** cuts prices directly (this module) → raises the real burden.
* **Engine 1 (ε, inflationary):** raises `i·D/P` (cost channel) and `impairment/P` (the rentier's
  risk premium, CYB-23) → **more** inflation.

So the **same debt-distress** routes to inflation OR deflation, and which **collapse basin** you
fall into is set by **φ vs ε — the strength of the price channel**, exactly the pivot CYB-23
named. Over a (φ, ε) grid all three outcomes are reachable — **bounded grind · Engine-1
inflation-collapse · Engine-2 debt-deflation collapse** — with a **ragged contested frontier**
between the two collapse basins (the two feedbacks fight step-by-step, the same raggedness CYB-23
found on the impairment horizon). **Both collapse basins reachable ⇒ not rigged.**

## AC1 — deflation is a *threshold* phenomenon (φ* ≈ 1.63)

![threshold and anchor](figures/cybeersym_fisher_v0_threshold_and_anchor.png)

Isolating Engine 2 (ε=0) and sweeping φ: below **φ\* ≈ 1.63** the grind stays bounded (the Fisher
cut is overpowered by the conflict layer's markup-defense response — a falling `P` raises the wage
share `ω=W/P`, which makes firms want to raise `P`); above φ* the loop wins and debt-deflation
collapses. You have to **strengthen the price channel past φ\*** to reach deflation — CYB-17's
symmetric damper never could.

## AC3 — the collapse is the LOOP, not the mechanical cut (the honesty anchor)

A **frozen-leverage regression** (the `pressure` term reads a *held-constant* leverage — same cut
magnitude, no feedback) stays **BOUNDED** (1.17%/step grind) at φ = 2, 4, 8 where the live loop
deflation-collapses. So the collapse is genuinely the self-reinforcing `D/P` feedback, not the
price decrement alone (cf. CYB-10's `κ=0` decoupling anchor).

## AC4 — conservation through the deflationary transient: the SFC payoff

![real-burden runaway](figures/cybeersym_fisher_v0_real_burden_runaway.png)

The nominal capital-account identity (rentier asset ≡ firm liability, Godley–Lavoie) is
**P-independent**, so the Fisher price cut *cannot* break it — worst residual **1e-16** through a
full deflationary collapse. And **that is the SFC point of debt-deflation**: it is a **REAL-burden
runaway** (`D/P` climbs and the per-step deflation accelerates through the −25%/step freeze; left
unfrozen `P→0`, `D/P→∞`) while the **nominal accounting stays exact**. Debt-deflation is not an
accounting failure — it is the real burden diverging under a consistent balance sheet.

## AC5 — the resolution of CYB-23's caveat

* **φ=0 (shipped CYB-23 config):** deflation **unreachable** — exactly as CYB-23's AC6 reported.
  CYB-23 was **right for that config**.
* **φ > φ\* ≈ 1.63:** the Fisher **deflationary basin opens.**

**Verdict:** the *"inflationary, not Fisher"* result is **CONDITIONAL** — it holds for the shipped
(weak-price-channel) configuration and is **NOT a refutation of debt-deflation.** Two engines,
opposite sign, one distress signal; the price-channel strength picks the basin. This is the honest
characterization to carry into any outreach to a Minsky/Keen-orbit economist: we did **not** ignore
the Fisher condition — we built it, and mapped the boundary between the two engines.

## Nested regression — byte-exact at each shell

`CYB-17 ⊂ Phase 1 ⊂ Phase 2 (CYB-23) ⊂ Phase 2b`: `fisher_phi=0` ⇒ CYB-23 exactly (`W,P,D` Δ =
`0.0`). Determinism (σ=0): byte-identical reruns.

## Scope / forward-links

* **Bare-CYB-17 substrate** (as CYB-23). Phase-2b-on-coupled (the CYB-22 recursion territory) is
  a later cell — recursion re-loading the gap should shift φ* and thicken the contested frontier.
* **Aggregate only** — no unit-level / network default topology.
* The Fisher engagement `b_ref` and the linear `pressure` map are v0 choices; a structural
  output-gap price mechanism (real activity, not just leverage) is the natural v1.
* Feeds the **monetarism critique (CYB-16, gated)** and the **formal bifurcation program
  (CYB-13, gated)**: the inflation/deflation basin boundary is a new switching structure a
  piecewise-smooth specialist could formalize.

## Files

- `model.py` — `FisherEconomy`: composes an unchanged `ContagionEconomy` + the genuine Fisher
  debt-deflation loop (excess-real-burden → distress-selling price cut → higher real burden) +
  symmetric blow-down detection + the frozen-leverage honesty switch.
- `run_v0.py` — nested regression → φ* threshold (AC1) → two-basin map (AC2, headline) → the
  loop-not-cut anchor (AC3) → capital-account conservation through deflation (AC4) → the CYB-23
  resolution (AC5) → determinism (AC6).
- `figures/` — the two-basin map (headline); the φ* threshold + frozen-leverage anchor; the
  real-burden runaway with the nominal identity holding.

## Anchors

Fisher 1933 (debt-deflation — **now wired**, Engine 2). Minsky (FIH). Keen (Goodwin–Minsky debt
dynamics). Godley–Lavoie (SFC capital-account consistency — the P-independence of the nominal
identity is the load-bearing observation). The descriptive/normative firewall holds: this reports
*what the price-channel strength does*; the monetarism conclusion (CYB-16) stays out.
