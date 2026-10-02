"""
Mini Project 1.3 — Step 5 sweep: per-job execution-time variability.
"""

import numpy as np

from periodic_loop import periodic_loop
from disturbances import ExecTimeVariability
from analyzer import analyze, format_result


# ---------------------------------------------------------------------------
# Sweep 5a — Normal distribution, vary spread
# ---------------------------------------------------------------------------
NORMAL_SPREADS = [0, 1000, 3000, 6000, 10000]     # mean fixed at 5000

if __name__ == "__main__":
    print("=== Sweep 5a: normal distribution, spread sweep (mean = 5000) ===")
    print()

    normal_results = []
    for spread in NORMAL_SPREADS:
        body = ExecTimeVariability(
            distribution="normal", mean=5000, spread=spread, seed=42
        )
        r = periodic_loop(T=0.05, n_jobs=200, job_body=body)
        res = analyze(r, label=f"normal spread = {spread}")
        print(format_result(res))
        print()
        normal_results.append((spread, res))

    np.savez(
        "sweep_exec_normal.npz",
        spreads       =np.array([s for s, _ in normal_results]),
        exec_mean     =np.array([r.response_time_mean for _, r in normal_results]),
        exec_max      =np.array([r.response_time_max for _, r in normal_results]),
        rel_jitter_std=np.array([r.release_jitter_std for _, r in normal_results]),
        cmp_jitter_std=np.array([r.completion_jitter_std for _, r in normal_results]),
        cmp_jitter_max=np.array([r.completion_jitter_max for _, r in normal_results]),
        hit_fraction  =np.array([r.hit_fraction for _, r in normal_results]),
    )
    print("Saved sweep_exec_normal.npz\n")

    # -----------------------------------------------------------------------
    # Sweep 5b — Heavy-tailed distribution
    # -----------------------------------------------------------------------
    print("=== Sweep 5b: heavy-tailed distribution (various means) ===")
    print()

    means = [2000, 4000, 6000, 8000]
    heavy_results = []
    for m in means:
        body = ExecTimeVariability(
            distribution="heavy_tail", mean=m, spread=0, seed=42
        )
        r = periodic_loop(T=0.05, n_jobs=200, job_body=body)
        res = analyze(r, label=f"heavy_tail mean = {m}")
        print(format_result(res))
        print()
        heavy_results.append((m, res))

    np.savez(
        "sweep_exec_heavy.npz",
        means         =np.array([m for m, _ in heavy_results]),
        exec_mean     =np.array([r.response_time_mean for _, r in heavy_results]),
        exec_max      =np.array([r.response_time_max for _, r in heavy_results]),
        rel_jitter_std=np.array([r.release_jitter_std for _, r in heavy_results]),
        cmp_jitter_std=np.array([r.completion_jitter_std for _, r in heavy_results]),
        cmp_jitter_max=np.array([r.completion_jitter_max for _, r in heavy_results]),
        hit_fraction  =np.array([r.hit_fraction for _, r in heavy_results]),
    )
    print("Saved sweep_exec_heavy.npz")