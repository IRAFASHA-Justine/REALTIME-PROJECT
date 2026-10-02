"""
Mini Project 1.2 — Input-generation strategies.

For each target we provide two strategies:
  - random / representative
  - adversarial, hand-crafted to stress the longest path
"""

import random
from typing import List


# ---------------------------------------------------------------------------
# Target 1 — early_exit_scan(data, target)
# ---------------------------------------------------------------------------
def random_inputs_early_exit(n: int, seed: int = 0) -> List:
    """Random lists, target usually present → short scans."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        size = rng.randint(10, 500)
        data = [rng.randint(0, 1_000_000) for _ in range(size)]
        target = rng.choice(data)
        out.append((data, target))
    return out


def adversarial_inputs_early_exit(n: int, seed: int = 0) -> List:
    """Target absent from a long list → forces a full scan."""
    out = []
    for _ in range(n):
        size = 500
        data = list(range(size))
        target = -1  # guaranteed not in data
        out.append((data, target))
    return out


# ---------------------------------------------------------------------------
# Target 2 — data_dependent_loop(n)
# ---------------------------------------------------------------------------
def random_inputs_data_loop(n: int, seed: int = 0) -> List:
    """n drawn uniformly from a moderate range."""
    rng = random.Random(seed)
    return [(rng.randint(50, 500),) for _ in range(n)]


def adversarial_inputs_data_loop(n: int, seed: int = 0) -> List:
    """Every call uses the largest n in the range → longest loop."""
    return [(500,) for _ in range(n)]


# ---------------------------------------------------------------------------
# Target 3 — nested_conditional(x)
# ---------------------------------------------------------------------------
def random_inputs_nested(n: int, seed: int = 0) -> List:
    """x drawn uniformly across the whole range."""
    rng = random.Random(seed)
    return [(rng.randint(-10, 1999),) for _ in range(n)]


def adversarial_inputs_nested(n: int, seed: int = 0) -> List:
    """
    x chosen to land in the deepest branch AND satisfy x % 6 == 0
    (the 2000-iteration loop).
    """
    return [(1200,) for _ in range(n)]