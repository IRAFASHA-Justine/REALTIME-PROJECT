"""
Mini Project 1.3 — Disturbance mechanisms.

Step 3: Background CPU-load thread with adjustable duty cycle.
Step 4: Bernoulli random extra delay (interrupt/DMA-stall stand-in).
Step 5: Per-job execution-time variability (cache/pipeline stand-in).
"""

import threading
import time
import random
import numpy as np


# ---------------------------------------------------------------------------
# Disturbance 1 — Background CPU load with adjustable duty cycle
# ---------------------------------------------------------------------------
class BackgroundLoad:
    def __init__(self, intensity: float, window: float = 0.01):
        if not 0.0 <= intensity <= 1.0:
            raise ValueError("intensity must be in [0, 1]")
        self.intensity = intensity
        self.window = window
        self._stop = threading.Event()
        self._thread = None

    def start(self) -> None:
        if self.intensity <= 0.0:
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=1.0)
            self._thread = None

    def _run(self) -> None:
        burn_time = self.window * self.intensity
        rest_time = self.window * (1.0 - self.intensity)
        while not self._stop.is_set():
            deadline_burn = time.perf_counter() + burn_time
            x = 0.0
            while time.perf_counter() < deadline_burn and not self._stop.is_set():
                x += 1.234 * 0.567
            if rest_time > 0.0:
                time.sleep(rest_time)


# ---------------------------------------------------------------------------
# Disturbance 2 — Occasional random extra delay
# ---------------------------------------------------------------------------
class ExtraDelay:
    def __init__(self, probability: float, magnitude: float, seed: int = 0):
        if not 0.0 <= probability <= 1.0:
            raise ValueError("probability must be in [0, 1]")
        if magnitude < 0.0:
            raise ValueError("magnitude must be >= 0")
        self.p = probability
        self.magnitude = magnitude
        self._rng = random.Random(seed)
        self.hits = 0
        self.calls = 0

    def __call__(self, k: int) -> None:
        self.calls += 1
        if self._rng.random() < self.p:
            self.hits += 1
            time.sleep(self.magnitude)


# ---------------------------------------------------------------------------
# Disturbance 3 — Per-job execution-time variability
# ---------------------------------------------------------------------------
class ExecTimeVariability:
    """
    A job body whose workload size is drawn from a configurable
    distribution. Stands in for cache effects, pipeline hazards, and
    data-dependent control flow.
    """

    def __init__(
        self,
        distribution: str = "normal",
        mean: int = 5000,
        spread: int = 2000,
        seed: int = 0,
    ):
        if distribution not in ("normal", "heavy_tail"):
            raise ValueError("distribution must be 'normal' or 'heavy_tail'")
        self.distribution = distribution
        self.mean = mean
        self.spread = spread
        self._rng = np.random.default_rng(seed)

    def sample(self) -> int:
        if self.distribution == "normal":
            n = int(self._rng.normal(self.mean, self.spread))
            return max(100, n)
        else:  # heavy_tail
            alpha = 1.5
            n = int((self._rng.pareto(alpha) + 1.0) * self.mean / 3)
            return max(100, n)

    def __call__(self) -> float:
        n = self.sample()
        x = 0.0
        for i in range(n):
            x += i * 0.5
        return x