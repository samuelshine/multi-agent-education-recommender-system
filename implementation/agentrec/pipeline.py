"""Pipeline orchestrator: the five-agent flow plus the three ablation modes.

Modes (paper Section: Evaluation Plan ablations):
- full:             profiling -> retrieval -> recommend -> reflect -> explain, with memory
- no_memory:        same, but no MEMORY block ever injected (H3 ablation)
- single_objective: recommend ranks by academic fit only (H2 ablation)
- single_prompt:    one LLM call does everything after the deterministic prefilter
                    (architecture ablation, cf. onlinecoursemaskg)

Spike requirements carried in (spike/SPIKE_REPORT.md):
#1 hard admission filter — deterministic, applied in the prefilter AND as a
   post-reflection guard; unknown values never count as violations.
#2 revision-action validation — schemas.check_reflection; one re-prompt naming the
   violation, then fail-closed to the pre-reflection shortlist.
#3 throughput — LLM cache (llm.py) + run records safe to resume.
"""

import json
import time

from . import prompts, schemas
from .memory import MemoryStore
from .simulate import render_message

K = 5            # max shortlist size
PRE_N = 20       # deterministic prefilter keeps top PRE_N candidates
N_SELECT = 8     # retrieval agent narrows to N_SELECT


# ------------------------------------------------------------- deterministic layer

def admission_infeasible(constraints: dict, program: dict) -> bool:
    """Hard filter (spike req #1). Unknown student values are NOT violations."""
    grade = (constraints.get("academic_background") or {}).get("grade_pct")
    if isinstance(grade, (int, float)) and grade < program["min_grade_pct"] - 5:
        return True
    return False


def hard_violates(constraints: dict, program: dict) -> bool:
    if admission_infeasible(constraints, program):
        return True
    budget = constraints.get("budget_max_usd_per_year")
    if isinstance(budget, (int, float)) and \
            program["annual_tuition_usd"] > 1.25 * budget:
        return True
    mobility = constraints.get("mobility")
    home = (constraints.get("location_preference") or "")
    if mobility == "fixed_city" and home and \
            program["city"].lower() not in home.lower():
        return True
    if mobility in ("fixed_city", "prefers_region", "open_domestic") and \
            program["country"] != "India":
        return True
    return False


def prefilter(constraints: dict, programs: list) -> list:
    """Drop hard violations, rank survivors by a cheap heuristic, keep PRE_N."""
    goal = " ".join(str(constraints.get(f) or "") for f in
                    ("career_goal", "other_constraints")).lower()
    scored = []
    for p in programs:
        if hard_violates(constraints, p):
            continue
        kw = sum(1 for f in p["fields"] if any(
            tok in goal for tok in f.split("_") if len(tok) > 3))
        emp = p["placement_rate_pct"] / 100 + \
            min(p["median_starting_salary_usd"] / 50000, 1.0)
        scored.append((kw * 2 + emp, p))
    scored.sort(key=lambda t: -t[0])
    return [p for _, p in scored[:PRE_N]]


def slim(p: dict) -> dict:
    """Program fields shown to the LLM (drop generation internals like tier)."""
    keep = ("program_id", "institution", "program", "fields", "city", "country",
            "annual_tuition_usd", "min_grade_pct", "requires_cs_background",
            "english_requirement", "placement_rate_pct",
            "median_starting_salary_usd", "post_study_work_visa_months")
    return {k: p[k] for k in keep}


# ------------------------------------------------------------------ orchestration

class Pipeline:
    def __init__(self, llm, programs: list, mode: str = "full", memory_dir=None,
                 version: int = 1):
        assert mode in ("full", "no_memory", "single_objective", "single_prompt")
        assert version in (1, 2)
        self.llm = llm
        self.programs = programs
        self.by_id = {p["program_id"]: p for p in programs}
        self.mode = mode
        self.version = version   # v2 = post-registration pruning-policy revision
        self.memory = (MemoryStore(memory_dir)
                       if mode not in ("no_memory",) and memory_dir else None)

    # one validated LLM step: parse -> check -> one re-prompt -> fallback
    def _step(self, name, system, user, checker, fallback):
        for attempt in (1, 2):
            raw = self.llm.chat(system, user, force_json=True)
            try:
                return checker(schemas.parse_json(raw, name)), attempt, False
            except schemas.SchemaError as e:
                if attempt == 1:
                    user = user + f"\n\nYour previous output was rejected: {e}. " \
                                   "Emit corrected JSON only."
        return fallback(), 2, True

    def run(self, student: dict, session: dict) -> dict:
        t0 = time.time()
        sid = student["student_id"]
        message = render_message(student, session)
        mem_block = self.memory.render_block(sid) if self.memory else None
        record = {"student_id": sid, "session": session["session"],
                  "mode": self.mode, "version": self.version, "message": message,
                  "memory_used": mem_block is not None, "fallbacks": []}

        # ---- profiling
        user = message if not mem_block else f"{mem_block}\n\nCURRENT MESSAGE:\n{message}"
        constraints, _, failed = self._step(
            "profiling", prompts.PROFILING, user, schemas.check_constraints,
            fallback=lambda: {"academic_background": {}, "career_goal": None,
                              "budget_max_usd_per_year": None,
                              "location_preference": None, "mobility": "open_domestic",
                              "employability_priority": "medium",
                              "other_constraints": [], "uncertainty_notes":
                              ["profiling failed; neutral defaults"]})
        if failed:
            record["fallbacks"].append("profiling")
        record["constraints"] = constraints

        # ---- deterministic prefilter
        candidates = prefilter(constraints, self.programs)
        record["prefilter_ids"] = [p["program_id"] for p in candidates]
        cand_ids = set(record["prefilter_ids"])
        cand_json = json.dumps([slim(p) for p in candidates], indent=1)
        cons_json = json.dumps(constraints, indent=1)

        if self.mode == "single_prompt":
            obj, _, failed = self._step(
                "single_prompt",
                prompts.SINGLE_PROMPT_BASELINE.format(k=K),
                f"Student message:\n{message}\n\nCandidate programs:\n{cand_json}",
                lambda o: schemas.check_shortlist(
                    {"shortlist": [{**s, "scores": s.get("scores", {
                        "academic_fit": 0, "financial_feasibility": 0,
                        "location_fit": 0, "employability": 0})}
                        for s in o.get("shortlist", [])]}, cand_ids, K),
                fallback=lambda: {"shortlist": [
                    {"program_id": p["program_id"], "rank": i + 1, "explanation": ""}
                    for i, p in enumerate(candidates[:K])]})
            if failed:
                record["fallbacks"].append("single_prompt")
            final_ids = [s["program_id"] for s in obj["shortlist"]]
            record["final_shortlist"] = final_ids
            record["explanation"] = "\n\n".join(
                s.get("explanation", "") for s in obj["shortlist"])
            record["wall_s"] = round(time.time() - t0, 1)
            return record

        # ---- retrieval
        sel, _, failed = self._step(
            "retrieval", prompts.RETRIEVAL.format(n_select=N_SELECT),
            f"Student-constraint object:\n{cons_json}\n\nCandidates:\n{cand_json}",
            lambda o: schemas.check_candidates(o, cand_ids),
            fallback=lambda: {"candidates": [
                {"program_id": p["program_id"], "why_relevant": "prefilter fallback",
                 "hard_constraint_check": {}} for p in candidates[:N_SELECT]]})
        if failed:
            record["fallbacks"].append("retrieval")
        sel_ids = [c["program_id"] for c in sel["candidates"]][:N_SELECT]
        sel_json = json.dumps([slim(self.by_id[i]) for i in sel_ids], indent=1)
        record["retrieved_ids"] = sel_ids

        # ---- recommend (single_objective swaps the prompt: the H2 ablation)
        rec_prompt = (prompts.RECOMMEND_SINGLE_OBJECTIVE
                      if self.mode == "single_objective" else
                      (prompts.RECOMMEND_V2 if self.version == 2
                       else prompts.RECOMMEND))
        rec_user = f"Student-constraint object:\n{cons_json}\n\nCandidate programs:\n{sel_json}"
        if mem_block and self.mode == "full":
            rec_user = f"{mem_block}\n\n{rec_user}"
        checker = (lambda o: schemas.check_shortlist(
            {"shortlist": [{**s, "scores": {"academic_fit": s["scores"].get("academic_fit", 0),
                                            "financial_feasibility": 0, "location_fit": 0,
                                            "employability": 0}} for s in o["shortlist"]]},
            set(sel_ids), K)) if self.mode == "single_objective" else \
            (lambda o: schemas.check_shortlist(o, set(sel_ids), K))
        rec, _, failed = self._step(
            "recommend", rec_prompt.format(k=K), rec_user, checker,
            fallback=lambda: {"shortlist": [
                {"program_id": i, "rank": n + 1,
                 "scores": {"academic_fit": 0, "financial_feasibility": 0,
                            "location_fit": 0, "employability": 0},
                 "tradeoff_note": "recommend fallback"} for n, i in
                enumerate(sel_ids[:K])]})
        if failed:
            record["fallbacks"].append("recommend")
        shortlist_ids = [s["program_id"] for s in rec["shortlist"]]
        record["proposed_shortlist"] = shortlist_ids

        # ---- reflect
        refl, _, failed = self._step(
            "reflect",
            (prompts.REFLECT_V2 if self.version == 2 else prompts.REFLECT).format(k=K),
            f"Student-constraint object:\n{cons_json}"
            f"\n\nProposed shortlist:\n{json.dumps(rec['shortlist'], indent=1)}"
            f"\n\nFull candidate set:\n{sel_json}",
            lambda o: schemas.check_reflection(o, shortlist_ids, set(sel_ids), K),
            fallback=lambda: {"approved": True, "violations_found": [],
                              "revisions": [], "final_shortlist": shortlist_ids,
                              "reflection_note": "reflect fallback: kept proposal"})
        if failed:
            record["fallbacks"].append("reflect")
        final_ids = refl["final_shortlist"]

        # ---- post-reflection deterministic guard (spike req #1, final guarantee)
        guarded = [i for i in final_ids
                   if not hard_violates(constraints, self.by_id[i])]
        record["guard_dropped"] = sorted(set(final_ids) - set(guarded))
        final_ids = guarded or final_ids[:1]

        # ---- v2 deterministic backfill: restore list to K with valid candidates
        # (retrieval order), so abstention below K happens only when the candidate
        # pool is genuinely exhausted. v1 never backfills (pre-registered behavior).
        if self.version == 2 and len(final_ids) < K:
            pool = [i for i in sel_ids
                    if i not in final_ids
                    and not hard_violates(constraints, self.by_id[i])]
            record["backfilled"] = pool[: K - len(final_ids)]
            final_ids = final_ids + record["backfilled"]
        record["final_shortlist"] = final_ids
        record["reflection_note"] = refl["reflection_note"]

        # ---- explain
        final_json = json.dumps([slim(self.by_id[i]) for i in final_ids], indent=1)
        record["explanation"] = self.llm.chat(
            prompts.EXPLAIN,
            f"Student-constraint object:\n{cons_json}\n\nFinal shortlist:\n{final_json}",
            force_json=False)

        # ---- memory write
        if self.memory:
            self.memory.update(sid, session["session"], constraints, final_ids,
                               session.get("feedback"))
        record["wall_s"] = round(time.time() - t0, 1)
        return record
