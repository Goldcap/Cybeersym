import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from v00_eggs_demo import run, TIERS

econ = run(shock_t=80, shock_len=15, shock_frac=0.35, total=200)  # moderate, plausible cull
h = econ.hist
t = np.array(h["t"])
sb0, sb1 = 80, 95  # shock band

INK="#1e2327"; ACC="#c0392b"; MUT="#7f8c8d"; GRID="#e8e6e1"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                     "figure.facecolor":"white","axes.facecolor":"white"})

fig, ax = plt.subplots(2, 2, figsize=(13, 8))
fig.suptitle("Cybeersym v0 — eggs: a supply shock, told four ways",
             fontsize=14, fontweight="bold", color=INK, y=0.98)

def band(a):
    a.axvspan(sb0, sb1, color=ACC, alpha=0.08, lw=0)
    a.grid(True, color=GRID, lw=0.7); a.set_axisbelow(True)

# (1) prices
a=ax[0,0]; band(a)
a.plot(t, h["retail"], color=ACC, lw=2, label="retail price")
a.plot(t, h["replacement"], color=INK, lw=1.3, ls="--", label="replacement (supplier) cost")
a.set_title("Price: sticky markup over replacement", fontweight="bold")
a.set_ylabel("money / egg"); a.legend(frameon=False, fontsize=9)
a.annotate("avian-flu\ncull", (87.5, a.get_ylim()[1]*0.92), ha="center",
           fontsize=8, color=ACC)

# (2) the wedge — personal inflation by tier
a=ax[0,1]; band(a)
infl = lambda key: (np.array(h[key])-1)*100
a.plot(t, infl("cpi_t0"), color=ACC, lw=2.2, label="bottom quintile")
a.plot(t, infl("cpi_agg"), color=INK, lw=1.6, label="aggregate CPI")
a.plot(t, infl(f"cpi_t{TIERS-1}"), color=MUT, lw=1.6, ls="--", label="top quintile")
a.set_title("The wedge: who actually pays", fontweight="bold")
a.set_ylabel("personal inflation  (%)"); a.legend(frameon=False, fontsize=9)
a.axhline(0, color=INK, lw=0.6)

# (3) physical shortage
a=ax[1,0]; band(a)
a.plot(t, h["store_inv"], color=INK, lw=1.6, label="store inventory (eggs)")
a.plot(t, h["supp_inv"], color="#8e44ad", lw=1.3, label="supplier stock")
a.set_title("Physical: inventory drains, lead time bites", fontweight="bold")
a.set_ylabel("eggs"); a.set_xlabel("tick"); a.legend(frameon=False, fontsize=9)
a2=a.twinx()
a2.plot(t, np.array(h["served_frac"])*100, color=ACC, lw=1.2, alpha=0.8)
a2.set_ylabel("% of demand served", color=ACC); a2.tick_params(axis="y", colors=ACC)
a2.set_ylim(0,105)

# (4) the plumbing proof
a=ax[1,1]; band(a)
a.plot(t, np.abs(h["money_resid"]), color=INK, lw=1.4, label="|money residual|")
a.plot(t, np.abs(h["egg_resid"]), color="#27ae60", lw=1.4, label="|egg residual|")
a.set_yscale("log"); a.set_ylim(1e-14, 1e-6)
a.axhline(1e-6, color=ACC, ls=":", lw=1)
a.set_title("Godley check: conservation holds (log scale)", fontweight="bold")
a.set_ylabel("residual"); a.set_xlabel("tick"); a.legend(frameon=False, fontsize=9)
a.annotate("assert threshold 1e-6", (60, 1.4e-6), color=ACC, fontsize=8)

plt.tight_layout(rect=[0,0,1,0.96])
plt.savefig("cybeersym_v0_eggs.png", dpi=140, bbox_inches="tight")

# headline numbers for this moderate run
base_p=econ._p0; peak_i=int(np.argmax(h["retail"]))
print(f"moderate cull (35%): pre {base_p:.2f} -> peak {max(h['retail']):.2f} "
      f"(+{(max(h['retail'])/base_p-1)*100:.0f}%);  "
      f"bottom {(h['cpi_t0'][peak_i]-1)*100:.0f}% vs top "
      f"{(h[f'cpi_t{TIERS-1}'][peak_i]-1)*100:.0f}% vs agg "
      f"{(h['cpi_agg'][peak_i]-1)*100:.0f}%;  "
      f"min served {min(h['served_frac'])*100:.0f}%")
print("saved cybeersym_v0_eggs.png")
