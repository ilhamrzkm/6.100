from pset import (
    create_graph,
    compute_town_combos_pruning,
    compute_valid_districts,
    compute_valid_partitions,
    analyze_voting_outcomes,
)

from utils import (
    read_data_from_file,
    plot_voronoi_from_graph,
)

import matplotlib.pyplot as plt
import random


def max_distance_from_start(graph, start, district):

    current_frontier = {start}
    visited = {start}
    current_depth = 0

    while current_frontier:
        next_frontier = set()

        for node in current_frontier:
            for neighbor in graph[node]:
                if neighbor in district and neighbor not in visited:
                    visited.add(neighbor)
                    next_frontier.add(neighbor)

        if next_frontier:
            current_depth += 1

        current_frontier = next_frontier

    return current_depth


def district_diameter(graph, district):
    max_diameter = 0

    for node in district:
        dist = max_distance_from_start(graph, node, district)
        max_diameter = max(max_diameter, dist)

    return max_diameter


def analyze_gerrymandering_possibilities(
    graph, town_populations, voter_proportions, num_districts, depths
):
    """
    Analyze how varying maximum district diameter affects the proportion
    of districting plans that favor each party.
    """
    party1 = []
    party2 = []
    popular = []

    for depth in depths:
        results = analyze_voting_outcomes(
            graph, town_populations, voter_proportions, num_districts, depth,
        )

        total = results["num_partitions"]

        if total == 0:
            party1.append(0)
            party2.append(0)
        else:
            party1.append(results["partition_party1_wins"] / total)
            party2.append(results["partition_party2_wins"] / total)
            popular.append(results['proportion_party1_total_votes'])

        print("\nMax Distance: ", depth)
        print("Outcomes data:")
        print(
            f"Party 1 proportion of total votes: {results['proportion_party1_total_votes']}"
        )
        print(f"Number of partitions: {results['num_partitions']}")
        print(
            f"Number of partitions favoring party 1: {results['partition_party1_wins']}"
        )
        print(
            f"Number of partitions favoring party 2: {results['partition_party2_wins']}"
        )
        print(
            f"Number of partitions resulting in a tie: {results['partition_ties']}"
        )


    plt.figure(figsize=(8, 5))

    plt.plot(depths, party1, marker="o", label="Party 1 partition proportion")
    plt.plot(depths, party2, marker="o", label="Party 2 partition proportion")
    plt.plot(depths, popular, ls="--", color="black", label="Party 1 popular vote proportion")

    plt.xlabel("Max Diameter")
    plt.ylabel("Proportion of Favorable Partitions")

    plt.xticks(depths)
    plt.legend()
    plt.tight_layout()


def analyze_comprehensive_gerrymandering(
    graph, town_populations, num_districts, depths, file_name
):
    """
    Perform a comprehensive analysis of districting plans under varying
    compactness constraints.
    """
    file_path_json = f"data/{file_name}.json"

    depth_to_diameters = {}
    selected_samples = {}

    # data processing
    for depth in depths:

        all_districts = compute_valid_districts(
            graph, town_populations, num_districts,
            depth,
            compute_town_combos_pruning,
        )
        all_partitions = compute_valid_partitions(
            graph, num_districts, all_districts
        )

        partition_max_diameters = []
        max_diam_found = -1
        least_compact_partitions = []

        for partition in all_partitions:
            # compute the max diameters for each partition
            diameters = [district_diameter(graph, d) for d in partition]
            partition_max_diameters.append(max(diameters))

            # select one of the least compact partitions for the voronoi map
            current_partition_max = max(diameters)
            if current_partition_max >= max_diam_found:
                max_diam_found = current_partition_max
                least_compact_partitions.append(partition)
        selected_samples[depth] = random.choice(least_compact_partitions)

        depth_to_diameters[depth] = partition_max_diameters

    # histogram
    fig_hist, axes_hist = plt.subplots(2, 2, figsize=(10, 8))
    axes_hist = axes_hist.flatten()
    for i, depth in enumerate(depths):
        ax = axes_hist[i]
        data = depth_to_diameters[depth]
        if data:
            bins = [x - 0.5 for x in range(depth + 2)]
            ax.hist(
                data, bins=bins, rwidth=0.8
            )
            ax.set_xlim(-0.5, depth + 0.5)
            ax.set_xticks(range(depth + 1))
        ax.set_title(f"Distributions at Depth {depth}")
        ax.set_ylabel("Frequency")

    plt.tight_layout()

    # voronoi maps for one sample partition per depth
    fig_map, axes_map = plt.subplots(2, 2, figsize=(10, 10))
    axes_map = axes_map.flatten()
    for i, depth in enumerate(depths):
        ax = axes_map[i]
        partition = selected_samples.get(depth)
        if partition:
            plot_voronoi_from_graph(
                graph, partition, file_path_json, ax=ax, show_plot=False
            )
            ax.set_title(f"Sample Layout: Depth {depth}")
        else:
            ax.set_title(f"Depth {depth}: No Valid Partitions")
            ax.axis("off")

    plt.tight_layout()
    plt.show()


def gerrymandering(file_name, depths):
    file_path_json = f"data/{file_name}.json"
    (
        graph_filepath,
        num_districts,
        town_populations,
        voter_party1_proportions,
    ) = read_data_from_file(file_path_json)

    graph = create_graph(graph_filepath)

    analyze_gerrymandering_possibilities(
        graph,
        town_populations,
        voter_party1_proportions,
        num_districts,
        depths,
    )

    analyze_comprehensive_gerrymandering(
        graph, town_populations, num_districts, depths, file_name
    )


if __name__ == "__main__":
    gerrymandering("gerrymandering_data_1", list(range(2, 6)))
