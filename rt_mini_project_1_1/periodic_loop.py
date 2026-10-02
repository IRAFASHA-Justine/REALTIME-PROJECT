import time
import numpy as np

from task_model import job_function

# ---------- Parameters ----------
T = 0.1                 # nominal period, seconds
D = 0.8 * T             # relative deadline, seconds
n_jobs = 10             # quick preview only; step 4 will do 100+

rng = np.random.default_rng(seed=42)
workloads = rng.integers(low=10_000, high=200_000, size=n_jobs)

# ---------- Periodic release loop ----------
r_0 = time.perf_counter()      # reference start instant

print(f"T = {T:.4f} s,  D = {D:.4f} s,  n_jobs = {n_jobs}")
print(f"{'k':>3} | {'ideal_rel':>11} | {'actual_rel':>11} | "
      f"{'rel_jit(ms)':>12} | {'exec(ms)':>10} | {'R(ms)':>8} | {'meetsD?':>7}")
print("-" * 90)

for k in range(n_jobs):
    # Ideal release instant for job k (recomputed from r_0 each time -> no drift)
    ideal_release = r_0 + k * T

    # Sleep until the absolute target instant
    now = time.perf_counter()
    sleep_time = ideal_release - now
    if sleep_time > 0:
        time.sleep(sleep_time)

    actual_release = time.perf_counter()

    # --- job body ---
    t0 = time.perf_counter()
    job_function(int(workloads[k]))
    t1 = time.perf_counter()
    # --- end job body ---

    completion = t1
    R = completion - actual_release
    rel_jitter_ms = (actual_release - ideal_release) * 1000.0
    exec_ms = (t1 - t0) * 1000.0
    R_ms = R * 1000.0
    meets = "YES" if R <= D else "NO"

    print(f"{k:>3} | {ideal_release - r_0:>11.6f} | "
          f"{actual_release - r_0:>11.6f} | {rel_jitter_ms:>12.3f} | "
          f"{exec_ms:>10.3f} | {R_ms:>8.3f} | {meets:>7}")