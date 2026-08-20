# Problem Set 2: Waiting for the T

## Introduction

You live near Kendall/MIT and you have a 10 a.m. lecture. In theory the Red Line is a clockwork loop: trains leave stations, glide along the track, and arrive just as you reach the platform. In practice you have watched three trains bunch together and then vanish for ten minutes.

The MBTA (in this problem set, a highly simplified MBTA) has asked 6.100 students for a model. You will simulate trains on a **circular track**, measure how long riders wait between trains, then add randomness — stalls, slowdowns, noisy speeds — and plot what happens to wait times.

The track is small enough to reason about by hand, but the same rules scale to a Monte Carlo study of “what if every train is a little late?”

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Debug someone else’s code with tests you write first
- Simulate state that updates over discrete time steps
- Measure a derived quantity (wait time) from a history of positions
- Run randomized trials and summarize them with mean and standard deviation

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Track length is `TRACK_LENGTH = 16`. Default speed is `DEFAULT_SPEED = 2` (distance per timestep). Trains move **counter-clockwise**. Positions wrap with `% TRACK_LENGTH`.

Do **not** modify `compute_mean`, `compute_standard_deviation`, `would_pass`, or `apply_none`.

Run the staff tests from this folder:

```bash
python3 test.py
```

---

## Problem 1: Geometry of a circular track

Before any trains move, you need to know how far it is from here to the next station, traveling the way the trains do.

### 1.1) `get_distance(loc1, loc2)`

Return the distance traveling **counter-clockwise** from `loc1` to `loc2`. If `loc2` is “behind” `loc1`, wrap around the circle.

**Hint:** On a circle of length `TRACK_LENGTH`, the counter-clockwise distance is `(loc2 - loc1)` wrapped into `[0, TRACK_LENGTH)`.

### 1.2) `get_next_station` (debug this)

Staff left a **buggy** implementation. Write your own tests first (see the two manual tests in `pset.py`), then change **two lines**.

You want the **smallest positive** counter-clockwise distance to a station that is **not** the current location. Think about:

- the initial `max_distance`, and
- the argument order of `get_distance`.

**Hint:** If you initialize the “best so far” distance to `0`, no positive distance will ever look better. And `get_distance(a, b)` is “from `a` to `b`,” not the other way around.

---

## Problem 2: An ideal day on the line

On a perfect day, every train has the same speed, stops at every station, and never overlaps another train. You will implement one train’s update, then the whole line, then a multi-step history.

### 2.1) `step_train(...)`

Update **one** train. Mutate `idle_time[idx]`. Apply the rules **in this order**:

1. If `idle_time[idx] > 0`, decrement it and stay put.
2. Project `next_loc = (current + speed) % TRACK_LENGTH`.
3. If that move would pass **another train**, stay put (do not idle).
4. If that move would pass a **station** (and you are not already sitting on it), snap to that station and set `idle_time[idx] = 2`.
5. Otherwise move to `next_loc`.

`would_pass` is provided — use it.

### 2.2) `step_simulation(...)`

Call `step_train` for every train. Return the new location list. Later (Problem 4), if `slowdown_func` is set, compute speed from it instead of `DEFAULT_SPEED`.

Early tests call `step_simulation(locs, stations, idle)` with no slowdown.

### 2.3) `simulate_trains(station_locations, num_steps, ...)`

Now run the line for many timesteps:

- Start with one train **at each station**.
- Initial idle time for every train is `2` (they leave after sitting).
- History length is `num_steps + 1` (include the starting positions).
- Each step: `step_simulation` on the latest locations.

Match the sample history in `get_sample_scenario()` for stations `[5, 6, 8]`.

**Hint:** Build the history as a list of location lists. Append the initial positions first, then loop `num_steps` times.

---

## Problem 3: How long do riders wait?

A student on the platform does not care about train indices. They care about the gap after a train leaves until the next one shows up.

**Intertrain wait time** at a station: time from a train **departing** until the next train **arrives**.

- **Arrival** at timestep `t`: a train is at the station at `t` but was not at `t-1`.
- **Departure** at timestep `t`: a train is at the station at `t` but not at `t+1`.

Pair departures with later arrivals.

### 3.1) `station_wait_times(location_history, station)`

For station `8` in the sample history, wait times sort to `[2, 2, 5]`.

### 3.2) `collect_all_wait_times(location_history, station_locations)`

Concatenate every station’s waits. Order does not matter; tests sort.

**Hint:** Walk the history once to collect arrival and departure times, then pair each departure with the next arrival after it.

---

## Problem 4: The T is never ideal

Real trains stall in the tunnel, crawl behind a disabled car, or just… have a weird day. Each timestep, **all trains share one sampled speed**.

Implement these slowdown functions:

| Function | Behavior |
|---|---|
| `apply_halt(p)` | Return `0` with probability `p`, else `DEFAULT_SPEED` |
| `apply_uniform_slow(_)` | Uniform random in `[0, DEFAULT_SPEED]` |
| `apply_gaussian_slow(sigma)` | `random.gauss(DEFAULT_SPEED/2, sigma)`, clipped to `[0, DEFAULT_SPEED]` |

Wire these into `step_simulation` / `simulate_trains` via `slowdown_func` and `slowdown_param`.

### 4.1) `run_monte_carlo(...)`

Run `num_trials` simulations. For each trial, take the **mean** wait time across all stations. Return:

`[mean of those trial-means, stdev of those trial-means, any one location_history]`

Use the provided `compute_mean` / `compute_standard_deviation`. Stochastic tests check that you are near the staff mean.

**Hint:** One location history is enough for plotting later; the statistics come from the list of per-trial mean waits.

---

## Problem 5: Plots

These are not unit-tested; use the manual plot helpers in `pset.py`.

- `plot_wait_time_distribution`: histogram of all wait times.
- `plot_monte_carlo_distributions`: for each parameter value, run Monte Carlo and plot average wait vs that parameter.

Look at the plots. Does a higher halt probability make waits worse, or does it also space trains out? That is the kind of question the model is for.

---

## Suggested order

`get_distance` → fix `get_next_station` → `step_train` → `step_simulation` → `simulate_trains` → wait times → slowdowns → Monte Carlo → plots.
