"""
Calibrate Cybeersym to the real 2022-23 egg shock (FRED APU0000708111).

The 2022 rise was MULTI-WAVE (repeated HPAI culls Feb-Dec 2022), so we drive the
model with a stylised cull-intensity PATH (slow ~9-month rise to a Dec-2022 peak,
faster ~6-month recovery) scaled by a depth parameter, rather than one rectangle.
NOTE: the path SHAPE is stylised, not yet derived from monthly flock-loss data —
that real input is the next fixture. Search = depth + rocket/feather speeds.
Objective: RMSE of baseline-indexed price over 2022-01..2023-12. Leaky runs rejected.
"""
import numpy as np
from itertools import product
from model import Params, run
from data.eggs_fred import window

labels, real = window((2022,1),(2023,12))
_, base_prices = window((2021,1),(2021,12))
real_base = float(np.mean(base_prices))
r_idx = np.array(real) / real_base
WIN = len(r_idx)

# stylised multi-wave cull shape (asymmetric bump): peak ~Dec 2022 (month 11)
def cull_shape():
    sh = np.zeros(WIN)
    for k in range(WIN):
        if   k < 2:   sh[k] = 0.0
        elif k <= 11: sh[k] = (k - 2) / 9.0          # 9-month rise
        elif k <= 18: sh[k] = max(0.0, 1 - (k-11)/7) # 7-month fall
        else:         sh[k] = 0.0
    return sh
SHAPE = cull_shape()

def model_index(P, depth):
    e = run(P, warmup=24, cull_path=list(depth * SHAPE))
    m = np.array(e.hist["retail"][24:24+WIN]) / e.p0
    leak = max(max(abs(x) for x in e.hist["money_resid"]),
               max(abs(x) for x in e.hist["egg_resid"]))
    return m, leak

grid = dict(                         # proportional pass-through: supp_up = sensitivity
    depth     = [0.45, 0.55, 0.65, 0.75, 0.85],
    supp_up   = [0.15, 0.25, 0.35, 0.50, 0.70],
    supp_down = [0.0],                  # unused in proportional body (kept for branded)
    store_up  = [0.03, 0.06, 0.10],     # store ~constant; cost-pass-through dominates
)
keys = list(grid); best = None
for combo in product(*[grid[k] for k in keys]):
    kw = dict(zip(keys, combo))
    P = Params(store_up=kw["store_up"], store_down=kw["store_up"],
               supp_up=kw["supp_up"], supp_down=kw["supp_down"],
               store_hi=2.0, supp_hi=12.0)
    try:
        m, leak = model_index(P, kw["depth"])
    except AssertionError:
        continue
    if leak > 1e-6: continue
    rmse = float(np.sqrt(np.mean((m - r_idx)**2)))
    if best is None or rmse < best[0]:
        best = (rmse, kw, m)

rmse, kw, m = best
corr = float(np.corrcoef(m, r_idx)[0,1])
print("="*60)
print("CALIBRATION vs FRED 2022-23 egg shock  (multi-wave cull path)")
print("="*60)
print(f"  best params : {kw}")
print(f"  RMSE (index): {rmse:.3f}   correlation: {corr:.3f}")
print(f"  peak  model : +{(m.max()-1)*100:.0f}%   real : +{(r_idx.max()-1)*100:.0f}%")
print(f"  peak month  : model {labels[int(m.argmax())]}   real {labels[int(r_idx.argmax())]}")
print("="*60)
np.savez("calib_best.npz", m=m, r=r_idx, labels=np.array(labels),
         shape=SHAPE, rmse=rmse, corr=corr, real_base=real_base, **kw)
