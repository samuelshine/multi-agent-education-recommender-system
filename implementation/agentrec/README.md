# agentrec — five-agent LLM recommender for pre-admission decision support

The prototype for the paper in `../../paper/`. Five agents (Profiling & Constraint,
Retrieval, Recommendation & Planning, Memory & Reflection, Explanation) over a
program catalog, with cross-session memory and deterministic safety guards.

## Requirements

- Python 3.10+ (stdlib only — no pip installs)
- An LLM backend, either:
  - **Ollama** (default): `ollama pull gemma4:e4b` and have the server running; or
  - **Any OpenAI-compatible API**: set `AGENTREC_BASE_URL`, `AGENTREC_API_KEY`,
    `AGENTREC_MODEL`, and pass `--backend openai`.

Paper experiments run on `gemma4:e4b` (Ollama). The code is model-agnostic.

## Quick start

```bash
cd implementation
# generate the dataset first (see datagen/README.md), then:
python3 run_pipeline.py --n 2 --sessions 1 --mode full --metrics
```

## Modes (= the paper's ablations)

| Mode | What changes | Tests |
|---|---|---|
| `full` | all five agents + memory | the proposed system |
| `no_memory` | MEMORY block never injected | H3 (cold-start/memory) |
| `single_objective` | Recommendation ranks by academic fit only | H2 (multi-objective) |
| `single_prompt` | one LLM call after the prefilter | architecture ablation |

## Module map

| File | Responsibility |
|---|---|
| `llm.py` | Backend-agnostic client + disk cache (ablations share upstream calls) |
| `prompts.py` | All agent prompts, single source |
| `schemas.py` | Structural validation + deterministic revision-action semantics |
| `simulate.py` | datagen student/session → simulated student message (evaluation drives the same code path as live use) |
| `memory.py` | Per-student cross-session memory store |
| `pipeline.py` | Orchestrator, deterministic prefilter, post-reflection guard |
| `eval/metrics.py` | NDCG@k (headline), precision@k, recall@k vs. datagen qrels |

## Safety guards (from the week-1 spike, `../spike/SPIKE_REPORT.md`)

1. **Hard admission/budget/location filter** — deterministic, in the prefilter and
   again as a post-reflection guard. Unknown student values never count as violations
   (cold-start sessions must not be starved of candidates).
2. **Reflection revision validation** — `swap_in` only for non-shortlisted candidates,
   `keep`/`drop` only for shortlisted ones, no duplicates, ids must exist. One
   re-prompt naming the violation, then fail-closed to the pre-reflection shortlist.
3. **Every agent step fails closed** — a twice-invalid output degrades to a
   deterministic fallback and is flagged in the run record (`fallbacks`), never
   crashes a batch.

## Run records

`run_pipeline.py` writes one JSON per (student, session) under `../runs/<mode>/` —
constraint object, prefilter/retrieved/proposed/final id lists, guard drops,
reflection note, explanation, latency, fallbacks. Batches are resumable (existing
records skipped without `--force`).
