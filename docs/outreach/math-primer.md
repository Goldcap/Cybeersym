# A ground-up primer on the math in the bifurcation note

A plain-language companion to `bifurcation-note.md`, written for a non-specialist author who
wants to **own every claim in the note** before it reaches an external reviewer. No prior
dynamical-systems background assumed. Each concept is anchored to the section of the note
where it appears.

> This primer teaches the *ideas*. It is not itself part of the outreach artifact — it is
> study material. The note stays lean and self-contained.

---

## 0. The one big idea

Dynamical systems studies a single question: **you have a rule, you apply it over and over
— what happens in the long run?** The rule is a **map**, `F`. Applying it repeatedly,
`x₁ = F(x₀)`, `x₂ = F(x₁)`, … , produces a **trajectory** `x₀, x₁, x₂, …` — the path the
system traces.

## 1. State = a point in a high-dimensional space  *(note §1)*

The system's condition at one instant is 21 numbers (per tier: inventory, backlog, supply
line, forecast, 3 transit slots → 3×7 = 21). Treat those 21 numbers as the **coordinates
of one point** in 21-dimensional space. You can't picture 21-D, but the math handles it
exactly like a point in 3-D with more coordinates. `F` moves that point; the trajectory is
the point hopping around. That is all `F_β : ℝ²¹ → ℝ²¹` means.

## 2. Equilibrium = a point that doesn't move  *(note §2.1)*

A **fixed point** / **equilibrium** satisfies `F(x*) = x*`: apply the rule, nothing changes.
Here it is the calm state — every tier orders exactly 100, stocks sit at target, nothing
sloshes.

## 3. Stability, eigenvalues, and the unit circle — the central tool  *(note §3.3)*

Two marbles: one at the bottom of a **bowl** (nudge → rolls back = **stable**); one on top of
a **dome** (nudge → rolls away = **unstable**). To decide which an equilibrium is:

1. **Zoom in** very close to the fixed point, where the complicated rule `F` looks like
   simple stretching/rotating — a linear map captured by a matrix, the **Jacobian**.
2. Read that matrix's **eigenvalues** `λ`. Each says: *along one special direction, a small
   nudge is multiplied by `λ` every step.*
   - `|λ| < 1` → nudge **shrinks** → stable direction.
   - `|λ| > 1` → nudge **grows** → unstable direction.
3. Eigenvalues can be **complex**, so plot them on a plane; the decision line is the
   **unit circle** (radius 1). **Inside = stable, outside = unstable, on it = knife's edge.**
   A complex eigenvalue means the nudge also **spirals** (water circling a drain); its angle
   is how fast it rotates.

> **Memorize this:** the fate of a fixed point is decided by whether its eigenvalues sit
> inside or outside the unit circle.

The note's "leading complex pair, modulus ≈ 0.91, argument ≈ 40°" = the strongest
nudge-direction shrinks to 91% each step while spiralling — safely inside the circle → the
calm state is **stable**, and stays so (≈0.91, never reaching 1) as the knob turns.

## 4. Bifurcation = turning a knob until behavior suddenly changes  *(note §4)*

A **bifurcation** is a qualitative reorganization caused by a small parameter change. The
knob here is `β` (how much each tier trusts orders already in the pipeline). Standard
bifurcations are named by **how an eigenvalue crosses the unit circle**:

| crossing | name | what appears |
|----------|------|--------------|
| exits through **−1** | period-doubling (flip) | alternation between two states *(§4.1)* |
| a **complex pair** crosses | Neimark–Sacker | a small **loop** / oscillation *(§4.2)* |
| exits through **+1** | fold / saddle-node | fixed points appear or annihilate |

The note's §4 is a detective story: each was checked; **the eigenvalues never actually cross
the circle** (they park at 0.91). None of the standard "fixed point loses stability" stories
apply — the negative result at the heart of the note.

## 5. What trajectories settle onto — three kinds of attractor  *(note §3)*

An **attractor** is the long-run destiny of a trajectory:
- **Fixed point** — a single spot (calm).
- **Limit cycle** — a repeating **loop** (steady oscillation).
- **Strange attractor** — bounded but **never-repeating** → **chaos**.

"Invariant set" = a set that maps into itself (once on it, you stay). "Attracting" adds that
nearby trajectories get pulled onto it.

## 6. Chaos, precisely — and why "bounded" matters  *(note §3.1)*

Chaos has a sharp definition: **two nearly-identical starts drift apart exponentially fast**
(the butterfly effect), measured by the **largest Lyapunov exponent** `Λ`:
- `Λ < 0` → nearby trajectories converge (predictable).
- `Λ > 0` → they separate exponentially (chaotic) — here `Λ ≈ 0.054` nats/step.

But `Λ > 0` alone is not chaos: a trajectory exploding to infinity also has `Λ > 0`. Chaos
requires **bounded AND `Λ > 0`**. That is why the note insists the attractor stays bounded
(amplitude ≈525, not growing without limit) and *excludes* the runaway corner. The measuring
tool is validated first on the logistic map, where the answer is known exactly (`Λ = ln 2`).

## 7. The two twists that put this outside the textbook

Everything above is the **smooth** textbook. This system breaks it two ways — and those two
breaks are the reason the question deserves an expert.

### 7a. Kinks / borders → border-collision  *(note §3.4, §4.3)*
The rule has `max(0, order)` (no negative orders) and `min(inventory, backlog)` (can't ship
what you don't have). These are **kinks**: one linear map on one side, a *different* one on
the other. The dividing surfaces are **switching manifolds** (the "borders"). Kinked systems
have their own bifurcation — a **border-collision**, where the action is an orbit or fixed
point *hitting a border*, not an eigenvalue crossing the circle (theory: Nusse–Yorke,
Banerjee–Grebogi). §4.3 checks it and finds it *also* doesn't apply: the fixed point never
touches a border (orders = 100; stockout margin ≈ 129 — both far from their borders).

### 7b. Conservation → eigenvalues stuck on the circle → non-hyperbolic  *(note §2.2)*
The quantities `Cᵢ = Oᵢ − (sum of tier i's transit slots)` **never change** — they are
**conserved** (accounting identities; goods can't appear or vanish). A conserved quantity is
a **first integral**. A direction that never changes is a nudge that neither grows nor
shrinks → **eigenvalue exactly 1** → sitting **on** the unit circle, permanently, for every
β. Three conserved quantities → **three eigenvalues pinned at +1**.

Having an eigenvalue *on* the circle is called **non-hyperbolic** — and the standard
bifurcation theorems all require the fixed point to be **hyperbolic** (every eigenvalue
strictly off the circle). So this equilibrium sits in the theorems' blind spot *by
construction*, because of the very conservation laws that make the model physically honest.

**The leaf idea** *(note §2.2, §5):* since those three quantities are frozen, the real motion
lives on an **18-dimensional slice** (fix the 3 conserved values = a "conservation leaf"
`𝓛_c`). One request to the reviewer is exactly: *should the frozen directions be removed by
restricting to that 18-D leaf — is that the correct first reduction?*

## 8. Coexistence / bistability / hysteresis  *(note §3.2)*

Rather than "calm below threshold, turbulent above," a window of β has **both** the calm
fixed point **and** the turbulent attractor at once. Which one is realized depends on **where
you start** (small nudge → calm; large nudge → turbulence). Two destinies at identical
parameters, selected by history = **bistability / hysteresis**. It is why the attractor is
*born at finite amplitude* (appears full-sized, jumping 0 → ~525) instead of growing gently
from zero.

## 9. Why the question is well-posed (the thing to be able to say aloud)

The standard toolbox assumes (1) the fixed point is **hyperbolic** and (2) a bifurcation is
the fixed point **crossing the circle or colliding with a border**. This system violates
both, yet a large chaotic attractor still appears abruptly:
- nothing crosses the circle (the pair parks at 0.91);
- the fixed point never touches a border (interior; margins wide);
- three eigenvalues are permanently at +1 (non-hyperbolic, from conservation).

So the attractor is **not** created by anything happening *to the equilibrium*. It appears
elsewhere in the space and **coexists** with the still-calm equilibrium — a **global** event
(about the whole space, not a neighborhood of the fixed point) that is also **nonsmooth**
(the kinks matter). Asking *which established framework classifies this* is a genuine,
well-posed open question — precisely because the conservation laws push the equilibrium out
of the standard theory. That is the real mathematical content, not a gap in the author's
understanding.

---

### The vocabulary map

Every phrase in the note is one of the nine ideas above:

| note phrase | idea |
|-------------|------|
| piecewise-affine map | §1 rule + §7a kinks |
| interior equilibrium | §2 fixed point, far from borders |
| transverse spectrum / modulus | §3 eigenvalues vs the unit circle |
| non-hyperbolic, first integrals, λ=+1 | §7b conservation directions |
| period-doubling / Neimark–Sacker / border-collision | §4 named bifurcations |
| largest Lyapunov exponent | §6 chaos measure |
| bounded attractor | §5–6 chaos needs boundedness |
| coexistence / bistability / hysteresis | §8 two destinies, history-selected |
| global nonsmooth event | §9 the open question |
