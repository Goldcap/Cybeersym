"""
Cybeersym — figures for the CYB-25 outreach note (docs/outreach/bifurcation-note.md).

Two figures, generated deterministically from the SAME validated instruments used
elsewhere (model.py + linearize.py), so the note's images are reproducible from source:

  Figure 1 — hysteresis bifurcation diagram: down-sweep (from the calm equilibrium
             branch) and up-sweep (from the turbulent branch) overlaid. Shows the
             finite-amplitude onset (a jump, not growth-from-zero) and the coexistence
             interval where the two sweeps disagree.

  Figure 2 — transverse spectral radius of the interior equilibrium vs β: the largest
             |λ| after removing the three conserved λ=+1 directions. Stays strictly
             below 1 through the onset region — the equilibrium never loses transverse
             stability. (Distinct from the one-sided border-Jacobian plane at 0.945.)

Run from inside src/chaos/:  python3 outreach_figures.py
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

from model import ChaosChain, ChaosParams
from linearize import jacobian, fixed_point_iterate, fixed_point_newton, eigs

A_S, L, THETA, MU, S_STAR = 0.7, 3, 0.25, 100.0, 100.0
STRIDE = 4 + L
OUT = Path(__file__).resolve().parent.parent.parent / "docs" / "outreach" / "figures"


def _params(beta, perturb=0.0):
    return ChaosParams(beta=beta, a_S=A_S, L=L, theta=THETA, perturb=perturb)


def _physical(x, tol=1e-6):
    for i in range(3):
        b = i * STRIDE
        if x[b] < -tol or x[b + 2] < -tol or np.any(x[b + 4:b + 7] < -tol):
            return False
    return True


# ----------------------------------------------------------------- Figure 1
def figure1_bifurcation(path):
    """Down- and up-sweep bifurcation diagram (continuation), manufacturer net stock."""
    betas_down = np.round(np.arange(0.40, 0.079, -0.005), 3)
    betas_up = betas_down[::-1]
    transient, record = 4000, 600

    mfr = 2 * STRIDE  # manufacturer block offset; net stock = inventory - backlog

    def sweep(betas, seed_state):
        vec = seed_state.copy()
        pts_b, pts_v = [], []
        for beta in betas:
            c = ChaosChain(_params(beta))              # pure map F_β via step_vector
            for _ in range(transient):
                vec = c.step_vector(vec)
            vals = []
            for _ in range(record):
                vec = c.step_vector(vec)
                vals.append(vec[mfr] - vec[mfr + 1])
            sub = np.array(vals)[::4]                   # subsample recurrent values
            pts_b.extend([beta] * sub.size)
            pts_v.extend(sub.tolist())
        return np.array(pts_b), np.array(pts_v)

    # down-sweep: start on the CALM branch (tiny perturbation off the equilibrium)
    calm = ChaosChain(_params(0.40, perturb=1.0)).get_state()
    bd, vd = sweep(betas_down, calm)
    # up-sweep: start on the TURBULENT branch (developed attractor at low β)
    cturb = ChaosChain(_params(0.08))
    tvec = ChaosChain(_params(0.08, perturb=1.0)).get_state()
    for _ in range(20000):
        tvec = cturb.step_vector(tvec)
    bu, vu = sweep(betas_up, tvec)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.scatter(bd, vd, s=0.6, c="#1f5fbf", alpha=0.55, label="down-sweep (from calm branch)", rasterized=True)
    ax.scatter(bu, vu, s=0.6, c="#c0392b", alpha=0.55, label="up-sweep (from turbulent branch)", rasterized=True)
    ax.axvspan(0.26, 0.30, color="#f0d000", alpha=0.12)
    ax.set_xlabel(r"supply-line weight  $\beta$")
    ax.set_ylabel(r"manufacturer net stock  $S_3$  (recurrent values)")
    ax.set_title("Figure 1 — Finite-amplitude onset and coexistence (hysteresis sweeps)")
    ax.set_xlim(0.40, 0.08)  # decreasing β left→right matches 'underweighting increases →'
    y0, y1 = ax.get_ylim()
    ax.legend(loc="upper left", fontsize=8, markerscale=8, framealpha=0.9)
    ax.text(0.28, y0 + 0.10 * (y1 - y0), "onset /\ncoexistence", fontsize=7.5, ha="center",
            va="center", color="#7a6300",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#d8c060", alpha=0.85))
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  wrote {path}  (down {bd.size} pts, up {bu.size} pts)")


# ----------------------------------------------------------------- Figure 2
def figure2_transverse_spectrum(path):
    """Max transverse |λ| at the interior equilibrium vs β (excluding the 3 conserved λ=1)."""
    betas = np.round(np.arange(0.40, 0.259, -0.005), 3)
    radii = []
    prev = None
    for beta in betas:
        c = ChaosChain(_params(beta))
        step, x0 = c.step_vector, c.get_state()
        xi = fixed_point_iterate(step, x0, n=120000)
        if np.max(np.abs(step(xi) - xi)) < 1e-7 and _physical(xi):
            xs = xi
        else:
            xs, _ = fixed_point_newton(step, prev if prev is not None else x0, iters=80)
        if _physical(xs) and np.max(np.abs(step(xs) - xs)) < 1e-5:
            prev = xs.copy()
        ev = np.abs(eigs(jacobian(step, xs)))
        hyp = ev[np.abs(ev - 1.0) >= 1e-3]      # drop the three conserved λ≈1
        radii.append(hyp.max() if hyp.size else np.nan)
    radii = np.array(radii)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.axhline(1.0, color="#888", lw=1.0, ls="--")
    ax.text(0.395, 1.006, r"unit circle  $|\lambda|=1$", fontsize=8, color="#666")
    ax.axvline(0.29, color="#c0392b", lw=1.0, ls=":")
    ax.text(0.288, 0.862, "chaos onset\n$\\beta\\approx0.29$", fontsize=7.5, ha="right",
            va="bottom", color="#8a2a20")
    ax.annotate("", xy=(0.26, 0.858), xytext=(0.29, 0.858),
                arrowprops=dict(arrowstyle="->", color="#c0392b", lw=1.0))
    ax.text(0.275, 0.852, "numerically chaotic  ($\\Lambda>0$)", fontsize=7,
            ha="center", va="top", color="#8a2a20")
    ax.plot(betas, radii, "-o", ms=3.2, lw=1.4, color="#1f5fbf")
    ax.set_xlabel(r"supply-line weight  $\beta$")
    ax.set_ylabel(r"max transverse  $|\lambda|$  at the equilibrium")
    ax.set_title("Figure 2 — The equilibrium keeps transverse stability through onset")
    ax.set_xlim(0.40, 0.26)
    ax.set_ylim(min(0.84, radii.min() - 0.02), 1.03)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"  wrote {path}  (β {betas[0]}→{betas[-1]}, |λ| {radii.min():.4f}→{radii.max():.4f})")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print("Generating CYB-25 outreach figures (deterministic)...")
    figure1_bifurcation(OUT / "note_fig1_bifurcation_hysteresis.png")
    figure2_transverse_spectrum(OUT / "note_fig2_transverse_spectrum.png")
    print("done.")


if __name__ == "__main__":
    main()
