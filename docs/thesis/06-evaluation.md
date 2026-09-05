# 06 — How to evaluate this (the part a skeptic should hold us to)

*Part of the [Cybeersym thesis set](00-index.md). Bounded by [05 — limits & honesty](05-limits-and-honesty.md).*

The honest worry about any rich simulation: **with enough agents and parameters you can produce any
behaviour, so producing a plausible crash proves nothing.** Flexibility is not validation. We accept
that bar. This page is how to hold us to it — and how to *falsify* us.

## The bar the work must clear

1. **Out-of-sample reproduction.** Reproduce episodes/stylised facts the model was *not* tuned on,
   with the *same* frozen parameters. (Met, narrowly: the 2024‑25 HPAI egg episode was never fit; the
   model reproduced its price-peak *timing* with calibration frozen. That, not the in-sample fit, is
   the result that counts — and it is one commodity, two episodes.)
2. **Mechanism, not curve-fit.** A finding survives only if it holds across *independent* episodes
   for a *structural* reason — not because a coefficient was fit to one history. (The egg price–deficit
   slope is the same across both episodes; that consistency, honestly *including* where the single
   slope overshoots ep2, is the claim — not the fit to either alone.)
3. **Emergent stylised facts (for the network/classifier version).** The forthcoming distributed
   model will be judged on reproducing signatures it wasn't tuned to — fat tails, volatility
   clustering, measured bullwhip ratios — across regimes. Until it does, "reflects real-world
   dynamics" is a **goal, not a claim** ([08](08-future-work-roadmap.md)).

If the model reproduces what it wasn't shown, it is illustrative science. If it only reproduces what
it was tuned to, it is a painting. That difference is the entire point.

## What would falsify us (name it, so it's real)

- **A conservation assert fires** and the leak is real — a downstream result is invalidated.
- **Determinism breaks** (a result changes on rerun with σ=0) — it was a bug, not a finding.
- **The egg OOS fails on a genuinely new episode** — the timing mechanism was timestamp-tuned after all.
- **A composed-channel finding does not survive out-of-sample** on an independent episode — it was a
  curve-fit, and we retire it (the project has retired findings before — see `CHANGELOG.md`).
- **The classifier cannot beat a Markov-switching baseline on withheld data** — then the value stays
  *representational*, and [05](05-limits-and-honesty.md)/[08](08-future-work-roadmap.md) already
  reserve that outcome honestly.

## The internal falsification machinery

- **The reviewer gate** (builder ≠ reviewer; a fresh reviewer re-runs and re-derives before anything
  is *done*) — it has already dropped a would-be flagship whose strong claim was circular, and caught
  stated constants and self-overclaims about our own results ([`docs/reviewer-gate-log.md`](../reviewer-gate-log.md)).
- **Byte-exact nesting + conservation asserts** reject a change that breaks either.
- **Public + reproducible:** MIT, `github.com/Goldcap/Cybeersym`; deterministic (byte-identical
  reruns); the instruments and their self-tests shipped. Another researcher can inspect the
  definitions, validate the mathematics, reproduce the diagnostics, and attempt to falsify the
  assignment — which the [taxonomy principles](../../research/notes/concepts/taxonomy-principles.md)
  make the first obligation.

## Open threads

- **The strongest evaluation is one we haven't run:** withheld countries/episodes with a
  *pre-registered* signature set and decision rule (the discipline that stops us fooling ourselves).
  Small‑N makes it hard; that's why it's [08](08-future-work-roadmap.md), not a result.
- **"Falsifiable in principle" ≠ "falsified in practice."** Most of the debt-dynamics arc has not yet
  faced a real-data test that *could* kill it — it has faced only structural-robustness tests. That
  is a weaker bar, and we say so in [05](05-limits-and-honesty.md).

---

*Sources: [`THESIS.md`](../../THESIS.md) ("how to evaluate"); `CHANGELOG.md`; the taxonomy principles;
[`docs/reviewer-gate-log.md`](../reviewer-gate-log.md).*
