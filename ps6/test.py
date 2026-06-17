# standard library
from functools import wraps
import unittest
from unittest.mock import MagicMock, patch
import random

# local application
import pset


############################################################
# test case helpers
############################################################


def check_valid_packing(result, items, v_cap, w_cap):
    """
    result: output of choose_packing
    items, v_cap, w_cap: input to choose_packing
    Asserts that the packing respects the weight and volume constraints,
        the total value is correct,
        and each item appears at most once in the packing.
    """
    total_value, carry_on, checked_bag = (
        result["value"],
        result["carry"],
        result["checked"],
    )

    v_used = sum(item.get_volume() for item in carry_on)
    w_used = sum(item.get_weight() for item in checked_bag)

    # check each packed item is in the original item set
    for item in carry_on:
        assert (
            item in items
        ), f"Packing not valid: unknown item {item} appears in carry-on"
    for item in checked_bag:
        assert (
            item in items
        ), f"Packing not valid: unknown item {item} appears in checked bag"

    # check each item appears at most once
    assert len(set(carry_on).intersection(set(checked_bag))) == 0 and len(
        set(carry_on + checked_bag)
    ) == len(carry_on) + len(
        checked_bag
    ), "Packing not valid: an item appears more than once in the packing."

    # check weight and volume constraints
    assert (
        v_used <= v_cap
    ), "Packing not valid: carry-on volume exceeded: %s > %s" % (v_used, v_cap)
    assert (
        w_used <= w_cap
    ), "Packing not valid: checked bag weight exceeded: %s > %s" % (
        w_used,
        w_cap,
    )

    # check items in carry-on are actually carry-able
    assert all(not item.cannot_carry() for item in carry_on), (
        "Packing not valid: item %s in carry-on but cannot be carried"
        % [item for item in carry_on if not item.cannot_carry()][0]
    )

    # check items in checked bag are actually check-able
    assert all(not item.cannot_check() for item in checked_bag), (
        "Packing not valid: item %s in checked bag but cannot be checked in"
        % [item for item in checked_bag if not item.cannot_check()][0]
    )

    # check total value is correct
    value = sum(item.get_value() for item in carry_on) + sum(
        item.get_value() for item in checked_bag
    )
    assert (
        value == total_value
    ), "Total value does not match items packed: %s != %s" % (
        value,
        total_value,
    )


def check_packing_returntype(result):
    assert isinstance(result, dict), (
        "choose_packing didn't return a dictionary: instead returned an instance of %s."
        % type(result)
    )
    assert len(result) == 3, (
        "choose_packing didn't return 3 elements {value, carry, checked}. Expected %s, got %s."
        % (3, len(result))
    )

    # check value is a number...
    assert isinstance(result["value"], (int, float)), (
        'choose_packing\'s return value "value" should be a number: instead got %s.'
        % type(result["value"])
    )

    # check carry is a list...
    assert isinstance(result["carry"], list), (
        'choose_packing\'s return value "carry" should be a list of Items: instead got %s.'
        % type(result["carry"])
    )
    # ...of Items
    for item in result["carry"]:
        assert isinstance(
            item, pset.Item
        ), f'choose_packing\'s return value "carry" should be a list of Items: element {item} is instead a {type(item)}'

    # check checked is a list...
    assert isinstance(result["checked"], list), (
        'choose_packing\'s return value "checked" should be a list of Items: instead got %s.'
        % type(result["checked"])
    )
    # ...of Items
    for item in result["checked"]:
        assert isinstance(
            item, pset.Item
        ), f'choose_packing\'s return value "checked" should be a list of Items: element {item} is instead a {type(item)}'


def comparable_combos(combos):
    """
    Convert combos to a comparable format:
        sort the items in carry and checked, and
        sort the combos by value and then items.
    Parameters:
        combos: list of dictionaries of the form {carry: list of Items, checked: list of Items}
    """
    new_combos = []
    for combo in combos:
        carry_on = [f"{item}" for item in combo["carry"]]
        checked_bag = [f"{item}" for item in combo["checked"]]
        sorted_combo = {
            "carry": tuple(sorted(carry_on)),
            "checked": tuple(sorted(checked_bag)),
        }
        new_combos.append(sorted_combo)
    return sorted(new_combos, key=lambda x: (x["carry"], x["checked"]))


def first_missing_combo(expected_comparable, actual_comparable):
    actual_comparable = set(
        tuple(combo[key] for key in combo) for combo in actual_comparable
    )
    for combo in expected_comparable:
        if (combo["carry"], combo["checked"]) not in actual_comparable:
            return {
                "carry": list(combo["carry"]),
                "checked": list(combo["checked"]),
            }
    return None


############################################################
# test case settings
############################################################


# DO NOT MODIFY
def case_options(points, failure, error):
    """Decorator to add points and messages to a test case"""

    def decorator(func):
        # Directly set attributes on the original function
        func.points = points
        func.failure_message = failure
        func.error_message = error

        @wraps(func)
        def wrapper(*args, **kwargs):
            if isinstance(args[-1], MagicMock):
                args = args[:-1]
            return func(*args, **kwargs)

        return wrapper

    return decorator


# DO NOT MODIFY
def testsuite_options(timeout, weight):
    """Decorator to add timeout and weight to a test suite"""

    def decorator(cls):
        # Directly set attributes on the original class
        cls.timeout = timeout
        cls.weight = weight
        return cls

    return decorator


############################################################
# item class
############################################################


@testsuite_options(4, 3)
class TestItem(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="Your code does not instantiate Items correctly",
        error="Task item_getter_methods error",
    )
    def test_item_getters(self):
        item = pset.Item("jorts", 8, 2, 9, cannot_check=True)
        method_list = [
            "get_name",
            "get_value",
            "get_volume",
            "get_weight",
            "cannot_carry",
            "cannot_check",
            "get_info",
        ]
        expected_list = ["jorts", 8, 2, 9, False, True, (8, 2, 9, False, True)]
        actual_list = [
            item.get_name(),
            item.get_value(),
            item.get_volume(),
            item.get_weight(),
            item.cannot_carry(),
            item.cannot_check(),
            item.get_info(),
        ]
        for method, expected, actual in zip(
            method_list, expected_list, actual_list
        ):
            self.assertEqual(
                expected,
                actual,
                f"Method {method} incorrect, expected: {expected}, got: {actual}",
            )

    @case_options(
        1,
        failure="Your code does not instantiate invalid Items correctly",
        error="Task item_invalid error",
    )
    def test_item_invalid(self):
        self.assertRaises(
            ValueError,
            (lambda: pset.Item("exam solutions", 1000, 1, 1, True, True)),
        )

    @case_options(
        1,
        failure="Your code does not stringify Items correctly",
        error="Task item_str error",
    )
    def test_item_str(self):
        item = pset.Item("Ninja Blender", 15, 10, 7, cannot_carry=True)
        expected = "Ninja Blender: value = 15, volume = 10, weight = 7, cannot carry"
        actual = f"{item}"
        self.assertEqual(
            expected,
            actual,
            f"Incorrect item string, expected: {expected}, got: {actual}. "
            + "Make sure to NOT modify __str__",
        )
        item = pset.Item("lithium ion batteries", 2, 1, 3, cannot_check=True)
        expected = (
            "lithium ion batteries: value = 2, volume = 1, weight = 3, cannot check"
        )
        actual = f"{item}"
        self.assertEqual(
            expected,
            actual,
            f"Incorrect item string, expected: {expected}, got: {actual}. "
            + "Make sure to NOT modify __str__",
        )
        item = pset.Item("iPad", 30, 4, 5)
        expected = "iPad: value = 30, volume = 4, weight = 5"
        actual = f"{item}"
        self.assertEqual(
            expected,
            actual,
            f"Incorrect item string, expected: {expected}, got: {actual}. "
            + "Make sure to NOT modify __str__",
        )


############################################################
# all packing combinations
############################################################


@testsuite_options(8, 7)
class TestAllCombos(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_all_combinations(self, expected, actual):
        passing = True
        error_msg = ""

        if len(expected) != len(actual):
            passing = False
            error_msg += f"Incorrect number of packing combinations, expected: {len(expected)}, got: {len(actual)}\n"

        expected_comparable = comparable_combos(expected)
        actual_comparable = comparable_combos(actual)
        if expected_comparable != actual_comparable:
            passing = False
            error_msg += f"Incorrect packing combinations, example missing combo: {first_missing_combo(expected_comparable, actual_comparable)}"

        assert passing, error_msg

    @case_options(
        3,
        failure="Your code does not generate all packing combinations correctly",
        error="Task test_combos_1 error",
    )
    def test_combos_1(self):
        shampoo = pset.Item("shampoo", 10, 5, 10)
        jorts = pset.Item("jorts", 8, 2, 8)
        items = [shampoo, jorts]
        expected = [
            {"carry": [], "checked": []},
            {"carry": [shampoo], "checked": []},
            {"carry": [shampoo, jorts], "checked": []},
            {"carry": [shampoo], "checked": [jorts]},
            {"carry": [], "checked": [shampoo]},
            {"carry": [jorts], "checked": [shampoo]},
            {"carry": [], "checked": [shampoo, jorts]},
            {"carry": [jorts], "checked": []},
            {"carry": [], "checked": [jorts]},
        ]
        actual = pset.all_packing_combinations(items)
        self.check_all_combinations(expected, actual)

    @case_options(
        2,
        failure="Your code does not generate the right number of packing combinations",
        error="Task test_combos_2 error",
    )
    def test_combos_2(self):
        items = [
            pset.Item("shampoo", 10, 5, 10, cannot_carry=True),
            pset.Item("pomade", 8, 3, 4),
            pset.Item("brush", 6, 4, 4, cannot_check=True),
            pset.Item("wave cap", 4, 1, 1),
        ]
        actual = pset.all_packing_combinations(items)
        self.assertEqual(
            3**4,
            len(actual),
            f"Incorrect number of packing combinations, expected: {3**4}, got: {len(actual)}",
        )

    @case_options(
        1,
        failure="Your code does not generate all packing combinations correctly (for 1 item)",
        error="Task test_combos_3 error",
    )
    def test_combos_3(self):
        shampoo = pset.Item("shampoo", 10, 5, 10)
        items = [shampoo]
        expected = [
            {"carry": [], "checked": []},
            {"carry": [shampoo], "checked": []},
            {"carry": [], "checked": [shampoo]},
        ]
        actual = pset.all_packing_combinations(items)
        self.check_all_combinations(expected, actual)

    @case_options(
        1,
        failure="Your code does not generate all packing combinations correctly (for 0 items)",
        error="Task test_combos_4 error",
    )
    def test_combos_4(self):
        items = []
        expected = [{"carry": [], "checked": []}]
        actual = pset.all_packing_combinations(items)
        self.assertEqual(
            expected,
            actual,
            f"Incorrect packing combinations, expected: {expected}, got: {actual}",
        )


############################################################
# exhaustive enumeration solution
############################################################


@testsuite_options(8, 6)
class TestExhaustive(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_exhaustive_all_fit error",
    )
    def test_exhaustive_all_fit(self):
        # test case where all items fit, no constraints
        items = [
            pset.Item("shampoo", 10, 5, 10),
            pset.Item(
                "Introduction to Computation and Programming Using Python, Third Edition, With Application to Computational Modeling and Understanding Data by John Guttag",
                15,
                10,
                20,
            ),
            pset.Item("pokemon plushies", 7, 3, 5),
            pset.Item("jorts", 8, 2, 8),
        ]

        v_cap = 15
        w_cap = 25

        result = pset.choose_packing_exhaustive(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 40)  # check for optimality

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_exhaustive_not_optimal_1_first error",
    )
    def test_exhaustive_not_optimal_1_first(self):
        # test case where it's not optimal to take the first item
        items = [
            pset.Item("spray tan spray", 8, 6, 6, cannot_carry=True),
            pset.Item("bucket hat collection", 10, 5, 5),
            pset.Item("baby shark singing plushie", 9, 5, 5),
        ]

        v_cap = 0
        w_cap = 10

        result = pset.choose_packing_exhaustive(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 19)
        self.assertEqual(result["carry"], [])
        self.assertEqual(set(result["checked"]), set([items[1], items[2]]))

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_exhaustive_not_optimal_2_carry_on error",
    )
    def test_exhaustive_not_optimal_2_carry_on(self):
        # test case where greedy solution that puts items in carry-on till full isn't optimal
        items = [
            pset.Item("7.012 textbook", 1, 3, 10),
            pset.Item("Pocari sweat", 1, 3, 3, cannot_carry=True),
            pset.Item(
                "extra underwear", 10, 6, 20
            ),  # greedy would put 1st two in carry-on, but optimal is to put this one in carry-on
            pset.Item("laptop", 5, 5, 10),
            pset.Item("extra shoes", 5, 5, 4),
            pset.Item("6-7 packs of gum", 2, 5, 4),
        ]

        v_cap = 6  # Carry-on volume capacity
        w_cap = 15  # Checked bag weight capacity

        result = pset.choose_packing_exhaustive(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 20)

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_exhaustive_not_optimal_3_checked error",
    )
    def test_exhaustive_not_optimal_3_checked(self):
        # test case where greedily filling the checked first is not optimal
        items = [
            pset.Item("Curious george plushie", 1, 3, 5),
            pset.Item("scented hand lotion", 1, 3, 5),
            pset.Item(
                "camera", 10, 6, 10
            ),  # greedy would put 1st two in checked, but optimal is to put this one in checked
            pset.Item("portable battery", 5, 5, 10),
        ]

        v_cap = 2
        w_cap = 10

        result = pset.choose_packing_exhaustive(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 10)

    @case_options(
        2,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_exhaustive_constrained error",
    )
    def test_exhaustive_constrained(self):
        # test case with significant constraints
        items = [
            pset.Item("Curious george plushie", 1, 3, 5),
            pset.Item("scented hand lotion", 1, 3, 5),
            pset.Item("camera", 10, 6, 10, cannot_check=True),
            pset.Item("portable battery", 5, 5, 10, cannot_carry=True),
            pset.Item("extra shoes", 5, 5, 4, cannot_carry=True),
        ]

        v_cap = 5
        w_cap = 10

        result = pset.choose_packing_exhaustive(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 7)


############################################################
# dynamic programming solution
############################################################


@testsuite_options(8, 3)
class TestDP(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        3,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_1_large error",
    )
    def test_dp_1_large(self):
        # large test case where recursive solution would hang for a long time
        random.seed(21)
        # 20 random items
        items = [
            pset.Item(
                f"Item {i}",
                random.randint(5, 20),
                random.randint(2, 10),
                random.randint(2, 10),
            )
            for i in range(20)
        ]
        v_cap = 50
        w_cap = 50

        result = pset.choose_packing_dp(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 267)

    @case_options(
        3,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_2_restrictions error",
    )
    def test_dp_2_restrictions(self):
        items = [
            pset.Item("A", 10, 5, 5, cannot_carry=True),
            pset.Item("B", 12, 5, 5, cannot_check=True),
        ]
        v_cap = 5
        w_cap = 5

        result = pset.choose_packing_dp(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)

        # must respect placement constraints
        self.assertEqual(result["value"], 22)
        self.assertEqual(result["carry"], [items[1]])
        self.assertEqual(result["checked"], [items[0]])

    @case_options(
        3,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_3_not_optimal_first error",
    )
    def test_dp_3_not_optimal_first(self):
        items = [
            pset.Item("A", 20, 10, 10),
            pset.Item("B", 19, 1, 5),
            pset.Item("C", 25, 10, 11),
            pset.Item("D", 5, 1, 5),
        ]
        v_cap = 10
        w_cap = 10

        result = pset.choose_packing_dp(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)

        self.assertEqual(result["value"], 49)
        self.assertEqual(result["carry"], [items[2]])
        self.assertEqual(set(result["checked"]), set([items[1], items[3]]))


############################################################
# item class modifications for pair extension
############################################################


@testsuite_options(4, 3)
class TestItemPairs(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="Your code does not implement pairs in Items correctly",
        error="Task item_set_and_get_pair error",
    )
    def test_item_pair(self):
        item1 = pset.Item("toothbrush", 8, 2, 9)
        item2 = pset.Item("toothpaste", 5, 1, 5)

        item1.set_pair(item2)
        item2.set_pair(item1)
        self.assertEqual(
            item1.get_pair(),
            item2,
            f"Item set_pair or get_pair not working correctly: expected {item2}, got {item1.get_pair()}",
        )
        self.assertEqual(
            item2.get_pair(),
            item1,
            f"Item set_pair or get_pair not working correctly: expected {item1}, got {item2.get_pair()}",
        )

    @case_options(
        1,
        failure="Your code does not implement pairs in Items correctly",
        error="Task test_item_pair_nonexistent error",
    )
    def test_item_pair_nonexistent(self):
        item1 = pset.Item("toothbrush", 8, 2, 9)
        item2 = pset.Item("toothpaste", 5, 1, 5)

        self.assertIsNone(
            item1.get_pair(),
            f"Item get_pair not working correctly: expected None, got {item1.get_pair()}",
        )
        self.assertIsNone(
            item2.get_pair(),
            f"Item get_pair not working correctly: expected None, got {item2.get_pair()}",
        )


############################################################
# group_pairs function for pairs extension
############################################################


@testsuite_options(4, 3)
class TestGroupPairs(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="Your code does not group pairs correctly",
        error="Task test_group_pairs error",
    )
    def test_group_pairs(self):
        items = [
            pset.Item("toothbrush", 3, 1, 1),
            pset.Item("shampoo", 5, 6, 5, cannot_carry=True),
            pset.Item("toothpaste", 3, 2, 2, cannot_carry=True),
            pset.Item("left shoe", 10, 7, 5),
            pset.Item("conditioner", 5, 6, 5, cannot_carry=True),
            pset.Item("right shoe", 10, 7, 5),
        ]
        items[0].set_pair(items[2])
        items[2].set_pair(items[0])
        items[1].set_pair(items[4])
        items[4].set_pair(items[1])
        items[3].set_pair(items[5])
        items[5].set_pair(items[3])

        result = pset.group_pairs(items)
        self.assertEqual(
            abs(result.index(items[0]) - result.index(items[2])), 1
        )
        self.assertEqual(
            abs(result.index(items[1]) - result.index(items[4])), 1
        )
        self.assertEqual(
            abs(result.index(items[3]) - result.index(items[5])), 1
        )


############################################################
# dynamic programming solution w/pairs
############################################################


@testsuite_options(8, 3)
class TestDPWithPairs(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_with_pair_1_basic error",
    )
    def test_dp_with_pair_1_basic(self):
        items = [
            pset.Item("toothbrush", 3, 1, 1),
            pset.Item("toothpaste", 3, 2, 2, cannot_carry=True),
            pset.Item("airpods", 10, 1, 2, cannot_check=True),
            pset.Item("airpod case", 5, 1, 1),
        ]
        items[0].set_pair(items[1])
        items[1].set_pair(items[0])
        items[2].set_pair(items[3])
        items[3].set_pair(items[2])

        v_cap, w_cap = 5, 5

        result = pset.choose_packing_dp_with_pair(items, v_cap, w_cap)

        self.assertEqual(result["value"], 21)
        self.assertIn(items[1], result["checked"])
        self.assertIn(items[2], result["carry"])
        self.assertIn(items[0], result["carry"] + result["checked"])
        self.assertIn(items[2], result["carry"] + result["checked"])

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_with_pair_2_tiny error",
    )
    def test_dp_with_pair_2_tiny(self):
        items = [
            pset.Item("jeans", 5, 3, 6),
            pset.Item("shampoo", 5, 3, 3),
            pset.Item("conditioner", 5, 3, 3),
        ]
        items[1].set_pair(items[2])
        items[2].set_pair(items[1])

        v_cap, w_cap = 5, 0

        result = pset.choose_packing_dp_with_pair(items, v_cap, w_cap)

        self.assertEqual(result["value"], 5)
        self.assertIn(items[0], result["carry"])
        self.assertNotIn(items[1], result["carry"] + result["checked"])
        self.assertNotIn(items[2], result["carry"] + result["checked"])

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_with_pair_3_small error",
    )
    def test_dp_with_pair_3_small(self):
        items = [
            pset.Item("toothbrush", 3, 1, 1),
            pset.Item("shampoo", 5, 6, 5, cannot_carry=True),
            pset.Item("toothpaste", 3, 2, 2, cannot_carry=True),
            pset.Item("left shoe", 10, 7, 5),
            pset.Item("conditioner", 5, 6, 5, cannot_carry=True),
            pset.Item("right shoe", 10, 7, 5),
        ]
        items[0].set_pair(items[2])
        items[2].set_pair(items[0])
        items[1].set_pair(items[4])
        items[4].set_pair(items[1])
        items[3].set_pair(items[5])
        items[5].set_pair(items[3])

        v_cap = 5
        w_cap = 15

        result = pset.choose_packing_dp_with_pair(items, v_cap, w_cap)

        self.assertEqual(result["value"], 26)
        self.assertIn(items[0], result["carry"] + result["checked"])
        self.assertNotIn(items[1], result["carry"] + result["checked"])
        self.assertIn(items[2], result["checked"])
        self.assertIn(items[3], result["checked"])
        self.assertNotIn(items[4], result["carry"] + result["checked"])
        self.assertIn(items[5], result["checked"])

    @case_options(
        1,
        failure="Your code does not generate an optimal packing solution",
        error="Task test_dp_with_pair_4_large error",
    )
    def test_dp_with_pair_4_large(self):
        # large test case where recursive solution would hang for a long time
        random.seed(42)
        # 20 random items
        items = [
            pset.Item(
                f"Item {i}",
                random.randint(5, 20),
                random.randint(2, 10),
                random.randint(2, 10),
            )
            for i in range(20)
        ]

        for i in range(0, 20, 4):
            items[i].set_pair(items[i + 1])
            items[i + 1].set_pair(items[i])

        v_cap = 20
        w_cap = 30

        result = pset.choose_packing_dp_with_pair(items, v_cap, w_cap)
        check_packing_returntype(result)
        check_valid_packing(result, items, v_cap, w_cap)
        self.assertEqual(result["value"], 181)


############################################################
# test results calculation and reporting
############################################################


class Results_600(unittest.TextTestResult):
    """Custom test result class to capture output and points."""

    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 0
        self.max_points = 0

    def _getOptions(self, test):
        method_name = getattr(test, "_testMethodName")
        method = getattr(test, method_name)
        func = method.__func__
        points = getattr(func, "points", 0)
        failure_msg = getattr(func, "failure_message", "")
        error_msg = getattr(func, "error_message", "")
        return points, failure_msg, error_msg

    def addSuccess(self, test):
        points, _, _ = self._getOptions(test)
        self.points += points
        self.max_points += points
        return super().addSuccess(test)

    def addFailure(self, test, err):
        points, failure_msg, _ = self._getOptions(test)
        self.output.append(f"❌ [-{points}] {failure_msg}, {err[1]}\n")
        self.max_points += points
        super().addFailure(test, err)

    def addError(self, test, err):
        points, _, error_msg = self._getOptions(test)
        self.output.append(f"❌ [-{points}] {error_msg}, {err[1]}\n")
        self.max_points += points
        super().addError(test, err)

    def getOutput(self):
        """Return the captured output."""
        if self.points > 0:
            self.output.append(
                f"\n✅ [+{self.points}] "
                f"{'All' if self.points == self.max_points else 'Some'}"
                f" tests passed!\n"
            )
        return "\n".join(self.output)

    def getPoints(self):
        """Return the total points."""
        return self.points


if __name__ == "__main__":
    test_parts = [
        TestItem,
        TestAllCombos,
        TestExhaustive,
        TestDP,
        TestItemPairs,
        TestGroupPairs,
        TestDPWithPairs,
    ]

    suite = unittest.TestSuite()
    for part in test_parts:
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(part))
    runner = unittest.TextTestRunner(resultclass=Results_600, verbosity=2)
    result = runner.run(suite)

    output = result.getOutput()
    points_earned = round(result.getPoints(), 3)
    print(output)
    print(f"Total points: {points_earned} / {result.max_points}")
    print(f"Score: {points_earned / result.max_points:4.0%}")
