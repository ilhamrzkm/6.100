"""
6.100 Spring 2026
Problem Set 2

Fill out the following info:
Name: Sana Shah
Kerberos: Sanashah
Approximate time spent (HH:MM): 07:00 
"""

import random
import matplotlib.pyplot as plt
# NO OTHER IMPORTS ALLOWED


############################################################
# supplied helper functions -- DO NOT MODIFY
############################################################


TRACK_LENGTH = 16
DEFAULT_SPEED = 2


def compute_mean(data):
    """
    Compute the average of a list of numbers.

    Parameters:
        data (list): The list of numerical values.

    Return the average of the numbers in data.
    """
    # NOTE: DO NOT MODIFY
    assert data, "empty data has no mean"
    return sum(data) / len(data)


def compute_standard_deviation(data):
    """
    Compute the standard deviation of a list of numbers.

    Parameters:
        data (list): The list of numerical values.

    Return the standard deviation of the numbers in data.
    """
    # NOTE: DO NOT MODIFY
    assert data, "empty data has no stdev"
    mean = compute_mean(data)
    numerator = 0
    for datum in data:
        numerator += (datum - mean) ** 2
    denominator = len(data)
    return (numerator / denominator) ** 0.5


############################################################
# simulating ideal MBTA train lines
############################################################


def get_distance(loc1, loc2):
    """
    Calculate the distance a train would travel to get from loc1 to loc2
    traveling counter-clockwise around the circular track.

    Parameters:
        loc1 (float): The position of point 1 on the track.
        loc2 (float): The position of point 2 on the track.

    Return distance from loc1 to loc2
    """
    distance = loc2 - loc1 
    if distance < 0: 
        distance += TRACK_LENGTH
    
    return distance 
    


def get_next_station(current_loc, station_locations):
    """
    Determine the first station a train starting from current_loc would
    reach on the circular track.

    Parameters:
        current_loc (float): The current position of the train.
        station_locations (list): The list of MBTA station locations.

    Return the location of the closest station to a train at current_loc.
    """
    # TODO: after writing test cases, fix this buggy staff implementation!
    # you should only need to edit 2 lines of code

    max_distance = TRACK_LENGTH #change from 0 to track length 
    closest_station = None

    for station in station_locations:
        station_distance = get_distance(current_loc, station) #flip current_loc and station so that get_dist does subtraction correctly 
        if station_distance < max_distance and current_loc != station:
            closest_station = station
            max_distance = station_distance

    return closest_station


def would_pass(current_loc, next_loc, passing_loc):
    """
    Determines if a train moving from current_loc to next_loc would have
    to pass through passing_loc on the circular track.

    Parameters:
        current_loc (float): The current position of the train.
        next_loc (float): The (projected) next position of the train on
            the track.
        passing_loc (float): The position on the track to check if
            the train would pass.

    Return True if the train would pass passing_loc, False otherwise.
    """
    # NOTE: DO NOT MODIFY
    epsilon = 0.0001 # for precision
    next_loc_distance = get_distance(current_loc, next_loc)
    passing_loc_distance = get_distance(current_loc, passing_loc)
    # if the passing_loc is further away than the next_loc, we wouldn't pass it
    return next_loc_distance + epsilon >= passing_loc_distance


def step_train(idx, train_locations, idle_time, station_locations, speed):
    """
    Calculate the next position of a single train moving from its
    current location on the circular track at the given speed, with
    stations at each position in station_locations.

    Parameters:
        idx (int): The index of the train.
        train_locations (list): The current positions of all trains on
            the track after the last time step.
        idle_time (list): The idle time left for each train after the
            last time step; idle_time[i] > 0 means the ith train should
            NOT move in this timestep.
        station_locations (list): The list of MBTA station locations.
        speed (float): The speed of the train (miles per time step).

    Return the next location of the train, and mutate the idle_time list
    for that train, following our model's rules:
    - the train does not move if it is still idle.
    - the train does not move if it would pass another at this speed.
    - the train stops at any station it would pass.
    """
    current_loc = train_locations[idx]
    next_loc = (train_locations[idx] + speed) % TRACK_LENGTH
    
    if idle_time[idx] > 0:
        idle_time[idx] -= 1
        return current_loc
   
    for i in range(len(train_locations)):    
        if idx != i and would_pass(current_loc, next_loc, train_locations[i]):
            return current_loc
        
    for i in range(len(station_locations)):
            if would_pass(current_loc, next_loc, station_locations[i]):               
                for j in range(len(train_locations)):
                    if idx != j and would_pass(current_loc, next_loc, train_locations[j]):
                        idle_time[idx] = 1
                        return current_loc
                if current_loc == station_locations[i]:
                    continue    
                idle_time[idx] = 2
                return station_locations[i]
    return (train_locations[idx] + speed) % TRACK_LENGTH

def step_simulation(
    train_locations,
    station_locations,
    idle_time,
    slowdown_func=None,
    slowdown_param=None,
    speed = float(DEFAULT_SPEED)
):
    """
    Determine the new positions of all the trains after one time step of
    the simulation, and update their idle times.

    Parameters:
        train_locations (list): The same as in step_train().
        station_locations (list): The same as in step_train().
        idle_time (list): The same as in step_train().
        speed (float): The speed of the train (miles per time step).

    Return a list containing the new positions of each train one time
    step later, and mutate the idle_time list for all trains.
    """
    current_speed = speed
                                                   
    if slowdown_func == apply_gaussian_slow:        
        current_speed = apply_gaussian_slow(slowdown_param)
    elif slowdown_func == apply_halt:
        current_speed = apply_halt(slowdown_param)
    elif slowdown_func == apply_uniform_slow:
        current_speed = apply_uniform_slow(slowdown_param)

    New_train_locations = []    

    for i in range(len(train_locations)):                            
        new_loc = step_train(i, train_locations, idle_time, station_locations, current_speed)
        New_train_locations.append(new_loc)
    return New_train_locations 
    
    



def simulate_trains(
    station_locations,
    num_steps,
    slowdown_func= None,
    slowdown_param=None,
    speed = float(DEFAULT_SPEED)
):
    """
    Run one MBTA simulation for num_steps steps, with each train starting
    at a station, to produce a history of train locations.

    Parameters:
        station_locations (list): The same as in step_train().
        num_steps (int): The number of time steps to simulate.
        # TODO (section 4): add optional parameters!

    Return a nested list of length num_steps+1, where each element is a
    list of the train locations at a timestep.
    """
    trains = station_locations.copy()                   
    idle_time = [2]*len(station_locations)
    Train_History = [trains.copy()]
    for i in range(num_steps):                     
        Train_History.append(step_simulation(Train_History[i], station_locations, idle_time, slowdown_func, slowdown_param))
    return Train_History


############################################################
# intertrain wait time
############################################################


def station_wait_times(location_history, station):
    """
    Aggregate the wait times for this station over the duration of the
    given simulation history.

    Parameters:
        location_history (list): The nested list of simulation data,
            where location_history[t][i] is the location of train i at
            time step t.
        station (float): An MBTA station location.

    Return a list of all the intertrain wait times at this specific
    station across the simulation history.
    """
    arrivals = []
    departures =[]

    for t in range(len(location_history)):                        
        for i in range(len(location_history[0])):                    
            if location_history[t][i] == station:                    
                if t > 0 and location_history[t-1][i] != station:  
                    arrivals.append(t)
                if t+1 < len(location_history) and location_history[t+1][i] != station:
                    departures.append(t)
        
    wait_times = [a - d for a, d in zip(arrivals, departures)]  
    return wait_times


def collect_all_wait_times(location_history, station_locations):
    """
    Collect the wait times across all stations for the given simulation
    history.

    Parameters:
        location_history (list): The nested list of simulation data,
            where location_history[t][i] is the location of train i at
            time step t.
        station_locations (list): The list of MBTA station locations.

    Return a list of wait times.
    """
    wait_time_nested = []

    for i in range(len(station_locations)):
        wait_time_nested.append(station_wait_times(location_history, station_locations[i]))
    flattened = [i for s in wait_time_nested for i in s]             
    flattened.sort()

    return flattened


############################################################
# realistic environments
############################################################


def apply_none(param):
    """
    Dummy slowdown function that does not modify the train's speed.

    Parameters:
        param (float): A placeholder for a slowdown function parameter
        (not used in this function).

    Return the default train speed.
    """
    # NOTE: DO NOT MODIFY
    return DEFAULT_SPEED


def apply_halt(p):
    """
    Halt a train with probability p.

    Parameters:
        p (float): The probability of halting.

    Return 0 if the train halts, otherwise the default speed.
    """
    if p > random.random():    
        return 0
    
    return DEFAULT_SPEED


def apply_uniform_slow(param):
    """
    Reduce a train's speed to a random value drawn uniformly from the
    interval [0, DEFAULT_SPEED].

    Parameters:
        param (float): A placeholder for a slowdown function parameter
        (not used in this function).

    Return the updated train speed after applying a uniform slowdown.
    """
    new_speed = random.uniform(0, DEFAULT_SPEED)     
    return new_speed

def apply_gaussian_slow(sigma):
    """
    Reduce a train's speed by a random amount drawn from a Gaussian
    distribution with the given standard deviation, centered around half
    the default train speed.

    Parameters:
        sigma (float): The standard deviation of the distribution.

    Return the updated train speed after applying a Gaussian slowdown.
    If the updated speed is outside of [0, DEFAULT_SPEED], clip it to be
    in that range.
    """
    new_speed = random.gauss(mu = (DEFAULT_SPEED/2), sigma = sigma) 
    if new_speed > DEFAULT_SPEED:
        new_speed = DEFAULT_SPEED

    if new_speed < 0:
        new_speed = 0
    return new_speed


def run_monte_carlo(
    station_locations,
    num_steps,
    slowdown_func,
    slowdown_param,
    num_trials,
):
    """
    Run multiple trials of the realistic train simulation and compute the
    mean and standard deviation of the average intertrain wait time
    over all trials.

    Parameters:
        station_locations (list): The same as in simulate_trains().
        num_steps (int): The same as in simulate_trains().
        slowdown_func (function): A slowdown function that changes a
            train's speed from its default. Takes a single parameter.
        slowdown_param (float): The parameter used in slowdown_func.
        num_trials (int): The number of trials to run.

    Return a list [mean, stdev, location_history], corresponding to the
    mean and standard deviation of the average intertrain wait time for
    each trial, along with a location_history from any trial.
    """
    trial_mean = 0.0
    trial_stdev = 0.0

    for _ in range(num_trials): 
        Location_history = simulate_trains(station_locations, num_steps, slowdown_func, slowdown_param)    
        data =collect_all_wait_times(Location_history, station_locations)
        trial_mean += compute_mean(data)
        trial_stdev += compute_standard_deviation(data)

    mean = trial_mean/num_trials 
    stdev = trial_stdev/num_trials

    return [mean, stdev, Location_history]


############################################################
# analyzing wait times
############################################################


def plot_wait_time_distribution(
    location_history,
    station_locations,
    slowdown_name="apply_none",
    bins=10,
):
    """
    Plot a histogram of all intertrain wait times observed across every
    station for the given simulation history.

    Parameters:
        location_history (list): The nested list of simulation data,
            where location_history[t][i] is the location of train i at
            time step t.
        station_locations (list): The list of MBTA station locations.
        slowdown_name (str): The name of the slowdown function applied
            (for labeling purposes).
        bins (int): The number of bins to use in the histogram plot.
    """
    wait_times = collect_all_wait_times(location_history, station_locations)

    plt.hist(wait_times, bins=bins)
    plt.title(f"Wait Time Distribution ({slowdown_name})")
    plt.xlabel("Wait Time")
    plt.ylabel("Frequency")
    plt.show()


def plot_monte_carlo_distributions(
    station_locations,
    num_steps,
    num_trials,
    slowdown_func,
    slowdown_param_values,
    param_name,
):
    """
    Analyze and plot the effect of varying a track parameter on average
    wait time.

    Parameters:
        station_locations (list): The same as in simulate_trains().
        num_steps (int): The same as in simulate_trains().
        num_trials (int):  The same as in run_monte_carlo().
        slowdown_func (function): A slowdown function that changes a
            train's speed from its default. Takes a single parameter.
        slowdown_param_values (list): The different values to vary the
            tested parameter over.
        param_name (str): The name of the parameter being varied
            (for labeling purposes).
    """
    means = []

    for param in slowdown_param_values:
        mean, _, _ = run_monte_carlo(
            station_locations,
            num_steps,
            slowdown_func,
            param,
            num_trials,
        )
        means.append(mean)

    plt.plot(slowdown_param_values, means)
    plt.xlabel(param_name)
    plt.ylabel("Average Wait Time")
    plt.title(f"Effect of {param_name} on Wait Time")
    plt.show()


############################################################
# manual testing code
############################################################


def get_sample_scenario():
    # t0 -> t16 starting from stations 5, 6, and 8
    sample_scenario_stations = [5, 6, 8]
    sample_scenario_history = [
        [5, 6, 8],
        [5, 6, 8],
        [5, 6, 8], # train 2 is departing from station 8
        [5, 6, 10],
        [5, 8, 12], # train 1 is arriving to station 8
        [6, 8, 14],
        [6, 8, 0], # train 1 is departing from station 8
        [6, 10, 2],
        [8, 12, 4], # train 0 is arriving to station 8
        [8, 14, 5],
        [8, 0, 5], # train 0 is departing from station 8
        [10, 2, 5],
        [12, 4, 6],
        [14, 4, 6],
        [0, 4, 6],
        [2, 4, 8], # train 2 is arriving to station 8
        [2, 5, 8],
    ]
    return [sample_scenario_stations, sample_scenario_history]


# def manual_test_step_train():
#     print("Manual test step_train...")
#     station_locs = [0.5, 8, 13]
#     train_locs = [0.5, 6.5, 13]
#     idle_time = [0, 0, 1] # train 0 and 1 moving, train 2 idle
#     print(f"train idx={1}", f"{station_locs=}", f"{train_locs=}", f"{idle_time=}")

#     # train 1 should move to a station (6.5 -> 8)
#     new_loc = step_train(1, train_locs, idle_time, station_locs, DEFAULT_SPEED)
#     print(f"Expected location: {8}, got {new_loc}")
#     print(f"Expected idle time: {[0, 2, 1]}, got {idle_time}")
#     print()

def manual_test_step_train():
    print("Manual test step_train...")
    station_locs = [0.5, 8, 13]
    train_locs = [3, 6.5, 15.9]
    idle_time = [0, 0, 0] # train 0 and 1 moving, train 2 idle
    print(f"train idx={2}", f"{station_locs=}", f"{train_locs=}", f"{idle_time=}")

    # train 1 should move to a station (6.5 -> 8)
    new_loc = step_train(2, train_locs, idle_time, station_locs, DEFAULT_SPEED)
    print(f"Expected location: {13.1}, got {new_loc}")
    print()

def manual_test_step_simulation():
    print("Manual test step_simulation...")
    station_locs = [0.5, 8, 13]
    train_locs = [0.5, 6.5, 13]
    idle_time = [0, 0, 1] # train 0 and 1 moving, train 2 idle
    print(f"{station_locs=}", f"{train_locs=}", f"{idle_time=}")

    # train 0 moves regular, train 1 moves to station, train 2 idle
    new_locations = step_simulation(train_locs, station_locs, idle_time, DEFAULT_SPEED)
    print(f"Expected locations: {[2.5, 8, 13]}, got {new_locations}")
    print(f"Expected idle time: {[0, 2, 0]}, got {idle_time}")
    print()


def manual_test_simulate_trains():
    print("Manual test simulate_trains w/ sample scenario...")
    station_locations, expected_history = get_sample_scenario()
    actual_history = simulate_trains(station_locations, len(expected_history)-1)

    print(f"Expected history length {len(expected_history)}, got {len(actual_history)}")
    for t in range(len(expected_history)):
        if t >= len(actual_history):
            print(f"time step {t}: expected {expected_history[t]}, got (nothing)")
        else:
            print(f"time step {t}: expected {expected_history[t]}, got {actual_history[t]}")
    print()


def manual_test_station_wait_times():
    print("Testing station_wait_times w/ sample scenario...")
    # stations located at 5, 6, and 8. check for wait times at 8
    location_history = get_sample_scenario()[1]
    wait_times = station_wait_times(location_history, station=8)
    print(f"Expected wait times: {[2, 2, 5]}, got {sorted(wait_times)}")
    print()


def manual_test_collect_all_wait_times():
    print("Testing collect_all_wait_times w/ sample scenario...")
    station_locations, location_history = get_sample_scenario()
    expected_data = sorted([5, 5] + [2, 5] + [2, 2, 5]) # wait times for 5, 6, and 8 resp.
    actual_data = collect_all_wait_times(location_history, station_locations)
    print(f"Expected wait times: {expected_data}, got {sorted(actual_data)}")
    print()


def manual_test_run_monte_carlo():
    print("Testing run_monte_carlo...")

    random.seed(2)
    station_locations = [0, 1.5, 7.75]
    mean, stdev, _ = run_monte_carlo(
        station_locations=station_locations,
        num_steps=100,
        slowdown_func=apply_halt,
        slowdown_param=0.25, # p = 0.25 -> trains have a 25% chance of halting
        num_trials=500,
    )
    staff_mean, staff_stdev = 5.53335631, 0.27019038
    print(f"Staff mean: {staff_mean:>12.8f}, staff stdev: {staff_stdev:>12.8f}")
    print(f"Student mean: {mean:>10.8f}, student stdev: {stdev:>10.8f}")
    one_stdev = staff_mean - staff_stdev < mean < staff_mean + staff_stdev
    print(f"Within 1 standard deviation of the staff mean: {one_stdev}")
    two_stdev = staff_mean - 2*staff_stdev < mean < staff_mean + 2*staff_stdev
    print(f"Within 2 standard deviations of the staff mean: {two_stdev}")
    print("If your mean is far from the staff mean, check your implementation.")
    print()


def manual_test_plot_wait_time_distribution():
    print("Testing plot_wait_time_distribution...")
    random.seed(2)
    station_locations = [2.5, 7, 8.75, 13]
    num_steps = 500

    # no slowdown
    location_history = simulate_trains(station_locations, num_steps)
    plot_wait_time_distribution(location_history, station_locations, slowdown_name="apply_none")

    p = 0.25
    location_history = simulate_trains(station_locations, num_steps, apply_halt, p)
    plot_wait_time_distribution(location_history, station_locations, slowdown_name="apply_halt")

    location_history = simulate_trains(station_locations, num_steps, apply_uniform_slow, None)
    plot_wait_time_distribution(location_history, station_locations, slowdown_name="apply_uniform")

    sigma = 0.25
    location_history = simulate_trains(station_locations, num_steps, apply_gaussian_slow, sigma)
    plot_wait_time_distribution(location_history, station_locations, slowdown_name="apply_gaussian")
    print()


def manual_test_plot_monte_carlo_distributions():
    print("Testing plot_monte_carlo_distributions...")
    random.seed(2)
    station_locations = [2.5, 7, 8.75, 13]
    num_steps = 100
    num_trials = 100
    p_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
    sigma_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

    plot_monte_carlo_distributions(
        station_locations, num_steps, num_trials, apply_halt, p_values, "p"
    )
    plot_monte_carlo_distributions(
        station_locations, num_steps, num_trials, apply_gaussian_slow, sigma_values, "sigma"
    )
    print()

def manual_test_get_next_station_general():
    print("Testing get_next_station_ general case...")
    station_locs = [0.5, 8, 13]
    train_loc = 0.6
    next_station = get_next_station(train_loc, station_locs)
    if next_station == 8:
        print(True)
        return True  
    else: 
        print(False)
        return False  

def manual_test_get_next_station_edge():
    print("Testing get_next_station edge case...")
    station_locs = [0.5, 8, 13]
    train_loc = 0.5
    next_station = get_next_station(train_loc, station_locs)
    if next_station == 8:
        print(True)
        return True  
    else: 
        print(False)
        return False  


if __name__ == "__main__":
    pass

    # manual_test_get_next_station_general()
    # manual_test_get_next_station_edge()

    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # Feel free to modify or extend them when debugging your code.
    # Run test.py to make sure your code passes all our test cases.

    manual_test_step_train()
    # manual_test_step_simulation()
    # manual_test_simulate_trains()
    # manual_test_station_wait_times()
    # manual_test_collect_all_wait_times()
    # manual_test_run_monte_carlo()
    # manual_test_plot_wait_time_distribution()
    # manual_test_plot_monte_carlo_distributions()
