"""
Cybeersym — accommodation module (the first SUSTAINING channel), v0.  CYB-17.

CYB-6 (conflict) produced an **unbounded** nominal runaway for gap g>0. That "unbounded"
was never a law of the conflict mechanism — it was the **full-accommodation limit** hiding
in plain sight: CYB-6 has no money and no credit, so nothing had to be financed and nothing
could choke. This module names that hidden constraint. It requires the nominal **wage bill
to be financed** by credit at a **policy rate `i`** (working-capital / wage-fund finance;
circuit theory, Graziani), and asks two neutral questions:

  H1a — once the wage bill must be financed, is CYB-6's runaway still unconditional, or does
        a high enough `i` bound it? (accommodation as the *sustaining condition*.)
  H1b — when `i` moves inflation, through WHICH channel does it act?

THE RATE'S THREE CHANNELS (all present; the decomposition is the headline — fewer than three
would rig the answer):
  * COST (inflationary): interest is a cost of production; firms defend margin NET of
    interest ⇒ higher `i` raises the effective gap. Strength `cost_c`.
        ω_f_eff = ω_f0 − cost_c · int_share     (int_share = i·D/P)
  * DEMAND (symmetric, disinflationary): higher `i` → slack → damps claim adjustment on
    BOTH sides equally. Strength `demand_b`.
        α_w_eff = α_w0·(1 − demand_b·slack),   α_p_eff = α_p0·(1 − demand_b·slack)
  * DISTRIBUTIONAL (asymmetric-on-labor, disinflationary): the same slack breaks the
    workers' side (unemployment) — lowers ω_w, moving the gap in capital's favor. Strength
    `distrib_a`.        ω_w_eff = ω_w0 − distrib_a·slack
  slack(i) = i (rate-induced slack; a v0 linear map).

The decomposition turns on SYMMETRY: demand cools both sides (rate down, distribution
unchanged); distributional breaks labor's side (rate down AND ω* toward ω_f); cost feeds
(rate up). Reporting which dominates is the deliverable — every outcome is a valid finding.

SFC — a minimal PASSIVE rentier-bank pool. Firms finance the wage bill; debt stock `D`
(revolving wage fund + capitalized uncovered interest); interest flow `i·D` is income to the
rentier pool whose asset = `D`. The conserved flow identity EXTENDS from CYB-6's
wage+profit=1 to **wage share + interest share + retained-profit share = 1** (retained is the
residual claimant, now after both wages and interest). Debt bookkeeping ΔD = borrowing −
repayment is asserted.

SWITCHING MANIFOLDS — the set completes. Order non-negativity (CYB-2), conservation clamp
(CYB-4), wage floor (CYB-6), and now the **solvency ceiling** `D/P ≤ D_max`: accommodation is
elastic at rate `i` up to a creditworthiness limit, then rationed (the wage bill can't be
financed → wage growth capped). A static tripwire in v0; the Minsky cascade that fires off it
is deferred. A monetarist money-growth cap `μ` is included as a comparison switch — the
quantity lever physically in the room, to be shown inert or not, not asserted dead.

DISCIPLINE: `i>0` and `D_max` finite are ALWAYS a restraint — but a restraint present is not
a restraint sufficient. The model can produce a spiral that OUTRUNS the rate (cost channel
strong / claims stubborn). Determinism (σ=0, pure function of state). At `i→0`, `D_max→∞`,
cost off, it reproduces CYB-6 byte-for-byte (the load-bearing regression).
"""
from dataclasses import dataclass
from pathlib import Path
import importlib.util as _ilu

def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_cm = _load("conflict_model", "conflict/model.py")
ConflictEconomy, ConflictParams = _cm.ConflictEconomy, _cm.ConflictParams


@dataclass
class AccommodationParams:
    # --- CYB-6 base substrate (bare conflict layer) ---
    omega_f: float = 0.65
    gap: float = 0.10                 # g0 = ω_w − ω_f  (control knob; g>0 = incompatible)
    alpha_w: float = 0.30
    alpha_p: float = 0.30
    dt: float = 1.0
    wage_floor: bool = True
    trigger: float = 0.10
    # --- accommodation: the policy rate and its three channels ---
    i: float = 0.0                    # policy rate (the conditioning parameter)
    cost_c: float = 1.0               # cost-channel strength (interest into effective gap)
    demand_b: float = 0.0             # symmetric-demand strength (damps both α's)
    distrib_a: float = 0.0            # distributional strength (labor-asymmetric slack → ω_w)
    # --- the solvency ceiling (accommodation's nonsmooth border) ---
    D_max: float = 1e18               # creditworthiness limit on D/P (∞ ⇒ never binds)
    # --- monetarist comparison switch ---
    mode: str = "horizontalist"       # "horizontalist" (rate lever; quantity inert) | "monetarist"
    mu: float = 1e18                  # money(≈wage-bill)-growth cap, monetarist mode only

    @property
    def omega_w(self) -> float:
        return self.omega_f + self.gap


class AccommodationEconomy:
    """Bare CYB-6 conflict layer + a working-capital financing loop. Composes an unmodified
    `ConflictEconomy` and drives its EFFECTIVE targets/speeds each step from the rate `i`,
    the interest share, and the induced slack (so `i→0`, cost off recovers CYB-6 exactly)."""

    def __init__(self, p: AccommodationParams):
        self.p = p
        # base (fixed) conflict targets/speeds; the rate perturbs *effective* copies of these
        self.omega_f0 = p.omega_f
        self.gap0 = p.gap
        self.omega_w0 = p.omega_f + p.gap
        self.alpha_w0 = p.alpha_w
        self.alpha_p0 = p.alpha_p
        self.conflict = ConflictEconomy(ConflictParams(
            omega_f=p.omega_f, gap=p.gap, alpha_w=p.alpha_w, alpha_p=p.alpha_p,
            dt=p.dt, wage_floor=p.wage_floor, trigger=p.trigger))
        # debt stock: firms revolve the wage fund. Start = the initial wage bill.
        self.D = self.conflict.W
        self.rentier_asset = self.D            # passive bank: asset = the loan
        self.last_int_share = 0.0
        self.last_pi = 0.0
        self.solvency_bound = False            # solvency ceiling active this step?
        self.max_residual = 0.0

    # ---- shares (three-way flow split) -------------------------------------
    @property
    def omega(self) -> float:
        return self.conflict.omega
    @property
    def int_share(self) -> float:
        return self.p.i * self.D / self.conflict.P
    @property
    def retained_share(self) -> float:
        return 1.0 - self.omega - self.int_share      # residual claimant, after wages AND interest

    def _assert_conserved(self, borrowing, repayment, D_next) -> None:
        # (a) three-way flow identity: wage + interest + retained = 1
        total = self.omega + self.int_share + self.retained_share
        # (b) debt stock-flow identity: ΔD = borrowing − repayment; rentier asset = D
        d_resid = abs(D_next - (self.D + borrowing - repayment))
        scale = max(1.0, abs(self.D), abs(self.conflict.P))
        r1 = abs(total - 1.0)
        r2 = d_resid / scale
        self.max_residual = max(self.max_residual, r1, r2, self.conflict.max_residual)
        assert r1 < 1e-9, f"FLOW SHARE LEAK: wage+interest+retained = {total:.12f}"
        assert r2 < 1e-9, f"DEBT BOOKKEEPING LEAK: ΔD ≠ borrowing−repayment (rel {r2:.2e})"
        assert abs(self.rentier_asset - self.D) < 1e-9 * scale, "rentier asset ≠ firm debt"

    # ---- one financed tick -------------------------------------------------
    def step(self) -> None:
        p = self.p
        i = p.i
        int_share = self.int_share                 # i·D/P at start of period
        slack = i                                  # rate-induced slack (linear v0 map)

        # --- the three channels → effective conflict targets/speeds ---
        # cost: firms defend margin net of interest ⇒ ω_f down, gap up by cost_c·int_share
        # distributional: labor-asymmetric slack ⇒ ω_w down by distrib_a·slack
        omega_f_eff = self.omega_f0 - p.cost_c * int_share
        gap_eff = self.gap0 + p.cost_c * int_share - p.distrib_a * slack   # = ω_w_eff − ω_f_eff
        omega_w_eff = omega_f_eff + gap_eff        # = ω_w0 − distrib_a·slack
        damp = max(0.0, 1.0 - p.demand_b * slack)  # symmetric demand damping (both α's)

        # --- rationing: the wage bill can't be financed past the ceiling / money cap ---
        self.solvency_bound = False
        omega = self.conflict.omega
        if (self.D / self.conflict.P) >= p.D_max:                 # solvency ceiling
            omega_w_eff = min(omega_w_eff, omega); self.solvency_bound = True
        if p.mode == "monetarist":                                # money-growth cap μ:
            # cap financed wage growth so ŵ ≤ μ (D≈wage fund ⇒ money growth ≈ ŵ)
            cap_ratio = omega + p.mu / max(1e-12, p.alpha_w * damp) if p.alpha_w * damp > 0 else omega
            omega_w_eff = min(omega_w_eff, cap_ratio)

        # drive the unmodified conflict layer with the effective parameters
        self.conflict.p.omega_f = omega_f_eff
        self.conflict.p.gap = omega_w_eff - omega_f_eff
        self.conflict.p.alpha_w = self.alpha_w0 * damp
        self.conflict.p.alpha_p = self.alpha_p0 * damp
        self.conflict.step()                       # updates W, P; fires CYB-6's (gross) assert
        self.last_pi = self.conflict.last_pi
        self.last_int_share = int_share

        # --- debt update: revolving wage fund + capitalized uncovered interest ---
        W, P = self.conflict.W, self.conflict.P
        interest = i * self.D
        gross_margin = P - W
        capitalized = max(0.0, interest - gross_margin)     # interest the margin can't cover
        D_next = W + capitalized
        borrowing = W + capitalized                         # new wage fund + capitalized interest
        repayment = self.D                                  # old debt rolled/repaid
        self._assert_conserved(borrowing, repayment, D_next)
        self.D = D_next
        self.rentier_asset = self.D

    def run(self, n: int, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out
