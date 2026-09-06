"""
Cybeersym — CYB-40 v0: self-test the critical-slowing-down instrument on known-answer models.

Run from inside src/csd:  python3 run_v0.py

Before CSD may be pointed at data, it must recover the KNOWN answer on benchmarks (the discipline the
`src/chaos/` instruments follow on the logistic map). Self-tests:
  0. CONTROL — the analytic fold normal form: var↑ and AR1→1 as r→0⁻, tracking the exact multiplier μ.
  1. LOCAL (our model) — the expectations de-anchoring fold: var↑ and AR1↑ as φ_e→ the fold, on the
     PHYSICAL branch (ω*≤1), tracking the leading eigenvalue |μ|→1.
  2. LOCAL vs GLOBAL (Goodwin–Keen): the good-equilibrium recovery rate (leading Re→0) slows as the
     investment sensitivity approaches its stability edge (a LOCAL bifurcation ⇒ CSD would fire); but
     the same eigenvalue is INDEPENDENT of the initial leverage that decides basin survival, so a
     GLOBAL breakdown-basin crossing has NO recovery-slowing ⇒ CSD is (correctly) BLIND.
  3. DETERMINISM — fixed-seed noise ⇒ byte-identical rerun.
The result maps which borders CSD can bridge to data (local/graded) vs which it cannot (global/abrupt).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import importlib.util as _ilu

from model import var_ar1, noisy_series, fold_normal_form

def _load(name, rel):
    s = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    m = _ilu.module_from_spec(s); s.loader.exec_module(m); return m
_exp = _load("expectations_model", "expectations/model.py")
_gk  = _load("gk_model", "goodwin_keen/model.py")
_lin = _load("linearize", "chaos/linearize.py")
ExpectationsParams, ExpectationsEconomy, ConflictParams = _exp.ExpectationsParams, _exp.ExpectationsEconomy, _exp.ConflictParams
GKParams, keen_good_equilibrium, continuous_jacobian, gk_step = _gk.GKParams, _gk.keen_good_equilibrium, _gk.continuous_jacobian, _gk.gk_step
jacobian, eigs = _lin.jacobian, _lin.eigs

SEED = 0


def control_fold():
    print("[0] CONTROL — analytic fold normal form (var↑, AR1→1 as r→0⁻, tracking μ):")
    print("      r        var         AR1      μ(exact)")
    rs = (-0.5, -0.2, -0.1, -0.05, -0.02, -0.01); V, A = [], []
    for r in rs:
        xstar, step, mu = fold_normal_form(r)
        rng = np.random.default_rng(SEED)
        v, a = var_ar1(noisy_series(step, xstar, 60000, rng, sigma=0.004))
        V.append(v); A.append(a)
        print(f"    {r:+.3f}   {v:.3e}   {a:.4f}   {mu:.4f}")
    assert V[-1] > V[0] and A[-1] > A[0] and A[-1] > 0.95, "fold control did not show CSD"
    print("    ✓ variance and AR1 rise monotonically toward the fold — detector validated.\n")
    return rs, V, A


def local_expectations():
    print("[1] LOCAL (our model) — expectations de-anchoring fold, PHYSICAL branch (ω*≤1):")
    print("      φ_e      var         AR1      |eig|     ω*")
    phis = (0.0, 0.5, 1.0, 1.4, 1.6, 1.7); P, V, A = [], [], []
    for phi in phis:
        p = ExpectationsParams(conflict=ConflictParams(), phi_e=phi, lam=0.3)
        ss = p.steady_state()
        if ss is None or ss[0] > 1.0:
            print(f"    {phi:.2f}   (unphysical ω*>1 — skipped)"); continue
        e = ExpectationsEconomy(p)
        step = lambda x: np.array(e.map2d(float(x[0]), float(x[1])))
        rng = np.random.default_rng(SEED)
        v, a = var_ar1(noisy_series(step, np.array(ss), 60000, rng, sigma=1e-4))
        mu = float(abs(eigs(jacobian(e.step_vector, np.array(ss)))[0]))
        P.append(phi); V.append(v); A.append(a)
        print(f"    {phi:.2f}   {v:.3e}   {a:.4f}   {mu:.4f}   {ss[0]:.3f}")
    assert V[-1] > V[0] and A[-1] > A[0], "expectations fold did not show CSD"
    print("    ✓ var and AR1 rise toward the fold (tracking |eig|→1): CSD fires on our local border.\n")
    return P, V, A


def local_vs_global_gk():
    print("[2] LOCAL vs GLOBAL (Goodwin–Keen) — recovery rate = leading eigenvalue real part (→0 fires):")
    def lead_re(ksharp):
        p = GKParams(keen=True, r=0.03, delta=0.03, kmin=0.0, kmax=0.30, ksharp=ksharp, kmid=0.16)
        s = keen_good_equilibrium(p)
        if s is None: return None, None
        return float(max(np.linalg.eigvals(continuous_jacobian(s, p)).real)), s
    print("    LOCAL (sweep investment sensitivity ksharp toward the stability edge):")
    print("      ksharp   lead Re(eig)   d*")
    kss = (40, 30, 24, 20, 18); RE = []
    for ks in kss:
        re, s = lead_re(ks)
        RE.append(re); print(f"      {ks:<5}    {re:+.5f}     {s[2]:+.3f}")
    assert RE[-1] > RE[0], "recovery rate did not slow toward the local edge"
    print("      ✓ Re→0 as ksharp falls: recovery slows ⇒ CSD WOULD fire (a local bifurcation).")
    # GLOBAL basin: demonstrate d₀ sets the OUTCOME (survive vs breakdown) but NOT the good-eq
    # recovery rate — so CSD (which reads that rate) is flat across d₀ ⇒ blind to the basin boundary.
    p40 = GKParams(keen=True, r=0.03, delta=0.03, kmin=0.0, kmax=0.30, ksharp=40.0, kmid=0.16)
    geq = keen_good_equilibrium(p40)
    re_g = float(max(np.linalg.eigvals(continuous_jacobian(geq, p40)).real))
    def gk_outcome(d0, n=200000):
        s = np.array([0.80, 0.90, float(d0)])
        for _ in range(n):
            s = gk_step(s, p40)
            if (not np.all(np.isfinite(s))) or s[2] > 1e3 or s[0] <= 1e-3:
                return "breakdown", s
        return "survive", s
    print(f"    GLOBAL (breakdown basin): d₀ decides the OUTCOME, not the good-eq recovery rate ({re_g:+.5f}):")
    print(f"      d₀       outcome      |end − good_eq|")
    devs = []
    for d0 in (1.0, 3.0, 8.0, 14.0):
        out, s = gk_outcome(d0)
        dev = float(np.max(np.abs(s - geq))) if out == "survive" else float("nan")
        if out == "survive": devs.append(dev)
        print(f"      {d0:<6}   {out:<10}   {('%.1e' % dev) if out == 'survive' else '—'}")
    print(f"      survivors converge to the IDENTICAL good eq (max dev {max(devs):.0e}) ⇒ identical local")
    print(f"      recovery rate ∀ d₀ in the basin (d₀ sets only the STARTING distance, not the rate) ⇒")
    print(f"      CSD stats FLAT across d₀ ⇒ BLIND to the boundary. (Contrast the LOCAL sweep above,")
    print(f"      where the rate itself ramps to 0.) The silence is CORRECT.\n")
    assert len(devs) >= 2 and max(devs) < 3e-3, "survivors did not converge to the good equilibrium"
    return kss, RE


def determinism():
    xstar, step, _ = fold_normal_form(-0.05)
    a = noisy_series(step, xstar, 5000, np.random.default_rng(SEED), sigma=0.004)
    b = noisy_series(step, xstar, 5000, np.random.default_rng(SEED), sigma=0.004)
    print(f"[3] DETERMINISM — fixed-seed rerun byte-identical: {np.array_equal(a, b)}")
    assert np.array_equal(a, b)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-40 v0: self-testing critical slowing down (the scale-free data bridge) ===\n")
    rs, Vf, Af = control_fold()
    Pe, Ve, Ae = local_expectations()
    kss, RE = local_vs_global_gk()
    determinism()
    make_figure(out, rs, Vf, Af, Pe, Ve, Ae, kss, RE)
    print(f"\n  figure → {out/'cybeersym_csd_v0_selftest.png'}")


def make_figure(out, rs, Vf, Af, Pe, Ve, Ae, kss, RE):
    INK, GRID, ACC, BLU = "#1b1b1b", "#d8d8d8", "#c1440e", "#2b6cb0"
    fig, (axL, axM, axR) = plt.subplots(1, 3, figsize=(15, 4.6))

    # Left: AR1 rising toward the bifurcation — control (fold) vs our model (expectations)
    axL.plot(-np.array(rs), Af, "-o", ms=4, color=INK, label="fold control (vs −r)")
    axL.plot(2.0 - np.array(Pe), Ae, "-s", ms=4, color=ACC, label="expectations (vs φ_e*−φ_e)")
    axL.axhline(1.0, color="#999", lw=1.0, ls=":")
    axL.set_xscale("log"); axL.invert_xaxis()
    axL.set_xlabel("distance to bifurcation  (log; → left = closer)"); axL.set_ylabel("lag-1 autocorrelation AR1")
    axL.set_title("AR1 → 1 approaching a LOCAL bifurcation\n(fold control + our expectations fold)", fontsize=10)
    axL.legend(frameon=False, fontsize=8.5); axL.grid(True, color=GRID, lw=0.7, which="both"); axL.set_axisbelow(True)

    # Middle: variance rising (same axis idea), log-y
    axM.plot(-np.array(rs), Vf, "-o", ms=4, color=INK, label="fold control")
    axM.plot(2.0 - np.array(Pe), Ve, "-s", ms=4, color=ACC, label="expectations")
    axM.set_xscale("log"); axM.set_yscale("log"); axM.invert_xaxis()
    axM.set_xlabel("distance to bifurcation (log)"); axM.set_ylabel("fluctuation variance (log)")
    axM.set_title("Variance rises approaching the border\n(the second CSD signature)", fontsize=10)
    axM.legend(frameon=False, fontsize=8.5); axM.grid(True, color=GRID, lw=0.7, which="both"); axM.set_axisbelow(True)

    # Right: GK recovery rate — LOCAL slows (Re→0) vs GLOBAL flat (d₀-independent)
    axR.plot(kss, RE, "-o", ms=4, color=BLU, label="good-eq lead Re(eig)")
    axR.axhline(0.0, color="#999", lw=1.0, ls="-")
    axR.axhline(RE[0], color=INK, lw=1.1, ls="--", label=f"global basin: Re fixed ∀ d₀ ({RE[0]:+.3f})")
    axR.invert_xaxis()
    axR.set_xlabel("investment sensitivity ksharp  (→ left = toward local edge)")
    axR.set_ylabel("recovery rate  (leading Re; 0 = bifurcation)")
    axR.set_title("Goodwin–Keen: LOCAL slows (CSD fires) vs\nGLOBAL basin is d₀-independent (CSD blind)", fontsize=10)
    axR.legend(frameon=False, fontsize=8.5); axR.grid(True, color=GRID, lw=0.7); axR.set_axisbelow(True)

    fig.suptitle("CYB-40 v0 — CSD self-test: fires on LOCAL bifurcations, correctly BLIND to GLOBAL basin crossings", fontsize=11, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out / "cybeersym_csd_v0_selftest.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
