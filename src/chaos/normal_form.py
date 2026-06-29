"""
Cybeersym — border-collision normal-form classifier (reusable instrument).

Given the two one-sided Jacobians of a piecewise-smooth map at a border point (or
their trace/determinant pairs), name the border-collision bifurcation and predict the
born attractor from the piecewise-linear NORMAL FORM theory — rather than only
observing it. Built for CYB-4 (formally classifying CYB-2's border-collision), but
model-agnostic like `lyapunov.py` / `bifurcation.py` / `linearize.py`: it takes
numbers, not a supply chain.

THE NORMAL FORM (Nusse–Yorke 1992; Banerjee & Grebogi 1999). Near a border-collision,
a 2-D piecewise-smooth map reduces to the piecewise-LINEAR normal form (switching
boundary x=0, bifurcation parameter μ):

    x ≤ 0:  (x, y) ↦ ( τ_L·x + y + μ ,  −δ_L·x )
    x ≥ 0:  (x, y) ↦ ( τ_R·x + y + μ ,  −δ_R·x )

where (τ_L, δ_L) = (trace, determinant) of the LEFT one-sided Jacobian and (τ_R, δ_R)
the RIGHT. Each side's eigenvalues solve λ² − τλ + δ = 0: a complex FOCUS of modulus
√δ when τ² < 4δ, else a real NODE/SADDLE. The fixed point sits on the border at μ=0;
the bifurcation is μ crossing 0.

CLASSIFICATION (Feigin / Banerjee–Grebogi, dissipative δ>0 regime, with extensions):
  * Feigin sign-counters σ⁺, σ⁻ = number of real eigenvalues > +1, < −1 (per side).
    Feigin's rules (di Bernardo–Feigin–Hogan–Homer 1999):
      σ_L⁺+σ_R⁺ even → PERSISTENCE (one orbit → one orbit);
      σ_L⁺+σ_R⁺ odd  → NONSMOOTH FOLD (two orbits collide & vanish);
      σ_L⁻+σ_R⁻ odd  → PERIOD-2 born (border-collision period-doubling).
  * CLOSED INVARIANT CURVE (Neimark–Sacker analogue; Patra & Banerjee 2009): needs the
    NON-dissipative regime — contracting one side, expanding focus the other:
    |δ_L|<1, |δ_R|>1 (or symmetric), with the stable side −(1+δ)<τ<(1+δ) and the
    expanding side a focus, −2√δ<τ<2√δ (modulus √δ>1 = spiral repellor).
  * ROBUST CHAOS (Banerjee–Yorke–Grebogi 1998): saddle–saddle plus a homoclinic-corner
    inequality φ>0 — a chaotic attractor with NO periodic windows over an interval.

SELF-TEST (`python3 normal_form.py`) — validate before trusting any verdict, same
discipline as the other instruments. Three documented cases:
  #1 (τ_L,δ_L,τ_R,δ_R)=(1.7,0.5,−1.7,0.5)  → ROBUST CHAOS  [Banerjee–Grebogi 1999, Fig.7]
  #2 (−1.43,0.5,−1.52,0.5)                  → PERIOD-2 (BCB period-doubling)
  #3 (0.3,0.5,0.5,1.5)                       → CLOSED INVARIANT CURVE  [Patra–Banerjee regime]

CAVEAT — DIMENSION (load-bearing for CYB-4). This normal form is 2-D. For an N-D map
the rigorous reductions are only three codim-2 cases; "project onto the dominant
eigenplane" is NOT a sanctioned theorem, and *especially* not when a complex pair
dominates (Simpson et al., Phys. Lett. A 2025, "Three forms of dimension reduction for
border-collision bifurcations" — the only sanctioned N-D robust-chaos reduction is to a
1-D skew tent map when a REAL eigenvalue dominates). `reduce_dominant_plane` is provided
for a HEURISTIC probe only and flags itself `sanctioned=False`. Treat its verdict as
provisional.
"""
import math
from typing import Optional
import numpy as np


# --------------------------------------------------------- per-side eigen-structure
def side_eigen(tau: float, delta: float) -> dict:
    """Eigenvalue structure of one linear piece with trace τ, determinant δ.
    Returns kind ('focus'|'node'|'saddle'), the eigenvalues, modulus, and Feigin
    counters σ⁺ (#real λ>+1), σ⁻ (#real λ<−1)."""
    disc = tau * tau - 4.0 * delta
    sp = sm = 0
    if disc < 0:                                   # complex focus, modulus √δ (δ>0)
        mod = math.sqrt(delta)
        return {"kind": "focus", "eigs": None, "modulus": mod,
                "sigma_plus": 0, "sigma_minus": 0, "expanding": mod > 1.0}
    s = math.sqrt(disc)
    l1, l2 = 0.5 * (tau + s), 0.5 * (tau - s)
    for l in (l1, l2):
        if l > 1.0:
            sp += 1
        elif l < -1.0:
            sm += 1
    kind = "saddle" if (abs(l1) > 1.0) != (abs(l2) > 1.0) else "node"
    return {"kind": kind, "eigs": (l1, l2), "modulus": max(abs(l1), abs(l2)),
            "sigma_plus": sp, "sigma_minus": sm, "expanding": max(abs(l1), abs(l2)) > 1.0}


# ---------------------------------------------------------------- robust-chaos test
def _robust_chaos(tau_L, delta_L, tau_R, delta_R) -> bool:
    """Banerjee–Yorke–Grebogi (1998) condition, one orientation: L expands via a real
    eigenvalue >1, R via a real eigenvalue <−1, plus the homoclinic inequality φ>0."""
    if not (0.0 < delta_L < tau_L - 1.0 and 0.0 < delta_R < -tau_R - 1.0):
        return False
    discL = tau_L * tau_L - 4.0 * delta_L
    if discL < 0:
        return False
    lamL_u = 0.5 * (tau_L + math.sqrt(discL))                 # unstable eigenvalue, L
    phi = delta_R - (tau_R + delta_L + delta_R - (1.0 + tau_R) * lamL_u) * lamL_u
    return phi > 0.0


def _closed_curve(tau_L, delta_L, tau_R, delta_R) -> bool:
    """Patra–Banerjee (2009): contracting side + expanding focus → invariant curve.
    Tests both orientations (which side is the spiral repellor)."""
    def ok(t_s, d_s, t_e, d_e):
        stable_side = (abs(d_s) < 1.0) and (-(1.0 + d_s) < t_s < (1.0 + d_s))
        focus_exp = (d_e > 1.0) and (t_e * t_e < 4.0 * d_e) and (-2 * math.sqrt(d_e) < t_e < 2 * math.sqrt(d_e))
        return stable_side and focus_exp
    return ok(tau_L, delta_L, tau_R, delta_R) or ok(tau_R, delta_R, tau_L, delta_L)


# ----------------------------------------------------------------------- classify
def classify_2d(tau_L: float, delta_L: float, tau_R: float, delta_R: float) -> dict:
    """Name the border-collision bifurcation of the 2-D normal form with the given
    one-sided trace/determinant pairs. Returns a structured verdict."""
    L, R = side_eigen(tau_L, delta_L), side_eigen(tau_R, delta_R)
    sp = L["sigma_plus"] + R["sigma_plus"]
    sm = L["sigma_minus"] + R["sigma_minus"]

    feigin = "persistence" if sp % 2 == 0 else "nonsmooth_fold"
    period_doubling = (sm % 2 == 1)
    closed_curve = _closed_curve(tau_L, delta_L, tau_R, delta_R)
    robust_chaos = (_robust_chaos(tau_L, delta_L, tau_R, delta_R)
                    or _robust_chaos(tau_R, delta_R, tau_L, delta_L))

    invertible = (abs(delta_L) > 1e-12) and (abs(delta_R) > 1e-12)
    dissipative = (abs(delta_L) < 1.0) and (abs(delta_R) < 1.0)

    # headline (most specific wins)
    if robust_chaos:
        headline = "robust chaos (chaotic attractor, no periodic windows)"
    elif closed_curve:
        headline = "closed invariant curve (Neimark–Sacker analogue)"
    elif period_doubling:
        headline = "border-collision period-doubling (period-2 born)"
    elif feigin == "nonsmooth_fold":
        headline = "nonsmooth fold (saddle-node analogue: pair appears/vanishes)"
    else:
        headline = "persistence (fixed point → fixed point, type may change)"

    warnings = []
    if not dissipative:
        warnings.append("non-dissipative (|δ|≥1 on a side) — outside the standard "
                        "Banerjee–Grebogi dissipative classification; closed-curve / "
                        "exotic regimes possible")
    if not invertible:
        warnings.append("non-invertible (δ≈0 on a side) — a piece collapses dimension")

    return {"headline": headline, "feigin": feigin, "period_doubling": period_doubling,
            "closed_curve": closed_curve, "robust_chaos": robust_chaos,
            "sigma_plus_sum": sp, "sigma_minus_sum": sm, "left": L, "right": R,
            "invertible": invertible, "dissipative": dissipative, "warnings": warnings,
            "tau_delta": (tau_L, delta_L, tau_R, delta_R)}


# --------------------------------------------------- N-D → 2-D reduction (HEURISTIC)
def reduce_dominant_plane(J: np.ndarray) -> dict:
    """HEURISTIC reduction of an N-D one-sided Jacobian to a (τ, δ) pair from its
    leading eigenvalue(s). NOT a sanctioned border-collision reduction (Simpson et al.
    2025): returned `sanctioned=False`. For a leading COMPLEX pair ρe^{±iφ}: τ=2ρcosφ,
    δ=ρ². For a leading real pair: τ=λ1+λ2, δ=λ1λ2."""
    ev = np.linalg.eigvals(J)
    ev = ev[np.argsort(-np.abs(ev))]
    lead = ev[0]
    if abs(lead.imag) > 1e-9:
        rho, phi = abs(lead), abs(np.angle(lead))
        tau, delta = 2.0 * rho * math.cos(phi), rho * rho
        kind = "complex pair"
    else:
        l1, l2 = ev[0].real, ev[1].real
        tau, delta = l1 + l2, l1 * l2
        kind = "real pair"
    return {"tau": float(tau), "delta": float(delta), "leading_kind": kind,
            "leading_modulus": float(abs(lead)), "sanctioned": False,
            "caveat": "dominant-plane reduction is a heuristic, not a theorem "
                      "(Simpson et al., Phys. Lett. A 2025); provisional verdict only"}


def classify_jacobians(J_L: np.ndarray, J_R: np.ndarray) -> dict:
    """Classify from two one-sided Jacobians. If 2×2, exact. If larger, reduce each via
    the (unsanctioned) dominant-plane heuristic and flag the verdict provisional."""
    J_L, J_R = np.asarray(J_L, float), np.asarray(J_R, float)
    if J_L.shape == (2, 2) and J_R.shape == (2, 2):
        out = classify_2d(np.trace(J_L), np.linalg.det(J_L),
                          np.trace(J_R), np.linalg.det(J_R))
        out["reduction"] = "exact (2-D)"
        return out
    rL, rR = reduce_dominant_plane(J_L), reduce_dominant_plane(J_R)
    out = classify_2d(rL["tau"], rL["delta"], rR["tau"], rR["delta"])
    out["reduction"] = "HEURISTIC dominant-plane (NOT sanctioned — provisional)"
    out["reduce_left"], out["reduce_right"] = rL, rR
    out["warnings"].append(rL["caveat"])
    return out


# ------------------------------------------------------------------------ self-test
def _self_test() -> None:
    print("normal_form self-test — documented 2-D border-collision cases\n")
    cases = [
        ("#1 robust chaos      [Banerjee–Grebogi 1999, Fig.7]", (1.7, 0.5, -1.7, 0.5),
         lambda r: r["robust_chaos"]),
        ("#2 period-doubling   [BCB period-2 born]           ", (-1.43, 0.5, -1.52, 0.5),
         lambda r: r["period_doubling"] and not r["robust_chaos"]),
        ("#3 closed inv. curve [Patra–Banerjee regime]       ", (0.3, 0.5, 0.5, 1.5),
         lambda r: r["closed_curve"]),
    ]
    ok = True
    for label, (tL, dL, tR, dR), check in cases:
        r = classify_2d(tL, dL, tR, dR)
        passed = check(r)
        ok &= passed
        print(f"  {label}: {r['headline']}")
        print(f"      (τL,δL,τR,δR)=({tL},{dL},{tR},{dR})  σ⁺={r['sigma_plus_sum']} "
              f"σ⁻={r['sigma_minus_sum']}  {'PASS' if passed else 'FAIL'}")

    # eigenvalue typing sanity: a stable focus and a real saddle
    f = side_eigen(0.4, 0.5)      # τ²=0.16 < 4δ=2 → focus, modulus √0.5≈0.707
    s = side_eigen(2.0, 0.5)      # real, one eigenvalue >1 → saddle
    ok &= f["kind"] == "focus" and abs(f["modulus"] - math.sqrt(0.5)) < 1e-12
    ok &= s["kind"] == "saddle" and s["sigma_plus"] == 1
    print(f"\n  eigen-typing: focus modulus={f['modulus']:.4f} (√0.5), "
          f"saddle σ⁺={s['sigma_plus']}  {'PASS' if f['kind']=='focus' and s['kind']=='saddle' else 'FAIL'}")

    assert ok, "normal_form self-test FAILED"
    print("\n  PASS: classifier reproduces documented border-collision verdicts.")
    print("  Instrument trusted (2-D). N-D use is heuristic only — see reduce_dominant_plane.")


if __name__ == "__main__":
    _self_test()
