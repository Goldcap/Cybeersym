---
artifact_contract: ce-unified-plan/v1
artifact_readiness: implementation-ready
product_contract_source: ce-brainstorm
execution: code
deepened: 2026-09-05
---

# Cybeersym Thesis Document Set - Plan

## Goal Capsule

**Objective.** Build a `docs/thesis/` **set of documents** that, when a skeptic comes in
challenging or probing the project's reasoning, hands them a TOC + outline and then exposition on
every axis we can anticipate — *and* records our own brainstorming (open questions, roads not
taken) for future reuse. It absorbs and expands the existing `THESIS.md` rather than duplicating
it, and it is anchored by a flagship **real-world worked example** showing how the approach
**augments** the current economics discipline (answers a question the standard local toolkit
structurally cannot), *without* claiming forecast superiority.

**Product authority.** Andy (final say on scope, framing, and what may be claimed).

**Open blockers.** None blocking planning. Two scope forks are recorded as Open Questions for
`ce-plan` (fate of `THESIS.md`; whether the flagship exhibit is built now or stubbed).

## Product Contract

### Context

- `THESIS.md` (461 lines) already carries ~80% of the argument: the one-sentence claim, the channel
  taxonomy, "why not the standard tools," "what this is NOT claiming," "how to evaluate," lineage.
  The new set **absorbs/expands** it — no duplication, no authority-shadowing.
- Source material to draw on (link, don't copy — the notebook/`docs` rule): `research/notes/concepts/`
  (`taxonomy.md`, `taxonomy-principles.md`, `phase-space-macroeconomics.md`,
  `parameterization-and-control-structure.md`), `docs/solutions/*`, `docs/empirical_grounding.md`,
  `docs/outreach/` (the bifurcation note), `CHANGELOG.md` (the version-by-version arc).
- Honesty discipline is the project's spine (the reviewer gate, `docs/reviewer-gate-log.md`,
  taxonomy-principles' reproducibility levels): every claim is labelled **demonstrated vs
  aspirational**, and the **descriptive/normative firewall** holds (no monetarism/policy verdict).

### Requirements

**R1 — A set of documents under `docs/thesis/`, TOC-first.** An index/front-door plus one file per
axis. Proposed set (final naming is a planning detail):
| # | doc | carries |
|---|---|---|
| 00 | index | TOC, one-sentence claim, who-reads-what, reading order |
| 01 | claim-and-argument | what we claim / don't (absorbs THESIS core) |
| 02 | method | SFC conservation + chaos instruments + real-data-as-referee; determinism |
| 03 | taxonomy-and-regimes | the regime classifier, class registry, domain-of-validity |
| 04 | augmenting-the-discipline | **the flagship**: a real-world worked example (below) |
| 05 | limits-and-honesty | not-claiming; the reproducibility ladder; the empirical gap named |
| 06 | evaluation | how to falsify us; the standard a skeptic should hold us to |
| 07 | lineage-and-history | Keen/Minsky/Godley–Lavoie/MMT/complexity + the "beautiful lie" refutation arc |
| 08 | future-work-roadmap | what we do now → the path to forecast-superiority; the gated items |

**R2 — Dual, co-equal in every doc.** Each axis carries *both* the polished defense *and* an "open
threads / where we're still unsure / roads not taken" part (the internal record lives inside each
doc, not a separate appendix).

**R3 — Doc 04 ARGUES augmentation (no worked exhibit — the on-hand one was built, gated, and
DROPPED).** A reviewer-gated attempt to *show* augmentation on the Fisher model was found
trivial/circular: it reduced to a re-illustration of the **Lucas critique** on an authored DGP, with
a mislabeled "deflation" border (actually the CYB-30 bounded limit cycle) and an out-of-support
regression extrapolation. So doc 04 makes the honest **argument**, not a demonstration: the Phillips
curve is local-by-construction; a good in-regime fit has no term for the structural parameter, so it
cannot locate its own domain-of-validity border (an instance of the Lucas critique + its constructive
corollary); concede where classical tools win; name the real competitor; state the honest boundary —
**representational/diagnostic value, NOT forecast superiority.** A genuinely non-circular
*demonstration* needs independent/held-out data + a real classifier → deferred to doc 08 (future
work). Neutral framing — **no named person.**

**R4 — Concede where the mainstream wins.** Doc 04/05 explicitly grant the turf: forecasting the
egg spike; the linearization-safe regime (taxonomy A1). Credibility comes from the concession.

**R5 — The honest comparative boundary is stated plainly.** "We can *represent* and *diagnose* what
linearized-around-a-unique-equilibrium models cannot; we have **not** shown we beat a
Markov-switching VAR out-of-sample." Name the real competitor (regime-switching econometrics +
central-bank ABMs + post-Keynesian SFC), not the textbook. Note the frontier is converging.

**R6 — The roadmap (doc 08) stages the ambition.** What we already do → exactly the out-of-sample
/ forecast-superiority test we'd have to pass and haven't (the withheld-episode validation) → the
classifier arc (CYB-26→29) → gated items (CYB-13, CYB-16). Turns the gap into a stated agenda.

**R7 — Reviewer gate on the economics.** The whole set goes through a Linear ticket + the reviewer
gate (`CLAUDE.md` §"The reviewer gate"), whose reviewer specifically **fact-checks the economics
claims** (SMD, Lucas critique, Markov-switching, central-bank ABMs, the characterizations of
mainstream positions) — the class of claim most likely to contain a "whoops."

### In scope

The 9-doc set; the flagship worked example and its framing; absorbing/expanding `THESIS.md`;
linking (not copying) the notebook + `docs`; the honesty labelling throughout.

### Out of scope (explicit)

- **The forecast-superiority *proof* itself** (out-of-sample horse-race vs a VAR) — that is doc 08's
  *future work*, deliberately **not** claimed or built here.
- **Any normative/policy verdict** (the monetarism critique, CYB-16) — firewalled.
- **New economic modeling** beyond what the flagship exhibit minimally needs.

### Acceptance / success criteria

- A skeptic can enter at the TOC, find the axis they want to probe, and get a straight answer plus
  our honest uncertainty on it.
- Every claim is labelled demonstrated / aspirational; the empirical gap is stated, not hidden.
- The flagship shows the diagnostic gap concretely (a runnable exhibit or a clearly-figured
  walk-through), framed as augmentation, no named person.
- The reviewer gate's economics fact-check passes (or its findings are resolved) before merge.
- `THESIS.md` and the set are consistent — no contradictory or duplicated claims.

### Key decisions (session-settled)

- **Dual, co-equal** defense + internal record — `session-settled` (Andy, 2026-09-05).
- **A set of documents** (`docs/thesis/` folder), not one file — `session-settled`.
- **Flagship = diagnostic/representational superiority**, not forecast superiority — `session-settled`.
- **Neutral framing**, no named commentator ("augment the discipline with a real-world example") — `session-settled`.
- **A `future-work` roadmap doc** stages the forecast-superiority ambition honestly — `session-settled`.
- **Absorbs/expands `THESIS.md`**; honesty ladder + descriptive/normative firewall; **ticket +
  reviewer gate with an economics fact-check** — `session-settled`.

### Open questions

- **RESOLVED — flagship build depth + scenario (Andy, 2026-09-05):** build the **runnable exhibit
  now**, on the **on-hand Fisher model (CYB-30)**. Fit a simple Phillips curve / small VAR to the
  Fisher model's output and *show* the classical fit is confidently stable while our model flags the
  one-parameter sign-flip + a critical-slowing-down early-warning. Treated as a real sub-build (fit +
  validate + figures), under the reviewer gate.

Resolved in planning:
1. **Fate of `THESIS.md`** — keep it as the **top-level front-door summary** that links into
   `docs/thesis/`; `01-claim-and-argument` carries the full argument. `THESIS.md` slims to
   summary + map, reconciled so it never contradicts or duplicates 01.
2. **Internal-record weight per doc** — each doc carries a **capped** `## Open threads` section (a
   few bullets: where we're unsure / roads not taken), never a sprawling record that drowns the defense.

---

## Product Contract preservation

Product Contract (R1–R7, scope, acceptance, key decisions) **unchanged** — this enrichment adds the
HOW only; all IDs preserved.

---

## Planning Contract

**Approach.** A `docs/thesis/` folder of 9 short, cross-linked docs (00–08), each dual (defense +
capped Open threads), fronted by a slimmed `THESIS.md`. The flagship (04) is written *from* a
runnable exhibit built first (U5). Everything **links, never copies** the canonical sources (`src/`,
`docs/solutions/`, the research notebook, `CHANGELOG`). numpy + matplotlib only.

**Key technical decisions.**
- **KTD1 — Doc 04 is ARGUMENTATIVE; NO built exhibit** (REVERSED — supersedes the earlier
  build-the-exhibit-first decision). The on-hand exhibit was built and reviewer-gated over two
  attempts; the gate found the strong claim **trivial/circular** (it re-illustrates the Lucas
  critique on an authored DGP; mislabeled the CYB-30 bounded limit cycle as "deflation"; leaned on
  out-of-support regression extrapolation). **Dropped** — no `src/thesis_exhibit/`. The honest
  surviving point is argued in prose (R3): Lucas cited, the authored-model limit owned, a genuine
  demonstration deferred to doc 08. (The prior KTD2 "numpy classical baselines" and KTD3
  "structural-blindness exhibit" are now **moot** — no build.)
- **KTD4 — Honesty labels are structural:** every load-bearing claim tagged demonstrated /
  aspirational; the descriptive–normative firewall is a standing section (05).

---

## Implementation Units

**Sequencing (predicate order — revised after the exhibit was dropped).** Doc 04 (U6) is no longer
built from a demonstration; its honest claim *cites the boundary* (doc 05 / U7) and *defers the real
"more informative" demonstration to the roadmap* (doc 08 / U10). So **05 and 08 are predicates for
04** — they must exist first, or 04 has nothing honest to point at. Run order:

> **U1** (scaffold + index + `THESIS.md` front-door) → **U7** (05 limits-and-honesty) + **U10** (08
> future-work roadmap) → **U6** (04 augmenting-the-discipline, argumentative) → the remaining axis
> docs **U2 / U3 / U4 / U8 / U9** → **U11** (reviewer gate + CYB-36 + PR).

U-IDs are stable (never renumbered); this list is the run order, not the numbering. No feature-bearing
unit remains (the exhibit U5 was dropped) — the whole set is prose under the U11 reviewer gate.

### U1. Scaffold `docs/thesis/` + index + THESIS.md front-door
- **Goal.** Create `docs/thesis/00-index.md` (TOC, one-sentence claim, who-reads-what, reading order)
  and reslim `THESIS.md` into a front-door summary that links into the set.
- **Requirements.** R1.
- **Dependencies.** none.
- **Files.** `docs/thesis/00-index.md` (new); `THESIS.md` (modify — add a "full thesis: docs/thesis/"
  map, ensure no claim contradicts the set).
- **Approach.** 00-index is the navigation spine; lists 01–08 with a one-line "what it carries" + a
  "start here if you're a {mathematician / economist / future collaborator}" router.
- **Test expectation: none — docs scaffolding.** Verification: every 01–08 link resolves; `THESIS.md`
  and 00-index agree on the one-sentence claim.

### U5. ~~Build the flagship exhibit~~ — DROPPED (reviewer-gated out; see KTD1 / R3)
**Status: DROPPED.** Built and reviewer-gated over two attempts; the gate ruled the strong "more
informative" claim **trivial/circular** (re-illustrates Lucas on an authored DGP; mislabeled the
CYB-30 bounded limit cycle as "deflation"; out-of-support regression extrapolation). `src/thesis_exhibit/`
removed. The honest point is argued in doc 04 (U6); a non-circular demonstration (real classifier on
independent/held-out data) is deferred to doc 08 (U10). Logged at U11. The build spec below is
retained only as the record of what was tried and why it didn't hold.

- **Goal.** A runnable script that fits classical baselines **in the inflation basin** of the on-hand
  Fisher/contagion structure (where they are confident and well-behaved), then *shows* the SAME
  structure one structural step away (α_p/φ) is a deflation regime the fit **cannot represent** — the
  local fit's confidence is false near a regime border our classifier maps. Produces the figures doc
  04 reports. (Reshaped from a smooth-flip+CSD exhibit the model doesn't honestly support — log #3.)
- **Requirements.** R3, R4, R5.
- **Dependencies.** U1. Reuses `src/fisher/` (and `src/contagion/` if cleaner) read-only.
- **Files.** `src/thesis_exhibit/augmentation_demo.py`, `src/thesis_exhibit/test_augmentation_demo.py`,
  `src/thesis_exhibit/figures/*`, `src/thesis_exhibit/README.md` (all new). `src/fisher/` untouched.
- **Approach.**
  1. Pick the structural parameter that indexes the basin (markup-defense α_p, or the ε-vs-φ balance)
     and two settings: an **inflation-basin** setting (stable, mean π>0 grind) and a **deflation**
     setting one structural step away.
  2. Fit the classical baselines (KTD2 — numpy OLS Phillips + small VAR via `lstsq`) on the
     inflation-basin series; report a **good in-sample fit + a confident forward projection** (Δp>0).
  3. Show the SAME classical model has no α_p/φ term, so applied at the deflation setting it still
     projects inflation — it is **structurally blind** to the border. Overlay our model's basin map
     (the deflation regime is one structural step away) that the fit cannot see.
  4. Frame it as *false confidence at a border*, not *missing term*: the fit looks complete and
     well-behaved in-basin, which is exactly why it can't warn you.
- **Patterns to follow.** `src/fisher/run_v0.py` / `run_v1.py` figure style; `numpy.linalg.lstsq`.
- **Test scenarios** (`test_augmentation_demo.py`):
  - The classical fit on the inflation-basin series is genuinely good (small in-sample residuals) and
    its forward projection is confidently inflationary (Δp>0 across the horizon).
  - That same fit, applied at the deflation setting, still projects Δp>0 while the true regime is
    deflationary — the fit is blind to the border (assert the sign mismatch).
  - Determinism: byte-identical reruns (σ=0).
  - Honesty guard: NO out-of-sample forecast-accuracy metric and NO manufactured
    critical-slowing-down signal are computed (assert the demo exposes only the structural-blindness contrast).
- **Verification.** `python3 augmentation_demo.py` runs green + deterministic, emits the figures;
  `src/fisher/` unmodified (git clean).

### U6. Doc 04 — augmenting-the-discipline (ARGUMENTATIVE; no exhibit)
- **Goal.** The flagship doc, made honest: concede where classical tools win (R4); Phillips-is-local
  by construction; **cite the Lucas critique explicitly** and position our point as its constructive
  corollary (structural models can supply an ex-ante domain-of-validity map a good local fit cannot);
  name the real competitor (regime-switching + central-bank ABMs + SFC); state the honest boundary
  (R5 — representational, not forecast). Neutral framing, no named person.
- **Requirements.** R3, R4, R5, R2.
- **Dependencies.** U1, **U7 (05 limits — the boundary 04 cites), U10 (08 roadmap — where 04 defers
  the real demonstration).** Both are predicates; write 04 after them. (No longer depends on U5.)
- **Files.** `docs/thesis/04-augmenting-the-discipline.md` (new).
- **Approach.** Lead with the concession; make the local-vs-global argument; cite Lucas and **own
  that a *demonstration* on a model we authored would be circular** (why we don't claim one); state
  the claim precisely (*answers, ex ante, what theirs structurally can't*, NOT *forecasts better*);
  Open threads = the non-circular demonstration we'd need (a real classifier + independent/held-out
  data) → doc 08.
- **Test expectation: none — prose.** Verification: reviewer-gate **economics fact-check** (U11) —
  especially that the Lucas relationship is stated honestly and no over-claim slips back in.

### U2 / U3 / U4 / U7 / U8 / U9 / U10. The remaining axis docs
- **Goal.** One doc each — dual (defense + capped Open threads), absorbing/expanding `THESIS.md`,
  linking (not copying) canonical sources:
  - **U2** `01-claim-and-argument` (absorbs THESIS core) — R1, R2.
  - **U3** `02-method` (SFC conservation + chaos instruments + real-data-as-referee; determinism) — R1, R2.
  - **U4** `03-taxonomy-and-regimes` (classifier, class registry, domain-of-validity; link `taxonomy.md`) — R1, R2.
  - **U7** `05-limits-and-honesty` (not-claiming; reproducibility ladder; empirical gap named; the
    descriptive/normative firewall) — R2, R4, R5, KTD4.
  - **U8** `06-evaluation` (how to falsify us; the skeptic's standard: OOS, mechanism-not-curve-fit) — R2.
  - **U9** `07-lineage-and-history` (Keen/Minsky/Godley–Lavoie/MMT/complexity + the "beautiful lie"
    refutation arc; distill `CHANGELOG.md`) — R2.
  - **U10** `08-future-work-roadmap` (what we do now → the forecast-superiority proof we'd have to
    pass and haven't → a model-free **critical-slowing-down early-warning** (aspirational — not
    demonstrated on the current abrupt-collapse model; needs a slow-manifold substrate) → classifier
    arc CYB-26→29 → gated CYB-13/16) — R6.
- **Dependencies.** U1.
- **Files.** `docs/thesis/{01,02,03,05,06,07,08}-*.md` (new).
- **Test expectation: none — prose.** Verification: links resolve; every claim labelled demonstrated/
  aspirational; no contradiction with `THESIS.md` or canonical sources; reviewer gate (U11).

### U11. Reviewer gate + Linear (CYB-36) + PR
- **Goal.** Run the standing reviewer gate (CLAUDE.md §"The reviewer gate") with an **economics
  fact-check**; resolve findings; file/confirm CYB-36; open the PR.
- **Requirements.** R7.
- **Dependencies.** U1–U10.
- **Files.** `docs/reviewer-gate-log.md` (append the entry).
- **Approach.** A FRESH reviewer (builder≠reviewer) that (a) re-runs U5's exhibit and re-derives its
  claims, (b) **fact-checks the economics** (SMD, Lucas critique, Markov-switching, central-bank ABMs,
  the characterizations of mainstream positions — the class most likely to contain a whoops), (c)
  checks every claim is labelled and the firewall holds. HOLD + surface anything unresolved; log the run.
- **Test expectation: none — process.** Verification: findings resolved; CYB-36 linked; PR open.

---

## Verification Contract

- U5 exhibit runs green + deterministic; `src/fisher/` untouched (git clean).
- Every 00–08 cross-link and every canonical-source link resolves.
- Every load-bearing claim carries a demonstrated / aspirational label; the descriptive–normative
  firewall section is present (05); the forecast-superiority claim is made **nowhere** (it lives in
  08 as future work).
- The reviewer gate's economics fact-check passes (or findings resolved); logged in `docs/reviewer-gate-log.md`.
- `THESIS.md` and the set are consistent — no contradictory or duplicated claims.

## Definition of Done

The 9-doc set + slimmed `THESIS.md` front-door are written and cross-linked; the flagship exhibit
(U5) is built, green, and reported in doc 04; every honesty label and the firewall are in place; the
reviewer gate ran with an economics fact-check and its findings are resolved; CYB-36 is linked and a
PR is open for Andy's merge.
