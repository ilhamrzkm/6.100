# Problem Set 4: Getting There from Here

## Introduction

You have a flight out of Logan and a limited number of tolls left on your transponder. The map is a tangle of one-way streets, local roads, and Mass Pike ramps. Google would just tell you the answer. In 6.100, you will **build the map, search it, and then change the map** so that an ordinary unweighted search can respect travel times and toll budgets.

The same code should also work on a tiny Manhattan grid (the kind of toy city a mapping intern uses to debug pathfinding). If you can get from `N0` to `N24` on a one-way 5×5, and you can refuse a path that burns too many tolls, you can get a student to the airport.

Use `neighbors(graph, node)` from `utils.py`. Graph values are lists of `(neighbor, weight, edge_type)` with `edge_type` in `{"one_way", "local", "toll"}`.

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Build a graph from a text file
- Implement BFS for unweighted shortest paths
- Reduce weighted shortest paths to unweighted BFS by expanding edges
- Encode a constraint (max tolls) as extra graph layers
- Compare a slow BFS with a predecessor-map BFS

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Run the staff tests from this folder:

```bash
python3 test.py
```

---

## Problem 1: Reading the map

### 1.1) `build_graph(filepath)`

Each non-blank line is: `node1 node2 edge_type weight`.

- Every node that appears should be a key. Isolated nodes map to `[]`.
- `"one_way"`: only `node1 → node2`.
- `"local"` and `"toll"`: **both** directions, same weight and type.

**Hint:** A two-way street is two outgoing edges. Do not forget to create a key for a node that is only ever a destination.

---

## Problem 2: Unweighted shortest path

Treat every edge as one hop. This is the “fewest turns” version of the trip, ignoring how long each block actually takes.

### 2.1) `bfs(graph, start, goal)`

Return a node list or `None`.

- If `start == goal`, return `[start]`.
- Standard BFS: queue of paths **or** a predecessor map. Mark visited when you first discover a node.
- On the one-way 5×5 grid, `N0 → N24` has 9 nodes (8 moves). `N24 → N0` is impossible. On the two-way grid both directions work.

**Hint:** If you mark a node visited only when you pop it, you can enqueue the same node many times. Mark it when you first discover it.

---

## Problem 3: When blocks are not the same length

BFS ignores weights, so a two-minute local road and a ten-minute tunnel look identical. The trick: expand a weight-`w` edge into a chain of `w` unit edges. Then BFS on the expanded graph is a shortest *time* path.

### 3.1) `expand_edge_iterative` / `expand_edge_recursive`

Mutate `expanded_graph`. Original nodes should already exist as keys.

- Weight 1: append `(v, 1, "local")` to `u`.
- Weight `w > 1`: introduce `w-1` intermediate nodes and unit edges `u → … → v`.
- Intermediate names must be unique per original edge (include both `u` and `v` in the name). Tests do not require a specific naming scheme.

Recursive version: add one hop, recurse with `weight - 1`.

### 3.2) `expand_weighted_graph(weighted_graph, expand_edge_fn)`

Copy all original nodes, then expand every outgoing edge with `expand_edge_fn`.

### 3.3) `strip_intermediate_nodes(path)`

Drop intermediates from a BFS path. `None` stays `None`.

### 3.4) `find_shortest_path(...)`

`build_graph` → expand → BFS → strip. On `small_weighted_mixed.txt`, A to F should be `A→C→D→E→F`, **not** the unweighted `A→B→F`.

**Hint:** The expanded graph is a modeling trick. The path you return to the traveler should only contain real intersections.

---

## Problem 4: You only have so many tolls

Your transponder will cover at most `max_tolls` toll segments. After that, those ramps might as well not exist. One clean way to encode “I have used `t` tolls so far” is **graph layering**: each state is `(node, tolls_used)`.

### 4.1) `build_layered_graph_for_tolls(graph, max_tolls)`

Layers `t = 0 … max_tolls`.

- Non-toll edge `u → v` at layer `t` stays at `t`.
- Toll edge `u → v` at layer `t` goes to `t+1` **only if** `t < max_tolls`.

Neighbor entries look like `((neighbor, new_t), weight, edge_type)`.

### 4.2) `strip_toll_state(path)`

Map `(node, t)` → `node`. Leave plain strings alone (expanded intermediates). `None` → `None`.

### 4.3) `find_shortest_path_with_tolls(...)`

Layer, then expand weights, then search.

The goal can be reached with **any** toll count `0 … max_tolls`. One approach: add a dummy sink connected from every `(goal, t)`, search to the sink, then strip the sink, toll state, and intermediates.

On `small_toll_test.txt`, A→E with `max_tolls=0` uses no tolls (`A→B→C→D→E`). With 1 toll, a shorter path using T1 is allowed.

**Hint:** Layering turns a constraint into ordinary graph reachability. BFS does not need to know what a toll is.

---

## Problem 5: BFS that does not copy whole paths

Copying a path at every hop is simple and slow. On a large grid, store predecessors instead.

### 5.1) `reconstruct_path(pred, start, goal)`

Walk predecessors from `goal` back to `start`, then reverse.

### 5.2) `bfs_predecessors`

Same result as `bfs`, but store `pred[neighbor] = node` instead of copying whole paths. Should be faster on large grids.

### 5.3) `generate_grid_graph` (debug this)

Staff code is buggy. `"up"` currently uses `if row >= 0`, which invents neighbors above row 0. Fix the bound.

Then run `compare_bfs_implementations` to plot path-copying BFS vs predecessor BFS. The plot is how you convince yourself the faster version is worth writing.

---

## Suggested order

`build_graph` → `bfs` → edge expansion → `find_shortest_path` → layered tolls → predecessor BFS → fix the grid bug.
