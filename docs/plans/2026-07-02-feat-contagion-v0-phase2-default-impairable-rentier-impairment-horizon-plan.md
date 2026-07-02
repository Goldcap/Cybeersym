---
title: "feat: CYB-19 Phase 2 — default + impairable rentier pool; the impairment horizon (cure vs contagion-collapse), Fisher gated"
type: feat
status: done
date: 2026-07-02
tracking: CYB-23
canonical_source: "Linear CYB-23 (https://linear.app/techno87/issue/CYB-23)"
depends_on: [CYB-17, CYB-19]
---

# feat: CYB-19 Phase 2 — default + impairable rentier pool

> **Canonical spec lives in Linear (CYB-23).** Forks resolved by Desktop (scoping + Fork C
> confirmed by Andy). Mirror into version control; shipped outcome at the bottom.

## Goal

Let Phase 1's grind terminate in **default**, and make the rentier pool **impairable**. Headline:
the **impairment horizon** — sweep the impairment→contraction elasticity and find where default's
clean CURE flips to CONTAGION-COLLAPSE. Both must be reachable or it's rigged.

## Two engines — one wired, one gated

* **Engine 1 (WIRED)** — credit-quantity contagion: the impaired rentier prices a risk premium on
  the rate (`i_eff = i + ε·impairment/P`); dearer credit → more Ponzi → default cascade.
* **Engine 2 (GATED OFF)** — price-level Fisher (activity collapse → P down → real burden up).
  Kept off so a contagion-collapse is not mislabeled Fisher-deflation.

## Acceptance criteria (all met — see outcome)

1. Default fires from Phase 1's accumulated pressure (pile → net-worth breach).
2. Impairment-horizon map (ε × recovery): cure ↔ collapse, both reachable, discover the boundary.
3. Balance-sheet / capital-account reconciliation < 1e-9 through the transient (STOCK write-offs).
4. Cure demonstrated or honestly negated.
5. Nested regression CYB-17 ⊂ P1 ⊂ P2 byte-exact.
6. Fisher gate present but OFF + demand-channel-strength verification (yes/no).
7. Determinism.

## Discipline guard

Do NOT read in the expected result (Andy's instruction) — sweep the horizon and observe. Both
cure and collapse reachable. Keep the descriptive/normative firewall (CYB-16 not built here).

---

## Outcome (shipped)

Delivered `src/contagion/{model.py, run_v0.py, README.md, 3 figures}`. All seven met.

1. **Default is the terminus of the grind.** The real capitalized-interest pile sawtooths to the
   net-worth bound; each default releases it (not a bolt-on trigger).
2. **Impairment-horizon map (headline).** ε=0 → CURE (loss absorbed, grind bounded ~1.2%/step);
   ε high → CONTAGION-COLLAPSE (risk-premium spiral → hyperinflation). Both reachable. The frontier
   is **ragged** because two feedbacks compete — impairment→premium→more-Ponzi (contagion) vs
   inflation→P↑→impairment/P↓ (self-cure via inflation eroding the real impairment).
   **Counterintuitive:** LOWER recovery (bigger haircut) collapses LESS (5% vs 62%) — clearing more
   debt per default cures faster than the extra impairment detonates.
3. **Capital-account reconciliation** (Godley–Lavoie: rentier asset ≡ firm liability; write-offs as
   STOCK events) closes to `≤ 4e-12` across the whole map, through defaults AND collapses.
4. **Cure demonstrated, honestly bounded.** ε=0 = clean loss-absorption (grind stays bounded); on
   the revolving-wage-fund substrate the write-off reverts, so cure does NOT beat the grind floor —
   the genuinely new outcome is the contagion collapse. (Honest negation of the strong-cure claim.)
5. **Nested regression byte-exact:** recovery=1 ⇒ Phase 1 (`0.0`); +crunch-off ⇒ CYB-17 (`0.0`).
6. **Fisher gated OFF; verification delivered.** CYB-17's demand channel damps π to 0 but never
   negative ⇒ Engine 2 needs a STRENGTHENED price mechanism (Phase 2b), not a switch-on. (Switch is
   wired — forcing it on does deflate P.)
7. **Determinism** — byte-identical reruns.

Learning: [`../solutions/contagion-impairment-horizon-cure-vs-collapse-bigger-haircut-stabilizes.md`](../solutions/contagion-impairment-horizon-cure-vs-collapse-bigger-haircut-stabilizes.md).
