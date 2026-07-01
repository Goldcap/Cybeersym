"""
Real fixture: US monthly table-egg-layer INVENTORY (flock on hand), first-of-month.

Source : USDA NASS QuickStats, series
         `CHICKENS, LAYERS, TABLE - INVENTORY`, agg_level=NATIONAL, unit=HEAD,
         reference_period = FIRST OF <month> (point-in-time monthly inventory).
         https://quickstats.nass.usda.gov/  — public domain. Retrieved 2026-07-01
         via the QuickStats API (see `fetch_live` for the exact, reproducible query).

PROVENANCE / DATA HYGIENE (CYB-7 criterion 1).
  * Exact series (NOT annual, NOT all-chickens, NOT broilers, NOT hatching layers,
    NOT total-layers-incl-hatching): commodity CHICKENS, class TABLE, statisticcat
    INVENTORY, unit HEAD, freq POINT IN TIME (reference_period FIRST OF <month>),
    agg_level NATIONAL. Verified by enumerating every chicken-inventory short_desc.
  * Determinism: the fixture below is committed and used at import; there is NO live
    API call on the model path. NASS *revises* releases, so a live pull would break
    determinism — `fetch_live` exists only to re-audit the pull, and was verified to
    reproduce this fixture exactly (78/78 months, 0 mismatches) on the pull date.
  * Gaps / suppressed cells: NONE. The national monthly series is complete over
    2020-01..2026-06 — 78 contiguous months, every one a real HEAD value, no
    withheld/(D)-suppressed/estimated cells. So there is nothing to interpolate or
    drop; if a future re-pull introduces a gap, handle it explicitly (do not let a
    missing month become a silent zero, which would read as a 100% flock deficit).

WHY THIS RETIRES `replace_lag`. `data/hpai_culls.py` reconstructs the flock-deficit
path from the cull FLOW plus a calibrated `replace_lag` (how many months until a
depopulated bird's replacement matures). That lag was the model's one soft spot: it
was fit so the *synthetic* deficit would peak near the observed price peak. This
series measures the flock STOCK directly, so the deficit needs no reconstruction and
no lag — the real data already contains the true timing.

THE DESEASONALIZATION. Layer inventory has a strong, recurring seasonal cycle
(summer laying-drop + fall molt → every year dips ~May–Aug, recovers Nov–Jan). A
flat-baseline deficit would read that normal summer dip as a "shortage." So the HPAI
signal is the shortfall of actual inventory BELOW its seasonal-normal level, where
the seasonal-normal is the pre-outbreak flock (2020–21, before the 2022 layer
outbreak) averaged by calendar month — the same detrend-calm-years method
`data/seasonality.py` uses for demand. (The 2022 and 2024–25 layer outbreaks are the
events we're measuring, so they are excluded from the normal.)

VALIDATED (see `v09_real_flock.py`): the deseasonalized real deficit peaks 2023-01
(ep1) and 2025-03 (ep2) — matching both real egg-price peaks — with ZERO timing
parameters, and fed through the model reproduces both price-peak months. ep2 is
fully out-of-sample and robust to the normal-year choice; ep1 lands Jan/Feb-2023
across normal choices at the model level (see the robustness note in v09).
"""

# (year, month) -> table-egg layers on hand (HEAD), NASS QuickStats, retrieved 2026-07-01
LAYERS_TABLE = {
    (2020, 1): 340667000, (2020, 2): 335552000, (2020, 3): 333452000, (2020, 4): 332919000,
    (2020, 5): 327225000, (2020, 6): 324481000, (2020, 7): 320902000, (2020, 8): 321041000,
    (2020, 9): 322553000, (2020, 10): 324269000, (2020, 11): 325304000, (2020, 12): 329107000,
    (2021, 1): 330068000, (2021, 2): 330273000, (2021, 3): 330521000, (2021, 4): 328017000,
    (2021, 5): 322683000, (2021, 6): 318690000, (2021, 7): 319940000, (2021, 8): 321524000,
    (2021, 9): 322969000, (2021, 10): 326203000, (2021, 11): 329648000, (2021, 12): 331352000,
    (2022, 1): 331624000, (2022, 2): 327142000, (2022, 3): 326052000, (2022, 4): 309890000,
    (2022, 5): 302849000, (2022, 6): 302757000, (2022, 7): 303766000, (2022, 8): 308689000,
    (2022, 9): 310235000, (2022, 10): 309976000, (2022, 11): 312009000, (2022, 12): 317689000,
    (2023, 1): 309982000, (2023, 2): 309994000, (2023, 3): 313990000, (2023, 4): 315617000,
    (2023, 5): 316723000, (2023, 6): 314566000, (2023, 7): 312695000, (2023, 8): 314214000,
    (2023, 9): 316838000, (2023, 10): 320618000, (2023, 11): 322572000, (2023, 12): 319923000,
    (2024, 1): 312582000, (2024, 2): 310352000, (2024, 3): 314271000, (2024, 4): 314691000,
    (2024, 5): 306664000, (2024, 6): 307217000, (2024, 7): 305759000, (2024, 8): 303801000,
    (2024, 9): 308186000, (2024, 10): 313506000, (2024, 11): 315242000, (2024, 12): 316574000,
    (2025, 1): 308959000, (2025, 2): 299092000, (2025, 3): 291871000, (2025, 4): 292858000,
    (2025, 5): 295613000, (2025, 6): 294774000, (2025, 7): 297663000, (2025, 8): 300580000,
    (2025, 9): 302504000, (2025, 10): 305528000, (2025, 11): 305168000, (2025, 12): 306538000,
    (2026, 1): 311261000, (2026, 2): 310014000, (2026, 3): 313253000, (2026, 4): 307253000,
    (2026, 5): 307356000, (2026, 6): 311504000,
}

# Pre-outbreak years used to build the seasonal-normal flock (layers untouched by HPAI).
NORMAL_YEARS = (2020, 2021)


def seasonal_normal(normal_years=NORMAL_YEARS):
    """Seasonal-normal flock level by calendar month = mean over `normal_years`.

    These are pre-2022-outbreak years, so this is the flock the industry runs at
    absent a disease shock — the reference the HPAI deficit is measured against.
    """
    return {m: sum(LAYERS_TABLE[(y, m)] for y in normal_years) / len(normal_years)
            for m in range(1, 13)}


def real_flock_deficit_path(start=(2022, 1), end=(2025, 12), normal_years=NORMAL_YEARS):
    """Deseasonalized real flock-deficit path — the drop-in replacement for
    `hpai_culls.flock_deficit_path`, with NO cull reconstruction and NO replace_lag.

    deficit_t = max(0, (seasonal_normal[month] - inventory_t) / seasonal_normal[month])

    Returns the monthly deficit fraction (fraction of the seasonal-normal laying
    flock that is missing) over [start, end] inclusive. Deterministic; pure function
    of the committed fixture.
    """
    normal = seasonal_normal(normal_years)
    (y0, m0), (y1, m1) = start, end
    path = []
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        actual = LAYERS_TABLE[(y, m)]
        path.append(max(0.0, (normal[m] - actual) / normal[m]))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return path


def fetch_live(api_key, year_ge=2020):
    """Reproduce the committed fixture from the NASS QuickStats API (stdlib only).

    Returns a {(year, month): head} dict identical in structure to LAYERS_TABLE.
    Not called at import — the committed fixture keeps the module deterministic and
    network-free. Kept so the pull is auditable and re-runnable:
        from data.nass_layers import fetch_live; fetch_live(os.environ["NASS_API_KEY"])
    """
    import json, urllib.parse, urllib.request
    _MON = {"JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
            "JUL": 7, "AUG": 8, "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12}
    q = urllib.parse.urlencode({
        "key": api_key,
        "short_desc": "CHICKENS, LAYERS, TABLE - INVENTORY",
        "agg_level_desc": "NATIONAL",
        "year__GE": str(year_ge),
        "format": "JSON",
    })
    url = "https://quickstats.nass.usda.gov/api/api_GET/?" + q
    with urllib.request.urlopen(url, timeout=30) as r:
        rows = json.load(r)["data"]
    out = {}
    for row in rows:
        month = _MON[row["reference_period_desc"].split()[-1]]
        out[(int(row["year"]), month)] = int(row["Value"].replace(",", ""))
    return out


if __name__ == "__main__":
    normal = seasonal_normal()
    path = real_flock_deficit_path()
    labels = [f"{y}-{m:02d}" for y in range(2022, 2026) for m in range(1, 13)]
    print("seasonal-normal flock (2020-21 avg), by month (M):",
          {m: round(normal[m] / 1e6, 1) for m in range(1, 13)})
    print(f"annual normal ~= {sum(normal.values())/len(normal)/1e6:.1f}M layers\n")
    print("month     deficit%   (deseasonalized, real inventory)")
    for lbl, d in zip(labels, path):
        print(f"{lbl}   {d*100:5.1f}  {'#'*int(d*300)}")
    for lo, hi, tag, pk in [("2022-01", "2023-12", "ep1", "2023-01"),
                            ("2024-01", "2025-12", "ep2", "2025-03")]:
        idx = [i for i, l in enumerate(labels) if lo <= l <= hi]
        j = max(idx, key=lambda i: path[i])
        print(f"{tag}: real-deficit peak {labels[j]} ({path[j]*100:.1f}%)  vs price peak {pk}")
