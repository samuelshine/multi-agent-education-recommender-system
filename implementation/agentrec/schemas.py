"""Structural validation of agent outputs + deterministic revision-action checks.

Spike finding #2 (spike/SPIKE_REPORT.md): the model follows JSON schemas but its
revision *semantics* drift (e.g. swap_in for an item already present). Schemas are
therefore enforced deterministically here; a violation triggers exactly one re-prompt
with the violation named, then fail-closed (keep the pre-reflection shortlist).
"""

import json


class SchemaError(ValueError):
    pass


def parse_json(raw: str, agent: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise SchemaError(f"{agent}: output is not valid JSON ({e})") from e


def require(obj: dict, keys: list, agent: str):
    missing = [k for k in keys if k not in obj]
    if missing:
        raise SchemaError(f"{agent}: missing keys {missing}")


def check_constraints(obj: dict) -> dict:
    require(obj, ["academic_background", "career_goal", "budget_max_usd_per_year",
                  "location_preference", "mobility", "employability_priority",
                  "other_constraints", "uncertainty_notes"], "profiling")
    if obj["mobility"] not in ("fixed_city", "prefers_region",
                               "open_domestic", "open_international"):
        raise SchemaError(f"profiling: bad mobility {obj['mobility']!r}")
    return obj


def check_candidates(obj: dict, valid_ids: set) -> dict:
    require(obj, ["candidates"], "retrieval")
    for c in obj["candidates"]:
        require(c, ["program_id", "why_relevant", "hard_constraint_check"], "retrieval")
        if c["program_id"] not in valid_ids:
            raise SchemaError(f"retrieval: hallucinated id {c['program_id']!r}")
    return obj


def check_shortlist(obj: dict, valid_ids: set, k: int) -> dict:
    require(obj, ["shortlist"], "recommend")
    if not 1 <= len(obj["shortlist"]) <= k:
        raise SchemaError(f"recommend: shortlist size {len(obj['shortlist'])} not in 1..{k}")
    for s in obj["shortlist"]:
        require(s, ["program_id", "rank", "scores"], "recommend")
        if s["program_id"] not in valid_ids:
            raise SchemaError(f"recommend: hallucinated id {s['program_id']!r}")
        require(s["scores"], ["academic_fit", "financial_feasibility",
                              "location_fit", "employability"], "recommend.scores")
    return obj


def check_reflection(obj: dict, shortlist_ids: list, candidate_ids: set, k: int) -> dict:
    """Deterministic semantics for revision actions (spike requirement #2)."""
    require(obj, ["approved", "violations_found", "revisions",
                  "final_shortlist", "reflection_note"], "reflect")
    present = set(shortlist_ids)
    for r in obj["revisions"]:
        require(r, ["program_id", "action", "reason"], "reflect.revisions")
        pid, action = r["program_id"], r["action"]
        if action not in ("keep", "drop", "swap_in"):
            raise SchemaError(f"reflect: unknown action {action!r}")
        if action == "swap_in" and pid in present:
            raise SchemaError(f"reflect: swap_in for {pid} already on shortlist")
        if action in ("keep", "drop") and pid not in present:
            raise SchemaError(f"reflect: {action} for {pid} not on shortlist")
        if action == "swap_in" and pid not in candidate_ids:
            raise SchemaError(f"reflect: swap_in {pid} not in candidate set")
    final = obj["final_shortlist"]
    if not 1 <= len(final) <= k:
        raise SchemaError(f"reflect: final shortlist size {len(final)} not in 1..{k}")
    unknown = [p for p in final if p not in candidate_ids]
    if unknown:
        raise SchemaError(f"reflect: final shortlist ids not in candidate set: {unknown}")
    if len(set(final)) != len(final):
        raise SchemaError("reflect: duplicate ids in final shortlist")
    return obj
