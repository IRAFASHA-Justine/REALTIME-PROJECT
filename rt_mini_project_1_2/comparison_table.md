# Mini Project 1.2 — Comparison table

Margin applied: 40 % (Section 1.7 utilisation-budget convention)

| Function | Random max (µs) | Adversarial max (µs) | Working max (µs) | Margined WCET (µs) | Adversarial winner? |
|---|---|---|---|---|---|
| early_exit_scan | 24.1 | 106.7 | 106.7 | 149.4 | yes |
| data_dependent_loop | 81.2 | 46.5 | 81.2 | 113.7 | no |
| nested_conditional | 181.0 | 220.7 | 220.7 | 309.0 | yes |
