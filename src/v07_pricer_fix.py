import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from data.hpai_culls import DEPOP_FULL, flock_deficit_path
from data.seasonality import seasonal_factor
from data.eggs_fred import window

P = Params(store_up=0.06, store_hi=2.5)
deficit = flock_deficit_path(DEPOP_FULL, replace_lag=12)
f = seasonal_factor(); demand=[f[k%12] for k in range(len(deficit))]
labels, real_all = window((2022,1),(2025,12)); _, b21=window((2021,1),(2021,12))
real=np.array(real_all)/np.mean(b21)
midx=[(int(l[:4])-2022)*12+(int(l[5:7])-1) for l in labels]

# OLD (v0.6 convex flow_gap pricer) vs NEW (linear egg pricer, single slope)
e_old=run(P,warmup=24,cull_path=deficit,demand_path=demand,
          pricing={"pricer":"proportional_flowgap","slope":8.0,"hi":40.0})
m_old=(np.array(e_old.hist["retail"][24:24+len(deficit)])/e_old.p0)[midx]
# historical (pre-CYB-7): pinned to slope=13 (was the EGG_PRICING default) so this frozen
# figure reproduces after CYB-9 recalibrated EGG_PRICING to 24.1. Superseded by v09/v10.
e_new=run(P,warmup=24,cull_path=deficit,demand_path=demand,
          pricing={"pricer":"linear_deficit","slope":13.0,"hi":40.0})
m_new=(np.array(e_new.hist["retail"][24:24+len(deficit)])/e_new.p0)[midx]
x=np.arange(len(labels))

INK="#1e2327";ACC="#c0392b";GRN="#27ae60";BLU="#2c6fbb";MUT="#7f8c8d";GRID="#e8e6e1"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,"figure.facecolor":"white","axes.facecolor":"white"})
fig=plt.figure(figsize=(13,8.5)); gs=fig.add_gridspec(2,1,height_ratios=[1.3,1])
fig.suptitle("Cybeersym v0.7 — egg pricer is now a commodity property (linear slope, both episodes lift together)",
             fontsize=13.5,fontweight="bold",color=INK,y=0.98)

a=fig.add_subplot(gs[0])
a.plot(x,real,color=ACC,lw=2.4,marker="o",ms=3,label="REAL egg price")
a.plot(x,m_new,color=GRN,lw=2,marker="^",ms=3,label="NEW linear egg pricer (slope=13, one commodity property)")
a.plot(x,m_old,color=MUT,lw=1.4,ls=":",label="OLD convex flow_gap pricer (v0.6)")
a.axhline(1,color=INK,lw=0.6)
for lbl in ["2023-01","2025-03"]:
    i=labels.index(lbl); a.annotate("✓",(i,m_new[i]),(i,m_new[i]+0.25),fontsize=12,color=GRN,ha="center")
a.set_ylabel("egg price (indexed, 2021=1)"); a.set_xticks(x[::3]); a.set_xticklabels([labels[i] for i in x[::3]],fontsize=7,rotation=45)
a.grid(True,color=GRID,lw=0.7); a.set_axisbelow(True); a.legend(frameon=False,fontsize=9,loc="upper left")
a.set_title("both peaks lifted toward real magnitude by ONE egg slope — timing unchanged",fontweight="bold",fontsize=10)

# gain curves: old convex vs new linear vs real points
a2=fig.add_subplot(gs[1])
dd=np.linspace(0,0.28,15)
def gain(pricing):
    g=[]
    for d in dd:
        ee=run(P,warmup=24,cull_path=[d]*24,demand_path=[f[k%12] for k in range(24)],pricing=pricing)
        g.append((np.array(ee.hist["retail"][24:48]).max()/ee.p0-1)*100)
    return np.array(g)
a2.plot(dd*100,gain({"pricer":"proportional_flowgap","slope":8.0,"hi":40}),color=MUT,lw=1.6,ls=":",label="old: convex (flow_gap)")
a2.plot(dd*100,gain({"pricer":"linear_deficit","slope":13.0,"hi":40}),color=GRN,lw=2.2,marker="^",ms=3,label="new: linear in deficit (slope=13)")
a2.scatter([13,23],[188,272],color=ACC,s=90,zorder=5,label="REAL")
for dx,dy,t in [(13,188,"2022-23"),(23,272,"2024-25")]: a2.annotate(t,(dx,dy),(dx-2.5,dy+18),fontsize=8.5,color=ACC)
xs=np.linspace(0,28,40); a2.plot(xs,13*xs,color=ACC,lw=1,ls="--",alpha=0.6,label="13%/pt target")
# saturation hint
a2.plot(xs,34.6*np.power(np.clip(xs,0,None),0.65),color=BLU,lw=1.3,ls="-.",alpha=0.7,label="real saturating fit (deficit^0.65)")
a2.set_xlabel("flock deficit at peak (%)"); a2.set_ylabel("peak price rise (%)")
a2.set_title("linear matches the target slope; real data mildly SATURATES at deep deficits (imports + demand destruction)",fontweight="bold",fontsize=9.5)
a2.grid(True,color=GRID,lw=0.7); a2.set_axisbelow(True); a2.legend(frameon=False,fontsize=8,loc="upper left")

plt.tight_layout(rect=[0,0,1,0.95]); plt.savefig("cybeersym_v07_pricer.png",dpi=140,bbox_inches="tight")

def pk(m,lo,hi):
    idx=[i for i,l in enumerate(labels) if lo<=l<=hi]; return (m[idx].max()-1)*100,labels[idx[m[idx].argmax()]]
print("            ep1(2022-23)        ep2(2024-25)")
for nm,m in [("REAL",real),("NEW linear",m_new),("OLD convex",m_old)]:
    p1,k1=pk(m,"2022-01","2023-12"); p2,k2=pk(m,"2024-01","2025-12")
    print(f" {nm:11s} +{p1:3.0f}% {k1}   +{p2:3.0f}% {k2}")
print("conservation leak:", f'{max(max(abs(x) for x in e_new.hist["money_resid"]),max(abs(x) for x in e_new.hist["egg_resid"])):.0e}')
