#!/usr/bin/env python3
"""Synthetic constraint-preference dataset generator.

Role in the paper (see ../../paper/chapter_plan.md, Methodology): the H2/H3 testbed
(conflicting constraints, multi-session cold start) and the H1 fallback benchmark.
Seeded from the public 20k-record student-features corpus (El-Keiey et al. 2025;
github.com/KLGLUG/student-career-area-prediction-using-machine-learning, GPL-3.0):
we sample real feature ROWS to get realistic co-occurrences (grades x skills x career
label), but the seed file itself is never redistributed — run download via README.

Integrity notes (also in the generated dataset_card.md):
- Institutions are FICTIONAL (real cities, invented names): no claims about real
  universities are fabricated.
- Ground-truth relevance comes from a published oracle utility defined here,
  independent of any system under evaluation. Circularity limitation is documented.
- Fully deterministic given --seed.

Usage: python3 generate.py [--seed 42] [--students 300] [--programs 200] [--out out]
Needs: seed/roo_data.csv (see README for download command). Stdlib only.
"""

import argparse
import csv
import json
import random
import statistics
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------------------------- vocabularies

# 34 seed job-role labels -> program field tags
ROLE_TO_FIELD = {
    "Applications Developer": "software_engineering",
    "Mobile Applications Developer": "software_engineering",
    "Programmer Analyst": "software_engineering",
    "Software Developer": "software_engineering",
    "Software Engineer": "software_engineering",
    "Software Systems Engineer": "software_engineering",
    "Web Developer": "software_engineering",
    "CRM Technical Developer": "software_engineering",
    "Technical Engineer": "software_engineering",
    "Business Intelligence Analyst": "data_science_analytics",
    "Data Architect": "data_science_analytics",
    "Database Developer": "data_science_analytics",
    "Database Administrator": "data_science_analytics",
    "Database Manager": "data_science_analytics",
    "E-Commerce Analyst": "business_information_systems",
    "Business Systems Analyst": "business_information_systems",
    "CRM Business Analyst": "business_information_systems",
    "Systems Analyst": "business_information_systems",
    "Information Security Analyst": "cybersecurity",
    "Network Security Administrator": "cybersecurity",
    "Network Security Engineer": "cybersecurity",
    "Systems Security Administrator": "cybersecurity",
    "Information Technology Auditor": "cybersecurity",
    "Network Engineer": "networking_cloud",
    "Solutions Architect": "networking_cloud",
    "Portal Administrator": "networking_cloud",
    "Information Technology Manager": "it_management",
    "Project Manager": "it_management",
    "Quality Assurance Associate": "qa_testing",
    "Software Quality Assurance (QA) / Testing": "qa_testing",
    "Design & UX": "design_hci",
    "UX Designer": "design_hci",
    "Technical Services/Help Desk/Tech Support": "it_support",
    "Technical Support": "it_support",
}
FIELDS = sorted(set(ROLE_TO_FIELD.values()))
# fields a student would consider "adjacent" to their goal field
ADJACENT = {
    "software_engineering": {"qa_testing", "networking_cloud", "data_science_analytics"},
    "data_science_analytics": {"software_engineering", "business_information_systems"},
    "business_information_systems": {"data_science_analytics", "it_management"},
    "cybersecurity": {"networking_cloud", "software_engineering"},
    "networking_cloud": {"cybersecurity", "software_engineering"},
    "it_management": {"business_information_systems", "software_engineering"},
    "qa_testing": {"software_engineering"},
    "design_hci": {"software_engineering", "business_information_systems"},
    "it_support": {"networking_cloud", "qa_testing"},
}

PROGRAM_NAME = {
    "software_engineering": ["MSc Software Engineering", "MCA", "MTech Computer Science"],
    "data_science_analytics": ["MSc Data Science", "MTech Data Engineering", "MSc Big Data Analytics"],
    "business_information_systems": ["MSc Information Systems", "MBA Business Analytics"],
    "cybersecurity": ["MTech Cyber Security", "MSc Information Security"],
    "networking_cloud": ["MSc Cloud Computing", "MTech Computer Networks"],
    "it_management": ["MSc IT Management", "MBA Technology Management"],
    "qa_testing": ["MSc Software Quality Engineering"],
    "design_hci": ["MDes Interaction Design", "MSc Human-Computer Interaction"],
    "it_support": ["MSc IT Operations", "PG Diploma in Systems Administration"],
}

# (country, region, cities, tuition_range_usd by tier, visa_months, salary_mult)
GEOS = [
    ("India", "south_asia",
     ["Bengaluru", "Pune", "Chennai", "Hyderabad", "Kolkata", "Delhi", "Mumbai", "Coimbatore"],
     {"elite": (2000, 5000), "strong": (1200, 4000), "mid": (800, 2500), "budget": (400, 1500)},
     0, 1.0, 0.60),
    ("Germany", "europe", ["Munich", "Berlin", "Aachen", "Dresden"],
     {"elite": (300, 1500), "strong": (300, 3000), "mid": (1500, 6000), "budget": (1000, 4000)},
     18, 3.2, 0.10),
    ("Netherlands", "europe", ["Amsterdam", "Delft", "Eindhoven"],
     {"elite": (16000, 21000), "strong": (13000, 18000), "mid": (11000, 15000), "budget": (9000, 13000)},
     12, 3.0, 0.06),
    ("UK", "europe", ["London", "Glasgow", "Manchester", "Edinburgh"],
     {"elite": (28000, 40000), "strong": (18000, 28000), "mid": (13000, 20000), "budget": (10000, 15000)},
     24, 2.6, 0.08),
    ("Canada", "north_america", ["Toronto", "Waterloo", "Vancouver", "Montreal"],
     {"elite": (25000, 40000), "strong": (18000, 30000), "mid": (12000, 22000), "budget": (9000, 16000)},
     36, 3.5, 0.10),
    ("USA", "north_america", ["Boston", "Austin", "Seattle", "Pittsburgh"],
     {"elite": (45000, 65000), "strong": (30000, 50000), "mid": (20000, 35000), "budget": (14000, 25000)},
     12, 5.5, 0.06),
]
TIERS = [("elite", 0.10), ("strong", 0.25), ("mid", 0.40), ("budget", 0.25)]

INSTITUTE_STEMS = [
    "Meridian", "Northgate", "Ashford", "Cavendish", "Silverline", "Braxton",
    "Kestrel", "Halcyon", "Vantage", "Crestwood", "Longford", "Aldermount",
    "Westbrook", "Stanmore", "Quilon", "Sarayu", "Nalanda Ridge", "Tejas",
    "Aravalli", "Charnock", "Keystone", "Bridgewater", "Elmhurst", "Fairfax",
]
INSTITUTE_KINDS = ["Institute of Technology", "University", "Technical University",
                   "School of Engineering", "Institute of Applied Sciences"]

# oracle weights by employability_priority (published; sum to 1.0)
WEIGHTS = {
    "high":   {"academic": 0.30, "financial": 0.20, "location": 0.15, "employability": 0.35},
    "medium": {"academic": 0.35, "financial": 0.25, "location": 0.20, "employability": 0.20},
    "low":    {"academic": 0.40, "financial": 0.30, "location": 0.20, "employability": 0.10},
}

# ---------------------------------------------------------------- generators


def gen_programs(rng, n):
    programs, used_names = [], set()
    for i in range(n):
        country, region, cities, tuition_by_tier, visa, sal_mult, share = \
            rng.choices(GEOS, weights=[g[6] for g in GEOS])[0]
        tier = rng.choices([t for t, _ in TIERS], weights=[w for _, w in TIERS])[0]
        field = rng.choice(FIELDS)
        extra = rng.random() < 0.35
        fields = sorted({field} | ({rng.choice(sorted(ADJACENT[field]))} if extra else set()))
        while True:
            name = f"{rng.choice(INSTITUTE_STEMS)} {rng.choice(INSTITUTE_KINDS)}"
            city = rng.choice(cities)
            if (name, city) not in used_names:
                used_names.add((name, city))
                break
        lo, hi = tuition_by_tier[tier]
        base_place = {"elite": 92, "strong": 84, "mid": 74, "budget": 64}[tier]
        placement = min(97, max(50, int(rng.gauss(base_place, 4))))
        base_sal = {"elite": 20000, "strong": 14000, "mid": 10000, "budget": 7500}[tier]
        salary = int(base_sal * sal_mult * rng.uniform(0.85, 1.15))
        min_grade = {"elite": 82, "strong": 72, "mid": 62, "budget": 55}[tier] + rng.randint(-3, 3)
        programs.append({
            "program_id": f"PR{i:04d}",
            "institution": name,                      # FICTIONAL institution
            "program": rng.choice(PROGRAM_NAME[field]),
            "fields": fields,
            "city": city, "country": country, "region": region,
            "tier": tier,
            "annual_tuition_usd": int(rng.uniform(lo, hi) // 50 * 50),
            "min_grade_pct": min_grade,
            "requires_cs_background": field in
                {"software_engineering", "data_science_analytics", "cybersecurity",
                 "networking_cloud"} and rng.random() < 0.6,
            "english_requirement": country != "India",
            "placement_rate_pct": placement,
            "median_starting_salary_usd": salary,
            "post_study_work_visa_months": visa,
        })
    return programs


def derive_student(rng, row, idx, home_cities):
    grades = [int(row[c]) for c in row if c.strip().lower().startswith(("acedamic", "percentage"))]
    academic_pct = round(statistics.mean(grades), 1)
    role = row["Suggested Job Role"]
    mobility = rng.choices(
        ["fixed_city", "prefers_region", "open_domestic", "open_international"],
        weights=[0.15, 0.25, 0.35, 0.25])[0]
    # budget: correlated with mobility ambition; lognormal-ish tiers (USD/yr)
    budget = int(rng.choice({
        "fixed_city": [1000, 1500, 2500, 4000, 6000],
        "prefers_region": [1500, 2500, 4000, 6000, 9000],
        "open_domestic": [1500, 2500, 4000, 6000, 12000],
        "open_international": [4000, 9000, 16000, 25000, 35000],
    }[mobility]) * rng.uniform(0.8, 1.2) // 100 * 100)
    emp_priority = ("high" if row["Salary/work"] == "salary" or row["Job/Higher Studies?"] == "job"
                    else rng.choice(["medium", "medium", "low"]))
    vague = rng.random() < 0.25  # cold-start sub-population for H3
    return {
        "student_id": f"ST{idx:04d}",
        "seed_row": row["_row_index"],           # provenance into seed CSV
        "academic_pct": academic_pct,
        "cs_background": True,                   # seed corpus is IT students
        "coding_skill": int(row["coding skills rating"]),
        "career_goal_role": role,
        "career_goal_field": ROLE_TO_FIELD[role],
        "career_goal_vague": vague,
        "interests": [row["Interested subjects"], row["interested career area "].strip()],
        "budget_max_usd_per_year": budget,
        "home_city": rng.choice(home_cities),
        "mobility": mobility,
        "employability_priority": emp_priority,
        "self_learner": row["self-learning capability?"] == "yes",
        "certifications": row["certifications"],
        "memory_capability": row["memory capability score"],
    }


def oracle(student, program):
    """Published ground-truth utility. Returns (utility 0..1, hard_violation, parts)."""
    # academic fit: field match x admission feasibility
    goal = student["career_goal_field"]
    if goal in program["fields"]:
        field_fit = 1.0
    elif set(program["fields"]) & ADJACENT[goal]:
        field_fit = 0.5
    else:
        field_fit = 0.1
    gap = student["academic_pct"] - program["min_grade_pct"]
    adm = 1.0 if gap >= 0 else (0.5 if gap >= -5 else 0.0)
    if program["requires_cs_background"] and not student["cs_background"]:
        adm = 0.0
    academic = field_fit * adm

    # financial feasibility
    ratio = program["annual_tuition_usd"] / max(student["budget_max_usd_per_year"], 1)
    financial = 1.0 if ratio <= 1.0 else (0.4 if ratio <= 1.25 else 0.0)

    # location fit under the mobility model
    same_city = program["city"] == student["home_city"]
    domestic = program["country"] == "India"
    location = {
        "fixed_city": 1.0 if same_city else 0.0,
        "prefers_region": 1.0 if same_city else (0.7 if domestic else 0.1),
        "open_domestic": 1.0 if domestic else 0.2,
        "open_international": 1.0,
    }[student["mobility"]]

    # employability (salary normalized against corpus max ~50k usable signal)
    employability = 0.6 * program["placement_rate_pct"] / 100 + \
        0.4 * min(program["median_starting_salary_usd"] / 50000, 1.0)

    w = WEIGHTS[student["employability_priority"]]
    utility = (w["academic"] * academic + w["financial"] * financial
               + w["location"] * location + w["employability"] * employability)
    hard_violation = academic == 0.0 or financial == 0.0 or location == 0.0
    return utility, hard_violation, {
        "academic": round(academic, 3), "financial": financial,
        "location": location, "employability": round(employability, 3)}


def grade(utility, hard_violation):
    if hard_violation:
        return 0
    return 3 if utility >= 0.75 else 2 if utility >= 0.55 else 1 if utility >= 0.35 else 0


def gen_sessions(rng, student, qrels_for_student):
    """3 sessions of progressive disclosure (H3) + drift events (H2)."""
    ranked = sorted(qrels_for_student, key=lambda q: -q["utility"])
    liked = [q["program_id"] for q in ranked[:2]]
    disliked = [q["program_id"] for q in ranked[-2:]]
    s1_fields = ["academic_pct", "cs_background", "interests"]
    if not student["career_goal_vague"]:
        s1_fields.append("career_goal_role")
    if rng.random() < 0.5:
        s1_fields.append("budget_max_usd_per_year")
    drift = rng.random() < 0.20
    sessions = [
        {"session": 1, "revealed_fields": sorted(s1_fields),
         "note": "cold start: no interaction history"},
        {"session": 2,
         "revealed_fields": sorted(set(s1_fields) | {
             "career_goal_role", "budget_max_usd_per_year", "home_city", "mobility"}),
         "feedback": {"liked": liked, "disliked": disliked}},
        {"session": 3, "revealed_fields": "all",
         "events": ([{"type": "budget_revised",
                      "new_budget_max_usd_per_year":
                          int(student["budget_max_usd_per_year"] * 0.6 // 100 * 100),
                      "reason": "family circumstances changed"}] if drift else [])},
    ]
    return sessions


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--students", type=int, default=300)
    ap.add_argument("--programs", type=int, default=200)
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    rng = random.Random(args.seed)

    seed_path = HERE / "seed" / "roo_data.csv"
    if not seed_path.exists():
        raise SystemExit("seed/roo_data.csv missing — see README for the download command")
    rows = list(csv.DictReader(open(seed_path)))
    for i, r in enumerate(rows):
        r["_row_index"] = i

    programs = gen_programs(rng, args.programs)
    india_cities = GEOS[0][2]
    sample = rng.sample(rows, args.students)
    students = [derive_student(rng, r, i, india_cities) for i, r in enumerate(sample)]

    qrels, by_student = [], {}
    for s in students:
        rel = []
        for p in programs:
            u, hard, parts = oracle(s, p)
            g = grade(u, hard)
            rel.append({"student_id": s["student_id"], "program_id": p["program_id"],
                        "utility": round(u, 4), "grade": g,
                        "hard_violation": hard, **{f"part_{k}": v for k, v in parts.items()}})
        by_student[s["student_id"]] = rel
        qrels.extend(rel)

    sessions = {s["student_id"]: gen_sessions(rng, s, by_student[s["student_id"]])
                for s in students}

    # conflict flag for H2: best academically-fitting program is financially infeasible
    n_conflict = 0
    for s in students:
        rel = by_student[s["student_id"]]
        best_acad = max(rel, key=lambda q: q["part_academic"])
        s["h2_conflict"] = best_acad["part_academic"] >= 0.5 and best_acad["part_financial"] == 0.0
        n_conflict += s["h2_conflict"]

    outdir = HERE / args.out
    outdir.mkdir(exist_ok=True)
    (outdir / "programs.json").write_text(json.dumps(programs, indent=1))
    (outdir / "students.json").write_text(json.dumps(students, indent=1))
    (outdir / "sessions.json").write_text(json.dumps(sessions, indent=1))
    with open(outdir / "qrels.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(qrels[0].keys()))
        w.writeheader()
        w.writerows(qrels)

    grades = [q["grade"] for q in qrels]
    stats = {
        "seed": args.seed, "students": len(students), "programs": len(programs),
        "qrel_pairs": len(qrels),
        "grade_distribution": {g: grades.count(g) for g in (0, 1, 2, 3)},
        "students_with_no_grade3": sum(
            1 for s in students
            if not any(q["grade"] == 3 for q in by_student[s["student_id"]])),
        "h2_conflict_students": n_conflict,
        "cold_start_vague_students": sum(s["career_goal_vague"] for s in students),
        "drift_students": sum(
            1 for sid in sessions if sessions[sid][2].get("events")),
    }
    (outdir / "stats.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
