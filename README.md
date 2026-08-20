# 6.100 Spring 2026 — Problem Set Collection (study companion)

Unofficial local copies of the seven **MIT 6.100 (Introduction to CS and Programming Using Python)** Spring 2026 problem sets, with solutions removed so you can implement them yourself.

Use this **together with** the official course site:

- Course: [https://introcomp.mit.edu/spring26](https://introcomp.mit.edu/spring26)
- Assignments: [https://introcomp.mit.edu/spring26/course-info/assignments](https://introcomp.mit.edu/spring26/course-info/assignments)

This repository is **not** MIT course staff material, is **not** affiliated with MIT, and is **not** a substitute for the official pset pages, checkoffs, or autograder. If you are enrolled, submit through the course site and follow the collaboration policy there.

---

## What this is for

Official psets on the Spring 2026 site are behind MIT login. This repo is a practice collection: the same function names, helpers, tests, and data files, plus a readable handout in each folder.

Typical workflow:

1. Read `homework.md` in a pset folder (and the official writeup if you have access).
2. Fill in the `NotImplementedError` stubs in `pset.py`. Do not change helpers marked do-not-modify.
3. Run the local tests from that folder:

```bash
python3 test.py
```

---

## What came from where

### From MIT 6.100 Spring 2026 (course staff)

The assignments themselves — topics, APIs, supplied helpers, autograder tests, and data — originate from **6.100 Spring 2026**. Files in this category include:

| Kind | Examples |
| --- | --- |
| Starter / student file | `pset.py` (headers, helpers, docstrings, intentional bugs to fix) |
| Local autograder | `test.py` |
| Staff utilities | `ps4/utils.py`, `ps5/utils.py`, `ps5/plot.py`, `ps7/visualization.py` |
| Data | `ps1/words.txt`, `ps1/contractions.txt`, `ps3/data/`, `ps4/data/`, `ps4/tests_data/`, `ps5/data/`, `ps5/graphs/`, `ps5/tester_data/` |
| Other course artifacts | `ps7/*.svg` plots |

Those files were first copied into this GitHub repo from a **completed** pset dump (implementations included). They are MIT / course-staff work. This repo does not claim ownership of them.

The official handouts and Catsoop pages remain the source of truth if anything here disagrees.

### Added in this repository (not official course text)

| What | Who / what it is |
| --- | --- |
| `ps1`–`ps7` **`homework.md`** | Companion writeups written for this repo. They restate the **same specifications** as the Spring 2026 `pset.py` / `test.py` files, in a narrative style similar to [MIT OCW 6.100L Fall 2022 problem sets](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/lists/problem-sets/). The stories and prose are original to this collection; they are **not** the official Spring 2026 PDFs. |
| Student function bodies in `pset.py` | Official solutions were stripped and replaced with `raise NotImplementedError` (or the staff-buggy code that you are meant to debug). Supplied helpers were left in place. |
| This `README.md` | Describes provenance and how to use the collection. |

**Style reference only:** [6.100L Fall 2022 on MIT OpenCourseWare](https://ocw.mit.edu/courses/6-100l-introduction-to-cs-and-programming-using-python-fall-2022/). Those OCW psets (Hangman, compound interest, and so on) are **different assignments**. Nothing from those PDFs was copied into the Spring 2026 code or tests.

---

## Problem sets

| Folder | Topic | Implement in |
| --- | --- | --- |
| [`ps1/`](ps1/) | Beaver cipher — encrypt, decrypt, break without the key | `ps1/pset.py` |
| [`ps2/`](ps2/) | MBTA-style circular-track simulation, wait times, Monte Carlo | `ps2/pset.py` |
| [`ps3/`](ps3/) | Line/polynomial fits, validation, permutation test on trend | `ps3/pset.py` |
| [`ps4/`](ps4/) | Graphs, BFS, weighted expansion, toll layering | `ps4/pset.py` |
| [`ps5/`](ps5/) | District enumeration, compactness, gerrymandering outcomes | `ps5/pset.py` |
| [`ps6/`](ps6/) | Two-bag knapsack (exhaustive + DP), paired items | `ps6/pset.py` |
| [`ps7/`](ps7/) | Agent-based epidemic model, movement subclasses, named diseases | `ps7/pset.py` |

Each folder has its own `homework.md`.

---

## Using this with official Spring 2026 materials

If you have access to [introcomp.mit.edu/spring26](https://introcomp.mit.edu/spring26):

- Keep lecture slides, recitation code, finger exercises, and exams on the course site (or your own download of **public** files). This repo is only the seven psets.
- Prefer the official pset page for due dates, submission, and checkoff rules.
- Use `homework.md` when you want a single-file spec plus story; use the official writeup when you need staff wording.

Python 3 is required. Some psets also need third-party packages already imported in the starter files (`matplotlib`, `numpy`, `pandas`, `networkx`).

---

## Academic integrity

If you are a current 6.100 student, do your own work. Do not copy another student’s `pset.py`. This collection is for studying the assignments, not for sharing solutions (there are none here).

---

## License / copyright

Course starter code, tests, and data remain **copyright MIT / 6.100 course staff**. Redistribute or reuse them only as those terms allow.

The `homework.md` companion writeups and this README were written for this study repo and are provided as-is, with no warranty.
