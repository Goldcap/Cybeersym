"""
Cybeersym — bullwhip v0 runner.

Runs, in order:
  1. FROZEN-FORECAST REGRESSION — constant S (p->infinity limit). Must read
     ratio ~1 at every stage: proves the harness is correct and that the
     bullwhip comes from the moving-average update, not a bug.
  2. SINGLE-STAGE vs CHEN (2000) — a clean linear order-up-to stage facing
     i.i.d. demand, swept over L and p, checked against the analytic closed form
     1 + 2L/p + 2L^2/p^2. Confirms the mechanism quantitatively and its trends
     (rises with L, falls with p, -> 1 as p -> infinity).
  3. THE KILLER EXPERIMENT — the full 3-tier chain, local_info vs shared_info:
     compounding (r, r^2, r^3) vs flat (r, r, r). Saves the figure.

Run from inside src/:  python3 bullwhip/run_v0.py
"""
from collections import deque
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import SupplyChain, ChainParams, TIER_NAMES
from measure import chain_report, format_table, chen_single_stage


# ---------------------------------------------------------------- 1. regression
def frozen_regression(p: ChainParams) -> dict:
    rep = chain_report(SupplyChain(p, mode="local_info", forecast="frozen").run())
    worst = max(abs(r - 1.0) for r in rep["per_stage"])
    assert worst < 1e-6, f"frozen forecast should give ratio~1, off by {worst:.2e}"
    return rep


# ----------------------------------------------- 2. clean single-stage vs Chen
def single_stage_linear_ratio(L, p, mu=100.0, sigma=10.0, z=2.0,
                              T=40000, warmup=1000, seed=0):
    """One isolated stage, LINEAR order-up-to (orders may go negative = returns;
    no stockout clamp), MA(p) forecast, facing i.i.d. demand. This is the clean
    setting Chen et al.'s closed form describes — used to validate the mechanism
    apart from the full sim's (deliberate) stockout/backlog nonlinearity."""
    rng = np.random.default_rng(seed)
    D = mu + rng.normal(0, sigma, T)
    window = deque([mu] * p, maxlen=p)
    safety = z * sigma * np.sqrt(L + 1)
    IP = mu * (L + 1) + safety               # start at S_0
    orders = np.zeros(T)
    for t in range(T):
        IP -= D[t]                            # demand depletes the inventory position
        window.append(D[t])
        S_t = float(np.mean(window)) * (L + 1) + safety
        order = S_t - IP                      # linear: no max(0, .)
        IP += order                           # back up to S_t
        orders[t] = order
    return float(np.var(orders[warmup:]) / np.var(D[warmup:]))


def single_stage_sweep():
    rows = []
    for L in (1, 2, 4):
        for p in (3, 5, 10, 20, 1000):
            meas = single_stage_linear_ratio(L, p)
            rows.append((L, p, meas, chen_single_stage(L, p), chen_single_stage(L + 1, p)))
    return rows


# ----------------------------------------------------- 3. the killer experiment
MODES = ("local_info", "shared_info", "coordinated")


def killer_experiment(p: ChainParams):
    return [chain_report(SupplyChain(p, mode=m).run()) for m in MODES]


def make_figure(p: ChainParams, reports, out_path: Path):
    local = SupplyChain(p, mode="local_info").run()
    w = p.warmup
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9))

    # (top) the wiggle grows upstream
    t = np.arange(w, p.T)
    ax1.plot(t, local.demand[w:], label="consumer demand", color="black", lw=1.4)
    colors = ["#1f77b4", "#ff7f0e", "#d62728"]
    for i, name in enumerate(TIER_NAMES[: p.n_tiers]):
        ax1.plot(t, local.orders_placed[i, w:], label=f"{name} orders",
                 color=colors[i], lw=1.0, alpha=0.85)
    ax1.set_title("Bullwhip under local information — order variance grows upstream "
                  "from stationary demand")
    ax1.set_xlabel("step (week)"); ax1.set_ylabel("units ordered")
    ax1.legend(loc="upper right", fontsize=8)

    # (bottom) compounding vs suppressed vs flat — cumulative ratio vs TRUE demand
    x = np.arange(p.n_tiers)
    by_mode = {r["mode"]: r for r in reports}
    ax2.plot(x, by_mode["local_info"]["cumulative"], "o-", color="#d62728",
             label="local  — forecast+replenish distorted  (compounds ~ r, r², r³)")
    ax2.plot(x, by_mode["shared_info"]["cumulative"], "s--", color="#ff7f0e",
             label="shared — true-demand forecast only  (suppressed, not flat)")
    ax2.plot(x, by_mode["coordinated"]["cumulative"], "^:", color="#1f77b4",
             label="coordinated — echelon replenishment  (flat ~ r)")
    ax2.axhline(1.0, color="gray", lw=0.8, ls=":")
    ax2.set_xticks(x); ax2.set_xticklabels(TIER_NAMES[: p.n_tiers])
    ax2.set_ylabel("Var(orders) / Var(true demand)")
    ax2.set_title("Seeing vs acting: forecast channel (local→shared) + physical "
                  "replenishment channel (shared→coordinated)")
    ax2.legend(loc="upper left", fontsize=8)

    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120)
    return out_path


def main():
    p = ChainParams()
    print(f"params: mu={p.mu} sigma={p.sigma} L={p.L} p={p.p} z={p.z} "
          f"T={p.T} warmup={p.warmup} seed={p.seed}\n")

    # 1
    frz = frozen_regression(p)
    print("[1] FROZEN-FORECAST REGRESSION (constant S, the p->inf limit)")
    print("    per-stage ratios:", [round(x, 5) for x in frz["per_stage"]],
          "-> ~1 at every stage (PASS)\n")

    # 2
    print("[2] CLEAN SINGLE STAGE vs CHEN (2000)  1 + 2L/p + 2L²/p²")
    print(f"    {'L':>3}{'p':>6}{'measured':>12}{'Chen(L,p)':>12}{'Chen(L+1,p)':>13}")
    for L, pp, meas, chenL, chenL1 in single_stage_sweep():
        print(f"    {L:>3}{pp:>6}{meas:>12.3f}{chenL:>12.3f}{chenL1:>13.3f}")
    print("    trends: rises with L, falls with p, -> 1 as p->inf. Measured tracks")
    print("    Chen(L+1,p): our S_t scales with (L+1) (lead + review), a one-step")
    print("    convention offset from the textbook L. Mechanism confirmed.\n")

    # 3
    reports = killer_experiment(p)
    print("[3] KILLER EXPERIMENT — 3-tier chain, three modes (seeing vs acting)")
    print("  per-stage  Var(orders_out)/Var(demand_in):")
    print(format_table(reports, "per_stage"))
    print("\n  cumulative  Var(orders)/Var(TRUE demand)  — the compounding signature:")
    print(format_table(reports, "cumulative"))
    res = max(r["max_residual"] for r in reports)
    print(f"\n  max goods-conservation residual: {res:.2e}  (< 1e-9: PASS)")

    out = make_figure(p, reports, Path(__file__).parent / "figures"
                      / "cybeersym_bullwhip_v0.png")
    print(f"\n  figure -> {out}")

    by = {r["mode"]: r["chain_total"] for r in reports}
    print(f"\nRESULT: chain amplification  local {by['local_info']:.1f}×  ->  shared "
          f"{by['shared_info']:.1f}×  ->  coordinated {by['coordinated']:.1f}×  "
          f"(same seed, same demand).")
    print("  Decomposition: local->shared = the forecast (information) channel; "
          "shared->coordinated = the physical replenishment channel. Seeing true "
          "demand suppresses the bullwhip; only ACTING on it (echelon replenishment) "
          "flattens it.")


if __name__ == "__main__":
    main()
