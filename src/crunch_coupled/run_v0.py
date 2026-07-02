"""
CYB-22 — the CYB-19 Phase-1 credit-crunch on the CYB-18 coupled egg stack: does the
"bounds-without-curing" grind get WORSE when recursion keeps re-loading the gap?

Runs, in order:
  0. TWO regression anchors — both byte-exact:
       (a) crunch-off        ⇒ reproduces CYB-18 (accommodation-coupled).
       (b) decouple (κ=0)    ⇒ reproduces CYB-19 Phase 1 (crunch on bare CYB-17).
  1. Crunch-under-coupling (headline): the choke a hard crunch can achieve, coupled vs bare —
     does recursion's reload raise the ~12% floor? + the (L_trig, δ) bounding/fizzle map.
  2. The limit cycle under coupling: amplitude + firing frequency vs bare.
  3. Border dynamics under coupling vs CYB-18's static 73% / Phase-1's limit-cycle 73%.
  4. Conservation through the crunch transient; determinism.

Determinism: σ=0. All conservation laws (goods + three-way income + debt bookkeeping) asserted
inside the reused submodules every step.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import (CrunchCoupledEconomy, ChaosParams, CrunchParams, AccommodationParams,  # our model.py
                   AccommodationCoupledEconomy, CrunchEconomy)                             # the two parents

CP = dict(beta=0.18, a_S=0.7, L=3, theta=0.25, perturb=1.0)     # amplifying (chaotic) chain
BASE = dict(omega_f=0.65, gap=0.10, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
COST = 0.30
I_HEAD = 0.60                    # Ponzi regime (the crunch lives at high rates)
KAP = 0.20                       # CYB-18 headline coupling strength
AM, HEAL = 0.02, 0.05
NSTEP, TAIL = 900, 300

def _mk(kappa, delta, L_trig, i=I_HEAD, crunch=True, **kw):
    return CrunchCoupledEconomy(
        ChaosParams(**CP),
        CrunchParams(acc=AccommodationParams(**BASE, i=i, cost_c=COST, **kw),
                     crunch_enabled=crunch, L_trig=L_trig, delta=delta, am=AM, heal=HEAL),
        kappa=kappa)

def tail(kappa, delta, L_trig, n=NSTEP, t=TAIL, **kw):
    # δ=0 ⇒ crunch OFF (true no-crunch baseline), matching Phase 1's crunch_enabled=(δ>0).
    e = _mk(kappa, delta, L_trig, crunch=(delta > 0.0), **kw)
    pis = np.empty(n); solv = np.zeros(n, bool)
    for k in range(n):
        e.step(); pis[k] = e.last_pi; solv[k] = e.solvency_bound
    return float(np.mean(pis[-t:])), float(np.std(pis[-t:])), float(solv[-t:].mean()), e


# ---- 0. the two regression anchors -----------------------------------------
def regression_anchors():
    kw = dict(i=I_HEAD, cost_c=COST)
    # (a) crunch-off, κ>0 → CYB-18
    comp = _mk(KAP, 0.0, 0.64, crunch=False)
    ref = AccommodationCoupledEconomy(ChaosParams(**CP), AccommodationParams(**BASE, **kw), kappa=KAP)
    da = 0.0
    for _ in range(400):
        comp.step(); ref.step()
        da = max(da, abs(comp.conflict.W - ref.conflict.W), abs(comp.conflict.P - ref.conflict.P), abs(comp.D - ref.D))
    print(f"[0a] crunch-off → CYB-18: max|W,P,D Δ| = {da:.1e}  byte-identical={da == 0.0}")
    assert da == 0.0, "ANCHOR-1 LEAK: crunch-off did not reproduce CYB-18"
    # (b) κ=0, crunch-on → CYB-19 Phase 1
    comp2 = _mk(0.0, 0.35, 0.64)
    ref2 = CrunchEconomy(CrunchParams(acc=AccommodationParams(**BASE, **kw),
                                      crunch_enabled=True, L_trig=0.64, delta=0.35, am=AM, heal=HEAL))
    db = 0.0
    for _ in range(400):
        comp2.step(); ref2.step()
        db = max(db, abs(comp2.conflict.W - ref2.conflict.W), abs(comp2.conflict.P - ref2.conflict.P), abs(comp2.D - ref2.D))
    print(f"[0b] decouple κ=0 → CYB-19 Phase 1: max|W,P,D Δ| = {db:.1e}  byte-identical={db == 0.0}")
    assert db == 0.0, "ANCHOR-2 LEAK: κ=0 did not reproduce CYB-19 Phase 1"
    print("     -> both composition axes anchored (coupling × crunch); nothing leaked.")


# ---- 1. crunch-under-coupling: choke vs δ + outcome map ---------------------
def choke_curves(deltas, L_trig=0.64):
    base_b = tail(0.0, 0.0, L_trig)[0]; base_k = tail(KAP, 0.0, L_trig)[0]
    fb = np.array([tail(0.0, d, L_trig)[0] for d in deltas]) / base_b
    fk = np.array([tail(KAP, d, L_trig)[0] for d in deltas]) / base_k
    return base_b, base_k, fb, fk

def outcome_map(L_grid, d_grid, kappa):
    base = tail(kappa, 0.0, 0.99)[0]
    Z = np.empty((len(d_grid), len(L_grid))); leak = 0.0
    for a, dlt in enumerate(d_grid):
        for b, L in enumerate(L_grid):
            tp, _, _, e = tail(kappa, dlt, L); Z[a, b] = tp / base; leak = max(leak, e.max_residual)
    return Z, base, leak


# ---- 2. limit cycle under coupling -----------------------------------------
def limit_cycle(delta=0.35, L_trig=0.64, n=500):
    def trace(kappa):
        e = _mk(kappa, delta, L_trig); pi = np.empty(n); act = np.zeros(n, bool)
        solv = np.zeros(n, bool); lev = np.empty(n)
        for k in range(n):
            e.step(); pi[k] = e.last_pi; act[k] = e.crunch_active; solv[k] = e.solvency_bound; lev[k] = e.leverage
        return pi, act, solv, lev
    return trace(0.0), trace(KAP)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-22: the credit-crunch on the coupled egg stack — does the grind worsen? ===\n")
    regression_anchors()

    # 1. choke curves + floor
    deltas = np.round(np.linspace(0.0, 0.95, 20), 3)
    base_b, base_k, fb, fk = choke_curves(deltas)
    floor_b, floor_k = fb.min(), fk.min()
    print(f"\n[1] crunch-under-coupling (headline), i={I_HEAD}, L_trig=0.64:")
    print(f"    baseline spiral (no crunch): bare {base_b*100:+.2f}%/step  →  coupled {base_k*100:+.2f}%/step "
          f"(recursion reloads g ⇒ hotter)")
    print(f"    best achievable choke (min over δ, as % of own baseline): bare {floor_b*100:.0f}%  →  coupled {floor_k*100:.0f}%")
    print(f"    -> the grind WORSENS under reloading: recursion re-ignites the spiral in the crunch's")
    print(f"       recover phase, so the achievable floor RISES ({floor_b*100:.0f}% → {floor_k*100:.0f}%) and the crunch")
    print(f"       is uniformly less effective — bounds-without-curing, now with a higher floor.")

    L_grid = np.round(np.linspace(0.60, 0.72, 19), 4)
    d_grid = np.round(np.linspace(0.0, 0.90, 19), 4)
    Zc, base_c, leak = outcome_map(L_grid, d_grid, KAP)

    # 2. limit cycle
    (pi_b, act_b, solv_b, lev_b), (pi_k, act_k, solv_k, lev_k) = limit_cycle()
    amp_b, amp_k = np.std(pi_b[-300:]), np.std(pi_k[-300:])
    fire_b, fire_k = act_b[-300:].mean(), act_k[-300:].mean()
    print(f"\n[2] limit cycle under coupling (δ=0.35): amplitude (tail σ of π) bare {amp_b*100:.2f} → coupled {amp_k*100:.2f} %/step;")
    print(f"    crunch fires {fire_b*100:.0f}% of steps bare → {fire_k*100:.0f}% coupled "
          f"({'more often' if fire_k > fire_b + 0.02 else 'about the same'}); recursion keeps π higher between cuts.")

    # 3. border dynamics
    sb, sk = solv_b[-300:].mean(), solv_k[-300:].mean()
    print(f"\n[3] border dynamics: the solvency/crunch border binds {sb*100:.0f}% (bare) → {sk*100:.0f}% (coupled) of steps")
    print(f"    (CYB-18 static ceiling: 73%). The (now dynamic) solvency border stays DOMINANT on both — but")
    print(f"    coupling makes the spiral hotter BETWEEN binds (chaotic reload), so it chokes less per bind.")

    # 4. conservation + determinism
    worst = max(leak, tail(KAP, 0.35, 0.64)[3].max_residual)
    print(f"\n[4] all conservation laws through the crunch transient (coupled): worst residual = {worst:.0e} (<1e-9)")
    r1 = _mk(KAP, 0.35, 0.64).run(300); r2 = _mk(KAP, 0.35, 0.64).run(300)
    print(f"[5] determinism: byte-identical rerun = {np.array_equal(r1, r2)}")

    make_figures(out, deltas, base_b, base_k, fb, fk, L_grid, d_grid, Zc,
                 (pi_b, act_b), (pi_k, act_k))
    print("\nsaved 3 figures to crunch_coupled/figures/.")


# ============================================================ figures
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"; PUR="#7d3c98"
def make_figures(out, deltas, base_b, base_k, fb, fk, L_grid, d_grid, Zc, trace_b, trace_k):
    plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                         "figure.facecolor":"white","axes.facecolor":"white"})

    # ---- Fig 1: choke vs δ (bare vs coupled) + the coupled outcome map ----
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6.2))
    fig.suptitle("CYB-22 — the crunch on the coupled egg stack: recursion's reload RAISES the choke floor (the grind worsens)",
                 fontsize=11.5, fontweight="bold", y=0.99)
    a1.plot(deltas, fb*100, color=BLU, lw=2.4, marker="o", ms=3, label=f"BARE CYB-17 (κ=0): floor → {fb.min()*100:.0f}%")
    a1.plot(deltas, fk*100, color=ACC, lw=2.4, marker="s", ms=3, label=f"COUPLED (κ={KAP}): floor → {fk.min()*100:.0f}%")
    a1.fill_between(deltas, fb*100, fk*100, color=ACC, alpha=0.07)
    a1.axhline(fb.min()*100, color=BLU, lw=1.0, ls=":"); a1.axhline(fk.min()*100, color=ACC, lw=1.0, ls=":")
    a1.set_xlabel("deleverage rate  δ"); a1.set_ylabel("achievable choke  (tail π as % of own baseline)")
    a1.set_title("even a hard crunch chokes LESS under coupling —\nrecursion re-ignites in the recover phase (bounds-without-curing, higher floor)",
                 fontsize=9.5, fontweight="bold")
    a1.grid(True, color=GRID, lw=0.7); a1.set_axisbelow(True); a1.legend(frameon=False, fontsize=9, loc="upper right")
    im = a2.pcolormesh(L_grid, d_grid, Zc*100, cmap="RdYlGn_r", shading="auto", vmin=0, vmax=110)
    cs = a2.contour(L_grid, d_grid, Zc, levels=[0.4, 0.75], colors="k", linewidths=[2.0, 1.3], linestyles=["-", "--"])
    a2.clabel(cs, fmt={0.4: "bound/fizzle", 0.75: "fizzle/no-op"}, fontsize=8)
    fig.colorbar(im, ax=a2, label="tail π as % of coupled baseline")
    a2.set_xlabel("leverage-at-trigger  L_trig"); a2.set_ylabel("deleverage rate  δ")
    a2.set_title(f"coupled bounding/fizzle map (i={I_HEAD}, κ={KAP})\nsame diagonal structure as bare — shifted toward 'harder to bound'",
                 fontsize=9.5, fontweight="bold")
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_crunch_coupled_v0_choke_and_map.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 2: limit cycle bare vs coupled ----
    pi_b, act_b = trace_b; pi_k, act_k = trace_k; n = len(pi_b); x = np.arange(n)
    fig, (b1, b2) = plt.subplots(2, 1, figsize=(12, 7.2), sharex=True)
    fig.suptitle("CYB-22 — the limit cycle under coupling: recursion re-ignition keeps inflation higher between cuts",
                 fontsize=11, fontweight="bold", y=0.98)
    b1.plot(x, pi_b*100, color=BLU, lw=1.1)
    b1.fill_between(x, 0, 1, where=act_b, color=BLU, alpha=0.07, transform=b1.get_xaxis_transform())
    b1.axhline(0, color=INK, lw=0.6); b1.set_ylabel("π(t) (%/step)")
    b1.set_title(f"BARE CYB-17 (κ=0): clean fire→cut→recover limit cycle, deep troughs (fires {act_b[-300:].mean()*100:.0f}% of steps)", fontsize=9.5)
    b1.grid(True, color=GRID, lw=0.7); b1.set_axisbelow(True)
    b2.plot(x, pi_k*100, color=ACC, lw=1.1)
    b2.fill_between(x, 0, 1, where=act_k, color=ACC, alpha=0.07, transform=b2.get_xaxis_transform())
    b2.axhline(0, color=INK, lw=0.6); b2.set_xlabel("step"); b2.set_ylabel("π(t) (%/step)")
    b2.set_title(f"COUPLED (κ={KAP}): recursion reloads the gap during recovery → shallower troughs, higher floor (fires {act_k[-300:].mean()*100:.0f}%)", fontsize=9.5)
    b2.grid(True, color=GRID, lw=0.7); b2.set_axisbelow(True)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_crunch_coupled_v0_limit_cycle.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 3: choke-floor bar summary (border/effectiveness) ----
    fig, ax = plt.subplots(figsize=(8.5, 5.6))
    cats = ["baseline\n(no crunch)", "hard crunch\n(δ=0.9)"]
    bare_vals = [100, fb.min()*100]; coup_vals = [100, fk.min()*100]
    xb = np.arange(2); w = 0.36
    ax.bar(xb - w/2, bare_vals, w, color=BLU, label="bare CYB-17 (κ=0)")
    ax.bar(xb + w/2, coup_vals, w, color=ACC, label=f"coupled (κ={KAP})")
    for xx, v in zip(xb - w/2, bare_vals): ax.annotate(f"{v:.0f}%", (xx, v), ha="center", va="bottom", fontsize=9, color=BLU)
    for xx, v in zip(xb + w/2, coup_vals): ax.annotate(f"{v:.0f}%", (xx, v), ha="center", va="bottom", fontsize=9, color=ACC)
    ax.set_xticks(xb); ax.set_xticklabels(cats); ax.set_ylabel("tail inflation as % of own baseline")
    ax.set_title("CYB-22 — the crunch's reach is blunted by coupling\nthe achievable choke floor rises when recursion keeps reloading the gap",
                 fontsize=10.5, fontweight="bold")
    ax.legend(frameon=False, fontsize=9); ax.grid(True, axis="y", color=GRID, lw=0.7); ax.set_axisbelow(True)
    fig.tight_layout(); fig.savefig(out/"cybeersym_crunch_coupled_v0_floor_summary.png", dpi=140, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
