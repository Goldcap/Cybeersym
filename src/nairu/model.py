"""
Cybeersym — NAIRU module (CYB-20 sibling): the natural rate as a DISTRIBUTIONAL equilibrium.  v0.

**Illustration under an explicit, contestable assumption — NOT a proof, NOT an empirical claim.**
This module makes ONE assumption vivid and traces its consequences: that unemployment stabilises
prices by *disempowering labour* (Kalecki 1943; Rowthorn 1977; the "cost of job loss" / conflict-
NAIRU tradition), not by clearing frictions. The CYB-6 conflict model is already a Rowthorn model
— steady inflation is set by the aspiration gap g = ω_w − ω_f — so this is its native reading.

THE ONE ASSUMPTION (the whole load-bearing content; everything else is CYB-6, reused unchanged):
the workers' target share falls with unemployment — a discipline function

    ω_w(u) = ω_w0 − b·u          # ω_w0 = full-employment (u=0) target; b = discipline slope

Then the aspiration gap is g(u) = ω_w(u) − ω_f, and the NAIRU is simply where it closes:

    u*  such that  g(u*) = 0   ⇒   u* = (ω_w0 − ω_f) / b

Below u* the gap is open (g>0) ⇒ CYB-6 transmits it as inflation π* = c·g(u), c = α_wα_p/(α_w+α_p);
at/above u* the floor binds (g≤0) ⇒ π* = 0. That is a downward-sloping Phillips curve with a stable
rate at u* — the ORTHODOX NAIRU, reproduced as a special case.

THE DIVERGENCE (the point): orthodoxy treats u* as a technical/frictional CONSTANT, invariant to
distribution. Here u* = (ω_w0 − ω_f)/b is a FUNCTION of the distributional parameters — it rises
with the firm markup target (ω_f↓) and with worker militancy (ω_w0↑). Same object, different NATURE
⇒ a policy lever orthodoxy's constant-u* forbids: compress the gap (incomes policy / lower the
markup) and inflation stabilises at the SAME unemployment — no recession. **This is a consequence of
the assumption, offered as illustration; whether the assumption holds of any real economy is exactly
what is NOT settled here (the frictional NAIRU rests on a different, equally-unproven assumption).**

DISCIPLINE (inherited): deterministic; CYB-6 conservation (shares partition 1) holds unchanged — this
layer only sets the gap, it does not touch the wage/price partition. `b=0` (or any u with g(u) fixed
to CYB-6's gap) recovers CYB-6 exactly. numpy only in the model.
"""
from dataclasses import dataclass, field
from pathlib import Path
import importlib.util as _ilu


def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, str(Path(__file__).resolve().parent.parent / rel))
    mod = _ilu.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

_conflict = _load("conflict_model", "conflict/model.py")
ConflictParams, ConflictEconomy = _conflict.ConflictParams, _conflict.ConflictEconomy


@dataclass
class NairuParams:
    """The discipline function + the CYB-6 conflict primitives that survive it. `ω_w` is now
    ENDOGENOUS to unemployment via (ω_w0, b); the conflict `gap` is derived, not primitive."""
    omega_f: float = 0.65      # firms' markup target share ω_f = 1/(1+m)  (firm power)
    omega_w0: float = 0.85     # workers' FULL-EMPLOYMENT (u=0) target share (militancy); > ω_f
    b: float = 4.0             # discipline slope: how fast unemployment lowers the worker target
    alpha_w: float = 0.30
    alpha_p: float = 0.30
    dt: float = 1.0
    wage_floor: bool = True    # the CYB-6 nominal-wage floor: makes g=0 a genuine border

    @property
    def c(self) -> float:
        """Conflict inflation gain: π* = c·g for g>0 (Rowthorn 1977)."""
        return self.alpha_w * self.alpha_p / (self.alpha_w + self.alpha_p)

    def omega_w(self, u: float) -> float:
        """The discipline function — workers' target share falls with unemployment."""
        return self.omega_w0 - self.b * u

    def gap(self, u: float) -> float:
        """Aspiration gap at unemployment u: g(u) = ω_w(u) − ω_f."""
        return self.omega_w(u) - self.omega_f

    @property
    def nairu(self) -> float:
        """u* where the aspiration gap closes, g(u*)=0 ⇒ u* = (ω_w0 − ω_f)/b. A function of the
        DISTRIBUTIONAL parameters — not a technical constant."""
        return (self.omega_w0 - self.omega_f) / self.b

    def steady_pi(self, u: float) -> float:
        """Closed-form steady inflation at unemployment u (CYB-6): c·g(u) for g>0, else 0 (floor)."""
        g = self.gap(u)
        if self.wage_floor and g <= 0.0:
            return 0.0
        return self.c * g

    def conflict_at(self, u: float) -> ConflictParams:
        """The exact CYB-6 ConflictParams realised at unemployment u (gap = g(u)). Running this is
        the rigour check: the sim's steady π must equal `steady_pi(u)`."""
        return ConflictParams(omega_f=self.omega_f, gap=self.gap(u), alpha_w=self.alpha_w,
                              alpha_p=self.alpha_p, dt=self.dt, wage_floor=self.wage_floor)


class NairuEconomy:
    """A CYB-6 `ConflictEconomy` whose aspiration gap is set by the discipline function at a fixed
    unemployment `u`. Pure pass-through to CYB-6 — this layer chooses the gap, nothing else — so
    conservation and determinism are inherited exactly. Holds `u` constant over a run (the NAIRU is a
    steady-state object; the dynamic u(t) path is a later cell)."""

    def __init__(self, p: NairuParams, u: float):
        self.p = p
        self.u = float(u)
        self.econ = ConflictEconomy(p.conflict_at(u))

    def step(self) -> None:
        self.econ.step()

    @property
    def last_pi(self) -> float:
        return self.econ.last_pi
    @property
    def omega(self) -> float:
        return self.econ.omega
    @property
    def max_residual(self) -> float:
        return self.econ.max_residual

    def run(self, n: int, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out

    def steady_pi(self, n: int = 20000) -> float:
        """Run to steady state and return the realised inflation rate (the sim-side of the closed form)."""
        for _ in range(n):
            self.step()
        return self.econ.last_pi
