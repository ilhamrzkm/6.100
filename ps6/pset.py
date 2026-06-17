"""
6.100 Spring 2026
Problem Set 6

Please fill out the following info:
Name: Sana Shah
Kerberos: sanashah
Approximate time spent (HH:MM): 10:00
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
        self._name = name 
        self._value = value 
        self._volume = volume 
        self._weight = weight 
        self._cannot_carry = cannot_carry
        self._cannot_check = cannot_check
        self._pair = pair 

        if cannot_carry and cannot_check:
            raise ValueError()

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
        return self._name

    def get_value(self):
        return self._value

    def get_volume(self):
        return self._volume  

    def get_weight(self):
        return self._weight

    def cannot_carry(self):
        return self._cannot_carry

    def cannot_check(self):
        return self._cannot_check

    def get_info(self):
        return (self._value, self._volume, self._weight, self._cannot_carry, self._cannot_check)

    def set_pair(self, pair):
        self._pair = pair 

    def get_pair(self):
        # wait until Section 5 to implement
        return self._pair 

    def get_branches(self):
        # wait until Section 5 to implement
        branches = []

        if self._pair is None:
            #no pair so up to 3 branches for just this item
            branches.append({"value": 0, "volume": 0, "weight": 0}) #skip

            if not self.cannot_carry(): #carry, if allowed
                branches.append({"value": self.get_value(),
                                "volume": self.get_volume(),
                                "weight": 0})
        
            if not self.cannot_check(): #check if allowed
                branches.append({"value": self.get_value(),
                                "volume": 0,
                                "weight": self.get_weight()})

        else:
            # has a pair so up to 5 joint branches for (self, pair)
            
            branches.append({"value": 0, "volume": 0, "weight": 0}) #skip both

            if not self.cannot_carry() and not self._pair.cannot_carry(): #both in carry-on, if both are allowed
                branches.append({"value": self.get_value() + self._pair.get_value(),
                                "volume": self.get_volume() + self._pair.get_volume(),
                                "weight": 0})

            if not self.cannot_check() and not self._pair.cannot_check(): #both in checked bag, if both are allowed
                branches.append({"value": self.get_value() + self._pair.get_value(),
                                "volume": 0,
                                "weight": self.get_weight() + self._pair.get_weight()})
            
            if not self.cannot_carry() and not self._pair.cannot_check(): #self in carry-on, pair in checked bag
                branches.append({"value": self.get_value() + self._pair.get_value(),
                                "volume": self.get_volume(),
                                "weight": self._pair.get_weight()})
            
            if not self.cannot_check() and not self._pair.cannot_carry(): #self in checked bag, pair in carry-on
                branches.append({"value": self.get_value() + self._pair.get_value(),
                                "volume": self._pair.get_volume(),
                                "weight": self.get_weight()})

        return branches


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
    # base case: empty set has a single empty combination
    if len(items) == 0:
        return [{"carry": [], "checked": []}]
    
    first = items[0]
    rest = items[1:]

    combos_without = all_packing_combinations(rest)
    result = []

    for combo in combos_without:
        skip_combo = {"carry": combo["carry"], "checked": combo["checked"]} #skip first item and don't add it to either bag
        result.append(skip_combo)

        carry_combo = {"carry": combo["carry"] + [first], "checked": combo["checked"]} #carry first item and add it to the carry-on bag
        result.append(carry_combo)

        check_combo = {"carry": combo["carry"], "checked": combo["checked"] + [first]} #check first item and add it to the checked bag
        result.append(check_combo)

    return result

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
    all_combos = all_packing_combinations(items)

    best_value = 0
    best_combo = {"value": 0, "carry": [], "checked": []}

    for combo in all_combos:
        carry_items = combo["carry"]
        checked_items = combo["checked"]

        valid = True  
        for item in carry_items: #carry-on item restrictions
            if item.cannot_carry():
                valid = False
                break
        if not valid:
            continue

        for item in checked_items: #checked bag item restrictions
            if item.cannot_check():
                valid = False
                break
        if not valid:
            continue

        total_volume = 0
        for item in carry_items: 
            total_volume = total_volume + item.get_volume()

        total_weight = 0
        for item in checked_items: 
            total_weight = total_weight + item.get_weight()

        if total_volume > v_cap or total_weight > w_cap: #capacity constraints 
            continue

        
        total_value = 0
        for item in carry_items: #calculate total value
            total_value = total_value + item.get_value()
        for item in checked_items:
            total_value = total_value + item.get_value()

        if total_value > best_value: #update best if this combo is better
            best_value = total_value
            best_combo = {"value": total_value, "carry": carry_items, "checked": checked_items}

    return best_combo
    

############################################################
# dynamic programming solution
############################################################


def choose_packing_dp(items, v_cap, w_cap):
    """
    Solve the same problem as choose_packing_exhaustive(), but use a
    dynamic programming approach for greater efficiency.
    """
    memo = {}

    def dp(index, remaining_volume, remaining_weight):
        if index == len(items): #no items left to consider
            return {"value": 0, "carry": [], "checked": []}

        if (index, remaining_volume, remaining_weight) in memo: #return saved result if this subproblem was already solved
            return memo[(index, remaining_volume, remaining_weight)]

        item = items[index]
        best = {"value": 0, "carry": [], "checked": []}

        skip_result = dp(index + 1, remaining_volume, remaining_weight) #skip this item
        if skip_result["value"] > best["value"]:
            best = {"value": skip_result["value"],
                    "carry": skip_result["carry"],
                    "checked": skip_result["checked"]}

        if not item.cannot_carry(): #put item in carry on if allowed and volume fits
            if item.get_volume() <= remaining_volume:
                carry_result = dp(index + 1, remaining_volume - item.get_volume(), remaining_weight)
                carry_value = carry_result["value"] + item.get_value()
                if carry_value > best["value"]:
                    best = {"value": carry_value,
                            "carry": carry_result["carry"] + [item],
                            "checked": carry_result["checked"]}

        if not item.cannot_check(): #put item in checked bag if allowed and weight fits
            if item.get_weight() <= remaining_weight:
                check_result = dp(index + 1, remaining_volume, remaining_weight - item.get_weight())
                check_value = check_result["value"] + item.get_value()
                if check_value > best["value"]:
                    best = {"value": check_value,
                            "carry": check_result["carry"],
                            "checked": check_result["checked"] + [item]}

        memo[(index, remaining_volume, remaining_weight)] = best
        return best #return the best result for this subproblem

    return dp(0, v_cap, w_cap)



############################################################
# handling item pairs
############################################################


def group_pairs(items):
    """
    Given a list of Items, return a new list of the same Items so that
    pairs (if any) are adjacent.
    """
    result = []
    already_added = set()

    for item in items:
        if item in already_added:
            continue

        result.append(item)
        already_added.add(item)

        if item.get_pair() is not None:
            result.append(item.get_pair())
            already_added.add(item.get_pair())

    return result


def choose_packing_dp_with_pair(items, v_cap, w_cap):
    """
    Solve the same problem as choose_packing_dp(), but also respect
    paired items that must either both be packed or not at all.
    """
    grouped = group_pairs(items)
    memo = {}

    def dp(index, remaining_volume, remaining_weight):
        # base case: no items left to consider
        if index == len(grouped):
            return {"value": 0, "carry": [], "checked": []}

        # return cached result if this subproblem was already solved
        if (index, remaining_volume, remaining_weight) in memo:
            return memo[(index, remaining_volume, remaining_weight)]

        item = grouped[index]
        
        if item.get_pair() is not None: #if this item has a pair next index skips over both items
            next_index = index + 2
        else: #if not next index just moves forward by one
            next_index = index + 1

        best = {"value": 0, "carry": [], "checked": []}

        for branch in item.get_branches(): #iterate through all valid branches 
            branch_value = branch["value"]
            branch_volume = branch["volume"]
            branch_weight = branch["weight"]

            if branch_volume > remaining_volume: #skip this branch if it exceeds capacities
                continue
            if branch_weight > remaining_weight:
                continue

            
            rest_result = dp(next_index, #recursively solve the rest of the items
                             remaining_volume - branch_volume,
                             remaining_weight - branch_weight)

            total_value = branch_value + rest_result["value"]

            if total_value > best["value"]: #update best if this branch gives a better value
                
                carry_additions = [] #figure out which items to add to each bag for this branch
                checked_additions = []

                
                
                if item.get_pair() is None:
                    if branch_volume > 0: #branch_volume > 0 means something went in the carry on
                        carry_additions = [item]
                    elif branch_weight > 0: #branch_weight > 0 means something went in the checked bag
                        checked_additions = [item]
                else:
                    pair = item.get_pair()
                    if branch_volume == item.get_volume() + pair.get_volume(): #both in carry on
                        carry_additions = [item, pair]
                    elif branch_weight == item.get_weight() + pair.get_weight(): #both in checked
                        checked_additions = [item, pair]
                    elif branch_volume == item.get_volume(): #self in carry on, pair in checked
                        carry_additions = [item]
                        checked_additions = [pair]
                    elif branch_weight == item.get_weight(): #self in checked pair in carry on
                        checked_additions = [item]
                        carry_additions = [pair]

                best = {"value": total_value,
                        "carry": carry_additions + rest_result["carry"],
                        "checked": checked_additions + rest_result["checked"]}

        memo[(index, remaining_volume, remaining_weight)] = best
        return best

    return dp(0, v_cap, w_cap)


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

    for num_items in num_items_list:
        total_exhaustive_time = 0
        total_dp_time = 0

        for trial in range(num_trials):
            
            items = [] #generate random items for this trial
            for i in range(num_items):
                name = "item" + str(i)
                value = random.randint(1, 20)
                volume = random.randint(1, 10)
                weight = random.randint(1, 10)
                item = Item(name, value, volume, weight)
                items.append(item)

            start = time.time()    #measure exhaustive enumeration runtime
            choose_packing_exhaustive(items, v_cap, w_cap)
            end = time.time()
            total_exhaustive_time = total_exhaustive_time + (end - start)

            #measure dp runtime
            start = time.time()
            choose_packing_dp(items, v_cap, w_cap)
            end = time.time()
            total_dp_time = total_dp_time + (end - start)

        avg_exhaustive_time = total_exhaustive_time / num_trials #average the runtimes across trials
        avg_dp_time = total_dp_time / num_trials

        exhaustive_times.append(avg_exhaustive_time)
        dp_times.append(avg_dp_time)

    plt.figure(figsize=(10, 6))
    plt.plot(
        num_items_list,
        "<YOUR EXHAUSTIVE ENUMERATION DATA HERE>",
        "o-",
        label="Exhaustive Enumeration",
        linewidth=2,
        markersize=8,
    )
    plt.plot(
        num_items_list,
        "<YOUR DP DATA HERE>",
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

    for divisor in divisors:
        dp_avg = 0

        for trial in range(num_trials):
            random.seed(42 + trial)
            items = []
            for i in range(num_items):
                item = Item(
                    f"Item {i}",
                    random.randint(1, 100),
                    divisor * random.randint(1, v_cap // divisor // 4),
                    divisor * random.randint(1, w_cap // divisor // 4),
                )
                items.append(item)

            start = time.time()
            choose_packing_dp(items, v_cap, w_cap)
            dp_avg += time.time() - start

        dp_times.append(dp_avg / num_trials)
        if divisor == 1:
            discreteness_labels.append("Any int")
        else:
            discreteness_labels.append(f"Multiple of {divisor}")

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
    # 11 random items
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

    #experiment1_runtime_vs_items()
    experiment2_dp_vs_discreteness()
