#!/usr/bin/env python3
"""Generate (or --check) the fidelity reference for the viz.

The viz (`viz/index.html`) contains a JS RK4 port of `src/goodwin_keen/model.py`. This script is the
SOURCE OF TRUTH side of the CI fidelity gate: it runs the real numpy engine and emits reference
trajectory checkpoints. `viz/verify_fidelity.mjs` then runs the JS port over the same checkpoints and
asserts they agree to < 1e-6.

    python3 viz/gen_reference.py            # print reference JSON to stdout
    python3 viz/gen_reference.py --write    # write viz/fidelity-reference.json
    python3 viz/gen_reference.py --check     # regenerate and diff against the committed JSON (CI drift guard)

Run from the repo root. Deterministic (σ=0). numpy only.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from goodwin_keen.model import GKParams, gk_step, goodwin_equilibrium, keen_good_equilibrium  # noqa: E402

R = 10  # round the reference to 10 dp; the gate tolerance (1e-6) is far looser, so this is exact enough


def _traj(p, s0, dumps):
    import numpy as np
    s = np.array(s0, dtype=float)
    out = {}
    for i in range(max(dumps) + 1):
        if i in dumps:
            out[str(i)] = [round(float(x), R) for x in s]
        s = gk_step(s, p)
    return out


def build():
    cases = []

    # 1. Goodwin conservative centre (keen=False, defaults), off-equilibrium start.
    p = GKParams()
    w, l, _ = goodwin_equilibrium(p)
    s0 = [round(w * 0.98, R), round(l * 0.98, R), 0.0]
    cases.append({"name": "goodwin", "params": {"keen": False},
                  "s0": s0, "checkpoints": _traj(p, s0, [1, 1000, 4000])})

    # 2. Keen stable good equilibrium (spirals in).
    p2 = GKParams(keen=True, r=0.03, delta=0.03, ksharp=40.0, kmid=0.16)
    gw, gl, gd = keen_good_equilibrium(p2)
    s2 = [round(gw * 0.98, R), round(gl * 0.98, R), round(gd + 0.02, R)]
    cases.append({"name": "keen_stable",
                  "params": {"keen": True, "r": 0.03, "delta": 0.03, "ksharp": 40.0, "kmid": 0.16},
                  "s0": s2, "checkpoints": _traj(p2, s2, [1, 20000])})

    # 3. Keen breakdown (large initial debt escapes the basin).
    s3 = [0.8, 0.9, 8.0]
    cases.append({"name": "keen_breakdown",
                  "params": {"keen": True, "r": 0.03, "delta": 0.03, "ksharp": 40.0, "kmid": 0.16},
                  "s0": s3, "checkpoints": _traj(p2, s3, [1, 6000])})
    return cases


def main():
    ref = build()
    js = json.dumps(ref, indent=2)
    out = ROOT / "viz" / "fidelity-reference.json"
    if "--check" in sys.argv:
        committed = json.loads(out.read_text())
        if committed != ref:
            print("FIDELITY REFERENCE DRIFT: viz/fidelity-reference.json does not match src/goodwin_keen/model.py.\n"
                  "Regenerate with `python3 viz/gen_reference.py --write` and review the change.", file=sys.stderr)
            sys.exit(1)
        print("reference matches model.py")
    elif "--write" in sys.argv:
        out.write_text(js + "\n")
        print(f"wrote {out}")
    else:
        print(js)


if __name__ == "__main__":
    main()
