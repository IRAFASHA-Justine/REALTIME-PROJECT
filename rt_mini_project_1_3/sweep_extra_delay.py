"""
Mini Project 1.3 — Step 4 sweep: Bernoulli random extra delay.

Sweeps two dimensions:
  - probability p in {0.05, 0.10, 0.20, 0.50}
  - magnitude  d in {1 ms, 5 ms, 10 ms, 20 ms}
as separate one-dimensional sweeps (probability sweep at fixed magnitude,
magnitude sweep at fixed probability) so the plots stay readable.
"""

import numpy as np

from periodic_loop import periodic_loop
from disturbances import ExtraDelay
from analyzer import analyze, format_result


PROB_VALUES = [0.05, 0.10, 0.20, 0.50]
MAG_FIXED_FOR_PROB = 0.005       # 5 ms

MAG_VALUES = [0.001, 0.005, 0.010, 0.020]   # 1, 5, 10, 20 ms
PROB_FIXED_FOR_MAG = 0.10


if __name__ == "__main__":
    # -------------------------------------------------------------------
    # Sweep 1 — vary probability at fixed magnitude
    # -------------------------------------------------------------------
    print("=== Sweep 4a: probability sweep (magnitude = 5 ms) ===")
    print()

    prob_results = []
    for p in PROB_VALUES:
        delay = ExtraDelay(probability=p, magnitude=MAG_FIXED_FOR_PROB, seed=42)
        r = periodic_loop(T=0.05, n_jobs=200, pre_job_hook=delay)
        res = analyze(r, label=f"p = {p:.2f}, d = {MAG_FIXED_FOR_PROB*1000:.0f} ms")
        print(format_result(res))
        print(f"  delay trigger rate      : {delay.hits}/{delay.calls} "
              f"({delay.hits / max(delay.calls, 1):.3f})")
        print()
        prob_results.append((p, res, delay.hits / max(delay.calls, 1)))

    np.savez(
        "sweep_prob.npz",
        probs         =np.array([p for p, _, _ in prob_results]),
        trigger_rate  =np.array([t for _, _, t in prob_results]),
        rel_jitter_std=np.array([r.release_jitter_std for _, r, _ in prob_results]),
        rel_jitter_max=np.array([r.release_jitter_max for _, r, _ in prob_results]),
        cmp_jitter_std=np.array([r.completion_jitter_std for _, r, _ in prob_results]),
        cmp_jitter_max=np.array([r.completion_jitter_max for _, r, _ in prob_results]),
        hit_fraction  =np.array([r.hit_fraction for _, r, _ in prob_results]),
    )
    print("Saved sweep_prob.npz\n")

    # -------------------------------------------------------------------
    # Sweep 2 — vary magnitude at fixed probability
    # -------------------------------------------------------------------
    print("=== Sweep 4b: magnitude sweep (probability = 0.10) ===")
    print()

    mag_results = []
    for d in MAG_VALUES:
        delay = ExtraDelay(probability=PROB_FIXED_FOR_MAG, magnitude=d, seed=42)
        r = periodic_loop(T=0.05, n_jobs=200, pre_job_hook=delay)
        res = analyze(r, label=f"p = {PROB_FIXED_FOR_MAG:.2f}, d = {d*1000:.0f} ms")
        print(format_result(res))
        print()
        mag_results.append((d, res))

    np.savez(
        "sweep_mag.npz",
        mags          =np.array([d for d, _ in mag_results]),
        rel_jitter_std=np.array([r.release_jitter_std for _, r in mag_results]),
        rel_jitter_max=np.array([r.release_jitter_max for _, r in mag_results]),
        cmp_jitter_std=np.array([r.completion_jitter_std for _, r in mag_results]),
        cmp_jitter_max=np.array([r.completion_jitter_max for _, r in mag_results]),
        hit_fraction  =np.array([r.hit_fraction for _, r in mag_results]),
    )
    print("Saved sweep_mag.npz")