"""
Mini Project 1.2 — Measurement harness.

A reusable wrapper that:
  - takes any target function
  - takes a list (or generator) of inputs
  - runs the function once per input, timing each call with perf_counter
  - returns the durations and the inputs that produced them
"""

import time
from typing import Callable, Iterable, Sequence, Tuple
import numpy as np


def measure_function(
    func: Callable,
    inputs: Sequence,
    repeat: int = 1,
    warmup: int = 20,
) -> Tuple[np.ndarray, list]:
    """
    Time `func` once per element of `inputs`.

    Parameters
    ----------
    func   : callable — the target function (takes *args or a single arg)
    inputs : sequence of argument tuples/lists OR plain values.
             If an element is a tuple/list, it is unpacked as *args;
             otherwise it is passed as a single argument.
    repeat : how many times each input is executed (>= 1). All samples
             are returned, so the array has len(inputs) * repeat elements.
    warmup : number of preliminary calls to warm caches / JIT / imports,
             performed before timing starts, results discarded.

    Returns
    -------
    durations : np.ndarray of float seconds (length len(inputs) * repeat)
    used_inputs : list of the inputs, in the same order as durations
    """
    if repeat < 1:
        raise ValueError("repeat must be >= 1")

    # -------- warm-up --------
    for i in range(min(warmup, len(inputs))):
        _invoke(func, inputs[i])

    # -------- measurement --------
    durations = []
    used_inputs = []

    for _ in range(repeat):
        for inp in inputs:
            t0 = time.perf_counter()
            _invoke(func, inp)
            t1 = time.perf_counter()
            durations.append(t1 - t0)
            used_inputs.append(inp)

    return np.asarray(durations, dtype=float), used_inputs


def _invoke(func: Callable, inp) -> None:
    """Call func with the given input; unpack tuples/lists as *args."""
    if isinstance(inp, (tuple, list)):
        func(*inp)
    else:
        func(inp)