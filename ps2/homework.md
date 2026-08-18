# Problem Set 2 — MBTA Train Simulation

Simulate trains on a circular track, measure passenger wait times, then add randomness and plot results.

```bash
python3 test.py
```

Track length is `TRACK_LENGTH = 16`. Default speed is `DEFAULT_SPEED = 2` (distance per timestep). Trains move **counter-clockwise**. Positions wrap with `% TRACK_LENGTH`.

Do not modify `compute_mean`, `compute_standard_deviation`, `would_pass`, or `apply_none`.

## 1. Geometry

### `get_distance(loc1, loc2)`

Distance traveling counter-clockwise from `loc1` to `loc2`. If `loc2` is "behind" `loc1`, wrap around the circle.

### `get_next_station` (debug this)

Staff left a **buggy** implementation. Write your own tests first (see the two manual tests), then change **two lines**.

Hints: you want the **smallest positive** counter-clockwise distance to a station that is not the current location. Think about the initial `max_distance` and the argument order of `get_distance`.

## 2. Ideal simulation

### `step_train(...)`

Update **one** train. Mutate `idle_time[idx]`. Rules, in order:

1. If `idle_time[idx] > 0`, decrement it and stay put.
2. Project `next_loc = (current + speed) % TRACK_LENGTH`.
3. If that move would pass **another train**, stay put (do not idle).
4. If that move would pass a **station** (and you are not already sitting on it), snap to that station and set `idle_time[idx] = 2`.
5. Otherwise move to `next_loc`.

`would_pass` is provided — use it.

### `step_simulation(...)`

Call `step_train` for every train. Return the new location list. Later (section 4), if `slowdown_func` is set, compute speed from it instead of `DEFAULT_SPEED`.

Early tests call `step_simulation(locs, stations, idle)` with no slowdown.

### `simulate_trains(station_locations, num_steps, ...)`

- Start with one train **at each station**.
- Initial idle time for every train is `2` (they leave after sitting).
- History length is `num_steps + 1` (include the starting positions).
- Each step: `step_simulation` on the latest locations.

Match the sample history in `get_sample_scenario()` for stations `[5, 6, 8]`.

## 3. Wait times

**Intertrain wait time** at a station: time from a train **departing** until the next train **arrives**.

- Arrival at timestep `t`: train is at the station at `t` but was not at `t-1`.
- Departure at timestep `t`: train is at the station at `t` but not at `t+1`.

Pair departures with later arrivals. For station `8` in the sample history, wait times sort to `[2, 2, 5]`.

`collect_all_wait_times` concatenates every station's waits (order does not matter; tests sort).

## 4. Realistic slowdowns

Each timestep, all trains share one sampled speed:

| Function | Behavior |
|---|---|
| `apply_halt(p)` | Return `0` with probability `p`, else `DEFAULT_SPEED` |
| `apply_uniform_slow(_)` | Uniform random in `[0, DEFAULT_SPEED]` |
| `apply_gaussian_slow(sigma)` | `random.gauss(DEFAULT_SPEED/2, sigma)`, clipped to `[0, DEFAULT_SPEED]` |

Wire these into `step_simulation` / `simulate_trains` via `slowdown_func` and `slowdown_param`.

### `run_monte_carlo(...)`

Run `num_trials` simulations. For each trial, take the **mean** wait time across all stations. Return:

`[mean of those trial-means, stdev of those trial-means, any one location_history]`

Use the provided `compute_mean` / `compute_standard_deviation`. Stochastic tests check you are near the staff mean.

## 5. Plots

- `plot_wait_time_distribution`: histogram of all wait times.
- `plot_monte_carlo_distributions`: for each parameter value, run Monte Carlo and plot average wait vs that parameter.

These are not unit-tested; use the manual plot helpers.

## Suggested order

`get_distance` → fix `get_next_station` → `step_train` → `step_simulation` → `simulate_trains` → wait times → slowdowns → Monte Carlo → plots.
