---
title: "feat: Bullwhip module v0 — isolate the recursion channel"
type: feat
status: done
date: 2026-06-28
tracking: CYB-1
canonical_source: "Linear CYB-1 (https://linear.app/techno87/issue/CYB-1)"
---

# feat: Bullwhip module v0 — isolate the recursion channel

> **Canonical spec lives in Linear (CYB-1).** This file mirrors the corrected
> spec into version control. Spec changes happen in Linear first, then sync here.
> Outcome / final numbers are at the bottom.

## Overview

The smallest honest demonstration that a 3-tier supply chain *amplifies* order
variance — bullwhip — from **demand-signal processing under local information**
(each tier estimating demand from the orders it sees), with lead time multiplying
the effect. Isolates the **recursion** channel (see `THESIS.md`). Standalone
module; the integrated SFC version will validate against this one's numbers.

> **Math note (why a fixed forecast gives NO bullwhip):** under order-up-to with
> a *constant* S, the order each period exactly equals the demand observed that
> period (`order_{t+1} = D_t`, one-for-one passthrough). Variance out = variance
> in, **ratio = 1 for any lead time L.** So amplification is NOT lead-time alone —
> it requires the order-up-to level `S_t` to *move with a demand forecast
> estimated from observed orders*. Lead time then multiplies that effect.
> Canonical mechanism: Chen, Drezner, Ryan & Simchi-Levi (2000).

## Acceptance criteria

1. Order-variance amplifies & compounds up the chain: cumulative
   `Var(out)/Var(true demand)` rises retailer→wholesaler→manufacturer,
   manufacturer worst — from *stationary* consumer demand.
2. **Structural**: same seed → byte-identical arrays; effect robust across seeds.
3. **Three-mode contrast (the killer experiment).** Separates *seeing* true
   demand from *acting* on it:
   - `local` — forecast off distorted received orders → **full compounding**.
   - `shared` — forecast off true demand, but still replenish the distorted
     orders physically received → **strongly suppressed (~3×) but NOT flat**. The
     residual is the physical-replenishment channel: `order ≈ received + ΔS`; a
     smooth (true-demand) ΔS still lets received-order variance pass through.
     *Information sharing suppresses; it does not eliminate. Seeing ≠ acting.*
   - `coordinated` — replenish off true end-demand too (echelon-style), not just
     forecast from it → **≈ flat, no compounding** (each stage near the
     single-stage Chen ratio). If it still compounds, that's a finding (lead-time
     structure compounds even under full coordination) — report it.

   The three-way table (per-stage + cumulative, all modes) localizes how much
   distortion is forecast-channel vs physical-channel. (Maps to installation- vs
   echelon-base-stock in the literature.)
4. Magnitude matches the **closed-form target** (below) to order-of-magnitude +
   correct trends.
5. **Conservation holds throughout:** every unit ordered is eventually shipped or
   sits in a named inventory. Goods never created/destroyed. Assert < 1e-9.
   Variance amplifies *while goods conserve* — the sanity check (leak = bug;
   conserve-but-amplify = real).

## Scope discipline (v0 excludes)

- **Demand estimation is IN; price anticipation is OUT.** Each tier estimates the
  demand *mean* from observed orders (moving average) — statistical inference
  under incomplete info, the heart of the recursion/information-structure story,
  *required* for any bullwhip. Excluded: *reflexivity* (forward **price**
  expectations). Estimating demand ≠ anticipating prices.
- No batching, no price promotions, no capacity limits → later experiments, one
  at a time. (Batching is a separate forecast-free bullwhip source but does NOT
  vanish under shared info, so it can't serve the killer experiment — which is
  why v0's mechanism is signal processing.)
- 3 tiers exactly. Generalize on contact, not on spec.

## The system (state + update)

Discrete steps `t` (`for t in range(T)`; "weeks"). Three tiers in series:
`consumer → [retailer t0] → [wholesaler t1] → [manufacturer t2] → (external supply)`

Each tier: `inventory` (on-hand), `backlog` (owed downstream), `pipeline` (orders
placed upstream not yet arrived, queue length L).

Constants: `mu` (mean demand ~100), `sigma` (noise sd ~10), `L` (lead time ~2),
`p` (MA forecast window, e.g. 5/10/15), `T` (~400), `warmup` (~100), `z` (safety
factor ~2), `seed`.

**Consumer demand:** `demand[t] = mu + rng.normal(0, sigma)`, clamp ≥ 0.

**Per step, per tier (downstream → upstream order of evaluation — fixed, part of spec):**

1. Receive arrivals: `inventory += pipeline.popleft()` (order placed L steps ago).
2. Receive demand: incoming order from downstream (t0's is consumer `D_t`);
   `backlog += incoming`.
3. Ship: `shipped = min(inventory, backlog)`; decrement both; `shipped` becomes
   downstream's arrival (respecting L). External supply above t2 is infinite,
   filled at lead time.
4. Order (rule below): push `order_qty` into pipeline; it's also **the demand the
   upstream tier sees** next step (the propagation).

## Decision rule — order-up-to with moving-average demand forecast

```
inventory_position = inventory - backlog + sum(pipeline)
order_qty = max(0, S_t - inventory_position)
```

`S_t` is **not constant** — it tracks an estimate updated each step:

```
demand_hat = mean(last p observed demands)          # the moving-average forecast (estimate)
S_t = demand_hat * (L + 1) + z * sigma * sqrt(L+1)  # lead-time+review demand + safety
```

**Why this amplifies and constant-S did not:** a high demand observation both (a)
depletes inventory *and* (b) raises the target — so the tier orders extra to
refill *and* extra to raise the level. Double response = amplification. Constant S
→ only (a) → one-for-one passthrough → ratio 1. Lead time L multiplies it; smaller
p (jumpier) amplifies more, larger p (smoother) damps toward 1.

**Mode wiring (the three modes differ ONLY in what signal feeds the rule):**

- `local`: `demand_hat` from received orders; replenish received orders. (both channels distorted)
- `shared`: `demand_hat` from true consumer demand `D_t`; still replenish received orders. (forecast channel clean, physical channel distorted)
- `coordinated`: forecast AND replenishment driven by true end-demand (echelon position depleted by `D_t`, not received orders). (both channels clean)

## Instrument

```python
def bullwhip_ratio(orders_placed, demand_received, warmup):
    o = orders_placed[warmup:]; d = demand_received[warmup:]
    return np.var(o) / np.var(d)
```

Report per tier (retailer/wholesaler/manufacturer) + chain product, for **all
three modes** (per-stage and cumulative-vs-true-demand).

## Validation target — exact closed form (Chen et al. 2000)

For stationary i.i.d. demand, single stage, MA window `p`, lead time `L`:

```
ratio_single_stage = 1 + 2*L/p + 2*L**2/p**2     # use L_effective = L+1 (lead + review) to match
```

Rigorous analytic target — sweep L and p, confirm measured single-stage ratio
matches. Predictions: rises with L, falls with larger p, → 1 as p → ∞. (Published
form is a lower bound; trends + order of magnitude is the v0 bar.) Citation: Chen,
Drezner, Ryan, Simchi-Levi (2000), *Quantifying the Bullwhip Effect in a Simple
Supply Chain*, Management Science 46(3):436-443.

## Deliverables

- `src/bullwhip/model.py` — 3-tier system + step loop + all three info modes
- `src/bullwhip/measure.py` — `bullwhip_ratio` + report
- `src/bullwhip/run_v0.py` — runs all modes, prints three-way ratio table, saves figure
- `src/bullwhip/figures/` — amplification plot
- conservation assert in the step loop
- `src/bullwhip/README.md` — result, three-mode table, formula check, lit numbers

## Implementer notes

- Determinism: single `numpy.random.default_rng(seed)`, threaded; no global random state.
- **Free sanity/regression check:** run with forecast frozen at true mean
  (constant S) → ratio ≈ 1 every stage. Confirms harness is correct and the
  bullwhip comes from the MA update, not a bug. (The p → ∞ limit.)
- Seed first `p` steps at `mu` (or extend warmup) so the measured window excludes
  forecast cold-start.
- Build single-seed first; get mechanism + conservation clean; THEN sweep seeds
  for robustness (ensemble).
- This module is a **reference implementation / oracle**: the integrated SFC
  version must reproduce these ratios. Keep it clean.

---

## Outcome (shipped 2026-06-28, commit `bc8946e`)

All five acceptance criteria met. Three-mode chain amplification (same seed, same
stationary demand):

| mode | cumulative ratio (retailer→wholesaler→manufacturer) | chain |
|------|------|------:|
| `local` (forecast + replenish distorted) | 2.92 → 10.32 → 36.62 | 36.6× |
| `shared` (true-demand *forecast* only) | 2.92 → 6.28 → 10.94 | 10.9× |
| `coordinated` (echelon *replenishment*) | 2.92 → 2.92 → 2.92 | 2.9× |

- **Decomposition:** `local→shared` ≈3.3× (forecast/information channel);
  `shared→coordinated` ≈3.7× (physical replenishment channel). Comparable size —
  *seeing true demand removes <half the gap; you must act on it.*
- `coordinated` flat value (2.92) ≈ the single-stage Chen ratio — the irreducible
  per-stage forecast response; the *compounding* is gone.
- Validations: Chen closed form matched to ~1% (all trends hold); goods
  conservation 3.6e-11 every step; deterministic + robust across seeds 0–7
  (strict `local > shared > coordinated`); frozen-forecast regression = 1.000.

**Spec correction this build earned:** the original criterion 3 predicted `shared
→ flat ≈ r`, which the model refuted (shared suppresses but does not flatten). The
fix — splitting `shared` (seeing) from `coordinated` (acting) — produced a sharper
result. See [`../solutions/bullwhip-seeing-is-not-acting.md`](../solutions/bullwhip-seeing-is-not-acting.md).
