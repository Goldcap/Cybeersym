"""
Cybeersym — critical slowing down (CSD): a model-free, scale-free early-warning instrument.  CYB-40.

CSD (Scheffer et al. 2009) is the early-warning signature of an approaching **local** bifurcation: as
a parameter drifts toward the transition, the equilibrium's recovery rate → 0, so under noise the
fluctuation **variance rises** and the **lag-1 autocorrelation (AR1) → 1**. It is the *topological,
scale-free* bridge to data the project needs — "when/how, not how much": var↑ / AR1→1 is a *shape*,
not a magnitude, so it needs no fit and no unit-matching (it is invariant under rescaling the axis).

SCOPE — a real boundary, self-tested in `run_v0.py`, not a limitation to hide:
  * CSD **fires** at LOCAL bifurcations (fold, Hopf, flip) — the equilibrium itself losing stability
    as a *parameter* drifts. The recovery rate slows; the warning is audible.
  * CSD is **blind** to GLOBAL / basin crossings (the equilibrium stays stable; a shock throws the
    system over a watershed) and to abrupt knife-edges. Nothing softens ⇒ no warning exists to detect.
  * That blindness is CORRECT and is what makes the instrument trustworthy — it discriminates
    forecastable (local) from unforecastable (global/shock) transitions rather than crying wolf.

This module is a reusable diagnostic (a candidate for promotion into `src/chaos/` alongside
`linearize`/`lyapunov` once it has earned a second use). Deterministic given a seed: the noise is a
*diagnostic perturbation* (CSD is inherently a fluctuation phenomenon), and the same seed ⇒
byte-identical output — the σ=0 discipline is preserved for the underlying deterministic maps.
numpy only.
"""
import numpy as np


def var_ar1(series, burn: float = 0.25):
    """The two CSD signatures of a (stationary) scalar series, after discarding a `burn` fraction as
    transient: (variance, lag-1 autocorrelation). Both rise toward a local bifurcation."""
    x = np.asarray(series, dtype=float)
    x = x[int(len(x) * burn):]
    x = x - x.mean()
    v = float(x.var())
    a = float(np.corrcoef(x[:-1], x[1:])[0, 1]) if v > 1e-300 and x.size > 2 else float("nan")
    return v, a


def noisy_series(step, x0, n: int, rng, sigma: float, observe=None, kick=None):
    """Iterate a deterministic map `step(x)->x` from `x0` with additive Gaussian noise, recording a
    scalar `observe(x)->float` each step. `kick(x, e)->x` applies the noise `e` (default: adds it to
    the first coordinate); `observe` defaults to the first coordinate. Returns the series (length n)."""
    obs = observe or (lambda x: float(np.ravel(x)[0]))
    add = kick or (lambda x, e: _add_first(x, e))
    x = x0
    out = np.empty(n)
    for k in range(n):
        x = add(step(x), sigma * rng.standard_normal())
        out[k] = obs(x)
    return out


def _add_first(x, e):
    x = np.array(np.ravel(x), dtype=float)
    x[0] += e
    return x if x.size > 1 else x[0]


def csd_curve(build_step, params, x_star, *, sigma, n=60000, seed=0, observe=None, kick=None):
    """(var, AR1) vs a swept `params`. `build_step(p) -> step(x)->x` is the deterministic map at p;
    `x_star(p) -> x0` seeds each run near the stable state (so we measure fluctuations, not a
    transient). Same seed for every p ⇒ the comparison across p is apples-to-apples and reproducible.
    A CSD signature is var monotonically ↑ and AR1 → 1 as p → the bifurcation."""
    rows = []
    for p in params:
        rng = np.random.default_rng(seed)
        rows.append(var_ar1(noisy_series(build_step(p), x_star(p), n, rng, sigma, observe, kick)))
    return rows


# ---- the analytic FOLD normal form: the built-in control CSD MUST fire on ----
def fold_normal_form(r: float, dt: float = 0.1):
    """Saddle-node/fold `dx/dt = r + x²` (bifurcation at r=0). For r<0 the stable fixed point is
    x* = −√(−r), and the Euler map `x ← x + dt(r+x²)` has multiplier μ = 1 + 2·dt·x* → 1 as r→0⁻
    (recovery slows). Returns (x_star, deterministic_step, mu) — the ground-truth CSD control."""
    xstar = -np.sqrt(-r)
    mu = 1.0 + 2.0 * dt * xstar
    def step(x):
        x = float(np.ravel(x)[0])
        return x + dt * (r + x * x)
    return xstar, step, mu
