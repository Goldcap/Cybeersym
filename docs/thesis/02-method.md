# 02 — Method: conserved substrate, validated instruments, data as referee

*Part of the [Cybeersym thesis set](00-index.md). Bounded by [05 — limits & honesty](05-limits-and-honesty.md).*

The method is the actual product. It is a small set of disciplines that, held together, let a
simulation make **falsifiable** claims about dynamics instead of pretty pictures.

## 1. A conserved, stock-flow-consistent substrate

Every model is a stock-flow-consistent (Godley–Lavoie) system: money and goods are **conserved to
machine precision** (residuals < 1e‑10), asserted on every step. Conservation is the crown jewel —
if the asserts fire, work stops until the leak is fixed, because a leak invalidates everything
downstream. This is the **Godley–Lavoie accounting spine** — every financial asset is a matching
liability. (It touches MMT's *territory*, but the base engine models a private household↔firm↔store
circuit with **no currency-issuer sector**, so this is the consolidated-ledger identity, not MMT's
issuer claim.)

Consequence, not decoration: conservation makes the equilibrium **structurally non-hyperbolic** (a
permanent center subspace, ∀ parameter), so a conserved-ledger economy does **not** lose stability
the textbook way — its instabilities are *global*, born at finite amplitude alongside a still-stable
equilibrium (CYB‑2/4; [03](03-taxonomy-and-regimes.md)). The rigor that makes it honest is what
places it outside the standard local-bifurcation toolkit.

## 2. The engine is commodity-blind; the commodity carries its own physics

The SFC engine (`src/model.py`) never knows it is pricing eggs. A commodity names a **pricer** (a
pure function of the flow gap) and carries its own slope; adverse events are pure path-transforms in
a plugin registry. New commodities/events/channels slot in at registries **without touching the
engine** — the seams are the point, and validation happens *at* them.

## 3. Real series in, never hand-drawn shapes

The refuting discipline: **feed real data** (FRED egg prices, USDA/NASS culls + the real flock
series, seasonality). Every version of this project that shaped an input to fit an output was
refuted by the next version that fed real data — the recorded history in `CHANGELOG.md` is a chain of
such refutations (the "beautiful lie" lesson). If a series must be stylised, it is flagged loudly and
the result treated as provisional.

## 4. Instruments, self-tested on known answers first

Dynamical claims are **measured**, not asserted. The instrument suite (`src/chaos/`: Lyapunov,
bifurcation, linearisation, border-collision) is self-tested on closed-form cases before it is
trusted — the logistic map's λ = ln 2, and the **Goodwin–Keen rung** (CYB‑33), where the tools
recover a conservative centre and Keen bistability against analytic answers. An instrument is not
pointed at the real substrate until it passes its hydrogen-atom test.

## 5. Determinism, nesting, and the reviewer gate

- **Determinism** (σ=0): same inputs → same outputs, guarded as a property; if it breaks, that's a bug.
- **Byte-exact nesting:** every composed module reproduces its parent exactly with the new mechanism
  off (`CYB‑17 ⊂ P1 ⊂ P2 ⊂ P2b`, etc.) — so a finding is attributable to *one* new mechanism.
- **The reviewer gate** ([`CLAUDE.md`](../../CLAUDE.md)): no result is *done* until a fresh,
  independent reviewer re-runs it and re-derives its claims (builder ≠ reviewer). The
  [escaped-defect log](../reviewer-gate-log.md) records what slips through and escalates the checks.

## The stance in one line

**Validate the *mechanism* across independent episodes; stay illustrative, not predictive; and never
claim to detect chaos in macro data directly** (the honesty firewall — see
[`docs/empirical_grounding.md`](../empirical_grounding.md), which documents why the 1980s–90s
detection programme failed).

## Open threads

- **The instruments are validated on benchmarks, not yet on the real coupled substrate** — that is
  the classifier arc ([08](08-future-work-roadmap.md)).
- **Conservation guarantees honesty, not relevance.** A perfectly-conserved model can still be the
  wrong model; only out-of-sample data settles that.

---

*Sources: [`THESIS.md`](../../THESIS.md); `src/model.py`, `src/pricers.py`, `src/events.py`,
`src/chaos/`; `docs/empirical_grounding.md`; `CHANGELOG.md`; `docs/reviewer-gate-log.md`.*
