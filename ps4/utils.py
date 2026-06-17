import matplotlib.pyplot as plt
import networkx as nx
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

############################################################
# graph and display helpers -- DO NOT MODIFY
############################################################


def neighbors(graph, node):
    """
    Return the neighbors of a given node in the graph.

    Parameters:
        graph (dict): A graph dictionary as returned by build_graph().
        node: A node in the graph.

    Return a list of (neighbor, weight, edge_type) tuples for the given node.
    """
    return graph.get(node, [])


def path_to_string(path):
    """
    Convert a path into a string representation.

    Parameters:
        path (list or None): A list of nodes representing a path, or None.

    Return a string showing the nodes in the path separated by '-->',
    or the string "None" if the path is None.
    """
    if path is None:
        return "Empty path"
    node_strs = []
    for node in path:
        node_strs.append(str(node))
    return "-->".join(node_strs)


def pathlist_to_string(queue):
    """
    Convert a list of paths into a string representation.

    Parameters:
        queue (list): A list of paths, where each path is a list of nodes.

    Return a string representation of the list of paths.
    """
    path_strs = []
    for path in queue:
        path_strs.append(path_to_string(path))
    return "[" + ", ".join(path_strs) + "]"


############################################################
# plotting and visualization helpers - DO NOT MODIFY
############################################################


def to_networkx_graph(graph):
    G = nx.DiGraph()
    for u in graph:
        for v, weight, edge_type in graph[u]:
            G.add_edge(u, v)
    return G


def grid_positions(n):
    """
    Generate positions for an n by n grid graph using node names "N0" ... "N(n*n - 1)".

    Parameters:
        n (int): The size of the grid.
    Return a dictionary mapping node names to (x, y) positions for plotting.
    """
    pos = {}
    for i in range(n * n):
        row = i // n
        col = i % n
        pos[f"N{i}"] = (col, -row)
    return pos


def time_pathfinding(algorithm, graph, start, goal):
    """
    Measure the runtime of a pathfinding algorithm.

    Parameters:
        algorithm (function): A pathfinding function that takes
            (graph, start, goal) as input.
        graph (dict): The graph dictionary to search.
        start: Starting node.
        goal: Target node.

    Return the runtime in seconds.
    """
    start_time = time.time()
    algorithm(graph, start, goal)
    end_time = time.time()
    return end_time - start_time


def visualize_graph_with_path(graph, path, start=None, goal=None, n=None):
    """
    Visualize a directed graph and highlight a given path.

    Parameters:
        graph (dict): A graph dictionary.
        path (list or None): Path to highlight.
        start: Starting node (optional).
        goal: Goal node (optional).
        n (int or None): Grid size if graph is an n x n grid.
    """
    G = nx.DiGraph()

    for u in graph:
        for v, weight, edge_type in graph[u]:
            G.add_edge(u, v, weight=weight)

    # Layout
    if n is not None:
        pos = grid_positions(n)
    else:
        pos = nx.spring_layout(G, seed=42)

    fig, ax = plt.subplots(figsize=(10, 6))

    path_nodes = set(path) if path is not None else set()

    # Node colors
    node_colors = []
    for node in G.nodes():
        if node == start:
            node_colors.append("green")
        elif node == goal:
            node_colors.append("orange")
        elif node in path_nodes:
            node_colors.append("lightcoral")
        else:
            node_colors.append("lightgray")

    # Draw base graph
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color=node_colors,
        node_size=800,
        edge_color="lightgray",
        width=1,
        arrows=True
    )

    # Highlight path edges (no arrows to avoid stacking)
    if path is not None:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=path_edges,
            edge_color="red",
            width=4,
            arrows=False,
            ax=ax
        )

    # Edge labels (weights)
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)

    # Create legend manually
    legend_elements = [
        Patch(facecolor="green", edgecolor="black", label="Start"),
        Patch(facecolor="orange", edgecolor="black", label="Goal"),
        Patch(facecolor="lightcoral", edgecolor="black", label="Path Node"),
        Patch(facecolor="lightgray", edgecolor="black", label="Other Node"),
        Patch(facecolor="red", edgecolor="red", label="Path Edge")
    ]

    ax.legend(
        handles=legend_elements,
        loc="center left",
        bbox_to_anchor=(1.02, 0.5),
        borderaxespad=0
    )

    ax.set_title("Graph Visualization with Highlighted Path")
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
