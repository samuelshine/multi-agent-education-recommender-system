#!/usr/bin/env python3
"""CLI for the agentrec pipeline: single students or batches, any mode.

Examples:
  python3 run_pipeline.py --n 2                          # smoke: 2 students, session 1
  python3 run_pipeline.py --students ST0000 --sessions 1,2,3 --mode full
  python3 run_pipeline.py --n 50 --mode single_prompt    # ablation batch
  python3 run_pipeline.py --n 5 --metrics                # also score vs qrels

Run records land in runs/<mode>/ as one JSON per (student, session) — safe to resume:
existing records are skipped unless --force.
"""

import argparse
import json
from pathlib import Path

from agentrec.llm import LLMClient
from agentrec.pipeline import Pipeline
from agentrec.eval.metrics import load_qrels, evaluate_runs

HERE = Path(__file__).parent


def simulated_feedback(prev_record, qrel_row, max_each=2):
    """Simulated-user reaction to what the system actually showed last session.

    The datagen sessions file scripts feedback from the oracle's global ranking,
    which can reference programs the student was never shown. For memory testing
    the student must react to the *actual* previous shortlist, so we grade it with
    the oracle: grade >= 2 -> liked, grade <= 1 -> disliked.
    """
    if not prev_record or not qrel_row:
        return None
    shown = prev_record["final_shortlist"]
    liked = [p for p in shown if qrel_row.get(p, 0) >= 2][:max_each]
    disliked = [p for p in shown if qrel_row.get(p, 0) <= 1][:max_each]
    if not liked and not disliked:
        return None
    return {"liked": liked, "disliked": disliked}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=str(HERE / "datagen" / "out"))
    ap.add_argument("--mode", default="full",
                    choices=["full", "no_memory", "single_objective", "single_prompt"])
    ap.add_argument("--students", help="comma-separated ids (default: first --n)")
    ap.add_argument("--n", type=int, default=2)
    ap.add_argument("--sessions", default="1")
    ap.add_argument("--model", default="gemma4:e4b")
    ap.add_argument("--backend", default="ollama", choices=["ollama", "openai"])
    ap.add_argument("--out", default=str(HERE / "runs"))
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--metrics", action="store_true")
    ap.add_argument("--all-revealed", action="store_true",
                    help="H1 full-information state: every requested session exposes "
                         "the complete profile with no scripted events/feedback — the "
                         "fair comparison against classical baselines, which receive "
                         "the full application form (see baselines/RECONSTRUCTION.md)")
    args = ap.parse_args()

    data = Path(args.data)
    students = {s["student_id"]: s for s in json.loads((data / "students.json").read_text())}
    programs = json.loads((data / "programs.json").read_text())
    sessions = json.loads((data / "sessions.json").read_text())

    ids = (args.students.split(",") if args.students
           else list(students)[: args.n])
    session_nos = [int(s) for s in args.sessions.split(",")]

    outdir = Path(args.out) / args.mode
    outdir.mkdir(parents=True, exist_ok=True)
    llm = LLMClient(backend=args.backend, model=args.model,
                    cache_dir=HERE / "cache")
    pipe = Pipeline(llm, programs, mode=args.mode,
                    memory_dir=outdir / "memory")

    qrels_all = load_qrels(data / "qrels.csv")
    records = []
    for sid in ids:
        for sn in session_nos:
            rec_path = outdir / f"{sid}_s{sn}.json"
            if rec_path.exists() and not args.force:
                records.append(json.loads(rec_path.read_text()))
                print(f"skip {sid} s{sn} (exists)")
                continue
            session = ({"session": sn, "revealed_fields": "all"}
                       if args.all_revealed else dict(sessions[sid][sn - 1]))
            if sn > 1 and not args.all_revealed:
                prev_path = outdir / f"{sid}_s{sn - 1}.json"
                prev = (json.loads(prev_path.read_text())
                        if prev_path.exists() else None)
                fb = simulated_feedback(prev, qrels_all.get(sid))
                if fb:
                    session["feedback"] = fb
            print(f"run  {sid} s{sn} [{args.mode}]", flush=True)
            rec = pipe.run(students[sid], session)
            rec_path.write_text(json.dumps(rec, indent=1))
            records.append(rec)
            print(f"     -> {rec['final_shortlist']}  "
                  f"({rec['wall_s']}s, fallbacks={rec['fallbacks']})", flush=True)

    print("\nllm stats:", json.dumps(llm.stats))
    if args.metrics:
        res = evaluate_runs(records, qrels_all)
        del res["per_student"]
        print("metrics:", json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
