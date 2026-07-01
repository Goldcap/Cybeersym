"""
Cybeersym — commodity pricer registry.

A pricer is a PURE function: (flow_gap, prev_markup, *, deficit, **knobs) -> markup.
The engine owns all state and builds the actual price (base_cost * (1+markup));
the pricer just maps scarcity -> markup. Same purity discipline as the events.

WHY THIS MODULE EXISTS (the architecture point):
The price-vs-scarcity SLOPE is a COMMODITY property, not an engine constant. How
violently a good reprices when supply tightens is a fact about THAT good's demand
inelasticity — eggs (a near-inelastic staple) reprice steeply and ~linearly;
something elastic barely moves. So the slope lives HERE, beside the commodity, and
the engine stays commodity-blind: it calls whatever pricer the commodity names,
with whatever knobs the commodity declares. Milk names its own pricer + slope;
microchips name theirs. The engine never learns what an egg is.

EMPIRICAL BASIS for the egg pricer (validated across two independent HPAI episodes):
retail egg price rises roughly LINEARLY in the missing-flock fraction (mildly
SATURATING), NOT convex. The slope is calibrated against the REAL NASS flock deficit
(CYB-7/CYB-9), out-of-sample discipline preserved (calibrate on ep1, validate on ep2):
  2022-23 peak (calibration):  7.6% real deficit -> +188%  (~24.7%/pt)
  2024-25 peak (out-of-sample):12.1% real deficit -> +272% (~22.5%/pt)
Calibrated on ep1 -> slope ~24.1; on the OOS ep2 the single linear slope OVERSHOOTS
(+~317% vs +272%), which quantifies the mild saturation (see TODO below).
NOTE ON THE 13 -> 24 RE-CHARACTERIZATION: the old ~13 was calibrated off the
synthetic cull-reconstruction deficit, which was ~2x too large (a compensating error:
too-big deficit x too-small slope ~= right price). CYB-7 fixed the deficit (real, ~half);
CYB-9 fixed the slope (~24) — two independently-correct values replace the pair. The
earlier convex miss came from pricing off flow_gap = 1/(1-deficit); keying off the
deficit directly removes that artifact.
"""
from typing import Callable, Dict


def linear_deficit(flow_gap, prev_markup, *, deficit=0.0, slope=11.0, hi=30.0,
                   demand_signal=None, horizon: int = 0) -> float:
    """Eggs: markup rises LINEARLY in the capacity deficit (the missing-flock
    fraction), at an egg-calibrated slope. Stateless — ignores prev_markup (eggs
    are a commodity; no integral ratchet). `demand_signal`/`horizon` accepted to
    hold the interface but unused (the dormant anticipation hooks)."""
    return float(min(slope * max(0.0, deficit), hi))


def power_deficit(flow_gap, prev_markup, *, deficit=0.0, slope=11.0, alpha=1.0, hi=30.0,
                  demand_signal=None, horizon: int = 0) -> float:
    """Eggs, CONCAVE variant: markup = slope·deficit**alpha. `alpha < 1` saturates
    (the per-point slope falls with depth); `alpha = 1` recovers `linear_deficit`
    exactly, so this nests the linear model — the clean form for the CYB-14
    linear-vs-concave OOS model comparison. Stateless, like `linear_deficit`."""
    return float(min(slope * (max(0.0, deficit) ** alpha), hi))


def saturating_deficit(flow_gap, prev_markup, *, deficit=0.0, A=3.0, k=8.0, hi=30.0,
                       demand_signal=None, horizon: int = 0) -> float:
    """Eggs, SATURATING variant: markup = A·(1−e^{−k·deficit}). A second concave
    family (bounded as deficit→∞) used only as a robustness check in the CYB-14
    model comparison — its per-point slope also falls with depth."""
    import math
    return float(min(A * (1.0 - math.exp(-k * max(0.0, deficit))), hi))


def proportional_flowgap(flow_gap, prev_markup, *, deficit=0.0, slope=8.0, hi=30.0,
                         demand_signal=None, horizon: int = 0) -> float:
    """The v0.5 pricer: markup proportional to flow-gap shortage. Convex in deficit
    (flow_gap = 1/(1-deficit)). Kept for provenance / behavior-preserving checks."""
    shortage = max(0.0, flow_gap - 1.0)
    return float(min(slope * shortage, hi))


PRICER_REGISTRY: Dict[str, Callable] = {
    "linear_deficit":      linear_deficit,
    "power_deficit":        power_deficit,
    "saturating_deficit":   saturating_deficit,
    "proportional_flowgap": proportional_flowgap,
}

# --------------------------------------------------------------------------- #
#  COMMODITY PROPERTY: the egg pricing spec. This is the thing that is
#  "egg-specific" — it names a pricer and carries eggs' calibrated slope.
#  (When eggs.yml lands, this dict is exactly what it deserializes to.)
# --------------------------------------------------------------------------- #
EGG_PRICING = {
    "pricer": "linear_deficit",
    "slope":  24.1,     # % retail rise per 1% REAL flock deficit; calibrated on ep1 (CYB-9)
    "hi":     40.0,
}
### RESOLVED(saturation) — CYB-14: the ep1-peak concavity (24.7 %/pt at 7.6% -> 22.5 %/pt at
### 12.1%) does NOT generalize. A linear-vs-concave model comparison calibrated on ep1's FULL
### monthly path and validated OOS on ep2's path (see v11_saturation.py) found: the power form
### markup=slope*deficit**alpha lands at alpha~=1.03 (NOT concave) with an OOS RMSE tie to
### linear (~0.3%), and the forced-concave saturating form A*(1-exp(-k*deficit)) is strictly
### WORSE. The concavity lives only BETWEEN the two peaks; on the path it's swamped by the
### shoulder months (a concave curve overshoots low-deficit prices). Verdict: within-noise at
### the path level -> KEEP THE LINEAR PRICER; don't carry an unearned second parameter. The
### `power_deficit` / `saturating_deficit` forms below are the comparison harness (not adopted).


def resolve(spec: dict) -> Callable:
    """Look up a commodity's pricer by name. Validates at load, not mid-sim."""
    name = spec["pricer"]
    if name not in PRICER_REGISTRY:
        raise KeyError(f"unknown pricer {name!r}; have {list(PRICER_REGISTRY)}")
    return PRICER_REGISTRY[name]
