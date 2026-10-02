import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

data = np.load("timing_data.npz")

T                 = float(data["T"])
D                 = float(data["D"])
actual_release    = data["actual_release"]      # offset from r_0
completion        = data["completion"]
absolute_deadline = data["absolute_deadline"]
meets_deadline    = data["meets_deadline"]

# We plot only a window of jobs for readability (fig1_3 is schematic).
# Try k = 0 .. 14 first; the miss at some index may or may not be in this window.
K_START = 55
K_END   = 70

fig, ax = plt.subplots(figsize=(11, 5))

for i in range(K_START, K_END):
    y = i
    start = actual_release[i]
    width = completion[i] - actual_release[i]
    color = "steelblue" if meets_deadline[i] else "crimson"

    # broken_barh wants (x_start, x_width) tuples in a list, per y
    ax.broken_barh([(start, width)], (y - 0.35, 0.7),
                   facecolors=color, edgecolor="black")

    # Deadline marker (vertical tick at absolute_deadline)
    ax.plot([absolute_deadline[i], absolute_deadline[i]],
            [y - 0.4, y + 0.4],
            color="black", linewidth=1.2)

ax.set_yticks(range(K_START, K_END))
ax.set_yticklabels([f"job {i}" for i in range(K_START, K_END)])
ax.set_xlabel("Time since r_0  [s]")
ax.set_title(f"fig1_3-style timing diagram (first {K_END - K_START} jobs)\n"
             f"T = {T*1000:.0f} ms, D = {D*1000:.0f} ms")

# Legend
handles = [
    Patch(facecolor="steelblue", edgecolor="black", label="Job met deadline"),
    Patch(facecolor="crimson",   edgecolor="black", label="Job missed deadline"),
    plt.Line2D([0], [0], color="black", lw=1.2, label="Deadline marker"),
]
ax.legend(handles=handles, loc="upper right")
ax.grid(alpha=0.3, axis="x")
plt.tight_layout()
plt.savefig("timing_diagram.png", dpi=130)
print("Saved timing_diagram.png")
plt.show()