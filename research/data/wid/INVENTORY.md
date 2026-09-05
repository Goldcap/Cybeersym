---
id: data-wid-inventory
status: raw-reference
tags: [data, wid, piketty, inventory, slow-manifold, coverage]
created: 2026-08-02
generated_by: inventory.py (pure stdlib csv; reads extracted/ per-country files)
---

# WID slow-variable inventory — "what's actually in here?"

The **can-it-carry-the-slow-variable-role?** readout for the phase-space classifier
(Q-2026-005), over the working slice of test countries. Coverage only — **no model
consumes this.** Regenerate with `python3 inventory.py`.

Cells show `min–max (N)` for each series. The distributional shares are equal-split adults
20+ (`sptincj992`, `shwealj992`); β is computed as `mnweali999 / mnninci999`.

| country | top1% income | top10% income | bot50% income | top1% wealth | net nat. income | net nat. wealth |
|---|---|---|---|---|---|---|
| **US** USA | 1820–2024 (117) | 1820–2024 (117) | 1820–2024 (117) | 1820–2024 (117) | 1800–2025 (226) | 1800–2025 (226) |
| **FR** France | 1820–2024 (115) | " | " | 1800–2024 (135) | 1800–2025 (226) | 1800–2025 (226) |
| **DE** Germany | 1820–2024 (123) | " | " | 1820–2024 (76) | 1800–2025 (226) | 1800–2025 (226) |
| **JP** Japan | 1820–2024 (141) | " | " | 1820–2024 (56) | 1800–2025 (226) | 1800–2025 (226) |
| **GB** UK | 1820–2024 (120) | " | " | 1820–2024 (125) | 1800–2025 (226) | 1800–2025 (226) |
| **SE** Sweden | 1820–2024 (99) | " | " | 1800–2024 (76) | 1800–2025 (226) | 1800–2025 (226) |
| **FI** Finland | 1920–2024 (105) | " | " | **1980**–2024 (45) | 1921–2025 (105) | **1980**–2025 (46) |
| **NO** Norway | 1820–2024 (101) | " | " | 1820–2024 (56) | 1800–2025 (226) | 1800–2025 (226) |
| **TH** Thailand | 1820–2024 (56) | " | " | 1820–2024 (56) | 1800–2025 (226) | 1800–2025 (226) |
| **ID** Indonesia | 1820–2024 (74) | " | " | 1820–2024 (56) | 1800–2025 (226) | 1800–2025 (226) |
| **KR** Korea | 1820–2024 (99) | " | " | 1820–2024 (56) | 1800–2025 (226) | 1800–2025 (226) |
| **MY** Malaysia | 1948–2024 (73) | " | " | **1980**–2024 (45) | 1948–2025 (78) | **1980**–2025 (46) |
| **AR** Argentina | 1820–2024 (81) | " | " | 1820–2024 (56) | 1800–2025 (226) | 1800–2025 (226) |
| **VE** Venezuela | **1980**–2024 (45) | " | " | **1980**–2024 (45) | 1950–2025 (76) | **1980**–2025 (46) |
| **ZW** Zimbabwe | 1917–2024 (102) | " | " | **1980**–2024 (45) | 1917–2025 (109) | **1980**–2025 (46) |
| **CN** China | 1820–2024 (58) | " | " | 1820–2024 (58) | 1800–2025 (226) | 1800–2025 (226) |

## Instrument self-check — the values are real (and correct)

`inventory.py` spot-checks latest observations against known facts:

- **US** top-1% pretax income share, 2024 = **20.7%** ✓ (matches published WID ~20%).
- **SE** top-1% = **9.5%** ✓ (Sweden's low concentration — correct).
- **AR** top-1% = **18.1%**; β (wealth/income): US **6.2**, SE **6.7**, AR **3.6** — all in
  Piketty's plausible 3–7 band for the respective economies. ✓

This is the same discipline as the `src/chaos/` instruments self-testing on a closed-form
case first: before trusting the data, confirm it reproduces things we already know.

## What this tells us (four findings)

1. **Frequency is annual — which is correct.** WID is at best one obs/year. That is not a
   limitation for the slow manifold; the slow variable is *supposed* to be slow. The fast
   system (prices/spreads) stays on FRED monthly/daily. The slow–fast split is literally
   two data cadences.
2. **The macro totals (income, wealth) are genuinely deep + dense** — ~annual 1800–2025
   (N≈226) for the major economies. β = wealth/income is therefore well-supported over two
   centuries where it matters.
3. **The distributional shares are broad but NOT uniformly dense.** `min–max` spans are
   wide, but `N < (max−min+1)` everywhere → **gaps**, concentrated in the deep past. For the
   big Western economies the honest dense window for income shares is ~**1913 onward**; for
   many others it is later.
4. **A hard 1980 wall on distributional *wealth* shares** for FI, MY, VE, ZW (and thin
   pre-1980 elsewhere) — the WID global-wealth project's baseline. Income shares reach
   further back than wealth shares.

## Honest caveats (the "beautiful lie, one level up" guard)

- **Deep-history developing-country numbers are modeled, not observed.** TH/CN/ID showing
  income shares back to "1820" (N≈56) is WID **backward extrapolation / regional imputation**,
  not national measurement. Treat pre-~1950 shares for these as *illustrative, not fitted* —
  the same rule the egg work applies to pre-1950 episodes.
- **N is the honesty column, not the range.** Always gate a test on the *dense* sub-window,
  not the nominal span.
- **Comparability across a century + 16 countries** is WID's own stated caveat; cross-country
  reproducibility tests (Q-2026-004) must use a common, well-covered window.

## Verdict

**WID can carry the slow-variable role for our test set** — the reproducibility banks all
have coverage in their crisis windows (Nordics through the 1990s; the Asian-97 four through
1997; Venezuela through 2016-19), and β is deep and dense. The binding constraint is not
availability but **comparability + imputation in the deep past** — manage it by restricting
each test to its dense window and pre-registering that window.

## Next (still ideation — no ticket yet)

The build that *consumes* this — a slow–fast substrate where β / top-share is the slow
parameter walking a fast SFC core across a border — is the ticket-worthy crossing (`CYB-<n>`).
Before that: a thin numpy loader (`load_series(iso, var, pct) -> (years, values)`) belongs
with the build, not here.

## Related

[PROVENANCE](PROVENANCE.md) · [Phase-Space Macroeconomics](../../notes/concepts/phase-space-macroeconomics.md) ·
[Natural-experiment portfolio](../../notes/concepts/natural-experiment-portfolio.md) ·
[Piketty](../../notes/people/piketty.md) · [Q-2026-005](../../indexes/questions.md)
