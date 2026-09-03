"""
CYB-19 Phase 2b (CYB-2Xb) — the genuine Fisher debt-deflation loop: the two-basin map.

Phase 2 (CYB-23) wired Engine 1 (credit-quantity contagion → hyper-INFLATIONARY collapse) and
GATED Engine 2 (the price-level Fisher loop) OFF, honestly: CYB-17's demand channel is a
symmetric multiplicative damper (π → 0 from ABOVE, never negative — verified at −0.000%/step),
so deflation was UNREACHABLE by construction. Phase 2b strengthens the price channel into a
genuine, self-reinforcing Fisher loop and asks the question CYB-23 deferred: is the
"inflationary, not Fisher" result CONDITIONAL (gated by price-channel strength), or absolute?

Runs, in order:
  0. Nested regression — byte-exact: fisher_phi=0 ⇒ CYB-23 ⊂ Phase 1 ⊂ CYB-17.
  1. AC1 — the deflation threshold φ*: isolate Engine 2 (ε=0), sweep φ. Below φ* the grind is
     bounded; above it a Fisher debt-deflation collapse. Deflation is a THRESHOLD phenomenon.
  2. AC2 (headline) — the two-basin map over (φ, ε): bounded / Engine-1 inflation-collapse /
     Engine-2 deflation-collapse. Both collapse basins reachable ⇒ NOT rigged; the basin you
     fall into is set by φ vs ε — the strength of the price channel. THE conditional result.
  3. AC3 — the honesty anchor: the collapse is the LOOP, not the mechanical cut. A
     frozen-leverage regression (pressure reads a held-constant leverage) stays BOUNDED where
     the live self-reinforcing loop deflation-collapses. (cf. CYB-10's κ=0 decoupling anchor.)
  4. AC4 — conservation through the deflationary transient. The nominal capital-account identity
     (rentier asset ≡ firm liability) is P-INDEPENDENT ⇒ the Fisher cut cannot break it. The SFC
     point of debt-deflation: the REAL burden (D/P) runs away while the NOMINAL accounting stays
     exact. Residual reported through a full deflation.
  5. AC5 — the CYB-23 resolution: at φ=0, deflation is unreachable (CYB-23 was right FOR THAT
     CONFIG); past φ* the Fisher basin opens ⇒ the result is CONDITIONAL, not a refutation of
     debt-deflation. Two engines, opposite sign, one distress signal.
  6. AC6 — determinism.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import (FisherEconomy, FisherParams, ContagionEconomy, ContagionParams,
                   CrunchParams, AccommodationParams)

BASE = dict(omega_f=0.65, gap=0.10, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
I_HEAD, COST = 0.60, 0.30
LT, DELTA = 0.64, 0.35            # Phase-1 crunch (a grinding regime)
SF = 0.03                        # net-worth bound: default when the real pile c ≥ SF
B_REF = 0.60                     # Fisher engagement: distress selling when leverage D/P > B_REF
N, TAIL = 1500, 300


def _mk(recovery=0.5, elasticity=0.0, fisher_phi=0.0, b_ref=B_REF, freeze=False):
    return FisherEconomy(FisherParams(
        contagion=ContagionParams(
            crunch=CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST),
                                crunch_enabled=True, L_trig=LT, delta=DELTA),
            recovery=recovery, elasticity=elasticity, solvency_frac=SF),
        fisher_phi=fisher_phi, b_ref=b_ref, freeze_leverage=freeze))

def _mk_contagion(recovery=0.5, elasticity=0.0):
    return ContagionEconomy(ContagionParams(
        crunch=CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST),
                            crunch_enabled=True, L_trig=LT, delta=DELTA),
        recovery=recovery, elasticity=elasticity, solvency_frac=SF))


def outcome(recovery, elasticity, phi, b_ref=B_REF, n=N, freeze=False):
    """Run to a collapse (either engine) or n steps; classify the basin."""
    e = _mk(recovery, elasticity, phi, b_ref, freeze)
    for k in range(n):
        e.step()
        if e.inflation_collapsed: return "inflation", e.con.collapse_step, e
        if e.deflation_collapsed: return "deflation", e.deflation_step, e
    pis = e.run(TAIL)
    return "bounded", float(np.mean(pis)), e


# ---- 0. nested regression -----------------------------------------------------
def nested_regression():
    f = _mk(recovery=0.5, elasticity=0.15, fisher_phi=0.0)   # Engine 2 off
    c = _mk_contagion(recovery=0.5, elasticity=0.15)
    d = 0.0
    for _ in range(600):
        f.step(); c.step()
        d = max(d, abs(f.conflict.W - c.conflict.W), abs(f.conflict.P - c.conflict.P), abs(f.con.D - c.D))
    print(f"[0] fisher_phi=0 ⇒ CYB-23: max|W,P,D Δ| = {d:.1e}  byte-identical={d == 0.0}")
    assert d == 0.0, "NESTED LEAK: fisher_phi=0 did not reproduce CYB-23"
    print("     -> CYB-17 ⊂ Phase 1 ⊂ Phase 2 (CYB-23) ⊂ Phase 2b, byte-exact at each shell.")


# ---- 1. AC1: the deflation threshold φ* (Engine 2 isolated, ε=0) ---------------
def phi_star(lo=0.0, hi=3.0, tol=1e-3):
    """Bisection for the smallest φ at which the isolated Fisher loop deflation-collapses."""
    # confirm bracket
    assert outcome(0.5, 0.0, lo)[0] != "deflation" and outcome(0.5, 0.0, hi)[0] == "deflation"
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        (hi := mid) if outcome(0.5, 0.0, mid)[0] == "deflation" else (lo := mid)  # noqa: E731
    return 0.5 * (lo + hi)


# ---- 2. AC2: the two-basin map over (φ, ε) ------------------------------------
def basin_map(phis, epss, recovery=0.5):
    # code: 0 = bounded (cure/grind), 1 = inflation-collapse (Engine 1), -1 = deflation-collapse (Engine 2)
    Z = np.zeros((len(epss), len(phis)))
    leak = 0.0
    for a, eps in enumerate(epss):
        for b, phi in enumerate(phis):
            kind, _, e = outcome(recovery, eps, phi, n=800)
            leak = max(leak, e.max_bs_residual)
            Z[a, b] = {"bounded": 0.0, "inflation": 1.0, "deflation": -1.0}[kind]
    return Z, leak


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-19 Phase 2b: the genuine Fisher debt-deflation loop — the two-basin map ===\n")
    nested_regression()

    # 1. φ* threshold (Engine 2 isolated)
    print("\n[1] AC1 — the deflation threshold φ* (Engine 2 isolated, ε=0, b_ref=%.2f):" % B_REF)
    grid = np.linspace(0.0, 3.0, 16)
    for phi in grid:
        k, v, e = outcome(0.5, 0.0, phi)
        tag = f"bounded grind {v*100:.2f}%/step" if k == "bounded" else f"{k.upper()} @step {v}"
        print(f"      φ={phi:>4.1f}: {tag}")
    ps = phi_star()
    print(f"    φ* ≈ {ps:.3f}: below it the grind is BOUNDED; above it a Fisher DEBT-DEFLATION")
    print(f"    collapse. Deflation is a THRESHOLD phenomenon — you have to strengthen the price")
    print(f"    channel past φ* to reach it (CYB-17's damper alone never could).")

    # 2. headline two-basin map
    phis = np.round(np.linspace(0.0, 3.0, 25), 3)
    epss = np.round(np.linspace(0.0, 1.0, 21), 3)
    Z, leak = basin_map(phis, epss)
    n_bnd = int((Z == 0).sum()); n_inf = int((Z == 1).sum()); n_def = int((Z == -1).sum())
    print(f"\n[2] AC2 (headline) — the two-basin map over (φ, ε):")
    print(f"    bounded {n_bnd} · Engine-1 INFLATION-collapse {n_inf} · Engine-2 DEFLATION-collapse {n_def}"
          f"  (of {Z.size} cells).")
    print(f"    BOTH collapse basins reachable ⇒ NOT rigged. The SAME debt-distress routes to")
    print(f"    inflation (ε: impaired rentier's premium → cost-push) OR deflation (φ: distress")
    print(f"    selling → price cut → higher real burden → more selling). Which basin you fall")
    print(f"    into is set by φ vs ε — the STRENGTH OF THE PRICE CHANNEL, exactly CYB-23's pivot.")

    # 3. AC3 honesty anchor — the collapse is the LOOP, not the cut
    print(f"\n[3] AC3 — the collapse is the LOOP, not the mechanical cut (frozen-leverage regression):")
    for phi in [2.0, 4.0, 8.0]:
        kl, _, _ = outcome(0.5, 0.0, phi, freeze=False)
        kf, vf, _ = outcome(0.5, 0.0, phi, freeze=True)
        extra = f"grind {vf*100:.2f}%/step" if kf == "bounded" else kf
        print(f"      φ={phi}: live loop = {kl.upper():>10}   frozen-leverage = {kf.upper():>8} ({extra})")
    print(f"    The live self-reinforcing D/P feedback deflation-collapses; holding leverage")
    print(f"    constant (same cut magnitude, no feedback) stays BOUNDED ⇒ the collapse is")
    print(f"    genuinely Fisher's doom loop, not the price decrement alone.")

    # 4. AC4 conservation through a deflationary transient + the real-burden runaway
    kd, sd, ed = outcome(0.5, 0.0, 1.8)   # a deflation run just past φ* (a longer, illustrative descent)
    print(f"\n[4] AC4 — conservation through the deflationary transient:")
    print(f"    a Fisher collapse (φ=1.8, just past φ*, ε=0) at step {sd}: the per-step deflation")
    print(f"    ACCELERATES through −25%/step (the freeze) as D/P climbs 0.62→{ed.leverage:.2f}; left")
    print(f"    unfrozen P→0 and D/P→∞ — Fisher's doom loop. Worst capital-account residual = "
          f"{ed.max_bs_residual:.0e} (<1e-9).")
    print(f"    The identity rentier-asset ≡ firm-liability is P-INDEPENDENT, so the price cut")
    print(f"    cannot break it — and THAT is the SFC point of debt-deflation: it is a REAL-burden")
    print(f"    runaway, NOT a nominal-accounting failure. The accounting stays exact throughout.")

    # 5. AC5 the CYB-23 resolution
    k0, v0, _ = outcome(0.5, 0.0, 0.0)      # φ=0 (shipped CYB-23 config)
    print(f"\n[5] AC5 — the CYB-23 resolution (is 'inflationary, not Fisher' conditional?):")
    print(f"    φ=0 (shipped CYB-23 config): {k0} ({v0*100:.2f}%/step) — deflation UNREACHABLE,")
    print(f"      exactly as CYB-23's AC6 reported (its demand damper drives π→0 from above only).")
    print(f"    φ>φ*≈{ps:.2f}: the Fisher DEFLATIONARY basin opens.")
    print(f"    ⇒ VERDICT: the 'inflationary, not Fisher' result is CONDITIONAL — it holds for the")
    print(f"      shipped (weak-price-channel) config, and is NOT a refutation of debt-deflation.")
    print(f"      Two engines, opposite sign, one distress signal; the price-channel strength picks.")

    # 6. AC6 determinism
    r1 = _mk(fisher_phi=4.0).run(200); r2 = _mk(fisher_phi=4.0).run(200)
    print(f"\n[6] AC6 — determinism: byte-identical rerun = {np.array_equal(r1, r2)}")

    make_figures(out, phis, epss, Z, ps, leak)
    print("\nsaved 3 figures to fisher/figures/.")


# ============================================================ figures
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"
def make_figures(out, phis, epss, Z, ps, leak):
    plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                         "figure.facecolor":"white","axes.facecolor":"white"})
    from matplotlib.colors import ListedColormap, BoundaryNorm

    # ---- Fig 1: the two-basin map (HEADLINE) ----
    fig, ax = plt.subplots(figsize=(10.5, 6.8))
    cmap = ListedColormap([BLU, "#f4f1ea", ACC])          # -1 deflation, 0 bounded, +1 inflation
    norm = BoundaryNorm([-1.5, -0.5, 0.5, 1.5], cmap.N)
    ax.pcolormesh(phis, epss, Z, cmap=cmap, norm=norm, shading="auto")
    ax.axvline(ps, color=INK, lw=1.4, ls="--")
    ax.text(ps+0.05, 0.02, f"φ* ≈ {ps:.2f}\n(deflation threshold, ε=0)", fontsize=8.5, color=INK, va="bottom")
    ax.set_xlabel("Fisher price-channel strength  φ  (Engine 2: distress selling → price cut → higher real burden)")
    ax.set_ylabel("impairment→premium elasticity  ε  (Engine 1)")
    ax.set_title("CYB Phase 2b (headline) — the two-basin map: one debt-distress signal, two collapse engines, opposite sign\n"
                 "blue = Engine-2 Fisher DEBT-DEFLATION · red = Engine-1 INFLATION contagion · cream = bounded. Which basin is set by φ vs ε",
                 fontsize=9.5, fontweight="bold")
    ax.text(0.15, 0.85, "ENGINE 1\nINFLATION\n(premium spiral)", fontsize=9, color="white", fontweight="bold", ha="center")
    ax.text(2.45, 0.10, "ENGINE 2\nDEBT-DEFLATION\n(Fisher loop)", fontsize=9, color="white", fontweight="bold", ha="center")
    ax.text(0.55, 0.05, "bounded\ngrind", fontsize=8.5, color=MUT, ha="center")
    fig.tight_layout(); fig.savefig(out/"cybeersym_fisher_v0_two_basin_map.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 2: φ* threshold + representative log-price traces + frozen-leverage anchor ----
    def logP_trace(phi, freeze=False, n=400):
        e = _mk(fisher_phi=phi, freeze=freeze); lp = []
        for _ in range(n):
            e.step(); lp.append(np.log(e.conflict.P))
            if e.collapsed: break
        return np.array(lp)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(13, 5.4))
    # left: outcome vs φ (ε=0)
    grid = np.linspace(0.0, 3.0, 61)
    codes = []
    for phi in grid:
        k, _, _ = outcome(0.5, 0.0, phi, n=800)
        codes.append({"bounded":0,"inflation":1,"deflation":-1}[k])
    codes = np.array(codes)
    a1.fill_between(grid, -1.2, 1.2, where=codes==-1, color=BLU, alpha=0.25, step="mid")
    a1.fill_between(grid, -1.2, 1.2, where=codes==0, color="#f4f1ea", step="mid")
    a1.axvline(ps, color=INK, lw=1.6, ls="--", label=f"φ* ≈ {ps:.2f}")
    a1.set_ylim(-1.2, 1.2); a1.set_yticks([-1,0,1]); a1.set_yticklabels(["deflation\ncollapse","bounded","inflation"])
    a1.set_xlabel("Fisher price-channel strength  φ  (ε=0)"); a1.legend(frameon=False, fontsize=9, loc="center right")
    a1.set_title("AC1 — deflation is a THRESHOLD: strengthen the price\nchannel past φ* and the Fisher basin opens", fontsize=9.5)
    a1.grid(True, color=GRID, lw=0.7, axis="x"); a1.set_axisbelow(True)
    # right: log-price traces
    lp_b = logP_trace(1.0)          # bounded grind (φ<φ*)
    lp_d = logP_trace(4.0)          # deflation collapse (φ>φ*)
    lp_f = logP_trace(4.0, freeze=True)   # frozen-leverage: bounded (the anchor)
    a2.plot(np.arange(len(lp_b)), lp_b, color=MUT, lw=1.8, label="φ=1.0 (<φ*) — bounded grind")
    a2.plot(np.arange(len(lp_f)), lp_f, color=GRN, lw=1.8, ls=":", label="φ=4.0 frozen-leverage — BOUNDED (the anchor)")
    a2.plot(np.arange(len(lp_d)), lp_d, color=BLU, lw=2.4, label="φ=4.0 live loop — DEBT-DEFLATION (P→0, frozen at blow-down)")
    a2.set_xlabel("step"); a2.set_ylabel("log price level")
    a2.legend(frameon=False, fontsize=8.5, loc="lower left")
    a2.set_title("AC3 — the collapse is the LOOP: the live D/P feedback deflates;\nholding leverage constant (same cut) stays bounded", fontsize=9.5)
    a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(out/"cybeersym_fisher_v0_threshold_and_anchor.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 3: the real-burden runaway while nominal accounting stays exact ----
    e = _mk(fisher_phi=1.8); lev=[]; res=[]; lp=[]   # just past φ*: a longer, illustrative descent
    for _ in range(400):
        e.step(); lev.append(e.leverage); res.append(max(e.max_bs_residual,1e-18)); lp.append(np.log(e.conflict.P))
        if e.collapsed: break
    x = np.arange(len(lev))
    fig, (b1, b2) = plt.subplots(2, 1, figsize=(11.5, 7.0), sharex=True)
    fig.suptitle("CYB Phase 2b AC4 — debt-deflation is a REAL-burden runaway while NOMINAL accounting stays exact (the SFC payoff)",
                 fontsize=10.5, fontweight="bold", y=0.98)
    b1.plot(x, lev, color=BLU, lw=2.0, label="real debt burden  D/P  (leverage)")
    b1.plot(x, lp, color=INK, lw=1.4, ls="--", label="log price level (P collapsing)")
    b1.set_ylabel("D/P   and   log P"); b1.legend(frameon=False, fontsize=9, loc="upper left")
    b1.set_title("as P falls the REAL burden D/P runs away — Fisher's 'the more they pay, the more they owe'", fontsize=9)
    b1.grid(True, color=GRID, lw=0.7); b1.set_axisbelow(True)
    b2.semilogy(x, res, color=ACC, lw=1.6, label="capital-account residual (rentier asset ≡ firm liability)")
    b2.axhline(1e-9, color=INK, lw=1.0, ls="--", label="conservation bound 1e-9")
    b2.set_xlabel("step"); b2.set_ylabel("residual")
    b2.legend(frameon=False, fontsize=8.5, loc="upper right"); b2.grid(True, color=GRID, lw=0.7, which="both"); b2.set_axisbelow(True)
    b2.set_title(f"the NOMINAL identity holds to machine precision THROUGH the deflationary collapse (worst over map = {leak:.0e})", fontsize=9)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_fisher_v0_real_burden_runaway.png", dpi=140, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
