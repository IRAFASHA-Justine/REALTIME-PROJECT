import threading
import time
import numpy as np

from task_model import job_function

# ---------- Background interference thread ----------
stop_flag = threading.Event()

def background_busy_loop():
    """
    Continuously burn CPU in a tight loop, imitating Section 1.6 sources
    of non-determinism: OS noise, co-running tasks competing for CPU/cache.
    """
    x = 0.0
    while not stop_flag.is_set():
        for _ in range(10_000):
            x += 1.234 * 0.567
        x = 0.0

# ---------- Periodic workload (same parameters as Step 4) ----------
T = 0.1
D = 0.8 * T
n_jobs = 120

rng = np.random.default_rng(seed=42)
workloads = rng.integers(low=10_000, high=200_000, size=n_jobs)

ideal_release = np.empty(n_jobs, dtype=float)
actual_release = np.empty(n_jobs, dtype=float)
completion = np.empty(n_jobs, dtype=float)
exec_time = np.empty(n_jobs, dtype=float)
response_time = np.empty(n_jobs, dtype=float)
release_jitter = np.empty(n_jobs, dtype=float)
completion_jitter = np.empty(n_jobs, dtype=float)
meets_deadline = np.empty(n_jobs, dtype=bool)

# ---------- Start the interference thread ----------
bg = threading.Thread(target=background_busy_loop, daemon=True)
bg.start()
time.sleep(0.05)   # let it warm up

# ---------- Periodic run under load ----------
r_0 = time.perf_counter()

for k in range(n_jobs):
    ideal = r_0 + k * T
    now = time.perf_counter()
    sleep_time = ideal - now
    if sleep_time > 0:
        time.sleep(sleep_time)
    rel = time.perf_counter()

    t0 = time.perf_counter()
    job_function(int(workloads[k]))
    t1 = time.perf_counter()
    comp = t1

    ideal_release[k]     = ideal - r_0
    actual_release[k]    = rel   - r_0
    completion[k]        = comp  - r_0
    exec_time[k]         = t1 - t0
    response_time[k]     = comp - rel
    release_jitter[k]    = rel - ideal
    completion_jitter[k] = (comp - r_0) - (ideal - r_0)
    meets_deadline[k]    = (comp - rel) <= D

# ---------- Stop the interference thread ----------
stop_flag.set()
bg.join(timeout=1.0)

# ---------- Summary ----------
hit_fraction = np.mean(meets_deadline)
print("=== Lab Task 1: periodic run WITH background interference ===")
print(f"n_jobs                 : {n_jobs}")
print(f"T (s)                  : {T:.4f}")
print(f"D (s)                  : {D:.4f}")
print(f"exec time  mean        : {np.mean(exec_time)*1000:.3f} ms")
print(f"exec time  max         : {np.max(exec_time)*1000:.3f} ms")
print(f"response   mean        : {np.mean(response_time)*1000:.3f} ms")
print(f"response   max         : {np.max(response_time)*1000:.3f} ms")
print(f"release jitter std     : {np.std(release_jitter)*1000:.3f} ms")
print(f"release jitter max|.|  : {np.max(np.abs(release_jitter))*1000:.3f} ms")
print(f"completion jitter std  : {np.std(completion_jitter)*1000:.3f} ms")
print(f"completion jitter max|.|: {np.max(np.abs(completion_jitter))*1000:.3f} ms")
print(f"deadline hit fraction  : {hit_fraction:.4f}  ({int(hit_fraction*n_jobs)}/{n_jobs})")
print(f"misses                 : {np.sum(~meets_deadline)}")

# ---------- Save for later comparison ----------
np.savez(
    "timing_data_interference.npz",
    T=T, D=D, n_jobs=n_jobs,
    ideal_release=ideal_release, actual_release=actual_release,
    completion=completion, exec_time=exec_time,
    response_time=response_time,
    release_jitter=release_jitter, completion_jitter=completion_jitter,
    meets_deadline=meets_deadline,
)
print("\nSaved timing_data_interference.npz")