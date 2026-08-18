"""
6.100 Spring 2026
Problem Set 5

Please fill out the following info:
Name:
Kerberos:
Approximate time spent (HH:MM):
"""

import matplotlib.pyplot as plt
import os
import random
import sys
from utils import (
    plot_graph_and_voronoi,
    plot_voronoi_from_graph,
    read_data_from_file,
)

sys.setrecursionlimit(10000)


############################################################
# create graph
############################################################


def create_graph(filename):
    """
    Create a graph representation from a file.

    Parameters:
        filename (str): The name of the text file to be read.

    Return a dict that maps each town name (str) to a list of
    neighboring towns.
    """
    raise NotImplementedError


############################################################
# generate town combinations that satisfy the population constraint
############################################################


def powerset(items):
    """
    Compute all possible subsets of a collection of items, including the
    empty set and the set of all the items.

    Parameters:
        items (list): A collection of unique objects, i.e., none are ==
            to each other.

    Return a list of sets, where each set is a unique combination of
    objects from items.
    """
    # base case: empty set has a single empty combination
    # recursive case: include first item or not with each subset of the
    # remaining items
    raise NotImplementedError


def compute_town_combos_naive(town_populations, num_districts):
    """
    Find all combinations of towns that each satisfy the population
    constraint for districts, i.e., a valid combination's total
    population should be within 10% of the average district population.

    Parameters:
        town_populations (dict): A mapping from each town (str) to its
            population (int).
        num_districts (int): The required number of districts.

    Return a list of town combinations, each represented as a set of
    towns, where each town is a str.
    """
    raise NotImplementedError


############################################################
# generate valid districts by checking connectivity on town combinations
############################################################


def create_subgraph(graph, nodes):
    """
    From a graph, extract a subgraph on a given subset of nodes.

    Parameters:
        graph (dict): A mapping from nodes to lists of their neighbors.
        nodes (set): The nodes to include in the subgraph.

    Return a new dict representing the subgraph.
    """
    raise NotImplementedError


def find_nodes_within_distance(graph, start, depth):
    """
    Find all nodes reachable from start within a given number of edges.

    Parameters:
        graph (dict): A mapping from nodes to lists of their neighbors.
        start (str): The node we start from.
        depth (int): The maximum number of edges between start and any
            other node in the neighborhood.

    Return a set of all nodes reachable from start that are no more than
    depth edges away.
    """
    raise NotImplementedError


def is_compact(graph, towns, max_distance):
    """
    Check if a given set of nodes within a graph forms a compact
    subgraph. Compactness is specified by a maximum number of edges
    between any two nodes, i.e., the edge diameter.

    Parameters:
        graph (dict): A mapping from nodes to lists of their neighbors.
        nodes (set): The nodes to include in the subgraph.
        max_distance (int): The maximum allowed number of edges between
            any two towns in the subgraph.

    Return True if any two of the given nodes are reachable in graph
    within max_distance edges, False otherwise.
    """
    raise NotImplementedError


def compute_valid_districts(
    graph,
    town_populations,
    num_districts,
    max_distance,
    compute_town_combos,
):
    """
    Find all possible districts that satisfy the population, contiguity,
    and compactness constraints.

    Parameters:
        graph (dict): A graph of neighboring town connections in the
            form of create_graph()'s output.
        town_populations (dict): A mapping from each town (str) to its
            population (int).
        num_districts (int): The required number of districts.
        max_distance (int): The maximum number of towns any two towns in
            a district may be separated by.
        compute_town_combos (function): A procedure to finding all
            combinations of towns that satisfy the district population
            constraint for districts. In this pset, this will be either
            compute_town_combos_naive() or
            compute_town_combos_pruning().

    Return a list of districts, each represented as a set of towns,
    where each town is a str.
    """
    raise NotImplementedError


############################################################
# alternate approach for generating town combinations, with pruning
############################################################


def town_combos_helper(towns, population_bounds, populations):
    """
    Recursively find all possible combinations of towns, where each
    combination's total population lies within a given range.

    Parameters:
        towns (list): Town names (strs) to generate combinations from.
        population_bounds (tuple): A (lower, upper) range for the valid
            total population of selected towns.
        populations (dict): A mapping from each town (str) to its
            population (int).

    Return a list of town combinations, each represented as a set of
    towns, where each town is a str.
    """
    raise NotImplementedError


def compute_town_combos_pruning(town_populations, num_districts):
    """
    Same functionality as compute_town_combos_naive(), but use a
    decision tree with pruning.
    """
    raise NotImplementedError


############################################################
# generate valid partitions of the state's towns
############################################################


def valid_partitions_helper(candidate_districts, num_districts, towns):
    """
    Recursively find all possible partitions of towns into a given
    number of districts.

    Parameters:
        candidate_districts (list): Possible districts that each satify
            the population and compactness constraints. A district is a
            set of towns (strs).
        num_districts (int): The required number of districts.
        towns (set): Towns that need to be covered by a district.

    Return a list of partitions, each represented as a list of districts.
    """
    raise NotImplementedError


def compute_valid_partitions(graph, num_districts, candidate_districts):
    """
    Find all possible partitions of towns into a required number of
    valid districts.

    A valid partition comprises num_districts districts, which cover
    each town with a single district. I.e., all districts cover all
    towns and do not overlap.

    Parameters:
        graph (dict): A graph of neighboring town connections in the
            form of create_graph()'s output.
        num_districts (int): The required number of districts.
        candidate_districts (list): A list of possible districts that
            each satify the population and compactness constraints. A
            district is a set of towns (strs).

    Return a list of partitions, each represented as a list of districts.
    """
    raise NotImplementedError


############################################################
# analyze voting outcomes
############################################################


def tally_party_votes(towns, town_populations, voter_proportions):
    party1_total, party2_total = 0, 0
    for town in towns:
        votes = voter_proportions[town] * town_populations[town]
        party1_total += votes
        party2_total += town_populations[town] - votes
    return party1_total, party2_total


def tally_popular_votes(town_populations, voter_proportions):
    """
    Compute the total popular vote for each party across all towns.
    """
    return tally_party_votes(
        list(town_populations.keys()), town_populations, voter_proportions
    )


def tally_district_outcomes(partition, town_populations, voter_proportions):
    """
    Compute the election outcomes within a single partition of districts.
    """
    per_district_votes = []
    for district in partition:
        per_district_votes.append(
            tally_party_votes(district, town_populations, voter_proportions)
        )

    districts_party1, districts_party2, districts_ties = 0, 0, 0
    for party1, party2 in per_district_votes:
        if party1 > party2:
            districts_party1 += 1
        elif party1 < party2:
            districts_party2 += 1
        else:
            districts_ties += 1

    return districts_party1, districts_party2, districts_ties


def tally_partition_outcomes(
    all_partitions, town_populations, voter_proportions
):
    """
    Determine how many partitions favor each party overall.
    """
    partitions_party1, partitions_party2, partitions_ties = 0, 0, 0

    for partition in all_partitions:
        districts_party1, districts_party2, districts_ties = (
            tally_district_outcomes(
                partition, town_populations, voter_proportions
            )
        )
        if districts_party1 > districts_party2:
            partitions_party1 += 1
        elif districts_party1 < districts_party2:
            partitions_party2 += 1
        else:
            partitions_ties += 1

    return partitions_party1, partitions_party2, partitions_ties


def analyze_voting_outcomes(
    graph, town_populations, voter_proportions, num_districts, max_distance
):
    """
    Evaluate how often each party benefits across all valid districtings
    given the population and compactness constraints.

    Parameters:
        graph (dict): A graph of neighboring town connections in the
            form of create_graph()'s output.
        town_populations (dict): A mapping from each town (str) to its
            population (int).
        voter_proportions (dict): A mapping from each town (str) to the
            proportion of voters supporting Party 1 (float between 0 and 1).
        num_districts (int): The number of districts to divide the towns into.
        max_distance (int): The maximum allowed number of edges between
            any two towns in the subgraph.

    Return a dictionary containing the statistics described in the pset.
    """
    raise NotImplementedError


############################################################
# manual testing code
############################################################


def manual_test_print_files(file_name, print_json=True, print_txt=True):
    file_path_json = f"data/{file_name}.json"
    data = read_data_from_file(file_path_json)
    file_path_txt = f"{os.path.dirname(__file__)}/{data[0]}"

    if print_json:
        print(f"{file_name}.json:\n{data}\n\n")

    with open(file_path_txt, "r") as file:
        content = file.read()
        if print_txt:
            print(f"{file_name}.txt:\n{content}\n\n")


def manual_test_compute_town_combos_naive(file_name):
    file_path_json = f"data/{file_name}.json"
    graph_filepath, num_districts, town_populations, _ = read_data_from_file(
        file_path_json
    )

    all_town_combos = compute_town_combos_naive(town_populations, num_districts)

    print(f"Number of town combos: {len(all_town_combos)}")
    print(f"All town combos: {all_town_combos}")


def manual_test_compute_town_combos_pruning(file_name):
    file_path_json = f"data/{file_name}.json"
    graph_filepath, num_districts, town_populations, _ = read_data_from_file(
        file_path_json
    )

    all_town_combos = compute_town_combos_pruning(
        town_populations, num_districts
    )

    print(f"Number of town combos: {len(all_town_combos)}")
    print(f"All town combos: {all_town_combos}")


def manual_test_compute_valid_districts(
    file_name, max_distance, compute_town_combos_function
):
    file_path_json = f"data/{file_name}.json"
    graph_filepath, num_districts, town_populations, _ = read_data_from_file(
        file_path_json
    )

    graph = create_graph(graph_filepath)

    all_districts = compute_valid_districts(
        graph,
        town_populations,
        num_districts,
        max_distance,
        compute_town_combos_function,
    )

    plot_voronoi_from_graph(graph, [], file_path_json, show_plot=True)
    print(f"Number of valid districts: {len(all_districts)}")
    print(f"All valid districts: {all_districts}")


def manual_test_compute_valid_partitions(
    file_name, max_distance=2, plot_n=5, print_vals=False
):
    file_path_json = f"data/{file_name}.json"
    graph_filepath, num_districts, town_populations, _ = read_data_from_file(
        file_path_json
    )

    graph = create_graph(graph_filepath)

    all_districts = compute_valid_districts(
        graph,
        town_populations,
        num_districts,
        max_distance,
        compute_town_combos_pruning,
    )
    all_partitions = compute_valid_partitions(
        graph, num_districts, all_districts
    )
    if print_vals:
        print(f"Number of valid districts: {len(all_districts)}")
        print(f"Number of valid partitions: {len(all_partitions)}")

    random.seed(41)
    random.shuffle(all_partitions)

    for partition in all_partitions[:plot_n]:
        if print_vals:
            print("Partition:", partition)
        plot_graph_and_voronoi(graph, partition, file_path_json, show_plot=True)


def manual_test_analyze_voting_outcomes(
    file_name, max_distance=2, print_outcomes=True
):
    file_path_json = f"data/{file_name}.json"
    (
        graph_filepath,
        num_districts,
        town_populations,
        voter_party1_proportions,
    ) = read_data_from_file(file_path_json)

    graph = create_graph(graph_filepath)

    outcomes_data = analyze_voting_outcomes(
        graph,
        town_populations,
        voter_party1_proportions,
        num_districts,
        max_distance,
    )
    if print_outcomes:
        print("Outcomes data:")
        print(
            f"Party 1 proportion of total votes: {outcomes_data['proportion_party1_total_votes']}"
        )
        print(f"Number of partitions: {outcomes_data['num_partitions']}")
        print(
            f"Number of partitions favoring party 1: {outcomes_data['partition_party1_wins']}"
        )
        print(
            f"Number of partitions favoring party 2: {outcomes_data['partition_party2_wins']}"
        )
        print(
            f"Number of partitions resulting in a tie: {outcomes_data['partition_ties']}"
        )
    return outcomes_data


if __name__ == "__main__":
    pass

    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # Feel free to modify or extend them when debugging your code.
    # Run test.py to make sure your code passes all our test cases.

    # manual_test_print_files("mini_1", True, True)
    # manual_test_compute_town_combos_naive("mini_1")
    # manual_test_compute_town_combos_pruning("mini_1")
    # manual_test_compute_valid_districts("mini_1", 2, compute_town_combos_naive)
    # manual_test_compute_valid_districts("mini_1", 2, compute_town_combos_pruning)
    # manual_test_compute_valid_partitions("mini_1")
    # manual_test_analyze_voting_outcomes("mini_1")
