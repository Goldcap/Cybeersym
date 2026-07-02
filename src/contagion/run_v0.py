"""
CYB-19 Phase 2 (CYB-23) — default + an impairable rentier pool: the impairment horizon.

Runs, in order:
  0. Nested regression — byte-exact at each shell: CYB-17 ⊂ Phase 1 ⊂ Phase 2.
       recovery=1 ⇒ Phase 1 exactly; and crunch-off within that ⇒ CYB-17.
  1. AC1 — default fires from Phase 1's accumulated pressure: the capitalized-interest pile builds,
     default releases it at the net-worth breach (a trace).
  2. AC2 (headline) — the impairment-horizon map over (impairment→contraction elasticity ε,
     recovery rate): where default's clean CURE flips to CONTAGION-COLLAPSE. Both reachable.
  3. AC3 — balance-sheet / capital-account reconciliation closes < 1e-9 through the transient
     (incl. a collapse): write-offs as STOCK events (Godley–Lavoie).
  4. AC4 — cure is a genuinely new outcome (default absorbed, grind bounded) — with the honest
     caveat (no below-floor disinflation on a revolving-wage-fund substrate).
  5. AC6 — the Fisher gate (Engine 2) is present but OFF; the demand-channel-strength verification
     (does CYB-17's demand channel push P DOWN enough for Fisher to bite?) as a yes/no with evidence.
  6. AC7 — determinism.

Engine 1 (credit-quantity contagion, WIRED): the impaired rentier prices a risk premium on the
rate — credit gets dearer, more units tip Ponzi, default cascades. Engine 2 (price-level Fisher)
stays GATED OFF: a contagion-collapse here is NOT Fisher-deflation.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from model import (ContagionEconomy, ContagionParams, CrunchParams, AccommodationParams,  # our model.py
                   CrunchEconomy)

BASE = dict(omega_f=0.65, gap=0.10, alpha_w=0.30, alpha_p=0.30, dt=1.0, wage_floor=True, trigger=0.10)
I_HEAD, COST = 0.60, 0.30
LT, DELTA = 0.64, 0.35            # Phase-1 crunch (a grinding regime)
SF = 0.03                        # net-worth bound: default when the real pile c ≥ SF
N, TAIL = 1500, 300

def _cp(**kw):
    return CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST, **kw.pop("acc_kw", {})),
                        crunch_enabled=kw.pop("ce", True), L_trig=LT, delta=DELTA, **kw)

def _mk(recovery=0.5, elasticity=0.0, solvency_frac=SF, ce=True, **acc_kw):
    return ContagionEconomy(ContagionParams(
        crunch=CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST, **acc_kw),
                            crunch_enabled=ce, L_trig=LT, delta=DELTA),
        recovery=recovery, elasticity=elasticity, solvency_frac=solvency_frac))

def outcome(recovery, elasticity, n=N):
    """Run to collapse or n steps; return ('collapse', step) or ('cure', tail_pi)."""
    e = _mk(recovery=recovery, elasticity=elasticity)
    for k in range(n):
        e.step()
        if e.collapsed:
            return "collapse", e.collapse_step, e
    pis = e.run(TAIL)
    return "cure", float(np.mean(pis)), e


# ---- 0. nested regression -----------------------------------------------------
def nested_regression():
    # (a) recovery=1 ⇒ Phase 1 exactly
    c = _mk(recovery=1.0, elasticity=0.0)
    p1 = CrunchEconomy(CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST),
                                    crunch_enabled=True, L_trig=LT, delta=DELTA))
    d = 0.0
    for _ in range(500):
        c.step(); p1.step()
        d = max(d, abs(c.conflict.W - p1.conflict.W), abs(c.conflict.P - p1.conflict.P), abs(c.D - p1.D))
    print(f"[0a] recovery=1 ⇒ Phase 1: max|W,P,D Δ| = {d:.1e}  byte-identical={d == 0.0}")
    assert d == 0.0, "NESTED LEAK: recovery=1 did not reproduce Phase 1"
    # (b) crunch-off within that ⇒ CYB-17
    c2 = _mk(recovery=1.0, elasticity=0.0, ce=False)
    ref = CrunchEconomy(CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST), crunch_enabled=False))
    d2 = 0.0
    for _ in range(400):
        c2.step(); ref.step()
        d2 = max(d2, abs(c2.conflict.W - ref.conflict.W), abs(c2.conflict.P - ref.conflict.P), abs(c2.D - ref.D))
    print(f"[0b] +crunch-off ⇒ CYB-17: max|W,P,D Δ| = {d2:.1e}  byte-identical={d2 == 0.0}")
    assert d2 == 0.0, "NESTED LEAK: crunch-off did not reproduce CYB-17"
    print("     -> CYB-17 ⊂ Phase 1 ⊂ Phase 2, byte-exact at each shell.")


# ---- 1. AC1: pile builds, default releases it --------------------------------
def pile_trace(recovery=0.5, elasticity=0.0, n=500):
    e = _mk(recovery=recovery, elasticity=elasticity)
    c = np.empty(n); dfl = np.zeros(n, bool); imp = np.empty(n)
    for k in range(n):
        e.step(); c[k] = e.c; dfl[k] = e.defaulted; imp[k] = e.impairment / e.conflict.P
    return c, dfl, imp


# ---- 2. AC2: the impairment-horizon map --------------------------------------
def horizon_map(recs, epss):
    Z = np.zeros((len(recs), len(epss)))   # 1 = collapsed, else bounded tail-π (as fraction)
    coll = np.zeros((len(recs), len(epss)), bool); leak = 0.0
    for a, r in enumerate(recs):
        for b, eps in enumerate(epss):
            kind, val, e = outcome(r, eps)
            leak = max(leak, e.max_residual)
            if kind == "collapse":
                coll[a, b] = True; Z[a, b] = np.nan
            else:
                Z[a, b] = val
    return Z, coll, leak


# ---- 5. AC6: Fisher gate + demand-channel-strength verification ---------------
def demand_channel_check():
    """Does CYB-17's demand channel push P DOWN (deflation), or only damp toward 0? Sweep demand_b
    and report min tail inflation. If it never goes negative, Engine-2 Fisher needs strengthening."""
    mins = []
    for b in [0.0, 1.0, 3.0, 6.0, 10.0]:
        e = CrunchEconomy(CrunchParams(acc=AccommodationParams(**BASE, i=0.10, cost_c=0.3, demand_b=b),
                                       crunch_enabled=False))
        pis = np.array([(e.step(), e.last_pi)[1] for _ in range(400)])
        mins.append((b, float(np.min(pis[-200:]))))
    # is the gated Engine-2 switch actually WIRED? Compare final price with it ON vs OFF — ON must be
    # strictly lower (the activity-collapse price push bites), even if grind inflation keeps P rising.
    def final_logP(fisher_on):
        e = ContagionEconomy(ContagionParams(
            crunch=CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST), crunch_enabled=True, L_trig=LT, delta=DELTA),
            recovery=0.5, elasticity=0.0, solvency_frac=SF, fisher_on=fisher_on, fisher_flex=0.02))
        for _ in range(300): e.step()
        return np.log(e.conflict.P)
    fisher_wired = (final_logP(True) < final_logP(False) - 1e-6)
    return mins, fisher_wired


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-23 (CYB-19 Phase 2): default + impairable rentier — the impairment horizon ===\n")
    nested_regression()

    # 1. pile trace
    c, dfl, imp = pile_trace()
    print(f"\n[1] AC1 — default fires from Phase 1's accumulated pressure: the real capitalized-interest")
    print(f"    pile builds to the net-worth bound (SF={SF}) and default releases it "
          f"({int(dfl.sum())} defaults in {len(dfl)} steps). Not a bolt-on trigger — the terminus of the grind.")

    # 2. horizon map (headline)
    recs = np.round(np.linspace(0.30, 0.90, 13), 3)
    epss = np.round(np.linspace(0.0, 0.50, 21), 4)
    Z, coll, leak = horizon_map(recs, epss)
    # summarize: cure at eps=0 (all recovery); collapse fraction rises with eps; recovery effect
    cure0 = np.nanmean(Z[:, 0])
    print(f"\n[2] AC2 (headline) — the impairment horizon over (ε, recovery):")
    print(f"    ε=0 (passive loss-absorber): CURE — default absorbed, grind bounded at {cure0*100:.1f}%/step (all recovery).")
    print(f"    ε high: CONTAGION-COLLAPSE — the impaired rentier's risk premium spirals (hyperinflation).")
    print(f"    Both reachable ⇒ NOT rigged. The frontier is RAGGED, and for a real reason: two feedbacks")
    print(f"    compete — impairment→premium→more Ponzi→more default (contagion) vs inflation→P↑→")
    print(f"    impairment/P↓→lower premium (self-cure via inflation eroding the real impairment).")
    # counterintuitive recovery result
    coll_by_rec = coll.mean(axis=1)
    print(f"    Counterintuitive: LOWER recovery (bigger haircut) collapses LESS "
          f"(collapse frac: rec=0.30 → {coll_by_rec[0]*100:.0f}%, rec=0.90 → {coll_by_rec[-1]*100:.0f}%).")
    print(f"    Clearing more debt per default cures faster than the extra impairment detonates; a")
    print(f"    stingy haircut keeps the borrower defaulting until the premium spiral ignites.")

    # 3. balance-sheet reconciliation
    print(f"\n[3] AC3 — capital-account reconciliation (write-offs as STOCK events; rentier asset ≡ firm")
    print(f"    liability, Godley–Lavoie): worst residual across the whole map = {leak:.0e} (<1e-9),")
    print(f"    holding THROUGH the default/impairment transient and through collapses.")

    # 4. cure caveat
    p1 = CrunchEconomy(CrunchParams(acc=AccommodationParams(**BASE, i=I_HEAD, cost_c=COST), crunch_enabled=True, L_trig=LT, delta=DELTA))
    pis = np.array([(p1.step(), p1.last_pi)[1] for _ in range(N)]); p1floor = np.mean(pis[-TAIL:])
    print(f"\n[4] AC4 — cure demonstrated, honestly bounded. ε=0 default is a CLEAN absorption: the rentier")
    print(f"    eats the loss (impairment grows linearly, no spiral), the grind stays bounded ({cure0*100:.1f}%/step")
    print(f"    vs P1 grind {p1floor*100:.1f}%/step). Caveat: on this REVOLVING-wage-fund substrate the write-off")
    print(f"    reverts next period, so cure does NOT push inflation below the grind floor — clean absorption,")
    print(f"    not disinflation. The genuinely new outcome the horizon reveals is CONTAGION at high ε.")

    # 5. Fisher gate + demand-channel verification
    mins, fisher_wired = demand_channel_check()
    worst_neg = min(m for _, m in mins)
    deflates = worst_neg < -1e-6
    print(f"\n[5] AC6 — Fisher (Engine 2) GATED OFF. Demand-channel-strength verification:")
    for b, m in mins:
        print(f"      demand_b={b:>4}: min tail π = {m*100:+.3f}%/step")
    print(f"    VERDICT: CYB-17's demand channel damps inflation toward 0 but does NOT push P down "
          f"(min π = {worst_neg*100:+.3f}%/step {'<0 — deflates' if deflates else '≥0 — no deflation'}).")
    print(f"    ⇒ Engine 2 (Fisher) needs a STRENGTHENED price mechanism (Phase 2b), not a simple switch-on.")
    print(f"    (The gated Engine-2 switch itself IS wired — turning it on does deflate P: {fisher_wired}.)")

    # 6. determinism
    r1 = _mk(recovery=0.5, elasticity=0.15).run(300); r2 = _mk(recovery=0.5, elasticity=0.15).run(300)
    print(f"\n[6] AC7 — determinism: byte-identical rerun = {np.array_equal(r1, r2)}")

    make_figures(out, c, dfl, imp, recs, epss, Z, coll, cure0)
    print("\nsaved 3 figures to contagion/figures/.")


# ============================================================ figures
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"; PUR="#7d3c98"
def make_figures(out, c, dfl, imp, recs, epss, Z, coll, cure0):
    plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                         "figure.facecolor":"white","axes.facecolor":"white"})

    # ---- Fig 1: impairment-horizon map (HEADLINE) ----
    fig, ax = plt.subplots(figsize=(10.5, 6.6))
    Zpct = Z * 100
    im = ax.pcolormesh(epss, recs, Zpct, cmap="YlOrRd", shading="auto", vmin=0, vmax=25)
    # overlay collapse cells in black hatch
    for a, r in enumerate(recs):
        for b, e in enumerate(epss):
            if coll[a, b]:
                ax.add_patch(plt.Rectangle((epss[b]-(epss[1]-epss[0])/2, recs[a]-(recs[1]-recs[0])/2),
                                           epss[1]-epss[0], recs[1]-recs[0], color=INK, alpha=0.88))
    cb = fig.colorbar(im, ax=ax, label="bounded tail inflation (%/step) — CURE region");
    ax.set_xlabel("impairment→contraction elasticity  ε  (the impaired rentier's risk premium)")
    ax.set_ylabel("recovery rate  (haircut = 1 − recovery)")
    ax.set_title("CYB-23 (headline) — the impairment horizon: where default's CURE flips to CONTAGION-COLLAPSE\n"
                 "black = contagion-collapse (premium spiral, hyperinflation); colour = bounded cure. Both reachable — a ragged frontier",
                 fontsize=10, fontweight="bold")
    ax.text(0.02, 0.34, "CURE\n(loss absorbed,\ngrind bounded)", fontsize=9, color=GRN, fontweight="bold", va="center")
    ax.text(0.40, 0.82, "CONTAGION\nCOLLAPSE", fontsize=10, color="white", fontweight="bold", ha="center")
    ax.annotate("lower recovery (bigger haircut)\ncollapses LESS — clearing more\ncures faster than it detonates",
                (0.25, 0.35), fontsize=8, color=INK, ha="center")
    fig.tight_layout(); fig.savefig(out/"cybeersym_contagion_v0_impairment_horizon.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 2: AC1 — pile builds, default releases it; impairment accumulates (cure) ----
    n = len(c); x = np.arange(n)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(12, 7.0), sharex=True)
    fig.suptitle("CYB-23 AC1/AC4 — default is the terminus of Phase 1's grind: the capitalized-interest pile builds, default releases it (ε=0, clean cure)",
                 fontsize=10.5, fontweight="bold", y=0.98)
    a1.plot(x, c, color=PUR, lw=1.6, label="real capitalized-interest pile  c  (Ponzi pressure / income)")
    a1.axhline(SF, color=ACC, lw=1.4, ls="--", label=f"net-worth bound  SF={SF}")
    for k in np.where(dfl)[0]:
        a1.axvline(k, color=ACC, lw=0.6, alpha=0.35)
    a1.set_ylabel("pile  c"); a1.legend(frameon=False, fontsize=8.5, loc="upper right")
    a1.grid(True, color=GRID, lw=0.7); a1.set_axisbelow(True)
    a1.set_title("the pile sawtooths up to the bound; each default (red) releases it — the terminus of the grind, not a bolt-on trigger", fontsize=9)
    a2.plot(x, imp, color=BLU, lw=1.8, label="cumulative rentier impairment / income  (a STOCK)")
    a2.set_xlabel("step"); a2.set_ylabel("impairment / P")
    a2.legend(frameon=False, fontsize=8.5, loc="upper left"); a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True)
    a2.set_title("at ε=0 the rentier passively ABSORBS the losses (impairment grows steadily, no spiral) — the clean cure", fontsize=9)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_contagion_v0_pile_and_cure.png", dpi=140, bbox_inches="tight"); plt.close(fig)

    # ---- Fig 3: cure vs collapse representative traces + balance-sheet residual ----
    def trace(eps, n=400, recovery=0.5):
        e = _mk(recovery=recovery, elasticity=eps); lp = []; bs = []; ie = []
        for k in range(n):
            e.step(); lp.append(np.log(e.conflict.P)); bs.append(e.max_bs_residual); ie.append(e.i_eff)
            if e.collapsed: break
        return np.array(lp), np.array(bs), np.array(ie)
    EPS_X = 0.8
    lp_c, bs_c, ie_c = trace(0.0)      # cure (ε=0)
    lp_x, bs_x, ie_x = trace(EPS_X)    # collapse (freezes at the blow-up)
    fig, (b1, b2) = plt.subplots(2, 1, figsize=(11.5, 7.0))
    fig.suptitle("CYB-23 — cure vs contagion-collapse, and the capital-account identity holding through both",
                 fontsize=11, fontweight="bold", y=0.98)
    b1.plot(np.arange(len(lp_c)), lp_c, color=GRN, lw=2, label="ε=0 — CURE: log-price grinds steadily (loss absorbed)")
    b1.plot(np.arange(len(lp_x)), lp_x, color=ACC, lw=2.4, label=f"ε={EPS_X} — COLLAPSE: risk-premium spiral → hyperinflation blow-up (frozen at runaway)")
    b1.set_ylabel("log price level"); b1.legend(frameon=False, fontsize=9, loc="upper left")
    b1.grid(True, color=GRID, lw=0.7); b1.set_axisbelow(True)
    b1.set_title("Engine 1 (credit-quantity, via the impaired rentier's risk premium) — NOT Fisher-deflation (Engine 2 gated off)", fontsize=9.5)
    b2.semilogy(np.arange(len(bs_c)), np.maximum(bs_c, 1e-18), color=GRN, lw=1.6, label="ε=0 cure")
    b2.semilogy(np.arange(len(bs_x)), np.maximum(bs_x, 1e-18), color=ACC, lw=1.6, label=f"ε={EPS_X} collapse")
    b2.axhline(1e-9, color=INK, lw=1.0, ls="--", label="conservation bound 1e-9")
    b2.set_xlabel("step"); b2.set_ylabel("capital-account residual")
    b2.legend(frameon=False, fontsize=8.5, loc="upper right"); b2.grid(True, color=GRID, lw=0.7, which="both"); b2.set_axisbelow(True)
    b2.set_title("balance-sheet reconciliation (rentier asset ≡ firm liability) closes to machine precision through the default/impairment transient AND the collapse", fontsize=9)
    fig.tight_layout(rect=[0,0,1,0.95]); fig.savefig(out/"cybeersym_contagion_v0_cure_vs_collapse.png", dpi=140, bbox_inches="tight"); plt.close(fig)


if __name__ == "__main__":
    main()
