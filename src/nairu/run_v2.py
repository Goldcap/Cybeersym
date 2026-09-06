"""
Cybeersym — CYB-20 (NAIRU) v2: micro-found the γ dial from matching; compose expectations × NAIRU.

Run from inside src/nairu:  python3 run_v2.py

**Illustration under stated primitives — not proof, not empirics.** Two deepenings:

  v2a — γ FROM MATCHING. v1 left the cost-of-job-loss convexity γ a free dial; a Cobb–Douglas
        job-finding rate pins it: γ = 1 − a (a = matching elasticity). Since a∈(0,1), γ∈(0,1) is
        ALWAYS concave ⇒ the matching microfoundation predicts a Phillips curve that STEEPENS near
        full employment (a checkable fingerprint) — not the flat-when-tight (γ>1) shape.

  v2b — EXPECTATIONS × NAIRU. Below u* the aspiration gap g(u)>0 is open; the CYB-20 expectations
        channel TRANSMITS/de-anchors it. Combined steady inflation π(u,φ_e)=α_w·g(u)/(1+α_w/α_p−φ_e).
        The two borders are ORTHOGONAL — u* is set by distribution (φ_e-independent), the de-anchoring
        φ_e*=1+α_w/α_p is set by the adjustment structure (u-independent) — and de-anchoring is GATED
        by u<u* (expectations are inert where the gap is closed). This reframes the accelerationist
        NAIRU: below u* the *open distributional gap* is what expectations amplify — not expectations
        conjuring inflation from nothing.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import importlib.util as _ilu

from model import BargainParams, NairuParams, ConflictParams, ConflictEconomy, gamma_from_matching

def _load(name, rel):
    s = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    m = _ilu.module_from_spec(s); s.loader.exec_module(m); return m
_exp = _load("expectations_model", "expectations/model.py")
ExpectationsParams, ExpectationsEconomy = _exp.ExpectationsParams, _exp.ExpectationsEconomy

AW = AP = 0.30
PHI_STAR = 1.0 + AW / AP                      # expectations de-anchoring threshold (u-independent)


# ---------- v2a: γ micro-founded from matching ----------
def matching_gamma():
    print("[v2a] γ FROM MATCHING — γ = 1 − a (Cobb–Douglas job-finding rate), no longer a free dial:")
    for a in (0.3, 0.5, 0.7):
        bp = BargainParams.from_matching(a)
        assert abs(bp.gamma - gamma_from_matching(a)) < 1e-15 and abs(bp.gamma - (1 - a)) < 1e-15
        print(f"      matching elasticity a={a:.2f}  ⇒  γ={bp.gamma:.2f}  (concave, γ<1)")
    # the steepening prediction, at a fixed NAIRU so only the shape shows
    print("    prediction: γ<1 ⇒ the Phillips curve STEEPENS near full employment. At a=0.5 (γ=0.5),")
    base = dict(beta=0.60, ceiling=0.90, omega_e=0.70, omega_f=0.65)
    ustar = 0.05
    num = base["beta"]*base["ceiling"] + (1-base["beta"])*base["omega_e"] - base["omega_f"]
    k = num / ((1 - base["beta"]) * ustar ** 0.5)          # pin u*=5% so only curvature shows
    bp = BargainParams.from_matching(0.5, **base, k=k)
    us = np.linspace(1e-4, bp.nairu, 200); pis = np.array([bp.steady_pi(u) for u in us])
    s_lo = abs((pis[len(pis)//3]-pis[0])/(us[len(us)//3]-us[0]))
    s_hi = abs((pis[-1]-pis[-len(pis)//3])/(us[-1]-us[-len(us)//3]))
    print(f"      |slope| near full employment {s_lo:.3f}  vs when slack {s_hi:.3f}  ⇒ "
          f"{'STEEPER near full employment ✓' if s_lo > s_hi else 'not steeper'}")
    assert s_lo > s_hi
    print("    ⇒ a search/matching labour market forces γ<1: it bites HARDER as the market tightens.")


# ---------- v2b: expectations × NAIRU interaction ----------
def _np(): return NairuParams()   # v0 linear discipline function for g(u)
def pi_closed(u, phi_e):
    g = _np().gap(u)
    if g <= 0.0: return 0.0
    denom = 1.0 + AW/AP - phi_e
    return float("inf") if denom <= 0.0 else AW * g / denom
def pi_sim(u, phi_e, n=20000):
    g = _np().gap(u)
    e = ExpectationsEconomy(ExpectationsParams(conflict=ConflictParams(omega_f=_np().omega_f, gap=g,
                            alpha_w=AW, alpha_p=AP, wage_floor=True), phi_e=phi_e, lam=0.3))
    for _ in range(n):
        try: e.step()
        except Exception: return np.nan
        if not np.isfinite(e.P) or e.P <= 0: return np.nan
    return e.last_pi

def interaction():
    ustar = _np().nairu
    print(f"\n[v2b] EXPECTATIONS × NAIRU — u*={ustar*100:.2f}% (distributional), φ_e*={PHI_STAR:.2f} (expectations):")
    print("    (1) combined π(u,φ_e)=α_w·g(u)/(1+α_w/α_p−φ_e) — sim vs closed form:")
    worst = 0.0
    for u in (0.02, 0.04):
        for phi in (0.0, 1.0):
            pc, ps = pi_closed(u, phi), pi_sim(u, phi); worst = max(worst, abs(pc - ps))
            print(f"        u={u:.3f} φ_e={phi:.1f}: closed {pc:.5f}  sim {ps:.5f}  Δ={abs(pc-ps):.1e}")
    assert worst < 1e-9
    print(f"        worst Δ = {worst:.1e} ⇒ composition verified against the sim.")
    print("    (2) ORTHOGONAL borders (analytic): u*=(ω_w0−ω_f)/b carries NO φ_e; φ_e*=1+α_w/α_p carries")
    print("        NO u. So the NAIRU is set by distribution and the de-anchoring by the adjustment")
    print("        structure — independently. (A finite-horizon SIM overflows earlier & u-dependently:")
    print("        that is the transient overshoot, NOT the steady-state border — see expectations v0.)")
    print("    (3) de-anchoring GATED by the open gap (u<u*): expectations INERT where g≤0:")
    for u in (0.04, ustar, 0.07):
        g = _np().gap(u)
        tag = "de-anchors (g>0)" if (g > 0) else "INERT: π=0 ∀φ_e (g≤0)"
        print(f"        u={u:.4f} g={g:+.4f}: {tag}")
    print("    ⇒ the 'accelerationist NAIRU' reread: below u* the OPEN DISTRIBUTIONAL GAP is what")
    print("      expectations amplify; expectations do not create inflation where no gap is open.")


def determinism():
    def trace():
        e = ExpectationsEconomy(ExpectationsParams(conflict=ConflictParams(gap=_np().gap(0.02),
                                omega_f=_np().omega_f, alpha_w=AW, alpha_p=AP), phi_e=1.0, lam=0.3))
        return e.run(400)
    a, b = trace(), trace()
    print(f"\n[disc] DETERMINISM — byte-identical rerun: {np.array_equal(a, b)}")
    assert np.array_equal(a, b)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-20 (NAIRU) v2: γ from matching; expectations × NAIRU ===")
    print("    ILLUSTRATION under stated primitives — not proof, not empirics.\n")
    matching_gamma(); interaction(); determinism()
    make_figure(out)
    print(f"\n  figure → {out/'cybeersym_nairu_v2_matching_and_expectations.png'}")


def make_figure(out):
    INK, GRID = "#1b1b1b", "#d8d8d8"
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.0))

    # Left (v2a): γ=1−a and the steepening — Phillips curves at fixed u* for γ=1−a (a=0.3,0.5,0.7)
    base = dict(beta=0.60, ceiling=0.90, omega_e=0.70, omega_f=0.65); ustar = 0.05
    num = base["beta"]*base["ceiling"] + (1-base["beta"])*base["omega_e"] - base["omega_f"]
    cols = {0.3: "#2b6cb0", 0.5: "#1b1b1b", 0.7: "#c1440e"}
    for a in (0.3, 0.5, 0.7):
        g = gamma_from_matching(a); k = num / ((1 - base["beta"]) * ustar ** g)
        bp = BargainParams.from_matching(a, **base, k=k)
        us = np.linspace(1e-4, bp.nairu, 200)
        axL.plot(us*100, [bp.steady_pi(u)*100 for u in us], lw=2.1, color=cols[a],
                 label=f"a={a} ⇒ γ={g:.1f}")
    axL.set_xlabel("unemployment u (%)"); axL.set_ylabel("steady inflation π* (%/step)")
    axL.set_title("v2a — γ=1−a from matching (always <1):\nthe Phillips curve STEEPENS near full employment", fontsize=10)
    axL.legend(frameon=False, fontsize=9, title="matching elasticity a"); axL.grid(True, color=GRID, lw=0.7); axL.set_axisbelow(True)

    # Right (v2b): the (u, φ_e) regime map — orthogonal borders, analytic (not sim overflow)
    ustar_np = _np().nairu
    us = np.linspace(0.0, 0.09, 240); phis = np.linspace(0.0, 2.6, 240)
    Z = np.zeros((len(phis), len(us)))
    for i, phi in enumerate(phis):
        for j, u in enumerate(us):
            g = _np().gap(u)
            if g <= 0: Z[i, j] = 0.0                      # stable, π=0 (u≥u*)
            elif (1 + AW/AP - phi) <= 0: Z[i, j] = np.nan  # de-anchored (u<u*, φ_e≥φ_e*)
            else: Z[i, j] = AW * g / (1 + AW/AP - phi)     # stable elevated inflation
    Zm = np.ma.masked_invalid(Z)
    pcm = axR.pcolormesh(us*100, phis, np.clip(Zm, 0, 0.10)*100, cmap="YlOrRd", shading="auto")
    axR.contourf(us*100, phis, np.isnan(Z), levels=[0.5, 1.5], colors=["#3a0a0a"])
    axR.axvline(ustar_np*100, color=INK, lw=1.4, ls="--"); axR.axhline(PHI_STAR, color=INK, lw=1.4, ls=":")
    axR.text(ustar_np*100+0.1, 0.15, f"u*={ustar_np*100:.1f}%\n(distributional)", fontsize=8, color=INK)
    axR.text(0.15, PHI_STAR+0.05, f"φ_e*={PHI_STAR:.1f} (expectations)", fontsize=8, color=INK)
    axR.text(1.4, 2.3, "de-anchored\n(open gap ×\nde-anchored φ_e)", fontsize=8, color="w", ha="center")
    axR.text(6.6, 1.3, "stable π=0\n(u≥u*: no gap)", fontsize=8, color=INK, ha="center")
    axR.set_xlabel("unemployment u (%)"); axR.set_ylabel("expectations pass-through φ_e")
    axR.set_title("v2b — orthogonal borders; de-anchoring GATED by u<u*\n(colour = elevated stable π; analytic, not sim overflow)", fontsize=10)
    fig.colorbar(pcm, ax=axR, label="steady π (%/step)")

    fig.suptitle("CYB-20 v2 — γ micro-founded from matching; expectations × NAIRU (illustrative)", fontsize=11, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out / "cybeersym_nairu_v2_matching_and_expectations.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
