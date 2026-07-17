# Research Design

Working document. Not for submission — informs `main.tex` Introduction, Architecture, and
(later) Methodology sections. Supersedes the original 7-agent brainstorm per the
architecture critique below.

## Gap statement (from `literature_matrix.md`)

No existing work combines an agentic multi-agent LLM architecture with the **pre-admission,
cross-institution** higher-education decision (which university, which program) while
reasoning jointly over career goals, financial constraints, location, and employability
outcomes. Agentic education systems published in 2025-2026 (Cluster F) all target
**already-enrolled** students inside an **already-chosen** program. Systems that target the
pre-admission decision (Cluster A) all use pre-agentic methods (CF/CB/KB/ML classification).

## Research Questions

**RQ1 (primary).** Does an agentic multi-agent LLM architecture, applied to pre-admission
cross-institution university/program selection, improve explainability and adaptivity over
classical educational recommenders (CF/CB/KB/ML) while matching or exceeding their accuracy
on standard recommendation metrics (precision@k, recall@k, NDCG)?

**RQ2.** How should multi-objective constraints (academic fit, career goals, financial
constraints, location preference, employability outcomes) be represented and reasoned over
by specialized agents, compared to a single monolithic LLM prompt or a classical hybrid
scoring function?

**RQ3.** Do long-term memory and reflection mechanisms measurably reduce cold-start
degradation for prospective students with no prior interaction history, compared to a
stateless agent pipeline?

## Hypotheses

- **H1.** The multi-agent architecture produces higher user-perceived explanation quality
  than a faithfully re-implemented classical hybrid baseline (CF+KB, per
  `hrspca`/`studieme`) while remaining within a pre-registered **5% relative
  non-inferiority margin on NDCG@k** (headline metric; precision@k / recall@k
  secondary). Author decisions 2026-07-16, supersede "comparable-or-better" — see
  `chapter_plan.md` Methodology Rounds 1–2.
- **H2.** Explicit multi-objective agent reasoning improves recommendation relevance for
  students with conflicting constraints (e.g., financial limits vs. top academic fit)
  relative to a single-objective ranking baseline.
- **H3.** Memory + reflection agents mitigate cold-start degradation more effectively than
  a stateless agent pipeline, measured across simulated first-session vs. later-session
  interactions.

## Contribution claims

1. First agentic multi-agent LLM architecture (per the literature check above) targeting
   pre-admission, cross-institution higher-education decision support — a distinct decision
   scope from the in-program advising/pathway/course systems in Cluster F.
2. An explicit multi-objective reasoning mechanism (career, financial, location,
   employability) integrated into agent planning, evaluated against classical educational-RS
   baselines using both standard IR metrics and agentic-specific metrics (explanation
   quality, adaptivity, cold-start robustness) — directly answering the "lack of educational
   evaluation frameworks" gap named in `llmagentrecsyssurvey`.
3. A working prototype and evaluation protocol, released as an **open-source artifact
   anyone can run** (author decision, plan-mode Round 2, 2026-07-16 — see
   `chapter_plan.md`). Real-data pilots and field deployment are explicitly Future Work.

**Status:** Stress-tested in plan-mode Socratic dialogue 2026-07-16 (Step 1 complete —
see `chapter_plan.md` for the full log). Author decisions now locked in: (1) thesis is
**novelty-led** (first agentic system at this decision scope), with improvement framing
as explicit fallback if full-text reading of Cluster A/F kills the gap; (2) H1's
"comparable-or-better accuracy" is a hard commitment — the author's floor is **no loss
in accuracy** vs. classical baselines; (3) contribution 3 means a runnable open-source
release, not deployment claims. Consequence: the Cluster A/F full-text read is now
load-bearing for the thesis itself, not just Related Work hygiene.

## Architecture: 7 agents to 5 (merge, don't add)

Original brainstorm: Student Profiling, Goal Planning, Knowledge Retrieval, Recommendation,
Reflection, Explanation, Memory (7 agents). Two competitor systems bound the reasonable
range: `onlinecoursemaskg` ships 3 agents (profiling+intent, retrieval, recommendation) and
gets measurable accuracy/recall/F1 gains; `agenticedurec` ships 18+ agents in a 4-tier
hierarchy but only at production deployment scale (6,000+ users) — not reproducible by a
single-author dissertation prototype in a month. Target: closer to the 3-agent end, with an
explicit fourth/fifth agent only where the paper's headline claims (explainability, memory)
require a visibly separate component reviewers can point to.

**Recommended 5-agent design:**

| Agent | Merges | Responsibility |
|---|---|---|
| Profiling & Constraint Agent | Student Profiling + Goal Planning's constraint capture | Elicits academic background, career goals, financial/location/employability constraints; builds structured student-constraint object |
| Retrieval Agent | Knowledge Retrieval | RAG over institution/program data (admissions criteria, cost, location, outcomes) |
| Recommendation & Planning Agent | Recommendation + Goal Planning's ranking logic | Multi-objective ranking/matching over retrieved candidates against the constraint object |
| Explanation Agent | Explanation | Generates per-recommendation rationale grounded in retrieved evidence (addresses H1's explainability claim directly) |
| Memory & Reflection Agent | Memory + Reflection | Persists profile/preferences across sessions; self-critiques the shortlist before it reaches the student (addresses H3's cold-start claim) |

**Why merge rather than keep 7:** Reflection and Memory are both about persistence/
self-correction and are the two most implementation-heavy pieces to build separately in a
month; merging keeps scope buildable without weakening either headline claim (explanation
quality stays its own agent since it is a stated contribution, not folded into
Recommendation). This directly answers the "should some agents be merged" question you
raised in the original brief.

**Open for your pushback:** this merge is a judgment call, not a proof. If your dissertation
committee or the target IEEE venue expects a richer multi-agent story (more agents = more
"agentic"), 7 remains defensible — flag if you want to keep the original count instead.
