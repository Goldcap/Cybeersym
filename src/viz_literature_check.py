"""
CYB-42 — do the viz's "over time" trajectories match the LITERATURE? (topological, not metric)

The viz plots impulse responses (Lucas/RBC, Mankiw/NK) and cycles (Goodwin, Keen). Those were
validated against each model's own *self-test signatures*, but not against the shapes documented in
the published literature. This script computes the OUR-SIDE features and checks them against the
documented canonical shapes (see the LIT dict, sourced from the literature-review pass), reporting a
pass/fail per feature. Shape/sign/timing only — never a magnitude fit (Andy's topological rule).

Run from src/:  python3 viz_literature_check.py   (prints the comparison table; --fig saves figures)

Sources (see docs/ for the full review):
  RBC  — King–Plosser–Rebelo (1988); Campbell (1994).
  NK   — Galí (2015, ch.3); Clarida–Galí–Gertler (1999); Galí (1999) on technology & hours.
  Goodwin — Goodwin (1967); Harvie (2000, empirical OECD cycles).
  Keen — Keen (1995); Grasselli & Costa Lima (2012).
"""
import sys
import numpy as np
from orthodox.rbc import RBCParams, irf as rbc_irf
from orthodox.nk import NKParams, irf as nk_irf
from goodwin_keen.model import GKParams, gk_step, goodwin_equilibrium, goodwin_frequency, conserved_H, keen_good_equilibrium


def _mono_after_impact(x, n=120):
    """True if x[0:n] has no sign change in its increments after impact (monotone recovery)."""
    dx = np.diff(x[:n]); nz = dx[np.abs(dx) > 1e-9]
    return bool(np.all(nz > 0) or np.all(nz < 0))


def rbc_features():
    p = RBCParams(); r = rbc_irf(p, shock=-0.01, T=400)
    YK, IY, CY, theta = p.ratios()
    y, c, n = r["y"], r["c"], r["n"]
    inv = (y - CY * c) / IY                                   # investment via resource identity
    return {
        "output falls on impact & recovers monotonically": (y[0] < 0 and _mono_after_impact(y)),
        "consumption smoother than output (|c0|<|y0|)": abs(c[0]) < abs(y[0]),
        "investment more volatile than output (σ_i>σ_y)": np.std(inv) > np.std(y),
        "consumption less volatile than output (σ_c<σ_y)": np.std(c) < np.std(y),
        "hours overshoot (non-monotone, capital rebuild)": (not _mono_after_impact(n)) and np.max(n[1:]) > 0,
        "real wage procyclical (falls with output)": (y[0] - n[0]) < 0,
        "_nums": f"σ_c={np.std(c):.4f} σ_y={np.std(y):.4f} σ_i={np.std(inv):.4f}; y0={y[0]:.4f} c0={c[0]:.4f} n0={n[0]:.4f}",
    }


def nk_demand_features():
    p = NKParams(); s = nk_irf(p, shock=-0.01, kind="demand", T=400)
    x, pi, i = s["x"], s["pi"], s["i"]
    return {
        "gap & inflation move together (both fall)": (np.sign(x[0]) == np.sign(pi[0]) and x[0] < 0),
        "policy rate falls (eases)": i[0] < 0,
        "gap troughs ON IMPACT, not hump-shaped (bare 3-eq)": int(np.argmin(x)) == 0,
        "_nums": f"x0={x[0]:.4f} pi0={pi[0]:.4f} i0={i[0]:.4f}; trough@{int(np.argmin(x))}",
    }


def nk_costpush_features():
    p = NKParams(); s = nk_irf(p, shock=-0.01, kind="supply", T=400)
    x, pi, i = s["x"], s["pi"], s["i"]
    return {
        "TRADEOFF: output down, inflation UP (opposite signs)": (x[0] < 0 and pi[0] > 0),
        "policy tightens (rate up)": i[0] > 0,
        "_nums": f"x0={x[0]:.4f} pi0={pi[0]:.4f} i0={i[0]:.4f}",
    }


def goodwin_features():
    p = GKParams(keen=False, delta=0.0)
    w, l, _ = goodwin_equilibrium(p)
    s = np.array([w * 0.97, l * 0.97, 0.0]); dt = p.dt
    W, L, H = [], [], []
    for i in range(120000):
        W.append(s[0]); L.append(s[1]); H.append(conserved_H(s, p)); s = gk_step(s, p)
    W = np.array(W); L = np.array(L); H = np.array(H)
    per = int(round(2 * np.pi / goodwin_frequency(p) / dt))    # steps per cycle
    # Peak timing over one clean cycle: which variable peaks first tells which leads.
    seg = slice(0, min(len(L), 2 * per))
    tL = int(np.argmax(L[seg])); tW = int(np.argmax(W[seg]))
    lead_steps = (tW - tL) % per                               # steps wage-peak lags employment-peak
    lead_frac = lead_steps / per                               # ∈(0,1); ~0.25 ⇒ employment leads by a quarter cycle
    return {
        "closed orbit — invariant H conserved (σ_H/|H| tiny)": (np.std(H) / abs(np.mean(H))) < 1e-3,
        "employment LEADS wage share (peaks first)": 0 < lead_frac < 0.5,
        "lead ≈ quarter cycle (0.20–0.30)": 0.20 <= lead_frac <= 0.30,
        "_nums": f"period≈{per*dt:.1f}yr; employment peak@{tL}, wage peak@{tW}; lead={lead_frac:.3f} of a cycle; σ_H/H={np.std(H)/abs(np.mean(H)):.2e}",
    }


def keen_features():
    p = GKParams(keen=True, r=0.03, delta=0.03, ksharp=30.0, kmax=0.45, kmid=0.15)
    eq = keen_good_equilibrium(p)
    s = np.array([0.8, 0.9, 9.0]); broke = False
    dmax = s[2]; wmin = s[0]; lmin = s[1]
    for i in range(10000):
        s = gk_step(s, p)
        if not np.all(np.isfinite(s)) or s[0] <= 1e-3 or abs(s[2]) > 1e3:
            broke = True; break
        dmax = max(dmax, s[2]); wmin = min(wmin, s[0]); lmin = min(lmin, s[1])
    return {
        "good (finite-debt) equilibrium exists": eq is not None,
        "over-basin start → debt-deflation collapse (d↑, ω↓, λ↓)": (broke and dmax > 9.0 and wmin < 0.1 and lmin < 0.3),
        "_nums": f"eq={None if eq is None else [round(x,3) for x in eq]}; collapsed={broke} at step {i}; dmax={dmax:.1f} ωmin={wmin:.3f} λmin={lmin:.3f}",
    }


def main():
    blocks = [
        ("1. Lucas / RBC — response to a TFP shock", rbc_features()),
        ("2. Mankiw / NK — DEMAND shock", nk_demand_features()),
        ("3. Mankiw / NK — COST-PUSH (supply) shock", nk_costpush_features()),
        ("4. Goodwin — growth cycle", goodwin_features()),
        ("5. Keen — debt-deflation", keen_features()),
    ]
    allpass = True
    for title, feats in blocks:
        print(f"\n{title}")
        nums = feats.pop("_nums", "")
        for name, ok in feats.items():
            allpass = allpass and ok
            print(f"   [{'✓' if ok else '✗'}] {name}")
        if nums:
            print(f"       ({nums})")
    print("\n" + ("ALL FEATURES MATCH THE LITERATURE SHAPES" if allpass else "SOME FEATURES DO NOT MATCH — review above"))
    return allpass


if __name__ == "__main__":
    main()
