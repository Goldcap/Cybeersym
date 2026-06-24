"""
Cybeersym — the distributional wedge (the repo's namesake).
Regressive incidence of egg inflation, computed on the VALIDATED price path
(real culls + seasonal demand + calibrated egg pricer) crossed with the REAL
income/egg-share distribution (USDA-ERS food shares + BLS CE egg lines).

Why a read-out and not the engine's households: the engine's egg budget shares are
stylised high (good for the price mechanism, wrong for distributional LEVELS). The
honest incidence = validated egg-price path x realistic Engel shares by quintile.
"""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from data.hpai_culls import DEPOP_FULL, flock_deficit_path
from data.seasonality import seasonal_factor
from data.eggs_fred import window

# --- validated egg-price path (the engine's trustworthy output) ---
P = Params(store_up=0.06, store_hi=2.5)
deficit = flock_deficit_path(DEPOP_FULL, replace_lag=12)
f = seasonal_factor(); demand = [f[k % 12] for k in range(len(deficit))]
e = run(P, warmup=24, cull_path=deficit, demand_path=demand)
labels, _ = window((2022,1),(2025,12))
midx = [(int(l[:4])-2022)*12 + (int(l[5:7])-1) for l in labels]
price_idx = (np.array(e.hist["retail"][24:24+len(deficit)]) / e.p0)[midx]   # 2021=1
egg_infl = price_idx - 1.0                                                  # fractional rise

# --- REAL distribution (after-tax income; pre-shock egg $ ~flat; both data-grounded) ---
QUINT = ["Q1 (poorest)","Q2","Q3 (middle)","Q4","Q5 (richest)"]
income   = np.array([16171, 38000, 66606, 118000, 211042])   # after-tax, ERS 2023
egg_spend= np.array([   55,    67,    79,    102,    131])    # pre-shock annual $, ~flat (staple)
food_share = np.array([32.6, 20.0, 13.5, 10.0, 8.1])         # % of income on FOOD (ERS)
egg_share = egg_spend / income * 100                          # % of income on EGGS
ratio = egg_share[0] / egg_share[-1]

# --- personal inflation contribution from eggs, by quintile, over time ---
# fixed-basket: personal_infl_tier(t) = egg_share_tier * egg_infl(t)
pers = np.outer(egg_share/100, egg_infl) * 100               # points, [tier x month]
ipk = int(egg_infl.argmax())

print("="*64); print("THE DISTRIBUTIONAL WEDGE — eggs, on the validated price path"); print("="*64)
print(f"  egg budget share by quintile (pre-shock): "
      + ", ".join(f"{s:.2f}%" for s in egg_share))
print(f"  regressive ratio Q1/Q5: {ratio:.1f}x  (poorest spend {ratio:.0f}x the income share)")
print("-"*64)
print(f"  at the validated peak ({labels[ipk]}, egg +{egg_infl[ipk]*100:.0f}%):")
for q,p in zip(QUINT, pers[:,ipk]):
    print(f"     {q:14s}: personal inflation from EGGS ALONE +{p:.2f} pts")
print(f"  wedge (Q1 - Q5): {pers[0,ipk]-pers[-1,ipk]:+.2f} pts   ratio {pers[0,ipk]/pers[-1,ipk]:.1f}x")
print("-"*64)
# scale-up: same regressive structure on the whole food basket
print("  SCALE-UP — eggs are a lead indicator. Same shock structure on the")
print("  food-at-home basket (poorest spend 33% of income on food vs 6-8% richest):")
food_pers = food_share/100 * egg_infl[ipk] * 100
print(f"     if food moved like eggs: Q1 +{food_pers[0]:.0f} pts vs Q5 +{food_pers[-1]:.0f} pts")
print("="*64)

# ---------------- chart ----------------
INK="#1e2327";ACC="#c0392b";GRN="#27ae60";BLU="#2c6fbb";MUT="#7f8c8d";GRID="#e8e6e1"
TIERCOL=["#7b1d1d","#c0392b","#d68910","#5a8f3c","#2c6fbb"]
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,"figure.facecolor":"white","axes.facecolor":"white"})
fig=plt.figure(figsize=(13,8.8)); gs=fig.add_gridspec(2,2,height_ratios=[1,1])
fig.suptitle("Cybeersym — the distributional wedge: egg inflation is regressive (validated price path × real income shares)",
             fontsize=12.5,fontweight="bold",color=INK,y=0.98)

# (a) Engel: egg & food share by quintile
a=fig.add_subplot(gs[0,0]); xq=np.arange(5)
a.bar(xq-0.2, egg_share, 0.4, color=ACC, label="eggs")
a.bar(xq+0.2, food_share, 0.4, color=MUT, alpha=0.6, label="all food (right scale)")
a.set_ylabel("egg share of income (%)",color=ACC); a.set_xticks(xq); a.set_xticklabels(["Q1","Q2","Q3","Q4","Q5"])
a2=a.twinx(); a2.set_ylabel("food share of income (%)",color=MUT); a2.set_ylim(0,38)
a.set_title(f"Engel curves — poorest spend {ratio:.0f}× the egg income-share of richest",fontweight="bold",fontsize=9.5)
a.legend(frameon=False,fontsize=8,loc="upper right"); a.grid(True,color=GRID,lw=0.7,axis="y"); a.set_axisbelow(True)

# (b) personal inflation from eggs by quintile, over validated path
b=fig.add_subplot(gs[0,1]); x=np.arange(len(labels))
for k in range(5):
    b.plot(x, pers[k], color=TIERCOL[k], lw=2 if k in (0,4) else 1.2, label=QUINT[k])
b.set_ylabel("personal inflation from eggs (pts)"); b.set_xticks(x[::4]); b.set_xticklabels([labels[i] for i in x[::4]],fontsize=7,rotation=45)
b.set_title("the wedge opens during BOTH validated shocks",fontweight="bold",fontsize=9.5)
b.legend(frameon=False,fontsize=7.5,loc="upper left"); b.grid(True,color=GRID,lw=0.7); b.set_axisbelow(True)

# (c) peak wedge bars
c=fig.add_subplot(gs[1,0])
c.bar(xq, pers[:,ipk], color=TIERCOL)
c.set_ylabel("personal inflation, eggs (pts)"); c.set_xticks(xq); c.set_xticklabels(["Q1","Q2","Q3","Q4","Q5"])
c.set_title(f"At peak ({labels[ipk]}): poorest +{pers[0,ipk]:.2f} pts vs richest +{pers[-1,ipk]:.2f} pts from eggs alone",fontweight="bold",fontsize=9)
c.grid(True,color=GRID,lw=0.7,axis="y"); c.set_axisbelow(True)

# (d) scale-up to food basket
d=fig.add_subplot(gs[1,1])
d.bar(xq-0.2, pers[:,ipk], 0.4, color=ACC, label="eggs alone")
d.bar(xq+0.2, food_pers, 0.4, color=INK, alpha=0.7, label="if whole food basket moved like eggs")
d.set_ylabel("personal inflation (pts)"); d.set_xticks(xq); d.set_xticklabels(["Q1","Q2","Q3","Q4","Q5"])
d.set_title("eggs are the lead indicator; the basket is where it bites",fontweight="bold",fontsize=9)
d.legend(frameon=False,fontsize=8); d.grid(True,color=GRID,lw=0.7,axis="y"); d.set_axisbelow(True)

plt.tight_layout(rect=[0,0,1,0.95]); plt.savefig("cybeersym_v08_wedge.png",dpi=140,bbox_inches="tight")
print("chart saved")
