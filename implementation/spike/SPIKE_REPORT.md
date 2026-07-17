# Spike Report — gemma4:e4b five-agent capability test

**Date:** 2026-07-16 · **Run:** `outputs/results_20260716_175556.json` /
`outputs/transcript_20260716_175556.md` · **Model:** `gemma4:e4b` (Ollama 0.31.1)

## Verdict: GO

`gemma4:e4b` can carry the five-agent pipeline. Build the prototype on it. The
standing risk #2 in `../../paper/chapter_plan.md` (small-model capability) is
**retired** for the architecture as a whole and **narrowed** to the three specific
weak spots below.

## Quantitative results (5 profiles × 5 agents = 25 calls)

| Metric | Result |
|---|---|
| Fatal errors | 0 |
| JSON parse failures | 0 / 20 structured calls |
| Hallucinated KB ids | 0 |
| Budget violations surviving into final shortlist | 0 |
| Mean call latency | 30.2 s (range 12–54 s) |
| Wall time, full pipeline per student | ~2.5 min |
| Total run | 754.6 s |

## Qualitative findings

**Explanations are grounded.** Spot-checks across P2/P3/P5: every tuition figure,
placement rate, salary, visa duration, and budget comparison in the Explanation agent's
output matches the KB exactly; no invented facts found. Budget arithmetic ("$2,200 falls
well within your maximum budget of $6,000") is correct throughout.

**Constraint honesty beats instruction compliance (good).** P2 (location-locked to
Kolkata) produced a 2-item shortlist despite the "exactly 3" instruction, because only
two KB entries satisfy the hard constraint — the pipeline refused to pad with
violations. Prototype spec should legitimize this: shortlist size ≤ k when hard
constraints bind.

**Cold-start signal captured.** P4's vague profile yielded an explicit
`uncertainty_notes` entry ("Unsure of specific career path") — the hook the Memory &
Reflection agent needs for H3's cold-start machinery.

**Trade-off surfacing works.** Recommendation agent's `tradeoff_note` fields name real
conflicts (BCom math-background risk for an MCA; program focus vs. cost), which is the
H2 multi-objective mechanism in miniature.

## Weak spots (carry into prototype design)

1. **Admission-plausibility checking is lenient.** P3 (BSc Zoology career-switcher):
   TUM MSc Informatics (requires strong CS bachelor's) was marked
   `admission_plausible: true`, survived reflection, and reached the final shortlist —
   the explanation honestly flagged the mismatch, but Reflection should have demoted or
   dropped it. Prototype: give the Reflection agent an explicit admission-check rubric
   and make `admission_plausible: false` a hard filter.
2. **Reflection `revisions` semantics are loose.** P2 emitted `action: swap_in` for an
   item already on the list, with rambling justification. Schema was followed; semantics
   were not. Prototype: validate revision actions deterministically (swap_in requires
   the item to be absent, etc.) and re-prompt on violation.
3. **Throughput will bind at evaluation scale, not prototype scale.** ~2.5 min/student
   × (e.g.) 200 simulated students × 5 conditions (full, 3 ablations, single-prompt)
   ≈ 42 hours of pure inference. Plan evaluation as overnight batches, cache agent
   outputs shared across conditions where valid, and consider `gemma4:12b` (not yet
   pulled) only if e4b quality proves insufficient — latency will be worse, not better.

## What the spike does NOT show

No memory persistence across sessions (H3's mechanism), no real RAG (KB fit in
context), no adversarial profiles, n=5. These are prototype-phase questions.
