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


@dataclass
class BargainParams:
    """v1 — the discipline function MICRO-FOUNDED from Nash / McDonald–Solow wage bargaining, with the
    OUTSIDE OPTION made an explicit, dial-able parameterization. Answers the mainstream 'ad hoc'
    charge: ω_w(u) is now a *derived* bargaining outcome, not a posited shape.

    Nash sharing of the bargaining surplus with worker power β, ceiling C, over an outside option that
    falls with unemployment via a parameterized COST OF JOB LOSS:

        cjl(u)      = k · u^γ                 # γ = convexity dial: 1 linear (≡ nairu v0); >1 convex; <1 concave
        ω_threat(u) = ω_e − cjl(u)            # worker fallback share (reemployed share ω_e minus the cost)
        ω_w(u)      = β·C + (1−β)·ω_threat(u)  # bargained worker target

    γ=1 reduces EXACTLY to the nairu-v0 linear discipline function ω_w(u)=ω_w0−b·u, with
    ω_w0 = β·C+(1−β)·ω_e and b = (1−β)·k. So v1 nests v0 at γ=1, and the 'ad hoc' linear form is
    revealed as the bargaining solution. Turning γ dials the Phillips-curve CURVATURE (the sign of that
    curvature is itself a live empirical/fingerprint question). Still an ILLUSTRATION: micro-founding
    RELOCATES the assumption to bargaining primitives (protocol, outside-option shape) the mainstream
    accepts — it does not remove it, and does not make it true."""
    beta: float = 0.60         # worker bargaining power (Nash surplus share) — a POWER lever
    ceiling: float = 0.90      # ω_ceiling: max worker share attainable in the bargain
    omega_e: float = 0.70      # reemployed share (outside option at u=0) — a FRICTIONAL lever
    k: float = 8.0             # cost-of-job-loss scale — a FRICTIONAL/institutional lever
    gamma: float = 1.0         # cost-of-job-loss CONVEXITY dial (the new v1 knob)
    omega_f: float = 0.65      # firms' markup target — a POWER lever
    alpha_w: float = 0.30
    alpha_p: float = 0.30
    dt: float = 1.0
    wage_floor: bool = True

    @property
    def c(self) -> float:
        return self.alpha_w * self.alpha_p / (self.alpha_w + self.alpha_p)

    def cjl(self, u: float) -> float:
        return self.k * (u ** self.gamma)

    def omega_threat(self, u: float) -> float:
        return self.omega_e - self.cjl(u)

    def omega_w(self, u: float) -> float:
        """The bargained worker target share — DERIVED, not assumed."""
        return self.beta * self.ceiling + (1.0 - self.beta) * self.omega_threat(u)

    def gap(self, u: float) -> float:
        return self.omega_w(u) - self.omega_f

    @property
    def nairu(self) -> float:
        """u* where the bargained gap closes: ω_w(u*)=ω_f ⇒ (1−β)k·u*^γ = βC+(1−β)ω_e − ω_f, so
        u* = ( [βC+(1−β)ω_e − ω_f] / [(1−β)k] )^(1/γ). Depends on BOTH power (β, ω_f) and frictions
        (ω_e, k, and the shape γ). Returns nan if the gap never opens (no NAIRU)."""
        num = self.beta * self.ceiling + (1.0 - self.beta) * self.omega_e - self.omega_f
        den = (1.0 - self.beta) * self.k
        if num <= 0.0 or den <= 0.0:
            return float("nan")
        return (num / den) ** (1.0 / self.gamma)

    def steady_pi(self, u: float) -> float:
        g = self.gap(u)
        if self.wage_floor and g <= 0.0:
            return 0.0
        return self.c * g

    def conflict_at(self, u: float) -> ConflictParams:
        return ConflictParams(omega_f=self.omega_f, gap=self.gap(u), alpha_w=self.alpha_w,
                              alpha_p=self.alpha_p, dt=self.dt, wage_floor=self.wage_floor)

    def as_nairu_linear(self):
        """The v0 NairuParams whose linear discipline function coincides with this bargain at γ=1
        (ω_w0=βC+(1−β)ω_e, b=(1−β)k). Used for the nesting check."""
        return NairuParams(omega_f=self.omega_f,
                           omega_w0=self.beta * self.ceiling + (1.0 - self.beta) * self.omega_e,
                           b=(1.0 - self.beta) * self.k, alpha_w=self.alpha_w, alpha_p=self.alpha_p,
                           dt=self.dt, wage_floor=self.wage_floor)

    @classmethod
    def from_matching(cls, a: float, **overrides):
        """v2 — micro-found the cost-of-job-loss convexity γ from a search/matching job-finding rate,
        so γ is not a free dial. DMP logic: unemployed find work at rate f(u); expected duration
        D(u)=1/f(u); the cost of job loss rises with D. With a Cobb–Douglas matching function
        m=A·u^a·v^(1−a) and vacancies v held fixed, f(u)=A(v/u)^(1−a) ∝ u^(−(1−a)), so expected
        duration D(u)=1/f ∝ u^(1−a); taking the cost of job loss ∝ D gives cjl(u) ∝ u^(1−a) ⇒
        **γ = 1 − a** (the v-fixed, cost∝duration reduction is specific — see the README caveat). Since the matching elasticity a∈(0,1),
        γ∈(0,1) is ALWAYS concave — the matching microfoundation predicts a Phillips curve that
        STEEPENS near full employment (a checkable fingerprint), not the flat-when-tight (γ>1) shape.
        (`gamma` in `overrides` is ignored — it is set to 1−a here by construction.)"""
        overrides.pop("gamma", None)
        return cls(gamma=gamma_from_matching(a), **overrides)


def gamma_from_matching(a: float) -> float:
    """The cost-of-job-loss convexity implied by a Cobb–Douglas matching elasticity `a`: γ = 1 − a.
    a∈(0,1) ⇒ γ∈(0,1), always concave ⇒ the Phillips curve steepens near full employment."""
    return 1.0 - a


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
