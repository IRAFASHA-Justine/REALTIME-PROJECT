"""
Mini Project 1.3 — Jitter / deadline analyzer.

Takes the result dict produced by a periodic loop and computes:
  - release jitter  = actual_release - ideal_release
  - completion jitter = completion - ideal_release
  - response time R = completion - actual_release
  - hit fraction, miss count
  - std and max-absolute for each jitter type

Returns a structured record, so sweeps can collect them into a table.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class JitterResult:
    label: str
    n_jobs: int
    T: float
    D: float

    release_jitter_std: float
    release_jitter_max: float
    release_jitter_mean: float

    completion_jitter_std: float
    completion_jitter_max: float
    completion_jitter_mean: float

    response_time_mean: float
    response_time_max: float

    hit_fraction: float
    miss_count: int

    # Per-job arrays, kept for plots and further analysis
    release_jitter:    np.ndarray
    completion_jitter: np.ndarray
    response_time:     np.ndarray
    meets_deadline:    np.ndarray


def analyze(result: dict, label: str = "") -> JitterResult:
    """Compute JitterResult from a periodic-loop result dict."""
    ideal  = result["ideal_release"]
    rel    = result["actual_release"]
    comp   = result["completion"]
    D      = result["D"]
    T      = result["T"]
    n      = result["n_jobs"]

    rel_j  = rel  - ideal
    comp_j = comp - ideal
    R      = comp - rel
    hits   = R <= D

    return JitterResult(
        label=label,
        n_jobs=n, T=T, D=D,

        release_jitter_std=float(rel_j.std()),
        release_jitter_max=float(np.abs(rel_j).max()),
        release_jitter_mean=float(rel_j.mean()),

        completion_jitter_std=float(comp_j.std()),
        completion_jitter_max=float(np.abs(comp_j).max()),
        completion_jitter_mean=float(comp_j.mean()),

        response_time_mean=float(R.mean()),
        response_time_max=float(R.max()),

        hit_fraction=float(hits.mean()),
        miss_count=int((~hits).sum()),

        release_jitter=rel_j,
        completion_jitter=comp_j,
        response_time=R,
        meets_deadline=hits,
    )


def format_result(r: JitterResult) -> str:
    """Multi-line human-readable summary of a JitterResult."""
    return (
        f"--- {r.label or '(unlabeled)'} ---\n"
        f"  n_jobs                 : {r.n_jobs}\n"
        f"  T                      : {r.T*1000:8.3f} ms\n"
        f"  D                      : {r.D*1000:8.3f} ms\n"
        f"  release jitter std     : {r.release_jitter_std*1000:8.3f} ms\n"
        f"  release jitter max|.|  : {r.release_jitter_max*1000:8.3f} ms\n"
        f"  completion jitter std  : {r.completion_jitter_std*1000:8.3f} ms\n"
        f"  completion jitter max|.|: {r.completion_jitter_max*1000:8.3f} ms\n"
        f"  response time mean     : {r.response_time_mean*1000:8.3f} ms\n"
        f"  response time max      : {r.response_time_max*1000:8.3f} ms\n"
        f"  hit fraction           : {r.hit_fraction:8.4f}  "
        f"({r.n_jobs - r.miss_count}/{r.n_jobs})\n"
        f"  misses                 : {r.miss_count}"
    )