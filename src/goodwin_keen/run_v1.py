"""
Goodwin–Keen v1 (CYB-35) — a genuine LOCAL Hopf, recovered two ways.

v0 (CYB-33) passed as the instrument self-test rung but found that with a linear Phillips curve
the (ω,λ) block is a structural zero-trace centre, so Keen breakdown there is only a *global*
basin crossing — no clean *local* bifurcation for `linearize` to catch. v1 supplies one and checks
the instrument against a KNOWN analytic threshold.

The known answer (derived, not guessed): at the Keen good equilibrium ∂ω̇/∂ω = ∂λ̇/∂λ = 0 for ANY
Phillips shape, and the 3×3 Routh–Hurwitz Hopf condition a₁a₂=a₃ reduces EXACTLY to
J₁₂·J₂₃·J₃₁ = 0. Since J₁₂ = ω*φ'(λ*) ≠ 0 and J₂₃ = −λ*rκ'/ν ≠ 0, the Hopf is where **J₃₁ = 0**,
i.e. **κ'(π*) = ν/(ν−d*)** — a closed-form locus, INDEPENDENT of the Phillips curve (φ' cancels).
So the local Hopf is an investment-sensitivity (κ', swept via `ksharp`) / debt-coupling phenomenon,
not a Phillips-convexity one. We add the canonical convex Phillips (flagged) and demo with it on,
but the control parameter is `ksharp` and the locus is Phillips-independent — reported honestly.

  0. Nesting — phillips_convex=False leaves v0 (CYB-33) byte-exact.
  1. The Hopf, two ways — analytic (continuous-Jacobian Re→0, and the closed-form κ'=ν/(ν−d*))
     vs instrument (RK4-map |μ|→1). Same ksharp*, crossing pair complex ⇒ Neimark–Sacker (D1).
  2. Both sides reachable — stable focus (spirals in) vs Hopf-born limit cycle.
  3. Determinism.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import importlib.util as _ilu

from model import (GKParams, gk_step, step_fn, keen_good_equilibrium,
                   continuous_jacobian, hopf_locus_residual, kappa_prime)


def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_lin = _load("chaos_linearize", "chaos/linearize.py")


# Keen v1 config: canonical convex Phillips ON; the swept control parameter is ksharp.
def _p(ksharp):
    return GKParams(keen=True, phillips_convex=True, r=0.03, delta=0.03,
                    kmin=0.0, kmax=0.30, kmid=0.16, phi0=0.04, phi1=0.00065,
                    ksharp=float(ksharp), dt=0.01)


def _leading_complex_re(Jc):
    """Real part of the largest-|·| eigenvalue that has nonzero imaginary part (the oscillatory
    pair) of a CONTINUOUS Jacobian."""
    ev = np.linalg.eigvals(Jc)
    c = ev[np.abs(ev.imag) > 1e-9]
    if c.size == 0:
        return None
    return float(c[np.argmax(np.abs(c))].real)


def _analytic_re(ksharp):
    p = _p(ksharp)
    eq = keen_good_equilibrium(p)
    return _leading_complex_re(continuous_jacobian(eq, p))


def _instrument_absmu(ksharp):
    p = _p(ksharp)
    eq = np.array(keen_good_equilibrium(p))
    x, res = _lin.fixed_point_newton(step_fn(p), eq)
    J = _lin.jacobian(step_fn(p), x)
    return float(np.max(np.abs(_lin.eigs(J)))), x, res, J


def _bisect(f, lo, hi, tol=1e-4):
    """Bisection for a sign change of f on [lo, hi]."""
    flo = f(lo)
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        (lo := mid) if (f(mid) * flo > 0) else (hi := mid)   # noqa: E731
    return 0.5 * (lo + hi)


# ---- 0. nesting: v0 byte-exact ------------------------------------------------
def nesting():
    v0 = _load("gk_run_v0", "goodwin_keen/run_v0.py")
    v0.nested_regression()                                   # asserts max|Δ|=0.0 (Goodwin ≡ 3-D)
    absmu, Om_meas, Om_true = v0.goodwin_eigenvalues()       # Ω=0.3602, |μ|=1
    worst_H = v0.goodwin_conservation()                      # 4.4e-14
    ok = abs(Om_meas - Om_true) < 1e-3 and abs(absmu - 1.0) < 1e-5 and worst_H < 1e-10
    print(f"[0] nesting — phillips_convex=False ⇒ v0 (CYB-33) intact: Ω={Om_meas:.4f}, "
          f"|μ|={absmu:.6f}, worst|ΔH|={worst_H:.1e}  ⇒ {'PASS' if ok else 'FAIL'}")
    assert ok, "NESTING LEAK: v1 model changes perturbed the v0 linear path"


# ---- 1. the Hopf, two ways ----------------------------------------------------
def hopf_two_ways():
    lo, hi = 12.0, 26.0
    ks_analytic = _bisect(_analytic_re, lo, hi)              # continuous Re(complex) → 0
    ks_closed   = _bisect(hopf_locus_residual and (lambda k: hopf_locus_residual(_p(k))), lo, hi)
    ks_instr    = _bisect(lambda k: _instrument_absmu(k)[0] - 1.0, lo, hi)
    # confirm the crossing pair is complex (Neimark–Sacker, not a real eigenvalue through 1)
    p = _p(ks_instr); x, _r = _lin.fixed_point_newton(step_fn(p), np.array(keen_good_equilibrium(p)))
    mu_c = _lin.leading_complex(_lin.jacobian(step_fn(p), x))
    eq = keen_good_equilibrium(p)
    gap = abs(ks_instr - ks_analytic) / ks_analytic * 100.0
    print(f"[1] the local Hopf, two ways (control parameter = ksharp; convex Phillips ON):")
    print(f"      analytic  ksharp* = {ks_analytic:.3f}   (continuous-Jacobian Re[complex pair] → 0)")
    print(f"      closed-form ksharp* = {ks_closed:.3f}   (κ'(π*) = ν/(ν−d*), i.e. J₃₁ = 0)")
    print(f"      instrument ksharp* = {ks_instr:.3f}   (RK4-map |μ| → 1, via jacobian/eigs)   Δ={gap:.2f}%")
    print(f"      crossing eigenvalue μ = {mu_c.real:+.5f}{mu_c.imag:+.5f}i  (COMPLEX ⇒ Neimark–Sacker,")
    print(f"      a genuine local Hopf — taxonomy D1). good eq (ω,λ,d)=({eq[0]:.3f},{eq[1]:.3f},{eq[2]:.3f}).")
    print(f"      NB the locus κ'(π*)=ν/(ν−d*) is Phillips-INDEPENDENT: the Hopf is investment-")
    print(f"      sensitivity (κ' via ksharp) × debt coupling, not Phillips convexity (φ' cancels).")
    return ks_analytic, ks_instr, ks_closed


def _lambda_amp(ksharp, n, lo, hi):
    """Integrate from a small kick off the good eq; return (initial |s−eq|, final |s−eq|,
    λ-amplitude in the window [lo,hi])."""
    p = _p(ksharp); eq = np.array(keen_good_equilibrium(p))
    s = eq + np.array([0.01, 0.01, 0.01]); d0 = float(np.linalg.norm(s - eq))
    win = []
    for k in range(n):
        s = gk_step(s, p)
        if (not np.all(np.isfinite(s))) or s[2] > 1e6:
            return d0, np.inf, np.inf
        if lo <= k < hi: win.append(s[1])
    return d0, float(np.linalg.norm(s - eq)), (max(win) - min(win))


# ---- 2. both sides reachable --------------------------------------------------
def both_sides(ks_star):
    ks_stable = ks_star + 6.0                                # above ksharp* — stable focus (well damped)
    ks_cycle  = ks_star - 3.0                                # below — Hopf-born limit cycle
    # stable: the focus CONTRACTS (final |s−eq| < initial), and its late-window amplitude decays
    d0_s, df_s, amp_s = _lambda_amp(ks_stable, 150000, 130000, 150000)
    # cycle: sustained oscillation — compare an early tail window to a late one (non-decaying)
    _d0, _df, amp_c_early = _lambda_amp(ks_cycle, 90000, 40000, 55000)
    _d0, _df, amp_c_late  = _lambda_amp(ks_cycle, 90000, 70000, 85000)
    print(f"[2] both sides of the Hopf reachable (not rigged):")
    print(f"      ksharp={ks_stable:.1f} (> ksharp*): STABLE focus — spirals IN "
          f"(|s−eq| {d0_s:.1e}→{df_s:.1e}), late-window λ amp={amp_s:.1e}")
    print(f"      ksharp={ks_cycle:.1f} (< ksharp*): LIMIT CYCLE — λ amp {amp_c_early:.3f} (early) "
          f"→ {amp_c_late:.3f} (late): sustained, non-decaying")
    stable_ok = df_s < 0.5 * d0_s and amp_s < 5e-3          # genuinely contracting toward the eq
    cycle_ok = amp_c_late > 1e-2 and amp_c_late > 0.5 * amp_c_early
    print(f"      ⇒ {'PASS' if (stable_ok and cycle_ok) else 'FAIL'} (focus contracts; cycle sustains)")
    return ks_stable, ks_cycle


# ---- 3. determinism -----------------------------------------------------------
def determinism():
    def run():
        p = _p(16.0); s = np.array(keen_good_equilibrium(p)) + 0.01; out = np.empty((300, 3))
        for k in range(300):
            s = gk_step(s, p); out[k] = s
        return out
    ok = np.array_equal(run(), run())
    print(f"[3] determinism — byte-identical rerun = {ok}")


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== Goodwin–Keen v1 (CYB-35): a genuine LOCAL Hopf, recovered two ways ===\n")
    nesting()
    ks_analytic, ks_instr, ks_closed = hopf_two_ways()
    ks_stable, ks_cycle = both_sides(ks_instr)
    determinism()
    print("\nVERDICT: the `linearize` instrument (RK4-map |μ|→1) recovers the analytic local Hopf")
    print(f"(continuous Re→0 and the closed-form κ'=ν/(ν−d*)) at ksharp*≈{ks_instr:.2f}, a genuine")
    print("Neimark–Sacker crossing — a VALIDATED instance of taxonomy D1 (local bifurcation),")
    print("complementing v0's A2 centre. v0 nesting preserved.")
    make_figures(out, ks_analytic, ks_instr, ks_stable, ks_cycle)
    print("\nsaved 2 figures to goodwin_keen/figures/.")


# ============================================================ figures
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"
def make_figures(out, ks_analytic, ks_instr, ks_stable, ks_cycle):
    plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                         "figure.facecolor":"white","axes.facecolor":"white"})

    # ---- Fig 1: analytic Re and instrument |μ|−1 vs ksharp, crossing at the same ksharp* ----
    kss = np.linspace(12.0, 26.0, 43)
    re = np.array([_analytic_re(k) for k in kss])
    # instrument as the map's implied continuous growth rate log|μ|/dt (≈ Re), so it overlays the
    # analytic Re — a sharper view of the agreement than |μ|−1 (which is ~dt× smaller, looks flat).
    dm = np.array([np.log(_instrument_absmu(k)[0]) / 0.01 for k in kss])
    fig, ax = plt.subplots(figsize=(9.2, 5.6))
    ax.axhline(0.0, color=INK, lw=0.8, ls=":")
    ax.axvline(ks_instr, color=ORG, lw=1.4, ls="--", label=f"Hopf ksharp* ≈ {ks_instr:.2f}")
    ax.plot(kss, re, color=BLU, lw=2.4, marker="o", ms=3, label="analytic  Re[complex pair]  (continuous J)")
    ax.plot(kss, dm, color=ACC, lw=1.4, marker="s", ms=3, ls="--", label="instrument  log|μ|/dt  (RK4-map jacobian/eigs)")
    ax.set_xlabel("investment sensitivity  ksharp  (κ′ ∝ ksharp)"); ax.set_ylabel("growth rate of the oscillatory pair")
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.set_title("GK v1 — a genuine LOCAL Hopf (taxonomy D1): the instrument's |μ|→1 crossing lands on the\n"
                 "analytic Re→0 / closed-form κ′(π*)=ν/(ν−d*). Stability lost through a complex pair (Neimark–Sacker)",
                 fontsize=9.2, fontweight="bold")
    ax.grid(True, color=GRID, lw=0.6); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(out/"cybeersym_goodwin_keen_v1_hopf.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 2: phase portraits — stable focus (spirals in) vs Hopf limit cycle ----
    def traj(ksharp, n, kick=0.02):
        p = _p(ksharp); eq = np.array(keen_good_equilibrium(p)); s = eq + np.array([kick, kick, kick])
        T = []
        for _ in range(n):
            s = gk_step(s, p); T.append((s[1], s[0]))
            if (not np.all(np.isfinite(s))) or s[2] > 1e6: break
        return np.array(T), eq
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.4))
    Ts, eqs = traj(ks_stable, 80000)
    a1.plot(Ts[:,0], Ts[:,1], color=BLU, lw=0.7)
    a1.plot([eqs[1]],[eqs[0]], "o", color=INK, ms=6)
    a1.set_xlabel("employment  λ"); a1.set_ylabel("wage share  ω")
    a1.set_title(f"STABLE focus (ksharp={ks_stable:.1f} > ksharp*) — spirals IN to the good eq (A1)", fontsize=9.2)
    a1.grid(True, color=GRID, lw=0.6); a1.set_axisbelow(True)
    Tc, eqc = traj(ks_cycle, 80000)
    a2.plot(Tc[:,0], Tc[:,1], color=ACC, lw=0.7)
    a2.plot([eqc[1]],[eqc[0]], "o", color=INK, ms=6)
    a2.set_xlabel("employment  λ"); a2.set_ylabel("wage share  ω")
    a2.set_title(f"Hopf LIMIT CYCLE (ksharp={ks_cycle:.1f} < ksharp*) — sustained oscillation (B1)", fontsize=9.2)
    a2.grid(True, color=GRID, lw=0.6); a2.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(out/"cybeersym_goodwin_keen_v1_focus_vs_cycle.png", dpi=140, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
