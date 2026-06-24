import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from data.hpai_culls import flock_deficit_path, DEPOP
from data.eggs_fred import window
from v03_calibrate import SHAPE   # the stylised bump

labels, real = window((2022,1),(2023,12)); _, base = window((2021,1),(2021,12))
r = np.array(real)/np.mean(base); x = np.arange(24)

# (1) old "fit": stylised bump shaped to match
e1 = run(Params(store_up=0.10, store_hi=2.0, supp_up=0.70, supp_hi=12.0),
         warmup=24, cull_path=list(0.75*SHAPE))
m_styl = np.array(e1.hist["retail"][24:48])/e1.p0
# (2) honest: real flock-deficit path
deficit = flock_deficit_path()
e2 = run(Params(store_up=0.06, store_hi=2.0, supp_up=4.0, supp_hi=20.0),
         warmup=24, cull_path=deficit)
m_real = np.array(e2.hist["retail"][24:48])/e2.p0

INK="#1e2327"; ACC="#c0392b"; BLU="#2c6fbb"; GRN="#27ae60"; MUT="#7f8c8d"; GRID="#e8e6e1"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                     "figure.facecolor":"white","axes.facecolor":"white"})
fig = plt.figure(figsize=(13,8.5)); gs = fig.add_gridspec(2,2,height_ratios=[1.5,1])
fig.suptitle("Cybeersym v0.4 — real flock data refutes the stylised fit (and that's the point)",
             fontsize=14, fontweight="bold", color=INK, y=0.985)

a = fig.add_subplot(gs[0,:])
a.plot(x, r, color=ACC, lw=2.6, marker="o", ms=4, label="REAL egg price (FRED)")
a.plot(x, m_styl, color=BLU, lw=2, ls="--", marker="s", ms=3,
       label="model w/ STYLISED bump (corr 0.86 — but input was shaped to fit)")
a.plot(x, m_real, color=GRN, lw=2.2, marker="^", ms=4,
       label="model w/ REAL flock data (corr ~0 — honest, and wrong)")
a.axhline(1, color=INK, lw=0.6); a.set_ylabel("egg price (indexed, 2021=1)")
a.set_xticks(x[::3]); a.set_xticklabels([labels[i] for i in x[::3]], fontsize=8)
a.grid(True, color=GRID, lw=0.7); a.set_axisbelow(True); a.legend(frameon=False, fontsize=9, loc="upper left")
a.set_title("the stylised input faked the timing & magnitude the real input can't produce",
            fontweight="bold", fontsize=10)
a.annotate("real price peaks JAN\n(winter — every year)", (12,2.88), (14,2.5),
           fontsize=8, color=ACC, arrowprops=dict(arrowstyle="->",color=ACC,lw=1))
a.annotate("honest model peaks JUL\n(tracks the supply deficit)\nand undershoots hugely",
           (6,1.18), (7.5,1.7), fontsize=8, color=GRN, arrowprops=dict(arrowstyle="->",color=GRN,lw=1))

# input paths
a2 = fig.add_subplot(gs[1,0])
a2.fill_between(x, 0.75*SHAPE*100, color=BLU, alpha=0.25, label="stylised bump (peak Dec, ~64%)")
a2.plot(x, 0.75*SHAPE*100, color=BLU, lw=1.5)
a2.plot(x, np.array(deficit)*100, color=GRN, lw=2, label="REAL flock deficit (peak Jul, ~9.5%)")
a2.bar(x, [v for _,_,v in DEPOP], color=MUT, alpha=0.5, width=0.6, label="monthly cull (M birds)")
a2.set_title("Input: shaped fiction vs real flock dynamics", fontweight="bold", fontsize=10)
a2.set_ylabel("% capacity lost  /  M birds"); a2.set_xticks(x[::4]); a2.set_xticklabels([labels[i] for i in x[::4]], fontsize=8)
a2.legend(frameon=False, fontsize=7.5); a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True)

# the two findings as text
a3 = fig.add_subplot(gs[1,1]); a3.axis("off")
a3.text(0, 1.0, "What the real data forces us to add:", fontweight="bold", fontsize=11, color=INK, va="top")
a3.text(0, 0.80, "① SEASONAL DEMAND.  Supply deficit peaks\n    summer '22; price peaks winter '23. Every\n    egg peak is winter (Jan'23, Mar'25),\n    independent of cull timing. Demand\n    seasonality is a first-order driver.",
        fontsize=9, color=GRN, va="top")
a3.text(0, 0.42, "② CONVEXITY.  A ~9.5% real flock deficit\n    produced +188% price. The supply→price\n    map is far more convex than a free markup\n    gives — eggs are a near-inelastic staple;\n    small shortfalls → scrambles, hoarding.",
        fontsize=9, color=ACC, va="top")
a3.text(0, 0.05, "The stylised bump hid BOTH by being shaped\nto the answer. Real data is dispositive.",
        fontsize=8.5, color=INK, va="top", style="italic")

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("cybeersym_v04_realdata.png", dpi=140, bbox_inches="tight")
print(f"stylised corr {np.corrcoef(m_styl,r)[0,1]:+.2f} peak {labels[int(m_styl.argmax())]}")
print(f"realdata corr {np.corrcoef(m_real,r)[0,1]:+.2f} peak {labels[int(m_real.argmax())]} peakidx {m_real.max():.2f}")
