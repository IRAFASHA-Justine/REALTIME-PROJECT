import numpy as np
import matplotlib.pyplot as plt

data = np.load("timing_data.npz")

T              = float(data["T"])
D              = float(data["D"])
response_time  = data["response_time"]
meets_deadline = data["meets_deadline"]
n_jobs         = len(response_time)

# ---------- Utilities (same definitions as Step 6) ----------
HARD_PENALTY = -10.0
lateness     = np.maximum(0.0, response_time - D)
hard_utility = np.where(response_time <= D, 1.0, HARD_PENALTY)
firm_utility = np.where(response_time <= D, 1.0, 0.0)
soft_utility = np.where(response_time <= D, 1.0, np.exp(-lateness / T))

idx = np.arange(n_jobs)

# ---------- Plot ----------
fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)

# --- Top: response time with deadline line ---
ax1 = axes[0]
ax1.plot(idx, response_time * 1000.0, "o-", markersize=4,
         color="steelblue", label="Response time R")
ax1.axhline(D * 1000.0, color="crimson", linestyle="--", linewidth=1.8,
            label=f"Deadline D = {D*1000:.0f} ms")
ax1.plot(idx[~meets_deadline], (response_time[~meets_deadline]) * 1000.0,
         "x", color="crimson", markersize=8, label="Miss")
ax1.set_ylabel("R  [ms]")
ax1.set_title("Response time vs job index, with deadline")
ax1.grid(alpha=0.3)
ax1.legend(loc="upper left")

# --- Bottom: three utility sequences ---
ax2 = axes[1]
ax2.plot(idx, hard_utility, ".", color="crimson",    label="Hard utility")
ax2.plot(idx, firm_utility, ".", color="darkorange", label="Firm utility")
ax2.plot(idx, soft_utility, ".", color="seagreen",   label="Soft utility")
ax2.axhline(0.0, color="gray", linewidth=0.8)
ax2.set_xlabel("job index k")
ax2.set_ylabel("Utility")
ax2.set_title("Hard / firm / soft utility under identical timing")
ax2.grid(alpha=0.3)
ax2.legend(loc="lower left")

plt.tight_layout()
plt.savefig("response_and_utility.png", dpi=130)
print("Saved response_and_utility.png")
plt.show()