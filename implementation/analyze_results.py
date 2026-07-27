#!/usr/bin/env python3
"""Paper-facing analysis over completed run records: H2 conflict subset + H3 sessions.

Reads run records written by run_pipeline.py and the datagen qrels; prints the
tables the Results section needs. Deterministic, no LLM. Part of the released
artifact so reviewers can reproduce every reported number from the run records.

Usage: python3 analyze_results.py
"""

import json
import random
from pathlib import Path

from agentrec.eval.metrics import load_qrels, evaluate_runs, dcg, ndcg_at_k

HERE = Path(__file__).parent
QRELS = load_qrels(HERE / "datagen/out/qrels.csv")
STUDENTS = json.loads((HERE / "datagen/out/students.json").read_text())
EVAL_100 = [s["student_id"] for s in STUDENTS[:100]]
CONFLICT_56 = [s["student_id"] for s in STUDENTS[:100] if s["h2_conflict"]]
H3_30 = [s["student_id"] for s in STUDENTS[:30]]


def records(run_dir, students=None, session=None):
    out = []
    for p in sorted((HERE / run_dir).glob("ST*.json")):
        r = json.loads(p.read_text())
        if students and r["student_id"] not in students:
            continue
        if session and r["session"] != session:
            continue
        out.append(r)
    return out


def show(label, res, extra=""):
    print(f"{label:42s} n={res['n']:3d}  NDCG@5={res['ndcg@5']:.3f}  "
          f"P@5={res['precision@5']:.3f}  R@5={res['recall@5']:.3f}{extra}")


def mean_len(recs):
    return round(sum(len(r["final_shortlist"]) for r in recs) / max(len(recs), 1), 2)


print("== H1 (eval split n=100, session 1, full information) ==")
for label, d in [("five-agent v1", "runs_h1/full"),
                 ("five-agent v2", "runs_h1/full_v2"),
                 ("single-prompt", "runs_h1/single_prompt"),
                 ("single-prompt (grounded)", "runs_h1/single_prompt_grounded")]:
    recs = records(d, students=EVAL_100, session=1)
    show(label, evaluate_runs(recs, QRELS), f"  |list|={mean_len(recs)}")

print("\n== H2 (conflict subset n=56, session 1, full information) ==")
for label, d in [("five-agent v1 (multi-objective)", "runs_h1/full"),
                 ("five-agent v2 (multi-objective)", "runs_h1/full_v2"),
                 ("single-objective ablation", "runs_h1/single_objective"),
                 ("single-prompt", "runs_h1/single_prompt")]:
    recs = records(d, students=CONFLICT_56, session=1)
    show(label, evaluate_runs(recs, QRELS))

print("\n== H3 (n=30, progressive disclosure, per session) ==")
for mode in ["full", "no_memory"]:
    for s in [1, 2, 3]:
        recs = records(f"runs_h3/{mode}", students=H3_30, session=s)
        show(f"{mode} s{s}", evaluate_runs(recs, QRELS))

print("\n== H3 deltas (full - no_memory), per session ==")
for s in [1, 2, 3]:
    a = evaluate_runs(records("runs_h3/full", students=H3_30, session=s), QRELS)
    b = evaluate_runs(records("runs_h3/no_memory", students=H3_30, session=s), QRELS)
    print(f"s{s}: dNDCG@5={a['ndcg@5']-b['ndcg@5']:+.3f}  "
          f"dP@5={a['precision@5']-b['precision@5']:+.3f}  "
          f"dR@5={a['recall@5']-b['recall@5']:+.3f}")


# --------------------------------------------------------------------------- stats
# Paired bootstrap CIs behind every "statistically indistinguishable" claim in the
# Results section (review-requested, 2026-07-27) -- these compare per-student
# scores between two conditions run on the identical eval-split students, so a
# paired (not independent-sample) bootstrap on the mean difference is the right test.

def paired_bootstrap_ci(diffs, n_boot=10000, seed=42, alpha=0.05):
    rng = random.Random(seed)
    n = len(diffs)
    boot_means = []
    for _ in range(n_boot):
        boot_means.append(sum(diffs[rng.randrange(n)] for _ in range(n)) / n)
    boot_means.sort()
    lo = boot_means[int(alpha / 2 * n_boot)]
    hi = boot_means[int((1 - alpha / 2) * n_boot)]
    return lo, hi


def ndcg_at_own_length(ranked_ids, qrel_row):
    """NDCG normalized by the system's own emitted list length, not a fixed k --
    isolates rank quality of what was actually shown from the padding-to-k penalty
    (Results section, H1 diagnostics)."""
    k = len(ranked_ids)
    if k == 0:
        return 0.0
    got = dcg([qrel_row.get(pid, 0) for pid in ranked_ids[:k]])
    ideal = dcg(sorted(qrel_row.values(), reverse=True)[:k])
    return got / ideal if ideal > 0 else 0.0


def paired_diffs(dir_a, dir_b, students, session, score_fn):
    recs_a = {r["student_id"]: r for r in records(dir_a, students=students, session=session)}
    recs_b = {r["student_id"]: r for r in records(dir_b, students=students, session=session)}
    common = sorted(set(recs_a) & set(recs_b))
    return [score_fn(recs_a[sid]) - score_fn(recs_b[sid]) for sid in common], len(common)


print("\n== Paired-comparison statistics behind 'statistically indistinguishable' claims ==")

diffs, n = paired_diffs(
    "runs_h1/full", "runs_h1/single_prompt", EVAL_100, 1,
    lambda r: ndcg_at_own_length(r["final_shortlist"], QRELS[r["student_id"]]))
mean_diff = sum(diffs) / n
lo, hi = paired_bootstrap_ci(diffs)
print(f"H1 emitted-length NDCG, five-agent v1 - single-prompt: n={n}  "
      f"mean(v1)=0.827  mean(single-prompt)=0.830 (per Results text)  "
      f"paired mean diff={mean_diff:+.4f}  95% CI=[{lo:+.4f}, {hi:+.4f}]  "
      f"{'crosses zero' if lo < 0 < hi else 'does not cross zero'}")

diffs2, n2 = paired_diffs(
    "runs_h1/full_v2", "runs_h1/single_objective_v2", CONFLICT_56, 1,
    lambda r: ndcg_at_k(r["final_shortlist"], QRELS[r["student_id"]], 5))
mean_diff2 = sum(diffs2) / n2
lo2, hi2 = paired_bootstrap_ci(diffs2)
print(f"H2 conflict subset (v2), multi-objective - single-objective: n={n2}  "
      f"paired mean diff={mean_diff2:+.4f}  95% CI=[{lo2:+.4f}, {hi2:+.4f}]  "
      f"{'crosses zero' if lo2 < 0 < hi2 else 'does not cross zero'}")
