"""
6.100 Spring 2026
Problem Set 7

Please fill out the following info:
Name: Sana Shah
Kerberos: sanashah
Approximate time spent (HH:MM): 09:00
"""

import random
import math
from visualization import DiseaseSimVisualizer, plot_population_status


############################################################
# person
############################################################


class Person:
    """An abstract class for a person in a disease simulation."""

    def __init__(self, infected = False, alive = True):
        self._infected = infected
        self._alive = alive

    def move(self, observation):
        """
        Return the delta (dx, dy) of the person's move.
        The person moves in a random direction in the unit circle.
        """
        if not self._alive:
            return (0, 0)
    
        angle = random.uniform(0, 2 * math.pi)
        
        x = math.cos(angle)
        y = math.sin(angle)
        return (x, y)

    def update_health(self, infected=False, alive=True):
        """
        Update the person's health status.

        Parameters:
            infected (bool): whether the person is infected
            alive (bool): whether the person is alive
        """
        self._infected = infected 
        self._alive = alive

    def is_infected(self):
        """
        Return a boolean representing if the person is infected.
        """
        return self._infected

    def is_alive(self):
        """
        Return a boolean representing if the person is alive.
        """
        return self._alive


############################################################
# helper functions
############################################################


def find_distance(loc1, loc2):
    """
    Return the euclidean distance between two (x, y) locations.
    """
    x = loc2[0] - loc1[0]
    y = loc2[1] - loc1[1]
    return math.sqrt(x**2 + y**2)


def find_nearest_neighbor(observation, neighbors):
    """
    Return the nearest neighbor from the list of neighbors.
    """
    if not neighbors: 
        return None
    nearest = None
    nearest_dist = float('inf') #starting distance 
    for neighbor in neighbors: #go through each neighbor to find nearest 
        x, y = observation[neighbor]
        dist = math.sqrt(x**2 + y**2) #dist 
        if dist < nearest_dist:
            nearest_dist = dist
            nearest = neighbor
    
    return nearest

def move_towards_neighbor(observation, neighbor):
    """
    Return the delta (dx, dy) of the person's move.
    The person moves towards the neighbor.
    """
    x, y = observation[neighbor]
    dist = math.sqrt(x**2 + y**2)
    
    if dist == 0:
        return (0, 0)
    
    
    return (x / dist, y / dist) #unit vector so movement is within unit circle


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
        for person_type, count in self.people_counts.items():
             for i in range(count):
                 infected = random.random() < self.starting_infection_prob #does person start infected 
                 person = person_type(infected=infected, alive=True)
                 x = random.uniform(0, self.width) #places people within the bounds 
                 y = random.uniform(0, self.height)
                 self.people_locs[person] = (x, y) #fills the list with locations of the ppl in simulation


    def generate_observation(self, person):
        """
        Find all neighboring people within the infection radius of the
        given person.

        Return a dictionary mapping neighbors to their displacement
        (dx, dy) from person.
        """
        observation = {}
        person_loc = self.people_locs[person]

        for other, other_loc in self.people_locs.items(): #other people around
            if other == person: 
                continue 
            dist = find_distance(person_loc, other_loc)
            if dist <= self.infection_radius: #if the dist is within the radius that can affect the person
                x = other_loc[0] - person_loc[0]
                y = other_loc[1] - person_loc[1]
                observation[other] = (x,y) #store this new position in observation
        return observation


    def evolve_health(self, person, observation):
        """
        Determine the health status of the given person based on the
        observation.
        Return the infection and alive status of the person as a tuple
        (infected, alive)
        DO NOT MUTATE THE PERSON
        """
        if not person.is_alive(): #dead and are not infected
            return (False, False)
        
        if person.is_infected():
            if random.random() <= self.recovery_prob: #infected person recovers 
                return (False, True)
            if random.random() <= self.death_prob: #infected person dies 
                return (False, False)
            return (True, True) #infected and alive 
        
        neighbor_infected = False 

        for neighbor in observation:
            if neighbor.is_infected():
                neighbor_infected = True  #neighbor is infected
                break 

        if neighbor_infected and random.random() < self.infection_prob:
            return (True, True) #infected and alive
        
        return(False, True) #healthy and alive 


    def step(self):
        """
        Advance the simulation by one time step, updating all people and
        applying disease transmission rules.
        """
        new_loc = {} #based on current location 
        new_health = {}

        for person in self.people_locs: #
            observation = self.generate_observation(person)
            new_health[person] = self.evolve_health(person, observation)
            dx, dy = person.move(observation) #the move 
            x, y = self.people_locs[person] #the current locations
            new_x = max(0, min(self.width, x + dx)) #boundaries 
            new_y = max(0, min(self.height, y + dy))
            new_loc[person] = (new_x, new_y) 
        
        for person in self.people_locs: #make the changes happen 
            infected, alive = new_health[person]
            person.update_health(infected, alive)
            self.people_locs[person] = new_loc[person]



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
        state = {}
        for person in self.people_locs: #create dictionary
            state[person] = {
                "location": self.people_locs[person],
                "infected": person.is_infected(),
                "alive": person.is_alive()
            }

        people = list(self.people_locs.keys())
        num_infected = 0
        num_alive = 0 
        for p in people:
            if p.is_infected(): #number infected
                num_infected += 1
            if p.is_alive(): #number alive 
                num_alive += 1
        return (state, num_infected, num_alive)


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
        if self._infected:  # replace with your attribute name
            # find nearest healthy neighbor
            healthy_neighbors = [
                neighbor for neighbor in observation if not neighbor.is_infected()
            ]
            nearest_neighbor = find_nearest_neighbor(observation, healthy_neighbors)
            # move towards healthy neighbor
            if nearest_neighbor is not None:
                return move_towards_neighbor(observation, nearest_neighbor)
        return super().move(observation)

class CarefulPerson(Person):
    """A careful person moves away from infected people when healthy,
    or away from healthy people when infected."""

    def move(self, observation):
        """
        If healthy, move away from nearest infected neighbor.
        If infected, move away from nearest healthy neighbor.
        Move randomly if none of these conditions are met.
        """
        if not self._infected: #healthy so move away from nearest infected neighbor    
            infected_neighbors = [
                neighbor for neighbor in observation if neighbor.is_infected()
            ]
            nearest_neighbor = find_nearest_neighbor(observation, infected_neighbors)
            if nearest_neighbor is not None:
                dx, dy = move_towards_neighbor(observation, nearest_neighbor)
                return (-dx, -dy)  #move away is opposite direction of toward

        else: #infected so move away from nearest healthy neighbor
            healthy_neighbors = [
                neighbor for neighbor in observation if not neighbor.is_infected()
            ]
            nearest_neighbor = find_nearest_neighbor(observation, healthy_neighbors)
            if nearest_neighbor is not None:
                dx, dy = move_towards_neighbor(observation, nearest_neighbor)
                return (-dx, -dy)  #move away is opposite direction of toward

        return super().move(observation)  # random move if no conditions met
    
class MoreMenacingPerson(MenacingPerson):
    """A more menacing person moves towards the K nearest healthy people when infected."""

    K = 5
    def move(self, observation):
        """
        If infected, move towards the average location of the K nearest
        healthy neighbors. Otherwise, move randomly.
        """
        if self._infected:
            healthy_neighbors = [
                neighbor for neighbor in observation if not neighbor.is_infected()
            ]

            if len(healthy_neighbors) > 0:
                sorted_neighbors = sorted( #sort healthy neighbors by distance
                    healthy_neighbors,
                    key=lambda n: math.sqrt(observation[n][0]**2 + observation[n][1]**2)
                )

                
                k_nearest = sorted_neighbors[:self.K] #take K nearest

                
                avg_dx = sum(observation[n][0] for n in k_nearest) / len(k_nearest) #find average displacement of K nearest
                avg_dy = sum(observation[n][1] for n in k_nearest) / len(k_nearest)

                dist = math.sqrt(avg_dx**2 + avg_dy**2) #normalize to unit vector
                if dist == 0:
                    return (0, 0)
                return (avg_dx / dist, avg_dy / dist)

        return super().move(observation)


############################################################
# different disease simulations
############################################################


class CovidSimulation(DiseaseSimulation):

    def __init__(self, people_counts, width, height):
        disease_params = {
            "starting_infection_prob": 0.2,
            "infection_prob": 0.2,
            "recovery_prob": 0.05,
            "death_prob": 0.005,
            "infection_radius": 4,
        }
        super().__init__(disease_params, people_counts, width, height)


class EbolaSimulation(DiseaseSimulation):

    def __init__(self, people_counts, width, height):
        disease_params = {
            "starting_infection_prob": 0.2,
            "infection_prob": 0.9,
            "recovery_prob": 0.05,
            "death_prob": 0.5,
            "infection_radius": 2,
        }
        super().__init__(disease_params, people_counts, width, height)


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
    observation ={neighbor: (3, 4)}

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
        # CarefulPerson: 100, # uncomment after implementing CarefulPerson
        MenacingPerson: 100,
    }
    simulation = CovidSimulation(people_counts, width=100, height=100)
    simulation.run_simulation(num_steps=100)


def manual_test_ebola():
    people_counts = {
        Person: 100,
        # CarefulPerson: 100, # uncomment after implementing CarefulPerson
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
    # try covid simulation
    covid_simulation = CovidSimulation(people_counts, width=100, height=100)
    plot_population_status(covid_simulation, num_steps=100, filename="covid_sim.svg")
    # try ebola simulation
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

    # # person manual test
    # manual_test_person()

    # #simulation manual tests
    # manual_test_reset_stats()
    # manual_test_observation()
    # manual_test_evolve_health()
    # manual_test_step_stats()

    # #person subclasses
    # manual_test_direction_helpers()
    # manual_test_more_menacing_neighbors()

    # #run simulation
    #manual_test_small()
    # manual_test_more_menacing()
    # manual_test_covid()
    # manual_test_ebola()

    # #analyze
    analyze_disease_params()
    analyze_people_types()
