"""
Seasonal demand factor for eggs, derived from the real FRED series — not invented.
Method: take calm pre-shock years (2016-2021), detrend each year (divide by that
year's mean to remove the level), then average each calendar month across years.
The result is a recurring month-of-year multiplier: >1 in high season, <1 in low.

This is the empirical seasonal pattern (holiday baking demand + shorter-day winter
laying drop) that the supply-only model was missing — the reason every egg-price
peak lands in winter regardless of when the birds die.
"""
import numpy as np
from data.eggs_fred import SERIES

def seasonal_factor(calm_years=range(2016, 2022)):
    by_month = {m: [] for m in range(1, 13)}
    # detrend within each calm year, then collect by calendar month
    for yr in calm_years:
        vals = [(m, v) for (y, m, v) in SERIES if y == yr and v is not None]
        if len(vals) < 12:
            continue
        ymean = np.mean([v for _, v in vals])
        for m, v in vals:
            by_month[m].append(v / ymean)
    factor = np.array([np.mean(by_month[m]) for m in range(1, 13)])
    return factor / factor.mean()        # normalize to mean 1.0

if __name__ == "__main__":
    f = seasonal_factor()
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    print("month  seasonal_demand_factor")
    for mo, v in zip(months, f):
        bar = "#" * int((v-0.85)*200) if v > 0.85 else ""
        print(f"  {mo}   {v:5.3f}  {bar}")
    print(f"\n peak month: {months[int(f.argmax())]} ({f.max():.3f}),  "
          f"trough: {months[int(f.argmin())]} ({f.min():.3f})")
