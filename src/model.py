"""
Cybeersym model (calibratable). Single perishable staple, stock-flow consistent,
sticky markup-over-replacement pricing with ROCKETS-AND-FEATHERS asymmetry:
markups rise fast on scarcity, fall slow on surplus (margin, once captured, is
defended). Conservation asserts retained — money and eggs may not leak.

1 tick == 1 month, so the model can be laid alongside monthly FRED data.
Economy owns its own household-money array so it can be re-run cleanly in a
calibration grid search.
"""
from dataclasses import dataclass, field
from collections import deque
from typing import NamedTuple, Optional
import numpy as np

# ---- fixed household structure (5 income quintiles) ----
N_PER_TIER = 200; TIERS = 5; N = N_PER_TIER * TIERS
tier_wage  = np.array([12., 20., 32., 55., 100.])
tier_base  = np.array([4.0, 4.5, 5.0, 5.5, 6.0])
tier_elast = np.array([-0.06, -0.08, -0.10, -0.13, -0.18])
tier_idx = np.repeat(np.arange(TIERS), N_PER_TIER)
h_wage  = tier_wage[tier_idx]
h_base  = tier_base[tier_idx]
h_elast = tier_elast[tier_idx]
OTHER_PRICE = 1.0

@dataclass
class Params:
    # rockets-and-feathers markup dynamics (up >> down)
    store_up: float = 0.45;  store_down: float = 0.04;  store_lo: float = 0.10;  store_hi: float = 6.0
    supp_up:  float = 0.35;  supp_down:  float = 0.03;  supp_lo:  float = 0.05;  supp_hi:  float = 6.0
    lead_time: int = 1
    shelf_life: int = 2          # months an egg stays sellable
    # shock
    shock_t: int = 30; shock_len: int = 9; shock_frac: float = 0.45

class PriceQuote(NamedTuple):
    """Frozen return contract for pricing. Callers read .price; the rest is
    diagnostics (and feeds the conservation/plot machinery). New fields may be
    APPENDED later without breaking any existing caller."""
    price: float
    tightness: float      # the flow gap that drove this quote (expected_demand / capacity)
    markup: float         # supplier markup state after the quote


def _adjust(markup, inv_ratio, up, down, lo, hi):
    signal = 1.0 - inv_ratio                 # >0 when short
    speed = up if signal > 0 else down       # rocket up, feather down
    return float(np.clip(markup + speed * signal, lo, hi))

class Economy:
    def __init__(self, P: Params, pricing: dict = None):
        self.P = P
        # COMMODITY pricing spec (egg slope lives here, not in engine Params).
        from pricers import EGG_PRICING, resolve
        self.pricing = dict(pricing or EGG_PRICING)
        self._pricer = resolve(self.pricing)
        self._pricer_knobs = {k: v for k, v in self.pricing.items() if k != "pricer"}
        base_demand = float((tier_base * N_PER_TIER).sum())
        self.base_demand = base_demand
        self.cap0 = base_demand * 1.05
        self.s_inv = base_demand * 0.5
        self.s_target = base_demand * 0.5
        self.s_markup = 0.25
        self.s_base_cost = 0.50
        self.pipe = deque([self.cap0] * P.lead_time)
        # store holds ~1 month of sales, seeded spread across age buckets so no perish-cliff
        self.st_target = base_demand
        n_ages = max(1, P.shelf_life)
        self.buckets = deque((a, base_demand / n_ages) for a in range(n_ages))
        self.st_markup = 0.60
        self.hm = np.full(N, 50.0)
        self.firm = 200000.0
        self.wagebill = float(h_wage.sum())
        self.cum_prod = self.s_inv + sum(self.pipe) + self._store_inv()
        self.cum_cons = 0.0; self.cum_per = 0.0
        self.M0 = float(self.hm.sum()) + self.firm
        self.p0 = None
        self.hist = {k: [] for k in ["retail","repl","tightness","store_inv","served","money_resid","egg_resid"]}

    def _store_inv(self):
        return sum(q for _, q in self.buckets)

    def supplier_price(self, flow_gap, *, deficit=0.0, demand_signal=None, horizon: int = 0) -> PriceQuote:
        """
        Price eggs off the FLOW GAP — a *leading* indicator — instead of realized
        inventory, a *lagging* stock. flow_gap = expected_demand / capacity; > 1
        means this month's output won't cover this month's demand, so the price
        firms NOW, before the shelf empties. This is the fix for the stockout
        deadzone the FRED series exposed (model stayed flat, then spiked).

        OPTION (i) — REACTIVE (this body): uses only the contemporaneous flow_gap.

        ### TODO(option ii — ANTICIPATION). `demand_signal` and `horizon` are WIRED
        ### AND DELIBERATELY UNUSED in v0. A forward-looking pricer would blend the
        ### realized flow_gap with an EXPECTED future gap assembled from
        ### `demand_signal` over the next `horizon` months — i.e. read announced
        ### USDA cull/depopulation the way wholesale & futures markets priced in
        ### scarcity *before* eggs actually went missing. That expectation gets
        ### something real to form on once step (b) lands real cull data. Until
        ### then: reactive only. These two args are accepted to freeze the
        ### interface, NOT because the body honors them yet.
        """
        # PROPORTIONAL cost-pass-through (P-controller, not I): price tracks the
        # CURRENT gap, so it peaks WITH scarcity and falls back as the gap closes —
        # the commodity behaviour the egg series demands. An accumulating (integral)
        # markup, by contrast, lags and ratchets (it peaks at the END of a shortage
        # and never feathers back). `supp_up` is the pass-through sensitivity.
        # Dispatch to the COMMODITY's pricer (slope is an egg property, held in
        # self.pricing — NOT an engine constant). Eggs reprice ~linearly in the
        # capacity DEFICIT; keying off `deficit` avoids the flow_gap 1/(1-d) convexity.
        markup = self._pricer(flow_gap, self.s_markup, deficit=deficit,
                              demand_signal=demand_signal, horizon=horizon,
                              **self._pricer_knobs)
        self.s_markup = markup
        price = self.s_base_cost * (1.0 + markup)
        ### TODO(branded goods): a sticky/asymmetric INTEGRAL term (rockets &
        ### feathers) belongs here for non-commodities; supp_down would govern its
        ### feather rate. Eggs are a commodity -> pure proportional for now.
        return PriceQuote(price=price, tightness=flow_gap, markup=markup)

    def step(self, t, cap_loss=0.0, demand_mult=1.0):
        P = self.P
        cap = self.cap0 * (1.0 - cap_loss)
        # supplier pipeline + production
        arr = self.pipe.popleft() if self.pipe else 0.0
        self.s_inv += arr
        self.pipe.append(cap); self.cum_prod += cap
        # supplier price: off the FLOW GAP (leading), not realized inventory (lagging)
        expected_demand = self.base_demand          # reactive (i): structural demand
        flow_gap = expected_demand / max(cap, 1e-9)
        quote = self.supplier_price(flow_gap, deficit=cap_loss)   # egg pricer keys off deficit
        repl = quote.price
        # store restock (physical eggs)
        order = max(0.0, self.st_target - self._store_inv())
        ship = min(order, self.s_inv); self.s_inv -= ship
        if ship > 0: self.buckets.append((0, ship))
        # perish
        nb = deque()
        for age, qty in self.buckets:
            age += 1
            if age >= P.shelf_life: self.cum_per += qty
            else: nb.append((age, qty))
        self.buckets = nb
        store_inv = self._store_inv()
        # store retail price (rockets & feathers)
        self.st_markup = _adjust(self.st_markup, store_inv/max(self.st_target,1e-9),
                                 P.store_up, P.store_down, P.store_lo, P.store_hi)
        retail = repl * (1 + self.st_markup)
        # wages firm->households
        self.firm -= self.wagebill; self.hm += h_wage
        # demand (inelastic) + proportional rationing
        p0 = self.p0 or retail
        desired = h_base * demand_mult * (retail/p0) ** h_elast   # seasonal demand scales base need
        afford = (0.6 * h_wage) / max(retail, 1e-9)
        want = np.minimum(desired, afford); tw = float(want.sum())
        served = 1.0 if tw <= store_inv else store_inv/max(tw,1e-9)
        bought = want * served
        self._consume(float(bought.sum())); self.cum_cons += float(bought.sum())
        spend = bought * retail
        self.hm -= spend; self.firm += float(spend.sum())
        other = np.minimum(np.maximum(0.0, h_wage - spend), self.hm)
        self.hm -= other; self.firm += float(other.sum())
        # conservation
        mr = (float(self.hm.sum()) + self.firm) - self.M0
        er = (self.cum_prod - self.cum_cons - self.cum_per) - (sum(self.pipe) + self.s_inv + self._store_inv())
        assert abs(mr) < 1e-6, f"money leak t={t}: {mr:.2e}"
        assert abs(er) < 1e-6, f"egg leak t={t}: {er:.2e}"
        h = self.hist
        h["retail"].append(retail); h["repl"].append(repl); h["tightness"].append(flow_gap); h["store_inv"].append(store_inv)
        h["served"].append(served); h["money_resid"].append(mr); h["egg_resid"].append(er)
        return retail

    def _consume(self, need):
        rem = need; nb = deque()
        for age, qty in self.buckets:
            if rem <= 0: nb.append((age, qty)); continue
            take = min(qty, rem); qty -= take; rem -= take
            if qty > 1e-12: nb.append((age, qty))
        self.buckets = nb

def run(P: Params, warmup=24, total=None, cull_path=None, demand_path=None, pricing=None):
    if cull_path is not None:
        total = len(cull_path)
    if total is None:
        total = P.shock_t + 30
    e = Economy(P, pricing=pricing)
    for t in range(warmup):
        last = e.step(t, cap_loss=0.0, demand_mult=1.0)
    e.p0 = last                       # fix baseline after warmup
    for k in range(total):
        if cull_path is not None:
            loss = cull_path[k]
        else:
            loss = P.shock_frac if (P.shock_t <= k < P.shock_t + P.shock_len) else 0.0
        dm = demand_path[k] if demand_path is not None else 1.0
        e.step(warmup + k, cap_loss=loss, demand_mult=dm)
    return e

if __name__ == "__main__":
    e = run(Params())
    h = e.hist
    print("money leak:", max(abs(x) for x in h["money_resid"]))
    print("egg leak  :", max(abs(x) for x in h["egg_resid"]))
    print(f"baseline {e.p0:.3f}  peak {max(h['retail']):.3f}  (+{(max(h['retail'])/e.p0-1)*100:.0f}%)")
