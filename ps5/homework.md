# Problem Set 5: Drawing the Districts

## Introduction

A reporter from *The Tech* drops a folder on your desk. Inside: a map of towns, each with a population and a two-party split, plus a proposed number of districts.

“The legislature says every district is compact and about the same size,” they say. “They also say the map is fair. Can a computer tell the difference between a fair map and a gerrymander?”

This problem set will not settle Massachusetts politics. It will, however, force you to **enumerate every legal district** under population and compactness rules, then assemble those districts into full partitions of the state, then count how often each party would win.

Start with `mini_1`. If your first version is a naive powerset, it will work on the toy map and collapse on `large_1`. That is the point: you will prune.

JSON files in `data/` describe a map. `read_data_from_file` returns `(graph_filepath, num_districts, town_populations, voter_proportions)`. Graph files in `graphs/` list cliques of mutually neighboring towns (comma-separated names per line).

Tally helpers (`tally_party_votes`, `tally_popular_votes`, `tally_district_outcomes`, `tally_partition_outcomes`) are provided. Do not change them.

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Build an undirected graph from clique lists
- Generate combinations recursively (with and without pruning)
- Test compactness using distances in an induced subgraph
- Assemble disjoint districts into partitions of all towns
- Compare popular vote to district-level outcomes

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Run the staff tests from this folder:

```bash
python3 test.py
```

The recursion limit is already raised for large maps.

---

## Problem 1: Who borders whom?

### 1.1) `create_graph(filename)`

Build an undirected adjacency list.

Each line is a group of towns that all neighbor each other. For every pair on a line, add both directions. Every town that appears should be a key even if it ends up with no extra neighbors.

**Hint:** A line `A,B,C` means A–B, A–C, and B–C, each as two directed adjacency entries.

---

## Problem 2: Districts that are the right size

Average district population is `total_population / num_districts`. A set of towns is allowed if its population is within **10%** of that average (inclusive): `[0.9 * avg, 1.1 * avg]`.

Too small, and a district is underrepresented. Too large, and you have packed voters. The 10% band is this problem set’s stand-in for “roughly equal population.”

### 2.1) `powerset(items)`

All subsets, including `{}` and the full set. Recurse: with/without the first item.

### 2.2) `compute_town_combos_naive(...)`

Generate the powerset of town names, keep sets whose population is in range. Empty set is usually invalid unless the range includes 0.

This version is the honest-but-slow census: try everything.

---

## Problem 3: Compactness — no salamander districts

A district that is a thin strip connecting distant towns can still hit the population target. Compactness is how this problem set forbids that cartoon.

A district is compact if **every pair** of its towns is at most `max_distance` edges apart **in the subgraph induced by those towns** (not in the full state graph). Using the full graph would let you “hop” through towns you did not include in the district.

### 3.1) `create_subgraph(graph, nodes)`

Keep only listed nodes; neighbor lists should only include neighbors that are also in `nodes`.

### 3.2) `find_nodes_within_distance(graph, start, depth)`

BFS (or equivalent) from `start`, at most `depth` hops. Return a **set** that includes `start` (distance 0).

### 3.3) `is_compact(graph, towns, max_distance)`

For each town in the district, the nodes reachable within `max_distance` in the subgraph must include every other town in the district.

### 3.4) `compute_valid_districts(...)`

Take population-valid combos from `compute_town_combos`, keep those that are compact.

**Hint:** Compactness is all-pairs, but you can check it as “from every town, can I reach everyone else within `max_distance`?”

---

## Problem 4: Pruning the combination tree

Naive powerset explodes. Instead, walk a decision tree: take or skip each town, and **stop taking** once you would blow the population cap.

### 4.1) `town_combos_helper(towns, (lower, upper), populations)`

- If no towns left: return `[{}]` if `lower <= 0` (you already met the minimum), else `[]`.
- Skip the first town always (bounds unchanged).
- If taking it would exceed `upper`, do not take it.
- Otherwise recurse with bounds decreased by that town’s population, then add the town into every set from that branch.

### 4.2) `compute_town_combos_pruning(...)`

Compute the same `[0.9 avg, 1.1 avg]` bounds and call the helper. Results should match naive on small maps and finish on `large_1`.

**Hint:** The empty set in the base case is not “a district with no towns.” It is the suffix of a combination you have already built. Adding the current town to every set from the take-branch is how the set grows on the way back up.

---

## Problem 5: Partitions — covering the whole state

A legal map is not one district. It is `num_districts` **disjoint** districts whose union is **every** town. No town left behind, no town in two districts.

### 5.1) `valid_partitions_helper(candidate_districts, num_districts, towns)`

`towns` is the set still uncovered.

- No candidates left: success if `num_districts == 0` and `towns` is empty (`[[]]` to build on), else `[]`.
- Skip the first candidate always.
- Take it only if it is a subset of remaining towns; then recurse with `num_districts - 1` and `towns - first`.

### 5.2) `compute_valid_partitions(graph, num_districts, candidate_districts)`

Call the helper with `towns = set(graph)`.

---

## Problem 6: Who would win?

Now the reporter’s question: if every legal partition is equally imaginable, how often does each party take more districts? How does that compare to the statewide popular vote?

### 6.1) `analyze_voting_outcomes(...)`

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

If the popular vote is close to even but one party wins almost every partition, you have found the shape of a gerrymander — or at least of a map that *could* be one.

---

## Suggested order

Graph → naive combos → subgraph / distance / compactness → valid districts → pruned combos → partitions → voting analysis.
