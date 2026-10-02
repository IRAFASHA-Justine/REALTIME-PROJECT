"""
Mini Project 1.2 — Target functions for measurement-based WCET estimation.

Three functions of increasing structural complexity:
  1. early_exit_scan         — early-exit branch
  2. data_dependent_loop     — loop count driven by input value
  3. nested_conditional      — nested branches with unequal workload
"""

from typing import List


# ---------------------------------------------------------------------------
# Target 1 — Early-exit branch
# ---------------------------------------------------------------------------
def early_exit_scan(data: List[int], target: int) -> int:
    """
    Scan `data` looking for `target`.
    Returns the index of the first match, or -1 if not found.

    Control-flow shape: a loop with an early exit on success, plus a
    fall-through when the item is absent. Runtime is proportional to
    (index_of_match + 1) if found, or len(data) if not found.
    """
    for i, value in enumerate(data):
        if value == target:
            return i
    return -1


# ---------------------------------------------------------------------------
# Target 2 — Data-dependent loop count
# ---------------------------------------------------------------------------
def data_dependent_loop(n: int) -> int:
    """
    Sum the squares of numbers 1..n via an explicit Python loop.
    The loop count is driven directly by the input argument n.
    """
    total = 0
    for i in range(n):
        total += i * i
    return total


# ---------------------------------------------------------------------------
# Target 3 — Nested conditionals with unequal branches
# ---------------------------------------------------------------------------
def nested_conditional(x: int) -> int:
    """
    A chain of nested if/elif/else branches whose workloads are unequal.
    The deepest, most expensive branch requires x divisible by 6 and > 1000.
    """
    acc = 0

    if x < 0:
        acc += 1
        return acc

    if x < 10:
        acc += 2
    else:
        if x < 100:
            acc += 5
            for i in range(20):
                acc += i
        else:
            if x < 1000:
                acc += 10
                for i in range(200):
                    acc += i * 2
            else:
                # heaviest branch — requires x >= 1000
                acc += 50
                if x % 6 == 0:
                    for i in range(2000):
                        acc += i * 3
                    acc += x % 7
                else:
                    for i in range(500):
                        acc += i * 5
    return acc