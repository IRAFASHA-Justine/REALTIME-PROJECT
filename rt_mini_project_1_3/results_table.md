# Mini Project 1.3 — Results table

All runs: T = 50 ms, D = 40 ms, N = 200 jobs per configuration.

## Table 1 — Background CPU load (intensity sweep)

| Intensity | Release jitter std (ms) | Release jitter max (ms) | Completion jitter std (ms) | Completion jitter max (ms) | Hit fraction |
|---|---|---|---|---|---|
| 0.00 | 1.456 | 15.999 | 1.450 | 16.187 | 1.0000 |
| 0.25 | 0.739 | 3.585 | 0.749 | 3.949 | 1.0000 |
| 0.50 | 1.686 | 5.913 | 1.683 | 6.157 | 1.0000 |
| 0.75 | 2.504 | 8.170 | 2.511 | 8.493 | 1.0000 |
| 1.00 | 4.699 | 22.118 | 4.700 | 22.282 | 1.0000 |

## Table 2 — Extra delay: probability sweep (magnitude = 5 ms)

| p | Release jitter std (ms) | Completion jitter std (ms) | Completion jitter max (ms) | Hit fraction |
|---|---|---|---|---|
| 0.05 | 1.092 | 1.636 | 14.475 | 1.0000 |
| 0.10 | 0.205 | 1.821 | 7.758 | 1.0000 |
| 0.20 | 0.461 | 2.227 | 8.123 | 1.0000 |
| 0.50 | 0.593 | 2.770 | 7.964 | 1.0000 |

## Table 3 — Extra delay: magnitude sweep (probability = 0.10)

| d (ms) | Release jitter std (ms) | Completion jitter std (ms) | Completion jitter max (ms) | Hit fraction |
|---|---|---|---|---|
| 1 | 1.524 | 1.603 | 17.456 | 1.0000 |
| 5 | 2.061 | 2.702 | 28.674 | 1.0000 |
| 10 | 0.433 | 3.494 | 12.088 | 1.0000 |
| 20 | 0.948 | 7.056 | 32.023 | 1.0000 |

## Table 4 — Execution-time variability (normal distribution)

| Spread | Response mean (ms) | Response max (ms) | Completion jitter std (ms) | Hit fraction |
|---|---|---|---|---|
| 0 | 0.589 | 1.063 | 0.578 | 1.0000 |
| 1000 | 0.668 | 2.547 | 1.897 | 1.0000 |
| 3000 | 0.679 | 2.315 | 0.855 | 1.0000 |
| 6000 | 0.765 | 3.360 | 1.004 | 1.0000 |
| 10000 | 0.823 | 5.176 | 0.989 | 1.0000 |

## Table 5 — Execution-time variability (heavy-tailed distribution)

| Mean workload | Response mean (ms) | Response max (ms) | Completion jitter std (ms) | Hit fraction |
|---|---|---|---|---|
| 2000 | 0.291 | 3.722 | 1.781 | 1.0000 |
| 4000 | 0.500 | 5.605 | 0.795 | 1.0000 |
| 6000 | 0.708 | 9.521 | 0.956 | 1.0000 |
| 8000 | 1.014 | 16.576 | 1.814 | 1.0000 |

## Table 6 — Combined summary: jitter and tail growth vs hit fraction

For each mechanism, the first and last configurations are shown side by side. Hit fraction remained 1.000 in every case, yet jitter and worst-case response time grew substantially.

| Mechanism | Config | Completion jitter std (ms) | Response time max (ms) | Hit fraction |
|---|---|---|---|---|
| Background load | intensity = 0.00 | 1.450 | 16.187 | 1.0000 |
| Background load | intensity = 1.00 | 4.700 | 22.282 | 1.0000 |
| Extra delay (prob) | p = 0.05 | 1.636 | 14.475 | 1.0000 |
| Extra delay (prob) | p = 0.50 | 2.770 | 7.964 | 1.0000 |
| Extra delay (mag) | d = 1 ms | 1.603 | 17.456 | 1.0000 |
| Extra delay (mag) | d = 20 ms | 7.056 | 32.023 | 1.0000 |
| Exec variability (normal) | spread = 0 | 0.578 | 1.063 | 1.0000 |
| Exec variability (normal) | spread = 10000 | 0.989 | 5.176 | 1.0000 |
| Exec variability (heavy) | mean = 2000 | 1.781 | 3.722 | 1.0000 |
| Exec variability (heavy) | mean = 8000 | 1.814 | 16.576 | 1.0000 |