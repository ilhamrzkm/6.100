from functools import wraps
import unittest
import json
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
# test graph construction
############################################################


class BuildGraphBase(unittest.TestCase):

    def _edge_diff_message(self, expected_edges, actual_edges):
        # internal graph diff helper, indicates missing and extra edges for a specific node
        expected_set = set(expected_edges)
        actual_set = set(actual_edges)
        missing = expected_set - actual_set
        extra = actual_set - expected_set

        diff_msg = []
        if missing:
            diff_msg.append(f"missing edges: {sorted(missing)}")
        if extra:
            diff_msg.append(f"extra edges: {sorted(extra)}")

        return "\n".join(diff_msg)


    def _layered_adjacency_list(self, adjacency):
        # avoids penalizing students for ambiguous edge_type instructions for layered graphs
        return [(node, weight, "LAYERED") for node, weight, _ in adjacency]


    def assertGraphsEqual(self, expected, actual, layered=False):
        expected = { k : sorted(v) for k, v in expected.items() }
        actual = { k : sorted(v) for k, v in actual.items() }

        self.assertEqual(
            len(expected),
            len(actual),
            f"expected {len(expected)} nodes, got {len(actual)}. returned nodes:\n{list(actual.keys())}"
        )

        self.assertEqual(
            expected.keys(),
            actual.keys(),
        )

        for k in expected.keys():
            if layered:
                expected_k = self._layered_adjacency_list(expected[k])
                actual_k = self._layered_adjacency_list(actual[k])
            else:
                expected_k = expected[k]
                actual_k = actual[k]
            self.assertTrue(
                expected_k == actual_k,
                f"incorrect edges for node {k}:\n{self._edge_diff_message(expected_k, actual_k)}"
            )


    def load_expected_graph(self, name):
        with open(f"./tests_data/{name}.json") as f:
            data = json.load(f)
        return {
            node: [tuple(edge) for edge in edges]
            for node, edges in data.items()
        }


    def load_expected_graph_layered(self, name, tolls):
        # expects filename w/ number of layers, aka tolls+1
        with open(f"./tests_data/{name}_{tolls+1}_layers.json") as f:
            data = json.load(f)
        loaded = {}
        for node, edges in data:
            node = tuple(node)
            loaded[node] = []
            for edge in edges:
                loaded[node].append((tuple(edge[0]), edge[1], edge[2]))
        return loaded


@testsuite_options(4, 1)
class TestBuildGraphOneway(BuildGraphBase):

    @case_options(
        1,
        "Function 'build_graph' is not implemented correctly",
        "Error occurred while testing 'build_graph' on one-way roads",
    )
    def test_build_graph_oneway_1(self):
        name = "small_oneway" # this is only used in tests currently
        expected = self.load_expected_graph(name)
        actual = pset.build_graph(f"./tests_data/{name}.txt")
        self.assertGraphsEqual(expected, actual)


    @case_options(
        1,
        "Function 'build_graph' is not implemented correctly",
        "Error occurred while testing 'build_graph' on one-way roads",
    )
    def test_build_graph_oneway_2(self):
        name = "manhattan_5x5_oneway"
        expected = self.load_expected_graph(name)
        actual = pset.build_graph(f"./data/{name}.txt")
        self.assertGraphsEqual(expected, actual)


@testsuite_options(4, 1)
class TestBuildGraphTwoway(BuildGraphBase):

    @case_options(
        1,
        "Function 'build_graph' is not implemented correctly",
        "Error occurred while testing 'build_graph'",
    )
    def test_build_graph_twoway_1(self):
        name = "manhattan_5x5_twoway"
        expected = self.load_expected_graph(name)
        actual = pset.build_graph(f"./data/{name}.txt")
        self.assertGraphsEqual(expected, actual)


    @case_options(
        1,
        "Function 'build_graph' is not implemented correctly",
        "Error occurred while testing 'build_graph'",
    )
    def test_build_graph_twoway_2(self):
        name = "small_toll_test"
        expected = self.load_expected_graph(name)
        actual = pset.build_graph(f"./data/{name}.txt")
        self.assertGraphsEqual(expected, actual)


    @case_options(
        1,
        "Function 'build_graph' is not implemented correctly",
        "Error occurred while testing 'build_graph'",
    )
    def test_build_graph_twoway_3(self):
        name = "small_weighted_mixed"
        expected = self.load_expected_graph(name)
        actual = pset.build_graph(f"./data/{name}.txt")
        self.assertGraphsEqual(expected, actual)


############################################################
# test bfs
############################################################


class BFSBase(unittest.TestCase):

    def is_valid_path(self, graph, path):
        # not to be used for cases where we expect the path to not exist
        assert path, f"expected a nonempty path, got {path}"
        # checks if nodes exist in graph
        for node in path:
            assert node in graph, f"expected valid nodes, got a node that doesn't exist: {node}"
        # checks that edges exist between sequential nodes
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            neighbors = [n for (n, _, _) in graph[u]]
            assert v in neighbors, f"expected valid edges, got an edge that doesn't exist: {u} -> {v}"


@testsuite_options(4, 1)
class TestBFSOneWay(BFSBase):

    @case_options(
        1,
        "Function 'bfs' does not return a shortest path",
        "Error occurred while testing 'bfs'",
    )
    def test_bfs_one_way_path_shortest(self):
        name = "manhattan_5x5_oneway"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "N0", "N12")
        expected, actual = 4, len(path)-1
        self.assertEqual(
            expected,
            actual,
            f"expected path length {expected}, got {actual}. returned path:\n{path}"
        )


    @case_options(
        1,
        "Function 'bfs' does not return valid path",
        "Error occurred while testing 'bfs'",
    )
    def test_bfs_one_way_path_valid(self):
        name = "manhattan_5x5_oneway"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "N0", "N12")
        self.is_valid_path(graph, path)


    @case_options(
        1,
        "Function 'bfs' does not handle unreachable cases correctly",
        "Error occurred while testing unreachable BFS",
    )
    def test_bfs_one_way_unreachable(self):
        name = "manhattan_5x5_oneway"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "N12", "N0")
        self.assertIsNone(path)


@testsuite_options(4, 1)
class TestBFSTwoWay(BFSBase):

    @case_options(
        1,
        "Function 'bfs' does not return correct path",
        "Error occurred while testing 'bfs'",
    )
    def test_bfs_two_way_path_shortest_1(self):
        name = "manhattan_5x5_twoway"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "N2", "N22")
        expected, actual = 4, len(path)-1
        self.assertEqual(
            expected,
            actual,
            f"expected path length {expected}, got {actual}. returned path:\n{path}"
        )


    @case_options(
        1,
        "Function 'bfs' does not return valid path",
        "Error occurred while testing 'bfs'",
    )
    def test_bfs_two_way_path_valid_1(self):
        name = "manhattan_5x5_twoway"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "N2", "N22")
        self.is_valid_path(graph, path)


    @case_options(
        1,
        "Function 'bfs' does not return correct path",
        "Error occurred while testing 'bfs'",
    )
    def test_bfs_two_way_path_shortest_2(self):
        name = "small_toll_test"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "T2", "A")
        expected, actual = 2, len(path)-1
        self.assertEqual(
            expected,
            actual,
            f"expected path length {expected}, got {actual}. returned path:\n{path}"
        )


    @case_options(
        1,
        "Function 'bfs' does not return valid path",
        "Error occurred while testing 'bfs'",
    )
    def test_bfs_two_way_path_valid_2(self):
        name = "small_toll_test"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs(graph, "T2", "A")
        self.is_valid_path(graph, path)


############################################################
# test weighted graph expansion
############################################################


class ExpandEdgeBase(unittest.TestCase):

    def check_expanded_edge_chain(self, graph, u, v, weight):
        chain = [u]
        next_node = graph[u][0][0]
        chain.append(next_node)
        for _ in range(weight - 1):
            next_node = graph[next_node][0][0]
            chain.append(next_node)
        self.assertEqual(
            weight,
            len(chain)-1,
            f"expected {weight} edges from {u}->{v}, got {len(chain)-1}. full expansion: {chain}"
        )
        self.assertEqual(
            v, chain[-1], f"expected expansion to end at {v}, got {chain[-1]}. full expansion: \n{chain}"
        )


    def check_edge_weights(self, graph):
        for u, neighbors in graph.items():
            for [v, weight, _] in neighbors:
                self.assertEqual(1, weight, f"expected unit weight graph, got edge {u}->{v} with weight {weight}")


@testsuite_options(4, 1)
class TestExpandEdge(ExpandEdgeBase):

    @case_options(
        1,
        "Function 'expand_edge_iterative' is not implemented correctly",
        "Error occurred while testing 'expand_edge_iterative'",
    )
    def test_expand_edge_iterative_1(self):
        graph = {
            "A" : [],
            "B" : [("C", 1, "local")],
            "C" : [("B", 1, "local")],
        }
        pset.expand_edge_iterative(graph, "A", "C", 6)
        self.check_edge_weights(graph)


    @case_options(
        1,
        "Function 'expand_edge_iterative' is not implemented correctly",
        "Error occurred while testing 'expand_edge_iterative'",
    )
    def test_expand_edge_iterative_2(self):
        graph = {
            "A" : [],
            "B" : [("C", 1, "local")],
            "C" : [("B", 1, "local")],
        }
        pset.expand_edge_iterative(graph, "A", "C", 1)
        self.check_expanded_edge_chain(graph, "A", "C", 1)


    @case_options(
        1,
        "Function 'expand_edge_iterative' is not implemented correctly",
        "Error occurred while testing 'expand_edge_iterative'",
    )
    def test_expand_edge_iterative_3(self):
        graph = {
            "A" : [],
            "B" : [("C", 1, "local")],
            "C" : [("B", 1, "local")],
        }
        pset.expand_edge_iterative(graph, "A", "C", 3)
        self.check_expanded_edge_chain(graph, "A", "C", 3)


    @case_options(
        1,
        "Function 'expand_edge_recursive' is not implemented correctly",
        "Error occurred while testing 'expand_edge_recursive'",
    )
    def test_expand_edge_recursive_1(self):
        graph = {
            "A" : [],
            "B" : [("C", 1, "local")],
            "C" : [("B", 1, "local")],
        }
        pset.expand_edge_recursive(graph, "A", "C", 6)
        self.check_edge_weights(graph)


    @case_options(
        1,
        "Function 'expand_edge_recursive' is not implemented correctly",
        "Error occurred while testing 'expand_edge_recursive'",
    )
    def test_expand_edge_recursive_2(self):
        graph = {
            "A" : [],
            "B" : [("C", 1, "local")],
            "C" : [("B", 1, "local")],
        }
        pset.expand_edge_recursive(graph, "A", "C", 1)
        self.check_expanded_edge_chain(graph, "A", "C", 1)


    @case_options(
        1,
        "Function 'expand_edge_recursive' is not implemented correctly",
        "Error occurred while testing 'expand_edge_recursive'",
    )
    def test_expand_edge_recursive_3(self):
        graph = {
            "A" : [],
            "B" : [("C", 1, "local")],
            "C" : [("B", 1, "local")],
        }
        pset.expand_edge_recursive(graph, "A", "C", 3)
        self.check_expanded_edge_chain(graph, "A", "C", 3)


@testsuite_options(4, 1)
class TestWeightedExpansion(ExpandEdgeBase):

    @case_options(
        1,
        "Function 'expand_weighted_graph' is not implemented correctly",
        "Error occurred while testing 'expand_weighted_graph'",
    )
    def test_expand_weighted_graph_1(self):
        graph = {
            "A": [("B", 3, "one_way")],
            "B": [],
            "C": [("D", 3, "one_way")],
            "D": [("B", 1, "one_way")],
        }
        expanded = pset.expand_weighted_graph(graph, pset.expand_edge_iterative)
        self.check_edge_weights(expanded)


    @case_options(
        1,
        "Function 'expand_weighted_graph' is not implemented correctly",
        "Error occurred while testing 'expand_weighted_graph'",
    )
    def test_expand_weighted_graph_2(self):
        graph = {
            "A": [("B", 3, "one_way")],
            "B": [],
            "C": [("D", 7, "one_way")],
            "D": [("B", 1, "one_way")],
        }
        expanded = pset.expand_weighted_graph(graph, pset.expand_edge_recursive)
        self.check_edge_weights(expanded)
        self.check_expanded_edge_chain(expanded, "A", "B", 3)
        self.check_expanded_edge_chain(expanded, "C", "D", 7)


    @case_options(
        1,
        "Function 'expand_weighted_graph' is not implemented correctly",
        "Error occurred while testing 'expand_weighted_graph'",
    )
    def test_expand_weighted_graph_3(self):
        name = "small_weighted_mixed"
        graph = pset.build_graph(f"./data/{name}.txt")
        expanded = pset.expand_weighted_graph(graph, pset.expand_edge_iterative)
        self.check_edge_weights(expanded)
        self.check_expanded_edge_chain(expanded, "A", "B", 5)


############################################################
# test weighted shortest path
############################################################


@testsuite_options(4, 1)
class TestStripIntermediateNodes(unittest.TestCase):

    @case_options(
        1,
        "Function 'strip_intermediate_nodes' is not implemented correctly",
        "Error occurred while testing 'strip_intermediate_nodes'",
    )
    def test_strip_intermediate_nodes_1(self):
        graph = {
            "A": [("B", 3, "one_way")],
            "B": [],
        }
        expanded = pset.expand_weighted_graph(graph, pset.expand_edge_iterative)
        # allows us to test independent of student intermediate representation
        intermediate_1 = expanded["A"][0][0]
        intermediate_2 = expanded[intermediate_1][0][0]
        expanded_path = ["A", intermediate_1, intermediate_2, "B"]
        expected = ["A", "B"]
        actual = pset.strip_intermediate_nodes(expanded_path)
        self.assertEqual(
            expected,
            actual,
            f"expected {expanded_path} to reduce to {expected}, got {actual}"
        )


    @case_options(
        1,
        "Function 'strip_intermediate_nodes' is not implemented correctly",
        "Error occurred while testing 'strip_intermediate_nodes'",
    )
    def test_strip_intermediate_nodes_2(self):
        expected = None
        actual = pset.strip_intermediate_nodes(None)
        self.assertEqual(
            expected,
            actual,
            f"expected {None} (no valid path) to reduce to {expected}, got {actual}"
        )


@testsuite_options(4, 1)
class TestFindShortestPath(unittest.TestCase):

    @case_options(
        1,
        "Function 'find_shortest_path' is not implemented correctly",
        "Error occurred while testing 'find_shortest_path'",
    )
    def test_find_shortest_path_unweighted(self):
        filepath = "./data/small_toll_test.txt"
        expected = ["A", "B", "C"] # only path from A to C in this graph
        actual = pset.find_shortest_path(filepath, "A", "C")
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to C in small_toll_test"
        )


    @case_options(
        1,
        "Function 'find_shortest_path' is not implemented correctly",
        "Error occurred while testing 'find_shortest_path'",
    )
    def test_find_shortest_path_weighted_1(self):
        filepath = "./data/small_weighted_mixed.txt"
        expected = ["A", "B"] # only path from A to B in this graph
        actual = pset.find_shortest_path(filepath, "A", "B")
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to B in small_weighted_mixed"
        )


    @case_options(
        1,
        "Function 'find_shortest_path' is not implemented correctly",
        "Error occurred while testing 'find_shortest_path'",
    )
    def test_find_shortest_path_weighted_2(self):
        filepath = "./data/small_weighted_mixed.txt"
        expected = ["A", "C", "D", "E", "F"] # shortest path from A to F
        actual = pset.find_shortest_path(filepath, "A", "F")
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to F in small_weighted_mixed"
        )


############################################################
# test graph layering (tolls)
############################################################


@testsuite_options(4, 1)
class TestBuildLayeredGraph(BuildGraphBase):

    @case_options(
        1,
        "Function 'build_layered_graph_for_tolls' is not implemented correctly",
        "Error occurred while testing 'build_layered_graph_for_tolls'",
    )
    def test_build_layered_graph_for_tolls(self):
        name = "small_toll_test"
        graph = pset.build_graph(f"./data/{name}.txt")
        tolls = 1
        toll_graph = pset.build_layered_graph_for_tolls(graph, tolls)
        expected = self.load_expected_graph_layered(name, tolls)
        self.assertGraphsEqual(expected, toll_graph, layered=True)


@testsuite_options(4, 1)
class TestStripTollState(unittest.TestCase):

    @case_options(
        1,
        "Function 'strip_toll_state' is not implemented correctly",
        "Error occurred while testing 'strip_toll_state'",
    )
    def test_strip_toll_state(self):
        path = [("A", 0), ("B", 0), ("C", 1), ("D", 2), ("E", 2), ("F", 2)]
        expected = ["A", "B", "C", "D", "E", "F"]
        actual = pset.strip_toll_state(path)
        self.assertEqual(
            expected,
            actual,
            f"expected path {path} to reduce to {expected}, got {actual}"
        )


@testsuite_options(4, 1)
class TestFindShortestPathTolls(unittest.TestCase):

    @case_options(
        1,
        "Function 'find_shortest_path_with_tolls' is not implemented correctly",
        "Error occurred while testing 'find_shortest_path_with_tolls'",
    )
    def test_find_shortest_path_with_tolls_1(self):
        filepath = "./data/small_toll_test.txt"
        tolls = 10
        expected = (["A", "T1", "T2", "E"], ["A", "T1", "D", "E"]) # 2 options
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls)
        self.assertTrue(
            actual == expected[0] or actual == expected[1],
            f"expected {expected[0]} or {expected[1]}, got {actual} for shortest path from A to E in small_toll_test, >1 tolls allowed"
        )


    @case_options(
        1,
        "Function 'find_shortest_path_with_tolls' is not implemented correctly",
        "Error occurred while testing 'find_shortest_path_with_tolls'",
    )
    def test_find_shortest_path_with_tolls_2(self):
        filepath = "./data/small_toll_test.txt"
        tolls = 1
        expected = ["A", "T1", "D", "E"]
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to E in small_toll_test, 1 toll allowed"
        )


    @case_options(
        1,
        "Function 'find_shortest_path_with_tolls' is not implemented correctly",
        "Error occurred while testing 'find_shortest_path_with_tolls'",
    )
    def test_find_shortest_path_with_tolls_3(self):
        filepath = "./data/small_toll_test.txt"
        tolls = 0
        expected = ["A", "B", "C", "D", "E"]
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to E in small_toll_test, no tolls allowed"
        )

    @case_options(
        1,
        "Function 'find_shortest_path_with_tolls' does not correctly handle weighted toll graphs",
        "Error occurred while testing weighted toll shortest paths",
    )
    def test_find_shortest_path_with_tolls_weighted_0(self):
        filepath = "./tests_data/small_toll_test_weighted.txt"
        tolls = 0
        expected = ["A", "B", "E"]
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to E with no tolls allowed"
        )


    @case_options(
        1,
        "Function 'find_shortest_path_with_tolls' does not correctly handle weighted toll graphs",
        "Error occurred while testing weighted toll shortest paths",
    )
    def test_find_shortest_path_with_tolls_weighted_1(self):
        filepath = "./tests_data/small_toll_test_weighted.txt"
        tolls = 1
        expected = ["A", "C", "E"]
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to E with one toll allowed"
        )


    @case_options(
        1,
        "Function 'find_shortest_path_with_tolls' does not correctly handle weighted toll graphs",
        "Error occurred while testing weighted toll shortest paths",
    )
    def test_find_shortest_path_with_tolls_weighted_2(self):
        filepath = "./tests_data/small_toll_test_weighted.txt"
        tolls = 2
        expected = ["A", "C", "E"]
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to E with two tolls allowed"
        )


############################################################
# test bfs with predecessors
############################################################


@testsuite_options(4, 1)
class TestReconstructPath(unittest.TestCase):

    @case_options(
        1,
        "Function 'reconstruct_path' is not implemented correctly",
        "Error occurred while testing 'reconstruct_path'",
    )
    def test_reconstruct_path_1(self):
        pred = {
            "N1":"N0", "N2":"N1", "N5":"N0", "N6":"N5", "N7":"N6", "N10":"N5", "N11":"N6"
        }
        start, goal = "N0", "N11"
        expected = ["N0", "N5", "N6", "N11"]
        actual = pset.reconstruct_path(pred, start, goal)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual}. pred: \n{pred}"
        )


    @case_options(
        1,
        "Function 'reconstruct_path' is not implemented correctly",
        "Error occurred while testing 'reconstruct_path'",
    )
    def test_reconstruct_path_2(self):
        pred = {
            ("B",0):("A",0), ("C",0):("B",0), ("D",0):("C",0), ("T",1):("A",0), ("D",1):("T",1), "N6100":("D",1)
        }
        start, goal = ("A",0), "N6100"
        expected = [("A",0), ("T",1), ("D",1), "N6100"]
        actual = pset.reconstruct_path(pred, start, goal)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual}. pred: \n{pred}"
        )


@testsuite_options(4, 1)
class TestBFSPredecessors(BFSBase):

    @case_options(
        1,
        "Function 'bfs_predecessors' is not implemented correctly",
        "Error occurred while testing 'bfs_predecessors'",
    )
    def test_bfs_predecessors_1(self):
        graph = {
            "A": [("B", 1, "one_way")],
            "B": [("C", 1, "one_way")],
            "C": [],
        }
        expected = ["A","B","C"]
        actual = pset.bfs_predecessors(graph, "A", "C")
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to C in the following graph: \n{graph}"
        )


    @case_options(
        1,
        "Function 'bfs_predecessors' is not implemented correctly",
        "Error occurred while testing 'bfs_predecessors'",
    )
    def test_bfs_predecessors_2(self):
        name = "manhattan_5x5_oneway"
        graph = pset.build_graph(f"./data/{name}.txt")
        path = pset.bfs_predecessors(graph, "N0", "N12")
        self.is_valid_path(graph, path)
        expected, actual = 4, len(path)-1
        self.assertEqual(
            expected,
            actual,
            f"expected path length {expected}, got {actual}. returned path:\n{path}"
        )


    @case_options(
        1,
        "Function 'bfs_predecessors' is not implemented correctly",
        "Error occurred while testing 'bfs_predecessors'",
    )
    def test_bfs_predecessors_weighted(self):
        # same test as test_find_shortest_path_weighted_2, just w/ bfs_predecessors
        filepath = "./data/small_weighted_mixed.txt"
        expected = ["A", "C", "D", "E", "F"] # shortest path from A to F
        actual = pset.find_shortest_path(filepath, "A", "F", pset.bfs_predecessors)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to F in small_weighted_mixed"
        )


    @case_options(
        1,
        "Function 'bfs_predecessors' is not implemented correctly",
        "Error occurred while testing 'bfs_predecessors'",
    )
    def test_bfs_predecessors_tolls(self):
        # same test as test_find_shortest_path_with_tolls_2, just w/ bfs_predecessors
        filepath = "./data/small_toll_test.txt"
        tolls = 1
        expected = ["A", "T1", "D", "E"]
        actual = pset.find_shortest_path_with_tolls(filepath, "A", "E", tolls, pset.bfs_predecessors)
        self.assertEqual(
            expected,
            actual,
            f"expected {expected}, got {actual} for shortest path from A to E in small_toll_test, 1 toll allowed"
        )


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
        TestBuildGraphOneway,
        TestBFSOneWay,
        TestBuildGraphTwoway,
        TestBFSTwoWay,
        TestExpandEdge,
        TestWeightedExpansion,
        TestStripIntermediateNodes,
        TestFindShortestPath,
        TestBuildLayeredGraph,
        TestStripTollState,
        TestFindShortestPathTolls,
        TestReconstructPath,
        TestBFSPredecessors,
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
