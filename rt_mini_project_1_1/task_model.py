import math
import time


def job_function(workload: int) -> float:
    """
    Simulated body of a real-time job.
    Execution time varies with the workload parameter.
    """
    x = 0.0
    for i in range(workload):
        x += math.sin(i * 0.001) * math.cos(i * 0.002) + math.sqrt(i + 1.0)
    return x


if __name__ == "__main__":
    for w in [10_000, 50_000, 100_000, 200_000]:
        t0 = time.perf_counter()
        job_function(w)
        t1 = time.perf_counter()
        print(f"workload={w:>7}  time={t1 - t0:.6f} s")