"""
Cybeersym — Minsky credit-crunch cascade, Phase 1 (dynamic deleveraging off the solvency
border).  CYB-19.

CYB-17 built the accommodation channel (finance the wage bill at a rate `i`) and a *static*
solvency ceiling `D/P ≤ D_max` that rations credit at the border. CYB-18 showed the coupled
system RIDES that ceiling (73% of steps) and no rate zeroes inflation — debt climbs against
the border in the ordinary course. This module fires the border: it turns the static clamp
into a **dynamic credit-crunch cascade**, and lets the outcome — does the crunch *bound* the
spiral or merely *fizzle* — fall out of the parameters rather than being designed in.

ONE NEW MECHANISM (everything else is CYB-17, reused unchanged and recovered byte-exact when
the crunch is off): a **financing-regime classifier** + a **deleveraging-rate cascade**.

  TRIGGER — a regime shift, not a level breach (Minsky's hedge → speculative → Ponzi, at the
  aggregate, from existing CYB-17 flows). Per period, with margin = P−W, interest = i·D:
      hedge        : margin ≥ interest + am·D     (covers interest AND amortizes principal)
      speculative  : interest ≤ margin < …        (covers interest, must roll principal)
      Ponzi        : margin < interest            (can't cover interest ⇒ D capitalizes to
                                                    service itself — exactly CYB-17's
                                                    `capitalized = max(0, interest − margin)`)
  The crunch fires when the aggregate tips into **Ponzi *and* leverage has reached the
  solvency border** (`D/P ≥ L_trig`): accommodation stops accommodating.

  CASCADE — a deleveraging RATE, not an instantaneous snap. On firing, the credit ceiling
  contracts at rate `delta` (`D_ceil ← min(D_ceil, D/P)·(1−delta)`); CYB-17's own solvency
  clamp then freezes the wage bill against the descending ceiling, so W is held while P rises
  ⇒ ω and D/P fall — forced deleveraging (the BOUNDING path: credit contracts → wage bill
  can't be financed → spiral choked). When coverage is restored to hedge, credit re-expands
  at rate `relax` (hysteresis). Whether the contraction durably chokes the spiral (**bound**)
  or the system re-levers and the spiral resumes (**fizzle**) is set by `(i, delta)` — the
  Phase-1 outcome map, NOT a design choice.

PHASE-1 SCOPE / HONESTY GUARD. The **Fisher debt-deflation** path (falling P·Y raises the real
debt burden ⇒ more deleveraging ⇒ the "more they pay, the more they owe" doom loop) is
structurally where this points, but it is **deliberately UNWIRED here**: Phase 1 contracts
*new* credit and forces repayment — it does NOT default, impair, or write off (the rentier
pool stays passive). So the debt-deflation *basin is unreachable by construction*, and this
module may characterize the bounding/fizzle outcomes but may NOT conclude "the crunch is
stabilizing." Default + impairable rentier pool → the Fisher basin is Phase 2 (its own ticket).

DISCIPLINE: deterministic (σ=0, pure function of state); one new mechanism; CYB-17 reused
unchanged and recovered byte-for-byte when `crunch_enabled=False` (the load-bearing anchor).
Conservation (three-way income identity + debt bookkeeping) holds THROUGH the deleveraging
transient — contracting credit must not leak accounting.
"""
from dataclasses import dataclass, field
from pathlib import Path
import importlib.util as _ilu


def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_acc = _load("accommodation_model", "accommodation/model.py")
AccommodationEconomy, AccommodationParams = _acc.AccommodationEconomy, _acc.AccommodationParams
ConflictEconomy, ConflictParams = _acc.ConflictEconomy, _acc.ConflictParams

_ELASTIC = 1e18            # credit ceiling value meaning "fully elastic" (never binds)


@dataclass
class CrunchParams:
    """CYB-17 substrate params + the crunch knobs. `crunch_enabled=False` ⇒ pure CYB-17."""
    acc: AccommodationParams = field(default_factory=AccommodationParams)
    crunch_enabled: bool = False
    L_trig: float = 0.66      # leverage (D/P) at which Ponzi arms the crunch — the solvency border
    delta: float = 0.10       # deleveraging RATE (credit-ceiling contraction per active step)
    am: float = 0.02          # amortization rate: hedge/speculative boundary (margin ≥ int + am·D)
    heal: float = 0.05        # credit re-expansion (healing) rate when not distressed
    L_rel: float = 0.60       # leverage below which the crunch releases (hysteresis floor)


class CrunchEconomy:
    """CYB-17 accommodation substrate + a Minsky financing-regime classifier and a
    deleveraging-rate cascade fired at Ponzi∧border. Composes an UNCHANGED
    `AccommodationEconomy` and, when the crunch is enabled, drives its solvency ceiling
    `D_max` dynamically (contract on firing, re-expand on recovery). When disabled it is a
    pure pass-through — byte-for-byte CYB-17."""

    def __init__(self, p: CrunchParams):
        self.p = p
        self.acc = AccommodationEconomy(p.acc)
        self.D_ceil = _ELASTIC                 # elastic until the crunch contracts it
        self.regime = "hedge"
        self.crunch_active = False
        self.last_pi = 0.0
        self.last_lev = self.acc.D / self.acc.conflict.P
        self.n_active = 0

    # ---- Minsky financing-regime classifier (from existing CYB-17 flows) ----
    def _classify(self):
        P, W, D = self.acc.conflict.P, self.acc.conflict.W, self.acc.D
        margin = P - W                          # gross profit before interest
        interest = self.p.acc.i * D
        amort = self.p.am * D
        lev = D / P
        if margin < interest:
            regime = "ponzi"                    # ≡ CYB-17 capitalizes interest (D services itself)
        elif margin < interest + amort:
            regime = "speculative"              # covers interest, rolls principal
        else:
            regime = "hedge"                    # covers interest + amortization
        return regime, lev

    # ---- one tick ----------------------------------------------------------
    def step(self) -> None:
        if not self.p.crunch_enabled:
            self.acc.step()                     # pure CYB-17 (byte-exact anchor)
            self.last_pi = self.acc.last_pi
            self.regime, self.last_lev = self._classify()
            return

        regime, lev = self._classify()
        # Hysteresis state machine. FIRE when the aggregate tips Ponzi at the border; stay in
        # the crunch until leverage is genuinely worked down (lev < L_rel). The outcome is a
        # RACE: while distressed the credit ceiling contracts at `delta` (deleveraging); when
        # not, it re-expands (heals) at `heal`. delta ≫ heal ⇒ contraction wins (BOUND);
        # delta ≪ heal ⇒ the spiral re-levers faster than credit tightens (FIZZLE).
        if not self.crunch_active and regime == "ponzi" and lev >= self.p.L_trig:
            self.crunch_active = True           # fire: Ponzi at the border
        elif self.crunch_active and regime == "hedge":
            self.crunch_active = False          # coverage restored ⇒ release (credit heals)
        if self.crunch_active:
            self.D_ceil = min(self.D_ceil, lev) * (1.0 - self.p.delta)   # contract (cumulative)
            self.n_active += 1
        elif self.D_ceil < _ELASTIC:
            self.D_ceil *= (1.0 + self.p.heal)                          # heal back toward elastic
            if self.D_ceil >= self.p.L_trig:
                self.D_ceil = _ELASTIC

        # drive CYB-17's solvency clamp with the (possibly contracted) ceiling, then step it.
        self.acc.p.D_max = self.D_ceil
        self.acc.step()
        self.last_pi = self.acc.last_pi
        self.regime, self.last_lev = regime, lev

    def run(self, n, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out

    # ---- pass-throughs -----------------------------------------------------
    @property
    def conflict(self):
        return self.acc.conflict
    @property
    def D(self) -> float:
        return self.acc.D
    @property
    def leverage(self) -> float:
        return self.acc.D / self.acc.conflict.P
    @property
    def solvency_bound(self) -> bool:
        return self.acc.solvency_bound
    @property
    def max_residual(self) -> float:
        return self.acc.max_residual
