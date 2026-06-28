"""
Cybeersym — bullwhip instrument. Measurement is a function, nothing more.

Two complementary views of the same run:

1. PER-STAGE ratio = Var(orders a tier PLACES) / Var(demand it RECEIVES).
   The local amplification each stage adds over the one below it.

2. CUMULATIVE ratio = Var(orders a tier PLACES) / Var(TRUE consumer demand).
   The compounding signature the killer experiment turns on: under local info
   this climbs ~ r, r^2, r^3 up the chain; under shared info it stays ~ r flat,
   because every stage forecasts off the same true demand and the distortion
   never gets re-distorted upstream.

`np.var` is the Var/sigma^2 of the papers. The warmup slice discards the startup
transient (and the forecast's cold start) before measuring — characterise the
steady mechanism, not the buffers filling.
"""
import numpy as np


def bullwhip_ratio(orders_placed, demand_received, warmup):
    """Var(orders out) / Var(demand in), post-warmup."""
    o = np.asarray(orders_placed)[warmup:]
    d = np.asarray(demand_received)[warmup:]
    dv = np.var(d)
    return float("nan") if dv == 0 else float(np.var(o) / dv)


def chen_single_stage(L, p):
    """Chen, Drezner, Ryan & Simchi-Levi (2000), Management Science 46(3):436-443.
    Single-stage Var(orders)/Var(demand) for i.i.d. demand, MA(p) forecast, lead
    time L. Rises with L, falls with p, -> 1 as p -> infinity. A rigorous analytic
    target (a lower bound for the order-up-to-with-estimated-variance case)."""
    return 1.0 + 2.0 * L / p + 2.0 * L ** 2 / p ** 2


def chain_report(chain):
    """Per-tier and cumulative ratios + the compounded whole-chain figure."""
    p = chain.p
    per_stage = [bullwhip_ratio(chain.orders_placed[i], chain.demand_received[i], p.warmup)
                 for i in range(p.n_tiers)]
    true_demand = chain.demand
    cumulative = [bullwhip_ratio(chain.orders_placed[i], true_demand, p.warmup)
                  for i in range(p.n_tiers)]
    return {"mode": chain.mode, "forecast": chain.forecast,
            "per_stage": per_stage, "cumulative": cumulative,
            "chain_total": float(np.prod(per_stage)),
            "max_residual": chain.max_residual}


def format_table(reports, key, tier_names=("retailer", "wholesaler", "manufacturer")):
    """Fixed-width table of `key` (e.g. 'per_stage' or 'cumulative') across modes."""
    lines = []
    head = f"{'mode':<12}" + "".join(f"{n:>14}" for n in tier_names)
    if key == "per_stage":
        head += f"{'CHAIN(prod)':>14}"
    lines.append(head)
    lines.append("-" * len(head))
    for r in reports:
        row = f"{r['mode']:<12}" + "".join(f"{x:>14.3f}" for x in r[key])
        if key == "per_stage":
            row += f"{r['chain_total']:>14.3f}"
        lines.append(row)
    return "\n".join(lines)
