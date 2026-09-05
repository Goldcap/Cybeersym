"""
Cybeersym — the Goodwin–Keen "instrument self-test rung" (the classifier arc's hydrogen atom).

The taxonomy registry (research/notes/concepts/taxonomy.md) and its principles demand that every
diagnostic be self-tested on a benchmark with a KNOWN class before it is trusted on the coupled
SFC substrate — exactly as `src/chaos/` self-tests its Lyapunov estimator on the logistic map
(r=4 → λ=ln2). This module is that rung for the macro-dynamics classifier, and it is Steve Keen's
own model, so it doubles as the concrete debt-dynamics artifact.

State s = [ω, λ, d]: ω = wage share (W/Y), λ = employment rate, d = D/Y debt ratio. Flow:

    π  = 1 − ω − r·d                 # net profit share (after interest)
    g  = κ(π)/ν − δ                  # capital (=output) growth: investment share / capital-output − depreciation
    ω̇ = ω·(φ(λ) − α)                 # Phillips wage bargaining vs productivity growth α
    λ̇ = λ·(g − α − β)                # employment grows with output net of productivity+labour-force growth
    ḋ = κ(π) − π − d·g               # debt funds investment beyond retained profit

  φ(λ) = −γ + ρ·λ                    # linear Phillips curve
  κ(π) = π                           # GOODWIN: invest exactly profits (keen=False; r=δ=0, d≡0)
  κ(π) = kmin + (kmax−kmin)·σ(ksharp·(π−kmid))   # KEEN: bounded increasing investment (keen=True)

GOODWIN (keen=False, r=δ=0, d₀=0) is the classic 2-D predator–prey (Lotka–Volterra) system —
a CONSERVATIVE CENTRE with an exact invariant H (taxonomy A2: structurally non-hyperbolic;
its closed orbits are B1). KEEN adds debt and a bounded investment appetite: a stable "good"
equilibrium (A1) that, as the interest rate r crosses a threshold r*, loses stability and the
economy breaks down (d→∞, ω→0, λ→0 — a debt-deflationary escape; taxonomy D-transition → E).

The KNOWN answers our instruments must recover (defaults below):
  ω* = 1 − ν(α+β) = 0.865 ,  λ* = (γ+α)/ρ = 0.9 ,  Ω = √(A·C) ≈ 0.3602   (A=1/ν−α−β, C=γ+α)
  H(ω,λ) = ρ·λ − (γ+α)·ln λ + (1/ν)·ω − (1/ν−α−β)·ln ω   is conserved along Goodwin orbits.

Discipline (inherited): deterministic (σ=0, pure function of state); the RK4 map `gk_step` is the
`StepFn: Vec→Vec` the `src/chaos/` instruments consume unchanged; Keen(κ=identity,r=δ=0,d₀=0)
reproduces Goodwin byte-exact (the nesting shell).
"""
from dataclasses import dataclass
import math
import numpy as np


@dataclass
class GKParams:
    # --- structural (shared) ---
    alpha: float = 0.025     # labour-productivity growth
    beta: float = 0.02       # labour-force growth
    nu: float = 3.0          # capital–output ratio
    rho: float = 0.5         # Phillips slope
    gamma: float = 0.425     # Phillips intercept  (φ(λ) = −γ + ρλ)
    delta: float = 0.0       # capital depreciation
    r: float = 0.0           # real interest rate on debt
    keen: bool = False       # False ⇒ κ(π)=π (Goodwin); True ⇒ the bounded sigmoid (Keen)
    # --- Keen investment sigmoid  κ(π) = kmin + (kmax−kmin)·σ(ksharp·(π−kmid)) ---
    kmin: float = 0.0
    kmax: float = 0.30
    ksharp: float = 10.0
    kmid: float = 0.14
    # --- integrator ---
    dt: float = 0.01
    # --- v1 (CYB-35): convex Phillips (Keen's canonical form) + the local Hopf. OFF by default,
    #     so the linear path — and every v0 result — is byte-for-byte unchanged (nesting). ---
    phillips_convex: bool = False   # True ⇒ φ(λ) = φ1/(1−λ)² − φ0 (steepens as λ→1)
    phi0: float = 0.04
    phi1: float = 0.00065


# ---- primitives ---------------------------------------------------------------
def phillips(lam: float, p: GKParams) -> float:
    if p.phillips_convex:                               # v1: Keen's convex Phillips curve
        return p.phi1 / (1.0 - lam) ** 2 - p.phi0
    return -p.gamma + p.rho * lam                       # v0: linear (default; nesting)


def _sigmoid(x: float) -> float:
    # numerically stable logistic (π→−∞ in breakdown must not overflow)
    if x >= 0.0:
        return 1.0 / (1.0 + math.exp(-x))
    ex = math.exp(x)
    return ex / (1.0 + ex)


def kappa(pi: float, p: GKParams) -> float:
    if not p.keen:
        return pi                                   # Goodwin: invest exactly profits
    return p.kmin + (p.kmax - p.kmin) * _sigmoid(p.ksharp * (pi - p.kmid))


def _rhs(omega: float, lam: float, d: float, p: GKParams):
    """The continuous RHS (ω̇, λ̇, ḋ)."""
    pi = 1.0 - omega - p.r * d
    k = kappa(pi, p)
    g = k / p.nu - p.delta
    dom = omega * (phillips(lam, p) - p.alpha)
    dlam = lam * (g - p.alpha - p.beta)
    dd = k - pi - d * g
    return dom, dlam, dd


# ---- the RK4 map (StepFn: Vec→Vec) --------------------------------------------
def gk_step(s, p: GKParams):
    """One RK4 step of the 3-D flow — a PURE function of the state (deterministic)."""
    s = np.asarray(s, dtype=float)
    dt = p.dt

    def f(v):
        dom, dlam, dd = _rhs(v[0], v[1], v[2], p)
        return np.array([dom, dlam, dd])

    k1 = f(s)
    k2 = f(s + 0.5 * dt * k1)
    k3 = f(s + 0.5 * dt * k2)
    k4 = f(s + dt * k3)
    return s + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def goodwin_2d_step(s2, p: GKParams):
    """Independent 2-D Goodwin RK4 (ω, λ only), sharing `_rhs` evaluated at d=0. Used to prove
    the 3-D system's debt-inert limit IS Goodwin, byte-for-byte."""
    s2 = np.asarray(s2, dtype=float)
    dt = p.dt

    def f(v):
        dom, dlam, _ = _rhs(v[0], v[1], 0.0, p)
        return np.array([dom, dlam])

    k1 = f(s2)
    k2 = f(s2 + 0.5 * dt * k1)
    k3 = f(s2 + 0.5 * dt * k2)
    k4 = f(s2 + dt * k3)
    return s2 + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def step_fn(p: GKParams):
    """A closure `Vec→Vec` for the chaos instruments (linearize/lyapunov)."""
    return lambda s: gk_step(s, p)


# ---- a mutable system for the bifurcation sweeper -----------------------------
class GKSystem:
    """Thin mutable wrapper: in-place `step()` + scalar `observe()`, for `bifurcation()`."""
    def __init__(self, p: GKParams, s0=None):
        self.p = p
        w, l, _d = goodwin_equilibrium(p)
        self.s = np.array(s0 if s0 is not None else [w * 0.98, l * 0.98, 0.11], dtype=float)

    def step(self):
        self.s = gk_step(self.s, self.p)

    def observe(self) -> float:
        return float(self.s[2])            # debt ratio d — the breakdown observable


# ---- analytic helpers (the KNOWN answers) -------------------------------------
def _ABCE(p: GKParams):
    A = 1.0 / p.nu - p.alpha - p.beta      # prey (λ) intrinsic growth
    B = 1.0 / p.nu                         # predation coefficient
    C = p.gamma + p.alpha                  # predator (ω) death rate
    E = p.rho                              # predator gain
    return A, B, C, E


def goodwin_equilibrium(p: GKParams):
    """Interior Goodwin equilibrium (ω*, λ*, d*=0)."""
    A, B, C, E = _ABCE(p)
    omega = A / B                          # = 1 − ν(α+β)
    lam = C / E                            # = (γ+α)/ρ
    return omega, lam, 0.0


def goodwin_frequency(p: GKParams) -> float:
    """Centre frequency Ω = √(A·C): the Lotka–Volterra small-oscillation rate."""
    A, B, C, E = _ABCE(p)
    return math.sqrt(A * C)


def conserved_H(s, p: GKParams) -> float:
    """The Lotka–Volterra invariant, constant along Goodwin (d=0) orbits.
    H = E·λ − C·ln λ + B·ω − A·ln ω  (prey λ, predator ω)."""
    A, B, C, E = _ABCE(p)
    omega, lam = float(s[0]), float(s[1])
    return E * lam - C * math.log(lam) + B * omega - A * math.log(omega)


# ---- v1 (CYB-35): the Keen good equilibrium, κ′, and the continuous Jacobian ------------------
def kappa_prime(pi: float, p: GKParams) -> float:
    """dκ/dπ (investment-appetite slope). Goodwin: κ=π ⇒ 1. Keen: the sigmoid derivative."""
    if not p.keen:
        return 1.0
    s = _sigmoid(p.ksharp * (pi - p.kmid))
    return (p.kmax - p.kmin) * p.ksharp * s * (1.0 - s)


def keen_good_equilibrium(p: GKParams):
    """Analytic interior 'good' equilibrium (ω*, λ*, d*) of the Keen system.
       λ* from φ(λ*)=α ;  κ(π*)=ν(α+β+δ) ⇒ π* (invert the sigmoid) ;  d*=(κ(π*)−π*)/(α+β)
       from ḋ=0 (g*=α+β) ;  ω*=1−π*−r·d* from π=1−ω−rd. Works for convex or linear Phillips."""
    if p.phillips_convex:
        lam = 1.0 - math.sqrt(p.phi1 / (p.phi0 + p.alpha))     # φ1/(1−λ)² − φ0 = α
    else:
        lam = (p.gamma + p.alpha) / p.rho
    target = p.nu * (p.alpha + p.beta + p.delta)               # κ(π*) must equal this
    if p.keen:
        frac = (target - p.kmin) / (p.kmax - p.kmin)
        pi = p.kmid + math.log(frac / (1.0 - frac)) / p.ksharp  # σ⁻¹
    else:
        pi = target
    g = p.alpha + p.beta                                        # g* = κ/ν − δ = α+β at eq
    d = (target - pi) / g                                       # ḋ = κ − π − d·g = 0
    omega = 1.0 - pi - p.r * d
    return omega, lam, d


def continuous_jacobian(s, p: GKParams, eps: float = 1e-6):
    """3×3 Jacobian of the CONTINUOUS RHS at state s (central finite difference) — the analytic
    side of the Hopf self-test, independent of the RK4 map the instrument sees."""
    s = np.asarray(s, dtype=float)
    J = np.empty((3, 3))
    for j in range(3):
        sp = s.copy(); sp[j] += eps
        sm = s.copy(); sm[j] -= eps
        fp = np.array(_rhs(sp[0], sp[1], sp[2], p))
        fm = np.array(_rhs(sm[0], sm[1], sm[2], p))
        J[:, j] = (fp - fm) / (2.0 * eps)
    return J


def hopf_locus_residual(p: GKParams) -> float:
    """The closed-form Hopf condition at the good equilibrium: Routh–Hurwitz a₁a₂−a₃ reduces
    EXACTLY to J₁₂·J₂₃·J₃₁, and J₁₂,J₂₃ ≠ 0, so the Hopf is where J₃₁ = 0, i.e.
    κ′(π*) = ν/(ν−d*). Returns κ′(π*) − ν/(ν−d*): zero at the Hopf, sign = which side.
    NB the threshold LOCATION is Phillips-independent (φ' cancels from J₃₁) — investment-sensitivity
    × debt; φ'>0 still sets the oscillatory character (the crossing pair is ±i√a₂, a₂=ω*λ*φ'κ'/ν)."""
    omega, lam, d = keen_good_equilibrium(p)
    pi = 1.0 - omega - p.r * d
    return kappa_prime(pi, p) - p.nu / (p.nu - d)
