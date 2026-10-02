import numpy as np
import matplotlib.pyplot as plt

data = np.load("timing_data.npz")

T                     = float(data["T"])
D                     = float(data["D"])
release_jitter        = data["release_jitter"]        # actual - ideal release
completion_jitter     = data["completion_jitter"]     # completion - ideal release
response_time         = data["response_time"]
meets_deadline        = data["meets_deadline"]

# ---------- Release jitter stats ----------
rj_std   = np.std(release_jitter)
rj_maxabs = np.max(np.abs(release_jitter))

# ---------- Completion jitter stats ----------
cj_std   = np.std(completion_jitter)
cj_maxabs = np.max(np.abs(completion_jitter))

print("=== Jitter report (Section 1.3) ===")
print(f"Release jitter    std     : {rj_std*1000:8.3f} ms")
print(f"Release jitter    max |.| : {rj_maxabs*1000:8.3f} ms")
print()
print(f"Completion jitter std     : {cj_std*1000:8.3f} ms")
print(f"Completion jitter max |.| : {cj_maxabs*1000:8.3f} ms")
print()
print(f"Deadline D                : {D*1000:8.3f} ms")
print(f"Period T                  : {T*1000:8.3f} ms")
print(f"Misses                    : {int(np.sum(~meets_deadline))} / {len(meets_deadline)}")

# ---------- One figure, two histograms ----------
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

axes[0].hist(release_jitter * 1000.0, bins=30, color="steelblue", edgecolor="black")
axes[0].set_title("Release jitter (ms)\nactual - ideal release")
axes[0].set_xlabel("ms")
axes[0].set_ylabel("count")

axes[1].hist(completion_jitter * 1000.0, bins=30, color="indianred", edgecolor="black")
axes[1].set_title("Completion jitter (ms)\ncompletion - ideal release")
axes[1].set_xlabel("ms")
axes[1].set_ylabel("count")

plt.tight_layout()
plt.savefig("jitter_histograms.png", dpi=130)
print("\nSaved jitter_histograms.png")
plt.show()