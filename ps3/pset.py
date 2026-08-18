"""
6.100 Spring 2026
Problem Set 3

Fill out the following info:
Name:
Kerberos:
Approximate time spent (HH:MM):
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
# NO OTHER IMPORTS ALLOWED


############################################################
# supplied helper function -- DO NOT MODIFY
############################################################


def scatter_plot(
    x_vals, y_vals, title="", xlabel="", ylabel="", ax=None, show_plot=False
):
    """
    Make a scatter plot of x vs y.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        title (str): Plot title.
        xlabel (str): x-axis label.
        ylabel (str): y-axis label.
        ax (matplotlib.axes.Axes or None): Axes to plot on (creates new if None).
        show_plot (bool): If True, display the plot.

    Return a [fig, ax].
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=[8, 6])
    else:
        fig = ax.figure

    ax.scatter(x_vals, y_vals, label="Observed total disasters")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    if show_plot:
        plt.show()

    return [fig, ax]


############################################################
# regression (multiple ways)
############################################################


def center(x_vals):
    """
    Center the data to prevent warnings and improve the interpretability
    of our results.

    Parameters:
        x_vals (list): x-values.
    Return a list of the centered x values.
    """
    raise NotImplementedError


def sse(y_true, y_pred):
    """
    Compute the sum of squared errors.

    Parameters:
        y_true (list): True y-values.
        y_pred (list): Predicted y-values.

    Return the SSE.
    """
    # NOTE: DO NOT MODIFY
    total = 0.0
    for i in range(len(y_true)):
        diff = y_true[i] - y_pred[i]
        total += diff * diff
    return total


def fit_line_exhaustive(x_vals, y_vals, a_values, b_values):
    """
    Fit y = m*x + b using exhaustive search.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        a_values (list or None): Candidate slopes.
        b_values (list or None): Candidate intercepts.

    Return a list [a, b, y_pred] representing the model y = ax + b and the
    predicted y-values associated with those coefficients.
    """
    raise NotImplementedError


def best_b_for_slope(x_vals, y_vals, a):
    """
    Compute the intercept b that minimizes SSE for a fixed slope a.

    For a fixed slope `a`, the sum of squared errors as a function of `b` is
    SSE(b) = sum_i (y_i - (a*x_i + b))^2, which is a quadratic in `b` of the
    form alpha*b^2 + beta*b + gamma. The minimum occurs at the vertex, where
    b* = -beta / (2*alpha).

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        a (float): Fixed slope value.

    Return a float, b, that minimizes SSE for this fixed slope a.
    """
    # NOTE: DO NOT MODIFY
    n = len(x_vals)
    residual_sum = 0.0
    for i in range(n):
        residual_sum += y_vals[i] - a * x_vals[i]
    alpha = n
    beta = -2 * residual_sum
    b_star = -beta / (2 * alpha)
    return b_star


def fit_line_bisection(x_vals, y_vals, a_lo=-5.0, a_hi=5.0, epsilon=0.05):
    """
    Fit y = m*x + b using a bisection-style search strategy.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        a_lo (float): Lower slope bound.
        a_hi (float): Upper slope bound.
        epsilon (float): Stop when a_hi - a_lo <= epsilon.

    Return a list [a, b, y_pred] representing the model y = ax + b and the
    predicted y-values associated with those coefficients.
    """
    raise NotImplementedError


def fit_line_polyfit(x_vals, y_vals):
    """
    Fit y = m*x + b using np.polyfit.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.

    Return a list [a, b, y_pred] representing the model y = ax + b and the
    predicted y-values associated with those coefficients.
    """
    raise NotImplementedError


############################################################
# train/validation + k-fold cross-validation
############################################################


def permute_xy(x_vals, y_vals):
    """
    Return randomly permuted copies of paired (x_vals, y_vals).

    This helper is used for train/validate split: we shuffle paired observations
    so x and y stay aligned.

    Parameters:
        x_vals (list): 1D sequence of x-values.
        y_vals (list): 1D sequence of y-values.

    Return a list [x_perm, y_perm] of the permuted x-values and y-values.
    """
    raise NotImplementedError


def train_validate_split(x_vals, y_vals, val_frac=0.2):
    """
    Shuffle and split x/y into train and validation sets.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        val_frac (float): Fraction held out for validation.

    Return a list [x_train, y_train, x_val, y_val] of the x-values in the
    training set, y-values in the training set, x-values in the validation
    set and y-values in the validation set.
    """
    raise NotImplementedError


def r2_score(y_true, y_pred):
    """
    Compute the R^2 score.

    Parameters:
        y_true (list): True y-values.
        y_pred (list): Predicted y-values.

    Return the R^2 score.
    """
    # NOTE: DO NOT MODIFY
    sse_val = sse(y_true, y_pred)
    mean_y = sum(y_true) / len(y_true)
    sst = 0.0
    for yt in y_true:
        diff = yt - mean_y
        sst += diff * diff

    if sst == 0.0:
        if sse_val == 0.0:
            return 1.0
        return 0.0
    return 1.0 - (sse_val / sst)


def evaluate_poly_degree(x_vals, y_vals, degree, k_or_val_frac=0.2):
    """
    Evaluate a polynomial model by degree using a train/validation split.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        degree (int): Polynomial degree.
        k_or_val_frac (float): Fraction held out for validation.

    Return a float val_r2 representing the R^2 value on the validation set.
    """
    raise NotImplementedError


def make_folds(x_perm, y_perm, k=5):
    """
    Split paired (x, y) data into k folds as evenly as possible.

    Parameters:
        x_perm (list): Shuffled x-values.
        y_perm (list): Shuffled y-values aligned with `x_perm`.
        k (int): Number of folds.

    Return a list [folds_x, folds_y], where folds_x is a list of k lists
    of x-values and folds_y is a list of k lists of y-values.
    """
    raise NotImplementedError


def get_validation_scores(folds_x, folds_y, degree, k):
    """
    Compute the validation R^2 for each fold in k-fold cross validation.

    Parameters:
        folds_x (list): List of k folds of x-values, as return from `make_folds`.
        folds_y (list): List of k folds of y-values
            (aligned with folds_x).
        degree (int): Polynomial degree to fit.
        k (int): Number of folds. Should match len(folds_x)
            and len(folds_y).

    Return a list of floats `fold_r2s` of length k, where fold_r2s[i] is
    the R^2 score on validation fold i.
    """
    raise NotImplementedError


def k_fold_cv(x_vals, y_vals, degree, k_or_val_frac=5):
    """
    Evaluate a polynomial model using k-fold cross validation.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        degree (int): polynomial degree to fit.
        k (int): number of folds.

    Return the mean validation R^2 (float) across k folds.
    """
    # NOTE: DO NOT MODIFY
    x_perm, y_perm = permute_xy(x_vals, y_vals)
    folds_x, folds_y = make_folds(x_perm, y_perm)
    fold_r2s = get_validation_scores(folds_x, folds_y, degree, k_or_val_frac)

    return sum(fold_r2s) / len(fold_r2s)


def compare_poly_degrees(
    x_vals, y_vals,
    degrees,
    k_or_val_frac=0.2,
    val_method=evaluate_poly_degree,
    show_plot=True
):
    """
    Compare polynomial degrees on the disaster time series.

    Parameters:
        x_vals (list): x-values corresponding to years.
        y_vals (list): y-values corresponding to total number of disaster
            for the year.
        degrees (list): List of polynomial degrees to evaluate
            (each element should be an int).
        k_or_val_frac (float or int): Fraction held out for validation (used by
            `evaluate_poly_degree()`) or int for k number of folds.
        val_method (function): A validation function that returns a validation
            R^2 score for a given degree (e.g., `evaluate_poly_degree` or
            `k_fold_cv`).
        show_plot (bool): If True, display the plot.

    Note: This function uses `val_method` only to *score* each polynomial
    degree. It uses `np.polyfit` / `np.polyval` internally to fit and plot the
    polynomial curves for each degree.

    Return a list [degree, vals] pairs sorted by degree, where
    vals = [coeffs, y_pred, val_r2].
    """
    raise NotImplementedError


############################################################
# hypothesis testing (permutation test for trend)
############################################################


def permute_y(y_vals):
    """
    Return a randomly permuted copy of y.

    This helper is used for permutation tests: we keep x fixed and randomly
    shuffle the association between x and y under the null hypothesis.

    Parameters:
        y_vals (list): 1D sequence of values.

    Return a list of a permuted copy of y with the same shape.
    """
    raise NotImplementedError


def trend_permutation_test(
    x_vals, y_vals, n_permutations=2000, method=fit_line_polyfit
):
    """
    Run a permutation test for a trend between x and y.

    Parameters:
        x_vals (list): x-values.
        y_vals (list): y-values.
        n_permutations (int): Number of permutations.
        method (function): `fit_line_polyfit`, `fit_line_bisection`,
            or `fit_line_exhaustive`.

    Return a list [a_obs, p_value, null_lo, null_hi] containing the observed
    slope, p-value after running the test, lower bound of the null interval,
    and upper bound of the null interval.
    """
    raise NotImplementedError


def temp_trend_analysis(x_vals, y_vals, show_plot=True, n_permutations=2000):
    """
    Run a full trend analysis on temperature vs year.

    Parameters:
        x_vals (list): x-values corresponding to years.
        y_vals (list): y-values corresponding to mean temperature change
            for the year.
        show_plot (bool): If True, display plots.
        n_permutations (int): Number of permutations.

    Return a list [a, b, r^2, p_value] of the slope, intercept, r^2, and
    the p-value after running the permutation test.
    """
    # NOTE: DO NOT MODIFY
    x_vals_c = center(x_vals)

    a, b, y_pred = fit_line_polyfit(x_vals_c, y_vals)
    r2 = r2_score(y_vals, y_pred)
    result = trend_permutation_test(
        x_vals_c,
        y_vals,
        n_permutations=n_permutations,
        method=fit_line_polyfit,
    )
    p_value = result[1]

    if show_plot:
        _, ax1 = scatter_plot(
            x_vals,
            y_vals,
            title="Temperature Trend Over Time",
            xlabel="Year",
            ylabel="Temperature change",
            ax=None,
            show_plot=False,
        )
        ax1.plot(x_vals, y_pred, label=f"Fit: y = {a:.4f}x + {b:.2f}")
        ax1.legend()
        plt.show()

    return [a, b, r2, p_value]


############################################################
# manual testing code
############################################################


def get_tiny_line_data():
    """A tiny deterministic dataset that lies exactly on y = 2x + 1."""
    x = [0, 1, 2, 3]
    y = [1, 3, 5, 7]
    return [x, y]


def manual_test_center():
    print("Manual test center()...")
    years = [1999, 2000, 2005]
    centered = center(years)
    print(f"Expected centered: {[0, 1, 6]}, got {centered}")
    print()


def manual_test_fit_line_polyfit():
    print("Manual test fit_line_polyfit()...")
    x, y = get_tiny_line_data()

    a, b, y_pred = fit_line_polyfit(x, y)
    print(f"Expected slope ~2, got {a}")
    print(f"Expected intercept ~1, got {b}")
    print(f"Expected predictions {y}, got {list(y_pred)}")
    print(f"R^2 (should be 1): {r2_score(y, y_pred)}")
    print()


def manual_test_fit_line_exhaustive():
    print("Manual test fit_line_exhaustive()...")
    x, y = get_tiny_line_data()

    a_values = [0, 1, 2, 3]
    b_values = [0, 1, 2]
    a, b, y_pred = fit_line_exhaustive(x, y, a_values, b_values)

    print(f"Expected slope: {2}, got {a}")
    print(f"Expected intercept: {1}, got {b}")
    print(f"Expected predictions {y}, got {y_pred}")
    print()


def manual_test_fit_line_bisection():
    print("Manual test fit_line_bisection()...")
    x, y = get_tiny_line_data()

    a, b, y_pred = fit_line_bisection(x, y, a_lo=-5.0, a_hi=5.0, epsilon=1e-4)
    print(f"Expected slope close to 2, got {a}")
    print(f"Expected intercept close to 1, got {b}")
    print(f"R^2 (should be very close to 1): {r2_score(y, y_pred)}")
    print()


def manual_test_permute_helpers():
    print("Manual test permute_y() and permute_xy()...")
    x = [10, 20, 30, 40]
    y = [1, 2, 3, 4]

    y_perm = permute_y(y)
    print(f"Original y: {y}")
    print(f"Permuted y (same multiset): {list(y_perm)}")

    x_perm, y_perm2 = permute_xy(x, y)

    original_pairs = []
    for i in range(len(x)):
        original_pairs.append((x[i], y[i]))

    permuted_pairs = []
    for i in range(len(x_perm)):
        permuted_pairs.append((x_perm[i], y_perm2[i]))

    print(f"Original pairs: {original_pairs}")
    print(f"Permuted pairs (still aligned): {permuted_pairs}")
    print()


def manual_test_train_validate_split():
    print("Manual test train_validate_split()...")

    x = list(range(10))
    y = []
    for xi in x:
        y.append(2 * xi + 1)

    x_train, y_train, x_val, y_val = train_validate_split(x, y, val_frac=0.2)
    print(f"Expected val size 2 (20% of 10), got {len(x_val)}")
    print(f"Train size should be 8, got {len(x_train)}")

    ok_train = True
    for i in range(len(x_train)):
        if y_train[i] != 2 * x_train[i] + 1:
            ok_train = False
            break

    ok_val = True
    for i in range(len(x_val)):
        if y_val[i] != 2 * x_val[i] + 1:
            ok_val = False
            break
    print(f"Train pairs aligned: {ok_train}")
    print(f"Val pairs aligned: {ok_val}")
    print()


def manual_test_evaluate_poly_degree_on_perfect_line():
    print("Manual test evaluate_poly_degree() on perfect line...")

    x = list(range(30))
    y = []
    for xi in x:
        y.append(2 * xi + 1)

    val_r2 = evaluate_poly_degree(x, y, degree=1, k_or_val_frac=0.2)
    print(f"Degree 1")
    print(f"Val R^2 (should be 1): {val_r2}")
    print()


def manual_test_k_fold_cv_on_perfect_line():
    print("Manual test k_fold_cv() on perfect line...")

    x = list(range(10))
    y = []
    for xi in x:
        y.append(2 * xi + 1)

    mean_r2 = k_fold_cv(x, y, degree=1, k_or_val_frac=5)
    print("Degree 1, k=5")
    print(f"Mean CV R^2 (should be 1): {mean_r2}")
    print()


def manual_test_compare_poly_degrees():
    DIS_PATH = "data/disasters.csv"
    df_dis = pd.read_csv(DIS_PATH)

    print("Manual test compare_poly_degrees()...")
    x = list(df_dis["year"])
    y = list(df_dis["num_disasters"])
    out = compare_poly_degrees(x, y, [1, 2, 5], k_or_val_frac=5, show_plot=True, val_method=k_fold_cv)
    degree_to_vals = out
    print(f"Returned {len(degree_to_vals)} degree entries (expected 3)")
    print(
        f"First entry looks like: {degree_to_vals[0][0]} -> val_r2={degree_to_vals[0][1][2]:.3f}"
    )
    print()


def manual_test_trend_permutation_test():
    print("Manual test trend_permutation_test()...")

    x = list(range(50))
    y = []
    for xi in x:
        y.append(3 * xi + 5)

    a_obs, p_value, null_lo, null_hi = trend_permutation_test(
        x, y, n_permutations=300, method=fit_line_polyfit
    )

    print(f"Observed slope (should be ~3): {a_obs}")
    print(f"p-value (often near 0 for strong trend): {p_value}")
    print(f"Null interval (central 95%): [{null_lo}, {null_hi}]")
    print("If p-value seems large, increase n_permutations to reduce randomness.")
    print()


def manual_test_temp_trend_analysis():
    TEMP_PATH = "data/temp_change.csv"
    df_temp = pd.read_csv(TEMP_PATH)

    print("Manual test temp_trend_analysis()...")
    x = list(df_temp["year"])
    y = list(df_temp["temperature_change"])

    a, _, r2, p_value = temp_trend_analysis(
        x,
        y,
        show_plot=True,
        n_permutations=300,
    )

    print(f"Expected slope close to 2, got {a}")
    print(f"Expected R^2 close to 1, got {r2}")
    print(f"p-value (should usually be small for a strong trend): {p_value}")
    print("If p-value seems large, increase n_permutations to reduce randomness.")
    print()


def manual_test_temp_trend_analysis_indoor():
    INDOOR_PATH = "data/indoor_temps.csv"
    df_indoor = pd.read_csv(INDOOR_PATH)

    print("Manual test temp_trend_analysis()...")
    x = list(df_indoor["year"])
    y = list(df_indoor["temperature_change"])

    a, _, r2, p_value = temp_trend_analysis(
        x,
        y,
        show_plot=True,
        n_permutations=300,
    )

    print(f"Expected slope close to 0, got {a}")
    print(f"Expected R^2 close to 0, got {r2}")
    print(f"p-value (should usually be large for a small trend): {p_value}")
    print()


if __name__ == "__main__":
    pass
    # Uncomment the function calls below to test manually.
    # Note these are not comprehensive tests.
    # Feel free to modify or extend them when debugging your code.
    # Run test.py to make sure your code passes all our test cases.
    # manual_test_center()
    # manual_test_fit_line_polyfit()
    # manual_test_fit_line_exhaustive()
    # manual_test_fit_line_bisection()
    # manual_test_permute_helpers()
    # manual_test_train_validate_split()
    # manual_test_evaluate_poly_degree_on_perfect_line()
    # manual_test_k_fold_cv_on_perfect_line()
    # manual_test_trend_permutation_test()
    # manual_test_compare_poly_degrees()
    # manual_test_temp_trend_analysis()
    # manual_test_temp_trend_analysis_indoor()
