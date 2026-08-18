"""
6.100 Spring 2026
Problem Set 6

Please fill out the following info:
Name:
Kerberos:
Approximate time spent (HH:MM):
"""

import matplotlib.pyplot as plt
import random
import time


############################################################
# model item properties
############################################################


class Item:

    def __init__(
        self, name, value, volume, weight,
        cannot_carry=False, cannot_check=False, pair=None,
    ):
        raise NotImplementedError

    def __str__(self):
        # DO NOT MODIFY THIS FUNCTION
        value_str = f"value = {self.get_value()}"
        volume_str = f"volume = {self.get_volume()}"
        weight_str = f"weight = {self.get_weight()}"
        components = [value_str, volume_str, weight_str]

        if self.cannot_carry():
            components.append("cannot carry")
        elif self.cannot_check():
            components.append("cannot check")

        return f"{self.get_name()}: " + ", ".join(components)

    __repr__ = __str__

    def get_name(self):
        raise NotImplementedError

    def get_value(self):
        raise NotImplementedError

    def get_volume(self):
        raise NotImplementedError

    def get_weight(self):
        raise NotImplementedError

    def cannot_carry(self):
        raise NotImplementedError

    def cannot_check(self):
        raise NotImplementedError

    def get_info(self):
        raise NotImplementedError

    def set_pair(self, pair):
        raise NotImplementedError

    def get_pair(self):
        # wait until Section 5 to implement
        raise NotImplementedError

    def get_branches(self):
        # wait until Section 5 to implement
        raise NotImplementedError


############################################################
# exhaustive enumeration solution
############################################################


def all_packing_combinations(items):
    """
    Generate all possible ways to pack the given items, ignoring
    capacity constraints and item restrictions.

    For each item, consider three possibilities: don't pack it, put it
    in the carry-on bag, or put it in the checked bag. Recursively
    generate all combinations.

    This function should NOT check capacity constraints or item
    restrictions. Those are validated later.

    Parameters:
        items (list): A list of Items to consider packing.

    Return a list of dicts, where each dict has the following mappings:
        "carry": A list of Items in the carry-on bag.
        "checked": A list of Items in the checked bag.
    """
    raise NotImplementedError


def choose_packing_exhaustive(items, v_cap, w_cap):
    """
    Evaluate all possible packing combinations to find the one with the
    maximum value that respects capacity constraints and item
    restrictions.

    Parameters:
        items (list): A list of Items.
        v_cap (int): The volume capacity of the carry-on bag.
        w_cap (int): The weight capacity of the checked bag.

    Return a dict representing the optimal packing solution, with the
    following mappings:
        "value": The total value (int) of the packed Items.
        "carry": A list of Items in the carry-on bag.
        "checked": A list of Items in the checked bag.
    """
    raise NotImplementedError


############################################################
# dynamic programming solution
############################################################


def choose_packing_dp(items, v_cap, w_cap):
    """
    Solve the same problem as choose_packing_exhaustive(), but use a
    dynamic programming approach for greater efficiency.
    """
    raise NotImplementedError


############################################################
# handling item pairs
############################################################


def group_pairs(items):
    """
    Given a list of Items, return a new list of the same Items so that
    pairs (if any) are adjacent.
    """
    raise NotImplementedError


def choose_packing_dp_with_pair(items, v_cap, w_cap):
    """
    Solve the same problem as choose_packing_dp(), but also respect
    paired items that must either both be packed or not at all.
    """
    raise NotImplementedError


############################################################
# experimental analysis
############################################################


def experiment1_runtime_vs_items():
    """
    Compare runtime of exhaustive enumeration vs DP as a function of the
    number of items.
    """
    num_items_list = list(range(5, 15))
    v_cap = 30
    w_cap = 30
    num_trials = 3
    exhaustive_times = []
    dp_times = []

    # TODO: time choose_packing_exhaustive and choose_packing_dp
    # for each n in num_items_list (average over num_trials).

    plt.figure(figsize=(10, 6))
    plt.plot(
        num_items_list,
        exhaustive_times,
        "o-",
        label="Exhaustive Enumeration",
        linewidth=2,
        markersize=8,
    )
    plt.plot(
        num_items_list,
        dp_times,
        "s-",
        label="Dynamic Programming",
        linewidth=2,
        markersize=8,
    )
    plt.xlabel("Number of Items", fontsize=12)
    plt.ylabel("Runtime (seconds)", fontsize=12)
    plt.title(
        "Runtime Comparison: Exhaustive Enumeration vs Dynamic Programming",
        fontsize=14,
    )
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    print("Experiment 1 complete: Runtime vs Number of Items")


def experiment2_dp_vs_discreteness():
    """
    Compare DP runtime as a function of volume and weight discreteness.
    """
    num_items = 15
    v_cap = 1024
    w_cap = 1024
    num_trials = 3

    divisors = [2**i for i in range(8)]
    dp_times = []
    discreteness_labels = []

    # TODO: for each divisor, generate items whose volume/weight are
    # multiples of that divisor, time choose_packing_dp, store averages.

    plt.figure(figsize=(10, 6))
    plt.plot(divisors, dp_times, "o-", color="green", linewidth=2, markersize=8)
    plt.xlabel("Discreteness (Divisor)", fontsize=12)
    plt.ylabel("DP Runtime (seconds)", fontsize=12)
    plt.title(
        "DP Runtime vs Volume/Weight Discreteness (12 items)", fontsize=14
    )
    plt.xscale("log")
    plt.xticks(divisors, discreteness_labels, rotation=45, ha="right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    print("Experiment 2 complete: DP Runtime vs Volume/Weight Discreteness")


############################################################
# manual testing code
############################################################


def manual_test_packing(size="small", dp=False):
    random.seed(21)

    num_items_dict = {"small": 5, "medium": 12, "large": 20}
    cap_size_dict = {"small": 12, "medium": 30, "large": 50}

    items = []
    for i in range(num_items_dict[size]):
        item = Item(
            f"Item {i}",
            random.randint(5, 20),
            random.randint(2, 10),
            random.randint(2, 10),
        )
        items.append(item)
    v_cap = cap_size_dict[size]
    w_cap = cap_size_dict[size]

    if dp:
        packing_function = choose_packing_dp
    else:
        packing_function = choose_packing_exhaustive

    start_time = time.time()
    result = packing_function(items, v_cap, w_cap)
    end_time = time.time()
    run_time = end_time - start_time

    print(format_results(result, run_time, label=size, dp=dp))
    return result, run_time


def manual_test_packing_pairs():
    random.seed(42)
    items = [
        Item(
            f"Item {i}",
            random.randint(5, 20),
            random.randint(2, 10),
            random.randint(2, 10),
        )
        for i in range(11)
    ]

    for i in range(0, 11, 3):
        items[i].set_pair(items[i + 1])
        items[i + 1].set_pair(items[i])

    v_cap = 10
    w_cap = 15

    start_time = time.time()
    result = choose_packing_dp_with_pair(items, v_cap, w_cap)
    end_time = time.time()
    run_time = end_time - start_time

    print(format_results(result, run_time, label="pairs test", dp=True))
    return result, run_time


def format_results(result, run_time, label, dp):
    output = []
    output.append(
        f"TEST: {label}, {'dynamic programming' if dp else 'exhaustive'}"
    )
    output.append(f"run time: {run_time:5f}s")
    output.append(f"total_value: {result['value']}")
    output.append(f"carry on:")
    for item in result["carry"]:
        output.append(f"  {item}")
    output.append(f"checked bag:")
    for item in result["checked"]:
        output.append(f"  {item}")
    output.append("")
    return "\n".join(output)


if __name__ == "__main__":
    pass

    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # feel free to modify or extend them when debugging your code.
    # run test.py to make sure your code passes all our test cases.

    # manual_test_packing(size="small", dp=False)
    # manual_test_packing(size="medium", dp=False)
    # manual_test_packing(size="large", dp=False)  # should take too long

    # manual_test_packing(size="small", dp=True)
    # manual_test_packing(size="medium", dp=True)
    # manual_test_packing(size="large", dp=True)

    # manual_test_packing_pairs()

    # experiment1_runtime_vs_items()
    # experiment2_dp_vs_discreteness()
