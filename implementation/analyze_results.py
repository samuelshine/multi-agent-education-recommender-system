#!/usr/bin/env python3
"""Paper-facing analysis over completed run records: H2 conflict subset + H3 sessions.

Reads run records written by run_pipeline.py and the datagen qrels; prints the
tables the Results section needs. Deterministic, no LLM. Part of the released
artifact so reviewers can reproduce every reported number from the run records.

Usage: python3 analyze_results.py
"""

import json
from pathlib import Path

from agentrec.eval.metrics import load_qrels, evaluate_runs

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
                 ("single-prompt", "runs_h1/single_prompt")]:
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
