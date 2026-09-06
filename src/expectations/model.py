"""
Cybeersym — expectations module (CYB-20): the second SUSTAINING channel.  v0.

CYB-6 (conflict) makes inflation a distributional struggle over one conserved pie, with a
*backward-looking* wage rule (workers chase the realised wage share ω). CYB-17 found that
distributional channel **self-exhausts**; recursion (CYB-10/18) is one sustaining channel; this
module builds the other — and the one **classical macro is built on: expectations.** Workers do
not only chase the realised real wage; they demand compensation for the inflation they *expect*.

THE ONE NEW MECHANISM (everything else is CYB-6, reused; recovered byte-exact when `phi_e=0`):
an adaptive **inflation expectation** `π^e` that passes into the wage claim.

    ω = W/P
    ŵ = α_w·(ω_w − ω) + φ_e·π^e          # + EXPECTED-inflation compensation (the new term)
    p̂ = α_p·(ω − ω_f)                    # firms respond to the realised wage share (UNCHANGED)
    W ← W·(1 + dt·ŵ);  P ← P·(1 + dt·p̂);  π = p̂
    π^e ← π^e + λ·(π − π^e)               # adaptive expectations (Cagan/Friedman)

`φ_e` = expectations **pass-through** into wage demands (the swept pivot; `φ_e=0` ⇒ CYB-6 exactly,
byte-exact — the new term vanishes and π^e never touches W,P). `λ` = expectations updating speed.
The nominal-wage floor is applied to the *whole* claim `max(0, α_w(ω_w−ω)+φ_e·π^e)` (indexation
can lift a floored claim off the kink — a deliberate, tested interaction).

THE FINDING (see run_v0 — analytic + instrument, both objects):
  * A closed-form steady state (ω stationary, π^e=π): **π = α_w·g / (1 + α_w/α_p − φ_e)**.
  * ⇒ a genuine **DE-ANCHORING** bifurcation: steady inflation DIVERGES as **φ_e → 1 + α_w/α_p**.
    This is NOT the textbook accelerationist `φ_e=1` (full indexation) — the de-anchoring point is
    set by the **conflict balance** `α_w/α_p` (relative worker/firm adjustment speed). The wage
    floor lifts, so the divergence is a real steady-state property, not a numerical overshoot.
  * There are TWO thresholds and run_v0 separates them honestly: (i) the STEADY-STATE de-anchoring
    at `φ_e = 1 + α_w/α_p` (where the equilibrium itself ceases to exist), and (ii) a lower
    DYNAMIC-STABILITY boundary where the equilibrium still exists but the PATH to it goes unstable
    — a genuine local bifurcation located by the eigenvalues of the 2-D map's Jacobian
    (`chaos/linearize`), NOT by finite-time overflow (which drifts with the horizon near marginal
    stability, and would be a detector artifact if trusted — the retired-two-basin lesson).

DISCIPLINE (inherited, non-negotiable):
  * Deterministic (σ=0, pure function of state) — same state ⇒ byte-identical trajectory.
  * Conservation: wage share + profit share partition one unit of value added, exactly, every step
    (the expectations term changes the wage RATE, never the partition). Asserted < 1e-9.
  * Nested byte-exact: `phi_e=0` ⇒ CYB-6 `ConflictEconomy` exactly (run_v0 asserts Δ = 0.0).
  * Don't pre-judge the dynamics — the reduced 2-D map `(ω, π^e)` is handed to the reusable
    `linearize`/`eigs` instruments; they locate the bifurcation.

Reflexivity (CYB-20 v1, NOT built here): let de-anchored π^e feed back and shift the *fundamentals*
(the markup target ω_f or the aspiration gap g) — the two-way Soros loop rational-expectations
models assume away. Scoped in the README; probed-then-built as its own reviewer-gated increment.
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
class ExpectationsParams:
    """CYB-6 conflict params + the expectations knobs. `phi_e=0` ⇒ byte-exact CYB-6."""
    conflict: ConflictParams = field(default_factory=ConflictParams)
    phi_e: float = 0.0     # expectations pass-through into the wage claim (the swept pivot)
    lam: float = 0.30      # adaptive-expectations updating speed λ ∈ (0,1]

    # convenience mirrors of the conflict sub-params (read-only)
    @property
    def alpha_w(self): return self.conflict.alpha_w
    @property
    def alpha_p(self): return self.conflict.alpha_p
    @property
    def omega_f(self): return self.conflict.omega_f
    @property
    def omega_w(self): return self.conflict.omega_w
    @property
    def gap(self): return self.conflict.gap
    @property
    def dt(self): return self.conflict.dt

    @property
    def deanchor_threshold(self) -> float:
        """Closed-form STEADY-STATE de-anchoring pass-through: φ_e* = 1 + α_w/α_p (denominator of
        the steady-π expression → 0). NOT the textbook accelerationist φ_e=1."""
        return 1.0 + self.alpha_w / self.alpha_p

    def steady_pi(self, phi_e: float = None) -> float:
        """Closed-form steady inflation π = α_w·g / (1 + α_w/α_p − φ_e) for g>0 below threshold;
        +inf at/above the de-anchoring threshold. (Floor is slack when g>0, as in CYB-6.)"""
        phi_e = self.phi_e if phi_e is None else phi_e
        denom = 1.0 + self.alpha_w / self.alpha_p - phi_e
        if self.gap <= 0.0:
            return 0.0 if self.conflict.wage_floor else self.alpha_w * self.gap / denom
        return float("inf") if denom <= 0.0 else self.alpha_w * self.gap / denom

    def steady_state(self, phi_e: float = None):
        """(ω*, π^e*) of the reduced map below threshold: π* = steady_pi, ω* = ω_f + π*/α_p."""
        phi_e = self.phi_e if phi_e is None else phi_e
        pistar = self.steady_pi(phi_e)
        if not (pistar == pistar) or pistar == float("inf"):   # nan/inf ⇒ no finite equilibrium
            return None
        return (self.omega_f + pistar / self.alpha_p, pistar)


class ExpectationsEconomy:
    """CYB-6 conflict + an adaptive inflation expectation π^e that passes into the wage claim.
    State is the nominal wage `W`, price `P`, and expectation `π^e`; the reduced dynamical state is
    `(ω=W/P, π^e)`. `phi_e=0` ⇒ byte-exact CYB-6 (the new term vanishes; π^e never touches W,P)."""

    def __init__(self, p: ExpectationsParams, pe0: float = 0.0):
        self.p = p
        c = p.conflict
        # SAME neutral baseline + one-off trigger as CYB-6, so phi_e=0 nests byte-exact.
        self.W = c.omega_f
        self.P = 1.0 * (1.0 + c.trigger)
        self.pe = float(pe0)
        self.last_pi = 0.0
        self.max_residual = 0.0
        self._assert_conserved()

    # ---- shares (identical partition to CYB-6) ---------------------------------
    @property
    def omega(self) -> float:
        return self.W / self.P
    @property
    def wage_share(self) -> float:
        return self.W / self.P
    @property
    def profit_share(self) -> float:
        return (self.P - self.W) / self.P
    @property
    def expected_pi(self) -> float:
        return self.pe

    def _assert_conserved(self) -> None:
        total = self.wage_share + self.profit_share
        scale = max(1.0, abs(self.wage_share), abs(self.profit_share))
        residual = abs(total - 1.0)
        self.max_residual = max(self.max_residual, residual / scale)
        assert residual < 1e-9 * scale, f"SHARE LEAK: shares sum to {total:.12f}"

    # ---- the augmented claim rates (CYB-6 + expectations pass-through) ----------
    def _rates(self, omega: float, pe: float):
        p = self.p
        w_hat = p.alpha_w * (p.omega_w - omega) + p.phi_e * pe   # + expected-inflation compensation
        if p.conflict.wage_floor:
            w_hat = max(0.0, w_hat)                              # floor on the WHOLE claim
        p_hat = p.alpha_p * (omega - p.omega_f)
        return w_hat, p_hat

    # ---- one tick --------------------------------------------------------------
    def step(self) -> None:
        p = self.p
        w_hat, p_hat = self._rates(self.omega, self.pe)
        self.W *= (1.0 + p.dt * w_hat)
        self.P *= (1.0 + p.dt * p_hat)
        self.last_pi = p_hat
        self.pe += p.lam * (p_hat - self.pe)                    # adaptive expectations
        self._assert_conserved()

    def run(self, n: int, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step(); out[k] = obs(self)
        return out

    # ---- the pure reduced 2-D map (ω, π^e), for the reusable instruments -------
    def map2d(self, omega: float, pe: float):
        """(ω, π^e) ↦ (ω', π^e'). ω' = ω·(1+dt·ŵ)/(1+dt·p̂); π^e' = π^e + λ(p̂ − π^e).
        The steady state (ω*, π*) is a genuine fixed point of this map."""
        p = self.p
        w_hat, p_hat = self._rates(omega, pe)
        omega_p = omega * (1.0 + p.dt * w_hat) / (1.0 + p.dt * p_hat)
        pe_p = pe + p.lam * (p_hat - pe)
        return omega_p, pe_p

    def step_vector(self, vec):
        """Flat-array wrapper for `linearize`/`eigs`/`fixed_point_newton` (StepFn on [ω, π^e])."""
        import numpy as np
        o, e = self.map2d(float(vec[0]), float(vec[1]))
        return np.array([o, e])
