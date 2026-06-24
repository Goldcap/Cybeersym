"""
Real fixture: monthly table-egg-layer depopulation, US HPAI outbreak.
Source: USDA APHIS, reported via WATTPoultry & USDA-ERS/CRS. Millions of layers.

The DISPOSITIVE fact this encodes: the biggest culls were spring 2022 (Mar 16.91M,
Apr 10.7M) but the egg price peaked Jan 2023 — because a depopulated layer flock
takes ~6 months (20 wks) to replace (USDA-ERS). So the supply constraint is a
LAGGED CUMULATIVE STOCK (depleted flock), not the monthly cull flow. A flow model
of capacity loss cannot reproduce the price timing; a stock-with-replacement-lag
model can. That mismatch is the data refuting the naive mechanism.

Documented monthly majors (USDA APHIS via WATTPoultry, 2024): 2022 total 43.4M;
Mar 16.91, Apr 10.7, Sep 4.9, Dec 3.9. 2023: no layer outbreak until Nov 5.1, Dec 7.8.
Minor months (*) estimated to approximate the documented $43.4M 2022 annual total;
the four documented majors are 84% of 2022 losses and dominate the dynamics.
"""
# (year, month, millions_of_layers_depopulated)
DEPOP = [
    (2022,1,0.0),(2022,2,0.5),(2022,3,16.91),(2022,4,10.70),(2022,5,0.8),(2022,6,0.2),  # *minors estimated
    (2022,7,0.2),(2022,8,0.3),(2022,9,4.90),(2022,10,0.5),(2022,11,1.5),(2022,12,3.90),
    (2023,1,0.0),(2023,2,0.0),(2023,3,0.0),(2023,4,0.0),(2023,5,0.0),(2023,6,0.0),
    (2023,7,0.0),(2023,8,0.0),(2023,9,0.0),(2023,10,0.0),(2023,11,5.10),(2023,12,7.80),
]
BASELINE_FLOCK = 310.0   # million table-egg layers, 2020-21 average (USDA NASS / CRS)

def flock_deficit_path(depop=None, baseline=BASELINE_FLOCK, replace_lag=6):
    """
    Turn the depopulation FLOW into a capacity-loss path via flock-STOCK dynamics:
    each cull removes hens; replacement pullets for that cull mature and re-enter
    `replace_lag` months later. Returns monthly deficit fraction (baseline-flock)/baseline
    — i.e. the fraction of laying capacity missing that month. This is the real,
    lag-aware capacity-loss path that replaces the stylised bump.
    """
    d = [v for _,_,v in (depop or DEPOP)]
    n = len(d)
    arriving = [0.0]*(n + replace_lag + 1)
    flock = baseline
    path = []
    for t in range(n):
        flock -= d[t]                                 # cull now
        if t + replace_lag < len(arriving):
            arriving[t + replace_lag] += d[t]         # its replacement, lagged
        flock += arriving[t]                          # replacements maturing now
        flock = min(flock, baseline)                  # never exceed baseline
        path.append(max(0.0, (baseline - flock) / baseline))
    return path

if __name__ == "__main__":
    from data.eggs_fred import window  # noqa
    p = flock_deficit_path()
    labels = [f"{y}-{m:02d}" for y,m,_ in DEPOP]
    print("month     depop(M)  flock_deficit%")
    for (y,m,v), d in zip(DEPOP, p):
        bar = "#" * int(d*120)
        print(f"{y}-{m:02d}   {v:6.2f}     {d*100:5.1f}  {bar}")
    pk = max(range(len(p)), key=lambda i:p[i])
    print(f"\ndeficit peaks {labels[pk]} ({p[pk]*100:.1f}%) — vs real egg-price peak 2023-01")


# --------------------------------------------------------------------------- #
#  Second episode: 2024 summer wave + 2024-25 winter wave (for OUT-OF-SAMPLE test)
#  Documented layer months (USDA APHIS via WATTPoultry / USDA-ERS / AMS Egg Mkts):
#    2024 Apr 8.4, May 5.7, Jul 3.1 ; Nov 3.97 ; Dec 13.2 (layer flocks)
#  Estimated* to fit Oct'24-Feb'25 ~= 52M (UT D253) and Jan+half-Feb ~= 28M (WATTPoultry):
#    Oct'24 3.3*, Jan'25 18.7*, Feb'25 12.8*, Mar'25 2.0*
#  Real retail price peaked $6.23 in Mar 2025 (CRS IF12949).
# --------------------------------------------------------------------------- #
DEPOP_2024_25 = [
    (2024,1,0.0),(2024,2,0.0),(2024,3,0.0),(2024,4,8.40),(2024,5,5.70),(2024,6,0.0),
    (2024,7,3.10),(2024,8,0.0),(2024,9,0.0),(2024,10,3.30),(2024,11,3.97),(2024,12,13.20),
    (2025,1,18.70),(2025,2,12.80),(2025,3,2.00),(2025,4,0.0),(2025,5,0.0),(2025,6,0.0),
    (2025,7,0.0),(2025,8,0.0),(2025,9,0.0),(2025,10,0.0),(2025,11,0.0),(2025,12,0.0),
]
# Continuous 2022->2025 depopulation (drives one unbroken flock-deficit path)
DEPOP_FULL = DEPOP + DEPOP_2024_25
