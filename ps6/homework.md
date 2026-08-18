# Problem Set 6 — Packing Bags (Knapsack / DP)

Pack items into a carry-on (volume limit) and a checked bag (weight limit) to maximize value. Some items cannot go in one of the bags. Later, some items must be taken as a pair.

```bash
python3 test.py
```

Do not modify `Item.__str__`.

## 1. `Item`

Store `name`, `value`, `volume`, `weight`, `cannot_carry`, `cannot_check`, and `pair` (default `None`).

- If `cannot_carry` **and** `cannot_check` are both True, raise `ValueError`.
- Getters: `get_name`, `get_value`, `get_volume`, `get_weight`, `cannot_carry`, `cannot_check`.
- `get_info()` returns `(value, volume, weight, cannot_carry, cannot_check)`.
- `set_pair` / `get_pair` for Section 5.

You can implement `get_pair` / `get_branches` when you reach pairs; earlier tests do not need branches.

## 2. Exhaustive search

### `all_packing_combinations(items)`

Each item: skip, carry-on, or checked. Recurse. **Do not** filter capacities or restrictions here.

Base case: no items → `[{"carry": [], "checked": []}]`. Length should be `3 ** n`.

### `choose_packing_exhaustive(items, v_cap, w_cap)`

Among those combos, keep the feasible one with maximum total value:

- No `cannot_carry` item in carry-on.
- No `cannot_check` item in checked.
- Sum of carry-on volumes ≤ `v_cap`.
- Sum of checked weights ≤ `w_cap`.

Return `{"value": int, "carry": [...], "checked": [...]}`. If nothing packs, value 0 and empty lists.

## 3. Dynamic programming

### `choose_packing_dp(items, v_cap, w_cap)`

Same optimum, without listing `3^n` packings.

Think in subproblems: remaining items from index `i`, leftover volume, leftover weight.

For item `i` you may:

1. Skip it.
2. Put it in carry-on if allowed and volume fits.
3. Put it in checked if allowed and weight fits.

Memoize on `(index, remaining_volume, remaining_weight)`. Rebuild the carry/checked lists when you take a branch.

Should match exhaustive on small instances and run on larger ones.

## 4. Pairs

Paired items must **both be packed or both left out**. They may go in different bags.

### `group_pairs(items)`

Return a new list of the same Item objects so each pair sits in adjacent positions (first of the pair, then its partner). Unpaired items stay as singletons. Do not duplicate items.

### `Item.get_branches()`

List of dicts `{"value", "volume", "weight"}` for legal choices of this item (and its pair if any):

**No pair** — up to 3 branches:

- skip: all zeros
- carry (if allowed): this item's value and volume, weight 0
- check (if allowed): this item's value and weight, volume 0

**Has a pair** — up to 5 joint branches:

- skip both
- both carry (if both allowed)
- both check (if both allowed)
- this carry + pair check (if those bag types are allowed)
- this check + pair carry (if those bag types are allowed)

When both packed, value is the **sum**. Volume/weight are only from the bag they actually go into.

### `choose_packing_dp_with_pair`

Group first. DP over the grouped list: if the current item has a pair, the next index skips **two** items; otherwise one.

For each branch, if volume/weight fit, recurse and add this branch's items into carry/checked.

## 5. Experiments (not autograded)

Fill in `experiment1_runtime_vs_items` (exhaustive vs DP vs `n`) and `experiment2_dp_vs_discreteness` (DP vs how coarse volume/weight are). Exhaustive should explode with `n`; DP should get faster when values are multiples of a large divisor (fewer distinct remaining-capacity states).

## Suggested order

Item class → combinations → exhaustive filter → DP → pairs / branches / grouped DP → runtime plots.
