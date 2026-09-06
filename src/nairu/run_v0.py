"""
Cybeersym — CYB-20 (NAIRU): the natural rate as a DISTRIBUTIONAL equilibrium.  v0.

Run from inside src/nairu:  python3 run_v0.py

**Illustration under an explicit, contestable assumption — NOT a proof, NOT an empirical claim.**
Structure (the project's orthodox-special-case → assumption → divergence template):
  0. REPRODUCTION — the sim's steady inflation equals the closed form c·g(u) (rigour: sim, not algebra).
  1. CONSERVATION — inherited CYB-6 partition holds on a real (inflating) trajectory.
  2. ORTHODOX SPECIAL CASE — a NAIRU u* with a downward-sloping Phillips curve; stable at u*.
  3. THE ASSUMPTION — orthodoxy's u* is a technical constant; here u*=(ω_w0−ω_f)/b is distributional.
  4. DIVERGENCE — u* shifts with firm power (ω_f) and worker militancy (ω_w0); no friction involved.
  5. POLICY (dynamical illustration) — after a markup shock, two disinflation PATHS run as real
     trajectories: (A) raise u to the new u* (recession); (B) compress the gap at the SAME u
     (incomes policy). Both kill the inflation; only A needs the unemployment. Illustrative only.
  6. DETERMINISM — byte-identical rerun.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import NairuParams, NairuEconomy, ConflictParams, ConflictEconomy


def reproduction():
    print("[0] REPRODUCTION — sim steady π == closed form c·g(u) (rigour check, not just algebra):")
    p = NairuParams()
    print(f"      u        g(u)       π* closed     π* sim(model)     Δ")
    worst = 0.0
    for u in (0.02, 0.04, p.nairu, 0.06, 0.08):
        pc = p.steady_pi(u); ps = NairuEconomy(p, u).steady_pi()
        worst = max(worst, abs(pc - ps))
        print(f"      {u:.4f}   {p.gap(u):+.4f}   {pc:>10.6f}   {ps:>13.6f}   {abs(pc-ps):.1e}")
    assert worst < 1e-9, "sim does not match the closed form"
    print(f"      worst Δ = {worst:.1e}  ⇒ the closed form is the model's, verified.")


def conservation():
    e = NairuEconomy(NairuParams(), u=0.02)          # below u*, inflating
    for _ in range(4000): e.step()
    print(f"\n[1] CONSERVATION — worst share residual on a real trajectory = {e.max_residual:.1e}  (< 1e-9)")
    assert e.max_residual < 1e-9


def orthodox_special_case():
    p = NairuParams()
    print(f"\n[2] ORTHODOX SPECIAL CASE (reproduced): ω_f={p.omega_f}, ω_w0={p.omega_w0}, b={p.b}")
    print(f"      NAIRU u* = (ω_w0−ω_f)/b = {p.nairu:.4f}  ({p.nairu*100:.2f}% unemployment) — where g(u*)=0.")
    print(f"      Phillips curve: below u* inflation is positive; at/above u* it is stable (floor binds).")


def the_assumption_and_divergence():
    print("\n[3] THE ASSUMPTION: orthodoxy's u* is a TECHNICAL/FRICTIONAL constant, invariant to")
    print("    distribution. Here u* = (ω_w0−ω_f)/b is a FUNCTION of the distributional parameters.")
    print("\n[4] DIVERGENCE: sweep firm power (ω_f) and worker militancy (ω_w0) — the NAIRU SHIFTS:")
    print("      ω_f (markup)   u*          |   ω_w0 (militancy)   u*")
    for uf, ww in [(0.70, 0.80), (0.65, 0.85), (0.60, 0.90), (0.55, 0.95)]:
        ua = NairuParams(omega_f=uf).nairu; ub = NairuParams(omega_w0=ww).nairu
        print(f"      {uf:.2f}           {ua*100:5.2f}%      |   {ww:.2f}                 {ub*100:5.2f}%")
    print("    Firm power↑ (ω_f↓) or militancy↑ (ω_w0↑) RAISES the NAIRU — no friction anywhere.")


def scenario(policy, n0=100, n1=150, n2=250):
    """Dynamical illustration. Phase 0: stable at u_old, ω_f=0.65. Phase 1: markup shock ω_f→0.60
    (gap opens). Phase 2: policy ∈ {'recession','incomes'}. Returns (pi[t], u[t])."""
    p = NairuParams()
    u_old = p.nairu                                  # 0.05
    e = ConflictEconomy(p.conflict_at(u_old))        # phase 0: g=0, stable
    pis, us = [], []
    def run(steps, omega_f, u):
        e.p.omega_f = omega_f
        e.p.gap = (p.omega_w0 - p.b * u) - omega_f    # g(u) at this markup
        for _ in range(steps):
            e.step(); pis.append(e.last_pi); us.append(u)
    run(n0, 0.65, u_old)                             # phase 0: stable
    run(n1, 0.60, u_old)                             # phase 1: markup shock at old u ⇒ inflation
    if policy == "recession":
        u_new = NairuParams(omega_f=0.60).nairu       # 0.0625: raise u to the NEW NAIRU
        run(n2, 0.60, u_new)                          # phase 2A: more unemployment closes the gap
    else:  # 'incomes'
        run(n2, 0.65, u_old)                          # phase 2B: compress the markup at the SAME u
    return np.array(pis), np.array(us)


def policy_illustration():
    print("\n[5] POLICY (dynamical illustration — a mechanism under the stated assumption, NOT a claim):")
    piA, uA = scenario("recession"); piB, uB = scenario("incomes")
    print(f"      markup shock ω_f 0.65→0.60 raises u* from {NairuParams().nairu*100:.2f}% to "
          f"{NairuParams(omega_f=0.60).nairu*100:.2f}%.")
    print(f"      Path A (orthodox, recession): raise u to {uA[-1]*100:.2f}% ⇒ tail π = {piA[-50:].mean():+.5f} (stable).")
    print(f"      Path B (incomes policy):      hold u at {uB[-1]*100:.2f}%, compress the gap ⇒ tail π = "
          f"{piB[-50:].mean():+.5f} (stable) — NO recession.")
    print("      Both kill the inflation; only A pays with unemployment. Illustrative of the assumption.")
    return piA, uA, piB, uB


def determinism():
    a = scenario("incomes")[0]; b = scenario("incomes")[0]
    print(f"\n[6] DETERMINISM — byte-identical rerun: {np.array_equal(a, b)}")
    assert np.array_equal(a, b)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-20 (NAIRU): the natural rate as a distributional equilibrium ===")
    print("    ILLUSTRATION under the discipline assumption ω_w(u)=ω_w0−b·u — not proof, not empirics.\n")
    reproduction(); conservation(); orthodox_special_case(); the_assumption_and_divergence()
    piA, uA, piB, uB = policy_illustration(); determinism()
    make_figure(out, piA, uA, piB, uB)
    print(f"\n  figure → {out/'cybeersym_nairu_v0_distributional.png'}")


def make_figure(out, piA, uA, piB, uB):
    INK, GRID, ACC, BLU = "#1b1b1b", "#d8d8d8", "#c1440e", "#2b6cb0"
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.0))

    # Left: two Phillips curves (two markup regimes) — the NAIRU shifts with distribution.
    us = np.linspace(0.0, 0.12, 300)
    for omega_f, col, lab in [(0.65, INK, "ω_f=0.65 (baseline)"), (0.60, ACC, "ω_f=0.60 (higher markup)")]:
        p = NairuParams(omega_f=omega_f)
        pis = np.array([p.steady_pi(u) for u in us])
        axL.plot(us * 100, pis * 100, lw=2.3, color=col, label=f"{lab}:  u*={p.nairu*100:.2f}%")
        axL.axvline(p.nairu * 100, color=col, lw=1.1, ls=":")
    axL.set_xlabel("unemployment u  (%)"); axL.set_ylabel("steady inflation π*  (%/step)")
    axL.set_title("The NAIRU is distributional: a higher markup shifts u* RIGHT\n(illustration under the discipline assumption)", fontsize=10)
    axL.legend(frameon=False, fontsize=9); axL.grid(True, color=GRID, lw=0.7); axL.set_axisbelow(True)

    # Right: the two disinflation PATHS after a markup shock — π(t) and the u cost.
    t = np.arange(len(piA))
    axR.plot(t, piA * 100, lw=1.8, color=ACC, label=f"A: recession (u→{uA[-1]*100:.2f}%)")
    axR.plot(t, piB * 100, lw=1.8, color=BLU, ls="--", label=f"B: incomes policy (u stays {uB[-1]*100:.2f}%)")
    axR.axvspan(100, 250, color="#f2c", alpha=0.05); axR.text(102, axR.get_ylim()[1]*0.9, "markup shock", fontsize=8, color="#555")
    axR.axvline(250, color="#999", lw=1.0, ls=":"); axR.text(252, axR.get_ylim()[1]*0.9, "policy", fontsize=8, color="#555")
    axR.set_xlabel("step"); axR.set_ylabel("inflation π  (%/step)")
    axR.set_title("Same disinflation, different unemployment cost\n(both →0; only A pays with a recession)", fontsize=10)
    axR.legend(frameon=False, fontsize=9); axR.grid(True, color=GRID, lw=0.7); axR.set_axisbelow(True)

    fig.suptitle("CYB-20 v0 — NAIRU as distributional equilibrium (illustrative; assumption-dependent, not proof)", fontsize=11, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out / "cybeersym_nairu_v0_distributional.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
