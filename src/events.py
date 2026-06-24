"""
Cybeersym — adverse-event plugin layer.

An EVENT is a pure path transform: given a horizon and a clock, it emits a per-month
MULTIPLIER on one channel. That's the whole contract.

  channel "supply"  -> capacity multiplier   (1.0 = full capacity, 0.8 = 20% lost)
  channel "demand"  -> demand multiplier      (1.0 = normal,        1.1 = +10%)

Design choices (all the same discipline we used for the pricer seam):
  * NARROW, not general. Events touch exactly one of two channels — supply or
    demand. There is no concrete third channel yet, so there isn't one. (Feed/energy
    COST series will land as a third channel when we actually feed them; see the
    ### TODO(cost-matrix) note below — that's the matrix-into-the-mechanism hook.)
  * PURE & STATELESS. An event takes a clock, returns a path, holds nothing.
    Same inputs -> same outputs (the determinism we want to GUARD, not aspire to).
    Trivial to test, trivial to validate, impossible to leak.
  * MULTIPLICATIVE composition. Two supply events compose on the capacity multiplier
    (0.9 * 0.8 = 0.72, never "120% lost"); two demand events on the demand multiplier.
    Physically correct at the extremes; additive is not.
  * The commodity-specific guts (flock dynamics, sawmill lags, ...) live INSIDE the
    event, not in the engine. `HPAISupplyEvent` runs the flock-deficit transform;
    the engine only ever sees a capacity path. This is the "grad student owns a
    commodity module" architecture.

The engine (`model.run`) is untouched: this layer composes events into the two
driver paths it already accepts (cull_path = capacity LOSS, demand_path = mult).
"""
from typing import Protocol, runtime_checkable, List
from model import Params, run
from data.hpai_culls import DEPOP, BASELINE_FLOCK, flock_deficit_path
from data.seasonality import seasonal_factor


# --------------------------------------------------------------------------- #
#  Contract
# --------------------------------------------------------------------------- #
@runtime_checkable
class Event(Protocol):
    name: str
    channel: str                       # "supply" | "demand"
    def path(self, n: int, *, start_month: int = 1) -> List[float]:
        """Per-month multiplier over `n` months. `start_month` is the calendar
        month (1=Jan) of tick 0, so recurring events phase-align to the window."""
        ...


# --------------------------------------------------------------------------- #
#  Concrete events
# --------------------------------------------------------------------------- #
class HPAISupplyEvent:
    """Avian-flu supply shock. Carries the REAL USDA depopulation series and runs
    the flock-stock-with-replacement-lag transform to a capacity path. The cull
    DATA and the flock biology both live here — not in the engine."""
    channel = "supply"
    name = "hpai_2022"

    def __init__(self, depop=DEPOP, replace_lag: int = 12, baseline_flock=BASELINE_FLOCK):
        # replace_lag=12 is the EFFECTIVE recovery (not the 6-mo biological floor):
        # the flock ran ~5% below baseline for years (slow/incomplete/re-culled
        # replacements). Calibrated; to be confirmed by the real NASS layer-inventory
        # series, which would retire this assumption entirely.
        self.depop = depop
        self.replace_lag = replace_lag
        self.baseline_flock = baseline_flock

    def path(self, n, *, start_month=1):
        deficit = flock_deficit_path(self.depop, self.baseline_flock, self.replace_lag)
        # NOTE: depop series is month-aligned to the outbreak start (Jan 2022 = idx 0).
        # Assumes run tick 0 == that start. (A dated-window mapper is the general fix.)
        return [1.0 - (deficit[k] if k < len(deficit) else 0.0) for k in range(n)]


class SeasonalDemandEvent:
    """Recurring month-of-year demand pattern (holiday baking + winter laying drop),
    extracted from calm-year prices. A *recurring* event, not a year-specific one —
    this is what keeps the model mechanism-temporal, not timestamp-tuned."""
    channel = "demand"
    name = "seasonal_baseline"

    def __init__(self, factor=None):
        self.factor = list(seasonal_factor()) if factor is None else list(factor)

    def path(self, n, *, start_month=1):
        return [self.factor[(start_month - 1 + k) % 12] for k in range(n)]


class PulseSupplyShock:
    """Example of how cheap a NEW adverse event is: a rectangular capacity cut over
    a window. Port strike, drought, feed crisis — all this shape. ~10 lines."""
    channel = "supply"
    name = "pulse_supply"

    def __init__(self, start: int, length: int, depth: float):
        self.start, self.length, self.depth = start, length, depth

    def path(self, n, *, start_month=1):
        return [1.0 - (self.depth if self.start <= k < self.start + self.length else 0.0)
                for k in range(n)]


# Registry: the hook the future YAML resolves names against
# (events: [{type: hpai_2022, replace_lag: 12}, {type: seasonal_baseline}]).
EVENT_REGISTRY = {
    "hpai_2022":         HPAISupplyEvent,
    "seasonal_baseline": SeasonalDemandEvent,
    "pulse_supply":      PulseSupplyShock,
}

### TODO(cost-matrix): the third channel. When real feed-cost / natural-gas series
### arrive, a CostEvent (channel="cost") returns a per-month base_cost multiplier
### path, composed multiplicatively like the others, and `model.run` gains a
### `cost_path` arg that scales the supplier's base_cost (currently the constant
### 0.50). That is the "data matrix into the mechanism" seam: real input series
### feeding STRUCTURAL cost accounting, not regression weights. Channels stay
### narrow ({supply, demand, cost}) — added on contact with real data, not before.


# --------------------------------------------------------------------------- #
#  Validation (fail fast at load, never deep in the sim loop)
# --------------------------------------------------------------------------- #
def validate_event(ev, n=24, start_month=1):
    assert isinstance(ev, Event), f"{ev!r} does not satisfy the Event protocol"
    assert ev.channel in ("supply", "demand"), f"{ev.name}: bad channel {ev.channel!r}"
    p = ev.path(n, start_month=start_month)
    assert len(p) == n, f"{ev.name}: path length {len(p)} != {n}"
    assert all(isinstance(v, (int, float)) for v in p), f"{ev.name}: non-numeric path value"
    if ev.channel == "supply":
        assert all(0.0 <= v <= 1.0 + 1e-9 for v in p), f"{ev.name}: capacity mult outside [0,1]"
    else:
        assert all(v > 0.0 for v in p), f"{ev.name}: demand mult must be > 0"
    return True


# --------------------------------------------------------------------------- #
#  Composition + run
# --------------------------------------------------------------------------- #
def compose(events, n, *, start_month=1):
    """Multiply same-channel events into one supply mult path and one demand mult path."""
    supply = [1.0] * n
    demand = [1.0] * n
    for ev in events:
        validate_event(ev, n, start_month)
        p = ev.path(n, start_month=start_month)
        if ev.channel == "supply":
            supply = [a * b for a, b in zip(supply, p)]
        else:
            demand = [a * b for a, b in zip(demand, p)]
    return supply, demand


def run_with_events(P: Params, events, n, *, warmup=24, start_month=1):
    """Compose events -> two driver paths -> the (untouched) engine. Conservation
    asserts fire inside run() exactly as before."""
    supply_mult, demand_mult = compose(events, n, start_month=start_month)
    cull_path = [1.0 - s for s in supply_mult]          # engine wants LOSS fraction
    return run(P, warmup=warmup, cull_path=cull_path, demand_path=demand_mult)


# --------------------------------------------------------------------------- #
#  Behavior-preserving test: the refactor must reproduce v0.5's 0.86 EXACTLY.
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    import numpy as np
    from data.eggs_fred import window

    labels, real = window((2022, 1), (2023, 12))
    _, base = window((2021, 1), (2021, 12))
    r = np.array(real) / np.mean(base)

    P = Params(supp_up=8.0, store_up=0.06, store_hi=2.5, supp_hi=30.0)

    # (1) old path: hand-assembled cull_path + demand_path
    from data.hpai_culls import flock_deficit_path as fdp
    old_cull = fdp(replace_lag=12)
    old_dem = [seasonal_factor()[k % 12] for k in range(24)]
    e_old = run(P, warmup=24, cull_path=old_cull, demand_path=old_dem)
    m_old = np.array(e_old.hist["retail"][24:48]) / e_old.p0

    # (2) new path: through the event plugin
    e_new = run_with_events(P, [HPAISupplyEvent(replace_lag=12), SeasonalDemandEvent()],
                            n=24, start_month=1)
    m_new = np.array(e_new.hist["retail"][24:48]) / e_new.p0

    diff = float(np.max(np.abs(m_new - m_old)))
    corr = float(np.corrcoef(m_new, r)[0, 1])
    print("=" * 60)
    print("EVENT REFACTOR — behavior-preserving check")
    print("=" * 60)
    print(f"  max |new - old| price path : {diff:.2e}   (must be ~0)")
    print(f"  corr vs real (new pipeline): {corr:+.3f}   (must equal v0.5 0.856)")
    print(f"  peak month                 : {labels[int(m_new.argmax())]}")
    print("-" * 60)

    # composition demo: a NEW adverse event stacks multiplicatively, for free
    e_stack = run_with_events(
        P,
        [HPAISupplyEvent(replace_lag=12), SeasonalDemandEvent(),
         PulseSupplyShock(start=18, length=3, depth=0.25)],   # hypothetical extra shock
        n=24, start_month=1)
    m_stack = np.array(e_stack.hist["retail"][24:48]) / e_stack.p0
    leak = max(max(abs(x) for x in e_stack.hist["money_resid"]),
               max(abs(x) for x in e_stack.hist["egg_resid"]))
    print("  composition demo: + PulseSupplyShock(18,3,0.25)")
    print(f"    peak {m_stack.max():.2f} (was {m_new.max():.2f}); conservation leak {leak:.0e}")
    print(f"    registry: {list(EVENT_REGISTRY)}")
    print("=" * 60)
