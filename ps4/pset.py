"""
6.100 Spring 2026
Problem Set 4

Fill out the following info:
Name:
Kerberos:
Approximate time spent (HH:MM):
"""

import matplotlib.pyplot as plt
import networkx as nx
from utils import (
    neighbors, path_to_string, pathlist_to_string,
    time_pathfinding, visualize_graph_with_path,
)
from matplotlib.patches import Patch

# NO OTHER IMPORTS ALLOWED
############################################################
# reading graph data and building graph data structure
############################################################

def build_graph(filepath):
    """
    Read the graph data from the given path and build a graph data structure.

    Parameters:
        filepath (str): Path to the graph data file.

    Return a graph dictionary where each key is a node and the value
    is a list of tuples (neighbor, weight, edge_type) representing
    the node's outgoing edges, where neighbor is a string,
    weight is an int and edge_type is a string that is either
    "one_way", "local" or "toll".

    If a node has no outgoing edges, map it to an empty list.
    """
    raise NotImplementedError

############################################################
# breath-first search
############################################################

def bfs(graph, start, goal):
    """
    Perform breadth-first search on the graph to find a path from start
    to goal. Ignore edge weights in the graph and treat all edges as
    having weight 1.

    Parameters:
        graph (dict): A graph dictionary returned by build_graph().
        start: The starting node for the search.
        goal: The target node for the search.

    Return a list of nodes representing the path from start to goal,
    or None if no path exists.
    """
    raise NotImplementedError

############################################################
# weighted graph search
############################################################


def expand_edge_iterative(expanded_graph, u, v, weight):
    """
    Expand a weighted edge (u -> v) using iteration.

    Parameters:
        expanded_graph (dict): A graph dictionary being built for the expanded graph.
        u: The starting node of the edge.
        v: The ending node of the edge.
        weight (int): Weight of the edge.

    Mutate expanded_graph by adding the necessary intermediate
    nodes and edges to represent the weighted edge.
    """
    raise NotImplementedError


def expand_edge_recursive(expanded_graph, u, v, weight):
    """
    Expand a weighted edge (u -> v) using recursion.

    Parameters:
        expanded_graph (dict): The same as in expand_edge_iterative().
        u: The starting node of the edge.
        v: The ending node of the edge.
        weight (int): Weight of the edge.

    Mutate expanded_graph by adding the necessary intermediate
    nodes and edges to represent the weighted edge.
    """
    raise NotImplementedError


def expand_weighted_graph(weighted_graph, expand_edge_fn):
    """
    Expand a weighted graph via edge expansion.

    Parameters:
        weighted_graph (dict): A graph dictionary returned by build_graph().
        expand_edge_fn (function): A function that takes
            (expanded_graph, u, v, weight) and mutates expanded_graph to
            add the necessary intermediate nodes and edges.

    Return a graph dictionary similar to build_graph(), but with expanded edges.
    """
    raise NotImplementedError


def strip_intermediate_nodes(path):
    """
    Remove intermediate expansion nodes from a path.

    Parameters:
        path (list or None): A list of nodes from the expanded graph, or None.

    Return a list of original graph nodes only, or None if the input path is None.
    """
    raise NotImplementedError


def find_shortest_path(
    filepath,
    start,
    goal,
    pathfinding_algorithm=bfs,
    expand_edge_fn=expand_edge_iterative,
):
    """
    Find the shortest path between start and goal in a weighted graph
    by expanding weighted edges and running BFS.

    Parameters:
        filepath (str): Path to the graph data file.
        start: Starting node.
        goal: Target node.
        pathfinding_algorithm (function): Pathfinding function that takes
            (graph, start, goal) as input. Default is bfs.

    Return a list of nodes representing the shortest path, or None if no path exists.
    """
    raise NotImplementedError


############################################################
# graph layering - pathfinding with constraints
############################################################


def build_layered_graph_for_tolls(graph, max_tolls):
    """
    Build a layered graph where each node tracks how many toll
    roads have been used so far.

    Parameters:
        graph (dict): The same as in bfs().
        max_tolls (int): Maximum number of toll roads allowed.

    Return a graph dictionary of the form:
    {
        (node, tolls_used): [((neighbor, new_tolls_used), weight, edge_type), ...],
        ...
    }
    Where each key is a tuple of (original_node, tolls_used) and the value
    is a list of tuples representing the neighbors in the layered graph.
    Each neighbor is a tuple of
    ((neighbor_node, new_tolls_used), weight, edge_type),
    where neighbor_node is a string, new_tolls_used is an int,
    weight is an int, and edge_type is a string.
    """
    raise NotImplementedError


def strip_toll_state(path):
    """
    Remove toll-state information from a layered path.

    Parameters:
        path (list or None): A list of (node, tolls_used) tuples
            representing a path in the layered graph, or None.

    Return a list of original node names in order, or None if the
    input path is None.
    """
    raise NotImplementedError


def find_shortest_path_with_tolls(
    filepath, start, goal, max_tolls, pathfinding_algorithm=bfs
):
    """
    Find the shortest path from start to goal using at most max_tolls toll roads.

    Parameters:
        filepath (str): Path to the graph data file.
        start: Starting node.
        goal: Goal node.
        max_tolls (int): Maximum number of toll roads allowed.
        pathfinding_algorithm (function): BFS-style function to use.

    Return a list of nodes representing the path, or None if no valid path exists.
    """
    raise NotImplementedError


############################################################
# bfs with predecessors, bfs comparison
############################################################


def reconstruct_path(pred, start, goal):
    """
    Reconstruct a path from start to goal using a predecessor dictionary.

    Parameters:
        pred (dict): Maps each node to the node it was discovered from.
        start: The starting node.
        goal: The target node.

    Return a list of nodes representing the path from start to goal.
    """
    raise NotImplementedError


def bfs_predecessors(graph, start, goal):
    """
    Perform breadth-first search on the graph using a predecessor
    dictionary to reconstruct the shortest path.

    Ignores edge weights in the graph and treats all edges as weight 1.

    Parameters:
        graph (dict): A graph dictionary returned by build_graph().
        start: The starting node for the search.
        goal: The target node for the search.

    Return a list of nodes representing the path from start to goal,
    or None if no path exists.
    """
    raise NotImplementedError

def generate_grid_graph(n):
    """
    Generate an n by n grid graph with unit-weight edges.

    Nodes are named "N0", "N1", ..., "N(n*n - 1)" in row-major order.
    Each node connects to its valid neighboring cells (up, down, left, right).
    All edges have weight 1 and edge type "local".

    Parameters:
        n (int): The dimension of the grid.

    Return a graph dictionary of the same type returned by build_graph().

    TODO: Fix the bug in this implementation!
    """
    graph = {}

    for row in range(n):
        for col in range(n):
            index = row * n + col
            node = f"N{index}"
            graph[node] = []

    for row in range(n):
        for col in range(n):
            index = row * n + col
            node = f"N{index}"

            # up
            if row >= 0:
                neighbor = f"N{(row - 1) * n + col}"
                graph[node].append((neighbor, 1, "local"))

            # down
            if row < n - 1:
                neighbor = f"N{(row + 1) * n + col}"
                graph[node].append((neighbor, 1, "local"))

            # left
            if col > 0:
                neighbor = f"N{row * n + (col - 1)}"
                graph[node].append((neighbor, 1, "local"))

            # right
            if col < n - 1:
                neighbor = f"N{row * n + (col + 1)}"
                graph[node].append((neighbor, 1, "local"))

    return graph


def compare_bfs_implementations(sizes, trials=3):
    """
    Compare the runtime of multiple pathfinding algorithms on n by n grid graphs.

    For each grid size n in sizes, generate an n by n grid graph and
    measure the runtime of each algorithm when finding a path from
    the top-left node to the bottom-right node.

    Parameters:
        algorithms (list): List of tuples (name, function), where name (str)
            is the label for plotting and function is a pathfinding function
            that takes (graph, start, goal).
        sizes (list): List of grid sizes n to test.
        trials (int): Number of repeated trials per size for averaging.

    Display a runtime comparison plot.
    """
    # NOTE: DO NOT MODIFY
    results = {}
    algorithms = [
        ("BFS (path copying)", bfs),
        ("BFS (predecessors)", bfs_predecessors),
    ]
    for name, _ in algorithms:
        results[name] = []

    for n in sizes:
        graph = generate_grid_graph(n)
        start = "N0"
        goal = f"N{n*n - 1}"

        for name, algorithm in algorithms:
            total_time = 0.0

            for _ in range(trials):
                total_time += time_pathfinding(algorithm, graph, start, goal)

            avg_time = total_time / trials
            results[name].append(avg_time)

    # plot results
    for name in results:
        plt.plot(sizes, results[name], label=name)

    plt.xlabel("Grid size n (n x n graph)")
    plt.ylabel("Average runtime (seconds)")
    plt.title("Pathfinding Algorithm Runtime Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()


############################################################
# manual testing code
############################################################


def manual_test_bfs_manhattan_one_way_grid():
    graph = build_graph("data/manhattan_5x5_oneway.txt")

    start = "N0"
    goal = "N24"

    path = bfs(graph, start, goal)

    print("Path from", start, "to", goal)
    print(path_to_string(path))
    print()
    # expected: a path of length 9 nodes (8 moves),
    # exact path may differ depending on neighbor ordering.
    # e.g. N0-->N1-->N2-->N3-->N4-->N9-->N14-->N19-->N24


def manual_test_bfs_twoway_vs_oneway_reachability():
    """
    Compare BFS on a one-way vs. two-way 5x5 Manhattan grid.

    Expected:
        One-way: N24 -> N0 has no path (must move up/left).
        Two-way: N24 -> N0 has a valid shortest path.
    """
    start = "N24"
    goal = "N0"

    g_one = build_graph("data/manhattan_5x5_oneway.txt")
    p_one = bfs(g_one, start, goal)
    print("One-way:", path_to_string(p_one))  # expected: "Empty path"

    g_two = build_graph("data/manhattan_5x5_twoway.txt")
    p_two = bfs(g_two, start, goal)
    print("Two-way:", path_to_string(p_two))  # expected: a valid path (length 9 nodes)


def manual_test_find_shortest_path_small_weighted():
    path = find_shortest_path("data/small_weighted_mixed.txt", "A", "F")

    print("Shortest path using expansion:")
    print(path_to_string(path))
    # expected: A-->C-->D-->E-->F


def manual_test_bfs_predecessors_manhattan_one_way_grid():
    graph = build_graph("data/manhattan_5x5_oneway.txt")

    start = "N0"
    goal = "N24"

    path = bfs_predecessors(graph, start, goal)

    print("Path from", start, "to", goal, "(BFS with predecessors):")
    print(path_to_string(path))
    print()


def manual_test_toll_layering():
    filepath = "data/small_toll_test.txt"

    for k in [0, 1, 2]:
        path = find_shortest_path_with_tolls(filepath, "A", "E", k)
        print("max_tolls =", k)
        print(path_to_string(path))
        print()


def manual_test_visualize_paths():
    filepath = "data/manhattan_5x5_oneway.txt"
    graph = build_graph(filepath)
    path = bfs(graph, "N0", "N24")

    print("Visualizing 5x5 one-way Manhattan grid")
    print("Path:", path_to_string(path))
    visualize_graph_with_path(graph, path, start="N0", goal="N24", n=5)

    filepath = "data/manhattan_5x5_twoway.txt"
    graph = build_graph(filepath)
    path = bfs(graph, "N24", "N0")

    print("Visualizing 5x5 two-way Manhattan grid")
    print("Path:", path_to_string(path))
    visualize_graph_with_path(graph, path, start="N24", goal="N0", n=5)

    filepath = "data/small_weighted_mixed.txt"
    graph = build_graph(filepath)
    path = find_shortest_path(filepath, "A", "F")

    print("Visualizing small weighted graph")
    print("Shortest weighted path:", path_to_string(path))
    visualize_graph_with_path(graph, path, start="A", goal="F")

    filepath = "data/5x5_weighted.txt"
    graph = build_graph(filepath)
    path = find_shortest_path(filepath="data/5x5_weighted.txt", start="N0", goal="N24")

    print("Visualizing 5x5 weighted graph")
    print("Shortest weighted path:", path_to_string(path))
    visualize_graph_with_path(graph, path, start="N0", goal="N24", n=5)


def manual_test_compare_bfs_versions():
    sizes = []
    for k in range(1, 21):
        sizes.append(10 * k)

    compare_bfs_implementations(
        sizes=sizes,
        trials=3,
    )


if __name__ == "__main__":
    pass

    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # Feel free to modify or extend them when debugging your code.
    # Run test.py to make sure your code passes all our test cases.

    # manual_test_bfs_manhattan_one_way_grid()
    # manual_test_bfs_twoway_vs_oneway_reachability()
    # manual_test_find_shortest_path_small_weighted()
    # manual_test_visualize_paths()
    # manual_test_toll_layering()
    # manual_test_bfs_predecessors_manhattan_one_way_grid()
    # manual_test_compare_bfs_versions()
