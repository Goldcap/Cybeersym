"""
Cybeersym — the orthodox foil #1: a real Real-Business-Cycle model (Kydland–Prescott 1982;
King–Plosser–Rebelo 1988; the log-linear mechanics follow Campbell 1994, "Inspecting the
mechanism"). This is the ENGINE OF RECORD for the viz's "RBC — real productivity shock (Lucas)"
beat: the orthodox curve there is this model's impulse response, not a hand-drawn shape.

The economics we are faithfully reproducing (steelman, not strawman):
  * A single representative agent chooses consumption and labour optimally under rational
    expectations. Fluctuations are the OPTIMAL response to real technology (TFP) shocks — the
    cycle is efficient, and there is no role for stabilisation policy (Lucas/Prescott).
  * An ADVERSE (negative) TFP shock lowers output and hours on impact; both then recover
    ~MONOTONICALLY as technology mean-reverts and the capital stock adjusts. No overshoot,
    no endogenous oscillation, no output "gap" (the economy is always on its efficient path).
This near-monotone, non-oscillatory IRF is the signature the self-test below pins.

Divisible-labour RBC, standard Cobb–Douglas + log-consumption / iso-elastic labour utility:
    U = Σ βᵗ [ log C_t − χ N_t^{1+φ}/(1+φ) ] ,   Y_t = Z_t K_t^α N_t^{1−α}
Log-deviations (hat = log X_t − log X_ss); Z is TFP with log Z_t = z_t, z_{t+1}=ρ_z z_t (+shock).
Steady state (from the Euler 1/β = α·Y/K + 1−δ):
    Y/K = (1/β − 1 + δ)/α ,   I/Y = δ·K/Y ,   C/Y = 1 − I/Y ,   θ ≡ 1 − β(1−δ) = (αY/K)/(1/β).
Equilibrium (log-linear), per period t:
  (P)  ŷ_t = z_t + α k̂_t + (1−α) n̂_t                         # production
  (L)  ĉ_t = ŷ_t − (1+φ) n̂_t                                  # labour FOC: χ N^φ C = (1−α)Y/N
  (K)  k̂_{t+1} = (1−δ) k̂_t + (Y/K)(ŷ_t − (C/Y) ĉ_t)          # capital accumulation via resource I=Y−C
  (E)  ĉ_{t+1} = ĉ_t + θ (ŷ_{t+1} − k̂_{t+1})                  # consumption Euler (real return = α Y/K·(ŷ−k̂))

k is PREDETERMINED (k̂_0 = 0 at the shock); c is a JUMP variable pinned by the saddle path.
We solve the two-point boundary-value problem by a stacked-time linear system (numpy-only; the
model is linear so perfect-foresight = the true IRF by certainty equivalence). A second,
independent policy-function (Blanchard–Kahn 2×2) solve is provided and cross-checked in the
self-test, so an algebra slip in either surfaces immediately.

Deterministic; pure functions of parameters. Run `python3 rbc.py` (from src/) for the self-test.
"""
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class RBCParams:
    alpha: float = 0.33     # capital share
    beta: float = 0.99      # quarterly discount
    delta: float = 0.025    # quarterly depreciation
    phi: float = 1.0        # inverse Frisch elasticity of labour
    rho_z: float = 0.95     # TFP persistence

    def ratios(self):
        YK = (1.0 / self.beta - 1.0 + self.delta) / self.alpha   # Y/K
        IY = self.delta / YK                                     # I/Y = δ (K/Y)
        CY = 1.0 - IY                                            # C/Y
        theta = 1.0 - self.beta * (1.0 - self.delta)            # (αY/K)/(1/β)
        return YK, IY, CY, theta


def _static_coeffs(p: RBCParams):
    """ŷ = Az·z + Ak·k̂ + Ac·ĉ, and n̂ = (ŷ − ĉ)/(1+φ), from (P) & (L)."""
    a = (1.0 - p.alpha) / (1.0 + p.phi)
    den = 1.0 - a
    return (1.0 / den, p.alpha / den, -a / den)   # Az, Ak, Ac


def irf(p: RBCParams = RBCParams(), shock: float = -0.01, T: int = 600):
    """Impulse response to a one-time TFP innovation `shock` (negative = adverse).

    Returns dict of arrays (length T): z, y, c, n, k (log-deviations from steady state).
    """
    YK, IY, CY, theta = p.ratios()
    Az, Ak, Ac = _static_coeffs(p)
    z = shock * (p.rho_z ** np.arange(T))            # AR(1) TFP path

    # Unknowns u = [y_0..y_{T-1}, c_0..c_{T-1}, n_0..n_{T-1}, k_1..k_{T-1}]  (length 4T-1).
    # k_0 = 0 (predetermined); k_T = 0 (terminal, T large); last Euler dropped (the jump freedom).
    def yi(t): return t
    def ci(t): return T + t
    def ni(t): return 2 * T + t
    def ki(t):                                       # k_0 and k_T are data (0), not unknowns
        return 3 * T + (t - 1)
    N = 4 * T - 1
    A = np.zeros((N, N))
    b = np.zeros(N)
    row = 0

    def kterm(t, coeff, r):
        """Add coeff·k̂_t to row r, handling the k_0=0 and k_T=0 boundaries."""
        if t <= 0 or t >= T:
            return                                   # k̂ at the boundaries is 0
        A[r, ki(t)] += coeff

    for t in range(T):                               # (P) production
        A[row, yi(t)] += 1.0
        A[row, ni(t)] += -(1.0 - p.alpha)
        kterm(t, -p.alpha, row)
        b[row] += z[t]
        row += 1
    for t in range(T):                               # (L) labour FOC
        A[row, ci(t)] += 1.0
        A[row, yi(t)] += -1.0
        A[row, ni(t)] += (1.0 + p.phi)
        row += 1
    for t in range(T):                               # (K) capital accumulation, defines k̂_{t+1}
        kterm(t + 1, 1.0, row)
        kterm(t, -(1.0 - p.delta), row)
        A[row, yi(t)] += -YK
        A[row, ci(t)] += YK * CY
        row += 1
    for t in range(T - 1):                            # (E) Euler (drop t=T-1: the terminal jump freedom)
        A[row, ci(t + 1)] += 1.0
        A[row, ci(t)] += -1.0
        A[row, yi(t + 1)] += -theta
        kterm(t + 1, theta, row)
        row += 1
    assert row == N, (row, N)

    u = np.linalg.solve(A, b)
    y = u[0:T]; c = u[T:2 * T]; n = u[2 * T:3 * T]
    k = np.zeros(T)
    k[1:] = u[3 * T:3 * T + (T - 1)]
    return {"z": z, "y": y, "c": c, "n": n, "k": k}


def irf_policy(p: RBCParams = RBCParams(), shock: float = -0.01, T: int = 600):
    """Independent solve via the Blanchard–Kahn saddle path (2×2), for cross-checking irf().

    State w=(k̂,ĉ). Substituting the static block gives w_{t+1}=J w_t + g z_t. J is a saddle
    (one root <1, one >1). The stable manifold pins ĉ_0; then k̂ evolves on the stable root.
    """
    YK, IY, CY, theta = p.ratios()
    Az, Ak, Ac = _static_coeffs(p)
    # k̂_{t+1} = (1-δ)k̂ + YK(ŷ - CY ĉ),  ŷ = Az z + Ak k̂ + Ac ĉ
    #        = [(1-δ)+YK·Ak] k̂ + YK(Ac - CY) ĉ + YK·Az z
    Jkk = (1.0 - p.delta) + YK * Ak
    Jkc = YK * (Ac - CY)
    gk = YK * Az
    # ĉ_{t+1}(1 - θ Ac) = ĉ + θ(Ak - 1) k̂_{t+1} + θ Az z_{t+1}
    s = 1.0 - theta * Ac
    # substitute k̂_{t+1}:
    Jck = (theta * (Ak - 1.0) * Jkk) / s
    Jcc = (1.0 + theta * (Ak - 1.0) * Jkc) / s
    gc = (theta * (Ak - 1.0) * gk + theta * Az * p.rho_z) / s
    J = np.array([[Jkk, Jkc], [Jck, Jcc]])
    g = np.array([gk, gc])

    w_eval, V = np.linalg.eig(J)
    order = np.argsort(np.abs(w_eval))               # stable root first, unstable second
    mu_s, mu_u = w_eval[order]
    assert abs(mu_s) < 1.0 < abs(mu_u), f"not a saddle: |μ|={np.abs(w_eval)}"
    P = V[:, order]                                  # columns = eigenvectors (canonical → level)
    Vinv = np.linalg.inv(P)
    gb = Vinv @ g                                    # forcing in canonical coords
    z = shock * (p.rho_z ** np.arange(T))

    # Canonical coords v = Vinv·w evolve as v_{t+1}=Λ v_t + gb·z_t. To stay on the stable
    # manifold we FORWARD-solve the unstable coord (never iterate it — that reintroduces μ_u):
    #   v_u,t = −gb_u · z_t /(μ_u − ρ_z)     (Σ_{j≥0} μ_u^{−(j+1)} gb_u ρ^j z_t)
    # and iterate ONLY the stable coord; v_s,0 is pinned by the predetermined k̂_0 = 0.
    vu = -gb[1] * z / (mu_u - p.rho_z)               # length-T unstable path
    vs = np.zeros(T)
    vs[0] = -P[0, 1] * vu[0] / P[0, 0]               # from k̂_0 = P00 vs0 + P01 vu0 = 0
    for t in range(T - 1):
        vs[t + 1] = mu_s * vs[t] + gb[0] * z[t]
    W = P @ np.vstack([vs, vu])                      # 2×T levels
    k = W[0].real.copy(); c = W[1].real.copy()
    Az, Ak, Ac = _static_coeffs(p)
    y = Az * z + Ak * k + Ac * c
    n = (y - c) / (1.0 + p.phi)
    return {"z": z, "y": y, "c": c, "n": n, "k": k}


def _selftest():
    p = RBCParams()
    r = irf(p, shock=-0.01, T=600)
    rp = irf_policy(p, shock=-0.01, T=600)
    y, n, c, k, z = r["y"], r["n"], r["c"], r["k"], r["z"]

    # (1) two independent solvers agree over the economically-relevant window (guards algebra
    # slips in either). The stacked solve has a tiny finite-horizon terminal artifact, so the
    # cross-check excludes the last 50 nodes; both are ~0 there anyway (checked in (5)).
    w = slice(0, 550)
    dmax = max(np.max(np.abs(r[v][w] - rp[v][w])) for v in ("y", "c", "n", "k"))
    assert dmax < 1e-6, f"stacked vs policy-function disagree: {dmax:.2e}"

    # (2) adverse shock: output & hours fall on impact
    assert y[0] < 0 and n[0] < 0, (y[0], n[0])

    # (3) near-MONOTONE recovery, NO oscillation (RBC signature — no sign changes after impact)
    dy = np.diff(y[:200])
    sign_changes = np.sum(np.diff(np.sign(dy[np.abs(dy) > 1e-9])) != 0)
    assert sign_changes == 0, f"output IRF should be monotone (no oscillation); sign changes={sign_changes}"

    # (4) efficient: consumption is SMOOTHER than output (|c| impact < |y| impact) — the RBC/PIH signature
    assert abs(c[0]) < abs(y[0]), (c[0], y[0])

    # (5) mean-reversion: everything returns to steady state
    assert abs(y[-1]) < 1e-4 and abs(k[-1]) < 1e-4, (y[-1], k[-1])

    print(f"RBC self-test OK  (solvers agree to {dmax:.2e})")
    print(f"  impact:  ŷ={y[0]:+.4f}  n̂={n[0]:+.4f}  ĉ={c[0]:+.4f}   (adverse 1% TFP shock)")
    print(f"  trough→recovery monotone; half-life ≈ {np.argmax(y > y[0]/2)} q")
    return r


if __name__ == "__main__":
    _selftest()
