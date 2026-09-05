"""
Cybeersym — CYB-19 Phase 2b: the genuine Fisher debt-deflation loop (Engine 2).  CYB-2Xb.

Phase 2 (CYB-23) wired Engine 1 (credit-QUANTITY contagion: the impaired rentier prices a risk
premium → dearer credit → more Ponzi → hyper-INFLATIONARY collapse) and GATED Engine 2 (the
price-level Fisher loop) OFF. It gated Engine 2 off honestly, with evidence: CYB-17's demand
channel is a *symmetric multiplicative damper* (`damp = max(0, 1 − demand_b·slack)` scales BOTH
α_w and α_p toward zero), so it drives π toward 0 FROM ABOVE and can never flip sign — verified
at min tail π = −0.000%/step even at demand_b=10. Deflation was therefore UNREACHABLE by
construction, and CYB-23 said so: "Engine 2 needs a STRENGTHENED price mechanism (Phase 2b),
not a simple switch-on." This module is that strengthened mechanism.

THE ONE NEW MECHANISM (everything else is CYB-23, reused unchanged; recovered byte-exact when
`fisher_phi=0`): a genuine, closed **Fisher debt-deflation loop**. Debt-distress — measured as
the excess REAL debt burden (leverage D/P above a reference) — triggers distress selling that
cuts the price level; the cut RAISES the real burden next period (P↓ ⇒ D/P↑), which drives more
distress selling. That is the "the more they pay, the more they owe" doom loop (Fisher 1933),
and it is genuinely self-reinforcing — NOT the crude fixed-decrement switch ContagionEconomy
carries (that switch stays OFF here; Phase 2b supersedes it with a real feedback loop):

    pressure = max(0, leverage − b_ref)          # excess real debt burden (distress)
    P ← P · (1 − φ · pressure)                    # distress selling cuts the price level
    # next period: leverage = D/P rises (D nominal, unchanged) ⇒ pressure rises ⇒ bigger cut

CORRECTION (the proper-proof pass — this SUPERSEDES the original v0 "two-basin / φ* threshold"
headline, which was a detector artifact). We stress-tested the deflation basin the honest way:
LIFT the single-step blow-up/blow-down detectors and ask whether P actually RUNS AWAY. It does
not. Composed on the conflict layer's markup-defense, the Fisher cut is a self-limiting feedback:
a falling P raises ω=W/P, so next tick the conflict layer pushes P back up. The two forces settle
into a BOUNDED LIMIT CYCLE — the running-min log P is byte-identical across early and late windows
for every φ up to 20 (non-secular ⇒ no divergence). The old φ*≈1.63 was merely where that cycle's
down-swing first breaches −25%/step; unfrozen, φ=1.8 sits at P≈0.9 forever. So:

  * GENUINE Fisher debt-deflation (D/P → ∞, P → 0) requires the markup-defense to be SUPPRESSED.
    Over the (α_p, φ) plane, genuine divergence appears ONLY at α_p → 0 (and then for φ ≳ 2);
    for ANY working markup layer (α_p ≥ 0.005) it is a bounded cycle at every φ tested.
  * THE STABILIZER IS STRUCTURAL. The isolated Fisher map is ALWAYS unstable (linearize
    u ← u·(1+φ·b_ref), multiplier > 1 for any φ>0); the conflict layer's markup-defense is the
    thing that stops it. So "inflationary, not Fisher" is not merely "conditional on a weak price
    channel" — it reflects the markup-defense acting as a structural PRICE FLOOR. That is a
    stronger, honest engagement with the Fisher condition than a reproduction would be.

DISCIPLINE (inherited, non-negotiable):
  * Deterministic (σ=0, pure function of state).
  * Nested byte-exact regression: fisher_phi=0 ⇒ CYB-23 exactly ⇒ (recovery=1) Phase 1 ⇒
    (crunch off) CYB-17. `CYB-17 ⊂ P1 ⊂ P2 ⊂ P2b`.
  * DON'T pre-decide the dynamics — SWEEP (α_p, φ) and classify by GENUINE divergence with the
    detectors LIFTED, not by a single-step swing. This is the correction that mattered.
  * Conservation THROUGH the deflationary transient — proven now on a GENUINE divergence (α_p=0):
    the nominal capital-account identity (rentier asset ≡ firm liability) is P-INDEPENDENT, so the
    Fisher price cut cannot break it. That is the SFC point of debt-deflation: a REAL-burden
    runaway (D/P → ∞) while the NOMINAL accounting stays exactly consistent (residual reported).
  * The collapse (where it is genuine, α_p→0) must be the LOOP, not the mechanical cut: a
    frozen-leverage regression stays bounded where the live loop diverges (cf. CYB-10's κ=0).
"""
from dataclasses import dataclass, field
from pathlib import Path
import importlib.util as _ilu


def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_con = _load("contagion_model", "contagion/model.py")
ContagionEconomy, ContagionParams = _con.ContagionEconomy, _con.ContagionParams
CrunchParams, AccommodationParams = _con.CrunchParams, _con.AccommodationParams
CrunchEconomy = _con.CrunchEconomy


@dataclass
class FisherParams:
    """CYB-23 contagion params + the Phase-2b Fisher knobs. `fisher_phi=0` ⇒ byte-exact CYB-23."""
    contagion: ContagionParams = field(default_factory=ContagionParams)
    fisher_phi: float = 0.0      # Engine-2 price-channel strength (the SWEPT pivot); 0 ⇒ Engine 2 off
    b_ref: float = 0.64          # real-debt-burden (leverage D/P) at which distress selling engages
    freeze_leverage: bool = False  # honesty regression: read pressure off a HELD-constant leverage
                                   #   (isolates the mechanical cut from the self-reinforcing loop)


class FisherEconomy:
    """CYB-23 contagion substrate + a genuine Fisher debt-deflation loop (Engine 2). Composes an
    UNCHANGED `ContagionEconomy` (its crude fisher_on switch left OFF) and applies the real
    distress-selling price cut after each contagion tick. fisher_phi=0 ⇒ byte-exact CYB-23."""

    # Runaway is DETECTED, not simulated to overflow, and frozen so the terminus is observable.
    # HONEST criterion (CORRECTED — see CORRECTION below): a genuine Fisher runaway is a REAL-burden
    # runaway, D/P → ∞. Detect it by leverage blow-up ALONE. The earlier `π < −25%/step` single-step
    # disjunct was an ARTIFACT: composed on the conflict layer's markup-defense (a falling P raises
    # ω=W/P ⇒ firms push P back up), the Fisher cut vs. that floor is a BOUNDED LIMIT CYCLE whose
    # down-swings breach −25%/step WITHOUT diverging (unfreeze and P returns). Leverage blow-up only
    # fires on true divergence — which, at the shipped α_p, never happens (it needs α_p → 0).
    _LEV_BLOWUP = 1e6            # D/P this large ⇒ P→0: the genuine Fisher (real-burden) terminus

    def __init__(self, p: FisherParams):
        self.p = p
        self.con = ContagionEconomy(p.contagion)   # fisher_on defaults False ⇒ crude switch inert
        self._lev_frozen = self.con.leverage       # for the freeze_leverage honesty regression
        self.deflation_collapsed = False
        self.deflation_step = None
        self.last_pi = 0.0
        self.last_fisher_cut = 0.0                  # this step's Fisher price decrement (≤0)
        self.max_residual = 0.0
        self._step = 0

    # ---- pass-throughs ---------------------------------------------------------
    @property
    def conflict(self):
        return self.con.conflict
    @property
    def leverage(self) -> float:
        return self.con.leverage
    @property
    def collapsed(self) -> bool:
        """True if EITHER engine has run away (inflationary Engine 1 or deflationary Engine 2)."""
        return self.con.collapsed or self.deflation_collapsed
    @property
    def inflation_collapsed(self) -> bool:
        return self.con.collapsed
    @property
    def max_bs_residual(self) -> float:
        return self.con.max_residual

    # ---- one financed, crunching, defaulting, debt-deflating tick --------------
    def step(self) -> None:
        if self.collapsed:
            return                                 # frozen at the blow-up/down
        self._step += 1
        P0 = self.con.conflict.P

        self.con.step()                            # CYB-23 tick (Engine 1); runs ALL inner asserts

        # --- Engine 2: the genuine Fisher debt-deflation loop ---
        lev = self._lev_frozen if self.p.freeze_leverage else self.con.leverage
        pressure = max(0.0, lev - self.p.b_ref)    # excess real debt burden = distress
        cut = self.p.fisher_phi * pressure
        if cut > 0.0:
            cut = min(cut, 0.99)                   # a single step can't wipe the whole price level
            self.con.conflict.P *= (1.0 - cut)     # distress selling cuts the price (P↓ ⇒ D/P↑ next)
            self.last_fisher_cut = -cut
        else:
            self.last_fisher_cut = 0.0

        # reported inflation = the TRUE combined price change this step (conflict π net of the cut)
        self.last_pi = self.con.conflict.P / P0 - 1.0

        # genuine-deflationary-runaway detection (the Engine-2 terminus): D/P → ∞, NOT a single-step
        # swing. A bounded limit cycle can swing past −25%/step every period without ever diverging;
        # only leverage blow-up marks a true real-burden runaway (P→0). At the shipped α_p this never
        # fires — the markup-defense floors P — so `deflation_collapsed` stays False (the honest result).
        if (not self.con.collapsed) and (self.con.leverage > self._LEV_BLOWUP):
            self.deflation_collapsed = True
            self.deflation_step = self._step

        # conservation: the nominal capital-account identity is P-independent, so the Fisher cut
        # cannot break it — this residual PROVES it holds through the deflationary transient.
        self.max_residual = max(self.max_residual, self.con.max_residual)

    def run(self, n, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out
