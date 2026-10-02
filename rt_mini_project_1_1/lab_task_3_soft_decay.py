"""
Mini Project 1.1 — Lab Task 3
Soft utility with different decay rates.
"""

import numpy as np
import matplotlib.pyplot as plt


data = np.load("timing_data.npz")
D             = float(data["D"])
T             = float(data["T"])
response_time = data["response_time"]
missed        = ~data["meets_deadline"]
lateness      = np.maximum(0.0, response_time - D)

# Three decay rates
taus = {
    "Fast decay (tau = 0.05 T)": 0.05 * T,
    "Baseline   (tau = T)":      T,
    "Slow decay (tau = 5 T)":    5.0 * T,
}

print("=== Lab Task 3: soft utility vs decay rate ===")
print(f"n_jobs: {len(response_time)},  misses: {int(missed.sum())}")
for label, tau in taus.items():
    soft = np.where(response_time <= D, 1.0, np.exp(-lateness / tau))
    print(f"  {label:>28} : "
          f"mean soft util = {soft.mean():.4f}  | "
          f"on misses = {soft[missed].mean():.4f}")

# Plot
late_axis = np.linspace(0.0, 3.0 * T, 400)
fig, ax = plt.subplots(figsize=(8, 4.5))
for (label, tau), col in zip(taus.items(),
                              ["crimson", "seagreen", "steelblue"]):
    curve = np.where(late_axis <= 0, 1.0, np.exp(-late_axis / tau))
    ax.plot(np.concatenate([[-1e-4], late_axis]),
            np.concatenate([[1.0], curve]),
            label=label, color=col, linewidth=2)

ax.axvline(0.0, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Lateness = max(0, R - D)  [s]")
ax.set_ylabel("Soft utility")
ax.set_title("Soft utility with three decay rates")
ax.set_ylim(-0.05, 1.1)
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("lt3_soft_decay.png", dpi=130)
plt.show()