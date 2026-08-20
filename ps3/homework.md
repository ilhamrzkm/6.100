# Problem Set 3: Is the Trend Real?

## Introduction

A UROP supervisor slides two CSVs across the table. One is a record of climate-related disasters over the years. The other is indoor office temperatures from a building on campus — a control dataset that *should not* show a global-warming trend, unless the thermostat is haunted.

“Fit a line,” they say. “Then a polynomial. Then convince me the slope isn’t just noise.”

This problem set is about that conversation. You will fit `y = ax + b` three different ways (brute force, a bisection-style search, and `numpy`), choose a polynomial degree with validation, and finish with a **permutation test**: shuffle the data until the universe is meaningless, and ask how often a slope as large as yours still appears.

Data files live in `data/`.

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Fit models by searching a parameter space and by using a library
- Separate training data from validation data
- Compare polynomial degrees with R² on held-out folds
- Use a permutation test to ask whether a fitted slope is surprising

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Do **not** modify `sse`, `best_b_for_slope`, `r2_score`, `k_fold_cv`, `temp_trend_analysis`, or `scatter_plot`. Line-fitting functions should return `[a, b, y_pred]`.

Run the staff tests from this folder:

```bash
python3 test.py
```

---

## Problem 1: Fitting `y = ax + b`

Years like `1999, 2000, 2005` make terrible polynomial inputs: `x^n` explodes. You will sometimes center the years first.

### 1.1) `center(x_vals)`

Subtract `x_vals[0]` from every x.

**Example:** `[1999, 2000, 2005]` → `[0, 1, 6]`.

### 1.2) `fit_line_exhaustive(x_vals, y_vals, a_values, b_values)`

You do not always get `numpy` in the field. Sometimes you just try a grid of guesses.

Try every pair `(a, b)` from the candidate lists. Keep the pair with smallest `sse`. Return that `a`, `b`, and the corresponding predictions.

### 1.3) `fit_line_bisection(x_vals, y_vals, a_lo, a_hi, epsilon)`

Now search over **slope** with a shrinking interval — the same idea as bisection, but you compare error instead of looking for a root:

- While `a_hi - a_lo > epsilon`, compute the best intercept for `a_lo` and for `a_hi` using `best_b_for_slope`.
- Compare SSE of the two candidate lines.
- Drop the half of the interval whose endpoint is worse (set the worse bound to the midpoint).
- When you stop, return the better endpoint’s `a`, `b`, and predictions.

This is approximate; tests only require you to get close.

**Hint:** `best_b_for_slope` is already written. Your job is the interval logic.

### 1.4) `fit_line_polyfit(x_vals, y_vals)`

Use `np.polyfit(..., 1)` on the **original** `x_vals` (centering is mainly for higher-degree polynomials later). Return `[a, b, y_pred]` so that predictions on the original x-values are `a * x + b`.

**Hint:** `np.polyfit` returns highest degree first, so the slope is `coeff[0]` and the intercept is `coeff[1]`.

---

## Problem 2: Validation — which curve should you trust?

A 20th-degree polynomial can thread every disaster count and still be useless next year. You need to hold data out.

### 2.1) `permute_xy` / `permute_y`

- `permute_xy`: shuffle **pairs** together (each x keeps its y).
- `permute_y`: shuffle only y (x stays put). This destroys any real relationship — you will need that for the permutation test.

Use `random.sample`.

### 2.2) `train_validate_split(..., val_frac=0.2)`

Shuffle pairs, then the first `int(n * val_frac)` points are validation, the rest train. Keep x and y aligned.

### 2.3) `evaluate_poly_degree(...)`

Split, `np.polyfit` on train with the given degree, predict on validation x, return `r2_score`. `np.polyval` is the easy way to evaluate a polynomial.

### 2.4) `make_folds(x_perm, y_perm, k=5)`

Split shuffled data into `k` folds as evenly as possible. The first `n % k` folds get one extra point.

### 2.5) `get_validation_scores(folds_x, folds_y, degree, k)`

For each fold `i`: train on all other folds, score R² on fold `i`.

`k_fold_cv` is already written; it calls your helpers. Note it calls `make_folds` **without** passing `k` (default 5). `get_validation_scores` still receives `k_or_val_frac`.

### 2.6) `compare_poly_degrees(...)`

This is the UROP plot: scatter the data, then for each degree:

1. Fit a polynomial on **centered** x (full dataset) for plotting.
2. Predict with `np.polyval` on centered x, but plot against original years.
3. Score with `val_method(x_vals, y_vals, degree, k_or_val_frac)` — this method uses original x.
4. Collect `[degree, [coeffs, y_pred, val_r2]]`, sort by degree.

A degree that fits the training wiggles but tanks on validation is a degree you should not publish.

---

## Problem 3: A permutation test for the slope

The disaster series *looks* like it goes up. Indoor temperatures look like a messy cloud. Looks are not a p-value.

### 3.1) `trend_permutation_test(...)`

1. Fit the observed slope `a_obs` with `method(x, y)`.
2. Repeat `n_permutations` times: shuffle y, refit, store the slope.
3. Two-sided p-value: fraction of |null slopes| ≥ |a_obs|.
4. Null interval: 2.5th and 97.5th percentiles (`np.percentile`).

Return `[a_obs, p_value, null_lo, null_hi]`.

A strong linear trend should give a small p-value. Indoor temperatures should look like noise (slope near 0, large p-value).

**Hint:** Use your `permute_y` so that each fake world has the same x-values and the same y-values, just re-paired.

Then run the temperature analysis helpers to see the story on real data.

---

## Suggested order

`center` → exhaustive fit → bisection → polyfit → shuffle/split → poly degree eval → folds / CV scores → `compare_poly_degrees` → permutation test. Then run the temperature analysis helpers.
