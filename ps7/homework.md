# Problem Set 7: Outbreak on Campus

## Introduction

A rumor moves through a dorm faster than the flu: someone on your floor is sick, someone else is “just tired,” and a third person is throwing a party anyway. Public health posters say “keep your distance.” Game theory says some people walk *toward* the healthy ones.

In this problem set you will build an **agent-based epidemic model**. People live in a rectangle (think: a quad, or a floorplan with the walls ignored). Each step they move, they look at neighbors inside an infection radius, and they recover — or they do not. Then you will specialize movement (careful vs. menacing) and disease parameters (a COVID-like illness vs. an Ebola-like one) and plot what the campus looks like afterward.

`DiseaseSimulation.__init__` and `run_simulation` are provided. Visualization lives in `visualization.py`.

Although this handout is long, the information is here to provide you with context, useful examples, and hints, so be sure to read carefully.

## Objectives

- Implement a small class and geometric helpers
- Update many agents from a snapshot of the previous state
- Use subclassing to change movement without rewriting the simulator
- Compare scenarios by changing parameters, not control flow

## Getting Started

Work in this folder. Fill in your name and kerberos at the top of `pset.py`.

Run the staff tests from this folder:

```bash
python3 test.py
```

---

## Problem 1: A person

Every agent is a `Person`: infected or not, alive or not, and (if alive) able to take a step.

### 1.1) `Person`

Store infected and alive flags (defaults `infected=False`, `alive=True`).

- `update_health(infected, alive)` sets both flags.
- `is_infected()` / `is_alive()` return those flags.
- `move(observation)`: if dead, return `(0, 0)`. If alive, pick a random angle with `random.uniform(0, 2*pi)` and return the unit vector `(cos θ, sin θ)`.

Tests patch `random.uniform` to `π/2`, which should give `(0, 1)`.

**Hint:** Dead people do not wander. Check `is_alive()` before sampling an angle.

---

## Problem 2: Geometry helpers

An “observation” is a map from nearby people to displacement `(dx, dy)` relative to you. Distances and chasing are just vector arithmetic.

- `find_distance(loc1, loc2)`: Euclidean distance between `(x, y)` tuples.
- `find_nearest_neighbor(observation, neighbors)`: among `neighbors`, pick the one whose displacement in `observation` is shortest. Empty list → `None`. Distances are from the current person, so use `sqrt(dx² + dy²)` on the stored `(dx, dy)`.
- `move_towards_neighbor(observation, neighbor)`: unit vector in that displacement’s direction. `(3, 4)` → `(0.6, 0.8)`. Zero length → `(0, 0)`.

---

## Problem 3: The simulation

People live in `self.people_locs`: `Person → (x, y)`.

### 3.1) `reset`

Clear / rebuild `people_locs`. For each class `C` and count `n` in `people_counts`:

- Construct `C(infected=..., alive=True)` where infected is True with probability `starting_infection_prob` (`random.random() < p`).
- Place uniformly in `[0, width] × [0, height]`.

### 3.2) `generate_observation(person)`

Map every **other** person within `infection_radius` to displacement `(other_x - person_x, other_y - person_y)`. Do not include self.

This is what a person “sees”: not the whole campus, only the neighborhood that can infect them (or that they can chase).

### 3.3) `evolve_health(person, observation)` — do **not** mutate the person

Return `(infected, alive)` for the **next** state:

1. Already dead → `(False, False)`.
2. Currently infected:
   - Recover with probability `recovery_prob` → `(False, True)`.
   - Else die with probability `death_prob` → `(False, False)`.
   - Else stay infected → `(True, True)`.
3. Currently healthy: if **any** neighbor in the observation is infected, become infected with probability `infection_prob`. Otherwise stay healthy.

### 3.4) `step`

Compute **all** new health and locations from the **current** state, then apply them. Do not update people mid-loop (otherwise later people see already-moved neighbors).

- Health: `evolve_health`.
- Motion: `dx, dy = person.move(observation)`, then clamp `x+dx` into `[0, width]` and `y+dy` into `[0, height]`.

Think of it as a simultaneous round in a board game, not a queue at the dining hall.

### 3.5) `get_stats`

Return `(state, num_infected, num_alive)` where `state[person] = {"location", "infected", "alive"}`.

---

## Problem 4: Not everyone walks the same way

Always fall back to `super().move(observation)` (random walk) if the special case does not apply.

### 4.1) `MenacingPerson`

If infected, walk toward the nearest **healthy** neighbor. Otherwise random.

(This is the person who should stay in. They do not.)

### 4.2) `CarefulPerson`

- Healthy: walk **away** from nearest infected neighbor (negate the toward vector).
- Infected: walk away from nearest healthy neighbor.
- If no such neighbor, random.

### 4.3) `MoreMenacingPerson` (`K = 5`)

If infected, take up to K nearest healthy neighbors, average their displacements, normalize to a unit vector. If none, random (or `MenacingPerson` behavior via `super()`).

**Hint:** Averaging displacements, then normalizing, is “walk toward the cluster,” not “walk toward whoever is closest.”

---

## Problem 5: Named diseases

Same simulator, different posters on the wall. `CovidSimulation` and `EbolaSimulation` should call `super().__init__(disease_params, people_counts, width, height)` with:

| | start infect | infect | recover | death | radius |
|---|---|---|---|---|---|
| COVID | 0.2 | 0.2 | 0.05 | 0.005 | 4 |
| Ebola | 0.2 | 0.9 | 0.05 | 0.5 | 2 |

Notice the tradeoff you are encoding: one disease reaches farther but infects less often; the other is deadly and sticky at short range.

---

## Problem 6: Analysis (not autograded)

`analyze_disease_params` and `analyze_people_types` write SVG plots comparing diseases and agent types. Use after the simulation works.

Ask yourself: does adding careful people actually slow the outbreak, or do menacing agents dominate the curve? The plots are the experiment; the code you wrote is the lab.

---

## Suggested order

Person → distance helpers → `reset` / `get_stats` → observation → `evolve_health` → `step` → subclasses → COVID/Ebola → plots.
