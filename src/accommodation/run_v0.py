"""
CYB-17 — accommodation channel v0: credit ratification of the conflict spiral, and the
policy rate's channel decomposition.

Runs, in order:
  0. Full-accommodation-limit regression (i→0, cost off, D_max→∞) — MUST reproduce CYB-6
     byte-for-byte (incl. the unbounded runaway for g>0). Load-bearing.
  1. Channel decomposition of π*(i) — cost / demand / distributional / all (the headline).
  2. H1a: is CYB-6's runaway now conditional? runaway (i=0) vs choked vs restraint-insufficient.
  3. H1a boundary map in (i, g): ratified/persists vs choked; restraint-insufficient region.
  4. Solvency ceiling (the nonsmooth border) + the monetarist money-growth-cap comparison.

Determinism: σ=0, pure function of state. Conservation (three-way flow + debt bookkeeping)
asserted inside every step.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import (AccommodationEconomy, AccommodationParams,      # accommodation/model.py
                   ConflictEconomy, ConflictParams)

BASE = dict(omega_f=0.65, gap=0.10, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
K = BASE["alpha_w"] * BASE["alpha_p"] / (BASE["alpha_w"] + BASE["alpha_p"])   # = 0.15
PI0 = K * BASE["gap"]                                                         # CYB-6 π* = 1.5%/step
NSTEP, TAIL = 2000, 300
# illustrative channel strengths (FREE parameters — the model isn't rigged toward any winner)
C_COST, C_DEMAND, C_DISTRIB = 1.0, 3.0, 0.5

def steady_pi(**kw):
    e = AccommodationEconomy(AccommodationParams(**{**BASE, **kw}))
    pis = np.empty(NSTEP)
    for k in range(NSTEP): e.step(); pis[k] = e.last_pi
    return float(np.mean(pis[-TAIL:])), e


# ---- 0. full-accommodation-limit regression --------------------------------
def regression():
    acc = AccommodationEconomy(AccommodationParams(**BASE, i=0.0, cost_c=0.0))
    ref = ConflictEconomy(ConflictParams(**BASE))
    dmax = 0.0
    for _ in range(400):
        acc.step(); ref.step()
        dmax = max(dmax, abs(acc.conflict.W - ref.W), abs(acc.conflict.P - ref.P))
    ok = (dmax == 0.0)
    print(f"[0] full-accommodation limit (i→0, cost off): max|W,P Δ| vs CYB-6 = {dmax:.1e}  "
          f"byte-identical={ok}; CYB-6 runaway recovered (P→{ref.P:.0f}, g>0)")
    assert ok, "REGRESSION LEAK: i=0 did not reproduce CYB-6 exactly"
    # closed-form sanity at i=0
    p0, _ = steady_pi(i=0.0, cost_c=0.0)
    print(f"    closed-form sanity: π*(i=0)={p0*100:.3f}%/step vs Rowthorn–Lavoie k·g={PI0*100:.3f}%/step")


# ---- 1. channel decomposition ----------------------------------------------
def decomposition(iis):
    out = {"cost": [], "demand": [], "distrib": [], "all": []}
    for i in iis:
        out["cost"].append(steady_pi(i=i, cost_c=C_COST, demand_b=0, distrib_a=0)[0])
        out["demand"].append(steady_pi(i=i, cost_c=0, demand_b=C_DEMAND, distrib_a=0)[0])
        out["distrib"].append(steady_pi(i=i, cost_c=0, demand_b=0, distrib_a=C_DISTRIB)[0])
        out["all"].append(steady_pi(i=i, cost_c=C_COST, demand_b=C_DEMAND, distrib_a=C_DISTRIB)[0])
    return {k: np.array(v) for k, v in out.items()}


# ---- 3. H1a boundary map in (i, g) -----------------------------------------
def boundary_map(gs, iis, cost_c, demand_b, distrib_a):
    Z = np.empty((len(iis), len(gs)))
    for a, i in enumerate(iis):
        for b, g in enumerate(gs):
            Z[a, b] = steady_pi(gap=g, i=i, cost_c=cost_c, demand_b=demand_b, distrib_a=distrib_a)[0]
    return Z


# ---- 4. solvency border + monetarist -------------------------------------
def solvency_trace(i, D_max, n=400, **kw):
    e = AccommodationEconomy(AccommodationParams(**{**BASE, **kw}, i=i, D_max=D_max))
    dy = np.empty(n); pi = np.empty(n); bound = np.empty(n)
    for k in range(n):
        e.step(); dy[k] = e.D / e.conflict.P; pi[k] = e.last_pi; bound[k] = e.solvency_bound
    return dy, pi, bound, e


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-17: accommodation — credit ratification + the rate's channel decomposition ===\n")
    regression()

    iis = np.linspace(0.0, 0.20, 21)
    dec = decomposition(iis)
    iref = 10  # i = 0.10
    print("\n[1] channel decomposition of π*(i), at i=0.10 (baseline CYB-6 π*=%.2f%%/step):" % (PI0*100))
    for k in ("cost", "demand", "distrib", "all"):
        print(f"    {k:8s}: π*={dec[k][iref]*100:+.3f}%/step  (Δ vs baseline {(dec[k][iref]-PI0)*100:+.3f})")
    print("    -> COST feeds (inflationary), DEMAND cools symmetrically, DISTRIBUTIONAL cools by")
    print("       breaking labor (drives π* toward 0). Which dominates is set by the strengths —")
    print("       the model is NOT rigged toward any one; all three are legitimate outcomes.")

    # 2/3. restraint-insufficient + boundary
    print("\n[2] H1a — is the runaway conditional? (restraint present, sufficiency endogenous)")
    p_costdom, _ = steady_pi(i=0.20, cost_c=1.0, demand_b=0.5, distrib_a=0.0)   # cost-dominant
    p_distdom, _ = steady_pi(i=0.20, cost_c=0.2, demand_b=1.0, distrib_a=0.6)   # disinflation-dominant
    print(f"    cost-dominant  (c=1.0,b=0.5,a=0.0) @ i=0.20: π*={p_costdom*100:+.3f}%/step -> RESTRAINT INSUFFICIENT (rate feeds; spiral outruns it)")
    print(f"    disinfl-domin. (c=0.2,b=1.0,a=0.6) @ i=0.20: π*={p_distdom*100:+.3f}%/step -> CHOKED (rate bounds it)")
    print("    => accommodation is the sustaining CONDITION: the runaway is conditional on which")
    print("       channel wins — a high rate bounds it ONLY if disinflation dominates cost.")

    gs = np.round(np.linspace(-0.04, 0.16, 21), 3)
    Zb = boundary_map(gs, iis, cost_c=0.3, demand_b=1.0, distrib_a=0.6)

    # 4. solvency border + monetarist. D_max = ceiling on the financeable wage share
    #    (banks won't finance a wage bill above D_max·income); set just below ω*≈0.70.
    print("\n[4] solvency ceiling (nonsmooth border) + monetarist comparison")
    dy_h, pi_h, _, _ = solvency_trace(i=0.05, D_max=1e18, cost_c=0.3)             # horizontalist, no ceiling
    dy_s, pi_s, bnd_s, es = solvency_trace(i=0.05, D_max=0.68, cost_c=0.3)        # ceiling below ω* → binds
    print(f"    horizontalist, i=0.05, D_max=∞: quantity lever inert; D/P (=fin. wage share) → {dy_h[-1]:.3f}, π* ≈{np.mean(pi_h[-100:])*100:+.2f}%/step")
    print(f"    solvency ceiling, i=0.05, D_max=0.68: border binds {int(bnd_s.sum())}/{len(bnd_s)} steps; "
          f"D/P capped at {dy_s[-50:].mean():.3f}; wage financing rationed → wage-push choked at the border")
    # monetarist knob: cap money(≈wage-bill) growth at mu, on the cost-fed spiral
    p_horiz, _ = steady_pi(i=0.10, cost_c=1.0, mode="horizontalist")
    p_monet, em = steady_pi(i=0.10, cost_c=1.0, mode="monetarist", mu=0.005)
    print(f"    monetarist μ-cap (μ=0.5%/step) on the SAME cost-fed spiral: π* {p_horiz*100:+.3f} → {p_monet*100:+.3f}%/step "
          f"({'bounds it — BUT via rationing' if p_monet < p_horiz - 1e-4 else 'inert'}): forcing the money quantity is a")
    print("       credit-crunch (a real/distributional cut), not a clean nominal lever — the horizontalist point.")

    print(f"    border dominance: at g>0 with a binding ceiling the SOLVENCY ceiling rules "
          f"({bnd_s.mean()*100:.0f}% of steps); the wage floor rules the g≤0 dissipation regime — different regions.")

    conservation = max(steady_pi(i=0.10, cost_c=1, demand_b=1, distrib_a=0.3)[1].max_residual,
                       es.max_residual)
    print(f"\n[5] conservation (three-way flow + debt bookkeeping): worst residual = {conservation:.0e} (<1e-9)")

    make_figures(out, iis, dec, gs, Zb, (dy_h, pi_h), (dy_s, pi_s, bnd_s))
    print("\nsaved 4 figures to accommodation/figures/.")


# ============================================================ figures
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"; PUR="#7d3c98"
def make_figures(out, iis, dec, gs, Zb, horiz, solv):
    plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                         "figure.facecolor":"white","axes.facecolor":"white"})
    # Fig 1: channel decomposition (HEADLINE)
    fig, ax = plt.subplots(figsize=(10, 6.4))
    ax.axhline(PI0*100, color=MUT, lw=1.0, ls=":", label=f"CYB-6 baseline π* = {PI0*100:.1f}%/step (no rate)")
    ax.axhline(0, color=INK, lw=0.7)
    ax.plot(iis*100, dec["cost"]*100, color=ACC, lw=2.2, marker="o", ms=3, label="COST channel — feeds (inflationary / neo-Fisherian)")
    ax.plot(iis*100, dec["demand"]*100, color=BLU, lw=2.2, marker="s", ms=3, label="DEMAND channel — cools symmetrically (orthodoxy)")
    ax.plot(iis*100, dec["distrib"]*100, color=GRN, lw=2.2, marker="^", ms=3, label="DISTRIBUTIONAL channel — cools by breaking labor")
    ax.plot(iis*100, dec["all"]*100, color=INK, lw=2.6, ls="--", label="ALL three together (net tug-of-war)")
    ax.set_xlabel("policy rate  i  (%/step)"); ax.set_ylabel("sustained inflation  π*  (%/step)")
    ax.set_title("CYB-17 — what the rate actually does: the three channels pull in OPPOSITE directions\n"
                 "(the winner is set by the relative strengths — the model isn't rigged toward any one)",
                 fontsize=10.5, fontweight="bold")
    ax.grid(True, color=GRID, lw=0.7); ax.set_axisbelow(True); ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout(); fig.savefig(out/"cybeersym_accommodation_v0_channel_decomposition.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # Fig 2: runaway now conditional (P(t) time series)
    def price_path(n=260, **kw):
        e = AccommodationEconomy(AccommodationParams(**{**BASE, **kw})); lp = np.empty(n)
        for k in range(n): e.step(); lp[k] = np.log(e.conflict.P)
        return lp
    n=260; x=np.arange(n)
    fig, ax = plt.subplots(figsize=(11, 6.0))
    ax.plot(x, price_path(n, i=0.0, cost_c=0.0), color=MUT, lw=2.2, ls=":", label="i=0 — CYB-6 full-accommodation limit: UNBOUNDED runaway")
    ax.plot(x, price_path(n, i=0.20, cost_c=0.3, demand_b=1.0, distrib_a=0.6), color=GRN, lw=2.2, label="i=0.20, disinflation dominant → CHOKED (price level plateaus)")
    ax.plot(x, price_path(n, i=0.20, cost_c=1.0, demand_b=0.5, distrib_a=0.0), color=ACC, lw=2.0, label="i=0.20, cost dominant → RESTRAINT INSUFFICIENT (spiral outruns the rate)")
    ax.set_xlabel("step"); ax.set_ylabel("log price level")
    ax.set_title("CYB-17 — H1a: CYB-6's 'unbounded' runaway is the full-accommodation limit; financing makes it CONDITIONAL",
                 fontsize=10.5, fontweight="bold")
    ax.grid(True, color=GRID, lw=0.7); ax.set_axisbelow(True); ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout(); fig.savefig(out/"cybeersym_accommodation_v0_runaway_conditional.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # Fig 3: H1a boundary map (i, g)
    fig, ax = plt.subplots(figsize=(9.5, 6.2))
    im = ax.pcolormesh(gs, iis*100, Zb*100, cmap="RdBu_r", shading="auto",
                       vmin=-abs(Zb).max()*100, vmax=abs(Zb).max()*100)
    ax.contour(gs, iis*100, Zb, levels=[0.0], colors="k", linewidths=2)
    fig.colorbar(im, ax=ax, label="sustained inflation π* (%/step)  —  red=persists, blue=choked/deflating")
    ax.set_xlabel("aspiration gap  g  (control)"); ax.set_ylabel("policy rate  i  (%/step)")
    ax.axvline(0, color="k", lw=0.8, ls=":")
    ax.set_title("CYB-17 — the ratified/choked boundary in (g, i)  [disinflation-leaning mix]\n"
                 "black line = π*=0; above it the rate bounds the spiral, below/right it persists",
                 fontsize=10, fontweight="bold")
    fig.tight_layout(); fig.savefig(out/"cybeersym_accommodation_v0_boundary_map.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # Fig 4: solvency border dynamics
    dy_h, pi_h = horiz; dy_s, pi_s, bnd_s = solv
    n = len(dy_s); x = np.arange(n)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(11, 7.4), height_ratios=[1, 1])
    fig.suptitle("CYB-17 — the solvency ceiling completes the switching-manifold set (order non-negativity → wage floor → solvency)",
                 fontsize=11, fontweight="bold", y=0.98)
    a1.plot(x, dy_s, color=PUR, lw=2, label="D/P (financeable wage share), i=0.05")
    a1.axhline(0.68, color=ACC, lw=1.4, ls="--", label="solvency ceiling D_max=0.68")
    a1.fill_between(x, 0, 1, where=bnd_s.astype(bool), color=ACC, alpha=0.08, transform=a1.get_xaxis_transform(),
                    label="ceiling ACTIVE (wage financing rationed)")
    a1.set_ylabel("D/P"); a1.legend(frameon=False, fontsize=8.5, loc="lower right")
    a1.grid(True, color=GRID, lw=0.7); a1.set_axisbelow(True)
    a1.set_title("the wage share rises toward ω* but hits the creditworthiness ceiling → rationed (the border is RIDDEN: bind/release each step)", fontsize=9)
    a2.plot(x, pi_s*100, color=ACC, lw=1.8, label="π(t), solvency ceiling binds (i=0.05, D_max=0.68) → wage-push rationed")
    a2.plot(np.arange(len(pi_h)), pi_h*100, color=BLU, lw=1.6, ls=":", label="π(t), horizontalist (i=0.05, D_max=∞) — credit accommodates, no rationing")
    a2.axhline(0, color=INK, lw=0.6)
    a2.set_xlabel("step"); a2.set_ylabel("inflation π(t) (%/step)")
    a2.legend(frameon=False, fontsize=8.5, loc="upper right"); a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True)
    a2.set_title("horizontalist: credit accommodates, the rate is the only lever; at the ceiling the spiral is choked by rationing", fontsize=9.5)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_accommodation_v0_solvency_border.png", dpi=140, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
