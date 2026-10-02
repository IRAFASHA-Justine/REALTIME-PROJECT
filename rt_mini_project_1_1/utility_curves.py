import numpy as np
import matplotlib.pyplot as plt

data = np.load("timing_data.npz")

D              = float(data["D"])
T              = float(data["T"])
response_time  = data["response_time"]
meets_deadline = data["meets_deadline"]
n_jobs         = len(response_time)

# ---------- Lateness ----------
lateness = np.maximum(0.0, response_time - D)   # 0 for on-time jobs

# ---------- Hard utility ----------
# 1 while R <= D, large negative once R > D
HARD_PENALTY = -10.0
hard_utility = np.where(response_time <= D, 1.0, HARD_PENALTY)

# ---------- Firm utility ----------
# 1 while R <= D, exactly 0 once R > D
firm_utility = np.where(response_time <= D, 1.0, 0.0)

# ---------- Soft utility ----------
# decays gradually after the deadline.
# Choose a decay rate that makes the curve visibly decay over ~1-2 periods.
# Here we use an exponential: u = exp(-lateness / tau), tau = T.
tau = T
soft_utility = np.where(
    response_time <= D,
    1.0,
    np.exp(-lateness / tau)
)

# ---------- Summary ----------
hit_fraction = np.mean(meets_deadline)
print("=== Utility summary ===")
print(f"n_jobs                : {n_jobs}")
print(f"T (s)                 : {T:.4f}")
print(f"D (s)                 : {D:.4f}")
print(f"Deadline hit fraction : {hit_fraction:.4f}  ({int(hit_fraction*n_jobs)}/{n_jobs})")
print(f"Misses                : {int(np.sum(~meets_deadline))}")
print()
print("Mean utility over all jobs:")
print(f"  Hard  : {np.mean(hard_utility):8.3f}")
print(f"  Firm  : {np.mean(firm_utility):8.3f}")
print(f"  Soft  : {np.mean(soft_utility):8.3f}")
print()
print("On missed jobs only, mean utility:")
missed = ~meets_deadline
print(f"  Hard  : {np.mean(hard_utility[missed]):8.3f}")
print(f"  Firm  : {np.mean(firm_utility[missed]):8.3f}")
print(f"  Soft  : {np.mean(soft_utility[missed]):8.3f}")

# ---------- Plot utility curves as a function of lateness ----------
late_axis = np.linspace(0.0, 3.0 * T, 300)
hard_curve = np.where(late_axis <= 0, 1.0, HARD_PENALTY)        # marker only
firm_curve = np.where(late_axis <= 0, 1.0, 0.0)
soft_curve = np.where(late_axis <= 0, 1.0, np.exp(-late_axis / tau))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.step(np.concatenate([[-1e-3], late_axis]),
        np.concatenate([[1.0], hard_curve]),
        where="post", label="Hard",  color="crimson", linewidth=2)
ax.step(np.concatenate([[-1e-3], late_axis]),
        np.concatenate([[1.0], firm_curve]),
        where="post", label="Firm",  color="darkorange", linewidth=2)
ax.plot(np.concatenate([[-1e-3], late_axis]),
        np.concatenate([[1.0], soft_curve]),
        label="Soft (exp, tau = T)", color="seagreen", linewidth=2)

ax.axvline(0.0, color="gray", linestyle="--", linewidth=1)
ax.set_xlabel("Lateness = max(0, R - D)  [s]")
ax.set_ylabel("Utility of the result")
ax.set_title("Utility vs lateness — hard / firm / soft (fig1_1 analog)")
ax.set_ylim(min(HARD_PENALTY, -1) - 0.5, 1.3)
ax.grid(alpha=0.3)
ax.legend()
plt.tight_layout()
plt.savefig("utility_curves.png", dpi=130)
print("\nSaved utility_curves.png")

# ---------- Plot per-job utilities ----------
fig2, ax2 = plt.subplots(figsize=(10, 4.5))
idx = np.arange(n_jobs)
ax2.plot(idx, hard_utility, ".", label="Hard", color="crimson")
ax2.plot(idx, firm_utility, ".", label="Firm", color="darkorange")
ax2.plot(idx, soft_utility, ".", label="Soft", color="seagreen")
ax2.set_xlabel("job index k")
ax2.set_ylabel("utility")
ax2.set_title("Per-job utility under hard / firm / soft classification")
ax2.grid(alpha=0.3)
ax2.legend()
plt.tight_layout()
plt.savefig("utility_per_job.png", dpi=130)
print("Saved utility_per_job.png")

plt.show()
