"""
Mini Project 1.2 — Comparison table.

Writes a markdown table summarising random max, adversarial max,
working max, and margined recommended WCET per target function.
"""

import numpy as np

from margin import compute_margined_wcet


data = np.load("strategy_data.npz")

TARGETS = ["early_exit_scan", "data_dependent_loop", "nested_conditional"]
MARGIN = 0.40


def us(x: float) -> str:
    return f"{x*1e6:.1f}"


lines = []
lines.append("| Function | Random max (µs) | Adversarial max (µs) | Working max (µs) | Margined WCET (µs) | Adversarial winner? |")
lines.append("|---|---|---|---|---|---|")

rows_data = {}

for name in TARGETS:
    d_rand = data[f"{name}__rand"]
    d_adv  = data[f"{name}__adv"]

    max_rand = float(d_rand.max())
    max_adv  = float(d_adv.max())
    working  = max(max_rand, max_adv)
    margined = compute_margined_wcet(working, margin_fraction=MARGIN).margined

    winner = "yes" if max_adv > max_rand else "no"

    lines.append(
        f"| {name} "
        f"| {us(max_rand)} "
        f"| {us(max_adv)} "
        f"| {us(working)} "
        f"| {us(margined)} "
        f"| {winner} |"
    )

    rows_data[name] = dict(
        random_max=max_rand,
        adversarial_max=max_adv,
        working=working,
        margined=margined,
        adv_wins=(max_adv > max_rand),
    )

table = "\n".join(lines)
print(table)
print()

with open("comparison_table.md", "w", encoding="utf-8") as f:
    f.write("# Mini Project 1.2 — Comparison table\n\n")
    f.write(f"Margin applied: {int(MARGIN*100)} % (Section 1.7 utilisation-budget convention)\n\n")
    f.write(table)
    f.write("\n")
print("Saved comparison_table.md")
