"""
Mini Project 1.1 — Lab Task 4
Vary period T, keep D = 0.8 * T fixed.
Study how release jitter, both in ms and as a fraction of T, behaves.
"""

import time
import numpy as np
import matplotlib.pyplot as plt

from task_model import job_function


n_jobs   = 50
T_values = [0.05, 0.10, 0.15, 0.20]
D_frac   = 0.8

rng = np.random.default_rng(seed=7)
workloads = rng.integers(low=10_000, high=200_000, size=n_jobs)

results = {}

for T_i in T_values:
    D_i = D_frac * T_i
    rel_jit = np.empty(n_jobs, dtype=float)
    R_arr   = np.empty(n_jobs, dtype=float)
    hits    = np.empty(n_jobs, dtype=bool)

    r0 = time.perf_counter()
    for k in range(n_jobs):
        ideal = r0 + k * T_i
        now = time.perf_counter()
        s = ideal - now
        if s > 0:
            time.sleep(s)
        rel = time.perf_counter()

        t0 = time.perf_counter()
        job_function(int(workloads[k]))
        t1 = time.perf_counter()

        rel_jit[k] = rel - ideal
        R_arr[k]   = t1 - rel
        hits[k]    = (t1 - rel) <= D_i

    results[T_i] = dict(rel_jit=rel_jit, R=R_arr, hits=hits)
    rj_ms    = rel_jit * 1000.0
    frac_pc  = np.abs(rel_jit) / T_i * 100.0
    print(f"T = {T_i*1000:6.1f} ms | D = {D_i*1000:6.1f} ms | "
          f"jitter std {rj_ms.std():6.3f} ms | max {np.abs(rj_ms).max():6.3f} ms | "
          f"as %T std {frac_pc.std():5.2f}% max {frac_pc.max():5.2f}% | "
          f"hit {hits.mean():.3f}")

# ---- Plot 1: jitter in ms ----
fig, ax = plt.subplots(figsize=(8, 4.5))
for T_i in T_values:
    ax.plot(np.arange(n_jobs), results[T_i]["rel_jit"] * 1000.0,
            ".-", label=f"T = {T_i*1000:.0f} ms")
ax.axhline(0, color="gray", linewidth=0.8)
ax.set_xlabel("job index")
ax.set_ylabel("Release jitter [ms]")
ax.set_title("Release jitter for various periods (D = 0.8 T)")
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("lt4_jitter_vs_T.png", dpi=130)
plt.close(fig)

# ---- Plot 2: jitter as % of T ----
fig, ax = plt.subplots(figsize=(8, 4.5))
for T_i in T_values:
    ax.plot(np.arange(n_jobs), results[T_i]["rel_jit"] / T_i * 100.0,
            ".-", label=f"T = {T_i*1000:.0f} ms")
ax.axhline(0, color="gray", linewidth=0.8)
ax.set_xlabel("job index")
ax.set_ylabel("Release jitter as % of T")
ax.set_title("Release jitter as a fraction of period")
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("lt4_jitter_fraction.png", dpi=130)
plt.close(fig)

print("\nSaved lt4_jitter_vs_T.png and lt4_jitter_fraction.png")