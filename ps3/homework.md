# Problem Set 3 — Regression, Validation, and Trend Tests

Fit lines and polynomials to climate/disaster data, choose model degree with validation, then test whether a trend is statistically meaningful.

```bash
python3 test.py
```

Data files live in `data/`. Do not modify `sse`, `best_b_for_slope`, `r2_score`, `k_fold_cv`, `temp_trend_analysis`, or `scatter_plot`. Line-fitting functions should return `[a, b, y_pred]`.

## 1. Fitting `y = ax + b`

### `center(x_vals)`

Subtract `x_vals[0]` from every x. `[1999, 2000, 2005]` → `[0, 1, 6]`.

Centering years avoids huge `x^n` values in polynomial fits.

### `fit_line_exhaustive(x_vals, y_vals, a_values, b_values)`

Try every pair `(a, b)` from the candidate lists. Keep the pair with smallest `sse`. Return that `a`, `b`, and the corresponding predictions.

### `fit_line_bisection(x_vals, y_vals, a_lo, a_hi, epsilon)`

Search over **slope** with a shrinking interval:

- While `a_hi - a_lo > epsilon`, compute the best intercept for `a_lo` and for `a_hi` using `best_b_for_slope`.
- Compare SSE of the two candidate lines.
- Drop the half of the interval whose endpoint is worse (set the worse bound to the midpoint).
- When you stop, return the better endpoint's `a`, `b`, and predictions.

This is approximate; tests only require you to get close.

### `fit_line_polyfit(x_vals, y_vals)`

Use `np.polyfit(..., 1)`. If you center x first, convert the intercept back to the original x scale: `b_original = b_centered - a * x_vals[0]` if you centered by subtracting `x_vals[0]`... actually polyfit on centered x gives intercept at the centered origin, so `y = a * (x - x0) + b_c` which is `y = a*x + (b_c - a*x0)` wait: `y = a*(x - offset) + b_centered` ⇒ intercept on original scale is `b_centered - a * offset`. The previous solution used `b = coeff[1] + a*x_vals[0]` which matches centering with `x - x[0]` only if they fitted on centered and then... 

`y = a * (x - offset) + b_c` = `a*x + (b_c - a*offset)`.

So `b = b_c - a * offset`. The old code had `b = float(coeff[1]+ a*x_vals[0])` which is `b_c + a*offset`. That's the opposite!

Wait they did:
```
centered = center(x_vals)
coeff = np.polyfit(centered, y_vals, 1)
a = float(coeff[0])
b = float(coeff[1]+ a*x_vals[0])
y_pred = a*x + b  # using ORIGINAL x
```

If centered = x - x0, then true model is y = a*(x-x0) + b_c = a*x + (b_c - a*x0).

But they used b = b_c + a*x0 and y = a*x + b = a*x + b_c + a*x0 which is WRONG unless...

polyfit on centered: y ≈ a * x_c + b_c = a*(x-x0) + b_c.

If they then compute y_pred = a*x + (b_c + a*x0) that's a*x + b_c + a*x0 = a*(x+x0) + b_c which is wrong.

UNLESS they wanted y_pred = a * original_x + b with b adjusted differently...

Let me think again. If data is exactly y = 2x + 1 with x = [0,1,2,3], offset=0, centered=x, so b = b_c + 0 = 1. Works.

If x = [1999, 2000, ...] it might still pass tests if tests use small x starting at 0, or if they evaluate y_pred on original x and tests check y_pred not b...

manual_test uses get_tiny_line_data with x starting at 0.

I'll tell students: fit on **original** x, or if you center, convert intercept so predictions on original x are correct: `y = a * x_centered + b_c` then map back.

Simplest instruction: you may `np.polyfit` on the original x values. Centering is mainly for higher-degree polynomials in `compare_poly_degrees`. Tests for `fit_line_polyfit` should work with polyfit on original x.

I'll recommend fitting on original x for `fit_line_polyfit`.

## 2. Validation

### `permute_xy` / `permute_y`

Shuffle **pairs** together (`permute_xy`) vs shuffle only y (`permute_y`, x stays put). Use `random.sample`.

### `train_validate_split(..., val_frac=0.2)`

Shuffle pairs, then the first `int(n * val_frac)` points are validation, the rest train. Keep x/y aligned.

### `evaluate_poly_degree(...)`

Split, `np.polyfit` on train with the given degree, predict on validation x, return `r2_score`. `np.polyval` is the easy way to evaluate a polynomial.

### `make_folds(x_perm, y_perm, k=5)`

Split shuffled data into `k` folds as evenly as possible. The first `n % k` folds get one extra point.

### `get_validation_scores(folds_x, folds_y, degree, k)`

For each fold `i`: train on all other folds, score R² on fold `i`.

`k_fold_cv` is already written; it calls your helpers. Note it calls `make_folds` **without** passing `k` (default 5). `get_validation_scores` still receives `k_or_val_frac`.

### `compare_poly_degrees(...)`

Scatter the data, then for each degree:

1. Fit a polynomial on **centered** x (full dataset) for plotting.
2. Predict with `np.polyval` on centered x, but plot against original years.
3. Score with `val_method(x_vals, y_vals, degree, k_or_val_frac)` — this method uses original x.
4. Collect `[degree, [coeffs, y_pred, val_r2]]`, sort by degree.

## 3. Permutation test

### `trend_permutation_test(...)`

1. Fit the observed slope `a_obs` with `method(x, y)`.
2. Repeat `n_permutations` times: shuffle y, refit, store the slope.
3. Two-sided p-value: fraction of |null slopes| ≥ |a_obs|.
4. Null interval: 2.5th and 97.5th percentiles (`np.percentile`).

Return `[a_obs, p_value, null_lo, null_hi]`.

A strong linear trend should give a small p-value. Indoor temperatures should look like noise (slope near 0, large p-value).

## Suggested order

`center` → exhaustive fit → bisection → polyfit → shuffle/split → poly degree eval → folds / CV scores → `compare_poly_degrees` → permutation test. Then run the temperature analysis helpers.
