---
id: concept-natural-experiment-portfolio
status: developing
tags: [validation, natural-experiments, out-of-sample, commodities, crises, reproducibility, method, future-work]
created: 2026-08-01
derived_from: Claude Code session 2026-08-01 (extends concept-phase-space-macroeconomics)
---

# Portfolio of natural experiments — "finding other eggs"

**Future-work brainstorm.** The empirical backbone under the classifier
([phase-space-macroeconomics](phase-space-macroeconomics.md)): a triaged set of clean natural
experiments. Two kinds — **mechanism-eggs** (test pricing dynamics, like the actual HPAI eggs)
and **regime-eggs** (test that the classifier *discriminates* dynamical classes).

## What makes a good "egg" (selection criteria)

1. Exogenous, well-identified shock (clean causality).
2. Measurable driver at high frequency (eggs: USDA/NASS culls).
3. Good outcome data (eggs: FRED prices).
4. Bounded / localized system (mechanism not swamped).
5. Repeated instances (out-of-sample + reproducibility).

## Mechanism-eggs (clean commodity natural experiments)

- **African Swine Fever, China 2018-19 — the egg's identical twin.** Disease → ~40% of the pig
  herd culled → measurable herd data → pork price ~doubles. Different country / commodity / decade
  → a true OOS replication of the HPAI structure. **Chase first.**
- **Coffee** (Brazil frosts, 2021), **Cocoa** (West Africa swollen-shoot + weather, 2023-24
  record), **Orange juice** (Florida greening + Hurricane Ian) — weather/disease, futures data,
  multiple instances each.
- **Texas winter storm (Uri), Feb 2021** — ERCOT at the price cap; ultra-clean, minute-level data.
- **Lumber 2021** — a clean boom-and-bust (bounded turbulence vs. limit cycle).
- **Onion / rice export bans (India, recurring)** — a *policy* switching-manifold going active,
  sharply dated.

## Regime-eggs (test class discrimination)

- **Escape:** Venezuela 2016-19 (high-frequency Hanke data), Zimbabwe 2008, Hungary 1946,
  **Argentina** (metastable — decades near a bifurcation, many episodes).
- **Peg border-collisions:** Swiss franc 15 Jan 2015 (SNB floor drop, ~30% intraday — a single-day
  border-collision), UK / ERM 1992.
- **Debt-driven collapse:** 1929, 2008, Japan 1990.

## Reproducibility banks (the OOS test that kills narrative-circularity)

Clusters of near-simultaneous *independent* realizations of one regime:

- **Nordic banking crises, early 1990s** — Sweden, Finland, Norway.
- **Asian financial crisis, 1997** — Thailand → Indonesia, Korea, Malaysia (also feeds the CYB-19
  crunch/contagion work).
- **Latin American hyperinflations, 1980s-90s** — Argentina, Brazil, Bolivia, Peru.

Set the signature on one sibling; test on the held-out siblings. Reproducibility ⇒ dynamical
class; failure ⇒ narrative.

## Honest tradeoff

Cleanest eggs (commodities) test the *mechanism* but aren't "regimes"; the most important ones
(crises / hyperinflations) test the *classes* but are messy, multi-channel, and — for the old ones
(Weimar, Hungary '46) — data-poor. Recent cases (Venezuela, Swiss franc, Texas, ASF) have the
high-frequency data. The portfolio must be deliberate; pre-1950 cases are **illustrative, not
fitted**.

## Next step

When triaged, promote to a `notes/episodes/` index — one stub per candidate: *shock · driver-data
source · price-data source · hypothesized class · data quality*. First ticket-worthy target:
**ASF-pork mechanism replication** (the cleanest "second egg").

## Related

[Phase-Space Macroeconomics](phase-space-macroeconomics.md) · [Hyperinflation](hyperinflation.md) ·
[Piketty](../people/piketty.md) · [Open questions](../../indexes/questions.md)
