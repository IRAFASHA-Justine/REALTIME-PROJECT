from harness import measure_function
from stats import summarise, format_stats
from margin import compute_margined_wcet, format_margin
from targets import early_exit_scan, data_dependent_loop, nested_conditional


def run_stats(name, func, inputs, repeat=1):
    d, _ = measure_function(func, inputs, repeat=repeat, warmup=10)
    s = summarise(d)
    print(format_stats(name, s))
    print()
    return s


if __name__ == "__main__":
    # ---------- Inputs for each target ----------
    inputs1 = [([i for i in range(100)], 99)] * 50
    inputs2 = [(n,) for n in range(50, 500, 25)]
    inputs3 = [(x,) for x in range(-10, 2000, 50)]

    # ---------- Statistics ----------
    s1 = run_stats("early_exit_scan (worst case in-list)",
                   early_exit_scan, inputs1, repeat=1)
    s2 = run_stats("data_dependent_loop",
                   data_dependent_loop, inputs2, repeat=3)
    s3 = run_stats("nested_conditional",
                   nested_conditional, inputs3, repeat=3)

    # ---------- Margined recommended WCET ----------
    print("=== Margined recommended WCET-for-scheduling ===")
    for name, s in [("early_exit_scan", s1),
                    ("data_dependent_loop", s2),
                    ("nested_conditional", s3)]:
        m = compute_margined_wcet(s.maximum, margin_fraction=0.40)
        print(format_margin(name, m))
        print()