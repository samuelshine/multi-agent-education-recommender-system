#!/usr/bin/env python3
"""Run both classical baselines over the synthetic dataset and score vs qrels.

Split: students ST0100..ST0299 are HRSPCA's historical training pool; ST0000..ST0099
are the evaluation set for ALL systems (baselines here, agentic pipeline batches).
Deterministic and fast (no LLM calls).
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))

from agentrec.eval.metrics import load_qrels, ndcg_at_k, precision_at_k, recall_at_k
from agentrec.simulate import render_message
from hrspca import HRSPCA
from studieme import StudieMe

K = 5
DATA = HERE.parent / "datagen" / "out"


def main():
    students = json.loads((DATA / "students.json").read_text())
    programs = json.loads((DATA / "programs.json").read_text())
    qrels = load_qrels(DATA / "qrels.csv")

    eval_set, train_set = students[:100], students[100:]
    train_qrels = {s["student_id"]: qrels[s["student_id"]] for s in train_set}

    hrspca = HRSPCA(programs, train_set, train_qrels)
    studieme = StudieMe(programs)

    results = {}
    for name, rank_fn in [
        ("hrspca", lambda s: hrspca.recommend(s, K)),
        ("studieme", lambda s: studieme.recommend(
            s, render_message(s, {"session": 3, "revealed_fields": "all"}), K)),
    ]:
        rows = []
        for s in eval_set:
            ranked = rank_fn(s)
            q = qrels[s["student_id"]]
            rows.append({"student_id": s["student_id"], "ranked": ranked,
                         "ndcg": ndcg_at_k(ranked, q, K),
                         "precision": precision_at_k(ranked, q, K),
                         "recall": recall_at_k(ranked, q, K)})
        n = len(rows)
        summary = {f"ndcg@{K}": round(sum(r["ndcg"] for r in rows) / n, 4),
                   f"precision@{K}": round(sum(r["precision"] for r in rows) / n, 4),
                   f"recall@{K}": round(sum(r["recall"] for r in rows) / n, 4),
                   "n": n}
        results[name] = {"summary": summary, "per_student": rows}
        print(name, json.dumps(summary))

    out = HERE / "results_baselines.json"
    out.write_text(json.dumps(results, indent=1))
    print("written:", out)


if __name__ == "__main__":
    main()
