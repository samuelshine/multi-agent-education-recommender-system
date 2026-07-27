# Implementation

Prototype system for the paper in `../paper/`. Kept separate from the paper source so the
paper's LaTeX build and the system's codebase can evolve independently.

## Status

Phase 5 (prototype) **in progress** — scaffold built 2026-07-16; single-session smoke
test and 3-student × 3-session memory test both passed same day (0 fallbacks across 45
agent calls). Next: classical baselines (`baselines/`, pending source PDFs).
Architecture decisions are final (see `../paper/chapter_plan.md` — plan-mode dialogue
completed 2026-07-16). Week-1 model spike completed 2026-07-16 with verdict **GO** on
`gemma4:e4b` — see `spike/SPIKE_REPORT.md`.

## License

Code in this directory is MIT-licensed — see `LICENSE`. The generated synthetic
dataset (`datagen/out/`) is CC BY 4.0 — see `datagen/DATASET_CARD.md`. The public seed
corpus consumed at generation time is not redistributed and remains under its own
license — see `datagen/README.md`.

## Layout

| Dir | What |
|---|---|
| `agentrec/` | The prototype package: five agents, memory, validation, metrics — see `agentrec/README.md` (this is the open-source artifact core) |
| `run_pipeline.py` | CLI: single students or batches, all five modes (`full` / `no_memory` / `single_objective` / `single_prompt` / `single_prompt_grounded`) |
| `datagen/` | Synthetic dataset generator + dataset card |
| `baselines/` | Faithful HRSPCA + StudieMe re-implementations, reconstruction table (paper appendix source), `run_baselines.py` — deterministic, no LLM. Eval split ST0000–ST0099; HRSPCA NDCG@5 0.793, StudieMe 0.673 |
| `spike/` | Week-1 disposable model-capability spike (kept for provenance) |
| `runs_h1/`, `runs_h3/` | Run records + judge scores backing every number in the paper's Results section (H1/H2 in `runs_h1/`, H3 in `runs_h3/`) — included in the release, not regenerated-only, so claims are checkable without re-running the LLM. `runs_h1/single_prompt_grounded/` is the review-requested ablation isolating grounding-instruction wording from architecture (`chain_single_prompt_grounded.sh`) |
| `analyze_results.py`, `analyze_judge.py` | Recompute every accuracy and explanation-quality table in the paper directly from the committed run records (deterministic, no LLM) |
| `runs/`, `cache/` | Scratch run output and LLM response cache (gitignored — regenerate locally; not part of the release) |

## Reproducing the paper's results

```bash
python3 analyze_results.py   # H1/H2/H3 accuracy tables (NDCG@5, P@5, R@5)
python3 analyze_judge.py     # explanation-quality tables + inter-judge agreement
```

Both scripts read only the committed run records and dataset files — no LLM calls, no
network access, deterministic. To regenerate the run records themselves from scratch
(re-running the five-agent pipeline against Ollama), see `agentrec/README.md`.

## `spike/` — week-1 model-capability spike (2026-07-16)

Disposable de-risking script, **not** the prototype. Tests standing risk #2 from
`chapter_plan.md`: can `gemma4:e4b` (local, Ollama) carry five-agent constraint
reasoning and grounded explanation?

- `profiles.json` — 5 hand-written student profiles (budget-constrained achiever,
  location-locked, career-switcher, cold-start/vague, international aspirant), each
  designed to stress a different constraint conflict.
- `knowledge_base.json` — 12-entry toy institution/program KB (8 India, 4 abroad) with
  tuition, placement, salary, visa, admission fields. Small enough to fit in context —
  no RAG index in the spike; the real prototype will retrieve.
- `spike_pipeline.py` — one full pass of the paper's 5-agent pipeline per profile
  (Profiling → Retrieval → Recommendation → Reflection → Explanation) against the local
  Ollama server. Logs per-call latency, JSON-parse failures, hallucinated KB ids, and
  budget violations surviving into the final shortlist (the deterministic spike metrics).
- `outputs/` — timestamped machine-readable results + human-readable transcripts.
- `SPIKE_REPORT.md` — written after each run; go/no-go assessment for building the
  prototype on this model.

Run: `python3 spike_pipeline.py [--model gemma4:e4b]` (requires Ollama running with the
model pulled).

Session memory persistence (the Memory half of Memory & Reflection) is intentionally out
of spike scope — it needs multi-session structure that only the real prototype will have.

## `datagen/` — synthetic dataset generator (2026-07-16)

Generates the H2/H3 evaluation testbed (and H1 fallback benchmark): 300 synthetic
students seeded from the public 20k career corpus, 200 fictional programs, 60k
oracle-graded relevance pairs, 3-session disclosure structure. See `datagen/README.md`
(usage) and `datagen/DATASET_CARD.md` (provenance, oracle definition, limitations —
paper-facing). v1 generated and validated; regenerate deterministically with
`python3 datagen/generate.py --seed 42`.
