"""
Mini Project 1.2 — Safety margin calculation.

Reference: Section 1.7 of the unit notes.

Section 1.7 states:
  - measurement-based WCET is unsafe (no guarantee the true worst case
    was exercised);
  - therefore practitioners add a safety margin;
  - a common industrial convention is to budget only 60-70% of processor
    time, leaving 30-40% headroom.

This module computes the margined recommended WCET-for-scheduling value
from a measured maximum.
"""

from dataclasses import dataclass


@dataclass
class MarginedWCET:
    measured_max: float          # seconds
    margin_fraction: float       # e.g. 0.40 for 40%
    margined: float              # seconds
    utilisation_target: float    # e.g. 0.65 (65%)


def compute_margined_wcet(
    measured_max: float,
    margin_fraction: float = 0.40,
) -> MarginedWCET:
    """
    Apply a safety margin to a measured maximum.

    Parameters
    ----------
    measured_max    : measured maximum execution time (seconds)
    margin_fraction : safety margin as a fraction (0.40 = +40%).
                      The 40% default corresponds to the lower end of the
                      60-70% utilisation budget: using 60% of the CPU
                      capacity is equivalent to +66.7% on top of the
                      estimate; using 70% is +42.9%. 0.40 is a common
                      conservative middle.

    Returns
    -------
    MarginedWCET dataclass.
    """
    if measured_max < 0:
        raise ValueError("measured_max must be >= 0")
    if margin_fraction < 0:
        raise ValueError("margin_fraction must be >= 0")

    margined = measured_max * (1.0 + margin_fraction)
    # utilisation_target: how much CPU we intend to consume if this task
    # had the whole processor. 1/(1+margin).
    utilisation_target = 1.0 / (1.0 + margin_fraction)

    return MarginedWCET(
        measured_max=measured_max,
        margin_fraction=margin_fraction,
        margined=margined,
        utilisation_target=utilisation_target,
    )


def format_margin(name: str, m: MarginedWCET) -> str:
    return (
        f"--- {name} ---\n"
        f"  measured max           : {m.measured_max*1e6:10.3f} us\n"
        f"  margin fraction        : {m.margin_fraction*100:10.1f} %\n"
        f"  recommended WCET       : {m.margined*1e6:10.3f} us\n"
        f"  implied CPU utilisation: {m.utilisation_target*100:10.1f} %"
    )