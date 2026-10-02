import time
import numpy as np

from task_model import job_function


def measure_execution_times(n_calls: int = 200, seed: int = 42) -> np.ndarray:
    """
    Run job_function n_calls times with varying workloads,
    measure each execution time with perf_counter,
    and return the durations as a NumPy array.
    """
    rng = np.random.default_rng(seed)

    # Workloads chosen so some calls are short, some long.
    # This imitates the execution-time variability discussed in Section 1.7.
    workloads = rng.integers(low=10_000, high=200_000, size=n_calls)

    durations = np.empty(n_calls, dtype=float)

    for k in range(n_calls):
        w = int(workloads[k])
        t0 = time.perf_counter()
        job_function(w)
        t1 = time.perf_counter()
        durations[k] = t1 - t0

    return durations


if __name__ == "__main__":
    durations = measure_execution_times(n_calls=200)

    mean_t = np.mean(durations)
    std_t = np.std(durations)
    max_t = np.max(durations)
    p95_t = np.percentile(durations, 95)

    print("=== Execution time statistics (200 calls) ===")
    print(f"mean        : {mean_t:.6f} s")
    print(f"std dev     : {std_t:.6f} s")
    print(f"maximum     : {max_t:.6f} s   <-- measured WCET estimate (not proven)")
    print(f"95th pct    : {p95_t:.6f} s")
    print(f"min         : {np.min(durations):.6f} s")
    print(f"number      : {len(durations)}")

    # Show the 5 slowest calls
    idx_sorted = np.argsort(durations)[::-1]
    print("\n5 slowest calls (index, time):")
    for i in idx_sorted[:5]:
        print(f"  call {i:>3}  {durations[i]:.6f} s")