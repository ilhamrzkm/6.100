# Problem Set 7 — Disease Simulation

Build an agent-based epidemic model: people move, infect neighbors, recover or die. Then specialize movement and disease parameters.

```bash
python3 test.py
```

`DiseaseSimulation.__init__` and `run_simulation` are provided. Visualization lives in `visualization.py`.

## 1. `Person`

Store infected and alive flags (defaults `infected=False`, `alive=True`).

- `update_health(infected, alive)` sets both flags.
- `is_infected()` / `is_alive()` return those flags.
- `move(observation)`: if dead, return `(0, 0)`. If alive, pick a random angle with `random.uniform(0, 2*pi)` and return the unit vector `(cos θ, sin θ)`.

Tests patch `random.uniform` to `π/2`, which should give `(0, 1)`.

## 2. Geometry helpers

- `find_distance(loc1, loc2)`: Euclidean distance between `(x, y)` tuples.
- `find_nearest_neighbor(observation, neighbors)`: among `neighbors`, pick the one whose displacement in `observation` is shortest. Empty list → `None`. Distances are from the current person, so use `sqrt(dx² + dy²)` on the stored `(dx, dy)`.
- `move_towards_neighbor(observation, neighbor)`: unit vector in that displacement's direction. `(3, 4)` → `(0.6, 0.8)`. Zero length → `(0, 0)`.

## 3. `DiseaseSimulation`

People live in `self.people_locs`: `Person → (x, y)`.

### `reset`

Clear / rebuild `people_locs`. For each class `C` and count `n` in `people_counts`:

- Construct `C(infected=..., alive=True)` where infected is True with probability `starting_infection_prob` (`random.random() < p`).
- Place uniformly in `[0, width] × [0, height]`.

### `generate_observation(person)`

Map every **other** person within `infection_radius` to displacement `(other_x - person_x, other_y - person_y)`. Do not include self.

### `evolve_health(person, observation)` — do **not** mutate the person

Return `(infected, alive)` for the **next** state:

1. Already dead → `(False, False)`.
2. Currently infected:
   - Recover with probability `recovery_prob` → `(False, True)`.
   - Else die with probability `death_prob` → `(False, False)`.
   - Else stay infected → `(True, True)`.
3. Currently healthy: if **any** neighbor in the observation is infected, become infected with probability `infection_prob`. Otherwise stay healthy.

### `step`

Compute **all** new health and locations from the **current** state, then apply them. Do not update people mid-loop (otherwise later people see already-moved neighbors).

- Health: `evolve_health`.
- Motion: `dx, dy = person.move(observation)`, then clamp `x+dx` into `[0, width]` and `y+dy` into `[0, height]`.

### `get_stats`

Return `(state, num_infected, num_alive)` where `state[person] = {"location", "infected", "alive"}`.

## 4. Movement subclasses

Always fall back to `super().move(observation)` (random walk) if the special case does not apply.

### `MenacingPerson`

If infected, walk toward the nearest **healthy** neighbor. Otherwise random.

### `CarefulPerson`

- Healthy: walk **away** from nearest infected neighbor (negate the toward vector).
- Infected: walk away from nearest healthy neighbor.
- If no such neighbor, random.

### `MoreMenacingPerson` (`K = 5`)

If infected, take up to K nearest healthy neighbors, average their displacements, normalize to a unit vector. If none, random (or `MenacingPerson` behavior via `super()`).

## 5. Named diseases

`CovidSimulation` and `EbolaSimulation` should call `super().__init__(disease_params, people_counts, width, height)` with:

| | start infect | infect | recover | death | radius |
|---|---|---|---|---|---|
| COVID | 0.2 | 0.2 | 0.05 | 0.005 | 4 |
| Ebola | 0.2 | 0.9 | 0.05 | 0.5 | 2 |

## 6. Analysis (not autograded)

`analyze_disease_params` and `analyze_people_types` write SVG plots comparing diseases and agent types. Use after the simulation works.

## Suggested order

Person → distance helpers → `reset` / `get_stats` → observation → `evolve_health` → `step` → subclasses → COVID/Ebola → plots.
