#!/usr/bin/env python3
"""Week-1 spike: one full pass of the paper's five-agent pipeline on gemma4:e4b.

Purpose (chapter_plan.md, standing risk #2): detect early whether an effective-4B
local model can carry five-agent constraint reasoning and grounded explanation.
This is NOT the prototype — it is a disposable de-risking script. No retries, no
memory persistence across sessions, no RAG index (the toy KB fits in context).

Usage: python3 spike_pipeline.py [--model gemma4:e4b]
Outputs: outputs/results_<ts>.json (machine-readable) + outputs/transcript_<ts>.md
"""

import argparse
import json
import time
import urllib.request
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).parent
OLLAMA_URL = "http://localhost:11434/api/chat"


def chat(model: str, system: str, user: str, force_json: bool) -> tuple[str, float]:
    body = {
        "model": model,
        "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": 0.2, "num_ctx": 8192},
    }
    if force_json:
        body["format"] = "json"
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=600) as resp:
        out = json.loads(resp.read())
    return out["message"]["content"], time.time() - t0


AGENTS = {
    "profiling": (
        "You are the Profiling & Constraint Agent in a university-recommendation "
        "system for prospective students. Extract a structured student-constraint "
        "object from the student's free-text introduction. Output ONLY JSON with "
        "keys: academic_background (object: degree, grade), career_goal (string), "
        "budget_max_usd_per_year (number or null), location_preference (string), "
        "mobility (one of: fixed_city, prefers_region, open_domestic, open_international), "
        "employability_priority (high/medium/low), other_constraints (array of strings), "
        "uncertainty_notes (array of strings: anything the student is unsure about)."
    ),
    "retrieval": (
        "You are the Retrieval Agent. Given a student-constraint object and a "
        "knowledge base of programs, select up to 6 candidate programs worth "
        "considering. Check hard constraints honestly. Output ONLY JSON with key "
        "candidates: array of objects {kb_id, why_relevant, hard_constraint_check: "
        "{budget_ok (bool), location_ok (bool), admission_plausible (bool)}}. Use "
        "only kb_id values that exist in the knowledge base."
    ),
    "recommend": (
        "You are the Recommendation & Planning Agent. Rank the candidate programs "
        "against the student-constraint object under four objectives: academic_fit, "
        "financial_feasibility, location_fit, employability. Score each 0-10. "
        "Output ONLY JSON with key shortlist: array of exactly 3 objects "
        "{kb_id, rank (1-3), scores: {academic_fit, financial_feasibility, "
        "location_fit, employability}, tradeoff_note (string naming the main "
        "conflict this pick involves, if any)}."
    ),
    "reflect": (
        "You are the Memory & Reflection Agent. Critique the shortlist BEFORE it "
        "reaches the student: check every entry against the constraint object for "
        "violated hard constraints (budget, location, admission plausibility) and "
        "for missed better options in the candidate set. Output ONLY JSON: "
        "{approved (bool), violations_found (array of strings), revisions (array of "
        "{kb_id, action: keep/drop/swap_in, reason}), final_shortlist (array of 3 "
        "kb_ids in rank order), reflection_note (string)}."
    ),
    "explain": (
        "You are the Explanation Agent. For each program in the final shortlist, "
        "write one short paragraph (3-5 sentences) explaining to the student why it "
        "was recommended. Ground every factual claim in the provided knowledge-base "
        "fields (tuition, placement rate, salary, visa, strengths, admission) and "
        "the student's own stated constraints. Do not invent facts not present in "
        "the knowledge base. Plain text, one paragraph per program, headed by the "
        "university name."
    ),
}


def run_profile(model, profile, kb, kb_by_id, log):
    steps = {}

    def step(name, user_content, force_json=True):
        raw, dt = chat(model, AGENTS[name], user_content, force_json)
        parsed, parse_ok = None, True
        if force_json:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parse_ok = False
        steps[name] = {
            "latency_s": round(dt, 1),
            "parse_ok": parse_ok,
            "output": parsed if parse_ok and force_json else raw,
        }
        log(f"    {name}: {dt:.0f}s, parse_ok={parse_ok}")
        return parsed if force_json else raw

    constraints = step("profiling", f"Student introduction:\n{profile['text']}")

    cands = step(
        "retrieval",
        "Student-constraint object:\n" + json.dumps(constraints, indent=1)
        + "\n\nKnowledge base:\n" + json.dumps(kb, indent=1),
    )
    cand_ids = [c.get("kb_id") for c in (cands or {}).get("candidates", [])]
    cand_entries = [kb_by_id[i] for i in cand_ids if i in kb_by_id]

    shortlist = step(
        "recommend",
        "Student-constraint object:\n" + json.dumps(constraints, indent=1)
        + "\n\nCandidate programs:\n" + json.dumps(cand_entries, indent=1),
    )

    reflection = step(
        "reflect",
        "Student-constraint object:\n" + json.dumps(constraints, indent=1)
        + "\n\nProposed shortlist:\n" + json.dumps(shortlist, indent=1)
        + "\n\nFull candidate set:\n" + json.dumps(cand_entries, indent=1),
    )
    final_ids = (reflection or {}).get("final_shortlist", []) or [
        s.get("kb_id") for s in (shortlist or {}).get("shortlist", [])
    ]
    final_entries = [kb_by_id[i] for i in final_ids if i in kb_by_id]

    step(
        "explain",
        "Student-constraint object:\n" + json.dumps(constraints, indent=1)
        + "\n\nFinal shortlist with full data:\n" + json.dumps(final_entries, indent=1),
        force_json=False,
    )

    # Deterministic spike checks (the numbers the spike report cares about)
    budget = (constraints or {}).get("budget_max_usd_per_year")
    checks = {
        "hallucinated_kb_ids": sorted(
            {i for i in cand_ids + final_ids if i and i not in kb_by_id}
        ),
        "final_shortlist_size": len(final_ids),
        "budget_violations_in_final": [
            {"kb_id": e["kb_id"], "tuition": e["annual_tuition_usd"], "budget": budget}
            for e in final_entries
            if isinstance(budget, (int, float)) and e["annual_tuition_usd"] > budget
        ],
        "json_parse_failures": [k for k, v in steps.items() if not v["parse_ok"]],
    }
    return {"profile_id": profile["id"], "steps": steps, "checks": checks}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemma4:e4b")
    args = ap.parse_args()

    profiles = json.loads((HERE / "profiles.json").read_text())
    kb = json.loads((HERE / "knowledge_base.json").read_text())
    kb_by_id = {e["kb_id"]: e for e in kb}

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = HERE / "outputs"
    outdir.mkdir(exist_ok=True)

    results, t_start = [], time.time()
    for p in profiles:
        print(f"  profile {p['id']}", flush=True)
        try:
            results.append(run_profile(args.model, p, kb, kb_by_id,
                                        lambda m: print(m, flush=True)))
        except Exception as exc:  # a dead pipeline is itself a spike finding
            results.append({"profile_id": p["id"], "fatal_error": repr(exc)})
            print(f"    FATAL: {exc!r}", flush=True)

    summary = {
        "model": args.model,
        "started": ts,
        "wall_time_s": round(time.time() - t_start, 1),
        "profiles_run": len(results),
        "fatal_errors": sum(1 for r in results if "fatal_error" in r),
        "total_parse_failures": sum(
            len(r.get("checks", {}).get("json_parse_failures", [])) for r in results
        ),
        "total_hallucinated_ids": sum(
            len(r.get("checks", {}).get("hallucinated_kb_ids", [])) for r in results
        ),
        "total_budget_violations": sum(
            len(r.get("checks", {}).get("budget_violations_in_final", []))
            for r in results
        ),
        "mean_call_latency_s": round(
            (lambda ls: sum(ls) / len(ls) if ls else 0)(
                [s["latency_s"] for r in results
                 for s in r.get("steps", {}).values()]
            ), 1),
    }
    (outdir / f"results_{ts}.json").write_text(
        json.dumps({"summary": summary, "results": results}, indent=1)
    )

    lines = [f"# Spike transcript — {args.model} — {ts}", ""]
    for r in results:
        lines += [f"## {r['profile_id']}", ""]
        if "fatal_error" in r:
            lines += [f"**FATAL**: `{r['fatal_error']}`", ""]
            continue
        for name, s in r["steps"].items():
            body = (s["output"] if isinstance(s["output"], str)
                    else json.dumps(s["output"], indent=1))
            lines += [f"### {name} ({s['latency_s']}s, parse_ok={s['parse_ok']})",
                      "", "```", body, "```", ""]
        lines += ["### deterministic checks", "", "```",
                  json.dumps(r["checks"], indent=1), "```", ""]
    (outdir / f"transcript_{ts}.md").write_text("\n".join(lines))

    print(json.dumps(summary, indent=1), flush=True)


if __name__ == "__main__":
    main()
