"""
Mini Project 1.1 — Lab Task 2
Adversarial inputs vs ordinary inputs for WCET estimation.

Goal: show that a measured maximum from random inputs is NOT a sound WCET,
because the true worst-case path may not have been exercised (Section 1.7).
"""

import time
import numpy as np

from task_model import job_function


def measure(workloads: np.ndarray) -> np.ndarray:
    """Run job_function once per workload and return per-call durations."""
    n = len(workloads)
    d = np.empty(n, dtype=float)
    for k in range(n):
        t0 = time.perf_counter()
        job_function(int(workloads[k]))
        t1 = time.perf_counter()
        d[k] = t1 - t0
    return d


def stats(name: str, arr: np.ndarray) -> None:
    print(f"{name:>12} | "
          f"mean {np.mean(arr)*1000:8.3f} ms | "
          f"p95 {np.percentile(arr, 95)*1000:8.3f} ms | "
          f"max {np.max(arr)*1000:8.3f} ms")


if __name__ == "__main__":
    n = 200
    rng = np.random.default_rng(seed=42)

    # (a) Ordinary inputs: random workload, same distribution as Step 2
    ordinary = rng.integers(low=10_000, high=200_000, size=n)

    # (b) Adversarial inputs: every call uses the largest workload
    adversarial = np.full(n, 200_000)

    # (c) Heavy-tail inputs: an even larger workload, beyond the ordinary range
    heavy = np.full(n, 400_000)

    ord_t   = measure(ordinary)
    adv_t   = measure(adversarial)
    heavy_t = measure(heavy)

    print("=== Lab Task 2: ordinary vs adversarial inputs ===")
    stats("Ordinary",    ord_t)
    stats("Adversarial", adv_t)
    stats("Heavy tail",  heavy_t)

    # Save for the report / plots
    np.savez(
        "lt2_data.npz",
        ordinary=ord_t,
        adversarial=adv_t,
        heavy=heavy_t,
    )
    print("\nSaved lt2_data.npz")