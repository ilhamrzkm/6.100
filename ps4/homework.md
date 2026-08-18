# Problem Set 4 — Graphs, BFS, Weights, and Tolls

Build graphs from files, search them with BFS, then handle edge weights and toll limits by transforming the graph.

```bash
python3 test.py
```

Use `neighbors(graph, node)` from `utils.py`. Graph values are lists of `(neighbor, weight, edge_type)` with `edge_type` in `{"one_way", "local", "toll"}`.

## 1. `build_graph(filepath)`

Each non-blank line is: `node1 node2 edge_type weight`.

- Every node that appears should be a key. Isolated nodes map to `[]`.
- `"one_way"`: only `node1 → node2`.
- `"local"` and `"toll"`: **both** directions, same weight and type.

## 2. `bfs(graph, start, goal)`

Unweighted shortest path (treat every edge as weight 1). Return a node list or `None`.

- If `start == goal`, return `[start]`.
- Standard BFS: queue of paths **or** a predecessor map. Mark visited when you first discover a node.
- On the one-way 5×5 grid, `N0 → N24` has 9 nodes (8 moves). `N24 → N0` is impossible. On the two-way grid both directions work.

## 3. Weighted search via expansion

BFS ignores weights, so expand a weight-`w` edge into a chain of `w` unit edges.

### `expand_edge_iterative` / `expand_edge_recursive`

Mutate `expanded_graph`. Original nodes should already exist as keys.

- Weight 1: append `(v, 1, "local")` to `u`.
- Weight `w > 1`: introduce `w-1` intermediate nodes and unit edges `u → … → v`.
- Intermediate names must be unique per original edge (include both `u` and `v` in the name). Tests do not require a specific naming scheme.

Recursive version: add one hop, recurse with `weight - 1`.

### `expand_weighted_graph(weighted_graph, expand_edge_fn)`

Copy all original nodes, then expand every outgoing edge with `expand_edge_fn`.

### `strip_intermediate_nodes(path)`

Drop intermediates from a BFS path. `None` stays `None`.

### `find_shortest_path(...)`

`build_graph` → expand → BFS → strip. On `small_weighted_mixed.txt`, A to F should be `A→C→D→E→F`, **not** the unweighted `A→B→F`.

## 4. Toll constraint (graph layering)

State is `(node, tolls_used)`.

### `build_layered_graph_for_tolls(graph, max_tolls)`

Layers `t = 0 … max_tolls`.

- Non-toll edge `u → v` at layer `t` stays at `t`.
- Toll edge `u → v` at layer `t` goes to `t+1` **only if** `t < max_tolls`.

Neighbor entries look like `((neighbor, new_t), weight, edge_type)`.

### `strip_toll_state(path)`

Map `(node, t)` → `node`. Leave plain strings alone (expanded intermediates). `None` → `None`.

### `find_shortest_path_with_tolls(...)`

Layer, then expand weights, then search.

The goal can be reached with **any** toll count `0 … max_tolls`. One approach: add a dummy sink connected from every `(goal, t)`, search to the sink, then strip the sink, toll state, and intermediates.

On `small_toll_test.txt`, A→E with `max_tolls=0` uses no tolls (`A→B→C→D→E`). With 1 toll, a shorter path using T1 is allowed.

## 5. Faster BFS

### `reconstruct_path(pred, start, goal)`

Walk predecessors from `goal` back to `start`, then reverse.

### `bfs_predecessors`

Same result as `bfs`, but store `pred[neighbor] = node` instead of copying whole paths. Should be faster on large grids.

### `generate_grid_graph` (debug this)

Staff code is buggy. `"up"` currently uses `if row >= 0`, which invents neighbors above row 0. Fix the bound.

Then run `compare_bfs_implementations` to plot path-copying BFS vs predecessor BFS.

## Suggested order

`build_graph` → `bfs` → edge expansion → `find_shortest_path` → layered tolls → predecessor BFS → fix the grid bug.
