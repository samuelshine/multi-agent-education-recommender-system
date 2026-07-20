#!/usr/bin/env python3
"""Paper-facing analysis of LLM-as-judge explanation-quality scores.

Reads the 6 judge_*.json files (2 judges x 3 systems) and prints per-system means,
inter-judge agreement (mean absolute difference per dimension), and the invented-claims
rate (groundedness failure signal). Deterministic, no LLM. Part of the released
artifact so reviewers can reproduce every reported number.

Usage: python3 analyze_judge.py
"""

import json
from pathlib import Path

HERE = Path(__file__).parent
DIMS = ["clarity", "groundedness", "usefulness"]
SYSTEMS = [("five-agent v1", "runs_h1/full"),
           ("five-agent v2", "runs_h1/full_v2"),
           ("single-prompt", "runs_h1/single_prompt")]
JUDGES = ["qwen2.5_14b", "mistral-nemo_12b"]


def load(run_dir, judge):
    path = HERE / run_dir / f"judge_{judge}.json"
    doc = json.loads(path.read_text())
    return {r["student_id"]: r for r in doc["results"] if "error" not in r}


def mean(vals):
    return round(sum(vals) / len(vals), 3) if vals else float("nan")


print("== Per-system, per-judge mean scores (1-5) ==")
all_data = {}
for label, d in SYSTEMS:
    all_data[label] = {}
    for j in JUDGES:
        rows = load(d, j)
        all_data[label][j] = rows
        n = len(rows)
        means = {dim: mean([r[dim] for r in rows.values()]) for dim in DIMS}
        n_invented = sum(1 for r in rows.values() if r.get("invented_claims"))
        print(f"{label:16s} {j:18s} n={n:3d}  "
              f"clarity={means['clarity']}  groundedness={means['groundedness']}  "
              f"usefulness={means['usefulness']}  invented_claims_flagged={n_invented}")

print("\n== Cross-judge mean (per system, per dimension) ==")
for label, d in SYSTEMS:
    q, m = all_data[label][JUDGES[0]], all_data[label][JUDGES[1]]
    common = sorted(set(q) & set(m))
    for dim in DIMS:
        vals = [(q[sid][dim] + m[sid][dim]) / 2 for sid in common]
        print(f"{label:16s} {dim:14s} cross-judge mean={mean(vals)}  (n={len(common)})")

print("\n== Inter-judge agreement: mean |qwen - mistral| per dimension ==")
for label, d in SYSTEMS:
    q, m = all_data[label][JUDGES[0]], all_data[label][JUDGES[1]]
    common = sorted(set(q) & set(m))
    diffs = {dim: mean([abs(q[sid][dim] - m[sid][dim]) for sid in common])
             for dim in DIMS}
    big_disagreements = sum(
        1 for sid in common
        if any(abs(q[sid][dim] - m[sid][dim]) > 1 for dim in DIMS)
    )
    print(f"{label:16s} n={len(common):3d}  mean|diff|: clarity={diffs['clarity']}  "
          f"groundedness={diffs['groundedness']}  usefulness={diffs['usefulness']}  "
          f"flagged(>1pt any dim)={big_disagreements}")

print("\n== Invented-claims detail (groundedness failures) ==")
for label, d in SYSTEMS:
    for j in JUDGES:
        rows = all_data[label][j]
        flagged = [(sid, r["invented_claims"]) for sid, r in rows.items()
                   if r.get("invented_claims")]
        if flagged:
            print(f"{label} / {j}: {len(flagged)} flagged")
            for sid, claims in flagged[:3]:
                print(f"    {sid}: {claims}")
