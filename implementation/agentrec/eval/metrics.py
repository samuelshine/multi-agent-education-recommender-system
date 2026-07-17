"""Ranking metrics against datagen qrels: NDCG@k (headline, H1), precision@k, recall@k.

NDCG uses graded relevance (0-3) with the standard log2 discount; ideal ranking from
the student's full qrel row. Precision/recall treat grade >= 2 as relevant.
"""

import csv
import math
from collections import defaultdict


def load_qrels(path):
    by_student = defaultdict(dict)
    for row in csv.DictReader(open(path)):
        by_student[row["student_id"]][row["program_id"]] = int(row["grade"])
    return by_student


def dcg(grades):
    return sum(g / math.log2(i + 2) for i, g in enumerate(grades))


def ndcg_at_k(ranked_ids, qrel_row, k):
    got = dcg([qrel_row.get(pid, 0) for pid in ranked_ids[:k]])
    ideal = dcg(sorted(qrel_row.values(), reverse=True)[:k])
    return got / ideal if ideal > 0 else 0.0


def precision_at_k(ranked_ids, qrel_row, k, rel_grade=2):
    top = ranked_ids[:k]
    return sum(1 for pid in top if qrel_row.get(pid, 0) >= rel_grade) / max(len(top), 1)


def recall_at_k(ranked_ids, qrel_row, k, rel_grade=2):
    n_rel = sum(1 for g in qrel_row.values() if g >= rel_grade)
    if n_rel == 0:
        return 0.0
    hit = sum(1 for pid in ranked_ids[:k] if qrel_row.get(pid, 0) >= rel_grade)
    return hit / n_rel


def evaluate_runs(records, qrels, k=5):
    """records: list of pipeline run records (uses final_shortlist as the ranking)."""
    rows = []
    for r in records:
        q = qrels.get(r["student_id"])
        if not q:
            continue
        ranked = r["final_shortlist"]
        rows.append({
            "student_id": r["student_id"], "session": r["session"], "mode": r["mode"],
            "ndcg": ndcg_at_k(ranked, q, k),
            "precision": precision_at_k(ranked, q, k),
            "recall": recall_at_k(ranked, q, k),
        })
    n = len(rows)
    mean = lambda f: round(sum(r[f] for r in rows) / n, 4) if n else 0.0
    return {"n": n, f"ndcg@{k}": mean("ndcg"),
            f"precision@{k}": mean("precision"), f"recall@{k}": mean("recall"),
            "per_student": rows}
