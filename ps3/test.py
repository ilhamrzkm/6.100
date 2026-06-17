from functools import wraps
import numpy as np
import os
import pandas as pd
import random
import pset
import unittest
import time


# Path relative to THIS test file
BASE_DIR = os.path.dirname(__file__)

# Path to the real data/ directory that ships with the pset
DATA_DIR = os.path.join(BASE_DIR, "data")
TEMP_FILE = os.path.join(DATA_DIR, "temp_change.csv")
DISASTERS_FILE = os.path.join(DATA_DIR, "disasters.csv")
INDOOR_FILE = os.path.join(DATA_DIR, "indoor_temps.csv")


############################################################
# test case settings
############################################################


# DO NOT MODIFY
def case_options(points, failure, error):
    """Decorator to add points and messages to a test case."""

    def decorator(func):
        func.points = points
        func.failure_message = failure
        func.error_message = error

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


# DO NOT MODIFY
def testsuite_options(timeout, weight):
    """Decorator to add timeout and weight to a test suite."""

    def decorator(cls):
        cls.timeout = timeout
        cls.weight = weight
        return cls

    return decorator


############################################################
# test regression implementations
############################################################


@testsuite_options(8, 4)
class TestRegression(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        "Function 'center' is not implemented correctly",
        "Error occurred while testing 'center'",
    )
    def test_center(self):
        fn = getattr(pset, "center", None)
        if not callable(fn):
            self.fail(
                "Function 'center' is not defined or not callable in the student script."
            )

        test_cases = [
            ([5, 7, 9, 11], [0, 2, 4, 6]),
            ([3, 3, 3], [0, 0, 0]),
            ([-4, -2, 1, 3], [0, 2, 5, 7]),
            ([10], [0]),
        ]

        for x, expected in test_cases:
            result = fn(x)
            self.assertIsInstance(
                result,
                list,
                f"center should return a list, got {type(result)}.",
            )
            self.assertEqual(
                len(result),
                len(x),
                f"Returned list has incorrect length. Expected {len(x)}, got {len(result)}.",
            )
            for val in result:
                self.assertIsInstance(
                    val,
                    (int, float),
                    f"All centered values should be numeric, got {type(val)}.",
                )
            self.assertEqual(
                result,
                expected,
                f"Incorrect centering.\nInput: {x}\nExpected: {expected}\nGot: {result}",
            )
            self.assertEqual(
                min(result),
                0,
                f"Centered data must have minimum 0, got min={min(result)}.",
            )

    @case_options(
        2,
        "Function 'fit_line_exhaustive' is not implemented correctly",
        "Error occurred while testing 'fit_line_exhaustive'",
    )
    def test_fit_line_exhaustive(self):
        fn = getattr(pset, "fit_line_exhaustive", None)
        if not callable(fn):
            self.fail(
                "Function 'fit_line_exhaustive' is not defined or not callable in the student script."
            )

        test_cases = [
            (
                [0, 1, 2, 3],
                [-1.5, 0.5, 2.5, 4.5],
                [0.5, 1.5, 2.0, 2.5],
                [-3.0, -1.5, 0.0],
                2.0,
                -1.5,
            ),
            (
                [0, 1, 2, 3],
                [3.5, 2.0, 0.5, -1.0],
                [-2.0, -1.5, -1.0, 0.0],
                [1.0, 3.5, 5.0],
                -1.5,
                3.5,
            ),
            (
                [0, 1, 2, 3],
                [-2.0, -2.0, -2.0, -2.0],
                [-1.0, 0.0, 1.0],
                [-4.0, -2.0, 0.0],
                0.0,
                -2.0,
            ),
        ]

        for x, y, m_vals, b_vals, exp_m, exp_b in test_cases:
            m, b, y_pred = fn(x, y, m_vals, b_vals)

            self.assertAlmostEqual(
                m,
                exp_m,
                places=6,
                msg=f"Incorrect slope returned. Expected {exp_m}, got {m}.",
            )
            self.assertAlmostEqual(
                b,
                exp_b,
                places=6,
                msg=f"Incorrect intercept returned. Expected {exp_b}, got {b}.",
            )
            self.assertEqual(
                len(y_pred),
                len(x),
                f"y_pred should have the same length as x: expected {len(x)=}, got {len(y_pred)=}.",
            )
            expected_preds = [exp_m * xi + exp_b for xi in x]
            self.assertTrue(
                np.allclose(y_pred, expected_preds),
                f"Incorrect y_pred values. Expected {expected_preds}, got {y_pred}.",
            )

    @case_options(
        2,
        "Function 'fit_line_bisection' is not implemented correctly",
        "Error occurred while testing 'fit_line_bisection'",
    )
    def test_fit_line_bisection(self):
        fn = getattr(pset, "fit_line_bisection", None)
        if not callable(fn):
            self.fail(
                "Function 'fit_line_bisection' is not defined or not callable in the student script."
            )

        test_cases = [
            ([0, 1, 2, 3], [-1.5, 0.5, 2.5, 4.5], 2.0, -1.5),
            ([0, 1, 2, 3], [3.5, 2.0, 0.5, -1.0], -1.5, 3.5),
            ([0, 1, 2, 3], [-2.0, -2.0, -2.0, -2.0], 0.0, -2.0),
        ]

        start_time = time.time()

        for x, y, exp_a, exp_b in test_cases:
            a, b, y_pred = fn(x, y, a_lo=-5.0, a_hi=5.0, epsilon=1e-6)

            self.assertIsInstance(a, float)
            self.assertIsInstance(b, float)
            self.assertIsInstance(y_pred, list)

            self.assertTrue(abs(a - exp_a) <= 0.15)
            self.assertTrue(abs(b - exp_b) <= 0.25)
            self.assertEqual(len(y_pred), len(x))

            expected_preds = [a * xi + b for xi in x]
            self.assertTrue(np.allclose(y_pred, expected_preds, atol=1e-6))

        elapsed_time = time.time() - start_time
        self.assertLess(
            elapsed_time,
            0.5,
            f"fit_line_bisection took too long to run: {elapsed_time:.2f} seconds. Ensure you are correctly implementing a bisection method."
        )

    @case_options(
        2,
        "Function 'fit_line_polyfit' is not implemented correctly",
        "Error occurred while testing 'fit_line_polyfit'",
    )
    def test_fit_line_polyfit(self):
        fn = getattr(pset, "fit_line_polyfit", None)
        if not callable(fn):
            self.fail(
                "Function 'fit_line_polyfit' is not defined or not callable in the student script."
            )

        test_cases = [
            (
                [0, 1, 2, 3],
                [-1.5, 0.5, 2.5, 4.5],
                2.0,
                -1.5,
            ),
            (
                [0, 1, 2, 3],
                [3.5, 2.0, 0.5, -1.0],
                -1.5,
                3.5,
            ),
            (
                [0, 1, 2, 3],
                [-2.0, -2.0, -2.0, -2.0],
                0.0,
                -2.0,
            ),
        ]

        for x, y, exp_a, exp_b in test_cases:
            result = fn(x, y)

            self.assertIsInstance(
                result,
                list,
                f"fit_line_polyfit should return a list, got {type(result)}.",
            )
            self.assertEqual(
                len(result),
                3,
                f"fit_line_polyfit should return [a, b, y_pred], got: {result}",
            )

            a, b, y_pred = result

            self.assertIsInstance(
                a,
                (int, float, np.number),
                f"Slope a should be numeric, got {type(a)}.",
            )
            self.assertIsInstance(
                b,
                (int, float, np.number),
                f"Intercept b should be numeric, got {type(b)}.",
            )
            self.assertIsInstance(
                y_pred,
                (list, np.ndarray),
                f"y_pred should be list-like, got {type(y_pred)}.",
            )

            self.assertEqual(
                len(y_pred),
                len(x),
                f"y_pred should have length {len(x)}, got {len(y_pred)}.",
            )

            expected_preds = [a * xi + b for xi in x]
            self.assertTrue(
                np.allclose(y_pred, expected_preds, atol=1e-6),
                f"y_pred values are inconsistent with returned a and b.\n"
                f"Expected (from a, b): {expected_preds}\nGot: {y_pred}",
            )

            self.assertTrue(
                abs(a - exp_a) <= 0.15,
                f"Incorrect slope. Expected a ≈ {exp_a}, got {a}.",
            )
            self.assertTrue(
                abs(b - exp_b) <= 0.25,
                f"Incorrect intercept. Expected b ≈ {exp_b}, got {b}.",
            )


############################################################
# test helpers for permutation
############################################################


@testsuite_options(8, 2)
class TestPermute(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        "Function 'permute_y' is not implemented correctly",
        "Error occurred while testing 'permute_y'",
    )
    def test_permute_y(self):
        fn = getattr(pset, "permute_y", None)
        if not callable(fn):
            self.fail(
                "Function 'permute_y' is not defined or not callable in the student script."
            )

        y = [10, 20, 30, 40, 50]
        y_copy = y.copy()

        random.seed(6100)
        result = fn(y)

        self.assertNotEqual(
            result,
            y,
            f"permute_y must change the order of elements: input {y} should not equal output {result}.",
        )

        self.assertIsInstance(
            result,
            list,
            f"permute_y should return a list, got {type(result)}.",
        )
        self.assertEqual(
            len(result),
            len(y),
            f"Permuted y has incorrect length. Expected {len(y)}, got {len(result)}.",
        )
        self.assertCountEqual(
            result,
            y,
            f"Permuted y must contain the same elements as input.\nExpected elements: {y}\nGot: {result}",
        )
        self.assertEqual(
            y,
            y_copy,
            f"permute_y must not modify the input list. Expected input list to be {y_copy}, got {y}.",
        )

    @case_options(
        1,
        "Function 'permute_xy' is not implemented correctly",
        "Error occurred while testing 'permute_xy'",
    )
    def test_permute_xy(self):
        fn = getattr(pset, "permute_xy", None)
        if not callable(fn):
            self.fail(
                "Function 'permute_xy' is not defined or not callable in the student script."
            )

        x = [1, 2, 3, 4, 5]
        y = [10, 20, 30, 40, 50]
        x_copy = list(x)
        y_copy = list(y)

        random.seed(6100)
        x_perm, y_perm = fn(x, y)

        self.assertNotEqual(
            list(zip(x_perm, y_perm)),
            list(zip(x, y)),
            f"permute_xy must change the order of (x, y) pairs. Original pairs: {list(zip(x, y))}\nGot: {list(zip(x_perm, y_perm))}",
        )

        self.assertIsInstance(
            x_perm,
            list,
            f"x_perm should be a list, got {type(x_perm)}.",
        )
        self.assertIsInstance(
            y_perm,
            list,
            f"y_perm should be a list, got {type(y_perm)}.",
        )
        self.assertEqual(
            len(x_perm),
            len(x),
            f"x_perm has incorrect length. Expected {len(x)}, got {len(x_perm)}.",
        )
        self.assertEqual(
            len(y_perm),
            len(y),
            f"y_perm has incorrect length. Expected {len(y)}, got {len(y_perm)}.",
        )
        self.assertCountEqual(
            x_perm,
            x,
            f"x_perm must contain the same elements as x.\nExpected: {x}\nGot: {x_perm}",
        )
        self.assertCountEqual(
            y_perm,
            y,
            f"y_perm must contain the same elements as y.\nExpected: {y}\nGot: {y_perm}",
        )

        original_pairs = set(zip(x, y))
        permuted_pairs = set(zip(x_perm, y_perm))
        self.assertSetEqual(
            permuted_pairs,
            original_pairs,
            f"permute_xy must preserve (x, y) pairing.\nOriginal pairs: {original_pairs}\nGot: {permuted_pairs}",
        )
        self.assertEqual(
            x,
            x_copy,
            f"permute_xy must not modify the input x list. Expected input x list to be {x_copy}, got {x}.",
        )
        self.assertEqual(
            y,
            y_copy,
            f"permute_xy must not modify the input y list. Expected input y list to be {y_copy}, got {y}.",
        )


############################################################
# test train validate split
############################################################


@testsuite_options(8, 3)
class TestTrainValidateSplit(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        2,
        "Function 'train_validate_split' is not implemented correctly",
        "Error occurred while testing 'train_validate_split'",
    )
    def test_train_validate_split(self):
        fn = getattr(pset, "train_validate_split", None)
        if not callable(fn):
            self.fail(
                "Function 'train_validate_split' is not defined or not callable in the student script."
            )

        x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        y = [v * 10 for v in x]
        val_frac = 0.3

        result = fn(x, y, val_frac=val_frac)

        self.assertIsInstance(
            result,
            list,
            f"train_validate_split should return a list, got {type(result)}.",
        )
        self.assertEqual(
            len(result),
            4,
            f"train_validate_split should return [x_train, y_train, x_val, y_val], got {result}",
        )

        x_train, y_train, x_val, y_val = result

        for name, arr in [
            ("x_train", x_train),
            ("y_train", y_train),
            ("x_val", x_val),
            ("y_val", y_val),
        ]:
            self.assertIsInstance(
                arr,
                list,
                f"{name} should be a list, got {type(arr)}.",
            )

        train_pairs = list(zip(x_train, y_train))
        val_pairs = list(zip(x_val, y_val))

        for xi, yi in train_pairs + val_pairs:
            self.assertEqual(
                yi,
                xi * 10,
                f"x/y pairing was not preserved: x={xi}, y={yi}.",
            )

        original_pairs = set(zip(x, y))
        returned_pairs = set(train_pairs + val_pairs)

        self.assertSetEqual(
            returned_pairs,
            original_pairs,
            f"train_validate_split must return exactly the original (x, y) pairs, no more and no less.\nExpected pairs: {original_pairs}\nReturned pairs: {returned_pairs}",
        )

        self.assertTrue(
            set(train_pairs).isdisjoint(set(val_pairs)),
            f"Training and validation sets must be disjoint.\nTraining pairs: {train_pairs}\nValidation pairs: {val_pairs}",
        )

        self.assertGreater(
            len(train_pairs),
            0,
            f"Training set must not be empty. Got training set: {train_pairs}",
        )
        self.assertGreater(
            len(val_pairs),
            0,
            f"Validation set must not be empty. Got validation set: {val_pairs}",
        )


    @case_options(
        2,
        "Function 'evaluate_poly_degree' is not implemented correctly",
        "Error occurred while testing 'evaluate_poly_degree'",
    )
    def test_evaluate_poly_degree(self):
        fn = getattr(pset, "evaluate_poly_degree", None)
        if not callable(fn):
            self.fail(
                "Function 'evaluate_poly_degree' is not defined or not callable in the student script."
            )

        x = list(range(20))
        y = [1.5 * xi**2 - 3.0 * xi + 2.0 for xi in x]

        degree = 2
        val_frac = 0.25

        result = fn(x, y, degree, k_or_val_frac=val_frac)

        val_r2 = result

        self.assertIsInstance(
            val_r2,
            (int, float, np.number),
            f"val_r2 should be numeric, got {type(val_r2)}.",
        )

        expected_train_r2 = 1.0
        expected_val_r2 = 1.0


        self.assertAlmostEqual(
            val_r2,
            expected_val_r2,
            places=5,
            msg=f"Incorrect val_r2: expected {expected_val_r2}, got {val_r2}.",
        )

        result2 = fn(x, y, degree, k_or_val_frac=val_frac)
        self.assertEqual(
            result,
            result2,
            "evaluate_poly_degree should be deterministic given the same seed.",
        )


############################################################
# test k-fold cross validation
############################################################


@testsuite_options(8, 4)
class TestKFoldCrossValidation(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        2,
        "Function 'make_folds' is not implemented correctly",
        "Error occurred while testing 'make_folds'",
    )
    def test_make_folds(self):
        fn = getattr(pset, "make_folds", None)
        if not callable(fn):
            self.fail(
                "Function 'make_folds' is not defined or not callable in the student script."
            )

        x = list(range(23))
        y = [3 * xi - 1 for xi in x]
        k = 5

        for seed in [0, 6100, 42]: # check multiple seeds to ensure consistent behavior
            random.seed(seed)
            x_perm, y_perm = pset.permute_xy(x, y)

            result = fn(x_perm, y_perm, k=k)

            self.assertIsInstance(result, list)
            self.assertEqual(len(result), 2)

            folds_x, folds_y = result
            self.assertEqual(len(folds_x), k)
            self.assertEqual(len(folds_y), k)

            for fx, fy in zip(folds_x, folds_y):
                self.assertIsInstance(fx, list)
                self.assertIsInstance(fy, list)
                self.assertEqual(len(fx), len(fy))

            returned_pairs = set()
            for fx, fy in zip(folds_x, folds_y):
                returned_pairs.update(zip(fx, fy))

            self.assertSetEqual(
                returned_pairs,
                set(zip(x, y)),
                f"make_folds must include every (x, y) pair exactly once. Expected pairs: {set(zip(x, y))}, got {returned_pairs}",
            )

            sizes = [len(fx) for fx in folds_x]
            self.assertLessEqual(
                max(sizes) - min(sizes),
                1,
                f"Fold sizes must be balanced, got sizes {sizes}.",
            )

    @case_options(
        2,
        "Function 'get_validation_scores' is not implemented correctly",
        "Error occurred while testing 'get_validation_scores'",
    )
    def test_get_validation_scores(self):
        fn = getattr(pset, "get_validation_scores", None)
        if not callable(fn):
            self.fail(
                "Function 'get_validation_scores' is not defined or not callable in the student script."
            )

        x = list(range(-20, 21))
        y_linear = [2 * xi + 1 for xi in x]
        y_quad = [xi**2 for xi in x]
        k = 5

        for seed in [0, 6100]: # check multiple seeds to ensure consistent behavior
            random.seed(seed)
            x_perm, y_perm = pset.permute_xy(x, y_linear)
            folds_x, folds_y = pset.make_folds(x_perm, y_perm, k=k)

            scores = fn(folds_x, folds_y, degree=1, k=k)

            self.assertIsInstance(scores, list)
            self.assertEqual(len(scores), k)

            for r2 in scores:
                self.assertIsInstance(r2, (int, float, np.number))
                self.assertLessEqual(r2, 1.000001)

            self.assertGreater(
                sum(scores) / len(scores),
                0.9,
                f"Expected high mean R^2 for linear data, got {scores}.",
            )

        random.seed(6100)
        x_perm, y_perm = pset.permute_xy(x, y_quad)
        folds_x, folds_y = pset.make_folds(x_perm, y_perm, k=k)

        r2_deg1 = sum(fn(folds_x, folds_y, degree=1, k=k)) / k
        r2_deg2 = sum(fn(folds_x, folds_y, degree=2, k=k)) / k

        self.assertGreater(
            r2_deg2,
            r2_deg1 + 0.3,
            f"Degree-2 model should outperform degree-1 on quadratic data.\nGot r2_deg1={r2_deg1}, r2_deg2={r2_deg2}.",
        )


############################################################
# test compare poly degrees
############################################################


@testsuite_options(8, 3)
class TestComparePolyDegrees(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        2,
        "Function 'compare_poly_degrees' is not implemented correctly",
        "Error occurred while testing 'compare_poly_degrees'",
    )
    def test_compare_poly_degrees(self):
        fn = getattr(pset, "compare_poly_degrees", None)
        if not callable(fn):
            self.fail(
                "Function 'compare_poly_degrees' is not defined or not callable in the student script."
            )

        x = [2000, 2001, 2002, 2003, 2004, 2005]
        y = [2, 3, 7, 13, 21, 31]

        degrees = [2, 0, 1]

        result = fn(
            x,
            y,
            degrees,
            k_or_val_frac=0.3,
            show_plot=False,
        )

        self.assertIsInstance(
            result,
            list,
            f"compare_poly_degrees should return a list, got {type(result)}.",
        )
        self.assertEqual(
            len(result),
            len(degrees),
            f"Expected {len(degrees)} degree results, got {len(result)}.",
        )

        returned_degrees = [item[0] for item in result]
        self.assertEqual(
            returned_degrees,
            sorted(degrees),
            f"Degrees should be returned sorted. Expected {sorted(degrees)}, got {returned_degrees}.",
        )

        for deg, vals in result:
            self.assertIsInstance(
                vals,
                list,
                f"Values for degree {deg} should be a list, got {type(vals)}.",
            )
            self.assertEqual(
                len(vals),
                3,
                f"Values for degree {deg} should be [coeffs, y_pred, val_r2].",
            )

            coeffs, y_pred, val_r2 = vals

            self.assertIsInstance(
                coeffs,
                (list, np.ndarray),
                f"Coefficients for degree {deg} should be a list, got {type(coeffs)}.",
            )
            self.assertEqual(
                len(coeffs),
                deg + 1,
                f"Degree {deg} polynomial should have {deg + 1} coefficients.",
            )

            self.assertIsInstance(
                y_pred,
                (list, np.ndarray),
                f"y_pred for degree {deg} should be array-like, got {type(y_pred)}.",
            )
            self.assertEqual(
                len(y_pred),
                len(x),
                f"y_pred length mismatch for degree {deg}. Expected {len(x)}, got {len(y_pred)}.",
            )

            self.assertIsInstance(
                val_r2,
                (int, float, np.number),
                f"val_r2 for degree {deg} should be numeric, got {type(val_r2)}.",
            )


############################################################
# test permutation trend
############################################################


@testsuite_options(8, 4)
class TestPermutationTrend(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        3,
        "Function 'trend_permutation_test' is not implemented correctly",
        "Error occurred while testing 'trend_permutation_test'",
    )
    def test_trend_permutation_test(self):
        fn = getattr(pset, "trend_permutation_test", None)
        if not callable(fn):
            self.fail(
                "Function 'trend_permutation_test' is not defined or not callable in the student script."
            )

        x = [0, 1, 2, 3, 4]
        y = [1, 3, 5, 7, 9]  # strong linear trend

        result = fn(
            x,
            y,
            n_permutations=500,
        )

        self.assertIsInstance(
            result,
            list,
            f"trend_permutation_test must return a list, got {type(result)}.",
        )
        self.assertEqual(
            len(result),
            4,
            f"trend_permutation_test must return [a_obs, p_value, null_lo, null_hi], got {result}.",
        )

        a_obs, p_value, null_lo, null_hi = result

        for name, val in zip(
            ["a_obs", "p_value", "null_lo", "null_hi"],
            [a_obs, p_value, null_lo, null_hi],
        ):
            self.assertIsInstance(
                val,
                (int, float, np.number),
                f"{name} should be numeric, got {type(val)}.",
            )

        self.assertGreater(
            abs(a_obs),
            0,
            f"Observed slope should be nonzero for a clear trend, got {a_obs}.",
        )

        self.assertGreaterEqual(
            p_value,
            0.0,
            f"p_value must be between 0 and 1. Got {p_value}.",
        )
        self.assertLessEqual(
            p_value,
            1.0,
            f"p_value must be between 0 and 1. Got {p_value}.",
        )

        self.assertLess(
            p_value,
            0.05,
            f"p_value should be small for a strong trend, got {p_value}.",
        )

        self.assertLess(
            null_lo,
            null_hi,
            f"Null interval lower bound must be less than upper bound. Got [null_lo, null_hi] = [{null_lo}, {null_hi}].",
        )

        x2 = [0, 1, 2, 3, 4]
        y2 = [5, 5, 5, 5, 5]  # no variation -> no trend

        result2 = fn(
            x2,
            y2,
            n_permutations=500,
        )

        a_obs2, p_value2, null_lo2, null_hi2 = result2

        self.assertAlmostEqual(
            a_obs2,
            0.0,
            places=3,
            msg=f"Observed slope should be ~0 when there is no trend, got {a_obs2}.",
        )

        self.assertGreater(
            p_value2,
            0.5,
            f"p_value should be large when no trend exists, got {p_value2}.",
        )

        tol = 1e-8
        self.assertTrue(
            null_lo2 <= tol and null_hi2 >= -tol,
            f"Null interval should include 0 within tolerance. Got [{null_lo2}, {null_hi2}].",
        )


        csv_cases = [
            {
                "name": "temp_change",
                "file": TEMP_FILE,
                "x_col": "year",
                "y_col": "temperature_change",
                "a": 0.026541317969067967,
                "p": 0.0,
                "lo": -0.006907482412494906,
                "hi": 0.006849227508140011,
            },
            {
                "name": "indoor_temps",
                "file": INDOOR_FILE,
                "x_col": "year",
                "y_col": "temperature_change",
                "a": 0.017404150197628494,
                "p": 0.7066666666666667,
                "lo": -0.08198292984189735,
                "hi": 0.08262880434782614,
            },
            {
                "name": "disasters",
                "file": DISASTERS_FILE,
                "x_col": "year",
                "y_col": "num_disasters",
                "a": 6.2267457180500685,
                "p": 0.0,
                "lo": -2.28977602108037,
                "hi": 2.1237845849802355,
            },
        ]

        for case in csv_cases:
            random.seed(6100)
            df = pd.read_csv(case["file"])

            x = list(df[case["x_col"]])
            y = list(df[case["y_col"]])

            a_obs, p_value, null_lo, null_hi = fn(
                x,
                y,
                n_permutations=300,
            )

            # basic sanity
            for val in [a_obs, p_value, null_lo, null_hi]:
                self.assertIsInstance(val, (int, float, np.number))

            self.assertLess(null_lo, null_hi)
            self.assertTrue(0.0 <= p_value <= 1.0)

            self.assertAlmostEqual(a_obs,
                                    case["a"],
                                    places=2,
                                    msg=f"{case['name']}: observed slope a is incorrect: expected {case['a']}, got {a_obs}.")
            self.assertAlmostEqual(p_value,
                                    case["p"],
                                    delta=0.02,
                                    msg=f"{case['name']}: p_value is incorrect: expected {case['p']}, got {p_value}.")
            self.assertAlmostEqual(null_lo,
                                    case["lo"],
                                    delta=0.6,
                                    msg=f"{case['name']}: null interval lower bound is incorrect: expected {case['lo']}, got {null_lo}.")
            self.assertAlmostEqual(null_hi,
                                    case["hi"],
                                    delta=0.5,
                                    msg=f"{case['name']}: null interval upper bound is incorrect: expected {case['hi']}, got {null_hi}.")


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
        TestRegression,
        TestPermute,
        TestTrainValidateSplit,
        TestKFoldCrossValidation,
        TestComparePolyDegrees,
        TestPermutationTrend,
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
