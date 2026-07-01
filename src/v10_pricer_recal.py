"""
Cybeersym v0.10 — recalibrate the egg pricer slope against the REAL flock deficit (CYB-9).

Second half of CYB-7, split out to keep the replace_lag retirement honest (recalibrating
in place would have let the slope silently absorb the deficit correction). CYB-7 halved
the deficit (synthetic ~2x -> real); with the frozen v0.6 slope (~13, calibrated off the
too-large synthetic deficit) the model then undershot. Here we recalibrate the ONE
parameter — the egg pricer's price-per-deficit slope — against the real deficit, and
re-validate out-of-sample.

DISCIPLINE (the load-bearing guard): calibrate the slope on ONE episode (ep1, 2022-23),
freeze it, and validate OUT-OF-SAMPLE on the other (ep2, 2024-25). Fitting both episodes
would recover a nice number but destroy the thing that makes the egg model credible —
that frozen params reproduce an un-fit episode. Nothing else moves (timing is data-driven
and clean post-CYB-7; no new free parameters).

RESULT (honest, both ways):
  * Slope recalibrates 13 -> ~24.1 (calibrated on ep1) — independently lands on the
    ~24 %/pt CYB-7 estimated from the real deficit-price ratio. Timing unchanged (clean).
  * ep1 (in-sample): +188% by construction (matches real).
  * ep2 (OUT-OF-SAMPLE): model OVERSHOOTS (+~317% vs real +272%). A single LINEAR slope
    calibrated on the shallower ep1 deficit overshoots the deeper ep2 deficit — the real
    per-point slope falls from ~24.7 %/pt (ep1, 7.6%) to ~22.5 %/pt (ep2, 12.1%). That is
    the mild SATURATION/concavity the pricer's TODO(saturation) predicted, now measured
    against real data. We do NOT add a saturation term here (out of scope: one parameter
    only) — the overshoot is reported as the finding and quantifies the saturation for a
    future ticket.

Claim stays narrow (CYB-3 / CYB-7): the mechanism reproduces the episodes with real
ingredients under a single measured parameter; NOT price prediction.

Regenerates figures/cybeersym_v10_pricer_recal.png and prints the calibrate/validate split.
"""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from model import Params, run
from pricers import EGG_PRICING
from data.nass_layers import real_flock_deficit_path
from data.seasonality import seasonal_factor
from data.eggs_fred import window

P = Params(supp_up=8.0, store_up=0.06, store_hi=2.5, supp_hi=30.0)
rd = np.array(real_flock_deficit_path((2022, 1), (2025, 12)))
f = seasonal_factor(); demand = [f[k % 12] for k in range(len(rd))]
labels = [f"{y}-{m:02d}" for y in range(2022, 2026) for m in range(1, 13)]
_, b21 = window((2021, 1), (2021, 12)); mean21 = np.mean(b21)
REAL_EP1, REAL_EP2 = 4.823 / mean21, 6.227 / mean21   # indexed real peaks (Jan-23, Mar-25)

def model_path(slope):
    e = run(P, warmup=24, cull_path=list(rd), demand_path=demand,
            pricing={"pricer": "linear_deficit", "slope": slope, "hi": EGG_PRICING["hi"]})
    m = np.array(e.hist["retail"][24:24 + len(rd)]) / e.p0
    leak = max(max(abs(x) for x in e.hist["money_resid"]),
               max(abs(x) for x in e.hist["egg_resid"]))
    return m, leak

def peak(m, lo, hi):
    idx = [i for i, l in enumerate(labels) if lo <= l <= hi]
    j = max(idx, key=lambda i: m[i]); return m[j], labels[j]

# ---- CALIBRATE the slope on ep1 (2022-23) only, by bisection to the real ep1 peak ----
lo, hi = 8.0, 45.0
for _ in range(50):
    mid = (lo + hi) / 2
    v1, _ = peak(model_path(mid)[0], "2022-01", "2023-12")
    lo, hi = (mid, hi) if v1 < REAL_EP1 else (lo, mid)
slope_cal = round((lo + hi) / 2, 1)     # committed rounded value (-> EGG_PRICING)

# ---- report with the committed rounded slope; ep2 is the OUT-OF-SAMPLE test ----
m_new, leak = model_path(slope_cal)
m_old, _ = model_path(13.0)
e1v, e1m = peak(m_new, "2022-01", "2023-12"); e2v, e2m = peak(m_new, "2024-01", "2025-12")
o1v, _ = peak(m_old, "2022-01", "2023-12");   o2v, _ = peak(m_old, "2024-01", "2025-12")

print("=== CYB-9: recalibrate egg pricer slope against REAL deficits ===")
print(f"calibrate/validate split: CALIBRATE slope on ep1 (2022-23); FREEZE; VALIDATE OOS on ep2 (2024-25).")
print(f"committed EGG_PRICING slope in repo: {EGG_PRICING['slope']}  (this run's calibration: {slope_cal})\n")
print(f"                 ep1 / 2022-23 (in-sample)     ep2 / 2024-25 (OUT-OF-SAMPLE)")
print(f"  REAL           +{(REAL_EP1-1)*100:3.0f}%  2023-01              +{(REAL_EP2-1)*100:3.0f}%  2025-03")
print(f"  slope={slope_cal:<5}     +{(e1v-1)*100:3.0f}%  {e1m}  (fit)        +{(e2v-1)*100:3.0f}%  {e2m}  <- OOS")
print(f"  slope=13 (old) +{(o1v-1)*100:3.0f}%  (undershoot)         +{(o2v-1)*100:3.0f}%  (undershoot)")
oos_err = (e2v - REAL_EP2) / (REAL_EP2 - 1) * 100
print(f"\nOOS magnitude: model overshoots ep2 by {oos_err:+.0f}pp of the price rise.")
print("  real per-point slope: ep1 %.1f %%/pt (7.6%% deficit), ep2 %.1f %%/pt (12.1%% deficit)"
      % ((REAL_EP1-1)*100/7.6, (REAL_EP2-1)*100/12.1))
print("  -> single linear slope calibrated on shallow ep1 overshoots deeper ep2 = mild")
print("     SATURATION (the pricers.TODO). NOT fixed here (one parameter only); reported.")
print(f"conservation leak: {leak:.0e}  (substrate untouched)")

# ---------------------------------------------------------------- figure
INK="#1e2327"; ACC="#c0392b"; GRN="#27ae60"; BLU="#2c6fbb"; MUT="#7f8c8d"; GRID="#e8e6e1"; ORG="#d68910"
plt.rcParams.update({"font.size":10,"axes.edgecolor":INK,"axes.linewidth":0.8,
                     "figure.facecolor":"white","axes.facecolor":"white"})
fig = plt.figure(figsize=(13, 8.7)); gs = fig.add_gridspec(2, 1, height_ratios=[1.25, 1])
fig.suptitle("Cybeersym v0.10 — pricer slope recalibrated on real deficits (13→24), OOS reveals mild saturation",
             fontsize=13.5, fontweight="bold", color=INK, y=0.98)
labs, real_all = window((2022, 1), (2025, 12)); real_price = np.array(real_all) / mean21
midx = [(int(l[:4]) - 2022) * 12 + (int(l[5:7]) - 1) for l in labs]
xr = np.arange(len(labs))

a = fig.add_subplot(gs[0])
a.plot(xr, real_price, color=ACC, lw=2.4, marker="o", ms=3, label="REAL egg price (FRED)")
a.plot(xr, m_new[midx], color=GRN, lw=2, marker="^", ms=3, label=f"MODEL recalibrated (slope={slope_cal}, calibrated on ep1)")
a.plot(xr, m_old[midx], color=MUT, lw=1.5, ls=":", label="MODEL old slope=13 (undershoots — synthetic-era value)")
a.axhline(1, color=INK, lw=0.6)
a.axvspan(0, 23, color=BLU, alpha=0.05); a.axvspan(24, 47, color=ORG, alpha=0.06)
a.text(11, 3.4, "2022-23\n(CALIBRATION)", ha="center", fontsize=8.5, color=BLU, fontweight="bold")
a.text(35, 3.4, "2024-25\n(OUT-OF-SAMPLE)", ha="center", fontsize=8.5, color=ORG, fontweight="bold")
a.set_ylabel("egg price (indexed, 2021=1)"); a.set_xticks(xr[::3]); a.set_xticklabels([labs[i] for i in xr[::3]], fontsize=7, rotation=45)
a.grid(True, color=GRID, lw=0.7); a.set_axisbelow(True); a.legend(frameon=False, fontsize=9, loc="upper right")
a.set_title("ep1 matched by construction; ep2 (OOS) slightly OVERSHOT — the honest single-slope limit", fontweight="bold", fontsize=9.5)

# gain curve: model emergent peak vs deficit, recalibrated; real points show concavity
b = fig.add_subplot(gs[1])
dd = np.linspace(0, 0.14, 15); gain = []
for d in dd:
    ee = run(P, warmup=24, cull_path=[d]*24, demand_path=[f[k%12] for k in range(24)],
             pricing={"pricer":"linear_deficit","slope":slope_cal,"hi":EGG_PRICING["hi"]})
    gain.append((np.array(ee.hist["retail"][24:48]).max()/ee.p0 - 1)*100)
b.plot(dd*100, gain, color=GRN, lw=2.2, marker="^", ms=3, label=f"model emergent gain (slope={slope_cal})")
b.scatter([7.6, 12.1], [(REAL_EP1-1)*100, (REAL_EP2-1)*100], color=ACC, s=90, zorder=5, label="REAL (real deficit, price rise)")
for dx, dy, t in [(7.6, (REAL_EP1-1)*100, "ep1 2022-23 (fit)"), (12.1, (REAL_EP2-1)*100, "ep2 2024-25 (OOS)")]:
    b.annotate(t, (dx, dy), (dx-3.5, dy+22), fontsize=8.5, color=ACC)
b.set_xlabel("real flock deficit at peak (%)"); b.set_ylabel("peak price rise (%)")
b.grid(True, color=GRID, lw=0.7); b.set_axisbelow(True); b.legend(frameon=False, fontsize=8.5, loc="upper left")
b.set_title("calibrated to ep1; the ep2 real point sits BELOW the line — reality saturates at deep deficits", fontweight="bold", fontsize=9.5)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("figures/cybeersym_v10_pricer_recal.png", dpi=140, bbox_inches="tight")
print("\nsaved figures/cybeersym_v10_pricer_recal.png")
