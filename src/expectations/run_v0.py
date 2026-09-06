"""
Cybeersym — CYB-20 v0: the expectations channel and its DE-ANCHORING bifurcation.

Run from inside src/expectations:  python3 run_v0.py

Self-tests + characterization (all printed; a figure regenerated):
  0. NESTING — phi_e=0 ⇒ CYB-6 ConflictEconomy byte-exact (Δ = 0.0).
  1. CONSERVATION — shares partition 1 on a REAL trajectory (not the fixed point), worst < 1e-9.
  2. CLOSED FORM — steady π = α_w·g/(1+α_w/α_p−φ_e) matches the sim to machine precision below
     threshold, and the de-anchoring threshold φ_e* = 1+α_w/α_p tracks the α_w/α_p ratio.
  3. THE BIFURCATION (the honest part) — located by the Jacobian eigenvalues of the reduced 2-D
     map (chaos/linearize), NOT by finite-time overflow. Separates the DYNAMIC-stability boundary
     (|leading eig|→1, the equilibrium exists but its PATH goes unstable) from the STEADY-STATE
     de-anchoring (φ_e=1+α_w/α_p, the equilibrium ceases to exist). Reports the bifurcation type.
  4. DETERMINISM — byte-identical rerun.
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path
import importlib.util as _ilu

from model import ExpectationsParams, ExpectationsEconomy, ConflictParams, ConflictEconomy

def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    m = _ilu.module_from_spec(spec); spec.loader.exec_module(m); return m
_lin = _load("linearize", "chaos/linearize.py")
jacobian, eigs, fixed_point_newton = _lin.jacobian, _lin.eigs, _lin.fixed_point_newton


def nesting():
    print("[0] NESTING — phi_e=0 ⇒ CYB-6 conflict byte-exact:")
    cp = ConflictParams()                       # defaults: ω_f=0.65,g=0.10,α_w=α_p=0.30,floor,trig=0.10
    e = ExpectationsEconomy(ExpectationsParams(conflict=cp, phi_e=0.0, lam=0.5))
    c = ConflictEconomy(cp)
    d = 0.0
    for _ in range(1000):
        e.step(); c.step()
        d = max(d, abs(e.W - c.W), abs(e.P - c.P))
    print(f"    max|W,P Δ| over 1000 steps = {d:.1e}   byte-identical = {d == 0.0}")
    assert d == 0.0, "NESTING LEAK: phi_e=0 did not reproduce CYB-6"
    print("    -> CYB-6 ⊂ expectations (phi_e=0), byte-exact.")


def conservation():
    p = ExpectationsParams(conflict=ConflictParams(), phi_e=1.0, lam=0.3)   # a real (inflating) run
    e = ExpectationsEconomy(p)
    for _ in range(2000): e.step()
    print(f"\n[1] CONSERVATION — worst share residual on a real trajectory = {e.max_residual:.1e}  "
          f"(< 1e-9; wage+profit partition 1 through the spiral)")
    assert e.max_residual < 1e-9


def closed_form():
    print("\n[2] CLOSED FORM — steady π = α_w·g/(1+α_w/α_p−φ_e):")
    p = ExpectationsParams(conflict=ConflictParams(), phi_e=0.0, lam=0.3)
    print(f"    de-anchoring threshold φ_e* = 1 + α_w/α_p = {p.deanchor_threshold:.3f}  "
          f"(NOT the textbook accelerationist φ_e=1)")
    print("    φ_e     sim π (20k steps)     closed-form        Δ")
    for phi in (0.0, 0.5, 1.0):
        e = ExpectationsEconomy(ExpectationsParams(conflict=ConflictParams(), phi_e=phi, lam=0.3))
        for _ in range(20000): e.step()
        cf = p.steady_pi(phi)
        print(f"    {phi:<5.2f}   {e.last_pi:>16.6f}   {cf:>14.6f}   {abs(e.last_pi-cf):.1e}")
        assert abs(e.last_pi - cf) < 1e-9
    print("    threshold φ_e* = 1+α_w/α_p tracks the conflict balance:")
    for aw, ap in [(0.30, 0.30), (0.20, 0.40), (0.40, 0.20), (0.10, 0.30)]:
        q = ExpectationsParams(conflict=ConflictParams(alpha_w=aw, alpha_p=ap))
        print(f"      α_w={aw}, α_p={ap}:  φ_e* = {q.deanchor_threshold:.3f}")


def dyn_at(phi_e, lam=0.3, aw=0.30, ap=0.30):
    """(xstar, residual, eigenvalues) of the reduced 2-D map's fixed point, via linearize."""
    p = ExpectationsParams(conflict=ConflictParams(alpha_w=aw, alpha_p=ap), phi_e=phi_e, lam=lam)
    ss = p.steady_state()
    if ss is None: return None
    e = ExpectationsEconomy(p)
    xstar, res = fixed_point_newton(e.step_vector, np.array(ss))
    return xstar, res, eigs(jacobian(e.step_vector, xstar))


def physical_deanchor(p):
    """φ_e where the steady wage share ω* first hits 1 (workers capture the whole pie; profit→0) —
    the economically meaningful de-anchoring, BELOW the formal π*→∞ threshold. π* at ω*=1 is
    α_p(1−ω_f); invert π*(φ)=that."""
    pi_phys = p.alpha_p * (1.0 - p.omega_f)
    return p.deanchor_threshold - p.alpha_w * p.gap / pi_phys, pi_phys


def bifurcation():
    print("\n[3] THE BIFURCATION — reduced 2-D (ω,π^e) map, eigenvalues via chaos/linearize:")
    p0 = ExpectationsParams()
    thr = p0.deanchor_threshold
    phi_phys, pi_phys = physical_deanchor(p0)
    print(f"    formal de-anchoring   φ_e* = 1+α_w/α_p = {thr:.3f}  (π*→∞; but ω*→∞ too ⇒ UNPHYSICAL branch)")
    print(f"    PHYSICAL de-anchoring φ_e_phys = {phi_phys:.3f}  (steady wage share ω*→1: workers capture the")
    print(f"      whole pie, profit share→0; π*={pi_phys:.3f}) — the economically meaningful border, below φ_e*.")
    grid = np.round(np.linspace(0.0, thr - 0.01, 40), 4)
    mods, omegas, imags, reals = [], [], [], []
    for phi in grid:
        xstar, res, ev = dyn_at(phi)
        mods.append(float(abs(ev[0]))); omegas.append(float(xstar[0]))
        imags.append(abs(complex(ev[0]).imag)); reals.append(float(complex(ev[0]).real))
    mods, omegas, imags, reals = map(np.array, (mods, omegas, imags, reals))
    phys = omegas <= 1.0
    max_imag = float(imags.max())               # swept, not a single point
    print(f"    leading |eig|: {mods[0]:.4f} (φ_e=0) → {mods[phys][-1]:.4f} (last physical, ω*≤1) "
          f"→ {mods[-1]:.4f} (φ_e={grid[-1]}, unphysical)")
    print(f"    |leading eig| < 1 throughout the equilibrium's existence ⇒ LOCALLY STABLE. The leading")
    print(f"      eigenvalue is REAL across the whole sweep (max |Im| = {max_imag:.1e}) and its real part")
    print(f"      → +1 as the equilibrium escapes to ∞ at φ_e* ({reals[-1]:.4f} at φ_e={grid[-1]}): a")
    print(f"      +1-multiplier de-anchoring (steady-π pole), NOT a Hopf (no complex pair) or flip (not −1).")
    print(f"    (NB: my scratch probe's 'dynamic boundary below threshold' was a transient/basin overshoot")
    print(f"      from a far start — NOT a local instability. Eigenvalue-located ⇒ n-stable; the linearize")
    print(f"      instrument corrects the probe.)")
    assert (mods[phys] < 1.0).all(), "equilibrium not stable across the physical range"
    assert max_imag < 1e-9, "leading eigenvalue is not real across the sweep"
    return grid, mods, omegas, thr, phi_phys


def determinism():
    def trace():
        e = ExpectationsEconomy(ExpectationsParams(conflict=ConflictParams(), phi_e=1.2, lam=0.3))
        return e.run(500)
    a, b = trace(), trace()
    print(f"\n[4] DETERMINISM — byte-identical rerun: {np.array_equal(a, b)}")
    assert np.array_equal(a, b)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-20 v0: the expectations channel & its de-anchoring bifurcation ===\n")
    nesting(); conservation(); closed_form()
    grid, mods, omegas, thr, phi_phys = bifurcation()
    determinism()
    make_figure(out, grid, mods, omegas, thr, phi_phys)
    print(f"\n  figure → {out/'cybeersym_expectations_v0_deanchoring.png'}")


def make_figure(out, grid, mods, omegas, thr, phi_phys):
    INK, GRID, ACC, BLU = "#1b1b1b", "#d8d8d8", "#c1440e", "#2b6cb0"
    p = ExpectationsParams()
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.0))

    # Left: steady π* and steady ω* vs φ_e — the physical de-anchoring (ω*→1) below the formal one.
    xs = np.linspace(0.0, thr - 3e-3, 400)
    pis = np.array([p.steady_pi(x) for x in xs])
    oms = np.array([p.omega_f + pi / p.alpha_p for pi in pis])
    axL.plot(xs, pis, lw=2.2, color=INK, label="steady inflation π*")
    axL.plot(xs, oms, lw=2.2, color=BLU, label="steady wage share ω*")
    axL.axhline(1.0, color=BLU, lw=0.9, ls=":")
    axL.axvline(phi_phys, color=ACC, lw=1.7, ls="--", label=f"PHYSICAL de-anchor ω*→1: φ_e={phi_phys:.2f}")
    axL.axvline(thr, color="#888", lw=1.2, ls="-.", label=f"formal φ_e*=1+α_w/α_p={thr:.2f} (unphysical)")
    axL.axvline(1.0, color="#bbb", lw=1.0, ls=":", label="textbook φ_e=1")
    axL.set_ylim(0, 2.0); axL.set_xlabel("expectations pass-through  φ_e")
    axL.set_ylabel("π*   and   ω*")
    axL.set_title("Expectations pass-through drives a wage–price spiral:\nπ* rises and ω*→1 (workers take the whole pie) at φ_e_phys", fontsize=10)
    axL.legend(frameon=False, fontsize=8); axL.grid(True, color=GRID, lw=0.7); axL.set_axisbelow(True)

    # Right: leading |eig| of the 2-D map — stable (<1) throughout; →1 at the fold (n-stable).
    phys = omegas <= 1.0
    axR.plot(grid[phys], mods[phys], "-o", ms=3.5, lw=1.7, color=INK, label="leading |eig| (physical, ω*≤1)")
    axR.plot(grid[~phys], mods[~phys], "-o", ms=3.5, lw=1.3, color="#aaa", label="leading |eig| (unphysical, ω*>1)")
    axR.axhline(1.0, color="#888", lw=1.0, ls="-")
    axR.axvline(phi_phys, color=ACC, lw=1.7, ls="--", label=f"physical φ_e={phi_phys:.2f}")
    axR.axvline(thr, color="#888", lw=1.2, ls="-.", label=f"escape φ_e*={thr:.2f}")
    axR.set_xlabel("expectations pass-through  φ_e"); axR.set_ylabel("leading |eigenvalue| of the (ω,π^e) map")
    axR.set_title("Locally STABLE throughout (|eig|<1); real eig → +1 only as\nthe equilibrium escapes — not a Hopf/flip; eigenvalue-located, n-stable", fontsize=10)
    axR.legend(frameon=False, fontsize=8); axR.grid(True, color=GRID, lw=0.7); axR.set_axisbelow(True)

    fig.suptitle("CYB-20 v0 — the expectations channel: a +1-multiplier de-anchoring at φ_e set by the conflict balance", fontsize=11, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out / "cybeersym_expectations_v0_deanchoring.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
