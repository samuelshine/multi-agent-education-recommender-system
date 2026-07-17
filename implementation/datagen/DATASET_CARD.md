# Dataset Card — Synthetic Constraint-Preference Dataset (v1)

Generated 2026-07-16 by `generate.py` (seed 42). This card is the authoritative
description for the paper's Data Availability Statement and for reviewers auditing the
evaluation. Update it whenever the generator changes.

## Purpose

Evaluation testbed for a pre-admission, cross-institution recommender:

- **H2** (multi-objective conflict): 162/300 students whose academically best-fitting
  program is financially infeasible (`h2_conflict: true`).
- **H3** (cold start / memory): 3-session progressive-disclosure structure per student;
  61 students with deliberately vague session-1 career goals; 67 with a session-3
  budget-revision event.
- **H1 fallback**: graded relevance enables NDCG@k / precision@k / recall@k if the
  requested real dataset (Elahi et al. 2022) does not arrive in time.

## Provenance

- **Student features** are sampled rows (not aggregates) from the public 20,000-record
  IT-student corpus of El-Keiey, ElMenshawy & Hassanein (IJACSA 16(3), 2025;
  `github.com/KLGLUG/student-career-area-prediction-using-machine-learning`, GPL-3.0).
  Sampling preserves realistic co-occurrence of grades × skills × career labels. Each
  student records its `seed_row` index. The seed file is **not redistributed**; the
  download command is in `README.md`.
- **Constraints** (budget, home city, mobility, employability priority) are NOT in the
  seed corpus — they are attached by documented sampling rules in `generate.py`
  (`derive_student`), with budget correlated to mobility ambition.
- **Programs and institutions are fictional.** Names are invented; cities are real;
  tuition/placement/salary/visa values are drawn from realistic country × tier ranges
  calibrated against public figures (spot-checked 2026-07-16). No value describes any
  real institution.

## Ground-truth oracle (published, system-independent)

Relevance is defined by a utility function fixed *before* any system is evaluated
(`oracle()` in `generate.py`):

```
utility = w_a·academic + w_f·financial + w_l·location + w_e·employability
```

- **academic** = field match (goal field ∈ program fields: 1.0; adjacent field: 0.5;
  else 0.1) × admission feasibility (grade ≥ bar: 1.0; within 5 pts: 0.5; else 0;
  CS-required × non-CS student: 0)
- **financial** = tuition ≤ budget: 1.0; ≤ 1.25×budget: 0.4; else 0
- **location** = mobility model (fixed_city / prefers_region / open_domestic /
  open_international — see code)
- **employability** = 0.6·placement% + 0.4·min(salary/50k, 1)
- **weights** by employability priority: high (.30/.20/.15/.35),
  medium (.35/.25/.20/.20), low (.40/.30/.20/.10)
- **grades**: any fully-violated hard constraint → 0; else utility ≥ .75 → 3,
  ≥ .55 → 2, ≥ .35 → 1, else 0.

## Known limitations (state these in the paper)

1. **Oracle circularity.** Ground truth is a formula, not human judgment. Any system
   that reverse-engineers the formula scores perfectly. Mitigations: the oracle is
   published and fixed pre-evaluation; all compared systems (proposed + baselines) face
   the same oracle; H1's primary benchmark remains the real Elahi et al. data when
   available; explanation quality is judged independently (LLM-as-judge).
2. **IT-only career coverage** — the seed corpus is IT students; career goals span 34
   IT roles only. Generalization beyond IT-bound students is untested.
3. **Synthetic economics** — tuition/salary ranges are calibrated but invented;
   absolute values must not be quoted as facts about real markets.
4. **Simplified mobility/location model** — four mobility classes, region-level
   geography.
5. **Session structure is scripted**, not observed user behavior.

## License / availability

Generated files: release with the paper's artifact (CC BY 4.0 recommended for data;
decide at artifact-release time). Seed corpus: remains under its GPL-3.0 repo; fetched
at generation time, never redistributed. Generator: part of the paper's open-source
artifact.
