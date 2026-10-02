"""
Mini Project 1.3 — Step 3 sweep: background CPU load intensity.
"""

import time
import numpy as np

from periodic_loop import periodic_loop
from disturbances import BackgroundLoad
from analyzer import analyze, format_result


INTENSITIES = [0.0, 0.25, 0.5, 0.75, 1.0]


if __name__ == "__main__":
    summary = []

    for intensity in INTENSITIES:
        bg = BackgroundLoad(intensity=intensity)
        bg.start()
        time.sleep(0.05)                 # let the load thread warm up

        r = periodic_loop(T=0.05, n_jobs=200)
        bg.stop()

        res = analyze(r, label=f"background intensity = {intensity:.2f}")
        print(format_result(res))
        print()

        summary.append((intensity, res))

    # Save summary arrays for later plotting (Step 7)
    np.savez(
        "sweep_background.npz",
        intensities=np.array([i for i, _ in summary]),
        rel_jitter_std =np.array([r.release_jitter_std    for _, r in summary]),
        rel_jitter_max =np.array([r.release_jitter_max    for _, r in summary]),
        cmp_jitter_std =np.array([r.completion_jitter_std for _, r in summary]),
        cmp_jitter_max =np.array([r.completion_jitter_max for _, r in summary]),
        hit_fraction   =np.array([r.hit_fraction           for _, r in summary]),
    )
    print("Saved sweep_background.npz")