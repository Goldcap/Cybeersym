"""
Cybeersym — linearization instrument (reusable): Jacobian, fixed points, eigenvalues.

Built to *name* a bifurcation rigorously rather than infer it from a picture. For a
discrete map `step(state) -> state` it provides:

  - `jacobian`      — central finite-difference linearization at a point.
  - `fixed_point_iterate` — the fixed point in a STABLE regime (just iterate the map;
                      guaranteed to land on the physically realized equilibrium).
  - `fixed_point_newton`  — Newton continuation (uses the Jacobian) to track a fixed
                      point as a parameter moves, including just past where it
                      stops being attracting.
  - `eigs` / `leading_complex` — spectrum and the largest-modulus complex pair.

Model-agnostic on purpose (operates on a callable + a flat state vector), like
`lyapunov.py` and `bifurcation.py` — the next mechanism reuses it unchanged.

WHY THIS MATTERS FOR CYB-2 (the border-collision finding). Whether the supply
chain's route to chaos is a smooth Hopf/Neimark–Sacker (eigenvalue pair crosses the
unit circle) or a *border-collision* (the equilibrium hits a switching manifold of
the piecewise-linear map while still linearly stable) cannot be read off a
trajectory — it requires the eigenvalues of the linearization at the physical fixed
point. This instrument supplies them; the verdict was border-collision (the leading
pair tops out at |λ|≈0.91 and the fixed point loses feasibility before any crossing).

CAVEAT — piecewise-smooth maps. The model has kinks (`max(0, order)`,
`ship=min(inventory, backlog)`). The Jacobian is only meaningful where the fixed
point is INTERIOR to a smooth branch; on a kink the finite difference depends on eps
and direction. `jacobian` exposes `eps`; always check eps-insensitivity (the CYB-2
fixed point is interior to its branch and passes — identical spectrum for
eps ∈ {1e-3,1e-5,1e-7}). Newton can also walk a root THROUGH a kink into an
unphysical branch; `fixed_point_newton` returns the root and you must check it is
physically valid (e.g. non-negative inventories / supply lines) before trusting it.

SELF-TEST (`python3 linearize.py`): the logistic map x→r·x·(1−x) has fixed point
x*=1−1/r with exact multiplier f'(x*)=2−r. The instrument must recover 2−r (and find
x*) before it is trusted on the supply chain — same discipline as the Lyapunov and
bifurcation self-tests.
"""
from typing import Callable
import numpy as np

Vec = np.ndarray
StepFn = Callable[[Vec], Vec]


def jacobian(step: StepFn, x: Vec, eps: float = 1e-6) -> np.ndarray:
    """Central finite-difference Jacobian of `step` at `x`. Column j is
    (step(x + eps e_j) − step(x − eps e_j)) / (2 eps)."""
    x = np.asarray(x, dtype=float)
    n = x.size
    J = np.empty((n, n))
    for j in range(n):
        dp = x.copy(); dp[j] += eps
        dm = x.copy(); dm[j] -= eps
        J[:, j] = (np.asarray(step(dp)) - np.asarray(step(dm))) / (2.0 * eps)
    return J


def fixed_point_iterate(step: StepFn, x0: Vec, n: int = 200000) -> Vec:
    """Fixed point by plain iteration — valid only where it is ATTRACTING. Returns
    the physically realized equilibrium in a stable regime."""
    x = np.asarray(x0, dtype=float).copy()
    for _ in range(n):
        x = np.asarray(step(x), dtype=float)
    return x


def fixed_point_newton(step: StepFn, x0: Vec, *, iters: int = 200,
                       tol: float = 1e-12, eps: float = 1e-6) -> tuple[Vec, float]:
    """Fixed point by Newton on F(x)=step(x)−x, using the finite-difference
    Jacobian. Tracks an equilibrium past where it stops attracting (continuation).
    Returns (x*, residual). CHECK the root is physically valid — Newton can cross a
    kink into an unphysical branch of a piecewise-smooth map."""
    x = np.asarray(x0, dtype=float).copy()
    I = np.eye(x.size)
    res = np.inf
    for _ in range(iters):
        Fx = np.asarray(step(x), dtype=float) - x
        res = float(np.max(np.abs(Fx)))
        if res < tol:
            break
        x = x - np.linalg.solve(jacobian(step, x, eps) - I, Fx)
    return x, res


def eigs(J: np.ndarray) -> np.ndarray:
    """Eigenvalues sorted by descending modulus."""
    ev = np.linalg.eigvals(J)
    return ev[np.argsort(-np.abs(ev))]


def leading_complex(J: np.ndarray, imag_tol: float = 1e-6):
    """Largest-modulus eigenvalue that has a nonzero imaginary part (the oscillatory
    pair). Returns None if the spectrum is purely real."""
    ev = np.linalg.eigvals(J)
    c = ev[np.abs(ev.imag) > imag_tol]
    if c.size == 0:
        return None
    return c[np.argmax(np.abs(c))]


# --------------------------------------------------------------- self-test
def _logistic(r: float) -> StepFn:
    return lambda x: r * x * (1.0 - x)


def _self_test() -> None:
    print("linearize self-test — logistic map x→r·x·(1−x), x*=1−1/r, multiplier 2−r")
    print(f"  {'r':>5}{'x* (newton)':>14}{'x* exact':>12}{'mult (jac)':>13}{'2−r':>8}")
    ok = True
    for r in (2.5, 3.2, 3.5, 3.8):
        xstar, res = fixed_point_newton(_logistic(r), np.array([0.4]))
        mult = jacobian(_logistic(r), xstar)[0, 0]
        exact_x = 1.0 - 1.0 / r
        print(f"  {r:>5.1f}{xstar[0]:>14.6f}{exact_x:>12.6f}{mult:>13.6f}{2 - r:>8.3f}")
        ok &= abs(xstar[0] - exact_x) < 1e-8 and abs(mult - (2 - r)) < 1e-5

    # complex-eigenvalue recovery: a 2-D rotation+scale map x → A x, A=[[a,-b],[b,a]]
    a, b = 0.8, 0.5
    A = np.array([[a, -b], [b, a]])
    lc = leading_complex(jacobian(lambda x: A @ x, np.array([1.0, 1.0])))
    ok &= abs(lc.real - a) < 1e-6 and abs(abs(lc.imag) - b) < 1e-6
    print(f"  2-D rotation+scale A=[[{a},-{b}],[{b},{a}]]: leading complex eig "
          f"{lc.real:.4f}{lc.imag:+.4f}i  (expect {a}{b:+}i)")

    assert ok, "linearize self-test FAILED"
    print("\n  PASS: multipliers match 2−r, x* matches 1−1/r, complex pair recovered.")
    print("  Instrument trusted for naming the supply-chain bifurcation.")


if __name__ == "__main__":
    _self_test()
