# Cybeersym

**Statistical and Distributive Modelling of Inflation Economies.**
An agent-based, stock-flow-consistent (SFC) simulation for testing *structural*
inflation hypotheses. A wind tunnel, not a crystal ball: supply a shock, observe the
structural response. Econometrics is the *referee* (out-of-sample validation), not the
engine. Homage to Stafford Beer's Cybersyn (+ beer).

The working commodity is **eggs** — the 2022-23 and 2024-25 US HPAI price spikes —
because they're a clean natural experiment: a real, measurable supply shock (USDA
flock depopulation) driving a large, well-documented price move (FRED), with a sharp
distributional footprint.

## What's here

```
src/model.py    SFC engine — conservation asserts, 5 income quintiles, supplier/store
src/pricers.py  commodity pricer registry (the egg price-deficit slope lives here)
src/events.py   adverse-event plugin layer (supply/demand path-transforms)
src/data/       real fixtures: FRED egg prices, USDA culls + flock transform, seasonality
src/vNN_*.py    the analysis script that established each version (see CHANGELOG.md)
src/figures/    one chart per version
CHANGELOG.md    the version arc — each version is one finding. START HERE.
```

## Quick start

```bash
pip install -r requirements.txt        # numpy, matplotlib
cd src
python3 v06_oos_test.py                # out-of-sample validation (both episodes)
python3 v08_wedge.py                   # the distributional wedge
```

Run any `vNN_*.py` from inside `src/`; each regenerates its figure and prints its
result. They import the engine (`model`, `pricers`, `events`) and data (`data.*`) as
sibling modules, so `src/` is the working directory.

## The one idea

Every version where we shaped an input to fit an output got **refuted by the next
version that fed real data**. The model reproduces the 2022-23 *and* 2024-25 episodes
on timing (peaks land on the right month, out-of-sample) and brackets them on
magnitude with a single commodity-owned slope — and the egg price spike lands **5.5×
harder** on the bottom income quintile than the top. Conservation holds to 1e-10
throughout. See `CHANGELOG.md` for how each result was earned (and where one was
briefly faked, then caught).

## Theoretical commitments

Stock-flow consistency (Godley & Lavoie); endogenous instability (Minsky, Keen);
complexity / out-of-equilibrium dynamics (Farmer & Foley, Santa Fe); money as
balance-sheet entries (MMT — Mosler, Kelton, Mitchell, Fullwiler); data as dispositive
(Keen). Inflation treated as *plural and regime-dependent* — demand-pull, cost-push,
sectoral propagation, distributional conflict — not a single demand-shaped lever.
