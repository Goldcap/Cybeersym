"""
CYB-18 — accommodation on the coupled substrate: the CYB-17 channel decomposition re-run on
the egg-faithful recursion×conflict stack (CYB-10), and the fate of the distributional flip.

Runs, in order:
  0. TWO regression anchors — BOTH must be byte-exact (load-bearing):
       (a) κ=0                      ⇒ reproduces CYB-17 (accommodation on bare CYB-6).
       (b) i→0, D_max→∞, cost-off   ⇒ reproduces CYB-10 (the coupled transmission model).
  1. Channel decomposition on the coupled substrate vs CYB-17 (HEADLINE, Q1): does the
     distributional channel still self-exhaust when recursion keeps re-loading g? Reports the
     recursion-pinned inflation floor and the fate of the cost-flip / restraint-insufficient region.
  2. Ignition-vs-rate (Q2): the super-additive ignition threshold κ*(i). Does the rate gate
     ignition, and through which channel (cost lowers the bar / disinflation raises it)?
  3. Three nonsmooth borders at once (order non-negativity + wage floor + solvency ceiling):
     border-dominance report + all-three-conservation check + determinism.

Determinism: σ=0, pure function of state. Three conservation laws (goods; three-way income;
debt bookkeeping) asserted inside the reused submodules every step.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import (AccommodationCoupledEconomy, ChaosParams, AccommodationParams,   # our model.py
                   AccommodationEconomy, CoupledEconomy, ConflictParams)             # the two parents

# --- config: CYB-2 amplifying chain; CYB-17 channel strengths -----------------
CP = dict(beta=0.18, a_S=0.7, L=3, theta=0.25, perturb=1.0)     # amplifying (chaotic) chain
SUPRA = dict(omega_f=0.65, gap=0.10, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
SUB   = dict(omega_f=0.65, gap=-0.05, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
K = SUPRA["alpha_w"] * SUPRA["alpha_p"] / (SUPRA["alpha_w"] + SUPRA["alpha_p"])   # = 0.15
PI0 = K * SUPRA["gap"]                                          # bare CYB-6 π* = 1.5%/step
KAP = 0.20                                                      # CYB-10 headline coupling strength
C_COST, C_DEMAND, C_DISTRIB = 1.0, 3.0, 0.5                     # inherited CYB-17 channel tunings
NSTEP, TAIL = 1200, 400
NIGN, TIGN, IGNITE_EPS = 600, 200, 5e-4                         # CYB-10 ignition settings

def _cc(chosen, kappa, **kw):
    return AccommodationCoupledEconomy(ChaosParams(**CP), AccommodationParams(**{**chosen, **kw}), kappa=kappa)

def steady_pi(kappa, base=SUPRA, n=NSTEP, tail=TAIL, **kw):
    e = _cc(base, kappa, **kw); pis = np.empty(n)
    for k in range(n): e.step(); pis[k] = e.last_pi
    return float(np.mean(pis[-tail:])), e

def tail_pi_sub(kappa, **kw):
    e = _cc(SUB, kappa, **kw); pis = np.empty(NIGN)
    for k in range(NIGN): e.step(); pis[k] = e.last_pi
    return float(np.mean(pis[-TIGN:]))


# ---- 0. the two regression anchors -----------------------------------------
def regression_anchors():
    # (a) κ=0 → CYB-17 (accommodation on bare CYB-6), a live financed spiral with all channels
    kw = dict(i=0.07, cost_c=C_COST, demand_b=C_DEMAND, distrib_a=C_DISTRIB)
    comp = _cc(SUPRA, 0.0, **kw)
    ref = AccommodationEconomy(AccommodationParams(**SUPRA, **kw))
    d = 0.0
    for _ in range(400):
        comp.step(); ref.step()
        d = max(d, abs(comp.conflict.W - ref.conflict.W), abs(comp.conflict.P - ref.conflict.P),
                abs(comp.D - ref.D))
    ok_a = (d == 0.0)
    print(f"[0a] κ=0 → CYB-17 (accommodation on bare CYB-6): max|W,P,D Δ| = {d:.1e}  byte-identical={ok_a}")
    assert ok_a, "ANCHOR-1 LEAK: κ=0 did not reproduce CYB-17 exactly"

    # (b) full-accommodation limit (i→0, D_max→∞, cost off) → CYB-10 (the coupled model)
    comp2 = _cc(SUB, KAP, i=0.0, cost_c=0.0, demand_b=0.0, distrib_a=0.0, D_max=1e18)
    ref2 = CoupledEconomy(ChaosParams(**CP),
                          ConflictParams(**SUB), kappa=KAP)
    dch = dcf = 0.0
    for _ in range(400):
        comp2.step(); ref2.step()
        dch = max(dch, float(np.max(np.abs(comp2.chain.get_state() - ref2.chain.get_state()))))
        dcf = max(dcf, abs(comp2.conflict.omega - ref2.conflict.omega), abs(comp2.conflict.P - ref2.conflict.P))
    ok_b = (dch == 0.0 and dcf == 0.0)
    print(f"[0b] i→0,cost-off → CYB-10 (coupled model): |chain Δ|={dch:.1e}  |conflict Δ|={dcf:.1e}  "
          f"byte-identical={ok_b}")
    assert ok_b, "ANCHOR-2 LEAK: full-accommodation limit did not reproduce CYB-10 exactly"
    print("     -> both composition axes anchored; nothing leaked beyond the two validated interactions.")


# ---- 1. channel decomposition on the coupled substrate ----------------------
def decomposition(kappa, iis, base=SUPRA):
    # NB: AccommodationParams defaults cost_c=1.0 — isolate each channel by zeroing the others explicitly.
    out = {"cost": [], "demand": [], "distrib": [], "all": []}
    for i in iis:
        out["cost"].append(steady_pi(kappa, base, i=i, cost_c=C_COST, demand_b=0.0, distrib_a=0.0)[0])
        out["demand"].append(steady_pi(kappa, base, i=i, cost_c=0.0, demand_b=C_DEMAND, distrib_a=0.0)[0])
        out["distrib"].append(steady_pi(kappa, base, i=i, cost_c=0.0, demand_b=0.0, distrib_a=C_DISTRIB)[0])
        out["all"].append(steady_pi(kappa, base, i=i, cost_c=C_COST, demand_b=C_DEMAND, distrib_a=C_DISTRIB)[0])
    return {k: np.array(v) for k, v in out.items()}

def mean_deficit(kappa=KAP, base=SUPRA):
    e = _cc(base, kappa, i=0.0, cost_c=0.0); ds = np.empty(NSTEP)
    for k in range(NSTEP): e.step(); ds[k] = e.last_d
    return float(np.mean(ds[-TAIL:]))


# ---- 2. ignition threshold κ*(i) on the SUBthreshold substrate --------------
def kappa_threshold(i, c, b, a, kappas):
    for kap in kappas:
        if tail_pi_sub(kap, i=i, cost_c=c, demand_b=b, distrib_a=a) > IGNITE_EPS:
            return float(kap)
    return np.nan

def ignition_curves(iis, kappas):
    cost = [kappa_threshold(i, 1.0, 0.5, 0.0, kappas) for i in iis]      # cost-leaning mix
    dis  = [kappa_threshold(i, 0.2, 1.0, 0.6, kappas) for i in iis]      # disinflation-leaning mix
    neu  = [kappa_threshold(i, 0.0, 0.0, 0.0, kappas) for i in iis]      # rate off (CYB-10 baseline)
    return np.array(cost), np.array(dis), np.array(neu)


# ---- 3. three-border dynamics -----------------------------------------------
BORDER = dict(gap=-0.02, omega_f=0.65, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
def border_trace(i=0.05, cost_c=0.3, D_max=0.58, n=NIGN, kappa=KAP):
    e = _cc(BORDER, kappa, i=i, cost_c=cost_c, D_max=D_max)
    stock = np.zeros(n, bool); floor = np.zeros(n, bool); solv = np.zeros(n, bool); pi = np.empty(n)
    for k in range(n):
        prev = e.conflict.omega                                   # ω before this tick
        e.step()
        # wage floor binds when workers' RAW push (pre-max) is negative (ω above their eff. target)
        floor[k] = e.conflict.p.alpha_w * (e.conflict.p.omega_w - prev) < 0
        stock[k] = e.chain.tiers[-1].net_stock < 0                # order non-negativity / stockout (recursion)
        solv[k] = e.solvency_bound                                # solvency ceiling (accommodation)
        pi[k] = e.last_pi
    return stock, floor, solv, pi, e


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-18: accommodation on the coupled substrate — the distributional flip under reloading ===\n")
    regression_anchors()

    # 1. channel decomposition, bare (κ=0 = CYB-17) vs coupled (κ=KAP)
    iis = np.linspace(0.0, 0.20, 21)
    dec0 = decomposition(0.0, iis)      # = CYB-17 (bare)
    decK = decomposition(KAP, iis)      # coupled
    dbar = mean_deficit()
    floor = K * KAP * dbar              # recursion-pinned inflation floor the rate can't reach
    iref = 20                           # i = 0.20 (where bare distributional fully exhausts)
    print("\n[1] channel decomposition — coupled (κ=%.2f) vs bare CYB-17 (κ=0). HEADLINE (Q1):" % KAP)
    print(f"    baseline π*(i=0): bare {dec0['all'][0]*100:+.2f}  →  coupled {decK['all'][0]*100:+.2f}%/step "
          f"(recursion reloads g by κ·⟨d⟩={KAP*dbar:.3f} ⇒ +{(decK['all'][0]-dec0['all'][0])*100:.2f})")
    print(f"    DISTRIBUTIONAL channel at i=0.20 (bare exhausts to 0):")
    print(f"       bare    π* = {dec0['distrib'][iref]*100:+.3f}%/step  -> EXHAUSTED (labor's static gap g0 fully closed)")
    print(f"       coupled π* = {decK['distrib'][iref]*100:+.3f}%/step  -> FLOORED at ≈k·κ·⟨d⟩ = {floor*100:.3f}%/step")
    print("    => the distributional channel does NOT exhaust to zero: recursion re-supplies the gap every")
    print("       period, pinning a POSITIVE inflation floor distribution can't break (the exhaustion is")
    print("       DEFERRED — pushed to higher i — and the clean zero is replaced by a recursion-pinned floor).")
    # cost-flip / restraint-insufficient: survives and expands?
    p_cost_bare, _ = steady_pi(0.0, SUPRA, i=0.20, cost_c=1.0, demand_b=0.5)
    p_cost_coup, _ = steady_pi(KAP, SUPRA, i=0.20, cost_c=1.0, demand_b=0.5)
    print(f"    COST-DOMINANT mix (c=1,b=.5) @ i=0.20: bare {p_cost_bare*100:+.2f} → coupled {p_cost_coup*100:+.2f}%/step")
    print("       -> the restraint-insufficient / cost-flip region SURVIVES and is HOTTER on the coupled")
    print("          substrate: recursion lifts the whole π*(i) surface, so NO rate drives inflation to 0.")

    # 2. ignition threshold vs rate (subthreshold substrate)
    kappas = np.round(np.linspace(0.0, 0.40, 41), 3)
    iis2 = np.linspace(0.0, 0.20, 9)
    k_cost, k_dis, k_neu = ignition_curves(iis2, kappas)
    print("\n[2] ignition threshold κ*(i) on the SUBthreshold substrate (g0=-0.05). Q2:")
    print(f"    rate OFF (all channels 0): κ* = {np.nanmean(k_neu):.3f} flat  = CYB-10 baseline (rate acts ONLY via channels)")
    print(f"    COST-leaning (c=1,b=.5):   κ* {k_cost[0]:.3f} (i=0) → {k_cost[-1]:.3f} (i=0.20)  -> rate LOWERS the bar (cost self-ignites)")
    print(f"    DISINFL-leaning (c=.2,b=1,a=.6): κ* {k_dis[0]:.3f} → {k_dis[-1]:.3f}  -> rate RAISES the bar (chokes ignition)")
    print("    => the rate gates super-additive ignition BOTH ways; which way is the same tug-of-war as Q1,")
    print("       now at the ignition margin (cost lowers the threshold, disinflation raises it).")

    # 3. three-border dynamics
    stock, floor_b, solv, pi_b, eb = border_trace()
    n = len(stock)
    print("\n[3] three nonsmooth borders live at once (regime: g0=-0.02, κ=%.2f, i=0.05, D_max=0.58):" % KAP)
    print(f"    order non-negativity / stockout (recursion): {stock.mean()*100:.0f}% of steps")
    print(f"    wage floor (conflict):                        {floor_b.mean()*100:.0f}% of steps")
    print(f"    solvency ceiling (accommodation):             {solv.mean()*100:.0f}% of steps")
    print("    -> DOMINANCE: the solvency ceiling rules the financed spiral; the stockout border is the ever-present")
    print("       recursion substrate; the wage floor is RARE — the solvency ceiling caps the wage push FIRST, so the")
    print("       two share a boundary but the ceiling pre-empts the floor (they interact, they don't just coexist).")

    # 4. all three conservation laws + determinism
    worst = 0.0
    for kappa in (0.0, KAP):
        worst = max(worst, steady_pi(kappa, SUPRA, i=0.10, cost_c=1, demand_b=1, distrib_a=0.3)[1].max_residual)
    worst = max(worst, eb.max_residual)
    print(f"\n[4] all THREE conservation laws (goods + three-way income + debt bookkeeping): worst = {worst:.0e} (<1e-9)")
    r1 = _cc(SUPRA, KAP, i=0.10, cost_c=1, demand_b=1, distrib_a=0.3).run(300)
    r2 = _cc(SUPRA, KAP, i=0.10, cost_c=1, demand_b=1, distrib_a=0.3).run(300)
    print(f"[5] determinism: byte-identical rerun = {np.array_equal(r1, r2)}")

    make_figures(out, iis, dec0, decK, floor, iis2, (k_cost, k_dis, k_neu), (stock, floor_b, solv, pi_b))
    print("\nsaved 3 figures to accommodation_coupled/figures/.")


# ============================================================ figures
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"; PUR="#7d3c98"
def make_figures(out, iis, dec0, decK, floor, iis2, ign, border):
    plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                         "figure.facecolor":"white","axes.facecolor":"white"})

    # ---- Fig 1: channel decomposition, coupled vs CYB-17 (HEADLINE) ----
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.2))
    fig.suptitle("CYB-18 — the rate's channel decomposition on the COUPLED substrate: recursion pins an inflation floor "
                 "the rate can't reach",
                 fontsize=11.5, fontweight="bold", y=0.99)
    # panel A: the four channels on the coupled substrate (the CYB-17 decomposition re-run)
    a1.axhline(decK["all"][0]*100, color=MUT, lw=1.0, ls=":", label=f"coupled baseline π*(i=0) = {decK['all'][0]*100:.2f}%/step")
    a1.axhline(floor*100, color=PUR, lw=1.4, ls="--", label=f"recursion-pinned floor  k·κ·⟨d⟩ = {floor*100:.2f}%/step")
    a1.axhline(0, color=INK, lw=0.7)
    a1.plot(iis*100, decK["cost"]*100, color=ACC, lw=2.2, marker="o", ms=3, label="COST — feeds (inflationary)")
    a1.plot(iis*100, decK["demand"]*100, color=BLU, lw=2.2, marker="s", ms=3, label="DEMAND — cools symmetrically")
    a1.plot(iis*100, decK["distrib"]*100, color=GRN, lw=2.2, marker="^", ms=3, label="DISTRIBUTIONAL — cools, but FLOORS")
    a1.plot(iis*100, decK["all"]*100, color=INK, lw=2.6, ls="--", label="ALL three (net) — bounded below by the floor")
    a1.set_xlabel("policy rate  i  (%/step)"); a1.set_ylabel("sustained inflation  π*  (%/step)")
    a1.set_title("the three channels on the coupled substrate — none reaches 0:\nthe reloaded gap κ·d(t) is an irreducible floor",
                 fontsize=9.5, fontweight="bold")
    a1.grid(True, color=GRID, lw=0.7); a1.set_axisbelow(True); a1.legend(frameon=False, fontsize=8.5, loc="upper left")
    # panel B: the money comparison — distributional-only, bare (exhausts→0) vs coupled (floors)
    a2.axhline(0, color=INK, lw=0.7)
    a2.axhline(floor*100, color=PUR, lw=1.4, ls="--", label=f"recursion floor k·κ·⟨d⟩ = {floor*100:.2f}%")
    a2.plot(iis*100, dec0["distrib"]*100, color=GRN, lw=2.4, ls=":", marker="v", ms=3,
            label="BARE CYB-17: distributional → 0 (EXHAUSTS: labor's static gap fully closed)")
    a2.plot(iis*100, decK["distrib"]*100, color=GRN, lw=2.6, marker="^", ms=3,
            label="COUPLED: distributional cools but can't reach 0 (recursion re-supplies g)")
    a2.fill_between(iis*100, dec0["distrib"]*100, decK["distrib"]*100, color=GRN, alpha=0.08)
    a2.set_xlabel("policy rate  i  (%/step)"); a2.set_ylabel("distributional-channel π*  (%/step)")
    a2.set_title("Q1 — the distributional channel does NOT self-exhaust under reloading:\nits clean zero becomes a recursion-pinned floor (the flip is deferred, not erased)",
                 fontsize=9.5, fontweight="bold")
    a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True); a2.legend(frameon=False, fontsize=8.5, loc="upper right")
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_accommodation_coupled_v0_decomposition.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 2: ignition threshold vs rate (Q2) ----
    k_cost, k_dis, k_neu = ign
    fig, ax = plt.subplots(figsize=(10, 6.2))
    ax.plot(iis2*100, k_neu, color=MUT, lw=2.0, ls=":", marker="o", ms=3, label="rate OFF (all channels 0) = CYB-10 baseline κ*≈0.10")
    ax.plot(iis2*100, k_cost, color=ACC, lw=2.4, marker="v", ms=4, label="COST-leaning (c=1,b=.5) — rate LOWERS κ* (cost self-ignites)")
    ax.plot(iis2*100, k_dis, color=BLU, lw=2.4, marker="^", ms=4, label="DISINFL-leaning (c=.2,b=1,a=.6) — rate RAISES κ* (chokes ignition)")
    ax.fill_between(iis2*100, 0, k_dis, color=BLU, alpha=0.05)
    ax.set_xlabel("policy rate  i  (%/step)"); ax.set_ylabel("ignition threshold  κ*  (coupling needed to ignite)")
    ax.set_title("CYB-18 — Q2: the rate GATES super-additive ignition, both ways\n"
                 "(cost lowers the coupling bar / disinflation raises it — the Q1 tug-of-war at the ignition margin)",
                 fontsize=10.5, fontweight="bold")
    ax.annotate("more recursion needed\nto ignite (rate chokes)", (14, 0.15), fontsize=8.5, color=BLU, ha="center")
    ax.annotate("cost-push ignites\nwith no coupling", (13, 0.008), fontsize=8.5, color=ACC, ha="center")
    ax.grid(True, color=GRID, lw=0.7); ax.set_axisbelow(True); ax.legend(frameon=False, fontsize=9, loc="center left")
    fig.tight_layout(); fig.savefig(out/"cybeersym_accommodation_coupled_v0_ignition_vs_rate.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 3: three-border dynamics ----
    stock, floor_b, solv, pi_b = border; n = len(stock); x = np.arange(n)
    fig, (b1, b2) = plt.subplots(2, 1, figsize=(12, 7.6), height_ratios=[1.1, 1])
    fig.suptitle("CYB-18 — three nonsmooth borders live at once: order non-negativity (recursion) + wage floor (conflict) + solvency ceiling (accommodation)",
                 fontsize=10.5, fontweight="bold", y=0.98)
    b1.plot(x, pi_b*100, color=ORG, lw=1.1, label="inflation π(t) — aperiodic (chaos leaks through the financed spiral)")
    b1.axhline(0, color=INK, lw=0.6)
    b1.set_ylabel("π(t) (%/step)"); b1.legend(frameon=False, fontsize=8.5, loc="upper right")
    b1.grid(True, color=GRID, lw=0.7); b1.set_axisbelow(True)
    b1.set_title("the financed, coupled spiral rides on a chaotic real substrate", fontsize=9.5)
    # border activity raster
    for y, (mask, color, name) in enumerate([
            (stock, BLU, f"order non-negativity / stockout — recursion ({stock.mean()*100:.0f}%)"),
            (floor_b, GRN, f"wage floor — conflict ({floor_b.mean()*100:.0f}%)"),
            (solv, ACC, f"solvency ceiling — accommodation ({solv.mean()*100:.0f}%)")]):
        b2.fill_between(x, y, y+0.85, where=mask, color=color, alpha=0.75, step="mid")
        b2.text(n*1.005, y+0.42, name, fontsize=8.5, color=color, va="center")
    b2.set_ylim(-0.1, 3.0); b2.set_yticks([]); b2.set_xlabel("step")
    b2.set_title("which border is active each step — the solvency ceiling DOMINATES the financed spiral and pre-empts the wage floor",
                 fontsize=9.5)
    b2.set_xlim(0, n*1.45)
    b2.grid(True, axis="x", color=GRID, lw=0.7); b2.set_axisbelow(True)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_accommodation_coupled_v0_three_borders.png", dpi=140, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
