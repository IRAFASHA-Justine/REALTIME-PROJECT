"""
Mini Project 1.2 — Statistics module.

Computes the standard summary statistics the brief requires:
  mean, std, min, max, p90, p95, p99
plus a flag for when the observed maximum lies unusually far above p99.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class TimingStats:
    n: int
    mean: float
    std: float
    minimum: float
    maximum: float
    p90: float
    p95: float
    p99: float
    max_over_p99_ratio: float

    @property
    def outlier_flag(self) -> bool:
        """
        Flag when the maximum is more than 1.5x the 99th percentile.
        A large ratio is a hint that a rare path was hit that the bulk
        of samples missed — worth investigating manually (Section 1.7).
        """
        return self.max_over_p99_ratio > 1.5


def summarise(durations: np.ndarray) -> TimingStats:
    """Compute TimingStats from a raw array of duration samples (seconds)."""
    if durations.size == 0:
        raise ValueError("empty sample array")

    p90 = float(np.percentile(durations, 90))
    p95 = float(np.percentile(durations, 95))
    p99 = float(np.percentile(durations, 99))
    mx  = float(np.max(durations))

    ratio = (mx / p99) if p99 > 0 else float("inf")

    return TimingStats(
        n=int(durations.size),
        mean=float(np.mean(durations)),
        std=float(np.std(durations)),
        minimum=float(np.min(durations)),
        maximum=mx,
        p90=p90,
        p95=p95,
        p99=p99,
        max_over_p99_ratio=ratio,
    )


def format_stats(name: str, s: TimingStats) -> str:
    """Human-readable multi-line summary of a TimingStats record."""
    lines = [
        f"--- {name} ---",
        f"  n            : {s.n}",
        f"  mean         : {s.mean*1e6:10.3f} us",
        f"  std          : {s.std*1e6:10.3f} us",
        f"  min          : {s.minimum*1e6:10.3f} us",
        f"  max          : {s.maximum*1e6:10.3f} us",
        f"  p90          : {s.p90*1e6:10.3f} us",
        f"  p95          : {s.p95*1e6:10.3f} us",
        f"  p99          : {s.p99*1e6:10.3f} us",
        f"  max / p99    : {s.max_over_p99_ratio:10.3f}",
        f"  outlier flag : {'YES' if s.outlier_flag else 'no'}",
    ]
    return "\n".join(lines)