"""
Mini Project 1.3 — Generalized drift-free periodic loop.

This is the canonical loop used from Step 3 onwards. Compared to the
baseline, it exposes two hooks so we can plug in disturbances later:

    job_body        : callable producing the work of a single job
    pre_job_hook    : callable invoked after release but before the job
                      body — used to inject the random extra delay

The loop recomputes the sleep target every iteration (r_0 + k*T), so
no drift accumulates.
"""

import time
import numpy as np


def default_job_body() -> float:
    """Lightweight fixed body — no variability."""
    x = 0.0
    for i in range(2000):
        x += i * 0.5
    return x


def periodic_loop(
    T: float = 0.05,
    n_jobs: int = 200,
    D_frac: float = 0.8,
    job_body=None,
    pre_job_hook=None,
) -> dict:
    """
    Run a drift-free periodic loop.

    Parameters
    ----------
    T           : nominal period (s)
    n_jobs      : number of job instances
    D_frac      : relative deadline as a fraction of T
    job_body    : callable with zero arguments, or None for the default
    pre_job_hook: callable(k) invoked after release, before job body; or None

    Returns
    -------
    dict with keys: T, D, n_jobs, ideal_release, actual_release,
                    completion, exec_time (all times are offsets from r_0).
    """
    if job_body is None:
        job_body = default_job_body

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

        # --- optional disturbance hook (random extra delay) ---
        if pre_job_hook is not None:
            pre_job_hook(k)

        t0 = time.perf_counter()
        job_body()
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