#!/usr/bin/env python3
"""WID slow-variable inventory — coverage readout, not a model.

For each country in the working slice, report year-coverage (min/max/N) of the
distributional slow variables the phase-space classifier needs (Q-2026-005):
  - top 1% / top 10% / bottom 50% pretax national income share (sptincj992)
  - top 1% net personal wealth share                           (shwealj992)
  - beta = net national wealth / net national income           (mnweali999 / mnninci999)

Pure stdlib + csv. Reads the extracted per-country CSVs (semicolon-delimited long
format: country;variable;percentile;year;value;age;pop;data_quality).
Prints a Markdown table to stdout. No model consumes this; it answers one question:
can WID carry the slow-manifold role, and over what window, for our test countries?
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EXTRACTED = os.path.join(HERE, "extracted")

# ISO-2 -> role bucket (why this country is in the slice)
COUNTRIES = [
    ("US", "reference / debt-collapse (1929, 2008)"),
    ("FR", "reference (Piketty home series)"),
    ("DE", "debt-collapse / Weimar lineage"),
    ("JP", "debt-collapse (1990)"),
    ("GB", "peg break (ERM 1992)"),
    ("SE", "reproducibility bank: Nordic 1990s"),
    ("FI", "reproducibility bank: Nordic 1990s"),
    ("NO", "reproducibility bank: Nordic 1990s"),
    ("TH", "reproducibility bank: Asian 1997"),
    ("ID", "reproducibility bank: Asian 1997"),
    ("KR", "reproducibility bank: Asian 1997"),
    ("MY", "reproducibility bank: Asian 1997"),
    ("AR", "escape / metastable (recurring)"),
    ("VE", "escape (2016-19 hyperinflation)"),
    ("ZW", "escape (2008 hyperinflation)"),
    ("CN", "mechanism context (ASF pork 2018-19)"),
]

# (label, variable_code, percentile). None percentile => any (for macro totals).
SERIES = [
    ("top1%  income share",  "sptincj992", "p99p100"),
    ("top10% income share",  "sptincj992", "p90p100"),
    ("bot50% income share",  "sptincj992", "p0p50"),
    ("top1%  wealth share",  "shwealj992", "p99p100"),
    ("net national income",  "mnninci999", None),
    ("net national wealth",  "mnweali999", None),
]


def scan_country(iso):
    path = os.path.join(EXTRACTED, f"WID_data_{iso}.csv")
    if not os.path.exists(path):
        return None
    # want[(var,pct)] -> list of (year, value)
    want = {(v, p) for _, v, p in SERIES}
    hits = {key: [] for key in want}
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f, delimiter=";")
        next(r, None)  # header
        for row in r:
            if len(row) < 5:
                continue
            var, pct, year, val = row[1], row[2], row[3], row[4]
            for (wv, wp) in want:
                if var == wv and (wp is None or pct == wp):
                    try:
                        y = int(year)
                        v = float(val) if val not in ("", "NA") else None
                    except ValueError:
                        continue
                    if v is not None:
                        hits[(wv, wp)].append((y, v))
    return hits


def fmt(hits, var, pct):
    rows = sorted(hits.get((var, pct), []))
    if not rows:
        return "—"
    yrs = [y for y, _ in rows]
    return f"{min(yrs)}–{max(yrs)} (N={len(rows)})"


def latest_value(hits, var, pct):
    rows = sorted(hits.get((var, pct), []))
    return rows[-1] if rows else None


def main():
    names = {}
    cpath = os.path.join(EXTRACTED, "WID_countries.csv")
    if os.path.exists(cpath):
        with open(cpath, newline="", encoding="utf-8") as f:
            r = csv.reader(f, delimiter=";")
            next(r, None)
            for row in r:
                if len(row) >= 3:
                    names[row[0]] = row[2]

    header = ["country"] + [lbl for lbl, _, _ in SERIES]
    print("| " + " | ".join(header) + " |")
    print("|" + "|".join(["---"] * len(header)) + "|")
    for iso, _role in COUNTRIES:
        hits = scan_country(iso)
        name = names.get(iso, iso)
        if hits is None:
            print(f"| {iso} {name} | " + " | ".join(["missing file"] * len(SERIES)) + " |")
            continue
        cells = [fmt(hits, v, p) for _, v, p in SERIES]
        print(f"| **{iso}** {name} | " + " | ".join(cells) + " |")

    # A couple of concrete spot-checks so the numbers are real, not just coverage.
    print("\n### Spot-checks (latest available observation)\n")
    for iso in ("US", "AR", "SE"):
        hits = scan_country(iso)
        if not hits:
            continue
        lv = latest_value(hits, "sptincj992", "p99p100")
        if lv:
            print(f"- **{iso}** top-1% pretax income share, {lv[0]}: {lv[1]*100:.1f}%")
        inc = latest_value(hits, "mnninci999", None)
        wlth = latest_value(hits, "mnweali999", None)
        if inc and wlth and inc[1]:
            # align on the later common-ish year for a rough beta read
            print(f"    beta (net wealth/income) ~ {wlth[1]/inc[1]:.2f} "
                  f"(wealth {wlth[0]} / income {inc[0]})")


if __name__ == "__main__":
    main()
