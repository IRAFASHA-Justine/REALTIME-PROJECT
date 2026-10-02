"""
Mini Project 1.2 — Per-function execution-time histograms.

For each target function, plots the distribution of random and
adversarial durations, marks the measured maximum of each, and the
margined recommended WCET.
"""

import numpy as np
import matplotlib.pyplot as plt

from margin import compute_margined_wcet


data = np.load("strategy_data.npz")

TARGETS = [
    ("early_exit_scan",     "early_exit_scan"),
    ("data_dependent_loop", "data_dependent_loop"),
    ("nested_conditional",  "nested_conditional"),
]

MARGIN = 0.40


for name, key in TARGETS:
    d_rand = data[f"{key}__rand"] * 1e6    # to microseconds
    d_adv  = data[f"{key}__adv"]  * 1e6

    max_rand = d_rand.max()
    max_adv  = d_adv.max()
    working_max = max(max_rand, max_adv)
    margined = working_max * (1.0 + MARGIN)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bins = np.linspace(0, max(d_rand.max(), d_adv.max()) * 1.1, 40)
    ax.hist(d_rand, bins=bins, alpha=0.6, label="Random strategy",
            color="steelblue", edgecolor="black")
    ax.hist(d_adv,  bins=bins, alpha=0.6, label="Adversarial strategy",
            color="indianred", edgecolor="black")

    ax.axvline(max_rand, color="steelblue", linestyle="--", linewidth=1.5,
               label=f"Random max = {max_rand:.1f} us")
    ax.axvline(max_adv, color="indianred", linestyle="--", linewidth=1.5,
               label=f"Adversarial max = {max_adv:.1f} us")
    ax.axvline(margined, color="black", linestyle=":", linewidth=2,
               label=f"Margined WCET = {margined:.1f} us")

    ax.set_xlabel("Execution time [us]")
    ax.set_ylabel("count")
    ax.set_title(f"Execution-time distribution — {name}\n"
                 f"(max of both strategies x 1.40 = margined recommendation)")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(f"hist_{name}.png", dpi=130)
    plt.close(fig)

    print(f"Saved hist_{name}.png  "
          f"(rand max {max_rand:.1f} us, adv max {max_adv:.1f} us, "
          f"margined {margined:.1f} us)")

print("\nAll histograms saved.")