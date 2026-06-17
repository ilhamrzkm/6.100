from functools import wraps
import unittest
from unittest.mock import patch

import pset


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
# test person
############################################################


@testsuite_options(4, 1)
class TestPerson(unittest.TestCase):

    @case_options(
        1,
        "Person.move is not implemented correctly",
        "Error occurred while testing Person.move",
    )
    def test_person_01_move(self):
        # check that move returns a unit step
        person = pset.Person()
        with patch.object(
            pset.random,
            "uniform",
            return_value=pset.math.pi / 2,
        ), patch.object(
            pset.random,
            "random",
            return_value=0.25,
        ):
            dx, dy = person.move(None)
        self.assertAlmostEqual(dx, 0)
        self.assertAlmostEqual(dy, 1)

    @case_options(
        1,
        "Person.update_health is not implemented correctly",
        "Error occurred while testing Person.update_health",
    )
    def test_person_02_update_health(self):
        # check that update_health changes infected and alive flags
        person = pset.Person()
        person.update_health(True, False)
        self.assertTrue(person.is_infected())
        self.assertFalse(person.is_alive())

    @case_options(
        1,
        "Person.is_infected and Person.is_alive are not implemented correctly",
        "Error occurred while testing Person.is_infected and Person.is_alive",
    )
    def test_person_03_health_accessors(self):
        # check that health status comes back in the expected format
        person = pset.Person()
        person.update_health(True, True)
        self.assertTrue(person.is_infected())
        self.assertTrue(person.is_alive())

    @case_options(
        1,
        "Person.move is not implemented correctly for dead people",
        "Error occurred while testing Person.move on a dead person",
    )
    def test_person_04_dead_person_does_not_move(self):
        person = pset.Person()
        person.update_health(False, False)
        self.assertEqual(person.move(None), (0, 0))


############################################################
# test simulation init/reset
############################################################


@testsuite_options(4, 1)
class TestSimulationInitReset(unittest.TestCase):

    def make_sim(self, **overrides):
        params = {
            "starting_infection_prob": 0,
            "infection_prob": 0,
            "recovery_prob": 0,
            "death_prob": 0,
            "infection_radius": 5,
        }
        params.update(overrides)
        return pset.DiseaseSimulation(params, {pset.Person: 2}, width=10, height=10)

    @case_options(
        1,
        "Simulation.reset is not implemented correctly",
        "Error occurred while testing Simulation.reset",
    )
    def test_initreset_01_reset(self):
        # check reset builds people, locations, and starting infections
        created = []
        original_init = pset.Person.__init__

        def record_init(person, *args, **kwargs):
            original_init(person, *args, **kwargs)
            created.append(person)

        sim = pset.DiseaseSimulation(
            {
                "starting_infection_prob": 1,
                "infection_prob": 0,
                "recovery_prob": 0,
                "death_prob": 0,
                "infection_radius": 5,
            },
            {pset.Person: 2},
            width=10,
            height=10,
        )

        with patch.object(pset.Person, "__init__", record_init), patch.object(
            pset.random, "random", return_value=0
        ), patch.object(
            pset.random, "uniform", return_value=0
        ), patch.object(pset.random, "randint", return_value=0):
            sim.reset()

        self.assertEqual(len(created), 2)
        self.assertEqual(len(sim.people_locs), 2)
        for person in created:
            x, y = sim.people_locs[person]
            self.assertTrue(0 <= x <= 10)
            self.assertTrue(0 <= y <= 10)
            self.assertTrue(person.is_infected())
            self.assertTrue(person.is_alive())

    @case_options(
        1,
        "Simulation.reset should create the right number of people",
        "Error occurred while testing person counts in Simulation.reset",
    )
    def test_initreset_02_reset_people_count(self):
        created = []
        original_init = pset.Person.__init__

        def record_init(person, *args, **kwargs):
            original_init(person, *args, **kwargs)
            created.append(person)

        sim = pset.DiseaseSimulation(
            {
                "starting_infection_prob": 0,
                "infection_prob": 0,
                "recovery_prob": 0,
                "death_prob": 0,
                "infection_radius": 5,
            },
            {pset.Person: 3},
            width=10,
            height=10,
        )
        with patch.object(pset.Person, "__init__", record_init), patch.object(
            pset.random, "random", return_value=1
        ), patch.object(
            pset.random, "uniform", return_value=0
        ), patch.object(pset.random, "randint", return_value=0):
            sim.reset()

        self.assertEqual(len(created), 3)
        self.assertEqual(len(set(created)), 3)
        self.assertEqual(len(sim.people_locs), 3)
        for person in created:
            x, y = sim.people_locs[person]
            self.assertTrue(0 <= x <= 10)
            self.assertTrue(0 <= y <= 10)
            self.assertFalse(person.is_infected())
            self.assertTrue(person.is_alive())


############################################################
# test simulation observation
############################################################


@testsuite_options(4, 1)
class TestSimulationObservation(unittest.TestCase):

    def make_sim(self, **overrides):
        params = {
            "starting_infection_prob": 0,
            "infection_prob": 0,
            "recovery_prob": 0,
            "death_prob": 0,
            "infection_radius": 5,
        }
        params.update(overrides)
        return pset.DiseaseSimulation(params, {pset.Person: 2}, width=10, height=10)

    def make_sim_with_locs(self, locations, **overrides):
        # set locations directly so random order does not matter
        params = {
            "starting_infection_prob": 0,
            "infection_prob": 0,
            "recovery_prob": 0,
            "death_prob": 0,
            "infection_radius": 5,
        }
        params.update(overrides)
        sim = pset.DiseaseSimulation(
            params,
            {pset.Person: len(locations)},
            width=10,
            height=10,
        )
        people = [pset.Person() for _ in locations]
        sim.people_locs = dict(zip(people, locations))
        return sim, people

    @case_options(
        1,
        "find_distance is not implemented correctly",
        "Error occurred while testing find_distance",
    )
    def test_obs_01_find_distance(self):
        self.assertEqual(pset.find_distance((0, 0), (3, 4)), 5)

    @case_options(
        1,
        "Simulation.generate_observation is not implemented correctly",
        "Error occurred while testing Simulation.generate_observation",
    )
    def test_obs_02_generate_observation(self):
        sim, people = self.make_sim_with_locs([(0, 0), (3, 3), (10, 10)])
        a, b, _ = people

        self.assertEqual(sim.generate_observation(a), {b: (3, 3)})

    @case_options(
        1,
        "Simulation.generate_observation should use relative displacements",
        "Error occurred while testing non-origin observations",
    )
    def test_obs_03_generate_observation_non_origin(self):
        sim, people = self.make_sim_with_locs([(5, 5), (7, 8), (10, 10)])
        a, b, _ = people

        self.assertEqual(sim.generate_observation(a), {b: (2, 3)})


############################################################
# test simulation health
############################################################


@testsuite_options(4, 1)
class TestSimulationHealth(unittest.TestCase):

    def make_sim(self, **overrides):
        params = {
            "starting_infection_prob": 0,
            "infection_prob": 0,
            "recovery_prob": 0,
            "death_prob": 0,
            "infection_radius": 5,
        }
        params.update(overrides)
        return pset.DiseaseSimulation(params, {pset.Person: 2}, width=10, height=10)

    @case_options(
        1,
        "Simulation.evolve_health should infect people correctly",
        "Error occurred while testing infection updates in Simulation.evolve_health",
    )
    def test_health_01_evolve_health_infects(self):
        # check that a healthy person can get infected from infected neighbors
        sim = self.make_sim(infection_prob=1)
        healthy = pset.Person()
        sick = pset.Person()
        sick.update_health(True, True)
        obs = {sick: (1, 1)}
        self.assertEqual(sim.evolve_health(healthy, obs), (True, True))
        self.assertFalse(healthy.is_infected())
        self.assertTrue(healthy.is_alive())

    @case_options(
        1,
        "Simulation.evolve_health should leave healthy people unchanged when no infected neighbor can infect them",
        "Error occurred while testing unchanged healthy updates in Simulation.evolve_health",
    )
    def test_health_02_evolve_health_stays_healthy(self):
        sim = self.make_sim(infection_prob=1)
        healthy = pset.Person()
        other_healthy = pset.Person()
        obs = {other_healthy: (1, 1)}

        self.assertEqual(sim.evolve_health(healthy, obs), (False, True))
        self.assertFalse(healthy.is_infected())
        self.assertTrue(healthy.is_alive())

    @case_options(
        1,
        "Simulation.evolve_health should recover people correctly",
        "Error occurred while testing recovery updates in Simulation.evolve_health",
    )
    def test_health_03_evolve_health_recovers(self):
        # check that an infected person can recover when recovery happens
        sim = self.make_sim(recovery_prob=1, death_prob=0)
        sick = pset.Person()
        sick.update_health(True, True)
        self.assertEqual(sim.evolve_health(sick, {}), (False, True))
        self.assertTrue(sick.is_infected())
        self.assertTrue(sick.is_alive())

    @case_options(
        1,
        "Simulation.evolve_health should handle deaths correctly",
        "Error occurred while testing death updates in Simulation.evolve_health",
    )
    def test_health_04_evolve_health_dies(self):
        # check that an infected person can die when death happens
        sim = self.make_sim(recovery_prob=0, death_prob=1)
        sick = pset.Person()
        sick.update_health(True, True)
        self.assertEqual(sim.evolve_health(sick, {}), (False, False))
        self.assertTrue(sick.is_infected())
        self.assertTrue(sick.is_alive())

    @case_options(
        1,
        "Simulation.evolve_health should keep infected people infected when they neither recover nor die",
        "Error occurred while testing unchanged infected updates in Simulation.evolve_health",
    )
    def test_health_05_evolve_health_stays_infected(self):
        sim = self.make_sim(recovery_prob=0, death_prob=0)
        sick = pset.Person()
        sick.update_health(True, True)
        self.assertEqual(sim.evolve_health(sick, {}), (True, True))
        self.assertTrue(sick.is_infected())
        self.assertTrue(sick.is_alive())

    @case_options(
        1,
        "Simulation.evolve_health should leave dead people dead and uninfected",
        "Error occurred while testing dead-person updates in Simulation.evolve_health",
    )
    def test_health_06_evolve_health_dead_person(self):
        sim = self.make_sim(infection_prob=1, recovery_prob=1, death_prob=1)
        dead = pset.Person()
        dead.update_health(False, False)
        neighbor = pset.Person()
        neighbor.update_health(True, True)

        self.assertEqual(
            sim.evolve_health(dead, {neighbor: (1, 1)}), (False, False)
        )
        self.assertFalse(dead.is_infected())
        self.assertFalse(dead.is_alive())


############################################################
# test simulation step/stats
############################################################


@testsuite_options(4, 1)
class TestSimulationStepStats(unittest.TestCase):

    def make_sim(self, **overrides):
        params = {
            "starting_infection_prob": 0,
            "infection_prob": 0,
            "recovery_prob": 0,
            "death_prob": 0,
            "infection_radius": 5,
        }
        params.update(overrides)
        return pset.DiseaseSimulation(params, {pset.Person: 2}, width=10, height=10)

    def make_sim_with_locs(self, locations, **overrides):
        # set locations directly so random order does not matter
        params = {
            "starting_infection_prob": 0,
            "infection_prob": 0,
            "recovery_prob": 0,
            "death_prob": 0,
            "infection_radius": 5,
        }
        params.update(overrides)
        sim = pset.DiseaseSimulation(
            params,
            {pset.Person: len(locations)},
            width=10,
            height=10,
        )
        people = [pset.Person() for _ in locations]
        sim.people_locs = dict(zip(people, locations))
        return sim, people

    @case_options(
        1,
        "Simulation.step is not implemented correctly",
        "Error occurred while testing Simulation.step",
    )
    def test_stepstats_01_step(self):
        # check that one step updates health and moves people
        sim, people = self.make_sim_with_locs(
            [(0, 0), (1, 1)],
            infection_prob=1,
        )
        healthy, sick = people
        sick.update_health(True, True)

        with patch.object(healthy, "move", return_value=(2, 3)), patch.object(
            sick, "move", return_value=(2, 3)
        ):
            sim.step()

        self.assertTrue(healthy.is_infected())
        self.assertTrue(healthy.is_alive())
        stats, _, _ = sim.get_stats()
        self.assertEqual(stats[healthy]["location"], (2, 3))
        self.assertEqual(stats[sick]["location"], (3, 4))

    @case_options(
        1,
        "Simulation.step should apply updates simultaneously instead of mutating mid-step",
        "Error occurred while testing simultaneous updates in Simulation.step",
    )
    def test_stepstats_02_step_uses_previous_state_for_all_people(self):
        sim, people = self.make_sim_with_locs(
            [(0, 0), (1, 0), (3, 0)],
            infection_prob=1,
            infection_radius=1.5,
        )
        a, b, c = people
        b.update_health(True, True)

        with patch.object(a, "move", return_value=(0, 0)), patch.object(
            b, "move", return_value=(0, 0)
        ), patch.object(c, "move", return_value=(0, 0)):
            sim.step()

        self.assertTrue(a.is_infected())
        self.assertTrue(a.is_alive())
        self.assertTrue(b.is_infected())
        self.assertTrue(b.is_alive())
        self.assertFalse(c.is_infected())
        self.assertTrue(c.is_alive())

    @case_options(
        1,
        "Simulation.step should keep people inside the simulation bounds",
        "Error occurred while testing boundary handling in Simulation.step",
    )
    def test_stepstats_03_step_keeps_people_in_bounds(self):
        sim, people = self.make_sim_with_locs([(0, 0), (10, 10)])
        a, b = people

        with patch.object(a, "move", return_value=(-5, -5)), patch.object(
            b, "move", return_value=(5, 5)
        ):
            sim.step()

        stats, _, _ = sim.get_stats()
        self.assertEqual(stats[a]["location"], (0, 0))
        self.assertEqual(stats[b]["location"], (10, 10))

    @case_options(
        1,
        "Simulation.get_stats is not implemented correctly",
        "Error occurred while testing Simulation.get_stats",
    )
    def test_stepstats_04_get_stats(self):
        sim, people = self.make_sim_with_locs([(1, 2), (3, 4)])
        a, b = people
        a.update_health(True, True)
        b.update_health(False, False)

        stats, num_infected, num_alive = sim.get_stats()

        self.assertEqual(
            stats[a],
            {"location": (1, 2), "infected": True, "alive": True},
        )
        self.assertEqual(
            stats[b],
            {"location": (3, 4), "infected": False, "alive": False},
        )
        self.assertEqual(num_infected, 1)
        self.assertEqual(num_alive, 1)


############################################################
# test different persons
############################################################


@testsuite_options(4, 1)
class TestDifferentPersons(unittest.TestCase):

    @case_options(
        1,
        "find_nearest_neighbor should return the closest filtered neighbor or None for an empty list",
        "Error occurred while testing find_nearest_neighbor",
    )
    def test_diff_01_find_nearest_neighbor(self):
        near_neighbor = pset.Person()
        far_neighbor = pset.Person()
        excluded_neighbor = pset.Person()
        observation = {
            near_neighbor: (3, 4),
            far_neighbor: (6, 8),
            excluded_neighbor: (1, 1),
        }

        self.assertIs(
            pset.find_nearest_neighbor(observation, [near_neighbor, far_neighbor]),
            near_neighbor,
        )
        self.assertIsNone(pset.find_nearest_neighbor(observation, []))

    @case_options(
        1,
        "move_towards_neighbor should move toward a target and stay still at zero distance",
        "Error occurred while testing move_towards_neighbor",
    )
    def test_diff_02_move_towards_neighbor(self):
        neighbor = pset.Person()
        observation = {neighbor: (3, 4)}

        dx, dy = pset.move_towards_neighbor(observation, neighbor)

        self.assertAlmostEqual(dx, 3 / 5)
        self.assertAlmostEqual(dy, 4 / 5)

        same_location_neighbor = pset.Person()
        same_location_observation = {same_location_neighbor: (0, 0)}
        self.assertEqual(
            pset.move_towards_neighbor(
                same_location_observation,
                same_location_neighbor,
            ),
            (0, 0),
        )

    @case_options(
        1,
        "CarefulPerson should inherit from Person and move away from infected neighbors when healthy",
        "Error occurred while testing healthy CarefulPerson behavior",
    )
    def test_diff_03_careful_person_move_healthy(self):
        self.assertTrue(issubclass(pset.CarefulPerson, pset.Person))

        person = pset.CarefulPerson()
        infected_neighbor = pset.Person()
        infected_neighbor.update_health(True, True)

        dx, dy = person.move({infected_neighbor: (3, 4)})
        self.assertAlmostEqual(dx, -3 / 5)
        self.assertAlmostEqual(dy, -4 / 5)

    @case_options(
        1,
        "CarefulPerson should move away from healthy neighbors when infected",
        "Error occurred while testing infected CarefulPerson behavior",
    )
    def test_diff_04_careful_person_move_infected(self):
        person = pset.CarefulPerson()
        person.update_health(True, True)
        healthy_neighbor = pset.Person()
        healthy_neighbor.update_health(False, True)

        dx, dy = person.move({healthy_neighbor: (3, 4)})
        self.assertAlmostEqual(dx, -3 / 5)
        self.assertAlmostEqual(dy, -4 / 5)

    @case_options(
        1,
        "MoreMenacingPerson should move toward the average location of up to 5 nearest healthy neighbors when infected",
        "Error occurred while testing MoreMenacingPerson behavior",
    )
    def test_diff_05_more_menacing_person_move(self):
        self.assertTrue(issubclass(pset.MoreMenacingPerson, pset.MenacingPerson))

        person = pset.MoreMenacingPerson()
        person.update_health(True, True)
        healthy_people = [pset.Person() for _ in range(6)]
        for healthy in healthy_people:
            healthy.update_health(False, True)
        neighbor_locs = {
            healthy_people[0]: (3, 4),
            healthy_people[1]: (0, 6),
            healthy_people[2]: (8, 0),
            healthy_people[3]: (0, 8),
            healthy_people[4]: (6, 8),
            healthy_people[5]: (100, 100),
        }

        dx, dy = person.move(neighbor_locs)

        target_x = (3 + 0 + 8 + 0 + 6) / 5
        target_y = (4 + 6 + 0 + 8 + 8) / 5
        distance = pset.find_distance((0, 0), (target_x, target_y))
        self.assertAlmostEqual(dx, target_x / distance)
        self.assertAlmostEqual(dy, target_y / distance)


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
        TestPerson,
        TestSimulationInitReset,
        TestSimulationObservation,
        TestSimulationHealth,
        TestSimulationStepStats,
        TestDifferentPersons,
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
