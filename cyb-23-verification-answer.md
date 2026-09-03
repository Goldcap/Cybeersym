# Verification answer — CYB-23: is the "inflationary, not deflationary" collapse *conditional*?

**Short answer: YES — the reconstruction holds, on all three points, verified against the actual
code and committed results. And it is now more than a reconstruction: Phase 2b (`src/fisher/`)
built the strengthened price channel the reconstruction hypothesized, so the "conditional" claim
is now demonstrated, not just argued.** A Minsky/Keen-orbit economist can be told we did *not*
ignore the Fisher condition — we wired it and mapped the boundary between the two engines.

## The three points, checked against the code

**1. Was the Fisher / price-level engine gated OFF in the CYB-23 headline runs? — YES.**
`ContagionParams.fisher_on` defaults to `False` (`src/contagion/model.py:67`), and the
impairment-horizon map (`horizon_map` → `outcome` → `_mk` in `run_v0.py`) never sets it. The
Engine-2 branch in `ContagionEconomy.step()` (`model.py:148`) is dead in every headline cell. So
the entire CYB-23 headline (the cure↔contagion-collapse horizon) is **Engine 1 only** —
credit-quantity, the impaired rentier's risk premium `i_eff = i + ε·(impairment/P)`.

**2. Was the demand/price channel verified too weak to pull the price level negative? — YES,
exactly. min ≈ −0.00%/step, and the reason is structural, not numerical.** CYB-23's AC6
(`demand_channel_check`) sweeps `demand_b` and reports min tail inflation (reproduced on a live
run):

| demand_b | min tail π |
|---:|---:|
| 0 | +1.810 %/step |
| 3 | +1.267 %/step |
| 6 | +0.724 %/step |
| 10 | **−0.000 %/step** |

The channel damps inflation toward **0 but never below it**. The mechanism is why: CYB-17's demand
channel is a *symmetric multiplicative damper* — `damp = max(0, 1 − demand_b·slack)` scales **both**
`α_w` and `α_p` toward zero (`accommodation/model.py:151,166-167`). It can shrink the spiral to
nothing but cannot flip its sign, so π approaches 0 **from above** asymptotically. Deflation was
**unreachable by construction**, not merely unobserved.

**3. Does forcing the Fisher gate ON produce deflation? — YES, but with an important nuance.**
CYB-23's AC6 confirms the *gated switch itself is wired*: `final_logP(True) < final_logP(False)`
returns `fisher_wired = True` — turning `fisher_on` on with `fisher_flex=0.02` does push `P` down.
BUT that switch is a **crude fixed decrement** (`P *= (1 − fisher_flex)` while the crunch is
active), not a genuine self-reinforcing loop — which is exactly why CYB-23 itself concluded "Engine
2 needs a **strengthened price mechanism (Phase 2b)**, not a simple switch-on." So "forced on →
deflation" is technically true for the crude switch, but the honest, load-bearing demonstration is
Phase 2b.

## What Phase 2b now shows (this upgrades the answer from "argued" to "demonstrated")

Phase 2b (`src/fisher/`) replaces the crude switch with a genuine Fisher loop — distress (excess
real debt burden `D/P > b_ref`) → distress selling cuts `P` → the cut **raises** the real burden
next period → more selling. Findings (all from `src/fisher/run_v0.py`, conservation ≤ 1e-16,
determinism byte-exact, `fisher_phi=0` ⇒ byte-exact CYB-23):

- **Deflation is reachable, as a threshold.** At ε=0, sweeping the price-channel strength φ: below
  **φ\* ≈ 1.63** the grind stays bounded; above it the Fisher loop deflation-collapses. So
  deflation is reachable *only when the price channel is strengthened past φ\** — precisely the
  reconstruction's "reachable only when forced," now quantified.
- **The two basins are a parametric contest.** A falling `P` feeds *both* engines with opposite
  sign: Engine 2 (φ) cuts prices (deflation) while Engine 1 (ε) raises `i·D/P` and `impairment/P`
  → premium/cost (inflation). Over a (φ, ε) grid all three outcomes appear — bounded (115 cells),
  Engine-1 inflation-collapse (173), Engine-2 deflation-collapse (237) of 525 — with a **ragged
  contested frontier** where the two feedbacks fight step-by-step. **Both collapse basins
  reachable ⇒ not rigged.**
- **The deflation is genuinely Fisher's loop, not a mechanical cut.** A frozen-leverage regression
  (the pressure term reads a held-constant leverage) stays **bounded** at φ = 2, 4, 8 where the
  live self-reinforcing loop collapses.
- **The SFC point.** Conservation holds to **1e-16 through the deflationary collapse**, because the
  nominal capital-account identity (rentier asset ≡ firm liability) is *P-independent*. Debt-
  deflation is a **real-burden runaway** (`D/P→∞`) under an *exact* balance sheet — not an
  accounting failure. This is a nice, defensible SFC framing for an economist.

## The single most honest one-sentence characterization

> Two collapse engines share one debt-distress signal and point in opposite directions — Engine 1
> (the impaired rentier's risk premium → cost-push, inflationary) and Engine 2 (distress selling →
> price cut → higher real burden, the genuine Fisher debt-deflation loop) — and which basin the
> model falls into is set parametrically by the strength of the price channel (φ) versus the
> premium channel (ε); in the shipped configuration (φ=0) only the inflationary basin is
> spontaneously reachable, while the Fisher deflationary basin opens once the price channel is
> strengthened past φ\*≈1.63, so *"inflationary, not Fisher"* is a **conditional property of the
> weak-price-channel configuration, not a refutation of debt-deflation.**

## Bottom line for the outreach

The framing is safe to send. The only correction to the reconstruction is a *strengthening*: point
3 ("forcing Fisher on produces deflation") was true for a crude switch and is now backed by a
genuine loop with a mapped threshold and a not-rigged two-basin result. Nothing overclaims; the
Fisher condition is addressed head-on, and the SFC balance-sheet consistency through both collapse
types is a credible technical calling-card.

*(Filing note: the CYB-23 spec is canonical in Linear — mirror this answer as a comment on CYB-23,
and file Phase 2b as its own ticket / link `src/fisher/`. Linear MCP was unreachable at write time,
so this lives in the repo for now.)*
