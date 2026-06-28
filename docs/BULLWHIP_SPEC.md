# BULLWHIP_SPEC.md — v0 (standalone)

**Goal:** the smallest honest demonstration that a 3-tier supply chain *amplifies*
order variance — bullwhip — from **demand signal processing under local information**
(each tier estimating demand from the orders it sees), with lead time multiplying the
effect. Isolates the **recursion** channel (see `THESIS.md`). Standalone module; the
integrated SFC version will validate against this one's numbers.

**Math note (why a fixed forecast gives NO bullwhip):** under order-up-to with a
*constant* S, the order each period exactly equals the demand observed that period
(`order_{t+1} = D_t`, one-for-one passthrough — ordering refills the inventory position
to S, demand depletes it by `D_t`, so you re-order exactly `D_t`). Variance out =
variance in, **ratio = 1 for any lead time L.** So the amplification is NOT lead-time
alone — it requires the order-up-to level `S_t` to *move with a demand forecast
estimated from observed orders*. Lead time then multiplies that effect. This is the
canonical mechanism (Chen, Drezner, Ryan & Simchi-Levi 2000).

This is a build ticket, written in code terms. Math notation, where it appears, is
glossed with its code form.

---

## What success looks like (acceptance criteria)

1. Order-variance amplifies up the chain: `ratio[tier] > 1`, compounding, with the
   manufacturer seeing the largest swings — from *stationary* consumer demand.
2. The amplification is **structural**: same seed → identical run (determinism guarded).
3. **Killer experiment (three modes — separating *seeing* from *acting*):**
   - `local_info`: each tier forecasts off the distorted orders it receives AND
     replenishes against its own (distorted) installation position → amplification
     **compounds** (≈ r, r², r³ vs true demand).
   - `shared_info`: each tier forecasts off true consumer demand but **still
     replenishes the distorted orders it physically received** → compounding is
     **strongly suppressed (~3× here) but does NOT flatten** — the residual is the
     physical-replenishment channel (received-order variance leaks through the
     inventory position regardless of the forecast). Seeing true demand ≠ acting on it.
   - `coordinated`: each tier forecasts off true demand AND replenishes against true
     **end-demand** (echelon position depleted by D_t, not by received orders) →
     cumulative ratio goes **≈ flat at r** across the chain, each stage near the
     single-stage Chen ratio, no compounding.

   The three-way contrast decomposes the bullwhip: `local→shared` = the forecast
   (information) channel; `shared→coordinated` = the physical replenishment channel.
   This is the installation- vs echelon-base-stock distinction, made measurable, and
   it localizes the *compounding* in the information+coordination structure — the thing
   equilibrium models assume away.
4. Magnitude is in the right ballpark vs the literature (Lee/Padmanabhan/Whang; Beer
   Game). Order-of-magnitude agreement is the v0 bar, not a tuned match.
5. **Conservation holds throughout:** every unit ordered is eventually shipped or sits
   in a named inventory. Goods never created/destroyed. Assert < 1e-9. Variance
   amplifies *while goods conserve* — that contrast is the sanity check (leak = bug;
   conserve-but-amplify = the real phenomenon).

## Scope discipline (what v0 deliberately excludes)

- **Demand estimation is IN; price anticipation is OUT.** Each tier estimates the
  demand *mean* from observed orders (moving average) — this is statistical inference
  under incomplete information, the heart of the recursion/information-structure story,
  and it's *required* for any bullwhip to exist. What stays excluded is *reflexivity* in
  the inflation sense: forward **price** expectations, agents anticipating inflation and
  building it in. Estimating demand ≠ anticipating prices. (The earlier "fixed forecast
  only" framing was wrong on the math — see the goal note — and conflated these two.)
- No batching, no price promotions, no capacity limits → later experiments, each added
  one at a time and measured for its marginal contribution. (Note: batching is a
  *separate*, forecast-free bullwhip source, but it does NOT vanish under shared info,
  so it can't serve the killer experiment — which is why v0's mechanism is signal
  processing, not batching.)
- 3 tiers exactly. Not N. Generalize on contact, not on spec.

---

## The system (state + update)

Discrete time steps `t` (= `for t in range(T)`; "weeks"). Three tiers in series:

```
consumer -> [retailer] -> [wholesaler] -> [manufacturer] -> (external supply)
              tier 0         tier 1           tier 2
```

Each tier holds state:
- `inventory`      on-hand stock (units)
- `backlog`        unfilled downstream demand (units owed)
- `pipeline`       orders placed upstream but not yet arrived (a queue of length L)

Constants:
- `mu`            mean consumer demand (e.g. 100)
- `sigma`         consumer demand noise sd (small, e.g. 10)
- `L`             lead time between tiers, in steps (e.g. 2)
- `p`             moving-average window for the demand forecast (e.g. 5, 10, 15)
- `T`             run length (e.g. 200) ; `warmup` to discard transients (e.g. 50)
- `z`             safety factor (e.g. 2) for the safety buffer
- `seed`         RNG seed (determinism)

**Consumer demand** (the boring input):
`D_t = mu + eps_t`  →  in code: `demand[t] = mu + rng.normal(0, sigma)`
(`_t` = "at step t" = array index; `mu` = constant; `eps_t` = seeded noise this step.)
Clamp at 0 (no negative demand).

**Per step, per tier (downstream → upstream order of evaluation):**

1. **Receive arrivals:** the order that was placed `L` steps ago arrives now →
   `inventory += pipeline.popleft()`.
2. **Receive demand:** incoming order from downstream (tier 0's "downstream" is the
   consumer; `D_t`). Add to backlog: `backlog += incoming`.
3. **Ship:** `shipped = min(inventory, backlog)`; `inventory -= shipped`;
   `backlog -= shipped`. `shipped` becomes the *arrival* for the downstream tier
   (enters *their* pipeline, respecting L). External supply (above tier 2) is assumed
   infinite and instant-at-lead-time, so tier 2's upstream orders always get filled L
   steps later.
4. **Order (the decision rule, below):** compute `order_qty`, push into this tier's
   pipeline (arrives upstream-shipped after L). `order_qty` is what the tier *places*;
   it's also the **demand the upstream tier sees** next step. This is the propagation.

## The decision rule — order-up-to with a moving-average demand forecast

Each tier targets an inventory *position* of `S_t` and orders the gap:

```
inventory_position = inventory - backlog + sum(pipeline)   # on-hand, owed, in-transit
order_qty = max(0, S_t - inventory_position)
```

The key change from a naive base-stock: `S_t` is **not constant** — it tracks an
*estimate* of lead-time demand, updated each step from observed orders:

```
demand_hat = mean(last p observed demands)         # moving-average forecast (the estimate)
S_t = demand_hat * (L + 1) + z * sigma * sqrt(L+1) # cover lead-time+review demand + safety
```
(`demand_hat` = the tier's running estimate of the demand mean from *its own* incoming
orders; `mean(last p ...)` = `np.mean(window)`. This is estimation, not price
anticipation — see scope note.)

**Why this produces bullwhip and the constant-S version did not:** because `S_t` moves
with `demand_hat`, a single high demand observation both (a) depletes inventory *and*
(b) raises the target — so the tier orders extra to refill *and* extra to raise the
level. That double response is the amplification. With constant S only (a) happens, and
orders pass demand through one-for-one (ratio 1). Lead time L multiplies the effect (the
target scales with L+1). Smaller `p` (jumpier forecast) amplifies more; larger `p`
(smoother) damps toward 1.

The rule is still the least-clever *defensible* rule — a real inventory system using a
moving-average forecast and a base-stock target. It is not trying to amplify. It
amplifies anyway. That's the result.

**Installation vs echelon position (what the `coordinated` mode changes).** The
`inventory_position` above is the *installation* position — depleted by the orders a
tier physically receives from downstream, which under local/shared info are already
distorted. The `coordinated` mode instead orders against an *echelon* position depleted
by true **end-demand** `D_t` (`coord_pos -= D_t; order = max(0, S_t - coord_pos);
coord_pos += order`). Every tier then replenishes what the consumer actually consumed,
so order variance stays flat up the chain. Forecasting off true demand (`shared`) fixes
only the `S_t` term; ordering off true demand (`coordinated`) also fixes the position
term — which is why only `coordinated` flattens.

## The three modes (the killer experiment) — seeing vs acting

Two channels carry the distortion upstream: the **forecast** (what a tier *sees*)
and the **physical replenishment** (what a tier *acts on* — the inventory position
it refills). The three modes turn each off in turn:

- `local_info` (default): a tier forecasts `demand_hat` from the (already-distorted)
  `order_qty` placed below it, and replenishes its installation inventory position
  (depleted by those distorted orders). Both channels distorted.
  **Expected: compounds up the chain (≈ r, r², r³).**
- `shared_info`: a tier forecasts `demand_hat` from *true consumer demand* `D_t`, but
  STILL replenishes the distorted orders it physically received (installation position
  unchanged). Only the forecast channel de-distorted.
  **Expected: strongly suppressed but NOT flat** — the received-order variance still
  leaks through the inventory-position channel. Seeing ≠ acting.
- `coordinated`: a tier forecasts off `D_t` AND replenishes against an **echelon
  position depleted by true end-demand `D_t`** (not by received orders) — echelon
  base-stock. Both channels de-distorted.
  **Expected: ≈ flat at r across the chain** — each stage near the single-stage Chen
  ratio, no compounding.

Same seed for all three. The *contrast* — compounds vs suppressed vs flat, and its
decomposition (`local→shared` = forecast channel, `shared→coordinated` = physical
channel) — is the proof, not any run alone. It shows the *multiplication* lives in the
information **and** coordination structure.

---

## The instrument (measurement = a function)

```
def bullwhip_ratio(orders_placed, demand_received, warmup):
    o = orders_placed[warmup:]      # discard transient
    d = demand_received[warmup:]
    return variance(o) / variance(d)     # Var(orders_out)/Var(demand_in)
```
(`variance` = `np.var`; `Σ`/sigma-notation you'll see in papers is just `sum`/`np.var`.)

Report per tier:
- `ratio[0]` retailer, `ratio[1]` wholesaler, `ratio[2]` manufacturer
- total chain amplification = `ratio[0] * ratio[1] * ratio[2]`
- the same four numbers for both `local_info` and `shared_info`

A plot: order time-series for consumer + each tier on one axis — the visual "the
wiggle grows upstream" — plus a small table of the ratios in both modes.

## Deliverables

- `bullwhip/model.py`      — the 3-tier system + step loop + all three modes
  (local_info / shared_info / coordinated)
- `bullwhip/measure.py`    — `bullwhip_ratio` + the report
- `bullwhip/run_v0.py`     — runs both modes, prints the ratio table, saves the figure
- `bullwhip/figures/`      — the amplification plot
- conservation assert inside the step loop (goods in = goods out + Δinventory)
- a short `bullwhip/README.md`: the result, the two-mode table, the literature numbers
  it's checked against

## Validation targets

**Primary — exact closed form (Chen, Drezner, Ryan & Simchi-Levi 2000).** For
stationary i.i.d. demand, a single stage, moving-average window `p`, lead time `L`, the
order-to-demand variance ratio is:

```
ratio_single_stage  =  1 + 2L/p + 2L**2 / p**2
```

This is a *rigorous analytic target*, not a fuzzy industry number — the v0 sim must
match it. Sweep `L` and `p` and check the measured single-stage `Var(orders)/Var(demand)`
against the formula. Predictions to confirm: ratio **rises with L**, **falls with larger
p** (more smoothing), → 1 as `p → ∞` (the constant-S limit, no bullwhip). For the
3-stage chain under local info, expect the per-stage ratios to compound (≈ formula at
each stage relative to the stage below). (The published form is technically a lower
bound due to how the demand variance is estimated; equality holds in cleaner setups.
Order-of-magnitude-plus-correct-trends is the v0 bar.)

**Secondary — sanity check vs literature.** Pull 1-2 real figures (P&G diapers; the Beer
Game) for an order-of-magnitude gut check. Document in the README. Citation:
Chen et al. (2000), *Quantifying the Bullwhip Effect in a Simple Supply Chain*,
Management Science 46(3):436-443.

## Notes for the implementer

- Determinism: single `numpy.random.default_rng(seed)`; thread it through. No global
  random state. Same seed → identical arrays.
- Build single-seed first; get the mechanism + conservation clean. Only THEN sweep
  seeds to show robustness (ensemble), per the in-sample-then-out-of-sample discipline.
- Keep the step-evaluation order fixed and documented (arrivals → demand → ship →
  order). Order-of-operations changes the dynamics; it's part of the spec, not a detail.
- This module is a reference implementation: the integrated SFC version must reproduce
  these ratios. Keep it clean enough to be an oracle.
- **Free sanity check:** run once with the forecast *frozen* at the true mean (constant
  S). You should measure ratio ≈ 1 at every stage — confirming the harness is correct
  and that the bullwhip genuinely comes from the moving-average update, not a bug. This
  is the `p → ∞` limit and it's worth asserting as a regression test.
- The forecast needs `p` observations before it's meaningful — seed the first `p` steps
  at `mu` (or extend warmup) so the measured window excludes the forecast's cold start.
