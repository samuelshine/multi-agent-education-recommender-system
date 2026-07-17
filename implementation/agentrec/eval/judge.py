"""LLM-as-judge for explanation quality (H1's primary claim).

Judge selection (decided 2026-07-16, rationale in ../../paper/chapter_plan.md):
- Cardinal rule: judge model family != experiment model family (gemma4 generates,
  so no Gemma judges) — self-preference bias runs 10-25% and is perplexity-driven,
  so a same-family judge inflates scores invisibly.
- Primary judge: qwen2.5:14b (Alibaba family, strong 14B-class local model).
- Agreement judge: mistral-nemo:12b (Mistral family). Two-judge agreement
  (Krippendorff-style on the 1-5 scale) is reported; disagreement > 1 point on any
  dimension flags the item for manual inspection.
- Absolute rubric scoring (not pairwise) avoids position bias; system identity is
  never revealed to the judge (blind judging).

Rubric (1-5 each, per explanation):
- clarity: readable, specific, well-structured for a prospective student
- groundedness: every factual claim traceable to the provided program fields and
  student constraints; invented facts cap the score at 1
- usefulness: helps the student decide; names trade-offs honestly

Pull models AFTER evaluation batches finish (GPU contention):
  ollama pull qwen2.5:14b && ollama pull mistral-nemo:12b
Usage: python3 -m agentrec.eval.judge --runs ../runs_h1/full --judge qwen2.5:14b
"""

import argparse
import json
from pathlib import Path

from ..llm import LLMClient

JUDGE_SYSTEM = (
    "You are an impartial evaluator of recommendation explanations written for "
    "prospective university students. You will see the student's constraint object, "
    "the recommended programs' data fields, and the explanation text. Score the "
    "explanation on three dimensions, each 1-5 (5 best):\n"
    "- clarity: readable, specific, well-structured for the student\n"
    "- groundedness: every factual claim must be traceable to the provided program "
    "fields or the student's constraints; if any claim is invented, groundedness "
    "is 1\n"
    "- usefulness: helps the student decide; honestly names trade-offs\n"
    "Output ONLY JSON: {\"clarity\": n, \"groundedness\": n, \"usefulness\": n, "
    "\"invented_claims\": [list any invented facts you found], "
    "\"justification\": \"one sentence\"}"
)


def judge_record(llm, record, programs_by_id):
    final = [programs_by_id[i] for i in record["final_shortlist"]
             if i in programs_by_id]
    user = (
        "Student-constraint object:\n" + json.dumps(record["constraints"], indent=1)
        + "\n\nRecommended programs (source of truth):\n"
        + json.dumps(final, indent=1)
        + "\n\nExplanation to evaluate:\n" + record["explanation"]
    )
    raw = llm.chat(JUDGE_SYSTEM, user, force_json=True)
    out = json.loads(raw)
    return {k: out.get(k) for k in
            ("clarity", "groundedness", "usefulness",
             "invented_claims", "justification")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True, help="dir of run-record JSONs")
    ap.add_argument("--judge", default="qwen2.5:14b")
    ap.add_argument("--data", default=str(Path(__file__).parents[2] / "datagen" / "out"))
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    programs = json.loads((Path(args.data) / "programs.json").read_text())
    by_id = {p["program_id"]: p for p in programs}
    llm = LLMClient(model=args.judge,
                    cache_dir=Path(__file__).parents[2].parent / "cache")

    results = []
    for f in sorted(Path(args.runs).glob("*_s*.json")):
        rec = json.loads(f.read_text())
        if not rec.get("explanation"):
            continue
        try:
            scores = judge_record(llm, rec, by_id)
        except Exception as exc:
            scores = {"error": repr(exc)}
        results.append({"file": f.name, "student_id": rec["student_id"],
                        "mode": rec["mode"], **scores})
        print(f.name, json.dumps(scores), flush=True)

    outpath = Path(args.out or (Path(args.runs) /
                                f"judge_{args.judge.replace(':', '_')}.json"))
    ok = [r for r in results if "error" not in r]
    summary = {dim: round(sum(r[dim] for r in ok) / len(ok), 3)
               for dim in ("clarity", "groundedness", "usefulness")} if ok else {}
    outpath.write_text(json.dumps({"judge": args.judge, "summary": summary,
                                   "n": len(ok), "results": results}, indent=1))
    print("summary:", json.dumps(summary), "->", outpath)


if __name__ == "__main__":
    main()
