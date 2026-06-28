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
src/bullwhip/   standalone bullwhip module — the recursion channel (own README)
docs/plans/     implementation specs/plans  (Compound Engineering convention)
docs/solutions/ solved-problem learnings, searchable before new work
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

## Docs & workflow

Work is planned in **Linear** (team **Cybeersym / `CYB`**) and mirrored into version
control under a [**Compound Engineering**](https://github.com/EveryInc/compound-engineering-plugin)
docs convention — two folders, each with YAML frontmatter so they're machine-searchable:

- **`docs/plans/`** — one spec/plan per feature, `YYYY-MM-DD-<type>-<slug>-plan.md`
  with `title / type / status / date` frontmatter. The **Linear ticket is the
  canonical spec**; the plan file is its version-controlled mirror — spec changes
  happen in Linear first, then sync here. Each plan closes with the *shipped outcome*
  (final numbers + commit), so the doc records what was built, not just what was hoped.
- **`docs/solutions/`** — one reusable **learning** per file (a refuted assumption, a
  non-obvious fix, a pattern), with richer frontmatter (`category / tags / component /
  root_cause / …`). These are meant to be read *before* the next build, so mistakes
  compound into knowledge instead of repeating. This is the "compound" in compound
  engineering.

The split mirrors this repo's method: a **plan** is the hypothesis, a **solution** is
what survived contact with the data. Example — the bullwhip module (`src/bullwhip/`)
was specced in `docs/plans/2026-06-28-feat-bullwhip-v0-recursion-channel-plan.md`
(tracking `CYB-1`) and its learnings captured in
`docs/solutions/bullwhip-seeing-is-not-acting.md`.

> **Multi-agent note.** This repo is worked by more than one Claude (Claude Code in the
> terminal, Claude Desktop in chat). Linear is the shared channel: tickets carry the
> canonical spec, comments carry the back-and-forth (each agent signs its comments). The
> repo holds code + committed results; Linear holds the live spec and discussion.

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
