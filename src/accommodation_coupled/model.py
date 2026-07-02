"""
Cybeersym — accommodation × coupled substrate (the full egg-faithful stack), v0.  CYB-18.

An INHERITANCE build — no new mechanism. It drops CYB-17's accommodation machinery
(credit ratification of the wage bill at a policy rate `i`, the three rate-channels,
the solvency ceiling) UNCHANGED onto CYB-10's coupled recursion×conflict substrate,
instead of the bare CYB-6 conflict layer. The two axes of composition:

  * RECURSION → CONFLICT  (CYB-10): a conserved 3-tier supply chain (CYB-1/2 `chaos`)
    amplifies a real deficit d(t) ∈ [0,1]; scarcity lowers firms' target wage share,
    which RAISES the aspiration gap:  g(t) = g0 + κ·d(t).  κ is the coupling strength.
  * FINANCE + RATE        (CYB-17): the nominal wage bill must be financed by credit at
    a policy rate `i` (working-capital / wage-fund finance); the rate acts through three
    channels (cost +, symmetric-demand −, distributional −); a solvency ceiling D/P≤D_max
    rations credit at the border; extended conservation wage+interest+retained = 1.

THE COMPOSITION (the single new line of code, everything else reused):
  CYB-17's `AccommodationEconomy` already drives a conflict layer off a FIXED base gap g0
  and perturbs it with the rate's three channels. CYB-10 drives that same base gap with
  recursion: g(t) = g0 + κ·d(t). So we simply RELOAD accommodation's base each step from
  the chain's deficit — set its base ω_f0 down by κ·d and its base g0 up by κ·d (holding
  ω_w0 = ω_f0+g0 fixed, exactly CYB-10's "lower ω_f, hold ω_w") — then let the UNMODIFIED
  accommodation step apply cost/demand/distributional + financing on top of the reloaded
  base. Recursion supplies the gap; accommodation finances and (dis)inflates it.

    base each step:  ω_f0(t) = ω_f0 − κ·d(t),   g0(t) = g0 + κ·d(t)      [CYB-10 reload]
    then CYB-17:     ω_f_eff = ω_f0(t) − c·int_share,  etc.               [unchanged]

TWO REGRESSION ANCHORS (both byte-exact — the load-bearing discipline; run_v0 asserts them):
  * κ = 0                         ⇒ no reload ⇒ reproduces CYB-17 (accommodation on bare CYB-6).
  * i → 0, D_max → ∞, cost off    ⇒ channels vanish ⇒ reproduces CYB-10 (the coupled model).
  Two axes of composition, one anchor each; together they prove the composition added nothing
  but the two interactions that were already validated in isolation.

THREE CONSERVATION LAWS now live at once, each asserted inside its own reused submodule every
step: goods conservation (chain), the three-way income identity wage+interest+retained=1 and
the debt bookkeeping ΔD = borrowing − repayment (accommodation, which itself wraps CYB-6's
share partition). THREE nonsmooth borders live at once: order non-negativity (recursion),
the wage floor (conflict), the solvency ceiling (accommodation).

DISCIPLINE: deterministic (σ=0, pure function of state); one-way coupling; exactly the two
inherited interactions; the chain, conflict and financing submodules are reused UNCHANGED —
we only read the chain's deficit and set accommodation's exogenous base targets. Do NOT
pre-judge the two headline questions (does the distributional flip survive reloading? does
the rate gate ignition?) — run_v0.py measures them.
"""
from pathlib import Path
import importlib.util as _ilu
import numpy as np


# chaos/model.py, conflict/model.py, accommodation/model.py, coupling/model.py and
# src/model.py all share the basename "model"; load the ones we need by file path.
def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_chaos = _load("chaos_model", "chaos/model.py")
_acc = _load("accommodation_model", "accommodation/model.py")
_coup = _load("coupling_model", "coupling/model.py")

ChaosChain, ChaosParams = _chaos.ChaosChain, _chaos.ChaosParams
AccommodationEconomy, AccommodationParams = _acc.AccommodationEconomy, _acc.AccommodationParams
# re-exported for run_v0's regression anchors (build the parents from the same params):
CoupledEconomy = _coup.CoupledEconomy
ConflictParams = _coup.ConflictParams


class AccommodationCoupledEconomy:
    """CYB-10 coupled recursion×conflict substrate + CYB-17 financing/rate loop.

    Composes an UNCHANGED `ChaosChain` (the recursion substrate) and an UNCHANGED
    `AccommodationEconomy` (which itself owns the conflict layer + the financing loop +
    the three rate-channels + the solvency ceiling). Each step reads the chain's deficit
    d(t) and reloads the accommodation module's *base* gap by κ·d(t) — the one-way CYB-10
    coupling — before letting accommodation take its financed tick on top.

    `kappa` is the coupling strength; `deficit_tier` selects which tier's scarcity drives
    the coupling (default the manufacturer, tier −1, matching CYB-10). The deficit is the
    fractional shortfall of that tier's net stock below S_star, clipped to [0,1] — the
    exact CYB-10 map (the anchor-2 regression proves byte-identity).
    """

    def __init__(self, chaos_params: ChaosParams, acc_params: AccommodationParams,
                 kappa: float = 0.0, deficit_tier: int = -1):
        self.chain = ChaosChain(chaos_params)
        self.acc = AccommodationEconomy(acc_params)
        self.kappa = float(kappa)
        self.deficit_tier = deficit_tier
        self.S_star = chaos_params.S_star
        # baselines held fixed: firms' target ω_f0 and the (constant) workers' target ω_w0.
        # recursion moves ω_f0 down by κ·d and g0 up by κ·d each step, holding their sum ω_w0.
        self.omega_f0_base = acc_params.omega_f
        self.g0_base = acc_params.gap
        self.omega_w0_base = self.omega_f0_base + self.g0_base
        self.last_d = 0.0
        self.last_g = self.g0_base

    # ---- the coupling variable: normalized supply-chain deficit (CYB-10 map) ----
    def _deficit(self) -> float:
        net = self.chain.tiers[self.deficit_tier].net_stock
        return float(np.clip((self.S_star - net) / self.S_star, 0.0, 1.0))

    # ---- one coupled, financed tick ---------------------------------------------
    def step(self) -> None:
        self.chain.step()                       # recursion advances (autonomous; asserts goods)
        d = self._deficit()
        g = self.g0_base + self.kappa * d       # g(t) = g0 + κ·d(t)
        # RELOAD accommodation's base: lower ω_f0 by κ·d, hold ω_w0 fixed ⇒ raise base gap to g(t).
        # κ=0 is FULLY decoupled — leave accommodation's base untouched so it runs identically to
        # standalone CYB-17 (anchor 1, byte-exact). The reload mirrors CYB-10's exact arithmetic
        # (ω_f = ω_f0−κ·d; gap = ω_w0−ω_f) so the full-accommodation limit matches CYB-10 (anchor 2).
        if self.kappa != 0.0:
            self.acc.omega_f0 = self.omega_f0_base - self.kappa * d
            self.acc.gap0 = self.omega_w0_base - self.acc.omega_f0
        self.acc.step()                         # financed conflict tick (asserts the 3-way identity)
        self.last_d, self.last_g = d, g

    def run(self, n: int, observe=None):
        obs = observe or (lambda e: e.acc.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out

    # ---- convenience pass-throughs ---------------------------------------------
    @property
    def conflict(self):
        return self.acc.conflict
    @property
    def last_pi(self) -> float:
        return self.acc.last_pi
    @property
    def D(self) -> float:
        return self.acc.D
    @property
    def solvency_bound(self) -> bool:
        return self.acc.solvency_bound

    @property
    def max_residual(self) -> float:
        """Worst conservation residual across ALL THREE laws: goods (chain), and the
        three-way income identity + debt bookkeeping (accommodation, which folds in the
        conflict share partition)."""
        return max(self.chain.max_residual, self.acc.max_residual)
