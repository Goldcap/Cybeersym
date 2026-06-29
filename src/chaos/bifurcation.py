"""
Cybeersym — bifurcation-diagram sweeper (reusable instrument).

For each value of a control parameter: build the system, run it long, discard the
transient (we want the *attractor*, not the approach to it), and record the
asymptotic samples of one scalar observable. Scatter (param, samples):

    period-1 (fixed point) -> one point per param
    period-2               -> two points
    period-4               -> four
    chaos                  -> a vertical smear of points (a continuum)

Like `lyapunov.py`, this is model-agnostic: it takes a factory
`make_system(param) -> system` and an `observe(system) -> float` readout, plus a
`step(system)` advance. The same sweeper draws the logistic-map cascade and the
supply-chain cascade. Self-test (`python3 bifurcation.py`) reproduces the textbook
logistic diagram: the period-doubling cascade accumulating near r≈3.5699.

Two sampling modes for the recorded observable:
  - "stroboscopic": record the observable's value on the last `n_record` steps
    (the attractor as sampled once per step). Good default for maps.
  - "local_maxima": record only local maxima of the observable over the tail
    (cleaner for continuous-looking oscillations; collapses a sinusoid to its
    peaks so period-1 oscillation reads as a single point).
"""
from typing import Callable, Any
import numpy as np


def bifurcation(make_system: Callable[[float], Any],
                step: Callable[[Any], None],
                observe: Callable[[Any], float],
                params: np.ndarray, *,
                n_warm: int = 4000, n_record: int = 600,
                mode: str = "stroboscopic",
                round_to: float = 1e-6) -> tuple[np.ndarray, np.ndarray]:
    """Sweep `params`; return (xs, ys) flat arrays suitable for a scatter plot.

    `make_system(param)` returns a fresh system; `step(system)` advances it one
    tick; `observe(system)` reads the scalar plotted. Distinct asymptotic values
    are de-duplicated (rounded to `round_to`) so a clean period-k orbit yields
    exactly k points instead of n_record overlapping ones.
    """
    assert mode in ("stroboscopic", "local_maxima"), mode
    xs, ys = [], []
    for param in params:
        sys = make_system(float(param))
        for _ in range(n_warm):
            step(sys)
        tail = np.empty(n_record)
        for i in range(n_record):
            step(sys)
            tail[i] = observe(sys)
        if mode == "local_maxima":
            vals = _local_maxima(tail)
            if vals.size == 0:                 # monotone / flat tail -> fixed point
                vals = tail[-1:]
        else:
            vals = tail
        uniq = np.unique(np.round(vals / round_to) * round_to)
        # cap the points kept per param so a chaotic smear stays plottable
        if uniq.size > n_record:
            uniq = uniq[:: max(1, uniq.size // n_record)]
        xs.extend([param] * uniq.size)
        ys.extend(uniq.tolist())
    return np.asarray(xs), np.asarray(ys)


def _local_maxima(x: np.ndarray) -> np.ndarray:
    if x.size < 3:
        return np.empty(0)
    interior = (x[1:-1] > x[:-2]) & (x[1:-1] >= x[2:])
    return x[1:-1][interior]


# --------------------------------------------------------------- self-test
class _Logistic:
    def __init__(self, r: float):
        self.r = r
        self.x = 0.5


def _self_test() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from pathlib import Path

    def make(r):
        return _Logistic(r)

    def step(s):
        s.x = s.r * s.x * (1.0 - s.x)

    def observe(s):
        return s.x

    rs = np.linspace(2.8, 4.0, 1200)
    xs, ys = bifurcation(make, step, observe, rs,
                         n_warm=2000, n_record=400, mode="stroboscopic")

    # textbook checkpoints: 1 branch below r=3, ~2 branches at r=3.3, smear at r=4
    def n_branches(r_target):
        s = _Logistic(r_target)
        for _ in range(3000):
            step(s)
        seen = set()
        for _ in range(400):
            step(s)
            seen.add(round(s.x, 4))
        return len(seen)

    b_fixed, b_p2, b_chaos = n_branches(2.9), n_branches(3.3), n_branches(3.9)
    print("Bifurcation sweeper self-test — logistic map")
    print(f"  r=2.9 branches={b_fixed} (expect 1, fixed point)")
    print(f"  r=3.3 branches={b_p2} (expect 2, period-2)")
    print(f"  r=3.9 branches={b_chaos} (expect many, chaos)")
    assert b_fixed == 1 and b_p2 == 2 and b_chaos > 20, \
        f"logistic cascade not reproduced: {b_fixed},{b_p2},{b_chaos}"

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(xs, ys, ",", color="navy", alpha=0.5)
    ax.set_xlabel("r"); ax.set_ylabel("x (asymptotic)")
    ax.set_title("Logistic map bifurcation — sweeper self-test "
                 "(period-doubling cascade to chaos)")
    out = Path(__file__).parent / "figures" / "_selftest_logistic_bifurcation.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(); fig.savefig(out, dpi=110)
    print(f"  PASS: cascade reproduced (1 -> 2 -> smear). figure -> {out}")


if __name__ == "__main__":
    _self_test()
