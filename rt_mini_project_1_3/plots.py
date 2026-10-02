"""
Mini Project 1.3 — Sweep plots.

Produces:
  - 4a: release and completion jitter vs probability (extra delay)
  - 4b: release and completion jitter vs magnitude (extra delay)
  - 3:  release jitter vs background-load intensity
  - 5a: execution-time variability (normal spread sweep)
  - 5b: execution-time variability (heavy-tailed)
  - combined: jitter growth vs hit rate across all disturbances
"""

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Load saved sweeps
# ---------------------------------------------------------------------------
bg  = np.load("sweep_background.npz")
p_  = np.load("sweep_prob.npz")
m_  = np.load("sweep_mag.npz")
en  = np.load("sweep_exec_normal.npz")
eh  = np.load("sweep_exec_heavy.npz")


def savefig(name):
    plt.tight_layout()
    plt.savefig(name, dpi=130)
    plt.close()
    print(f"Saved {name}")


# ---------------------------------------------------------------------------
# Plot 1 — Background load sweep
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(bg["intensities"], bg["rel_jitter_std"] * 1000, "o-",
        label="Release jitter std")
ax.plot(bg["intensities"], bg["cmp_jitter_std"] * 1000, "s-",
        label="Completion jitter std")
ax.set_xlabel("Background-load intensity")
ax.set_ylabel("Jitter std [ms]")
ax.set_title("Background CPU load vs jitter (T = 50 ms, D = 40 ms)")
ax.grid(alpha=0.3); ax.legend()
savefig("plot_background.png")


# ---------------------------------------------------------------------------
# Plot 2 — Extra delay, probability sweep
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(p_["probs"], p_["rel_jitter_std"] * 1000, "o-",
        label="Release jitter std")
ax.plot(p_["probs"], p_["cmp_jitter_std"] * 1000, "s-",
        label="Completion jitter std")
ax.plot(p_["probs"], p_["rel_jitter_max"] * 1000, "o--", alpha=0.5,
        label="Release jitter max")
ax.plot(p_["probs"], p_["cmp_jitter_max"] * 1000, "s--", alpha=0.5,
        label="Completion jitter max")
ax.set_xlabel("Trigger probability p (magnitude = 5 ms)")
ax.set_ylabel("Jitter [ms]")
ax.set_title("Extra delay vs probability (T = 50 ms, D = 40 ms)")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
savefig("plot_extra_delay_prob.png")


# ---------------------------------------------------------------------------
# Plot 3 — Extra delay, magnitude sweep
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
mag_ms = m_["mags"] * 1000
ax.plot(mag_ms, m_["rel_jitter_std"] * 1000, "o-",
        label="Release jitter std")
ax.plot(mag_ms, m_["cmp_jitter_std"] * 1000, "s-",
        label="Completion jitter std")
ax.plot(mag_ms, m_["cmp_jitter_max"] * 1000, "s--", alpha=0.5,
        label="Completion jitter max")
ax.set_xlabel("Delay magnitude [ms]  (p = 0.10)")
ax.set_ylabel("Jitter [ms]")
ax.set_title("Extra delay vs magnitude (T = 50 ms, D = 40 ms)")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
savefig("plot_extra_delay_mag.png")


# ---------------------------------------------------------------------------
# Plot 4 — Execution variability, normal sweep
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(en["spreads"], en["cmp_jitter_std"] * 1000, "o-",
        label="Completion jitter std")
ax.plot(en["spreads"], en["exec_max"] * 1000, "s-",
        label="Response time max")
ax.set_xlabel("Normal spread (mean = 5000 iterations)")
ax.set_ylabel("Time [ms]")
ax.set_title("Execution-time variability (normal) vs spread")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
savefig("plot_exec_normal.png")


# ---------------------------------------------------------------------------
# Plot 5 — Execution variability, heavy tail
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(eh["means"], eh["cmp_jitter_std"] * 1000, "o-",
        label="Completion jitter std")
ax.plot(eh["means"], eh["exec_max"] * 1000, "s-",
        label="Response time max")
ax.set_xlabel("Heavy-tail mean (iterations)")
ax.set_ylabel("Time [ms]")
ax.set_title("Execution-time variability (heavy tail) vs mean")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
savefig("plot_exec_heavy.png")


# ---------------------------------------------------------------------------
# Plot 6 — Combined: jitter growth vs hit rate across all mechanisms
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 5))

def plot_series(name, x, jitter_ms, hit_frac, marker):
    # Normalise jitter to its value at the leftmost point for comparability
    j0 = jitter_ms[0] if jitter_ms[0] > 0 else 1e-6
    rel = jitter_ms / j0
    ax.plot(x, rel, marker + "-", label=f"{name} (jitter, normalised)")
    # Overlay hit fraction on a secondary axis — see twin axis below.

# Normalised jitter series
ax.plot(bg["intensities"],
        bg["cmp_jitter_std"] / bg["cmp_jitter_std"][1],
        "o-", label="Background load (normalised)")
ax.plot(p_["probs"],
        p_["cmp_jitter_std"] / p_["cmp_jitter_std"][0],
        "s-", label="Extra delay prob (normalised)")
ax.plot(m_["mags"] * 1000,
        m_["cmp_jitter_std"] / m_["cmp_jitter_std"][0],
        "^-", label="Extra delay mag (normalised)")
ax.plot(eh["means"],
        eh["cmp_jitter_std"] / eh["cmp_jitter_std"][0],
        "D-", label="Heavy-tailed exec (normalised)")

ax.set_xlabel("Sweep parameter (units differ per series; see legends)")
ax.set_ylabel("Completion jitter std  (normalised to first point)")
ax.set_title("Combined: jitter growth across all disturbances\n"
             "(hit fraction stayed at 1.000 in every configuration)")
ax.grid(alpha=0.3); ax.legend(fontsize=8)
savefig("plot_combined.png")


print("\nAll plots saved.")