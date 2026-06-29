"""
Cybeersym — largest Lyapunov exponent estimator (reusable instrument).

The load-bearing measurement of CYB-2: chaos is *defined* by a positive largest
Lyapunov exponent (λ), not by wiggly-looking output. This module estimates λ for
any deterministic discrete map and is model-agnostic on purpose — it operates on
a `step(state) -> state` callable and a flat state vector, so the same instrument
reads the logistic map (1-D), the supply chain (high-D), and every future
mechanism. Build it clean and general; do not bolt it to one model.

METHOD — Benettin two-trajectory (the standard discrete-map estimator):

    1. Evolve a reference trajectory.
    2. Hold a second trajectory a tiny separation d0 away.
    3. Each step: advance both, measure the new separation d, accumulate
       log(d / d0), then RENORMALIZE the perturbed point back to distance d0
       from the reference along the current separation direction (so the
       separation keeps sampling the *local* stretching rate and never saturates
       on the attractor).
    4. After discarding a transient, λ = mean( log(d / d0) ) per step.

    λ > 0  => exponential divergence => chaos (sensitive dependence).
    λ = 0  => marginal (limit cycle, quasiperiodic).
    λ < 0  => convergence to a fixed point / stable periodic orbit.

Renormalizing along the separation vector projects onto the most-expanding
direction; iterated, this converges to the LARGEST Lyapunov exponent (the others
require the full Gram-Schmidt / QR spectrum, out of scope for v0).

SELF-TEST (required, mirrors CYB-1's frozen-forecast guard): the logistic map
x -> r*x*(1-x) at r=4 has the exact analytic value λ = ln 2 ≈ 0.6931. Run
`python3 lyapunov.py` to confirm the estimator reproduces it (and λ < 0 in a
periodic window) BEFORE trusting its verdict on the supply chain. An instrument
that cannot read a known chaotic map tells you nothing about an unknown one.
"""
from typing import Callable
import numpy as np

Vec = np.ndarray
StepFn = Callable[[Vec], Vec]


def largest_lyapunov(step: StepFn, state0: Vec, *, n_steps: int = 20000,
                     transient: int = 2000, d0: float = 1e-9) -> float:
    """Largest Lyapunov exponent of the map `step`, started from `state0`.

    `step` must be a PURE function of the state vector (deterministic; no hidden
    mutation of shared state between the two trajectories). `state0` is a 1-D
    float array. Returns λ in units of (nats per step).
    """
    ref = np.asarray(state0, dtype=float).copy()
    # perturb along an arbitrary axis; the direction self-corrects within a few
    # steps as it aligns with the most-expanding direction.
    pert = ref.copy()
    pert[0] += d0

    log_growth = 0.0
    counted = 0
    for k in range(n_steps):
        ref = step(ref)
        pert = step(pert)
        diff = pert - ref
        d = float(np.linalg.norm(diff))
        if d == 0.0:
            # trajectories collapsed (deep into a stable fixed point); re-seed the
            # separation so the average keeps reading the local (contracting) rate.
            pert = ref.copy()
            pert[0] += d0
            if k >= transient:
                log_growth += np.log(d0 / d0)  # == 0; a contraction step
                counted += 1
            continue
        if k >= transient:
            log_growth += np.log(d / d0)
            counted += 1
        # renormalize: pull the perturbed point back to distance d0 along `diff`.
        pert = ref + diff * (d0 / d)
    return log_growth / max(counted, 1)


# --------------------------------------------------------------- self-test
def _logistic_step(r: float) -> StepFn:
    def step(x: Vec) -> Vec:
        return r * x * (1.0 - x)
    return step


def _self_test() -> None:
    print("Lyapunov estimator self-test — logistic map x -> r*x*(1-x)")
    print(f"  {'r':>6}{'regime':>16}{'measured λ':>14}{'analytic':>14}")

    cases = [
        (4.0, "full chaos", np.log(2.0)),     # exact: λ = ln 2
        (3.5, "period-4", None),               # stable cycle -> λ < 0
        (3.2, "period-2", None),               # stable cycle -> λ < 0
        (2.8, "fixed point", None),            # stable fixed point -> λ < 0
        (3.7, "chaotic band", None),           # λ > 0, no clean closed form
    ]
    ln2 = np.log(2.0)
    for r, label, analytic in cases:
        lam = largest_lyapunov(_logistic_step(r), np.array([0.123456]),
                               n_steps=60000, transient=2000)
        a = f"{analytic:.4f}" if analytic is not None else "    —"
        print(f"  {r:>6.2f}{label:>16}{lam:>14.4f}{a:>14}")

    # the load-bearing assertions: r=4 hits ln 2; periodic windows are negative.
    lam4 = largest_lyapunov(_logistic_step(4.0), np.array([0.123456]),
                            n_steps=200000, transient=5000)
    assert abs(lam4 - ln2) < 0.02, f"r=4 should give ln2≈{ln2:.4f}, got {lam4:.4f}"
    lam_periodic = largest_lyapunov(_logistic_step(3.2), np.array([0.4]),
                                    n_steps=60000, transient=5000)
    assert lam_periodic < -0.01, f"period-2 window should be λ<0, got {lam_periodic:.4f}"
    print(f"\n  PASS: r=4 λ={lam4:.5f} matches ln2={ln2:.5f} (|Δ|<0.02); "
          f"period-2 λ={lam_periodic:.4f} < 0.")
    print("  Instrument trusted. Safe to read the supply chain.")


if __name__ == "__main__":
    _self_test()
