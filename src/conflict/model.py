"""
Cybeersym — conflict module (standalone, v0).

CYB-1/2 isolated the **recursion** channel (technical / input–output propagation:
a chain that amplifies, then — with a behavioural ordering bias — routes to chaos).
This module isolates the **conflict** channel: inflation as a *distributional
struggle*. Workers and firms each target a share of one conserved pie; when their
claims are incompatible (sum to more than the whole), the unresolvable fight over a
conserved total is released as ongoing inflation. This is where **distribution
becomes a cause** of inflation, not merely the outcome the egg model measured.

THE CONSERVED SUBSTRATE — wage share + profit share = 1, always.
A single sector produces one good. Per unit of value added (normalised to the price
`P`), the wage bill is `W` and profit is the residual `P − W`. So:

    wage_share   ω = W / P
    profit_share   = (P − W) / P = 1 − ω           (profit is the residual claimant)

These partition the unit of value added EXACTLY, every step, even mid-spiral —
the SFC spine of this module (cf. CYB-4: a conserved quantity is the load-bearing
constraint). Targets may *sum to more than one*; realised shares never can. The
conservation assert verifies the partition holds to < 1e-9.

THE CLAIMS (backward-looking adjustment; the conflict generator) — each step:

    ŵ = α_w · (ω_w − ω)        # workers push the nominal wage up when the real
                               #   wage (= wage share) is below their target ω_w
    p̂ = α_p · (ω − ω_f)        # firms push the price up when the wage share
                               #   exceeds their implied markup target ω_f
    W ← W · (1 + dt · ŵ)
    P ← P · (1 + dt · p̂)
    π = p̂                       # price inflation is the reported inflation rate

`ω_w` = workers' target wage share; `ω_f = 1/(1+m)` = the wage share implied by
firms' target markup `m`. The control parameter is the **aspiration gap**

    g = ω_w − ω_f

  g ≤ 0  — compatible claims (targets fit inside the pie). A one-off price trigger
           dissipates; inflation is transient.
  g > 0  — incompatible claims (targets overdraw the pie). The trigger *transmits*
           into sustained inflation, rate rising with g; the realised wage share
           settles strictly BETWEEN ω_w and ω_f (neither side gets its claim).

THE NOMINAL-WAGE FLOOR (a deliberate piecewise-smooth kink — and a finding).
Nominal wages are downward-rigid: `ŵ = max(0, α_w·(ω_w − ω))`. With the floor OFF
the rule is symmetric and g < 0 produces steady *deflation* (the mirror image of
g > 0 inflation). With the floor ON, g ≤ 0 dissipates to π = 0 exactly (wages
simply stop falling at ω_f) while g > 0 is unaffected (the floor never binds when
claims are incompatible). So the floor is what makes g = 0 a genuine
DISSIPATION→TRANSMISSION border — a nonsmoothness, in the spirit of CYB-2's
order-non-negativity border. It is ON by default; `run_v0.py` shows both.

DISCIPLINE (inherited from CYB-1/2):
  * No demand noise, no rng — the map is a pure function of state; same initial
    condition → byte-identical trajectory.
  * Conservation (shares sum to 1) is asserted every step, scale-relative.
  * We do NOT pre-judge the dynamics. The model exposes a pure 1-D map of the wage
    share to the reusable `lyapunov` / `bifurcation` / `linearize` instruments;
    they tell us what the dynamics are. (They say: a clean stable equilibrium in
    the *real* wage share, with the instability living in the *nominal* level —
    the opposite character from CYB-2. See README.)

THE INSTRUMENT-FACING MAP. The full physical state `(W, P)` is not a fixed point —
at equilibrium both grow at the common rate π*, only their ratio ω is stationary.
The dynamically meaningful reduced state is the wage share ω alone, and
`omega_map(ω) -> ω'` is the pure 1-D map the instruments iterate (ω* is a genuine
fixed point of it). `omega_step_vector` wraps it in the flat-array interface the
instruments expect.
"""
from dataclasses import dataclass


@dataclass
class ConflictParams:
    omega_f: float = 0.65      # firms' implied target wage share = 1/(1+m)
    gap: float = 0.10          # aspiration gap g = ω_w − ω_f  (THE control knob)
    alpha_w: float = 0.30      # wage-adjustment speed / worker power
    alpha_p: float = 0.30      # price-adjustment speed / firm power
    dt: float = 1.0            # time step (π* is exact for any dt; stability needs
                               #   dt·ω*·(α_w+α_p) < 2 — see linearize in run_v0)
    wage_floor: bool = True    # nominal wages downward-rigid: ŵ = max(0, ·)
    trigger: float = 0.10      # one-off price shock at t=0 (P↑ ⇒ ω↓): the egg/HPAI
                               #   analog. 0 disables it.

    @property
    def omega_w(self) -> float:
        """Workers' target wage share, ω_w = ω_f + g."""
        return self.omega_f + self.gap

    @property
    def markup(self) -> float:
        """Firms' target markup m implied by ω_f = 1/(1+m)."""
        return 1.0 / self.omega_f - 1.0

    @property
    def omega_star(self) -> float:
        """Conflict equilibrium wage share (ω̇ = 0): the convex combination
        ω* = (α_w·ω_w + α_p·ω_f)/(α_w + α_p). Always strictly between the two
        targets — neither side wins. With the wage floor ON and g ≤ 0 the realised
        equilibrium is ω_f instead (the floor binds; see `floored_omega_star`)."""
        aw, ap = self.alpha_w, self.alpha_p
        return (aw * self.omega_w + ap * self.omega_f) / (aw + ap)

    @property
    def floored_omega_star(self) -> float:
        """The equilibrium actually realised under the nominal-wage floor: ω* when
        claims are incompatible (g > 0, floor slack), ω_f when compatible (g ≤ 0,
        floor binds and wages stop falling at the markup target)."""
        if self.wage_floor and self.gap <= 0.0:
            return self.omega_f
        return self.omega_star

    @property
    def pi_star(self) -> float:
        """Closed-form steady inflation (Rowthorn 1977; Lavoie):
        π* = (α_w·α_p/(α_w+α_p))·g for g > 0; 0 under the floor for g ≤ 0
        (deflation −|π*| if the floor is OFF)."""
        aw, ap = self.alpha_w, self.alpha_p
        cf = (aw * ap / (aw + ap)) * self.gap
        if self.wage_floor and self.gap <= 0.0:
            return 0.0
        return cf


class ConflictEconomy:
    """Two classes (workers, firms) fighting over one conserved unit of value
    added. State is the nominal wage `W` and price `P`; the realised wage share is
    `ω = W/P` and profit is the residual `P − W`. Pure and deterministic: `step()`
    is a function of state only.

    Initialised at a neutral pre-conflict rest point (ω = ω_f, where firms' markup
    is exactly met), then hit with a one-off price trigger so every run starts from
    the SAME state and only the aspiration gap `g` differs — the cleanest
    dissipate-vs-transmit contrast.
    """

    def __init__(self, p: ConflictParams):
        self.p = p
        # neutral baseline: wage share at firms' target ω_f (P normalised to 1).
        self.W = p.omega_f
        self.P = 1.0
        # one-off price shock: prices jump, real wage (share) is cut below ω_f.
        self.P *= (1.0 + p.trigger)
        self.last_pi = 0.0
        self.max_residual = 0.0
        self._assert_conserved()

    # ---- shares ------------------------------------------------------------
    @property
    def omega(self) -> float:
        """Realised wage share ω = W/P (= the real wage in this single-good unit)."""
        return self.W / self.P

    @property
    def wage_share(self) -> float:
        return self.W / self.P

    @property
    def profit_share(self) -> float:
        """Profit is the residual claimant on the conserved unit of value added."""
        return (self.P - self.W) / self.P

    def _assert_conserved(self) -> None:
        # wage share + profit share partition one unit of value added, exactly.
        # Scale-relative tolerance (cf. CYB-2): guards the SFC closure on every edit.
        total = self.wage_share + self.profit_share
        scale = max(1.0, abs(self.wage_share), abs(self.profit_share))
        residual = abs(total - 1.0)
        self.max_residual = max(self.max_residual, residual / scale)
        assert residual < 1e-9 * scale, f"SHARE LEAK: shares sum to {total:.12f}"

    # ---- the claim-adjustment rates ----------------------------------------
    def _rates(self, omega: float) -> tuple[float, float]:
        p = self.p
        w_hat = p.alpha_w * (p.omega_w - omega)
        if p.wage_floor:
            w_hat = max(0.0, w_hat)               # nominal wages can't fall (kink)
        p_hat = p.alpha_p * (omega - p.omega_f)
        return w_hat, p_hat

    # ---- one tick ----------------------------------------------------------
    def step(self) -> None:
        p = self.p
        w_hat, p_hat = self._rates(self.omega)
        self.W *= (1.0 + p.dt * w_hat)
        self.P *= (1.0 + p.dt * p_hat)
        self.last_pi = p_hat                       # reported inflation rate π = p̂
        self._assert_conserved()

    def run(self, n: int, observe=None):
        import numpy as np
        obs = observe or (lambda e: e.last_pi)
        out = np.empty(n)
        for k in range(n):
            self.step()
            out[k] = obs(self)
        return out

    # ---- pure 1-D map of the wage share, for the reusable instruments ------
    def omega_map(self, omega: float) -> float:
        """ω ↦ ω' = ω·(1+dt·ŵ)/(1+dt·p̂). ω* is a genuine fixed point of this map
        (W and P grow at the common rate π* there, so their ratio is stationary)."""
        p = self.p
        w_hat, p_hat = self._rates(omega)
        return omega * (1.0 + p.dt * w_hat) / (1.0 + p.dt * p_hat)

    def omega_step_vector(self, vec):
        """Flat-array wrapper (1-element state) for `linearize` / `lyapunov` /
        `bifurcation`, which operate on `step(vec) -> vec`."""
        import numpy as np
        return np.array([self.omega_map(float(vec[0]))])
