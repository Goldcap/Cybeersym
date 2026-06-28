"""
Cybeersym — bullwhip module (standalone, v0).

The smallest honest 3-tier supply chain that amplifies order variance — the
bullwhip effect — from **demand-signal processing under local information**: each
tier estimates the demand mean from the orders it sees (a moving-average
forecast) and runs an order-up-to policy whose target moves with that estimate.
Lead time multiplies the effect. This isolates the **recursion** channel of
THESIS.md (propagation through input-output linkages) with no price-expectations
confound — estimating demand is statistical inference under incomplete
information, NOT anticipating inflation.

WHY A MOVING-AVERAGE FORECAST AND NOT A CONSTANT TARGET (the math the v0 spec
turns on): with a *constant* order-up-to level S, the order each period exactly
equals the demand observed that period (refill S, demand depleted it by D_t, so
re-order D_t) — variance out = variance in, ratio = 1 for ANY lead time. So
bullwhip is not lead-time alone. It needs S_t to MOVE with a demand estimate: a
single high observation both depletes inventory AND raises the target, so the
tier orders extra to refill and extra to re-level — that double response is the
amplification. Lead time scales the target (L+1) and multiplies it. This is the
canonical mechanism (Chen, Drezner, Ryan & Simchi-Levi 2000). The constant-S
case is kept as `forecast="frozen"` — a regression test that must read ~1.

CONSERVATION is the crown jewel, as in the egg engine: goods are created only by
the external supplier at the top, destroyed only by consumption at the bottom.
Every step,
    injected - consumed == sum(inventories) + sum(goods in transit)   (< 1e-9)
Variance may amplify; goods may not leak. Conserve-but-amplify is the whole
sanity check.

DETERMINISM is guarded: one seeded numpy Generator threaded through. Same seed ->
identical arrays.

----------------------------------------------------------------------------
THE SYSTEM

    consumer -> [retailer] -> [wholesaler] -> [manufacturer] -> (external supply)
                  tier 0         tier 1            tier 2

Goods flow DOWN with lead-time lag L (transit lines). Orders flow UP. Each tier
holds on-hand `inventory`, owed-downstream `backlog`, tracks `on_order` (units
ordered upstream but not yet received — this is `sum(pipeline)` in the spec's
terms; identical while upstream fills in full, and conservation-faithful when it
cannot), and keeps a length-`p` window of observed demand for its forecast.

PER STEP, PER TIER (downstream -> upstream evaluation; fixed and part of the spec):
  1. Receive arrivals: goods the upstream shipped L steps ago land now.
  2. Receive demand: the incoming order from downstream (consumer D_t for tier 0)
     is added to backlog AND fed to the forecast window.
  3. Ship: shipped = min(inventory, backlog) -> travels to the tier below (or
     leaves the system as consumption, for the retailer).
  4. Order: order_qty = max(0, S_t - inventory_position), where
        demand_hat = mean(last p observed demands)
        S_t        = demand_hat*(L+1) + z*sigma*sqrt(L+1)
     This order is the demand the upstream tier sees, and is what we measure.

THE THREE MODES (the killer experiment) — separating SEEING from ACTING:
  local_info  (default): a tier forecasts demand_hat from the (already-distorted)
                         ORDERS it receives, and replenishes against its own
                         (distorted) installation inventory position.
                         -> COMPOUNDS up the chain (~ r, r^2, r^3 vs true demand).
  shared_info:           a tier forecasts demand_hat from TRUE consumer demand
                         D_t, but STILL replenishes the distorted orders it
                         physically received (installation position). Sharing the
                         forecast de-distorts only ONE of two channels.
                         -> compounding SUPPRESSED but NOT flat: received-order
                            variance still leaks through the inventory-position
                            channel. Seeing true demand != acting on it.
  coordinated:           echelon-style — a tier both forecasts off true demand
                         AND replenishes against true END-demand (an echelon
                         position depleted by D_t, not by received orders). Both
                         channels de-distorted.
                         -> FLAT ~ r across the chain (cumulative vs true demand):
                            each stage near the single-stage Chen ratio, no
                            compounding. This is the installation- vs
                            echelon-base-stock distinction in the literature.

The three-way contrast decomposes the bullwhip: local->shared is the forecast
(information) channel; shared->coordinated is the physical replenishment channel.

`forecast="frozen"` holds demand_hat at the true mean (constant S) -> ratio ~1
at every stage: the p->infinity limit and the harness's regression test.
"""
from collections import deque
from dataclasses import dataclass
import numpy as np

TIER_NAMES = ("retailer", "wholesaler", "manufacturer")


@dataclass
class ChainParams:
    mu: float = 100.0          # mean consumer demand
    sigma: float = 10.0        # consumer demand noise sd
    L: int = 2                 # lead time between tiers, in steps
    p: int = 5                 # moving-average forecast window
    z: float = 2.0             # safety factor
    T: int = 400               # run length
    warmup: int = 100          # transient steps discarded before measuring (>> p)
    n_tiers: int = 3           # three, not N
    seed: int = 0

    @property
    def safety(self) -> float:
        # z * (lead-time demand sd over the lead+review period); flat, documented.
        return self.z * self.sigma * np.sqrt(self.L + 1)


class Tier:
    """One stage. Owns on-hand inventory, downstream backlog, the units it is
    still owed from upstream (on_order), inbound goods on a length-L delay line
    (transit_in), and a length-p window of observed demand for the forecast."""

    def __init__(self, name: str, p: ChainParams):
        self.name = name
        self.L = p.L
        # Steady-state start: forecast window seeded at mu (so demand_hat=mu and
        # S_0 = mu*(L+1)+safety), a full length-L in-transit pipeline of mu, and
        # inventory at the safety+one-period level -> initial position == S_0,
        # no startup kick from the buffers.
        self.inventory = p.mu + p.safety
        self.backlog = 0.0
        self.on_order = p.mu * p.L
        self.transit_in = deque([p.mu] * p.L, maxlen=p.L)
        self.window = deque([p.mu] * p.p, maxlen=p.p)
        # echelon position for `coordinated` mode: an inventory position depleted
        # by TRUE end-demand instead of received orders. Starts at S_0.
        self.coord_pos = p.mu * (p.L + 1) + p.safety

    @property
    def inventory_position(self) -> float:
        return self.inventory - self.backlog + self.on_order


class SupplyChain:
    """Three tiers in series. external supply above tier 2 is infinite and fills
    every order in full after L steps (goods INJECTED there). The consumer below
    tier 0 is the demand source and the sink (goods CONSUMED there)."""

    def __init__(self, p: ChainParams, mode: str = "local_info",
                 forecast: str = "moving_average"):
        assert mode in ("local_info", "shared_info", "coordinated"), mode
        assert forecast in ("moving_average", "frozen"), forecast
        self.p = p
        self.mode = mode
        self.forecast = forecast
        self.rng = np.random.default_rng(p.seed)
        self.tiers = [Tier(n, p) for n in TIER_NAMES[: p.n_tiers]]

        # consumer demand path (the boring, stationary input), clamped >= 0.
        self.demand = np.maximum(0.0, p.mu + self.rng.normal(0, p.sigma, p.T))

        # recorded series: what each tier PLACED, and the demand it RECEIVED.
        self.orders_placed = np.zeros((p.n_tiers, p.T))
        self.demand_received = np.zeros((p.n_tiers, p.T))

        # goods accounting for the conservation invariant.
        self.injected = self._goods_in_system()
        self.consumed = 0.0
        self.max_residual = 0.0

    def _goods_in_system(self) -> float:
        return (sum(t.inventory for t in self.tiers)
                + sum(sum(t.transit_in) for t in self.tiers))

    def _order_up_to(self, tier: Tier, observed: float, true_demand: float) -> float:
        """Update the tier's forecast from `observed` demand and return the order
        = max(0, S_t - position). `local`/`shared` order against the installation
        inventory position (depleted by received orders); `coordinated` orders
        against an echelon position depleted by TRUE end-demand."""
        p = self.p
        if self.forecast == "frozen":
            demand_hat = p.mu                    # p -> infinity limit; S constant
        else:
            tier.window.append(observed)
            demand_hat = float(np.mean(tier.window))
        S_t = demand_hat * (p.L + 1) + p.safety
        if self.mode == "coordinated":
            tier.coord_pos -= true_demand        # true end-demand depletes the echelon position
            order = max(0.0, S_t - tier.coord_pos)
            tier.coord_pos += order              # refill to S_t
            return order
        return max(0.0, S_t - tier.inventory_position)

    def step(self, t: int) -> None:
        p = self.p
        incoming = self.demand[t]               # tier 0's downstream is the consumer
        for i, tier in enumerate(self.tiers):
            # 1. receive arrivals (shipped by upstream L steps ago)
            arrival = tier.transit_in.popleft()
            tier.inventory += arrival
            tier.on_order -= arrival

            # 2. receive demand
            tier.backlog += incoming
            self.demand_received[i, t] = incoming

            # 3. ship downstream (or out of the system, for the retailer)
            shipped = min(tier.inventory, tier.backlog)
            tier.inventory -= shipped
            tier.backlog -= shipped
            if i == 0:
                self.consumed += shipped                       # leaves the system
            else:
                self.tiers[i - 1].transit_in.append(shipped)   # travels down, lag L

            # 4. order upstream. local: forecast off the (distorted) order this tier
            #    received; shared/coordinated: forecast off TRUE consumer demand
            #    (coordinated additionally replenishes against true demand).
            observed = incoming if self.mode == "local_info" else self.demand[t]
            order = self._order_up_to(tier, observed, self.demand[t])
            tier.on_order += order
            self.orders_placed[i, t] = order

            if i == p.n_tiers - 1:
                # tier 2 orders from the infinite external supplier: filled in full
                # after L. Goods are CREATED here (injected into the system).
                tier.transit_in.append(order)
                self.injected += order
            else:
                incoming = order                # the upstream tier sees this, this step

        # conservation: goods in = injected - consumed, to machine precision.
        residual = abs((self.injected - self.consumed) - self._goods_in_system())
        self.max_residual = max(self.max_residual, residual)
        assert residual < 1e-9, f"GOODS LEAK at t={t}: residual={residual:.3e}"

    def run(self) -> "SupplyChain":
        for t in range(self.p.T):
            self.step(t)
        return self
