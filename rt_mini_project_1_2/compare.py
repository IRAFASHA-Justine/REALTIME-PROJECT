"""
Mini Project 1.2 — Random vs adversarial comparison.

Runs each target under both strategies, prints a summary, and stores
the raw durations in numpy arrays for later plotting (Step 6) and
the comparison table (Step 7).
"""

import numpy as np

from harness import measure_function
from stats import summarise
from strategies import (
    random_inputs_early_exit,  adversarial_inputs_early_exit,
    random_inputs_data_loop,   adversarial_inputs_data_loop,
    random_inputs_nested,      adversarial_inputs_nested,
)
from targets import early_exit_scan, data_dependent_loop, nested_conditional


N       = 200   # samples per strategy per function
REPEAT  = 1
WARMUP  = 20

TARGETS = [
    ("early_exit_scan",
        early_exit_scan,
        random_inputs_early_exit,  adversarial_inputs_early_exit),
    ("data_dependent_loop",
        data_dependent_loop,
        random_inputs_data_loop,   adversarial_inputs_data_loop),
    ("nested_conditional",
        nested_conditional,
        random_inputs_nested,      adversarial_inputs_nested),
]


if __name__ == "__main__":
    print(f"=== Random vs adversarial comparison (N = {N} per strategy) ===")
    print()

    results = {}

    for name, func, rand_strat, adv_strat in TARGETS:
        rand_inputs = rand_strat(N, seed=42)
        adv_inputs  = adv_strat(N, seed=42)

        d_rand, _ = measure_function(func, rand_inputs, repeat=REPEAT, warmup=WARMUP)
        d_adv,  _ = measure_function(func, adv_inputs,  repeat=REPEAT, warmup=WARMUP)

        s_rand = summarise(d_rand)
        s_adv  = summarise(d_adv)

        adv_larger = s_adv.maximum > s_rand.maximum
        ratio = (s_adv.maximum / s_rand.maximum) if s_rand.maximum > 0 else float("inf")

        print(f"--- {name} ---")
        print(f"  random       max: {s_rand.maximum*1e6:8.3f} us   p99: {s_rand.p99*1e6:8.3f} us")
        print(f"  adversarial  max: {s_adv.maximum*1e6:8.3f} us   p99: {s_adv.p99*1e6:8.3f} us")
        print(f"  adversarial produced the larger max?  {'YES' if adv_larger else 'no'}")
        print(f"  ratio adv / rand (max): {ratio:.3f}")
        print()

        results[name] = dict(
            d_rand=d_rand, d_adv=d_adv,
            s_rand=s_rand, s_adv=s_adv,
        )

    # Save arrays for Step 6 (histograms) and Step 7 (table)
    save_dict = {}
    for name, r in results.items():
        save_dict[f"{name}__rand"] = r["d_rand"]
        save_dict[f"{name}__adv"]  = r["d_adv"]
    np.savez("strategy_data.npz", **save_dict)
    print("Saved strategy_data.npz")