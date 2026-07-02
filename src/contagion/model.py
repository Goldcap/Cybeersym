"""
Cybeersym — CYB-19 Phase 2: default + an impairable rentier pool (the impairment horizon).  CYB-23.

Phase 1 (CYB-19) found the credit-crunch **bounds without curing** — a grinding limit cycle that
only chokes to ~12% because its Ponzi units survive by capitalizing uncovered interest
(`max(0, interest − margin)`) onto D. That pile can't grow forever. Phase 2 lets it terminate in
**default**, and makes the rentier pool **impairable** (it stops being a passive loss-absorber).

THE REFRAME (governs the build): **default is simultaneously the cure and the contagion vector.**
It *cures the borrower* (clears the debt that was feeding the cost channel → resets the grind) but
*impairs the lender* (a capital loss). Whether default heals or detonates is set by whether the
impaired lender feeds back — which we do NOT pre-decide. We SWEEP it.

ONE NEW MECHANISM (everything else is Phase 1 / CYB-17, reused unchanged; recovered byte-exact):

  FORK A — Trigger (default = release of Phase 1's accumulated pressure). The capitalized-interest
  pile `C` (Σ of the Ponzi capitalization Phase 1 already produced) builds; **default fires when it
  pushes net worth past a solvency bound**, `C ≥ thresh`. Not a bolt-on trigger — the terminus of
  the grind.

  FORK B — Magnitude/incidence (recovery rate + the SFC upgrade). A recovery-rate haircut
  `writeoff = (1 − recovery)·D` clears part of the debt; the write-off hits the rentier pool as a
  **capital loss**. This forces the accounting upgrade that is the whole SFC point: a write-off is
  a STOCK event. Conservation extends from Phase 1's flow identity to a full **capital-account
  reconciliation** — `ΔD = borrowing − repayment − writeoffs`; rentier wealth ↓ by the write-off;
  borrower-liability-↓ ≡ lender-asset-↓ (Godley–Lavoie: every asset is someone's liability).

  FORK C — Impairment→contraction elasticity `ε` (the cure↔cascade pivot; SWEPT [0, high]). The
  impaired rentier contracts credit: the solvency bound tightens with cumulative impairment,
  `thresh = solvency_frac·P − ε·impairment`. At ε=0 the rentier is a passive loss-absorber →
  default is a clean **cure**, the grind resets. At high ε → impairment lowers the bar → more
  default → more impairment → **contagion runaway**. Do NOT read in the result; the sweep exists
  to observe the horizon. Both cure and collapse must be reachable, or it's rigged.

  FORK D — Fisher price loop (Engine 2): GATED OFF (`fisher_on=False`). Engine 1 above is
  credit-QUANTITY contagion (no new price machinery). Engine 2 is the price-level Fisher loop
  (activity collapse → P down → real burden up); it opens a *second* route to collapse and stays
  off here so any collapse is honestly attributable — a contagion-collapse is NOT Fisher-deflation.

NESTED REGRESSION: recovery=1 (⇒ writeoff=0) ⇒ Phase 1 exactly; and crunch_enabled=False within
that ⇒ CYB-17. `CYB-17 ⊂ Phase 1 ⊂ Phase 2`, byte-exact at each shell. Determinism (σ=0).
"""
from dataclasses import dataclass, field
from pathlib import Path
import importlib.util as _ilu


def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_crunch = _load("crunch_model", "crunch/model.py")
CrunchEconomy, CrunchParams = _crunch.CrunchEconomy, _crunch.CrunchParams
AccommodationParams = _crunch.AccommodationParams


@dataclass
class ContagionParams:
    """Phase-1 crunch params + the Phase-2 default/impairment knobs."""
    crunch: CrunchParams = field(default_factory=CrunchParams)
    recovery: float = 1.0        # recovery rate; haircut = 1−recovery (recovery=1 ⇒ no write-off ⇒ Phase 1)
    solvency_frac: float = 0.50  # net-worth bound: default when the REAL capitalized-interest pile c ≥ solvency_frac
    elasticity: float = 0.0      # impairment→credit-tightening elasticity ε (the SWEPT horizon): the impaired
                                 #   rentier prices a risk premium  i_eff = i + ε·(impairment/P)  (credit gets
                                 #   dearer → more units tip Ponzi → the Engine-1 contagion feedback)
    fisher_on: bool = False      # Engine 2 (price-level Fisher) — GATED OFF
    fisher_flex: float = 0.0     # activity-collapse price decline per distressed step (Engine 2 only)


class ContagionEconomy:
    """Phase-1 crunch substrate + default + an impairable rentier pool. Composes an UNCHANGED
    `CrunchEconomy`; adds the capitalized-interest pile, the net-worth default trigger, the
    recovery-rate write-off, the impairment→contraction elasticity, and the full balance-sheet
    reconciliation. recovery=1 ⇒ byte-exact Phase 1."""

    def __init__(self, p: ContagionParams):
        self.p = p
        self.crunch = CrunchEconomy(p.crunch)
        self.c = 0.0                              # REAL capitalized-interest pile (Ponzi pressure / income)
        self.C = 0.0                              # nominal Σ capitalization (reported diagnostic)
        self.impairment = 0.0                     # cumulative rentier capital loss (a STOCK, nominal)
        self.rentier_wealth = self.crunch.acc.D   # the rentier's claim = the loan (asset = liability)
        self.i_base = self.p.crunch.acc.i         # policy rate before the impairment risk premium
        self.i_eff = self.i_base
        self.defaulted = False
        self.n_default = 0
        self.last_writeoff = 0.0
        self.last_pi = 0.0
        self.max_bs_residual = 0.0                # worst balance-sheet / capital-account residual
        self.collapsed = False                    # contagion runaway detected (premium/inflation diverges)
        self.collapse_step = None
        self._step = 0

    @property
    def i(self) -> float:
        return self.p.crunch.acc.i

    # ---- one financed, crunching, defaulting tick ------------------------------
    # contagion runaway is detected (not simulated to numerical overflow): once the premium spiral
    # ignites, inflation diverges super-exponentially; we FREEZE the economy the step it crosses a
    # blow-up threshold and mark it collapsed, so the collapse basin is observable, not a NaN crash.
    _PI_BLOWUP = 0.25        # >25%/step ⇒ the premium spiral has run away (hyperinflationary collapse)
    _I_CAP = 20.0            # cap i_eff so the frozen state stays finite

    def step(self) -> None:
        if self.collapsed:
            return                                # frozen after runaway (state held at the blow-up)
        self._step += 1
        acc = self.crunch.acc
        P_start = acc.conflict.P
        D_start = acc.D

        # --- FORK C: the impaired rentier prices a risk premium on the rate (Engine-1 contagion).
        # i_eff = i_base + ε·(impairment/P). ε=0 or no impairment ⇒ i_eff=i_base ⇒ byte-exact Phase 1.
        self.i_eff = min(self._I_CAP, self.i_base + self.p.elasticity * (self.impairment / P_start))
        acc.p.i = self.i_eff
        interest = self.i_eff * D_start           # interest owed this period (on start-of-period debt)

        self.crunch.step()                        # Phase 1 tick (classify → cascade → acc.step); asserts flows
        self.last_pi = self.crunch.last_pi
        if self.last_pi > self._PI_BLOWUP:        # runaway detected → freeze at the blow-up
            self.collapsed = True; self.collapse_step = self._step
        W, P = acc.conflict.W, acc.conflict.P
        D_acc = acc.D                             # debt after revolving/capitalization (acc's ΔD applied)
        # the rentier's claim tracks the revolving debt (borrowing − repayment nets to ΔD_acc)
        self.rentier_wealth += (D_acc - D_start)

        # --- FORK A: the capitalized-interest pile (Ponzi pressure), tracked in REAL terms so
        # inflation doesn't silently erode it: c carries over deflated by π, plus this step's cap/P.
        cap = max(0.0, interest - (P - W))        # = Phase 1's capitalized interest (Ponzi ⇒ >0)
        self.C += cap
        self.c = self.c * (P_start / P) + cap / P

        # --- FORK A/B: default when the pile breaches net worth → recovery-rate write-off (STOCK event) ---
        self.defaulted = False; writeoff = 0.0
        if self.c >= self.p.solvency_frac:
            writeoff = (1.0 - self.p.recovery) * acc.D
            if writeoff > 0.0:
                acc.D -= writeoff                 # borrower liability ↓
                acc.rentier_asset = acc.D
                self.rentier_wealth -= writeoff   # lender asset ↓ by the SAME amount (Godley–Lavoie)
                self.impairment += writeoff
                self.defaulted = True; self.n_default += 1; self.last_writeoff = writeoff
            self.c = 0.0                           # the default releases the accumulated pile

        # --- FORK D: Engine 2 (Fisher) — GATED OFF by default ---
        if self.p.fisher_on and self.crunch.crunch_active and self.p.fisher_flex > 0.0:
            acc.conflict.P *= (1.0 - self.p.fisher_flex)   # activity collapse pushes P down (Engine 2)

        self._assert_balance_sheet(acc.D)

    # ---- AC3: capital-account reconciliation (every asset is someone's liability) ----
    def _assert_balance_sheet(self, D_end) -> None:
        scale = max(1.0, abs(D_end), abs(self.crunch.acc.conflict.P))
        # (i) rentier asset ≡ firm liability, exactly (a write-off debits BOTH sides equally)
        r1 = abs(self.rentier_wealth - D_end) / scale
        # (ii) rentier pool's booked asset also tracks D
        r2 = abs(self.crunch.acc.rentier_asset - D_end) / scale
        self.max_bs_residual = max(self.max_bs_residual, r1, r2)
        assert r1 < 1e-9, f"CAPITAL-ACCOUNT LEAK: rentier wealth {self.rentier_wealth:.6f} ≠ firm debt {D_end:.6f}"
        assert r2 < 1e-9, "rentier pool asset ≠ firm debt after write-off"

    def run(self, n, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out

    # ---- pass-throughs ---------------------------------------------------------
    @property
    def conflict(self):
        return self.crunch.acc.conflict
    @property
    def acc(self):
        return self.crunch.acc
    @property
    def D(self) -> float:
        return self.crunch.acc.D
    @property
    def leverage(self) -> float:
        return self.crunch.acc.D / self.crunch.acc.conflict.P

    @property
    def max_residual(self) -> float:
        """Worst residual across the flow identity (Phase 1/CYB-17) AND the capital-account
        reconciliation (Phase 2)."""
        return max(self.crunch.acc.max_residual, self.max_bs_residual)
