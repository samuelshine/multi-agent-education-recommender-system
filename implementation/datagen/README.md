# datagen — synthetic constraint-preference dataset generator

Generates the paper's H2/H3 testbed (and H1 fallback benchmark): synthetic prospective
students with multi-objective constraints, a fictional program catalog, graded
ground-truth relevance (for NDCG@k), and multi-session disclosure structure.
Design rationale: `../../paper/chapter_plan.md` (Methodology, decided 2026-07-16).
Full provenance, oracle definition, and limitations: `DATASET_CARD.md`.

## Setup (one-time): fetch the seed corpus

The generator samples feature rows from the public 20k-record student-features corpus
of El-Keiey et al. 2025 (GPL-3.0 licensed repo). We do **not** redistribute it — fetch
it yourself:

```bash
mkdir -p seed
curl -sL -o seed/roo_data.csv \
  "https://raw.githubusercontent.com/KLGLUG/student-career-area-prediction-using-machine-learning/master/Project%20Code/roo_data.csv"
```

(`seed/` is gitignored.)

## Generate

```bash
python3 generate.py                # defaults: --seed 42 --students 300 --programs 200
```

Stdlib only, deterministic given `--seed`. Writes to `out/`:

| File | Contents |
|---|---|
| `students.json` | 300 students: academic profile + career goal (from seed rows) + attached constraints (budget, home city, mobility, employability priority) + `h2_conflict` / `career_goal_vague` flags |
| `programs.json` | 200 **fictional** programs: field tags, city/country, tuition, admission bar, placement, salary, visa |
| `qrels.csv` | 60,000 (student, program) rows: oracle utility, per-objective parts, graded relevance 0–3 |
| `sessions.json` | 3 sessions per student: progressive field disclosure (cold start → full), feedback events, budget-drift events |
| `stats.json` | Generation summary (grade distribution, sub-population counts) |

## Validation status (seed 42, 2026-07-16)

- 0 students with all-zero relevance (NDCG@k defined for every student)
- 30 students with <10 relevant programs (deliberately hard cases, kept)
- 162 H2-conflict students (best academic fit financially infeasible)
- 61 cold-start-vague students, 67 budget-drift students (H3 material)
- Salary/tuition calibration spot-checked per country × tier
