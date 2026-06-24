"""
Cybeersym — v0 plumbing test: a single perishable staple (eggs).

Purpose of THIS file: not to be right about eggs, but to prove the architecture
holds water before we invest in real fixtures. Two things must be true at the end:

  1. MONEY CONSERVATION (Godley): total money is constant every tick, across a
     shock, to floating-point epsilon. If it leaks, the model is a lie.
  2. PHYSICAL CONSERVATION: every egg is accounted for —
     produced - consumed - perished == in-pipeline + supplier-stock + store-stock.

If both hold AND a supply shock produces (a) a retail price spike via sticky
markup + cost pass-through against inelastic demand, and (b) a REGRESSIVE
distributional wedge (bottom-tier personal inflation > aggregate > top-tier),
then the architecture has earned its first receipt.

Pricing: (A) sticky markup-over-replacement. No market clearing. No Walras.

Design note (v0 scope): money is a 2-account circuit — households vs a single
firm pool. The egg supply chain (supplier -> store) is modelled PHYSICALLY
(capacity, lead time, perishing) and the replacement price is an internal cost
signal that drives retail markup; splitting the firm into separate solvent
financial entities (so we can watch sectoral balance sheets) is v0.2.
Rationing is proportional (tier-neutral); ability-to-pay rationing is v0.2.
"""

from dataclasses import dataclass, field
from collections import deque
import numpy as np

SEED = 42
rng = np.random.default_rng(SEED)

# --------------------------------------------------------------------------
# Households: 5 income tiers (quintiles). Eggs are a staple — everyone eats a
# similar quantity, but because income rises steeply, the BUDGET SHARE of eggs
# falls with income (an Engel curve). The poor are also more captive (less
# elastic): they cannot not-buy the staple.
# --------------------------------------------------------------------------
N_PER_TIER = 200
TIERS = 5
N = N_PER_TIER * TIERS

tier_wage      = np.array([12., 20., 32., 55., 100.])   # income/tick by tier
tier_base_qty  = np.array([4.0, 4.5, 5.0, 5.5, 6.0])    # eggs/tick wanted at ref price
tier_elast     = np.array([-0.06, -0.08, -0.10, -0.13, -0.18])  # inelastic; poor most captive

tier_idx = np.repeat(np.arange(TIERS), N_PER_TIER)
h_wage   = tier_wage[tier_idx]
h_base   = tier_base_qty[tier_idx]
h_elast  = tier_elast[tier_idx]
h_money  = np.full(N, 50.0)        # initial household cash buffer

P_REF = 1.0                         # reference (pre-shock) retail egg price target
OTHER_PRICE = 1.0                   # composite "everything else", price fixed

# --------------------------------------------------------------------------
@dataclass
class Supplier:
    capacity: float                 # eggs producible / tick
    lead_time: int                  # ticks from production start to availability
    base_cost: float = 0.50         # unit production cost (the cost-push floor)
    markup: float = 0.25            # supplier's markup over cost -> replacement price
    inv: float = 0.0                # produced eggs available to ship
    target_inv: float = 0.0
    pipeline: deque = field(default_factory=deque)

    @property
    def replacement_price(self):
        return self.base_cost * (1.0 + self.markup)

@dataclass
class Store:
    target_inv: float
    shelf_life: int                 # ticks before an egg perishes
    markup: float = 0.60            # retail markup over replacement
    age_buckets: deque = field(default_factory=deque)  # (age, qty)

    @property
    def inv(self):
        return sum(q for _, q in self.age_buckets)

@dataclass
class Firm:
    money: float                    # single consolidated firm cash pool (v0)


# --------------------------------------------------------------------------
class Economy:
    def __init__(self):
        baseline_demand = float((tier_base_qty * N_PER_TIER).sum())  # ~5000 eggs/tick
        self.supplier = Supplier(
            capacity=baseline_demand * 1.05,
            lead_time=3,
            target_inv=baseline_demand * 2.0,
        )
        # warm the pipeline so we don't start starved
        for _ in range(self.supplier.lead_time):
            self.supplier.pipeline.append(self.supplier.capacity)
        self.supplier.inv = baseline_demand * 2.0

        self.store = Store(target_inv=baseline_demand * 4.0, shelf_life=4)
        # warm store inventory
        self.store.age_buckets.append((0, baseline_demand * 4.0))

        self.firm = Firm(money=200000.0)
        self.wagebill = float(h_wage.sum())

        # bookkeeping totals for the physical-conservation assert
        self.cum_produced = self.supplier.inv + sum(self.supplier.pipeline) + self.store.inv
        self.cum_consumed = 0.0
        self.cum_perished = 0.0

        self.M0 = float(h_money.sum()) + self.firm.money   # invariant target

        self.shock_active = False
        self._base_capacity = self.supplier.capacity

        # history
        self.hist = {k: [] for k in
                     ["t", "retail", "replacement", "store_inv", "supp_inv",
                      "money_resid", "egg_resid", "served_frac",
                      "cpi_agg"] + [f"cpi_t{t}" for t in range(TIERS)]}

        # per-tier pre-shock expenditure weights (filled after warmup)
        self.w_egg_tier = None
        self.w_egg_agg = None
        self._p0 = None

    # ----- one tick -------------------------------------------------------
    def step(self, t, shock=None):
        S, St, F = self.supplier, self.store, self.firm

        # 0. apply / lift shock to supplier capacity
        if shock is not None:
            S.capacity = self._base_capacity * (1.0 - shock)
        else:
            S.capacity = self._base_capacity

        # 1. SUPPLIER: pipeline advance + new production
        arrived = S.pipeline.popleft() if S.pipeline else 0.0
        S.inv += arrived
        produced = S.capacity
        S.pipeline.append(produced)
        self.cum_produced += produced

        # 2. SUPPLIER pricing: markup rises when its own stock runs tight
        s_ratio = S.inv / max(S.target_inv, 1e-9)
        S.markup += 0.03 * (1.0 - s_ratio)
        S.markup = float(np.clip(S.markup, 0.05, 4.0))
        repl = S.replacement_price

        # 3. STORE restock from supplier (PHYSICAL eggs; money is internal in v0)
        order = max(0.0, St.target_inv - St.inv)
        shipped = min(order, S.inv)
        S.inv -= shipped
        if shipped > 0:
            St.age_buckets.append((0, shipped))

        # 4. STORE perishing: age everything, drop the expired
        new_buckets = deque()
        for age, qty in St.age_buckets:
            age += 1
            if age >= St.shelf_life:
                self.cum_perished += qty
            else:
                new_buckets.append((age, qty))
        St.age_buckets = new_buckets
        store_inv = St.inv

        # 5. STORE retail pricing: sticky markup over replacement, inventory-adjusted
        inv_ratio = store_inv / max(St.target_inv, 1e-9)
        St.markup += 0.04 * (1.0 - inv_ratio)
        St.markup = float(np.clip(St.markup, 0.10, 4.0))
        retail = repl * (1.0 + St.markup)

        # 6. WAGES: firm -> households (pay first, so they can spend this tick)
        F.money -= self.wagebill
        h_money[:] += h_wage

        # 7. HOUSEHOLD egg demand (inelastic) + proportional rationing
        p0 = self._p0 if self._p0 else P_REF
        desired = h_base * (retail / p0) ** h_elast            # barely moves
        max_egg_budget = 0.6 * h_wage                          # can't spend everything on eggs
        affordable = max_egg_budget / max(retail, 1e-9)
        want = np.minimum(desired, affordable)
        total_want = float(want.sum())

        ration = 1.0 if total_want <= store_inv else store_inv / max(total_want, 1e-9)
        bought = want * ration
        served_frac = ration

        # consume eggs out of store inventory (oldest first)
        need = float(bought.sum())
        self._draw_from_store(St, need)
        self.cum_consumed += need

        # money: households -> firm for eggs
        egg_spend = bought * retail
        h_money[:] -= egg_spend
        F.money += float(egg_spend.sum())

        # 8. OTHER goods: spend remaining intended consumption (income) on "other"
        #    (unmet egg demand is simply saved -> stays as household money; conserved)
        other_spend = np.maximum(0.0, h_wage - egg_spend)
        # cap by cash on hand (never spend money you don't have)
        other_spend = np.minimum(other_spend, h_money)
        h_money[:] -= other_spend
        F.money += float(other_spend.sum())

        # 9. record per-tier expenditure shares during warmup to fix the basket
        egg_exp = egg_spend
        tot_exp = egg_spend + other_spend

        # ----- CONSERVATION ASSERTS (the whole point) ---------------------
        money_resid = (float(h_money.sum()) + F.money) - self.M0
        egg_resid = (self.cum_produced - self.cum_consumed - self.cum_perished) \
                    - (sum(self.supplier.pipeline) + S.inv + St.inv)
        assert abs(money_resid) < 1e-6, f"MONEY LEAK at t={t}: {money_resid:.3e}"
        assert abs(egg_resid) < 1e-6, f"EGG LEAK at t={t}: {egg_resid:.3e}"

        # ----- CPI computation (after weights are fixed) ------------------
        cpi_agg = np.nan
        cpi_tier = [np.nan] * TIERS
        if self.w_egg_tier is not None:
            price_rel = retail / self._p0
            cpi_agg = self.w_egg_agg * price_rel + (1 - self.w_egg_agg)
            for k in range(TIERS):
                cpi_tier[k] = self.w_egg_tier[k] * price_rel + (1 - self.w_egg_tier[k])

        # ----- history ----------------------------------------------------
        h = self.hist
        h["t"].append(t); h["retail"].append(retail); h["replacement"].append(repl)
        h["store_inv"].append(store_inv); h["supp_inv"].append(S.inv)
        h["money_resid"].append(money_resid); h["egg_resid"].append(egg_resid)
        h["served_frac"].append(served_frac); h["cpi_agg"].append(cpi_agg)
        for k in range(TIERS):
            h[f"cpi_t{k}"].append(cpi_tier[k])

        return retail, egg_exp, tot_exp

    def _draw_from_store(self, St, need):
        """Consume `need` eggs FIFO (oldest first) from age buckets."""
        remaining = need
        new_buckets = deque()
        for age, qty in St.age_buckets:
            if remaining <= 0:
                new_buckets.append((age, qty)); continue
            take = min(qty, remaining)
            qty -= take; remaining -= take
            if qty > 1e-12:
                new_buckets.append((age, qty))
        St.age_buckets = new_buckets


# --------------------------------------------------------------------------
def run(warmup=60, shock_t=80, shock_len=15, shock_frac=0.60, total=200):
    econ = Economy()

    # --- warmup to steady state, accumulating expenditure shares ---
    egg_acc = np.zeros(TIERS); tot_acc = np.zeros(TIERS)
    last_retail = P_REF
    for t in range(warmup):
        retail, egg_exp, tot_exp = econ.step(t)
        last_retail = retail
        if t >= warmup - 20:   # average the last 20 warmup ticks
            for k in range(TIERS):
                m = (tier_idx == k)
                egg_acc[k] += egg_exp[m].sum()
                tot_acc[k] += tot_exp[m].sum()

    # fix the pre-shock basket weights and reference price (Laspeyres)
    econ.w_egg_tier = egg_acc / np.maximum(tot_acc, 1e-9)
    econ.w_egg_agg = egg_acc.sum() / max(tot_acc.sum(), 1e-9)
    econ._p0 = last_retail

    # --- main run with a supply shock ---
    for t in range(warmup, total):
        in_shock = shock_t <= t < shock_t + shock_len
        econ.step(t, shock=shock_frac if in_shock else None)

    return econ


if __name__ == "__main__":
    econ = run()
    h = econ.hist
    import numpy as np

    money_leak = max(abs(x) for x in h["money_resid"])
    egg_leak   = max(abs(x) for x in h["egg_resid"])

    # peak retail inflation
    base_p = econ._p0
    peak_p = max(h["retail"])
    peak_infl = (peak_p / base_p - 1) * 100

    # distributional wedge at the peak tick
    peak_i = int(np.argmax(h["retail"]))
    bot = (h["cpi_t0"][peak_i] - 1) * 100
    top = (h[f"cpi_t{TIERS-1}"][peak_i] - 1) * 100
    agg = (h["cpi_agg"][peak_i] - 1) * 100

    print("=" * 64)
    print("CYBEERSYM v0 — PLUMBING TEST")
    print("=" * 64)
    print(f"  max |money residual| : {money_leak:.3e}   (must be ~0)")
    print(f"  max |egg residual|   : {egg_leak:.3e}   (must be ~0)")
    print("-" * 64)
    print(f"  pre-shock egg price  : {base_p:.4f}")
    print(f"  peak egg price       : {peak_p:.4f}   (+{peak_infl:.1f}%)")
    print(f"  min served fraction  : {min(h['served_frac']):.3f}  (rationing depth)")
    print("-" * 64)
    print(f"  egg budget share by tier (Engel): "
          + ", ".join(f"{w*100:.1f}%" for w in econ.w_egg_tier))
    print(f"  PERSONAL inflation at peak:")
    print(f"     bottom tier : +{bot:.2f}%")
    print(f"     aggregate   : +{agg:.2f}%")
    print(f"     top tier    : +{top:.2f}%")
    print(f"     regressive wedge (bottom - top): {bot - top:+.2f} pts")
    print("=" * 64)
