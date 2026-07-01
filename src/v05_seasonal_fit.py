import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from data.hpai_culls import flock_deficit_path, DEPOP
from data.seasonality import seasonal_factor
from data.eggs_fred import window

labels, real = window((2022,1),(2023,12)); _, base = window((2021,1),(2021,12))
r = np.array(real)/np.mean(base); x = np.arange(24)
f = seasonal_factor(); demand_path = [f[k%12] for k in range(24)]
deficit6  = flock_deficit_path(replace_lag=6)    # naive: recovers too fast
deficit12 = flock_deficit_path(replace_lag=12)   # data-plausible effective lag

# data-foundational model: real culls + seasonal demand + 12mo effective lag
# historical (pre-CYB-7): synthetic-deficit path + slope=13 (the compensating-error
# pair, superseded by the real-data pipeline v09/v10). Pinned so this frozen figure
# still reproduces after EGG_PRICING's slope was recalibrated to 24.1 in CYB-9.
e = run(Params(supp_up=8.0, store_up=0.06, store_hi=2.5, supp_hi=30.0),
        warmup=24, cull_path=deficit12, demand_path=demand_path,
        pricing={"pricer": "linear_deficit", "slope": 13.0, "hi": 40.0})
m = np.array(e.hist["retail"][24:48])/e.p0
corr = np.corrcoef(m, r)[0,1]

INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                     "figure.facecolor":"white","axes.facecolor":"white"})
fig = plt.figure(figsize=(13,8.5)); gs = fig.add_gridspec(2,2,height_ratios=[1.5,1])
fig.suptitle("Cybeersym v0.5 — timing solved from real data (real culls + seasonal demand)",
             fontsize=14, fontweight="bold", color=INK, y=0.985)

a = fig.add_subplot(gs[0,:])
a.plot(x, r, color=ACC, lw=2.6, marker="o", ms=4, label="REAL egg price (FRED)")
a.plot(x, m, color=GRN, lw=2.2, marker="^", ms=4,
       label=f"MODEL: real culls + seasonal demand + 12-mo lag  (corr {corr:+.2f})")
a.axhline(1, color=INK, lw=0.6); a.set_ylabel("egg price (indexed, 2021=1)")
a.set_xticks(x[::3]); a.set_xticklabels([labels[i] for i in x[::3]], fontsize=8)
a.grid(True, color=GRID, lw=0.7); a.set_axisbelow(True); a.legend(frameon=False, fontsize=9.5, loc="upper left")
a.set_title("peak now lands JAN 2023 from real inputs — but magnitude still undershoots (convexity)",
            fontweight="bold", fontsize=10)
a.annotate("TIMING fixed:\nreal Jan peak,\nmodel Jan peak", (12, 1.4), (14.5, 1.9),
           fontsize=8.5, color=GRN, arrowprops=dict(arrowstyle="->", color=GRN, lw=1))
a.annotate("MAGNITUDE gap:\nmodel +%.0f%% vs real +188%%\n= convexity (next)" % ((m.max()-1)*100),
           (12, 2.88), (8.5, 2.5), fontsize=8.5, color=ACC, arrowprops=dict(arrowstyle="->", color=ACC, lw=1))

a2 = fig.add_subplot(gs[1,0])
a2.plot(x, np.array(deficit6)*100, color=MUT, lw=1.5, ls="--", label="flock deficit, 6-mo lag (recovers too fast)")
a2.plot(x, np.array(deficit12)*100, color=GRN, lw=2, label="flock deficit, 12-mo lag (holds into winter)")
a2.bar(x, [v for _,_,v in DEPOP], color=MUT, alpha=0.35, width=0.6, label="monthly cull (M birds)")
a2.set_title("Real supply: deficit holds into winter with the true effective lag",
             fontweight="bold", fontsize=10)
a2.set_ylabel("% capacity lost / M birds"); a2.set_xticks(x[::4]); a2.set_xticklabels([labels[i] for i in x[::4]], fontsize=8)
a2.legend(frameon=False, fontsize=7.5); a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True)

a3 = fig.add_subplot(gs[1,1])
months=["J","F","M","A","M","J","J","A","S","O","N","D"]
colors=[GRN if v>=1 else MUT for v in f]
a3.bar(range(12), (f-1)*100, color=colors, alpha=0.8)
a3.axhline(0, color=INK, lw=0.6); a3.set_xticks(range(12)); a3.set_xticklabels(months, fontsize=8)
a3.set_title("Seasonal demand factor (from calm-year prices)", fontweight="bold", fontsize=10)
a3.set_ylabel("% vs annual mean"); a3.grid(True, color=GRID, lw=0.7, axis="y"); a3.set_axisbelow(True)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("cybeersym_v05_seasonal.png", dpi=140, bbox_inches="tight")
print(f"corr {corr:+.3f}  model peak {labels[int(m.argmax())]} ({m.max():.2f})  real peak {labels[int(r.argmax())]} ({r.max():.2f})")
