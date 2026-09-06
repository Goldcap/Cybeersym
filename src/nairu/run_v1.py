"""
Cybeersym — CYB-20 (NAIRU) v1: the discipline function MICRO-FOUNDED, with the outside option a dial.

Run from inside src/nairu:  python3 run_v1.py

**Illustration under bargaining primitives — not proof, not empirics.** v1 answers the mainstream
'ad hoc' charge: ω_w(u) is DERIVED from Nash / McDonald–Solow wage bargaining, and the outside
option (the cost of job loss) is an explicit, dial-able parameterization `cjl(u)=k·u^γ`.

  0. NESTING — γ=1 reduces the bargain to the nairu-v0 linear discipline function, exactly.
  1. MICRO-FOUNDATION + reproduction — ω_w(u) is the bargaining solution; sim π == closed form.
  2. DECOMPOSITION — u* depends on BOTH frictions (ω_e, k) AND power (β, ω_f), from one optimizing model.
  3. THE γ DIAL — turning the outside-option convexity dials the Phillips-curve CURVATURE (concave ↔
     linear ↔ convex/flat-then-steep). The SIGN of that curvature is a live empirical/fingerprint
     question (is the Phillips curve linear, or does it steepen when the market is tight?).
  4. DETERMINISM + conservation (inherited from the CYB-6 sim at each u).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import BargainParams, NairuParams, ConflictParams, ConflictEconomy


def nesting():
    print("[0] NESTING — γ=1 bargain ≡ the nairu-v0 linear discipline function:")
    bp = BargainParams(gamma=1.0)
    np0 = bp.as_nairu_linear()
    us = np.linspace(0.0, 0.10, 6)
    d = max(abs(bp.omega_w(u) - np0.omega_w(u)) for u in us)
    print(f"      ω_w0 = β·C+(1−β)·ω_e = {np0.omega_w0:.4f}   b = (1−β)·k = {np0.b:.4f}")
    print(f"      max|ω_w(u) bargain − v0 linear| over u = {d:.1e};  u* match: "
          f"{abs(bp.nairu - np0.nairu):.1e}")
    assert d < 1e-12 and abs(bp.nairu - np0.nairu) < 1e-12, "γ=1 does not reduce to nairu v0"
    print("      ⇒ the 'ad hoc' linear discipline function WAS the bargaining solution (γ=1).")


def microfoundation():
    print("\n[1] MICRO-FOUNDATION + reproduction — ω_w(u) derived; sim π == closed form:")
    bp = BargainParams()
    print(f"      ω_w(u) = β·C + (1−β)(ω_e − k·u^γ);  NAIRU u* = {bp.nairu*100:.2f}%  (illustrative)")
    worst = 0.0
    for u in (0.02, 0.04, bp.nairu, 0.07):
        e = ConflictEconomy(bp.conflict_at(u))
        for _ in range(20000): e.step()
        pc = bp.steady_pi(u); worst = max(worst, abs(pc - e.last_pi))
        print(f"      u={u:.4f}: closed π={pc:.6f}  sim π={e.last_pi:.6f}  Δ={abs(pc-e.last_pi):.1e}")
    assert worst < 1e-9
    print(f"      worst Δ = {worst:.1e} ⇒ verified against the CYB-6 sim.")


def decomposition():
    print("\n[2] DECOMPOSITION — u* depends on BOTH frictions AND power (one optimizing model):")
    base = dict(beta=0.60, ceiling=0.90, omega_e=0.70, k=8.0, gamma=1.0, omega_f=0.65)
    print("    FRICTIONAL levers (the mainstream's part):")
    for kk in (6.0, 8.0, 10.0):
        print(f"      cost-of-job-loss k={kk:<5}: u* = {BargainParams(**{**base,'k':kk}).nairu*100:5.2f}%")
    for oe in (0.68, 0.70, 0.72):
        print(f"      reemployed share ω_e={oe:<4}: u* = {BargainParams(**{**base,'omega_e':oe}).nairu*100:5.2f}%")
    print("    POWER levers (what the frictional u* omits):")
    for bt in (0.50, 0.60, 0.70):
        print(f"      worker power β={bt:<5}:    u* = {BargainParams(**{**base,'beta':bt}).nairu*100:5.2f}%")
    for of in (0.70, 0.65, 0.60):
        print(f"      firm markup ω_f={of:<5}:   u* = {BargainParams(**{**base,'omega_f':of}).nairu*100:5.2f}%")


def k_for_ustar(gamma, ustar, base):
    """k that puts the NAIRU at `ustar` for a given γ — lets us isolate the CURVATURE dial from the
    u*-shift. From u*^γ = num/((1−β)k):  k = num / ((1−β)·u*^γ)."""
    num = base["beta"] * base["ceiling"] + (1 - base["beta"]) * base["omega_e"] - base["omega_f"]
    return num / ((1 - base["beta"]) * ustar ** gamma)


def gamma_dial():
    print("\n[3] THE γ DIAL — the outside-option convexity sets the Phillips-curve CURVATURE")
    print("    (u* held at 5.0% by adjusting k, so only the SHAPE moves):")
    base = dict(beta=0.60, ceiling=0.90, omega_e=0.70, omega_f=0.65); USTAR = 0.05
    curves = {}
    for gamma in (0.5, 1.0, 2.0, 3.0):
        k = k_for_ustar(gamma, USTAR, base)
        bp = BargainParams(**base, k=k, gamma=gamma)
        us = np.linspace(1e-4, USTAR, 200)
        pis = np.array([bp.steady_pi(u) for u in us])
        # curvature signature: slope over the first vs last third of [0,u*]
        s_lo = (pis[len(pis)//3] - pis[0]) / (us[len(us)//3] - us[0])
        s_hi = (pis[-1] - pis[-len(pis)//3]) / (us[-1] - us[-len(us)//3])
        shape = "convex (flat then steep)" if abs(s_hi) > abs(s_lo)*1.15 else \
                ("concave (steep then flat)" if abs(s_lo) > abs(s_hi)*1.15 else "~linear")
        curves[gamma] = (us, pis, bp)
        print(f"      γ={gamma:<4}: |slope| low-u {abs(s_lo):.3f} vs high-u {abs(s_hi):.3f}  ⇒ {shape}")
    print("    γ>1 (convex cost of job loss): inflation is FLAT when the market is TIGHT (low u) and steep")
    print("    when SLACK — it FLATTENS near full employment (the post-2010 'flat Phillips curve' shape).")
    print("    γ<1 does the reverse: it STEEPENS near full employment. The curvature SIGN is a fingerprint")
    print("    target, not a claim — which shape the real Phillips curve takes is the open empirical question.")
    return curves


def determinism():
    def trace():
        e = ConflictEconomy(BargainParams(gamma=2.0).conflict_at(0.02)); return e.run(400), e
    (a, ea), (b, _) = trace(), trace()
    print(f"\n[4] DETERMINISM — byte-identical rerun: {np.array_equal(a, b)}; "
          f"conservation residual over the 400-step trajectory = {ea.max_residual:.1e}")
    assert np.array_equal(a, b)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-20 (NAIRU) v1: the discipline function micro-founded; the outside option a dial ===")
    print("    ILLUSTRATION under bargaining primitives — not proof, not empirics.\n")
    nesting(); microfoundation(); decomposition()
    curves = gamma_dial(); determinism()
    make_figure(out, curves)
    print(f"\n  figure → {out/'cybeersym_nairu_v1_microfounded.png'}")


def make_figure(out, curves):
    INK, GRID = "#1b1b1b", "#d8d8d8"
    cols = {0.5: "#2b6cb0", 1.0: "#1b1b1b", 2.0: "#c1440e", 3.0: "#8a2be2"}
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.0))

    # Left: the outside option / bargained target ω_w(u) for each γ (the dial on the mechanism)
    for gamma, (us, pis, bp) in curves.items():
        uu = np.linspace(0, 0.05, 200)
        axL.plot(uu * 100, [bp.omega_w(u) for u in uu], lw=2.0, color=cols[gamma], label=f"γ={gamma}")
    axL.axhline(0.65, color="#888", lw=1.0, ls=":"); axL.text(0.1, 0.652, "ω_f (firm target) ⇒ NAIRU where ω_w crosses", fontsize=8, color="#555")
    axL.set_xlabel("unemployment u (%)"); axL.set_ylabel("bargained worker target  ω_w(u)")
    axL.set_title("The dial: outside-option convexity γ shapes the\nbargained target ω_w(u) (u* held at 5%)", fontsize=10)
    axL.legend(frameon=False, fontsize=9, title="cost-of-job-loss\nconvexity γ"); axL.grid(True, color=GRID, lw=0.7); axL.set_axisbelow(True)

    # Right: the resulting Phillips curves — curvature dialed by γ
    for gamma, (us, pis, bp) in curves.items():
        axR.plot(us * 100, pis * 100, lw=2.1, color=cols[gamma], label=f"γ={gamma}")
    axR.set_xlabel("unemployment u (%)"); axR.set_ylabel("steady inflation π* (%/step)")
    axR.set_title("γ dials the Phillips-curve CURVATURE\n(γ>1: flat when TIGHT/low-u, steep when SLACK)", fontsize=10)
    axR.legend(frameon=False, fontsize=9, title="γ"); axR.grid(True, color=GRID, lw=0.7); axR.set_axisbelow(True)

    fig.suptitle("CYB-20 v1 — NAIRU micro-founded from bargaining; the outside option is a dial (illustrative)", fontsize=11, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out / "cybeersym_nairu_v1_microfounded.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
