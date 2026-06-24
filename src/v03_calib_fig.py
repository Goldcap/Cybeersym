import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from v03_calibrate import SHAPE, r_idx, labels, real_base

# best v0.2 fit: cost-pass-through-dominant (commodity) pricing
P = Params(store_up=0.10, store_down=0.10, store_hi=2.0,
           supp_up=0.70, supp_hi=12.0)
DEPTH = 0.75
e = run(P, warmup=24, cull_path=list(DEPTH*SHAPE))
m = np.array(e.hist["retail"][24:24+24]) / e.p0
served = np.array(e.hist["served"][24:24+24])
mr = [abs(v) for v in e.hist["money_resid"][24:24+24]]; er = [abs(v) for v in e.hist["egg_resid"][24:24+24]]
corr = np.corrcoef(m, r_idx)[0,1]; rmse = np.sqrt(np.mean((m-r_idx)**2))
x = np.arange(len(r_idx))

INK="#1e2327"; ACC="#c0392b"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                     "figure.facecolor":"white","axes.facecolor":"white"})
fig = plt.figure(figsize=(13, 8))
gs = fig.add_gridspec(2, 2, height_ratios=[1.5,1])
fig.suptitle("Cybeersym v0.3 — model vs reality: proportional cost-pass-through",
             fontsize=14, fontweight="bold", color=INK, y=0.98)

# main overlay
a = fig.add_subplot(gs[0,:])
a.plot(x, r_idx, color=ACC, lw=2.4, marker="o", ms=4, label="REAL  (FRED APU0000708111)")
a.plot(x, m, color=BLU, lw=2.0, marker="s", ms=3, label="MODEL (cost-pass-through fit)")
a.axhline(1, color=INK, lw=0.6)
a.set_xticks(x[::3]); a.set_xticklabels([labels[i] for i in x[::3]], rotation=0, fontsize=8)
a.set_ylabel("egg price  (indexed, 2021 = 1.0)")
a.grid(True, color=GRID, lw=0.7); a.set_axisbelow(True)
a.legend(frameon=False, fontsize=10, loc="upper right")
a.set_title(f"2022-23 avian-flu shock   |   corr = {corr:+.2f},  RMSE = {rmse:.2f},  "
            f"peak model +{(m.max()-1)*100:.0f}% vs real +{(r_idx.max()-1)*100:.0f}%",
            fontweight="bold", fontsize=10)
a.annotate("real rises GRADUALLY from Apr'22\n(multi-wave culls priced in early)",
           (4, 1.55), (1, 2.6), fontsize=8, color=ACC,
           arrowprops=dict(arrowstyle="->", color=ACC, lw=1))
a.annotate("model stays FLAT then spikes\n(price only moves at stockout —\nthe deadzone the data exposes)",
           (10, 1.05), (12.5, 1.35), fontsize=8, color=BLU,
           arrowprops=dict(arrowstyle="->", color=BLU, lw=1))

# input cull path
a2 = fig.add_subplot(gs[1,0])
a2.fill_between(x, DEPTH*SHAPE*100, color=MUT, alpha=0.5)
a2.plot(x, DEPTH*SHAPE*100, color=INK, lw=1.4)
a2.set_title("Input: stylised multi-wave cull path", fontweight="bold", fontsize=10)
a2.set_ylabel("% capacity lost"); a2.set_xticks(x[::4]); a2.set_xticklabels([labels[i] for i in x[::4]], fontsize=8)
a2.grid(True, color=GRID, lw=0.7); a2.set_axisbelow(True)
a2.annotate("(shape stylised, not yet\nreal monthly flock-loss data)", (12,70), fontsize=7.5, color=MUT)

# conservation
a3 = fig.add_subplot(gs[1,1])
a3.plot(x, mr, color=INK, lw=1.3, label="|money residual|")
a3.plot(x, er, color="#27ae60", lw=1.3, label="|egg residual|")
a3.set_yscale("log"); a3.set_ylim(1e-14,1e-6); a3.axhline(1e-6, color=ACC, ls=":", lw=1)
a3.set_title("Godley check: still airtight", fontweight="bold", fontsize=10)
a3.set_xticks(x[::4]); a3.set_xticklabels([labels[i] for i in x[::4]], fontsize=8)
a3.legend(frameon=False, fontsize=8); a3.grid(True, color=GRID, lw=0.7, which="both", alpha=0.4)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("cybeersym_v03_calibration.png", dpi=140, bbox_inches="tight")
print(f"corr {corr:+.3f}  rmse {rmse:.3f}  peak model {m.max():.2f} real {r_idx.max():.2f}")
print("saved cybeersym_v03_calibration.png")
