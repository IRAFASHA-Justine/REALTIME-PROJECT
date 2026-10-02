"""
Mini Project 1.3 — Consolidated results table.

Writes results_table.md, containing one table per disturbance
mechanism plus a combined summary table.
"""

import numpy as np


bg = np.load("sweep_background.npz")
p_ = np.load("sweep_prob.npz")
m_ = np.load("sweep_mag.npz")
en = np.load("sweep_exec_normal.npz")
eh = np.load("sweep_exec_heavy.npz")


def ms(x):    # seconds → milliseconds string
    return f"{x*1e3:.3f}"


lines = []
lines.append("# Mini Project 1.3 — Results table\n")
lines.append("All runs: T = 50 ms, D = 40 ms, N = 200 jobs per configuration.\n")


# ---------- Table 1 — Background load ----------
lines.append("## Table 1 — Background CPU load (intensity sweep)\n")
lines.append("| Intensity | Release jitter std (ms) | Release jitter max (ms) | Completion jitter std (ms) | Completion jitter max (ms) | Hit fraction |")
lines.append("|---|---|---|---|---|---|")
for i, intensity in enumerate(bg["intensities"]):
    lines.append(
        f"| {intensity:.2f} | {ms(bg['rel_jitter_std'][i])} | "
        f"{ms(bg['rel_jitter_max'][i])} | {ms(bg['cmp_jitter_std'][i])} | "
        f"{ms(bg['cmp_jitter_max'][i])} | {bg['hit_fraction'][i]:.4f} |"
    )
lines.append("")


# ---------- Table 2 — Extra delay, probability sweep ----------
lines.append("## Table 2 — Extra delay: probability sweep (magnitude = 5 ms)\n")
lines.append("| p | Release jitter std (ms) | Completion jitter std (ms) | Completion jitter max (ms) | Hit fraction |")
lines.append("|---|---|---|---|---|")
for i, p in enumerate(p_["probs"]):
    lines.append(
        f"| {p:.2f} | {ms(p_['rel_jitter_std'][i])} | "
        f"{ms(p_['cmp_jitter_std'][i])} | {ms(p_['cmp_jitter_max'][i])} | "
        f"{p_['hit_fraction'][i]:.4f} |"
    )
lines.append("")


# ---------- Table 3 — Extra delay, magnitude sweep ----------
lines.append("## Table 3 — Extra delay: magnitude sweep (probability = 0.10)\n")
lines.append("| d (ms) | Release jitter std (ms) | Completion jitter std (ms) | Completion jitter max (ms) | Hit fraction |")
lines.append("|---|---|---|---|---|")
for i, d in enumerate(m_["mags"]):
    lines.append(
        f"| {d*1000:.0f} | {ms(m_['rel_jitter_std'][i])} | "
        f"{ms(m_['cmp_jitter_std'][i])} | {ms(m_['cmp_jitter_max'][i])} | "
        f"{m_['hit_fraction'][i]:.4f} |"
    )
lines.append("")


# ---------- Table 4 — Normal exec variability ----------
lines.append("## Table 4 — Execution-time variability (normal distribution)\n")
lines.append("| Spread | Response mean (ms) | Response max (ms) | Completion jitter std (ms) | Hit fraction |")
lines.append("|---|---|---|---|---|")
for i, s in enumerate(en["spreads"]):
    lines.append(
        f"| {s} | {ms(en['exec_mean'][i])} | {ms(en['exec_max'][i])} | "
        f"{ms(en['cmp_jitter_std'][i])} | {en['hit_fraction'][i]:.4f} |"
    )
lines.append("")


# ---------- Table 5 — Heavy-tailed exec variability ----------
lines.append("## Table 5 — Execution-time variability (heavy-tailed distribution)\n")
lines.append("| Mean workload | Response mean (ms) | Response max (ms) | Completion jitter std (ms) | Hit fraction |")
lines.append("|---|---|---|---|---|")
for i, mn in enumerate(eh["means"]):
    lines.append(
        f"| {mn} | {ms(eh['exec_mean'][i])} | {ms(eh['exec_max'][i])} | "
        f"{ms(eh['cmp_jitter_std'][i])} | {eh['hit_fraction'][i]:.4f} |"
    )
lines.append("")


# ---------- Table 6 — Combined summary ----------
lines.append("## Table 6 — Combined summary: jitter and tail growth vs hit fraction\n")
lines.append("For each mechanism, the first and last configurations are shown side by side. "
             "Hit fraction remained 1.000 in every case, yet jitter and worst-case response time grew substantially.\n")
lines.append("| Mechanism | Config | Completion jitter std (ms) | Response time max (ms) | Hit fraction |")
lines.append("|---|---|---|---|---|")

def row(mech, cfg, jit, rmax, hit):
    lines.append(f"| {mech} | {cfg} | {ms(jit)} | {ms(rmax)} | {hit:.4f} |")

# Background load
row("Background load", f"intensity = {bg['intensities'][0]:.2f}",
    bg["cmp_jitter_std"][0], bg["cmp_jitter_max"][0], bg["hit_fraction"][0])
row("Background load", f"intensity = {bg['intensities'][-1]:.2f}",
    bg["cmp_jitter_std"][-1], bg["cmp_jitter_max"][-1], bg["hit_fraction"][-1])

# Extra delay, probability
row("Extra delay (prob)", f"p = {p_['probs'][0]:.2f}",
    p_["cmp_jitter_std"][0], p_["cmp_jitter_max"][0], p_["hit_fraction"][0])
row("Extra delay (prob)", f"p = {p_['probs'][-1]:.2f}",
    p_["cmp_jitter_std"][-1], p_["cmp_jitter_max"][-1], p_["hit_fraction"][-1])

# Extra delay, magnitude
row("Extra delay (mag)", f"d = {m_['mags'][0]*1000:.0f} ms",
    m_["cmp_jitter_std"][0], m_["cmp_jitter_max"][0], m_["hit_fraction"][0])
row("Extra delay (mag)", f"d = {m_['mags'][-1]*1000:.0f} ms",
    m_["cmp_jitter_std"][-1], m_["cmp_jitter_max"][-1], m_["hit_fraction"][-1])

# Normal exec variability
row("Exec variability (normal)", f"spread = {en['spreads'][0]}",
    en["cmp_jitter_std"][0], en["exec_max"][0], en["hit_fraction"][0])
row("Exec variability (normal)", f"spread = {en['spreads'][-1]}",
    en["cmp_jitter_std"][-1], en["exec_max"][-1], en["hit_fraction"][-1])

# Heavy-tailed exec variability
row("Exec variability (heavy)", f"mean = {eh['means'][0]}",
    eh["cmp_jitter_std"][0], eh["exec_max"][0], eh["hit_fraction"][0])
row("Exec variability (heavy)", f"mean = {eh['means'][-1]}",
    eh["cmp_jitter_std"][-1], eh["exec_max"][-1], eh["hit_fraction"][-1])


text = "\n".join(lines)
print(text)
with open("results_table.md", "w", encoding="utf-8") as f:
    f.write(text)
print("\nSaved results_table.md")