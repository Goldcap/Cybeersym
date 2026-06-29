"""
Cybeersym — chaos module (standalone, v0).

CYB-1 proved *amplification* (linear, bounded — a stationary demand blip rings up
the chain). Amplification is NOT chaos. This module asks the sharper, measurable
question: does the same conserved 3-tier supply chain, given a realistic
*nonlinear* ordering rule, generate **deterministic chaos** endogenously — bounded
aperiodic trajectories with sensitive dependence on initial conditions and a
positive largest Lyapunov exponent — as one behavioural parameter varies?

It reuses CYB-1's conserved physical flow (goods created only by the external
supplier, destroyed only by consumption; the residual stays < 1e-9) and swaps the
near-linear order-up-to rule for the documented **anchoring-and-adjustment**
heuristic (Sterman 1989; Mosekilde & Larsen 1988 showed it routes to chaos in the
beer game).

DISCIPLINE — chaos must be EARNED, not eyeballed (the spec's central guard):
  * Demand noise is OFF (sigma = 0). Any aperiodicity must come from the
    dynamics, not from random input — otherwise you cannot tell chaos from noise.
    The system is perturbed off its fixed point by a one-time initial-condition
    offset, then left alone.
  * Determinism is exact: the step map is a pure function of the state vector
    (no rng, no hidden mutation). Same initial state -> byte-identical trajectory.
  * Conservation still holds in the chaotic regime: chaos rides on a conserved
    substrate (trajectory unpredictable, goods conserved — the weather-prediction
    analogy). A conservation break is a bug, never "chaos".

THE ORDERING RULE (the chaos generator) — per tier, each step:

    D_hat   <- D_hat + theta*(received - D_hat)         # adaptive demand forecast
    S       =  inventory - backlog                       # current NET stock
    SL      =  on_order                                  # current supply line (in pipeline)
    SL_star =  L * D_hat                                 # desired supply line (cover lead time)
    order   =  max(0, D_hat + a_S*(S_star - S) + a_SL*(SL_star - SL))

The key behavioural parameter is the SUPPLY-LINE WEIGHT

    beta = a_SL / a_S

  beta = 1  -> the decision-maker fully credits orders already in the pipeline
               (does not re-order for gaps already on the way) -> stable.
  beta < 1  -> supply-line UNDERWEIGHTING (the documented human bias): the tier
               re-orders for gaps it has already addressed, over-corrects,
               oscillates. As beta falls, the chain goes
               stable -> oscillation -> period-doubling -> chaos.

The max(0, .) is a genuine nonlinearity (orders can't be negative); combined with
the lead-time delays and the feedback loop it is what makes chaos possible. A
purely linear rule can only decay or blow up — it cannot sustain a bounded
aperiodic attractor.

STATE VECTOR. So the reusable Lyapunov / bifurcation instruments can drive the
model without knowing its internals, the full deterministic state is exposed as a
flat float vector via `get_state()` / `set_state()`: per tier
[inventory, backlog, on_order, D_hat, *transit_in(L)]  ->  (4 + L) * n_tiers
scalars. `step_vector(vec) -> vec` is the pure map the instruments iterate.
"""
from collections import deque
from dataclasses import dataclass
import numpy as np

TIER_NAMES = ("retailer", "wholesaler", "manufacturer")


@dataclass
class ChaosParams:
    mu: float = 100.0          # constant consumer demand (sigma is 0 — noise OFF)
    L: int = 3                 # lead time between tiers, in steps (longer => more prone to instability)
    theta: float = 0.25        # demand-forecast smoothing (exponential)
    a_S: float = 0.5           # inventory-gap adjustment fraction
    beta: float = 1.0          # supply-line weight = a_SL / a_S  (THE control knob)
    S_star: float = 100.0      # desired net stock (inventory - backlog) at equilibrium
    n_tiers: int = 3
    perturb: float = 1.0       # one-time initial net-stock offset on the retailer (off the fixed point)

    @property
    def a_SL(self) -> float:
        return self.beta * self.a_S


class Tier:
    """One stage. State = on-hand inventory, downstream backlog, supply line
    (on_order = units ordered upstream not yet received), the adaptive demand
    forecast D_hat, and the inbound goods on a length-L transit delay line.

    Initialized AT the deterministic fixed point for constant demand mu: net
    stock = S_star, supply line full at mu*L, forecast = mu, pipeline carrying mu
    per step. At the fixed point the order rule returns exactly mu (both gaps
    zero), so an unperturbed run sits still — the dynamics only move once
    something is knocked off equilibrium."""

    def __init__(self, name: str, p: ChaosParams):
        self.name = name
        self.L = p.L
        self.inventory = p.S_star          # backlog 0 -> net stock = S_star
        self.backlog = 0.0
        self.on_order = p.mu * p.L          # supply line full (pipeline of mu, L deep)
        self.D_hat = p.mu                   # forecast seeded at the true mean
        self.transit_in = deque([p.mu] * p.L, maxlen=p.L)

    @property
    def net_stock(self) -> float:
        return self.inventory - self.backlog


class ChaosChain:
    """Three tiers in series with the anchoring-and-adjustment ordering rule and
    DETERMINISTIC (constant) consumer demand. External supply above tier 2 is
    infinite and fills every order in full after L steps (goods INJECTED there);
    the consumer below tier 0 is the constant demand source and the sink (goods
    CONSUMED there).

    Pure and deterministic: `step()` is a function of state only. The reusable
    instruments use `step_vector` / `get_state` / `set_state`.
    """

    # per-tier scalar layout in the flat state vector
    _BASE = 4  # inventory, backlog, on_order, D_hat  (transit_in adds L more)

    def __init__(self, p: ChaosParams):
        self.p = p
        self.tiers = [Tier(n, p) for n in TIER_NAMES[: p.n_tiers]]
        # one-time perturbation off the fixed point (a nonzero initial condition,
        # NOT a random kick) — gives the deterministic dynamics something to evolve.
        self.tiers[0].inventory += p.perturb

        self.injected = self._goods_in_system()
        self.consumed = 0.0
        self.max_residual = 0.0

    # ---- conserved-goods bookkeeping --------------------------------------
    def _goods_in_system(self) -> float:
        return (sum(t.inventory for t in self.tiers)
                + sum(sum(t.transit_in) for t in self.tiers))

    # ---- the ordering rule (the chaos generator) --------------------------
    def _order(self, tier: Tier, received: float) -> float:
        p = self.p
        tier.D_hat += p.theta * (received - tier.D_hat)     # adaptive forecast
        SL_star = p.L * tier.D_hat                           # desired supply line
        indicated = (tier.D_hat
                     + p.a_S * (p.S_star - tier.net_stock)   # inventory-gap correction
                     + p.a_SL * (SL_star - tier.on_order))   # supply-line-gap correction
        return max(0.0, indicated)                           # orders can't be negative

    # ---- one tick ----------------------------------------------------------
    def step(self) -> None:
        p = self.p
        incoming = p.mu                          # constant consumer demand (noise OFF)
        for i, tier in enumerate(self.tiers):
            # 1. receive arrivals shipped by upstream L steps ago
            arrival = tier.transit_in.popleft()
            tier.inventory += arrival
            tier.on_order -= arrival

            # 2. receive the downstream order (consumer demand for the retailer)
            tier.backlog += incoming

            # 3. ship downstream (or out of the system, for the retailer)
            shipped = min(tier.inventory, tier.backlog)
            tier.inventory -= shipped
            tier.backlog -= shipped
            if i == 0:
                self.consumed += shipped                       # leaves the system
            else:
                self.tiers[i - 1].transit_in.append(shipped)   # travels down, lag L

            # 4. order upstream via anchoring-and-adjustment; that order is the
            #    demand the upstream tier sees THIS step (the propagation).
            order = self._order(tier, incoming)
            tier.on_order += order
            if i == p.n_tiers - 1:
                tier.transit_in.append(order)   # filled by infinite supply, lag L
                self.injected += order          # goods CREATED here
            else:
                incoming = order

        # conservation: goods on hand + in transit == injected - consumed.
        # Tolerance is RELATIVE to the scale of goods moved (injected) so the test
        # stays at machine precision even when a runaway regime pushes totals to
        # millions — an absolute 1e-9 would trip on float round-off, not a leak.
        goods = self._goods_in_system()
        scale = max(1.0, abs(self.injected), abs(goods))
        residual = abs((self.injected - self.consumed) - goods)
        self.max_residual = max(self.max_residual, residual / scale)
        assert residual < 1e-9 * scale, f"GOODS LEAK: rel residual={residual/scale:.3e}"

    # ---- flat-state interface for the reusable instruments -----------------
    def get_state(self) -> np.ndarray:
        out = []
        for t in self.tiers:
            out.extend([t.inventory, t.backlog, t.on_order, t.D_hat])
            out.extend(t.transit_in)
        return np.asarray(out, dtype=float)

    def set_state(self, vec: np.ndarray) -> None:
        L = self.p.L
        stride = self._BASE + L
        for i, t in enumerate(self.tiers):
            b = i * stride
            t.inventory, t.backlog, t.on_order, t.D_hat = vec[b:b + 4]
            t.transit_in = deque(vec[b + 4:b + 4 + L], maxlen=L)

    def step_vector(self, vec: np.ndarray) -> np.ndarray:
        """Pure map for the Lyapunov estimator: state -> next state. Does not
        touch conservation bookkeeping (the perturbed twin is a math probe, not a
        second physical chain), so it never trips the conservation assert."""
        self.set_state(vec)
        self._step_no_conservation()
        return self.get_state()

    def _step_no_conservation(self) -> None:
        p = self.p
        incoming = p.mu
        for i, tier in enumerate(self.tiers):
            arrival = tier.transit_in.popleft()
            tier.inventory += arrival
            tier.on_order -= arrival
            tier.backlog += incoming
            shipped = min(tier.inventory, tier.backlog)
            tier.inventory -= shipped
            tier.backlog -= shipped
            if i != 0:
                self.tiers[i - 1].transit_in.append(shipped)
            order = self._order(tier, incoming)
            tier.on_order += order
            if i == p.n_tiers - 1:
                tier.transit_in.append(order)
            else:
                incoming = order

    # ---- convenience: run and record an observable -------------------------
    def run(self, n: int, observe=None) -> np.ndarray:
        obs = observe or (lambda c: c.tiers[-1].net_stock)
        out = np.empty(n)
        for k in range(n):
            self.step()
            out[k] = obs(self)
        return out
