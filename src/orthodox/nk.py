"""
Cybeersym — the orthodox foil #2: the canonical 3-equation New-Keynesian model (Clarida–Galí–
Gertler 1999; Woodford 2003; Galí 2015, ch. 3). ENGINE OF RECORD for the viz's "NK — demand
shock, sticky prices (Mankiw)" beat.

The economics we are faithfully reproducing (steelman, not strawman):
  * Nominal rigidity (sticky prices, Calvo) means an ADVERSE demand shock is NOT costlessly
    absorbed: it opens a real output GAP (output below its efficient level) and DISINFLATION —
    an INEFFICIENT fluctuation, unlike RBC where output is always on its efficient path. This
    is the New-Keynesian/Mankiw departure from Lucas: fluctuations are a problem, not the
    optimum.
  * Monetary policy (a Taylor rule) RESPONDS (eases) and closes the gap — policy has a
    stabilisation role, the opposite of RBC's "leave it alone."
  * HONEST SHAPE NOTE: in the canonical 3-equation model the gap troughs ON IMPACT and decays
    (it is NOT hump-shaped — the hump-shaped output IRF is a medium-scale-DSGE feature of habit
    formation / adjustment costs, not this model; an earlier hand-drawn viz curve wrongly implied
    a hump). What interest-rate SMOOTHING (ρ_i>0) does add is a mild policy-driven OVERSHOOT:
    because policy eases only gradually, the gap crosses zero and rings slightly positive before
    settling — a real, subtle signature that is ABSENT when ρ_i=0 (then the gap decays monotone,
    ∝ the AR(1) shock). The self-test pins this overshoot-vs-monotone contrast (ties shape to theory).
The RBC↔NK contrast the viz teaches is therefore EFFICIENCY + POLICY (a gap that policy closes,
with a co-moving rate and persistent inflation) — NOT "hump vs monotone."

Gap-form equations (log-deviations), per period t:
  (IS)   x_t = E_t x_{t+1} − (1/σ)(i_t − E_t π_{t+1} − r^n_t)     # dynamic IS / Euler
  (PC)   π_t = β E_t π_{t+1} + κ x_t                              # New-Keynesian Phillips curve
  (TR)   i_t = ρ_i i_{t-1} + (1−ρ_i)(φ_π π_t + φ_x x_t)          # inertial Taylor rule
  r^n_t = ρ_d r^n_{t-1}  (adverse demand: r^n_0 = shock < 0)      # natural-rate / demand shock

x = output gap, π = inflation, i = nominal rate. i is (weakly) predetermined via smoothing
(i_{-1}=0); x,π are jumps. Solved by a stacked-time linear system (numpy-only; linear ⇒
perfect-foresight = the true IRF). An independent residual check plugs the solution back into
plainly-written IS/PC/TR and confirms residuals ~0 (guards the matrix assembly).

Deterministic; pure. Run `python3 nk.py` (from src/) for the self-test.

References
  Mankiw, N. G. (1985). "Small Menu Costs and Large Business Cycles: A Macroeconomic Model of
    Monopoly." Quarterly J. Economics 100(2), 529–537.
  Clarida, R., Galí, J., & Gertler, M. (1999). "The Science of Monetary Policy: A New Keynesian
    Perspective." J. Economic Literature 37(4), 1661–1707.   (the 3-equation model used here)
  Woodford, M. (2003). Interest and Prices: Foundations of a Theory of Monetary Policy. Princeton.
  Galí, J. (2015). Monetary Policy, Inflation, and the Business Cycle, 2nd ed. Princeton.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class NKParams:
    sigma: float = 1.0      # inverse elasticity of intertemporal substitution
    beta: float = 0.99      # discount
    kappa: float = 0.1275   # NKPC slope (Galí baseline: θ=2/3, α=1/3, φ=1)
    phi_pi: float = 1.5     # Taylor inflation response (Taylor principle: >1)
    phi_x: float = 0.125    # Taylor gap response (0.5 annualised /4)
    rho_i: float = 0.8      # interest-rate smoothing (the source of the hump)
    rho_d: float = 0.5      # demand-shock persistence


def irf(p: NKParams = NKParams(), shock: float = -0.01, T: int = 400):
    """Impulse response to a one-time demand (natural-rate) innovation `shock`.

    Returns dict of arrays (length T): rn (shock path), x (output gap), pi (inflation), i (rate).
    """
    rn = shock * (p.rho_d ** np.arange(T))
    # Unknowns u = [x_0..x_{T-1}, pi_0..pi_{T-1}, i_0..i_{T-1}] (length 3T).
    # Terminal x_T = pi_T = 0 (T large); i_{-1} = 0 (predetermined).
    def xi(t): return t
    def pi(t): return T + t
    def ii(t): return 2 * T + t
    N = 3 * T
    A = np.zeros((N, N)); b = np.zeros(N)
    row = 0
    for t in range(T):                               # (IS)  x_t − x_{t+1} + (1/σ)(i_t − π_{t+1} − r^n_t)=0
        A[row, xi(t)] += 1.0
        if t + 1 < T:
            A[row, xi(t + 1)] += -1.0
            A[row, pi(t + 1)] += -1.0 / p.sigma
        A[row, ii(t)] += 1.0 / p.sigma
        b[row] += rn[t] / p.sigma
        row += 1
    for t in range(T):                               # (PC)  π_t − β π_{t+1} − κ x_t = 0
        A[row, pi(t)] += 1.0
        if t + 1 < T:
            A[row, pi(t + 1)] += -p.beta
        A[row, xi(t)] += -p.kappa
        row += 1
    for t in range(T):                               # (TR)  i_t − ρ_i i_{t-1} − (1−ρ_i)(φ_π π_t + φ_x x_t)=0
        A[row, ii(t)] += 1.0
        if t - 1 >= 0:
            A[row, ii(t - 1)] += -p.rho_i
        A[row, pi(t)] += -(1.0 - p.rho_i) * p.phi_pi
        A[row, xi(t)] += -(1.0 - p.rho_i) * p.phi_x
        row += 1
    assert row == N
    u = np.linalg.solve(A, b)
    return {"rn": rn, "x": u[0:T], "pi": u[T:2 * T], "i": u[2 * T:3 * T]}


def residuals(p: NKParams, sol):
    """Independent check: plug the solution into plainly-written IS/PC/TR; should be ~0."""
    x, pip, i, rn = sol["x"], sol["pi"], sol["i"], sol["rn"]
    T = len(x)
    xn = np.append(x[1:], 0.0); pn = np.append(pip[1:], 0.0); il = np.append(0.0, i[:-1])
    r_is = x - xn + (1.0 / p.sigma) * (i - pn - rn)
    r_pc = pip - p.beta * pn - p.kappa * x
    r_tr = i - p.rho_i * il - (1.0 - p.rho_i) * (p.phi_pi * pip + p.phi_x * x)
    return max(np.max(np.abs(r_is)), np.max(np.abs(r_pc)), np.max(np.abs(r_tr)))


def _selftest():
    p = NKParams()
    s = irf(p, shock=-0.01, T=400)
    x, pip, i = s["x"], s["pi"], s["i"]

    # (1) the solve satisfies its own equations (independent residual eval guards the assembly)
    res = residuals(p, s)
    assert res < 1e-10, f"NK residuals not zero: {res:.2e}"

    # (2) adverse demand shock opens a NEGATIVE output gap and pushes inflation down (inefficiency)
    assert x[0] < 0 and pip[0] < 0, (x[0], pip[0])
    trough = int(np.argmin(x))
    assert trough == 0, f"canonical 3-eq gap troughs on impact (NOT hump-shaped); trough@{trough}"

    # (3) the gap CLOSES (policy stabilises): returns to ~0
    assert abs(x[-1]) < 1e-5 and abs(pip[-1]) < 1e-5, (x[-1], pip[-1])

    # (4) policy responds — the rate eases in the adverse shock (RBC has no such lever)
    assert i[0] < 0, i[0]

    # (5) shape signature — smoothing ⇒ a mild positive OVERSHOOT (ringing); ρ_i=0 ⇒ monotone.
    overshoot = np.max(x[1:])
    assert overshoot > 0, f"with ρ_i>0 the gap should overshoot slightly positive; max={overshoot:.2e}"
    s0 = irf(NKParams(rho_i=0.0), shock=-0.01, T=400)
    assert np.max(s0["x"]) <= 1e-9, "ρ_i=0 gap should not overshoot (monotone decay ∝ AR(1) shock)"
    dx = np.diff(s0["x"][:100]); nz = dx[np.abs(dx) > 1e-12]
    assert np.all(nz > 0) or np.all(nz < 0), "ρ_i=0 gap should be monotone"

    print(f"NK self-test OK  (residuals {res:.2e})")
    print(f"  impact:  x={x[0]:+.4f}  π={pip[0]:+.4f}  i={i[0]:+.4f}   (adverse 1% demand shock)")
    print(f"  gap troughs ON IMPACT then decays (NOT hump); policy eases and closes it")
    print(f"  smoothing overshoot: gap rings to {overshoot:+.4f}; ρ_i=0 control is monotone (no overshoot)")
    return s


if __name__ == "__main__":
    _selftest()
