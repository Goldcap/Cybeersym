# 07 — Lineage & history: whose shoulders, and the refutation arc

*Part of the [Cybeersym thesis set](00-index.md). The version-by-version detail is `CHANGELOG.md`;
this doc distils the intellectual lineage and the epistemics. Bounded by
[05 — limits & honesty](05-limits-and-honesty.md).*

## Whose shoulders

- **Stock-flow consistency** — Godley & Lavoie. Every financial asset is someone's liability; a
  write-off debits both sides. The accounting spine.
- **Endogenous instability** — Minsky (the Financial Instability Hypothesis) and **Keen** (existence
  proofs that crises arise from internal structure, not outside shocks). The debt-dynamics core is
  Goodwin–Keen's territory.
- **Complexity / out-of-equilibrium economics** — Santa Fe; Arthur; Farmer & Foley. Emergence as the
  subject, not the residual.
- **Money as balance-sheet entries** — MMT (Mosler, Kelton, Mitchell, Fullwiler): the conserved
  ledger *is* the issuer's balance sheet.
- **Data as dispositive** — Keen again: neoclassical theory lacks foundational data because the data
  would refute it. This project's entire discipline is the constructive form of that jab.
- **Chaos, modelled honestly as illustrative-not-predictive** — the numerical-weather-prediction
  tradition (Lorenz, ensemble forecasting).

Cybeersym aims to supply the half these traditions point at but have not built: the **mechanistic,
validated transmission model** that turns the accounting truths (which MMT has right) into the
*dynamics* (which everyone is thin on). Keen's models prove the instability *can* arise; the aim
here is to show a structurally-realistic economy *reproduces the specific signatures* of real
instability, out-of-sample — a bar not yet cleared (see [06](06-evaluation.md), [08](08-future-work-roadmap.md)).

## The refutation arc (the epistemics are the product)

The through-line, from `CHANGELOG.md`: **let real data refute the model, repeatedly.** Every version
that shaped an input to fit an output was caught by the next version that fed real data. A distilled
spine:

- **v0.3** — a beautiful 0.86 correlation on a *hand-shaped* cull bump.
- **v0.4** — the **real USDA cull series refuted it** (peaked the wrong month); exposed two missing
  mechanisms (seasonal demand; convexity).
- **v0.5–0.6** — timing solved from real culls + seasonality + one physical lag; then **validated
  out-of-sample** on the 2024‑25 episode the model was never fit to.
- **CYB‑7 / CYB‑9** — `replace_lag` *retired* for the real NASS flock series (timing survived and
  improved; magnitude degraded honestly); the pricer slope recalibrated on real deficits and shown
  to overshoot ep2 OOS — a compensating-error pair split into two correct values.
- **CYB‑14** — a saturation term **tested and rejected** (concavity within-noise at the path level;
  keep the parsimonious linear pricer).
- **The channel stack** — CYB‑17 → 19 → 23 → 30, each nesting the previous byte-exact; the Fisher
  work's **"two-basin / φ\*" headline was itself caught as a detector artifact and corrected** to the
  bounded-limit-cycle / structural-price-floor result.
- **The reviewer-gate era** (this session) — the checks became load-bearing: a stated constant off by
  a digit, a self-overclaim about our own results, and a would-be *flagship exhibit* whose strong
  claim was trivial/circular were all **caught before publication and dropped/fixed**
  ([`docs/reviewer-gate-log.md`](../reviewer-gate-log.md)).

The pattern is the point: the correlation is incidental; the *repeated refutation* is what licenses
any claim at all. A version that only reproduces what it was tuned to is a painting.

## Open threads

- **The refutation arc is strongest on eggs** (real data has repeatedly refuted it there). The
  debt-dynamics and classifier arcs have faced *structural-robustness* refutation, not yet *empirical*
  refutation — a weaker fire (see [05](05-limits-and-honesty.md)).
- **Honesty machinery is young.** The reviewer gate and escaped-defect log are new; whether they keep
  catching the recurring "overclaim about our own results" class, or whether it needs escalation, is
  itself under measurement (the log is the instrument).

---

*Sources: `CHANGELOG.md` (the full arc); `HANDOFF.md`; the module `docs/solutions/` learnings;
[`docs/reviewer-gate-log.md`](../reviewer-gate-log.md).*
