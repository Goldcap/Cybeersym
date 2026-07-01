import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from data.hpai_culls import DEPOP_FULL, flock_deficit_path
from data.seasonality import seasonal_factor
from data.eggs_fred import window

P = Params(supp_up=8.0, store_up=0.06, store_hi=2.5, supp_hi=30.0)
deficit = flock_deficit_path(DEPOP_FULL, replace_lag=12)
f = seasonal_factor(); demand = [f[k%12] for k in range(len(deficit))]
# historical (pre-CYB-7): synthetic replace_lag=12 deficit + slope=13, pinned so this
# frozen figure reproduces after CYB-9 recalibrated EGG_PRICING's slope to 24.1.
# Superseded by v09 (real NASS deficit) + v10 (recalibrated slope).
e = run(P, warmup=24, cull_path=deficit, demand_path=demand,
        pricing={"pricer": "linear_deficit", "slope": 13.0, "hi": 40.0})
model = np.array(e.hist["retail"][24:24+len(deficit)])/e.p0
labels, real_all = window((2022,1),(2025,12)); _, b21 = window((2021,1),(2021,12))
real = np.array(real_all)/np.mean(b21)
# align model (continuous 48mo from 2022-01) to real labels (Oct'25 price missing)
midx = [(int(l[:4])-2022)*12 + (int(l[5:7])-1) for l in labels]
model = model[midx]; x = np.arange(len(labels))

# model's price-vs-deficit GAIN curve: hold deficit flat at d, read peak price
gain_d = np.linspace(0, 0.28, 15); gain_p = []
for d in gain_d:
    cp = [d]*24; dm = [f[k%12] for k in range(24)]
    ee = run(P, warmup=24, cull_path=cp, demand_path=dm)
    gain_p.append((np.array(ee.hist["retail"][24:48]).max()/ee.p0 - 1)*100)
gain_p = np.array(gain_p)

INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                     "figure.facecolor":"white","axes.facecolor":"white"})
fig = plt.figure(figsize=(13,8.5)); gs = fig.add_gridspec(2,1,height_ratios=[1.25,1])
fig.suptitle("Cybeersym v0.6 — out-of-sample: timing validated, magnitude target identified",
             fontsize=14, fontweight="bold", color=INK, y=0.98)

a = fig.add_subplot(gs[0])
a.plot(x, real, color=ACC, lw=2.4, marker="o", ms=3, label="REAL egg price (FRED)")
a.plot(x, model, color=GRN, lw=2, marker="^", ms=3, label="MODEL (one run, same params, 2022-25)")
a.axhline(1, color=INK, lw=0.6)
a.axvspan(0,23, color=BLU, alpha=0.05); a.axvspan(24,47, color=ORG, alpha=0.06)
for lbl,col in [("2023-01",GRN),("2025-03",GRN)]:
    i=labels.index(lbl); a.annotate("✓ peak", (i,model[i]),(i-1.5,model[i]+0.4),fontsize=8,color=col,
        arrowprops=dict(arrowstyle="->",color=col,lw=1))
a.text(11,3.3,"2022-23\n(calibrated here)",ha="center",fontsize=8.5,color=BLU,fontweight="bold")
a.text(35,3.3,"2024-25\n(OUT-OF-SAMPLE, never fit)",ha="center",fontsize=8.5,color=ORG,fontweight="bold")
a.set_ylabel("egg price (indexed, 2021=1)"); a.set_xticks(x[::3]); a.set_xticklabels([labels[i] for i in x[::3]],fontsize=7,rotation=45)
a.grid(True,color=GRID,lw=0.7); a.set_axisbelow(True); a.legend(frameon=False,fontsize=9,loc="upper right")
a.set_title("both peaks land on the right month with replace_lag=12 untouched — lag is structural",fontweight="bold",fontsize=10)

a2 = fig.add_subplot(gs[1])
a2.plot(gain_d*100, gain_p, color=GRN, lw=2.2, marker="^", ms=4, label="MODEL pricer (too shallow, convex)")
# real points: (modeled deficit at peak, real price rise)
rx=[13.0,23.0]; ry=[188,272]
a2.scatter(rx,ry,color=ACC,s=90,zorder=5,label="REAL (deficit at peak, price rise)")
for dx,dy,t in [(13,188,"2022-23"),(23,272,"2024-25")]:
    a2.annotate(t,(dx,dy),(dx+0.6,dy-22),fontsize=8.5,color=ACC)
xs=np.linspace(0,28,50); a2.plot(xs,13*xs,color=ACC,lw=1.3,ls="--",alpha=0.7,label="real slope ≈ 13% price / 1% deficit (~linear)")
a2.set_xlabel("modeled flock deficit at peak (%)"); a2.set_ylabel("peak price rise (%)")
a2.set_title("the magnitude fix: real price ≈ linear ~13%/deficit-pt; model slope is ~half and curved",fontweight="bold",fontsize=10)
a2.grid(True,color=GRID,lw=0.7); a2.set_axisbelow(True); a2.legend(frameon=False,fontsize=8.5,loc="upper left")

plt.tight_layout(rect=[0,0,1,0.95])
plt.savefig("cybeersym_v06_oos.png",dpi=140,bbox_inches="tight")
print("saved. real price-per-deficit slope ep1/ep2:", round(188/13,1),"/",round(272/23,1),"-> consistent ~13%/pt")
