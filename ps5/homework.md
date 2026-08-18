# Problem Set 5 — Gerrymandering with Search and Pruning

Enumerate legal voting districts under population and compactness rules, then see how often each party would win.

```bash
python3 test.py
```

JSON files in `data/` describe a map. `read_data_from_file` returns `(graph_filepath, num_districts, town_populations, voter_proportions)`. Graph files in `graphs/` list cliques of mutually neighboring towns (comma-separated names per line). Start with `mini_1`.

Tally helpers (`tally_party_votes`, `tally_popular_votes`, `tally_district_outcomes`, `tally_partition_outcomes`) are provided. Do not change them.

## 1. `create_graph(filename)`

Build an undirected adjacency list.

Each line is a group of towns that all neighbor each other. For every pair on a line, add both directions. Every town that appears should be a key even if it ends up with no extra neighbors.

## 2. Population-feasible town sets

Average district population is `total_population / num_districts`. A set of towns is allowed if its population is within **10%** of that average (inclusive): `[0.9 * avg, 1.1 * avg]`.

### `powerset(items)`

All subsets, including `{}` and the full set. Recurse: with/without the first item.

### `compute_town_combos_naive(...)`

Generate the powerset of town names, keep sets whose population is in range. Empty set is usually invalid unless the range includes 0.

## 3. Compactness

A district is compact if **every pair** of its towns is at most `max_distance` edges apart **in the subgraph induced by those towns** (not in the full state graph).

### `create_subgraph(graph, nodes)`

Keep only listed nodes; neighbor lists should only include neighbors that are also in `nodes`.

### `find_nodes_within_distance(graph, start, depth)`

BFS (or equivalent) from `start`, at most `depth` hops. Return a **set** that includes `start` (distance 0).

### `is_compact(graph, towns, max_distance)`

For each town in the district, the nodes reachable within `max_distance` in the subgraph must include every other town in the district.

### `compute_valid_districts(...)`

Take population-valid combos from `compute_town_combos`, keep those that are compact.

## 4. Pruned combination search

Naive powerset explodes. Instead, walk a decision tree: take or skip each town.

### `town_combos_helper(towns, (lower, upper), populations)`

- If no towns left: return `[{}]` if `lower <= 0` (you already met the minimum), else `[]`.
- Skip the first town always (bounds unchanged).
- If taking it would exceed `upper`, do not take it.
- Otherwise recurse with bounds decreased by that town's population, then add the town into every set from that branch.

### `compute_town_combos_pruning(...)`

Compute the same `[0.9 avg, 1.1 avg]` bounds and call the helper. Results should match naive on small maps and finish on `large_1`.

## 5. Partitions

A partition is `num_districts` **disjoint** districts whose union is **every** town.

### `valid_partitions_helper(candidate_districts, num_districts, towns)`

`towns` is the set still uncovered.

- No candidates left: success if `num_districts == 0` and `towns` is empty (`[[]]` to build on), else `[]`.
- Skip the first candidate always.
- Take it only if it is a subset of remaining towns; then recurse with `num_districts - 1` and `towns - first`.

### `compute_valid_partitions(graph, num_districts, candidate_districts)`

Call the helper with `towns = set(graph)`.

## 6. `analyze_voting_outcomes(...)`

Use pruning to get valid districts, then partitions. Return:

```python
{
    "proportion_party1_total_votes": round(party1 / (party1 + party2), 3),
    "num_partitions": ...,
    "partition_party1_wins": ...,  # more districts than party 2
    "partition_party2_wins": ...,
    "partition_ties": ...,
}
```

Use the tally helpers. Popular vote uses `tally_popular_votes`. Partition winners use `tally_partition_outcomes`.

## Suggested order

Graph → naive combos → subgraph / distance / compactness → valid districts → pruned combos → partitions → voting analysis. Recursion limit is already raised for large maps.
