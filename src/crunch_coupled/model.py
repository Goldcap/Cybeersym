"""
Cybeersym — crunch on the coupled substrate (CYB-19 Phase 1 crunch on the CYB-18 egg stack).  CYB-22.

Pure INHERITANCE build — no new mechanism. It drops CYB-19 Phase 1's credit-crunch cascade
(coverage-ratio regime classifier + deleveraging-rate cascade) UNCHANGED onto CYB-18's coupled
recursion×conflict+financing substrate, instead of bare CYB-17. Two axes of composition:

  * COUPLING (CYB-18): a conserved 3-tier chain amplifies a deficit d(t) that reloads the
    aspiration gap every period, g(t) = g0 + κ·d(t) — so the spiral is continuously re-ignited
    (recursion pins an inflation floor no rate zeroes).
  * CRUNCH  (CYB-19 P1): the coverage ratio tips hedge→speculative→Ponzi; at Ponzi∧border the
    credit ceiling contracts at rate δ, forcing deleveraging — a grinding limit cycle that
    bounds-without-curing (bare Phase 1 only choked to ~12%).

THE COMPOSITION (one inherited interaction, everything else reused):
  CYB-19's `CrunchEconomy` already wraps an `AccommodationEconomy` and drives its solvency
  ceiling `D_max` dynamically (classify regime → contract credit → CYB-17's clamp forces the
  wage-bill cut). CYB-18 drives the SAME accommodation layer's base gap from the chain deficit
  (g = g0 + κ·d). So we hold a `ChaosChain` and a `CrunchEconomy`, and each step RELOAD the
  crunch's inner accommodation base by κ·d (the CYB-18 coupling) before running the UNCHANGED
  crunch tick on top. Recursion reloads the gap; the crunch fires against the border.

    each step:  chain.step → d → reload crunch.acc base by κ·d  →  crunch.step (classify+cascade+acc.step)

TWO REGRESSION ANCHORS (both byte-exact — the load-bearing discipline; run_v0 asserts them):
  * crunch-off (crunch_enabled=False)        ⇒ reproduces CYB-18 (accommodation-coupled) exactly.
  * decouple (κ=0)                            ⇒ reproduces CYB-19 Phase 1 (crunch on bare CYB-17).
  Two axes of composition (coupling × crunch), one anchor each — nothing leaked.

Fisher basin still UNWIRED (no default — that's CYB-19 Phase 2 / CYB-23, bare substrate). This
module is the bounding/fizzle crunch on coupled, nothing more. Determinism (σ=0). The chain,
accommodation and crunch submodules are reused UNCHANGED — we only read the chain's deficit and
set the accommodation base gap.
"""
from pathlib import Path
import importlib.util as _ilu
import numpy as np


def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_chaos = _load("chaos_model", "chaos/model.py")
_crunch = _load("crunch_model", "crunch/model.py")
_accc = _load("accommodation_coupled_model", "accommodation_coupled/model.py")

ChaosChain, ChaosParams = _chaos.ChaosChain, _chaos.ChaosParams
CrunchEconomy, CrunchParams = _crunch.CrunchEconomy, _crunch.CrunchParams
AccommodationParams = _crunch.AccommodationParams
# re-exported for run_v0's regression anchors (build the parents from the same params):
AccommodationCoupledEconomy = _accc.AccommodationCoupledEconomy


class CrunchCoupledEconomy:
    """CYB-18 coupled+financed substrate + CYB-19 Phase-1 crunch.

    Composes an UNCHANGED `ChaosChain` (recursion) and an UNCHANGED `CrunchEconomy` (which itself
    owns the CYB-17 accommodation layer + the crunch cascade). Each step reads the chain deficit
    d(t) and reloads the crunch's inner accommodation base gap by κ·d (the CYB-18 coupling), then
    runs the unchanged crunch tick. `kappa` is the coupling strength; `deficit_tier` selects the
    tier whose scarcity drives the coupling (default −1, the manufacturer — as in CYB-10/18)."""

    def __init__(self, chaos_params: ChaosParams, crunch_params: CrunchParams,
                 kappa: float = 0.0, deficit_tier: int = -1):
        self.chain = ChaosChain(chaos_params)
        self.crunch = CrunchEconomy(crunch_params)
        self.kappa = float(kappa)
        self.deficit_tier = deficit_tier
        self.S_star = chaos_params.S_star
        ap = crunch_params.acc
        self.omega_f0_base = ap.omega_f
        self.g0_base = ap.gap
        self.omega_w0_base = self.omega_f0_base + self.g0_base
        self.last_d = 0.0
        self.last_g = self.g0_base

    # ---- the coupling variable: normalized supply-chain deficit (CYB-10/18 map) ----
    def _deficit(self) -> float:
        net = self.chain.tiers[self.deficit_tier].net_stock
        return float(np.clip((self.S_star - net) / self.S_star, 0.0, 1.0))

    # ---- one coupled, financed, crunching tick ---------------------------------
    def step(self) -> None:
        self.chain.step()                       # recursion advances (autonomous; asserts goods)
        d = self._deficit()
        g = self.g0_base + self.kappa * d       # g(t) = g0 + κ·d(t)
        # RELOAD the crunch's inner accommodation base (CYB-18 coupling). κ=0 is fully decoupled —
        # leave the base untouched so the crunch runs identically to bare CYB-19 P1 (anchor 2).
        acc = self.crunch.acc
        if self.kappa != 0.0:
            acc.omega_f0 = self.omega_f0_base - self.kappa * d
            acc.gap0 = self.omega_w0_base - acc.omega_f0
        self.crunch.step()                      # UNCHANGED crunch tick (classify → cascade → acc.step)
        self.last_d, self.last_g = d, g

    def run(self, n, observe=None):
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
    def last_pi(self) -> float:
        return self.crunch.last_pi
    @property
    def D(self) -> float:
        return self.crunch.acc.D
    @property
    def leverage(self) -> float:
        return self.crunch.acc.D / self.crunch.acc.conflict.P
    @property
    def crunch_active(self) -> bool:
        return self.crunch.crunch_active
    @property
    def solvency_bound(self) -> bool:
        return self.crunch.acc.solvency_bound

    @property
    def max_residual(self) -> float:
        """Worst residual across all conservation laws: goods (chain) + three-way income + debt
        bookkeeping (accommodation, inside the crunch)."""
        return max(self.chain.max_residual, self.crunch.acc.max_residual)
