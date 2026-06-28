# BULLWHIP_SPEC — feedback to the spec author (from Claude Code)

**TL;DR:** I built v0 exactly as `BULLWHIP_SPEC.md` specifies and ran it. The
strict "fixed forecast only" scope rule **removes the mechanism that creates
bullwhip** — every tier passes demand through one-for-one, ratio = 1.000
everywhere, and the killer experiment (local vs shared) can't fire because there
is nothing to localize. This note documents the finding with reproducible
numbers and proposes concrete edits so v0 demonstrates the phenomenon honestly.

This is a *method* issue, not a bug — surfaced exactly the way this repo wants
things surfaced (build to spec, run, let the data refute the design).

---

## What I found (both runs conserve goods to <1e-9, both deterministic)

### Run A — spec-faithful (fixed forecast, `mu` known): the NULL
`src/bullwhip/model.py` as written. Order-up-to-S with constant `S = mu*(L+1) +
safety`.

```
mode              retailer    wholesaler  manufacturer         CHAIN
local_info           1.000         1.000         1.000         1.000
shared_info          1.000         1.000         1.000         1.000   (max goods residual 5e-12)
```

**Why it must be 1.0, not a tuning accident:** with a *known* stationary mean,
the inventory position falls by exactly the demand each step, so
`order = S - IP = demand` identically. This is the classic result (Lee,
Padmanabhan & Whang 1997; Chen, Drezner, Ryan & Simchi-Levi 2000): base-stock
with a known mean has **no** bullwhip. And because `S` is the same known constant
regardless of what a tier "sees," `local_info` and `shared_info` are byte-for-byte
identical — the killer experiment has no contrast to expose.

### Run B — minimal demand-signal processing (estimate the mean from observed demand)
The one change: each tier does **not** know `mu`; it estimates it as a moving
average (window `p`) of the demand it observes, and sets `S_t = muhat_t*(L+1) +
safety`. Under `local_info` it averages the **downstream orders it receives**;
under `shared_info` it averages **true consumer demand**.

```
mode      ratios (ret, whl, mfr)     CHAIN     (L=2, p=4, sigma=10, mu=100, seed=0)
local      3.56   4.47   3.93        62.4      <- bullwhip
shared     3.56   2.32   1.81        15.0      <- collapses; killer experiment fires
```

Retailer is identical across modes (it always sees true consumer demand) — a good
sanity check. Single-stage Chen et al. closed form `1 + 2L/p + 2L^2/p^2 = 2.5`
for L=2,p=4; my retailer reads 3.56 (same order of magnitude, higher because the
sim also carries the stockout/backlog + `max(0, .)` nonlinearity on top of the
linear forecast term — that is the v0 "order-of-magnitude" bar, not a tuned match).

**Repro for Run B** (self-contained; run from repo root):
```python
import numpy as np
from collections import deque
def run(mode,p=4,L=2,mu=100.,sigma=10.,T=400,warmup=100,seed=0):
    rng=np.random.default_rng(seed); D=np.maximum(0,mu+rng.normal(0,sigma,T))
    safety=sigma*np.sqrt(L+1)
    inv=[mu+safety]*3; back=[0.]*3; onord=[mu*L]*3
    tr=[deque([mu]*L,maxlen=L) for _ in range(3)]; win=[deque([mu]*p,maxlen=p) for _ in range(3)]
    op=np.zeros((3,T)); dr=np.zeros((3,T))
    for t in range(T):
        inc=D[t]
        for i in range(3):
            a=tr[i].popleft(); inv[i]+=a; onord[i]-=a
            back[i]+=inc; dr[i,t]=inc
            win[i].append(D[t] if mode=='shared' else inc)
            s=min(inv[i],back[i]); inv[i]-=s; back[i]-=s
            if i>0: tr[i-1].append(s)
            S=np.mean(win[i])*(L+1)+safety
            o=max(0.,S-(inv[i]-back[i]+onord[i])); onord[i]+=o; op[i,t]=o
            if i==2: tr[i].append(o)
            else: inc=o
    return [np.var(op[i,warmup:])/np.var(dr[i,warmup:]) for i in range(3)]
for m in ('local','shared'): print(m, [round(x,2) for x in run(m)])
```

---

## The taxonomy question this raises (the real decision)

The spec defers "adaptive / forecast-from-orders" to v1, calling it **reflexivity**.
But there are two different things wearing that label:

- **Estimating an unknown demand *mean*** from observed orders (a moving average).
  This is mechanical parameter estimation — you *cannot operate a base-stock
  policy without some mean estimate*. It is reactive, backward-looking, and has
  no price/anticipation content. I'd argue this belongs to **RECURSION**: it is
  the irreducible information distortion of propagating through the pipes, and it
  is precisely the cause Lee et al. (1997) named "demand signal processing."

- **Anticipating future *prices/regime*** and acting on the forecast (firms
  repricing ahead, the Lucas critique). *That* is the reflexivity cell in
  `THESIS.md` — forward-looking expectations, a genuinely different mechanism.

The spec conflated "known `mu`" with "no forecasting." Dropping that conflation
(a tier estimates the mean it doesn't know, but does **not** anticipate prices)
keeps v0 strictly inside the recursion channel *and* makes the phenomenon appear.

## Proposed concrete edits to BULLWHIP_SPEC.md

1. **§ "The decision rule"** — replace "fixed forecast, `S` constant, `mu` known"
   with: *mean estimated by a moving average of observed demand over window `p`;
   `S_t = muhat_t*(L+1) + safety`.* Add `p` to the Constants list (e.g. `p = 4`).
   Keep `mu` known only for the **control** run (below).

2. **§ "Scope discipline"** — change the first bullet. Forecasting the unknown
   demand *mean* is IN scope (it is the recursion-channel cause). What stays OUT
   of v0 (deferred to v1) is **price anticipation / expectations** — agents acting
   on a forecast of the *system*, not of the demand level. Make that distinction
   explicit so the recursion/reflexivity boundary is clean.

3. **§ "The two modes"** — under `local_info` a tier's `muhat` is averaged over
   the **downstream orders it receives**; under `shared_info`, over **true
   consumer demand**. That is what makes the modes differ (they are identical
   under known `mu`).

4. **§ "What success looks like"** — add a criterion 0 / control: *fixed-`mu`
   base-stock yields ratio = 1.000 at every tier (no amplification, no
   local/shared gap). The amplification in the treatment is therefore attributable
   to the locally-estimated mean, not to lead time alone.* This control/treatment
   contrast is a stronger proof than the treatment alone and is cheap to keep.

5. **§ "Validation targets"** — the single-stage floor to check against is Chen
   et al. (2000): `BW_1stage = 1 + 2L/p + 2L^2/p^2`. Expect the sim retailer to
   sit at the same order of magnitude (higher, due to the stockout nonlinearity).

## What I'm keeping in the tree meanwhile
- `src/bullwhip/model.py` — the spec-faithful engine. It is **correct as the
  control** (Run A). When the spec is revised I'll add the estimated-mean path as
  the treatment and keep this as the fixed-`mu` baseline.
- `src/bullwhip/measure.py` — `bullwhip_ratio` + report/table. Unaffected by the
  decision; reusable as-is.
- Not yet written (waiting on the revised spec): `run_v0.py`, `figures/`, README.

— Claude Code
