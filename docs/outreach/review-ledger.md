# Review ledger — bifurcation note (CYB-25)

The note (`bifurcation-note.md`) and this ledger change **together**, one PR per coherent
claim-change set. Reviewers read the **diff**, not a pasted copy, so everyone reviews the
same version of the paper. Merge a PR only when every substantive objection is either
**resolved** or **explicitly logged here as OPEN**.

## Comment classification

- **CORRECTNESS** — the stated claim is false / the map or invariant is misstated.
- **RIGOR** — the claim exceeds its evidence, or a proved/numerical/conjectural label is wrong.
- **CLARITY** — the claim is right but ambiguously or misleadingly stated.
- **STYLE** — presentation, notation, wording.
- **OPEN QUESTION** — a genuine unknown surfaced for the record (not a defect).

---

## Round 0 — internal referee pass (Claude, against `src/chaos/` at commit on this branch)

The note's every quantitative claim was checked by re-running the instruments
(`linearize.py`, `bcb_classify.py`) and reading `model.py`. Findings:

| # | Type | Target | Finding | Status |
|---|------|--------|---------|--------|
| R0-1 | CLARITY | §3.3 | The "0.91–0.95" range conflated **two different objects**: the equilibrium's transverse modulus (≈0.91–0.92 through onset, from the FP linearization / full 21-D spectrum) and the **one-sided border Jacobian** oscillatory plane (0.945 ∠39.5°, evaluated on the attractor at β=0.22, `bcb_classify.py`). Not a discrepancy — distinct evaluation points. | **RESOLVED** — §3.3 rewritten to separate the two; the note's own "must be resolved before circulation" flag is discharged. |
| R0-2 | CORRECTNESS | §1 | Map definition matches `model.py` exactly: 21-D CPA map, Gauss–Seidel downstream→upstream sweep, `d_{i+1}=R_i`, `Y_{i+1}` into tier i's delay line, `max(0,·)` order and `min(·,·)` ship borders. | CONFIRMED |
| R0-3 | CORRECTNESS | §2.1 | Interior equilibrium: every tier orders exactly μ=100 (far from order border), stockout margin ≈129 (far from ship border), ∀β through onset (β=0.40→0.28 verified). | CONFIRMED |
| R0-4 | RIGOR | §2.2 | The three λ=+1 eigenvalues are correctly labelled **proved** (the `C_i = O_i − ΣQ_i` first-integral argument is exact and structural), and confirmed numerically ε-robust (`#(λ=+1)=3` ∀β). | CONFIRMED (labelling correct) |
| R0-5 | CORRECTNESS | §3.1–3.4 | Λ_max≈0.054, amplitude jump 0→~525 over Δβ≈0.003, order clamp 42–56 %, ship clamp 24–27 %, hyperbolic |λ| tops ≈0.92 — all reproduced. | CONFIRMED |
| R0-6 | OPEN QUESTION | Figures | The note references `[Figure 1]` (bifurcation diagram) and `[Figure 2]` (transverse-spectrum-vs-β). A dedicated Figure 2 was **not yet a generated artifact**. | **RESOLVED** — both figures generated deterministically by `src/chaos/outreach_figures.py` (Fig 1 = down/up hysteresis sweep showing finite-amplitude onset + coexistence; Fig 2 = transverse |λ| vs β, ≈0.86→0.93, crosses onset β≈0.29 at ≈0.91, never reaching 1), embedded in the note with captions, and rendered to `bifurcation-note.pdf` (7 pp, MathJax). |

### Open questions carried forward

- _(none)_

### Resolved this round

- **R0-1** — the 0.91–0.95 ambiguity (see above).
- **R0-6** — both figures generated, embedded, and rendered to PDF.

---

## Round 1 — external review (PR: CYB-25)

Reviewers: Prof. Hu (external) · Claude (referee proxy) · Desktop.

| # | Reviewer | Type | Target (§) | Comment | Status |
|---|----------|------|------------|---------|--------|
| _ | _ | _ | _ | _(awaiting external review)_ | — |

---

*Standing invitations to the reviewer (note §0 / §5): (1) verify the §1 recurrence against
`src/chaos/model.py`; (2) is restriction to the conservation leaf 𝓛_c the correct first
reduction (§2.2)?; (3) challenge every use of "attractor / invariant / chaos /
border-collision / bifurcation"; (4) adjudicate the §4.4 / §5 open classification — is
"global nonsmooth bifurcation of a coexisting oscillatory attractor" an appropriate
provisional characterization?*
