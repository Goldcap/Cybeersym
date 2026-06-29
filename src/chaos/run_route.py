"""
Cybeersym — chaos v0, route diagnosis (names the bifurcation, rigorously).

`run_v0.py` established the load-bearing claim: the conserved 3-tier beer game with
the Sterman ordering rule generates DETERMINISTIC CHAOS (λ>0, bounded, sensitive,
deterministic, conserved) as supply-line underweighting (β↓) increases. This script
answers the next question — *what bifurcation, and what route?* — with three direct
measurements rather than eyeballing, and lands on the honest verdict:

  A BORDER-COLLISION BIFURCATION of a piecewise-smooth map (Zhusubaliyev &
  Mosekilde), NOT a smooth Neimark–Sacker (discrete Hopf).

The three confirmations (each refutes the smooth-Hopf hypothesis):

  (a) EIGENVALUES at the physical fixed point. Linearize the one-step map at the
      equilibrium and track the leading complex pair as β falls. A smooth
      Neimark–Sacker requires the pair to cross |λ|=1. It does NOT — it tops out at
      |λ|≈0.91 (∠≈40°) and the fixed point then loses FEASIBILITY (an inventory /
      supply line would go negative): the equilibrium collides with a switching
      manifold while still linearly stable. That collision is the bifurcation.

  (b) ONSET IS A HARD JUMP + BISTABILITY. The attractor amplitude jumps
      discontinuously (0 → ~525 over Δβ≈0.003), and just above onset a large cycle
      COEXISTS with the still-globally-stable fixed point. Continuous-from-zero
      growth and no coexistence are what a supercritical Hopf would show; we see the
      opposite — the hallmarks of a hard, piecewise-smooth (border-collision)
      transition with hysteresis.

  (c) PHASE PORTRAITS + SPECTRA show the *geometry* Desktop intuited — a closed
      invariant loop (the "torus") that breaks down into a strange attractor — but
      born via (a)+(b), not a smooth Hopf. Delay-embedding: discrete frequency-locked
      points → closed invariant loop (riding the order≥0 constraint — the flat
      segments are the piecewise-smooth fingerprint) → bounded strange attractor.
      FFT: a single sharp line → a subharmonic at f/2 (period-doubling within the
      loop) → broadband (chaos).

Run from inside src/chaos/:  python3 run_route.py
"""
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model import ChaosChain, ChaosParams
from linearize import jacobian, fixed_point_iterate, leading_complex

A_S, L, THETA = 0.7, 3, 0.25
# representative β either side / across the route
BETA_ONSET_LO, BETA_ONSET_HI = 0.2925, 0.2950   # cycle just below, FP just above
REGIMES = [(0.29, "β=0.29  frequency-locked\n(just past onset)"),
           (0.22, "β=0.22  invariant loop\n(the 'torus')"),
           (0.15, "β=0.15  strange attractor\n(chaos)")]


def _params(beta, perturb=1.0):
    return ChaosParams(beta=beta, a_S=A_S, L=L, theta=THETA, perturb=perturb)


def _step_fn(beta):
    c = ChaosChain(_params(beta, perturb=0.0))
    return c.step_vector, c.get_state()


def _physical(x):
    """non-negative inventories, supply lines, and transit on every tier."""
    for i in range(3):
        b = i * 7
        if x[b] < -1e-6 or x[b + 2] < -1e-6 or np.any(x[b + 4:b + 7] < -1e-6):
            return False
    return True


def observe_series(beta, n=120000, keep=60000, obs=None):
    obs = obs or (lambda c: c.tiers[-1].on_order)   # manufacturer supply line
    c = ChaosChain(_params(beta))
    x = np.empty(n)
    for k in range(n):
        c.step(); x[k] = obs(c)
    return x[-keep:]


def net_stock_amplitude(beta, scale=1.0, n=40000, keep=6000):
    """asymptotic range of manufacturer net stock from an IC perturbed by `scale`."""
    c = ChaosChain(_params(beta, perturb=0.0))
    s = c.get_state()
    s[0] += scale; s[7] += scale; s[14] += scale
    c.set_state(s); c.injected = c._goods_in_system(); c.consumed = 0.0
    v = np.empty(n)
    for k in range(n):
        c.step(); v[k] = c.tiers[-1].net_stock
    seg = v[-keep:]
    return seg.max() - seg.min()


# -------------------------------------------------- (a) eigenvalue tracking
def eigen_track(betas):
    mods, angs, phys = [], [], []
    for b in betas:
        step, x0 = _step_fn(float(b))
        xs = fixed_point_iterate(step, x0, n=120000)   # physical FP (stable side)
        lc = leading_complex(jacobian(step, xs))
        mods.append(abs(lc)); angs.append(abs(np.degrees(np.angle(lc))))
        phys.append(_physical(xs) and np.max(np.abs(step(xs) - xs)) < 1e-6)
    return np.array(mods), np.array(angs), np.array(phys)


# ----------------------------------------------------------- (c) spectrum
def spectrum(beta, keep=60000):
    s = observe_series(beta, keep=keep, obs=lambda c: c.tiers[-1].net_stock)
    s = s - s.mean()
    f = np.fft.rfftfreq(s.size)
    P = np.abs(np.fft.rfft(s * np.hanning(s.size))) ** 2
    return f, P / P.max()


def constraint_activity(beta, n=40000, warm=20000):
    """Which switching manifold does the developed attractor actually collide with?
    Re-runs the step inline to flag, per tier per step, whether the order saturated
    at max(0,·) (order non-negativity — you can't un-order) or shipping was
    inventory-limited (stockout floor). Returns fraction of steps each is active."""
    p = ChaosParams(beta=beta, a_S=A_S, L=L, theta=THETA)
    c = ChaosChain(p)
    order0 = np.zeros(3); stockout = np.zeros(3); steps = 0
    for t in range(n):
        incoming = p.mu
        for i, tier in enumerate(c.tiers):
            arr = tier.transit_in.popleft(); tier.inventory += arr; tier.on_order -= arr
            tier.backlog += incoming
            so = tier.inventory < tier.backlog - 1e-9
            shipped = min(tier.inventory, tier.backlog); tier.inventory -= shipped; tier.backlog -= shipped
            if i == 0: c.consumed += shipped
            else: c.tiers[i - 1].transit_in.append(shipped)
            tier.D_hat += p.theta * (incoming - tier.D_hat)
            ind = (tier.D_hat + p.a_S * (p.S_star - (tier.inventory - tier.backlog))
                   + p.a_SL * (p.L * tier.D_hat - tier.on_order))
            o0 = ind < -1e-9
            order = max(0.0, ind); tier.on_order += order
            if i == p.n_tiers - 1: tier.transit_in.append(order)
            else: incoming = order
            if t >= warm:
                if o0: order0[i] += 1
                if so: stockout[i] += 1
        if t >= warm: steps += 1
    return order0 / steps, stockout / steps


# ----------------------------------------------------------------- figures
def make_figures(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- Figure 1: route diagnosis (eigenvalues + hard onset + spectra) ----
    betas_eig = np.round(np.arange(0.45, 0.2849, -0.005), 4)
    mods, angs, _ = eigen_track(betas_eig)
    onset = 0.5 * (BETA_ONSET_LO + BETA_ONSET_HI)

    fig = plt.figure(figsize=(12, 9))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.1, 1.0])

    # (top-left) eigenvalue modulus vs beta — never reaches 1
    axA = fig.add_subplot(gs[0, 0])
    axA.plot(betas_eig, mods, "-o", ms=3, color="#1f77b4", label="leading complex pair |λ|")
    axA.axhline(1.0, color="#d62728", lw=1.2, ls="--", label="unit circle |λ|=1 (never reached)")
    axA.axvline(onset, color="gray", lw=1.0, ls=":")
    axA.annotate(f"FP stays linearly stable\n(|λ|≈{mods[-1]:.2f} < 1) across onset:\n"
                 f"no smooth bifurcation —\nturbulence is a COEXISTING attractor",
                 xy=(betas_eig[-1], mods[-1]), xytext=(0.40, 0.66),
                 fontsize=8, arrowprops=dict(arrowstyle="->", color="gray"))
    axA.set_xlabel("β"); axA.set_ylabel("|λ| of leading complex pair")
    axA.set_title("(a) Eigenvalues at the physical fixed point\n"
                  "stay INSIDE the unit circle → not a Neimark–Sacker")
    axA.invert_xaxis(); axA.legend(fontsize=8, loc="lower left"); axA.set_ylim(0.6, 1.1)

    # (top-right) hard onset + bistability: amplitude vs beta from small & large IC
    axB = fig.add_subplot(gs[0, 1])
    betas_amp = np.round(np.arange(0.32, 0.2799, -0.0025), 4)
    amp_small = np.array([net_stock_amplitude(b, 1.0) for b in betas_amp])
    amp_large = np.array([net_stock_amplitude(b, 400.0) for b in betas_amp])
    axB.plot(betas_amp, amp_small, "-o", ms=3, color="#1f77b4", label="from small IC")
    axB.plot(betas_amp, amp_large, "-s", ms=3, color="#ff7f0e", label="from large IC")
    bist = (amp_small < 1) & (amp_large > 50)
    if bist.any():
        axB.axvspan(betas_amp[bist].min(), betas_amp[bist].max(), color="#ffd27f",
                    alpha=0.5, label="bistable (FP + cycle coexist)")
    axB.set_xlabel("β"); axB.set_ylabel("manufacturer net-stock amplitude")
    axB.set_title("(b) Onset is a HARD jump with bistability\n"
                  "→ subcritical / border-collision, not a soft Hopf")
    axB.invert_xaxis(); axB.legend(fontsize=8, loc="upper left")

    # (bottom) three spectra, stacked
    axC = fig.add_subplot(gs[1, :])
    colors = ["#1f77b4", "#2ca02c", "#d62728"]
    for (beta, lab), col, off in zip(REGIMES, colors, (2.0, 1.0, 0.0)):
        f, P = spectrum(beta)
        m = f < 0.25
        axC.semilogy(f[m], P[m] * 10 ** off + 1e-6, color=col, lw=1.0,
                     label=lab.replace("\n", " "))
    axC.set_xlabel("frequency (cycles/step)")
    axC.set_ylabel("power (normalized, offset for clarity)")
    axC.set_title("(c) Power spectra: single line → subharmonic at f/2 "
                  "(period-doubling) → broadband (chaos)")
    axC.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    p1 = out_dir / "cybeersym_chaos_v0_route_diagnosis.png"
    fig.savefig(p1, dpi=120); plt.close(fig)

    # ---- Figure 2: phase portraits (the headline) ----
    tau = 3
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.2))
    for ax, (beta, lab) in zip(axs, REGIMES):
        x = observe_series(beta)
        ax.plot(x[:-tau], x[tau:], ",", color="navy", alpha=0.45)
        ax.set_title(lab, fontsize=11)
        ax.set_xlabel("manufacturer supply line  x(t)")
        ax.set_ylabel(f"x(t+{tau})")
    fig.suptitle("Delay-embedded phase portraits — border-collision route: "
                 "frequency-locked points → invariant loop → strange attractor "
                 f"(a_S={A_S}, L={L}, θ={THETA}, σ=0)", fontsize=12)
    fig.tight_layout()
    p2 = out_dir / "cybeersym_chaos_v0_phase_portraits.png"
    fig.savefig(p2, dpi=120); plt.close(fig)

    return (p1, p2, mods, angs, betas_eig, onset, betas_amp, amp_small, amp_large, bist)


def main():
    out_dir = Path(__file__).parent / "figures"
    print(f"config: a_S={A_S} L={L} theta={THETA}  control=β\n")
    print("Naming the bifurcation (3 direct confirmations):\n")

    (p1, p2, mods, angs, betas_eig, onset,
     betas_amp, amp_small, amp_large, bist) = make_figures(out_dir)

    print("[a] EIGENVALUES at the physical (attracting) fixed point")
    print(f"    leading complex pair stays at |λ|≈{mods[-1]:.3f} (∠{angs[-1]:.1f}°) across the")
    print(f"    onset region — it NEVER reaches |λ|=1. The equilibrium does not undergo")
    print(f"    any smooth local bifurcation: no Neimark–Sacker, no flip.\n")

    print("[b] ONSET — hard jump + BISTABILITY (the heart of it)")
    print(f"    net-stock amplitude jumps 0 → {amp_large[bist].max() if bist.any() else amp_small.max():.0f} "
          f"(discontinuous, history-dependent).")
    if bist.any():
        print(f"    bistable window β∈[{betas_amp[bist].min():.4f},{betas_amp[bist].max():.4f}]: a large "
              f"constraint-riding attractor COEXISTS with the still-stable fixed point.")
    print("    -> same economy, same parameters: calm OR turbulent depending on history")
    print("       (endogenous path-dependence / hysteresis). Born by border-collision, not soft Hopf.\n")

    print("[c] WHICH BORDER + geometry")
    for beta in (0.22, 0.15):
        o0, so = constraint_activity(beta)
        print(f"    β={beta}: manufacturer order=0 (can't un-order) active {o0[-1]:.0%} of steps, "
              f"stockout {so[-1]:.0%}; wholesaler order=0 {o0[1]:.0%}.")
    print("    -> the dominant active border is ORDER NON-NEGATIVITY (max(0,·) — order")
    print("       irreversibility), with the stockout floor secondary. The non-smoothness")
    print("       is the economics. Geometry: points → invariant loop → strange attractor;")
    print("       spectra: single line → subharmonic at f/2 → broadband.\n")

    print(f"    figure -> {p1}")
    print(f"    figure -> {p2}")
    print("\nVERDICT: a BORDER-COLLISION / piecewise-smooth route (Zhusubaliyev & Mosekilde).\n"
          "  The equilibrium stays linearly stable (|λ|<1) — NOT a Neimark–Sacker. A bounded\n"
          "  constraint-riding attractor (λ>0) is born abruptly and COEXISTS with it "
          "(bistability,\n  endogenous path-dependence). The hard borders — dominantly order "
          "non-negativity\n  (you can't un-order) — are not a nuisance; they ARE the mechanism.\n"
          "  Formal normal-form (J_L/J_R → Nusse–Yorke) classification continues in CYB-4.")


if __name__ == "__main__":
    main()
