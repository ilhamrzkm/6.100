"""
6.100 Spring 2026
Problem Set 7

Please fill out the following info:
Name:
Kerberos:
Approximate time spent (HH:MM):
"""

import random
import math
from visualization import DiseaseSimVisualizer, plot_population_status


############################################################
# person
############################################################


class Person:
    """An abstract class for a person in a disease simulation."""

    def __init__(self, infected=False, alive=True):
        raise NotImplementedError

    def move(self, observation):
        """
        Return the delta (dx, dy) of the person's move.
        The person moves in a random direction in the unit circle.
        """
        raise NotImplementedError

    def update_health(self, infected=False, alive=True):
        """
        Update the person's health status.

        Parameters:
            infected (bool): whether the person is infected
            alive (bool): whether the person is alive
        """
        raise NotImplementedError

    def is_infected(self):
        """
        Return a boolean representing if the person is infected.
        """
        raise NotImplementedError

    def is_alive(self):
        """
        Return a boolean representing if the person is alive.
        """
        raise NotImplementedError


############################################################
# helper functions
############################################################


def find_distance(loc1, loc2):
    """
    Return the euclidean distance between two (x, y) locations.
    """
    raise NotImplementedError


def find_nearest_neighbor(observation, neighbors):
    """
    Return the nearest neighbor from the list of neighbors.
    """
    raise NotImplementedError


def move_towards_neighbor(observation, neighbor):
    """
    Return the delta (dx, dy) of the person's move.
    The person moves towards the neighbor.
    """
    raise NotImplementedError


############################################################
# disease simulation
############################################################


class DiseaseSimulation:
    """A class representing a disease simulation environment."""

    def __init__(self, disease_params, people_counts, width, height):
        """
        Initialize the attributes of DiseaseSimulation

        Parameters:
            disease_params (dict) with the keys:
                "starting_infection_prob": the starting infection
                    probability
                "infection_prob": the probability of infection
                "recovery_prob": the probability of recovery
                "death_prob": the probability of death
                "infection_radius": the infection radius
            people_counts (dict) mapping type of Person to the number of
                that type
            width (int) representing the width of the simulation
            height (int) representing the height of the simulation
        """
        self.starting_infection_prob = disease_params["starting_infection_prob"]
        self.infection_prob = disease_params["infection_prob"]
        self.recovery_prob = disease_params["recovery_prob"]
        self.death_prob = disease_params["death_prob"]
        self.infection_radius = disease_params["infection_radius"]

        self.people_counts = people_counts.copy()
        self.people_locs = {}

        self.width = width
        self.height = height

    def run_simulation(self, num_steps):
        """Run the simulation for a specified number of steps."""
        self.reset()
        visualizer = DiseaseSimVisualizer(self, num_steps)
        visualizer.start()
        for t in range(num_steps):
            _, _, num_alive = self.get_stats()
            if num_alive == 0:
                break
            visualizer.draw(t)
            self.step()
        print(f"Simulation ended after {num_steps} steps.")
        visualizer.stop()

    def reset(self):
        """
        Reset the simulation to an initial state.

        Each person is placed randomly in the environment.
        Each person starts alive.
        Each person starts infected with probability
        starting_infected_prob.
        """
        raise NotImplementedError

    def generate_observation(self, person):
        """
        Find all neighboring people within the infection radius of the
        given person.

        Return a dictionary mapping neighbors to their displacement
        (dx, dy) from person.
        """
        raise NotImplementedError

    def evolve_health(self, person, observation):
        """
        Determine the health status of the given person based on the
        observation.
        Return the infection and alive status of the person as a tuple
        (infected, alive)
        DO NOT MUTATE THE PERSON
        """
        raise NotImplementedError

    def step(self):
        """
        Advance the simulation by one time step, updating all people and
        applying disease transmission rules.
        """
        raise NotImplementedError

    def get_stats(self):
        """
        Return:
            Return a tuple of the following:
            + A dict representing the state of the simulation, with the
              following mappings:
                "location": The person's current location as a tuple of floats.
                "infected": A bool indicating whether the person is infected.
                "alive": A bool indicating whether the person is alive.
            + An int indicating the number of people who are infected.
            + An int indicating the number of people who are alive.
        """
        raise NotImplementedError


############################################################
# different persons
############################################################


class MenacingPerson(Person):
    """A menacing person moves towards healthy people when infected."""

    def move(self, observation):
        """
        Move towards healthy nearest individual if infected, or move
        randomly if not infected.
        """
        raise NotImplementedError


class CarefulPerson(Person):
    """A careful person moves away from infected people when healthy,
    or away from healthy people when infected."""

    def move(self, observation):
        """
        If healthy, move away from nearest infected neighbor.
        If infected, move away from nearest healthy neighbor.
        Move randomly if none of these conditions are met.
        """
        raise NotImplementedError


class MoreMenacingPerson(MenacingPerson):
    """A more menacing person moves towards the K nearest healthy people when infected."""

    K = 5

    def move(self, observation):
        """
        If infected, move towards the average location of the K nearest
        healthy neighbors. Otherwise, move randomly.
        """
        raise NotImplementedError


############################################################
# different disease simulations
############################################################


class CovidSimulation(DiseaseSimulation):

    def __init__(self, people_counts, width, height):
        # Fill in disease_params from homework.md, then call super().__init__.
        raise NotImplementedError


class EbolaSimulation(DiseaseSimulation):

    def __init__(self, people_counts, width, height):
        # Fill in disease_params from homework.md, then call super().__init__.
        raise NotImplementedError


############################################################
# manual testing
############################################################


def manual_test_person():
    person = Person()

    print("Initial infected/alive:", person.is_infected(), person.is_alive())
    print("Alive move:", person.move(None))
    person.update_health(True, True)
    print("Infected and alive:", person.is_infected(), person.is_alive())
    person.update_health(False, False)
    print("Dead move:", person.move(None))  # expected: (0, 0)


def manual_test_reset_stats():
    disease_parameters = {
        "starting_infection_prob": 0.5,
        "infection_prob": 0,
        "recovery_prob": 0,
        "death_prob": 0,
        "infection_radius": 2,
    }
    simulation = DiseaseSimulation(disease_parameters, {Person: 3}, 10, 10)
    simulation.reset()

    stats, infected, alive = simulation.get_stats()
    print("People:", len(stats))  # expected: 3
    print("Infected:", infected)
    print("Alive:", alive)  # expected: 3


def manual_test_observation():
    disease_parameters = {
        "starting_infection_prob": 0,
        "infection_prob": 0,
        "recovery_prob": 0,
        "death_prob": 0,
        "infection_radius": 20,
    }
    simulation = DiseaseSimulation(disease_parameters, {Person: 3}, 10, 10)
    simulation.reset()

    stats, _, _ = simulation.get_stats()
    person = next(iter(stats))
    observation = simulation.generate_observation(person)

    print("Observation:", observation)
    try:
        print("Neighbors:", len(observation))  # expected: 2
    except Exception as e:
        print("Error accessing observation:", e)


def manual_test_evolve_health():
    sick = Person()
    healthy = Person()
    recovering = Person()
    dying = Person()
    dead = Person()
    sick.update_health(True, True)

    disease_parameters = {
        "starting_infection_prob": 0,
        "infection_prob": 1,
        "recovery_prob": 0,
        "death_prob": 0,
        "infection_radius": 2,
    }
    simulation = DiseaseSimulation(disease_parameters, {Person: 1}, 10, 10)
    print(
        "Healthy near sick:",
        simulation.evolve_health(healthy, {sick: (1, 1)}),
    )  # expected: (True, True)

    recovering.update_health(True, True)
    disease_parameters["infection_prob"] = 0
    disease_parameters["recovery_prob"] = 1
    simulation = DiseaseSimulation(disease_parameters, {Person: 1}, 10, 10)
    print(
        "Recovering:",
        simulation.evolve_health(recovering, {}),
    )  # expected: (False, True)

    dying.update_health(True, True)
    disease_parameters["recovery_prob"] = 0
    disease_parameters["death_prob"] = 1
    simulation = DiseaseSimulation(disease_parameters, {Person: 1}, 10, 10)
    print(
        "Dying:",
        simulation.evolve_health(dying, {}),
    )  # expected: (False, False)

    dead.update_health(False, False)
    print(
        "Already dead:",
        simulation.evolve_health(dead, {sick: (1, 1)}),
    )  # expected: (False, False)


def manual_test_step_stats():
    disease_parameters = {
        "starting_infection_prob": 0.5,
        "infection_prob": 1,
        "recovery_prob": 0,
        "death_prob": 0,
        "infection_radius": 2,
    }
    simulation = DiseaseSimulation(disease_parameters, {Person: 3}, 10, 10)
    simulation.reset()

    print("Before:", simulation.get_stats())
    simulation.step()
    print("After:", simulation.get_stats())


def manual_test_direction_helpers():
    neighbor = Person()
    observation = {neighbor: (3, 4)}

    print(
        "Toward neighbor:",
        move_towards_neighbor(observation, neighbor),
    )  # expected: close to (0.6, 0.8)

    menacing = MenacingPerson()
    menacing.update_health(True, True)
    print("Menacing:", menacing.move(observation))  # expected: close to (0.6, 0.8)

    careful = CarefulPerson()
    neighbor.update_health(True, True)
    print("Careful:", careful.move(observation))  # expected: close to (-0.6, -0.8)


def manual_test_more_menacing_neighbors():
    person = MoreMenacingPerson()
    person.update_health(True, True)
    neighbors = [Person() for _ in range(6)]
    observation = {
        neighbors[0]: (3, 4),
        neighbors[1]: (0, 6),
        neighbors[2]: (8, 0),
        neighbors[3]: (0, 8),
        neighbors[4]: (6, 8),
        neighbors[5]: (100, 100),
    }

    print("More menacing:", person.move(observation))
    # expected: moves toward the average of the five nearest neighbors


def manual_test_small():
    disease_parameters = {
        "starting_infection_prob": 0.5,
        "infection_prob": 0.9,
        "recovery_prob": 0.05,
        "death_prob": 0.01,
        "infection_radius": 2,
    }
    people_counts = {Person: 5}
    simulation = DiseaseSimulation(
        disease_params=disease_parameters,
        people_counts=people_counts,
        width=10, height=10
    )
    simulation.run_simulation(num_steps=100)


def manual_test_covid():
    people_counts = {
        Person: 100,
        # CarefulPerson: 100,  # uncomment after implementing CarefulPerson
        MenacingPerson: 100,
    }
    simulation = CovidSimulation(people_counts, width=100, height=100)
    simulation.run_simulation(num_steps=100)


def manual_test_ebola():
    people_counts = {
        Person: 100,
        # CarefulPerson: 100,  # uncomment after implementing CarefulPerson
        MenacingPerson: 100,
    }
    simulation = EbolaSimulation(people_counts, width=100, height=100)
    simulation.run_simulation(num_steps=100)


def manual_test_more_menacing():
    disease_parameters = {
        "starting_infection_prob": 0.8,
        "infection_prob": 0.9,
        "recovery_prob": 0.05,
        "death_prob": 0.01,
        "infection_radius": 2,
    }
    people_counts = {Person: 4, MoreMenacingPerson: 1}
    simulation = DiseaseSimulation(
        disease_params=disease_parameters,
        people_counts=people_counts,
        width=10,
        height=10,
    )
    simulation.run_simulation(num_steps=100)


def analyze_disease_params():
    people_counts = {
        Person: 100,
        CarefulPerson: 100,
        MenacingPerson: 100,
    }
    covid_simulation = CovidSimulation(people_counts, width=100, height=100)
    plot_population_status(covid_simulation, num_steps=100, filename="covid_sim.svg")
    ebola_simulation = EbolaSimulation(people_counts, width=100, height=100)
    plot_population_status(ebola_simulation, num_steps=100, filename="ebola_sim.svg")


def analyze_people_types():
    people_counts_menacing = {
        Person: 50,
        CarefulPerson: 50,
        MenacingPerson: 200,
    }
    people_counts_more_menacing = {
        Person: 50,
        CarefulPerson: 50,
        MoreMenacingPerson: 200,
    }
    sim_menacing = CovidSimulation(people_counts_menacing, width=100, height=100)
    sim_more_menacing = CovidSimulation(people_counts_more_menacing, width=100, height=100)
    plot_population_status(sim_menacing, num_steps=100, filename="menacing.svg")
    plot_population_status(sim_more_menacing, num_steps=100, filename="more_menacing.svg")


def save_covid_sim_gif():
    people_counts = {
        Person: 100,
        CarefulPerson: 100,
        MenacingPerson: 100,
    }
    simulation = CovidSimulation(people_counts, width=100, height=100)
    visualizer = DiseaseSimVisualizer(simulation, num_steps=100)
    visualizer.save_gif("covid_sim.gif", steps=100)


if __name__ == "__main__":
    pass

    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # feel free to modify or extend them when debugging your code.
    # run test.py to make sure your code passes all our test cases.

    # manual_test_person()
    # manual_test_reset_stats()
    # manual_test_observation()
    # manual_test_evolve_health()
    # manual_test_step_stats()
    # manual_test_direction_helpers()
    # manual_test_more_menacing_neighbors()
    # manual_test_small()
    # manual_test_more_menacing()
    # manual_test_covid()
    # manual_test_ebola()
    # analyze_disease_params()
    # analyze_people_types()
