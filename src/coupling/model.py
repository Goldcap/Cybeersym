"""
Cybeersym — coupling module (recursion × conflict), v0.  CYB-10.

The first integration of two isolated channels:
  * RECURSION (CYB-1/2, `../chaos`): a conserved 3-tier supply chain with the
    anchoring-and-adjustment ordering rule. As the supply-line weight β falls it
    goes stable → oscillatory → deterministic chaos. It destabilizes the REAL side
    (bounded quantity chaos; goods conserved).
  * CONFLICT (CYB-6, `../conflict`): wage–price conflicting claims over a conserved
    pie. Above the aspiration-gap threshold g = 0 a shock transmits into a sustained
    wage–price spiral; below it (with the nominal-wage floor) it dissipates. It
    destabilizes the NOMINAL side (price-level runaway; real share a stable node).

THE COUPLING (one-way, recursion → conflict; exactly one interaction).
Supply-chain scarcity lifts firms' target markup — i.e. LOWERS their target wage
share ω_f — which RAISES the aspiration gap g. Concretely, with the chain's
normalized deficit d(t) ∈ [0,1] and coupling strength κ ≥ 0:

    ω_f(t) = ω_f0 − κ·d(t)                     (firms want more margin when scarce)
    g(t)   = ω_w − ω_f(t) = g0 + κ·d(t)        (ω_w held fixed → the gap widens)

So recursion feeds STRAIGHT INTO conflict's control parameter g. κ=0 is fully
decoupled (the two modules run side by side, untouched). This is the H1 test made
exact: start the conflict layer SUBTHRESHOLD (g0 < 0, dissipates alone) and watch
whether the chain's deficit drives g(t) across 0 into a sustained spiral.

Implementation note: the conflict model derives ω_w = ω_f + gap as a property, so to
realize "lower ω_f, hold ω_w fixed" we set BOTH `omega_f` and `gap` each step
(their sum stays ω_w0). Both submodules are used UNCHANGED — we only read the
chain's state and set the conflict layer's exogenous targets. Both conservation
asserts (goods; wage+profit share) therefore keep firing inside each submodule.

DISCIPLINE: deterministic (σ=0, no rng); one-way; exactly one interaction; do NOT
pre-judge the coupled dynamics — `run_v0.py` measures them. At κ=0 the composition
must reproduce CYB-2 and CYB-6 byte-for-byte (the load-bearing decoupling regression).
"""
from pathlib import Path
import importlib.util as _ilu
import numpy as np

# chaos/model.py, conflict/model.py and src/model.py all share the basename
# "model", so load the two we need explicitly by file path (no sys.path games).
def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_chaos = _load("chaos_model", "chaos/model.py")
_cm = _load("conflict_model", "conflict/model.py")
ChaosChain, ChaosParams = _chaos.ChaosChain, _chaos.ChaosParams
ConflictEconomy, ConflictParams = _cm.ConflictEconomy, _cm.ConflictParams


class CoupledEconomy:
    """Recursion chain × conflict layer, coupled one-way via d → ω_f → g.

    `kappa` is the coupling strength; `deficit_tier` selects which tier's scarcity
    drives the coupling (default the manufacturer — the upstream input-scarcity the
    CYB-2 chaos observable already tracks). The deficit is the fractional shortfall
    of that tier's net stock below its desired level S_star, clipped to [0,1]:
        d(t) = clip( (S_star − net_stock) / S_star , 0, 1 ).
    """

    def __init__(self, chaos_params: ChaosParams, conflict_params: ConflictParams,
                 kappa: float = 0.0, deficit_tier: int = -1):
        self.chain = ChaosChain(chaos_params)
        self.conflict = ConflictEconomy(conflict_params)
        self.kappa = float(kappa)
        self.deficit_tier = deficit_tier
        self.S_star = chaos_params.S_star
        # baselines held fixed: firms' target ω_f0 and workers' target ω_w0.
        self.omega_f0 = conflict_params.omega_f
        self.g0 = conflict_params.gap
        self.omega_w0 = self.omega_f0 + self.g0     # ω_w, held CONSTANT under coupling
        self.last_d = 0.0
        self.last_g = self.g0

    # ---- the coupling variable: normalized supply-chain deficit ------------
    def _deficit(self) -> float:
        net = self.chain.tiers[self.deficit_tier].net_stock
        return float(np.clip((self.S_star - net) / self.S_star, 0.0, 1.0))

    # ---- one coupled tick --------------------------------------------------
    def step(self) -> None:
        self.chain.step()                       # recursion advances (autonomous; asserts goods)
        d = self._deficit()
        g = self.g0 + self.kappa * d            # g(t) = g0 + κ·d(t)   (κ=0 ⇒ g0 exactly)
        # lower ω_f by κ·d, hold ω_w fixed ⇒ raise the gap to g(t)
        self.conflict.p.omega_f = self.omega_f0 - self.kappa * d
        self.conflict.p.gap = self.omega_w0 - self.conflict.p.omega_f
        self.conflict.step()                    # conflict advances (asserts shares sum to 1)
        self.last_d, self.last_g = d, g

    def run(self, n: int, observe=None):
        obs = observe or (lambda c: c.conflict.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step()
            out[k] = obs(self)
        return out

    # ---- flat reduced state for the reused instruments ---------------------
    # coupled reduced state = chain flat state  ⊕  conflict wage share ω
    def get_state(self) -> np.ndarray:
        return np.concatenate([self.chain.get_state(), [self.conflict.omega]])

    def step_vector(self, vec: np.ndarray) -> np.ndarray:
        """Pure map (chain_state ⊕ ω) → next, for `lyapunov`/`linearize`. Uses the
        chain's conservation-free twin step (a math probe), matching CYB-2's
        `step_vector` convention, and drives ω through the same d → g coupling."""
        nchain = vec.size - 1
        self.chain.set_state(vec[:nchain])
        self.chain._step_no_conservation()
        d = self._deficit()
        self.conflict.p.omega_f = self.omega_f0 - self.kappa * d
        self.conflict.p.gap = self.omega_w0 - self.conflict.p.omega_f
        omega2 = self.conflict.omega_map(float(vec[nchain]))
        return np.concatenate([self.chain.get_state(), [omega2]])

    @property
    def max_residual(self) -> float:
        """Worst conservation residual across BOTH substrates (goods; shares)."""
        return max(self.chain.max_residual, self.conflict.max_residual)
