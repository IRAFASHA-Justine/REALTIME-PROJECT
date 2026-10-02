"""
Mini Project 1.3 — Real-Time Jitter Analyzer Under Simulated System Noise

Step 1: baseline drift-free periodic loop with no disturbances.
Step 2: integrated with the jitter analyzer module.

The release loop recomputes the sleep time from the absolute next
release instant (r_0 + k*T) every iteration, so no drift accumulates.
"""

import time
import numpy as np


# ---------------------------------------------------------------------------
# Job body
# ---------------------------------------------------------------------------
def _job_body_fixed() -> float:
    """Lightweight fixed body — no variability."""
    x = 0.0
    for i in range(2000):
        x += i * 0.5
    return x


# ---------------------------------------------------------------------------
# Baseline periodic loop
# ---------------------------------------------------------------------------
def baseline_loop(T: float = 0.05, n_jobs: int = 200, D_frac: float = 0.8) -> dict:
    """
    Run a drift-free periodic loop with a fixed lightweight job body.

    Parameters
    ----------
    T       : nominal period (seconds)
    n_jobs  : number of job instances
    D_frac  : relative deadline as a fraction of T

    Returns
    -------
    dict with keys:
      T, D, n_jobs,
      ideal_release, actual_release, completion, exec_time
    All times are offsets from the reference start r_0 (seconds).
    """
    D = D_frac * T

    ideal_release  = np.empty(n_jobs, dtype=float)
    actual_release = np.empty(n_jobs, dtype=float)
    completion     = np.empty(n_jobs, dtype=float)
    exec_time      = np.empty(n_jobs, dtype=float)

    r0 = time.perf_counter()

    for k in range(n_jobs):
        ideal = r0 + k * T
        now = time.perf_counter()
        sleep_s = ideal - now
        if sleep_s > 0:
            time.sleep(sleep_s)
        rel = time.perf_counter()

        t0 = time.perf_counter()
        _job_body_fixed()
        t1 = time.perf_counter()

        ideal_release[k]  = ideal - r0
        actual_release[k] = rel   - r0
        completion[k]     = t1    - r0
        exec_time[k]      = t1 - t0

    return {
        "T": T, "D": D, "n_jobs": n_jobs,
        "ideal_release":  ideal_release,
        "actual_release": actual_release,
        "completion":     completion,
        "exec_time":      exec_time,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from analyzer import analyze, format_result

    r = baseline_loop(T=0.05, n_jobs=200)
    result = analyze(r, label="Step 2 — baseline, no disturbances")
    print(format_result(result))