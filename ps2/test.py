# standard library
from functools import wraps
import json
import os
import unittest
from unittest.mock import MagicMock, patch
from collections import OrderedDict
import random

# local application
import pset


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
# set up test case examples
############################################################


ACCEPTABLE_EPSILON = 1e-4

SCENARIO_1 = OrderedDict({
    "stations": [5, 6, 8],
    'p': 0.2,
    'sigma': 0.1,
    'num_steps_ideal': 16,
    'num_steps_realistic': 100,
    'num_trials': 50,
    'history': [ # for ideal sim
        [5, 6, 8],
        [5, 6, 8],
        [5, 6, 8],
        [5, 6, 10],
        [5, 8, 12],
        [6, 8, 14],
        [6, 8, 0],
        [6, 10, 2],
        [8, 12, 4],
        [8, 14, 5],
        [8, 0, 5],
        [10, 2, 5],
        [12, 4, 6],
        [14, 4, 6],
        [0, 4, 6],
        [2, 4, 8],
        [2, 5, 8],
    ]
})

SCENARIO_2 = OrderedDict({
    "stations": [0, 1.3, 7.1, 11.5],
    'p': 0.5,
    'sigma': 0.8,
    'num_steps_ideal': 16,
    'num_steps_realistic': 150,
    'num_trials': 100,
    'history': [ # for ideal sim
        [0, 1.3, 7.1, 11.5],
        [0, 1.3, 7.1, 11.5],
        [0, 1.3, 7.1, 11.5],
        [0, 3.3, 9.1, 13.5],
        [1.3, 5.3, 11.1, 15.5],
        [1.3, 7.1, 11.5, 15.5],
        [1.3, 7.1, 11.5, 15.5],
        [3.3, 7.1, 11.5, 15.5],
        [5.3, 9.1, 13.5, 0],
        [7.1, 11.1, 15.5, 0],
        [7.1, 11.5, 15.5, 0],
        [7.1, 11.5, 15.5, 1.3],
        [9.1, 11.5, 15.5, 1.3],
        [11.1, 13.5, 15.5, 1.3],
        [11.5, 13.5, 15.5, 3.3],
        [11.5, 13.5, 0, 5.3],
        [11.5, 15.5, 0, 7.1],
    ],
})


############################################################
# test get distance
############################################################

@testsuite_options(4, 1)
class TestGetDistance(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="get_distance() does not return the correct modular distance",
        error="get_distance() raised an error"
    )
    def test_get_distance(self):
        location_1_list = [12, 3, 5.1]
        location_2_list = [2, 5, 5]
        expected_distance = [6, 2, 15.9]

        for l1, l2, expected_distance in zip(location_1_list, location_2_list, expected_distance):
            actual_distance = pset.get_distance(l1, l2)
            self.assertAlmostEqual(
                expected_distance,
                actual_distance,
                delta=ACCEPTABLE_EPSILON,
                msg=f"got get_distance({l1}, {l2}) = {actual_distance}, expected {expected_distance}"
            )


############################################################
# test step train
############################################################


@testsuite_options(4, 1)
class TestStepTrain(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        2,
        failure="step_train() does not return the correct train state",
        error="step_train() raised an error"
    )
    def test_step_train_1(self):
        station_locs = [1, 4, 5]
        train_locs = [5, 7, 15]

        for idx in range(len(train_locs)):
            idle_time = [0, 1, 0]
            actual_loc = pset.step_train(idx, train_locs, idle_time, station_locs, 2)
            expected_locs = [5, 7, 1]
            expected_idle_time = [[0, 1, 0], [0, 0, 0], [0, 1, 2]]
            self.assertEqual(
                expected_locs[idx],
                actual_loc,
                f"got step_train({idx}, {train_locs}, {idle_time}, {station_locs}, {2})"
                + f" location = {actual_loc}, expected location {expected_locs[idx]}"
            )
            self.assertEqual(
                expected_idle_time[idx],
                idle_time,
                f"got step_train({idx}, {train_locs}, {idle_time}, {station_locs}, {2})"
                + f" idle_time = {idle_time}, expected location {expected_idle_time[idx]}"
            )

    @case_options(
        2,
        failure="step_train() does not return the correct train state",
        error="step_train() raised an error"
    )
    def test_step_train_2(self):
        station_locs = [0, 8, 9]
        train_locs = [15, 7, 9]

        for idx in range(len(train_locs)):
            idle_time = [0, 0, 2]
            actual_loc = pset.step_train(idx, train_locs, idle_time, station_locs, 2)
            expected_locs = [0, 7, 9]
            expected_idle_time = [[2, 0, 2], [0, 0, 2], [0, 0, 1]]
            self.assertEqual(
                expected_locs[idx],
                actual_loc,
                f"got step_train({idx}, {train_locs}, {idle_time}, {station_locs}, {2})"
                + f" location = {actual_loc}, expected location {expected_locs[idx]}"
            )
            self.assertEqual(
                expected_idle_time[idx],
                idle_time,
                f"got step_train({idx}, {train_locs}, {idle_time}, {station_locs}, {2})"
                + f" idle_time = {idle_time}, expected location {expected_idle_time[idx]}"
            )


############################################################
# test step simulation
############################################################


@testsuite_options(4, 1)
class TestStepSimulation(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        2,
        failure="step_simulation() does not return the correct train states",
        error="step_simulation() raised an error"
    )
    def test_step_simulation(self):
        station_locs = [1, 4, 5]
        train_locs = [5, 7, 15]
        idle_time = [0, 1, 0]
        actual_locations = pset.step_simulation(train_locs, station_locs, idle_time)
        expected_locations = [5, 7, 1]
        expected_idle_time = [0, 0, 2]
        self.assertEqual(expected_locations, actual_locations, f"got step_simulation({train_locs}, {station_locs}, {idle_time}) location = {actual_locations}, expected location {expected_locations}")
        self.assertEqual(expected_idle_time, idle_time, f"got gtep_simulation({train_locs}, {station_locs}, {idle_time}) idle_time = {idle_time}, expected location {expected_idle_time}")


############################################################
# test simulate trains
############################################################


class TestSimulationBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # helper function for comparing histories
    def assertHistoryEqual(self, expected: list[list], actual: list[list]):
        self.assertEqual(len(expected), len(actual), f"History lengths differ in number of steps, expected {len(expected)}, got {len(actual)}")
        for t, (exp_train_locations, actual_train_locations) in enumerate(zip(expected, actual)):
            self.assertEqual(
                len(exp_train_locations),
                len(actual_train_locations),
                f"History lengths differ in number of trains at time step {t}. Expected {len(exp_train_locations)}, got {len(actual_train_locations)}",
            )
            for i, (loc_expected, loc_actual) in enumerate(zip(exp_train_locations, actual_train_locations)):
                self.assertAlmostEqual(
                    loc_expected,
                    loc_actual,
                    delta=ACCEPTABLE_EPSILON,
                    msg=f"Train locations differ at step {t}, train {i}. Expected {loc_expected}, got {loc_actual}",
                )

@testsuite_options(4, 1)
class TestSimulateTrains(TestSimulationBase):

    @case_options(
        1,
        failure="simulate_trains() does not return the correct location history",
        error="simulate_trains() raised an error"
    )
    def test_simulate_trains_1(self):
        stations, p, sigma, num_steps_ideal, num_steps_realistic, num_trials, history = SCENARIO_1.values()
        expected = history
        actual = pset.simulate_trains(stations, num_steps_ideal)
        self.assertHistoryEqual(expected, actual)

    @case_options(
        1,
        failure="simulate_trains() does not return the correct location history",
        error="simulate_trains() raised an error"
    )
    def test_simulate_trains_2(self):
        stations, p, sigma, num_steps_ideal, num_steps_realistic, num_trials, history = SCENARIO_2.values()
        expected = history
        actual = pset.simulate_trains(stations, num_steps_ideal)
        self.assertHistoryEqual(expected, actual)


############################################################
# test station wait times
############################################################


@testsuite_options(4, 1)
class TestStationWaitTimes(unittest.TestCase):

    @case_options(
        2,
        failure="station_wait_times() does not return the correct wait times",
        error="station_wait_times() raised an error"
    )
    def test_station_wait_times_1(self):
        station = 8
        expected = [2, 2, 5]
        actual = pset.station_wait_times(SCENARIO_1['history'], station)
        self.assertEqual(
            expected,
            sorted(actual),
            f"Station at location {station} expected wait times {expected}, got {actual}"
        )

    @case_options(
        2,
        failure="station_wait_times() does not return the correct wait times",
        error="station_wait_times() raised an error"
    )
    def test_station_wait_times_2(self):
        station = 7.1
        expected = [2, 3, 5]
        actual = pset.station_wait_times(SCENARIO_2["history"], station)
        self.assertEqual(
            expected,
            sorted(actual),
            f"Station at location {station} expected wait times {expected}, got {actual}"
        )


############################################################
# test collect all wait times
############################################################


@testsuite_options(4, 1)
class TestCollectAllWaitTimes(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @case_options(
        1,
        failure="collect_all_wait_times() does not return the correct wait times",
        error="collect_all_wait_times() raised an error"
    )
    def test_collect_all_wait_times_1(self):
        expected = sorted([5, 5] + [2, 5] + [2, 2, 5])
        actual = pset.collect_all_wait_times(SCENARIO_1["history"], SCENARIO_1["stations"])
        self.assertEqual(
            expected,
            sorted(actual),
            f"Expected wait times {expected}, got {actual}"
        )

    @case_options(
        1,
        failure="collect_all_wait_times() does not return the correct wait times",
        error="collect_all_wait_times() raised an error"
    )
    def test_collect_all_wait_times_2(self):
        expected = sorted([5, 5] + [2, 5] + [2, 3, 5] + [2, 3, 3])
        actual = pset.collect_all_wait_times(SCENARIO_2["history"], SCENARIO_2["stations"])
        self.assertEqual(
            expected,
            sorted(actual),
            f"Expected wait times {expected}, got {actual}"
        )


############################################################
# test run monte carlo
############################################################


# NOTE: only exists to confirm realistic changes were done appropriately
@testsuite_options(4, 1)
class TestSimulationRealistic(TestSimulationBase):

    @case_options(
        1,
        failure="simulate_trains() does not return the correct location history (apply_none)",
        error="simulate_trains() raised an error (section 4)"
    )
    def test_apply_none_1(self):
        stations, p, sigma, num_steps_ideal, num_steps_realistic, num_trials, history = SCENARIO_1.values()
        expected = history
        actual = pset.simulate_trains(stations, num_steps_ideal, pset.apply_none, None)
        self.assertHistoryEqual(expected, actual)

    @case_options(
        1,
        failure="simulate_trains() does not return the correct location history (apply_none)",
        error="simulate_trains() raised an error (section 4)"
    )
    def test_apply_none_2(self):
        stations, p, sigma, num_steps_ideal, num_steps_realistic, num_trials, history = SCENARIO_2.values()
        expected = history
        actual = pset.simulate_trains(stations, num_steps_ideal, pset.apply_none, None)
        self.assertHistoryEqual(expected, actual)


class TestMonteCarloBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def assertAcceptableRange(self, expected_mean, stdev, actual_mean):
        num_stdevs = 2
        self.assertLess(
            abs(expected_mean - actual_mean),
            num_stdevs * stdev,
            f"Mean {actual_mean} is not within {num_stdevs} standard deviations"
            + f" of expected mean {expected_mean} (stdev: {stdev})"
        )


@testsuite_options(8, 1)
class TestMonteCarloHalting(TestMonteCarloBase):
    @case_options(
        1,
        failure="run_monte_carlo() with halting does not return the correct mean",
        error="run_monte_carlo() with halting raised an error"
    )
    def test_run_monte_carlo_halting_1(self):
        stations, p, _, _, num_steps_realistic, num_trials, _ = SCENARIO_1.values()
        random.seed(2)

        expected_mean, expected_stdev = 5.301971522666003, 0.22892637078919367
        mean, _, _ = pset.run_monte_carlo(
            stations,
            num_steps_realistic,
            pset.apply_halt,
            p,
            num_trials,
        )

        self.assertAcceptableRange(expected_mean, expected_stdev, mean)

    @case_options(
        1,
        failure="run_monte_carlo() with halting does not return the correct mean",
        error="run_monte_carlo() with halting raised an error"
    )
    def test_run_monte_carlo_halting_2(self):
        stations, p, _, _, num_steps_realistic, num_trials, _ = SCENARIO_2.values()
        random.seed(2)

        expected_mean, expected_stdev = 6.569137740262204, 0.370118123196888
        mean, _, _ = pset.run_monte_carlo(
            stations,
            num_steps_realistic,
            pset.apply_halt,
            p,
            num_trials,
        )

        self.assertAcceptableRange(expected_mean, expected_stdev, mean)


@testsuite_options(8, 1)
class TestMonteCarloUniform(TestMonteCarloBase):
    @case_options(
        1,
        failure="run_monte_carlo() with uniform does not return the correct mean",
        error="run_monte_carlo() with uniform raised an error"
    )
    def test_run_monte_carlo_uniform_1(self):
        stations, _, _, _, num_steps_realistic, num_trials, _ = SCENARIO_1.values()
        random.seed(2)

        expected_mean, expected_stdev = 6.392898856266503, 0.3075805200648147
        mean, _, _ = pset.run_monte_carlo(
            stations,
            num_steps_realistic,
            pset.apply_uniform_slow,
            None,
            num_trials,
        )

        self.assertAcceptableRange(expected_mean, expected_stdev, mean)

    @case_options(
        1,
        failure="run_monte_carlo() with uniform does not return the correct mean",
        error="run_monte_carlo() with uniform raised an error"
    )
    def test_run_monte_carlo_uniform_2(self):
        stations, _, _, _, num_steps_realistic, num_trials, _ = SCENARIO_2.values()
        random.seed(2)

        expected_mean, expected_stdev = 5.037926035001541, 0.19782576570167382
        mean, _, _ = pset.run_monte_carlo(
            stations,
            num_steps_realistic,
            pset.apply_uniform_slow,
            None,
            num_trials,
        )

        self.assertAcceptableRange(expected_mean, expected_stdev, mean)


@testsuite_options(8, 1)
class TestMonteCarloGaussian(TestMonteCarloBase):
    @case_options(
        1,
        failure="run_monte_carlo() with gaussian does not return the correct mean",
        error="run_monte_carlo() with gaussian raised an error"
    )
    def test_run_monte_carlo_gaussian_1(self):
        stations, _, sigma, _, num_steps_realistic, num_trials, _ = SCENARIO_1.values()
        random.seed(2)

        expected_mean, expected_stdev = 5.8413107995213265, 0.16200157910100907
        mean, _, _ = pset.run_monte_carlo(
            stations,
            num_steps_realistic,
            pset.apply_gaussian_slow,
            sigma,
            num_trials,
        )

        self.assertAcceptableRange(expected_mean, expected_stdev, mean)

    @case_options(
        1,
        failure="run_monte_carlo() with gaussian does not return the correct mean",
        error="run_monte_carlo() with gaussian raised an error"
    )
    def test_run_monte_carlo_gaussian_2(self):
        stations, _, sigma, _, num_steps_realistic, num_trials, _ = SCENARIO_2.values()
        random.seed(2)

        expected_mean, expected_stdev = 5.087072653851683, 0.21105442048169784
        mean, _, _ = pset.run_monte_carlo(
            stations,
            num_steps_realistic,
            pset.apply_gaussian_slow,
            sigma,
            num_trials,
        )

        self.assertAcceptableRange(expected_mean, expected_stdev, mean)


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
        TestGetDistance,
        TestStepTrain,
        TestStepSimulation,
        TestSimulateTrains,

        TestStationWaitTimes,
        TestCollectAllWaitTimes,

        TestSimulationRealistic,
        TestMonteCarloHalting,
        TestMonteCarloUniform,
        TestMonteCarloGaussian,
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
