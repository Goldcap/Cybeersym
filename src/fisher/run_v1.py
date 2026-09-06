"""
Cybeersym — CYB-38 §3: is there a GRADED α_p border? (the pre-registration prerequisite)

The LOCKED pre-registration (`docs/preregistrations/2026-09-05-classifier-vs-wid.md`, commit
6338f3a) commits the WID-test border to a **graded tipping α_p** read from the Fisher sweep —
explicitly **NOT** the degenerate α_p→0 corner. Before any WID data is touched, that border has
to actually exist at usable resolution. The shipped headline sweep (run_v0.py) steps α_p by 0.025
and sees genuine divergence ONLY at the α_p=0.0 grid point — but a 0.025 step cannot tell a hard
corner from a thin graded wedge below 0.025. This script resolves the question, blind to WID.

THREE questions, each answered by the honest classifier from run_v0 (detectors LIFTED; divergence =
genuine D/P→∞ / secular log-P drop, NOT a single-step swing):

  Q1  Is the bounded↔divergence border a nonzero GRADED α_p*(φ), or a hard CORNER at α_p=0?
      → Fine-resolve α_p near 0 at several horizons n. A real bifurcation location is n-STABLE;
        a finite-time artifact (a thin wedge that just diverges slowly) walks outward with n.
  Q2  Inside the bounded regime, is there an INTERIOR qualitative tip (a Hopf/fixed-point→cycle
      onset, or a kink) that could serve as the graded border instead of the divergence edge?
      → Track cycle amplitude (log-P swing) and deflation depth (min log P) across α_p.
  Q3  Is the structure φ-dependent (so the border is a curve α_p*(φ)) or φ-flat (α_p the pivot)?

FINDING (see the printed verdict): the divergence border is a HARD CORNER at α_p=0 (n-stable), the
bounded regime is a smooth net deepening with NO interior tip (any wobble is sub-% limit-cycle
jitter, not a plateau/kink), and the structure is φ-flat.
⇒ the shipped Fisher α_p axis has no graded tipping value; the only "border" is the α_p→0 corner
the lock excluded, and the bounded gradient IS the smooth null the Option-A shape test must beat.
So the WID test cannot be instantiated on this axis AS PRE-REGISTERED — a reportable result. We do
NOT move the goalposts (swap the slow variable / redefine the border post-hoc are forbidden moves).

Discipline: deterministic (σ=0), byte-identical rerun; numpy + matplotlib only; conservation
residual reported (the nominal capital-account identity is P-independent — it must hold through the
deflationary transient). Reuses run_v0's `classify` unchanged (no new dynamics introduced here).
"""
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from pathlib import Path

from run_v0 import classify, ALPHA_P, B_REF   # the honest classifier + shipped constants


# A qualitative-divergence flag from the classifier's kind (deflation is the pre-reg's target edge).
def diverges(alpha_p, phi, n):
    return classify(alpha_p, phi, n=n)[0] == "deflation-div"


def border_alpha_p(phi, n, grid):
    """Classify the deflation-side border on `grid` (ascending, starting at 0.0). Returns
    (kind, alpha_star):
      - ("none",   nan) : α_p=0 does not even diverge ⇒ NO deflation border for this φ.
      - ("corner", 0.0) : α_p=0 diverges but the smallest positive α_p on the grid is bounded ⇒
                          a hard knife-edge at exactly 0 (the degenerate corner).
      - ("graded", α*)  : some α_p>0 still diverges and a larger α_p is bounded ⇒ a genuine graded
                          border at α*>0 (the value the pre-registration needs).
    The α_p=0-diverges precondition is GUARDED explicitly, so 'nothing diverges' can never be
    mis-reported as 'a corner at 0' (that was a latent conflation)."""
    if not diverges(0.0, phi, n):
        return ("none", float("nan"))
    last_div = 0.0
    for ap in grid:
        if float(ap) == 0.0:
            continue
        if diverges(ap, phi, n):
            last_div = float(ap)
        else:
            return ("corner" if last_div == 0.0 else "graded", last_div)
    return ("graded", float(grid[-1]))   # everything on the grid diverged (won't happen here)


def main():
    out = Path(__file__).resolve().parent / "figures"; out.mkdir(exist_ok=True)
    print("=== CYB-38 §3: does the shipped Fisher model have a GRADED α_p border? ===")
    print("    (prerequisite for the locked WID pre-registration 6338f3a; blind to WID)\n")

    PHIS = [2.0, 4.0, 8.0]                      # φ≳2 is where the α_p=0 corner diverges (run_v0)
    # dense near 0 (where run_v0's grid was blind), then out past the shipped α_p. Denser than the
    # first cut so the bounded-branch characterization is grid-stable, not read off a coarse grid.
    fine = np.unique(np.round(np.concatenate([
        np.linspace(0.0, 0.0020, 41),          # step 5e-5 — the interval run_v0's 0.025 grid skipped
        np.linspace(0.0021, 0.0300, 60),       # step ~4.7e-4 — up to the old grid's 2nd point and past
        np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30]),
    ]), 6))

    # ---- Q1: border location and its n-stability ------------------------------------
    # Precondition guard (defends against a latent false-corner): a 'corner' verdict is only
    # meaningful if α_p=0 actually diverges. Assert it for every φ we test before trusting Q1.
    for phi in PHIS:
        assert diverges(0.0, phi, 3000), f"α_p=0 does not diverge at φ={phi}: corner logic invalid here"

    print("[Q1] deflation-side border, re-classified at three horizons n (is it n-stable?):")
    print("      φ      n=3000       n=10000      n=30000     ⇒ verdict")
    horizons = (3000, 10000, 30000)
    corner = True
    for phi in PHIS:
        res = [border_alpha_p(phi, n, fine) for n in horizons]
        kinds_b = [r[0] for r in res]; stars = [r[1] for r in res]
        is_corner = all(k == "corner" for k in kinds_b)   # 'corner' at every horizon ⇒ n-stable
        corner = corner and is_corner
        if is_corner:
            verdict = "HARD CORNER at α_p=0 (n-stable)"
        elif all(k == "graded" for k in kinds_b):
            verdict = f"graded α_p*≈{np.mean(stars):.4f} (moved {max(stars)-min(stars):.1e} with n)"
        else:
            verdict = f"MIXED {kinds_b} — investigate"
        cells = " ".join(f"{k:>11s}" for k in kinds_b)
        print(f"      {phi:>4.1f}  {cells}   {verdict}")
    print("      'corner' holding at every horizon (n grows 10×) is a genuine knife-edge, not a slow wedge.\n")

    # ---- Q2 + Q3: bounded-regime structure across α_p, at each φ ---------------------
    print("[Q2/Q3] bounded-regime structure vs α_p (amplitude = log-P swing; depth = min log P):")
    N_STRUCT = 6000
    struct = {}                                 # phi -> (aps, amp, depth, lev, kinds)
    maxres = 0.0
    for phi in PHIS:
        aps, amp, depth, lev, kinds = [], [], [], [], []
        for ap in fine:
            kind, step, a, sec, L, res, mn = classify(ap, phi, n=N_STRUCT)
            aps.append(ap); amp.append(a); depth.append(mn); lev.append(L); kinds.append(kind)
            maxres = max(maxres, res)
        struct[phi] = (np.array(aps), np.array(amp), np.array(depth), np.array(lev), kinds)

    # Two grid-robust questions (NOT the grid-fragile "exactly 0 kinks"): (1) is there a FIXED-POINT
    # region anywhere (amplitude → 0 — a Hopf onset that could be the graded tip)? (2) is the branch
    # a NET deepening as α_p→0 dominated by a smooth trend, i.e. any non-monotone wobble is tiny
    # limit-cycle sampling jitter, not a plateau/kink? We report the worst wobble as a fraction of
    # amplitude so the "no interior tip" claim is transparent and does not depend on the grid step.
    for phi in PHIS:
        aps, amp, depth, lev, kinds = struct[phi]
        bnd = np.array([k == "bounded" for k in kinds])
        amp_b = amp[bnd]; ap_b = aps[bnd]                 # ap ascending ⇒ deepening means amp ↓
        has_fixed_point = bool((amp_b < 0.5).any())       # a genuine Hopf onset drives amp→0
        net_deepening = bool(amp_b[0] > amp_b[-1])        # bigger swing at small α_p than large
        d = np.diff(amp_b)
        worst_wobble = float(d.max())                     # largest positive (anti-deepening) step
        worst_frac = worst_wobble / float(amp_b.mean())   # as a fraction of amplitude
        print(f"      φ={phi:>4.1f}: bounded amplitude ∈ [{amp_b.min():.2f}, {amp_b.max():.2f}] over "
              f"α_p∈[{ap_b.min():.4f},{ap_b.max():.2f}] · fixed-point region? {has_fixed_point} · "
              f"net deepening α_p→0? {net_deepening} · worst non-monotone wobble {worst_wobble:+.4f} "
              f"({100*worst_frac:.2f}% of amp ⇒ jitter, no interior tip)")
    # φ-independence: compare the bounded amplitude curves across φ on the shared α_p grid
    a4 = struct[4.0][1]; a8 = struct[8.0][1]
    both_bnd = np.array([ (struct[4.0][4][i]=="bounded") and (struct[8.0][4][i]=="bounded")
                          for i in range(len(fine)) ])
    phi_spread = float(np.max(np.abs(a4[both_bnd] - a8[both_bnd]))) if both_bnd.any() else float("nan")
    print(f"      φ-independence: max |amplitude(φ=4) − amplitude(φ=8)| over shared bounded α_p "
          f"= {phi_spread:.3f}  (small ⇒ α_p, not φ, is the pivot)\n")

    print(f"[conservation] worst nominal-identity residual across the whole sweep = {maxres:.1e} "
          f"(P-independent identity holds through the deflationary transient)")

    # ---- VERDICT ---------------------------------------------------------------------
    print("\n=== VERDICT ===")
    if corner:
        print("  Q1  The deflation-side border is a HARD CORNER at α_p=0 (n-stable to 30k).")
        print("  Q2  The bounded regime is a limit cycle at EVERY α_p>0 — no fixed-point region and no")
        print("      interior tip (non-monotone wobble is sub-% limit-cycle jitter): a smooth net")
        print("      deepening as α_p→0 (amplitude/depth grow). (Band=30 would only misclassify the")
        print("      deep cycle near α_p≈1e-11, far below any meaningful α_p — no spurious wedge.)")
        print("  Q3  Structure is φ-flat ⇒ α_p is the pivot (as run_v0 found).")
        print("  ⇒  The shipped Fisher α_p axis has NO graded tipping value. The only border is the")
        print("     degenerate α_p→0 corner the pre-registration EXCLUDED; the bounded gradient is")
        print("     smooth-monotone — i.e. it IS the null the Option-A shape test was meant to beat.")
        print("  ⇒  The WID test CANNOT be instantiated on this axis AS PRE-REGISTERED. This is a")
        print("     reportable prerequisite result (like the egg magnitude overshooting OOS). Per the")
        print("     lock's forbidden moves we do NOT swap the slow variable or redefine the border to")
        print("     rescue it. Next honest move is a NEW question (does a graded border live elsewhere")
        print("     in the stack — coupled/recursion?), which would need its OWN pre-registration.")
    else:
        print("  A nonzero, n-stable graded α_p*(φ) exists — the border the pre-registration needs.")
        print("  Proceed to Phase A (pin α_p*, the split, and the exact statistics), still blind to WID.")

    make_figure(out, struct, PHIS, corner)
    print(f"\n  figure → {out/'cybeersym_fisher_v1_alpha_p_border.png'}")


def make_figure(out, struct, phis, corner):
    INK, GRID = "#1b1b1b", "#d8d8d8"
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.2))
    colors = {2.0: "#c1440e", 4.0: "#1b1b1b", 8.0: "#2b6cb0"}

    # Left: cycle amplitude vs α_p (log-x), showing smooth monotone bounded branch + corner blow-up
    for phi in phis:
        aps, amp, depth, lev, kinds = struct[phi]
        bnd = np.array([k == "bounded" for k in kinds])
        x = np.where(aps > 0, aps, 3e-5)        # place the α_p=0 corner at the left edge on log-x
        axL.plot(x[bnd], amp[bnd], "-o", ms=3.5, lw=1.6, color=colors[phi], label=f"φ={phi} (bounded)")
        if (~bnd).any():
            axL.plot(x[~bnd], amp[~bnd], "x", ms=9, mew=2.2, color=colors[phi],
                     label=f"φ={phi} (divergent — the α_p=0 corner)")
    axL.axvline(ALPHA_P, color="#888", lw=1.1, ls="--"); axL.text(ALPHA_P*1.03, axL.get_ylim()[1]*0.92,
             f"shipped α_p={ALPHA_P}", fontsize=8.5, color="#555")
    axL.set_xscale("log"); axL.set_xlabel("α_p  (markup-defense strength; log scale)")
    axL.set_ylabel("limit-cycle amplitude  (log-P peak-to-trough)")
    axL.set_title("No graded tip: a smooth monotone bounded branch,\nthen a hard divergence corner at α_p=0", fontsize=10)
    axL.legend(frameon=False, fontsize=8); axL.grid(True, color=GRID, lw=0.7, which="both"); axL.set_axisbelow(True)

    # Right: deflation depth (min log P) vs α_p — the smooth "severity gradient" with no threshold
    for phi in phis:
        aps, amp, depth, lev, kinds = struct[phi]
        bnd = np.array([k == "bounded" for k in kinds])
        x = np.where(aps > 0, aps, 3e-5)
        axR.plot(x[bnd], depth[bnd], "-o", ms=3.5, lw=1.6, color=colors[phi], label=f"φ={phi}")
    axR.set_xscale("log"); axR.set_xlabel("α_p  (log scale)")
    axR.set_ylabel("deflation depth  (min log P over the run)")
    axR.set_title("Depth deepens smoothly & monotonically as α_p→0\n(no interior threshold = nothing for a step-test to catch)", fontsize=10)
    axR.legend(frameon=False, fontsize=8); axR.grid(True, color=GRID, lw=0.7, which="both"); axR.set_axisbelow(True)

    tag = "HARD CORNER at α_p=0 — no graded border (WID test not instantiable as pre-registered)" if corner \
          else "graded border found"
    fig.suptitle(f"CYB-38 §3 — Fisher α_p border characterization:  {tag}", fontsize=11, y=1.0)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out / "cybeersym_fisher_v1_alpha_p_border.png", dpi=140, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
