# Problem Set 6: Two Bags at Logan

## Introduction

Winter break. You are at Logan, staring at a pile of stuff that will not all fit. The carry-on has a **volume** limit (the bag has to close). The checked bag has a **weight** limit (the airline will charge you, or refuse it). Some items are liquids and cannot go in the cabin. Some are fragile and cannot go underneath. Everything has a “how much I care about bringing this” value.

This is a knapsack problem with two knapsacks and extra rules. You will first try every packing (there are `3^n` of them: skip, carry, or check). Then you will compute the same optimum with dynamic programming so that a realistic closet does not take until next semester. Finally, your roommate appears with a paired gift: **both pieces travel, or neither does**.

Do not modify `Item.__str__`.

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Design a small class with getters and an invariant
- Enumerate combinations recursively
- Replace exponential search with memoized DP
- Group paired decisions so DP still has a clean subproblem

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Run the staff tests from this folder:

```bash
python3 test.py
```

---

## Problem 1: Modeling an item

### 1.1) `Item`

Store `name`, `value`, `volume`, `weight`, `cannot_carry`, `cannot_check`, and `pair` (default `None`).

- If `cannot_carry` **and** `cannot_check` are both True, raise `ValueError`. (If it cannot go in either bag, it does not belong in this packing problem.)
- Getters: `get_name`, `get_value`, `get_volume`, `get_weight`, `cannot_carry`, `cannot_check`.
- `get_info()` returns `(value, volume, weight, cannot_carry, cannot_check)`.
- `set_pair` / `get_pair` for Problem 4.

You can implement `get_pair` / `get_branches` when you reach pairs; earlier tests do not need branches.

---

## Problem 2: Try every packing

At the curb, there are three choices per item. Ignore the airline’s limits first; just list the worlds.

### 2.1) `all_packing_combinations(items)`

Each item: skip, carry-on, or checked. Recurse. **Do not** filter capacities or restrictions here.

Base case: no items → `[{"carry": [], "checked": []}]`. Length should be `3 ** n`.

### 2.2) `choose_packing_exhaustive(items, v_cap, w_cap)`

Among those combos, keep the feasible one with maximum total value:

- No `cannot_carry` item in carry-on.
- No `cannot_check` item in checked.
- Sum of carry-on volumes ≤ `v_cap`.
- Sum of checked weights ≤ `w_cap`.

Return `{"value": int, "carry": [...], "checked": [...]}`. If nothing packs, value 0 and empty lists.

**Hint:** Generate first, filter second. That split makes the DP version easier to think about later: DP will refuse illegal branches instead of listing them.

---

## Problem 3: Dynamic programming

`3^n` is a cute demo and a terrible way to pack 20 souvenirs. Think in subproblems: remaining items from index `i`, leftover volume, leftover weight.

### 3.1) `choose_packing_dp(items, v_cap, w_cap)`

Same optimum, without listing `3^n` packings.

For item `i` you may:

1. Skip it.
2. Put it in carry-on if allowed and volume fits.
3. Put it in checked if allowed and weight fits.

Memoize on `(index, remaining_volume, remaining_weight)`. Rebuild the carry/checked lists when you take a branch.

Should match exhaustive on small instances and run on larger ones.

**Hint:** The value of a subproblem is the best total value you can still get. When you take an item, add its value to the recursive result and prepend the item onto `carry` or `checked`.

---

## Problem 4: The paired gift

Paired items must **both be packed or both left out**. They may go in different bags (one in the cabin, one below). Unpaired items are unchanged.

### 4.1) `group_pairs(items)`

Return a new list of the same Item objects so each pair sits in adjacent positions (first of the pair, then its partner). Unpaired items stay as singletons. Do not duplicate items.

### 4.2) `Item.get_branches()`

List of dicts `{"value", "volume", "weight"}` for legal choices of this item (and its pair if any):

**No pair** — up to 3 branches:

- skip: all zeros
- carry (if allowed): this item’s value and volume, weight 0
- check (if allowed): this item’s value and weight, volume 0

**Has a pair** — up to 5 joint branches:

- skip both
- both carry (if both allowed)
- both check (if both allowed)
- this carry + pair check (if those bag types are allowed)
- this check + pair carry (if those bag types are allowed)

When both packed, value is the **sum**. Volume/weight are only from the bag they actually go into.

### 4.3) `choose_packing_dp_with_pair`

Group first. DP over the grouped list: if the current item has a pair, the next index skips **two** items; otherwise one.

For each branch, if volume/weight fit, recurse and add this branch’s items into carry/checked.

**Hint:** `get_branches` is the interface that lets DP treat a pair as one decision. The index skip of 2 is what keeps you from packing the partner twice.

---

## Problem 5: Experiments (not autograded)

Fill in `experiment1_runtime_vs_items` (exhaustive vs DP vs `n`) and `experiment2_dp_vs_discreteness` (DP vs how coarse volume/weight are). Exhaustive should explode with `n`; DP should get faster when values are multiples of a large divisor (fewer distinct remaining-capacity states).

These plots are how you *see* why the algorithm change mattered at the curb.

---

## Suggested order

Item class → combinations → exhaustive filter → DP → pairs / branches / grouped DP → runtime plots.
