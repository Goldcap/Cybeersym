#!/usr/bin/env python3
"""Generate (or --check) the orthodox-IRF reference baked into the viz.

The viz's two orthodox beats (RBC, NK) plot REAL impulse responses from the numpy DSGE toy
models in `src/orthodox/` (rbc.py, nk.py) — not hand-drawn shapes. Unlike the Goodwin–Keen
model (ported to JS and computed live in the page), these small DSGE solves are not ported;
instead this script bakes their IRFs inline into `viz/index.html` between the
`// ==ORTHO-IRF-START==` / `// ==ORTHO-IRF-END==` markers, and the CI reference-drift job runs
`--check` to guarantee the baked numbers still match the numpy engines.

    python3 viz/gen_ortho.py            # print the JS block to stdout
    python3 viz/gen_ortho.py --write    # rewrite the marker block in viz/index.html
    python3 viz/gen_ortho.py --check    # regenerate and diff against the baked block (drift guard)

Run from the repo root. Deterministic. numpy only. The baked series are RAW model log-deviations
(what CI pins); the viz applies a DISCLOSED shape-normalisation for on-screen visibility
(magnitudes are not comparable across models — topological illustration, per the project method).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from orthodox.rbc import RBCParams, irf as rbc_irf          # noqa: E402
from orthodox.nk import NKParams, irf as nk_irf             # noqa: E402

HTML = ROOT / "viz" / "index.html"
START = "// ==ORTHO-IRF-START=="
END = "// ==ORTHO-IRF-END=="
QSTEP = 2          # sample every 2 quarters
QMAX = 120         # 120 quarters = 30 years (orthodox recovery is fast; this shows it fully)
R = 6              # decimals


def _samp(a):
    return [round(float(a[q]), R) for q in range(0, QMAX, QSTEP)]


def build():
    yrs = [round(q / 4.0, 4) for q in range(0, QMAX, QSTEP)]   # quarters → years

    rp = RBCParams()
    r = rbc_irf(rp, shock=-0.01, T=400)
    rbc = {"t": yrs, "emp": _samp(r["n"]), "out": _samp(r["y"]),
           "wage": _samp(r["y"] - r["n"])}                     # real wage ŵ = ŷ − n̂ (procyclical)

    npar = NKParams()
    sd = nk_irf(npar, shock=-0.01, kind="demand", T=400)
    nk = {"t": yrs, "emp": _samp(sd["x"]), "infl": _samp(sd["pi"]), "rate": _samp(sd["i"])}
    ss = nk_irf(npar, shock=-0.01, kind="supply", T=400)   # cost-push: output↓ inflation↑ (tradeoff)
    nk_supply = {"t": yrs, "emp": _samp(ss["x"]), "infl": _samp(ss["pi"]), "rate": _samp(ss["i"])}

    return {"rbc": rbc, "nk": nk, "nk_supply": nk_supply}


def block():
    data = build()
    return f"{START}\nconst ORTHO_IRF={json.dumps(data, separators=(',', ':'))};\n{END}"


def main():
    blk = block()
    if "--check" in sys.argv:
        txt = HTML.read_text()
        m = re.search(re.escape(START) + r"(.*?)" + re.escape(END), txt, re.S)
        if not m:
            print("ORTHO-IRF markers not found in viz/index.html", file=sys.stderr); sys.exit(1)
        baked = re.search(r"const ORTHO_IRF=(\{.*\});", m.group(0), re.S)
        cur = json.loads(baked.group(1))
        fresh = build()
        # numeric compare within tol (JSON round-trips exactly here, but be robust)
        def close(a, b, tol=1e-6):
            if isinstance(a, list):
                return len(a) == len(b) and all(close(x, y, tol) for x, y in zip(a, b))
            if isinstance(a, dict):
                return a.keys() == b.keys() and all(close(a[k], b[k], tol) for k in a)
            return abs(a - b) <= tol
        if not close(cur, fresh):
            print("ORTHO-IRF DRIFT: viz/index.html baked orthodox IRFs do not match src/orthodox/.\n"
                  "Regenerate with `python3 viz/gen_ortho.py --write` and review.", file=sys.stderr)
            sys.exit(1)
        print("orthodox IRFs match src/orthodox/")
    elif "--write" in sys.argv:
        txt = HTML.read_text()
        new = re.sub(re.escape(START) + r".*?" + re.escape(END), blk, txt, flags=re.S)
        if new == txt and START not in txt:
            print("markers not present; add them to viz/index.html first", file=sys.stderr); sys.exit(1)
        HTML.write_text(new)
        print(f"wrote ORTHO-IRF block into {HTML}")
    else:
        print(blk)


if __name__ == "__main__":
    main()
