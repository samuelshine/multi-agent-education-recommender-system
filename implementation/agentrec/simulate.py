"""Render a datagen student + session into a simulated student message.

The pipeline consumes free text (like a real prospective student typing), so
evaluation drives the same code path as live use. Only fields revealed in the
session appear in the message — the H3 cold-start manipulation happens here.
"""


def render_message(student: dict, session: dict) -> str:
    revealed = session["revealed_fields"]
    full = revealed == "all"

    def has(f):
        return full or f in revealed

    parts = [f"Hi, I'm a student with a {student['certifications']} certification "
             f"background." if has("interests") else "Hi."]
    if has("academic_pct"):
        parts.append(f"My overall academic average is {student['academic_pct']}% "
                     f"in an IT/computer-science degree.")
    if has("interests"):
        parts.append("I'm interested in " + " and ".join(student["interests"]) + ".")
    if has("career_goal_role"):
        if student["career_goal_vague"] and session["session"] == 1:
            parts.append("Honestly I'm not fully sure what I want to become — "
                         "something in tech.")
        else:
            parts.append(f"I want to become a {student['career_goal_role']}.")
    if has("budget_max_usd_per_year"):
        budget = student["budget_max_usd_per_year"]
        for ev in session.get("events", []):
            if ev["type"] == "budget_revised":
                budget = ev["new_budget_max_usd_per_year"]
                parts.append("Also, my situation changed: "
                             f"{ev['reason']}, so my budget is now lower.")
        parts.append(f"My family can afford at most about USD {budget} per year.")
    if has("home_city"):
        parts.append(f"I live in {student['home_city']}.")
    if has("mobility"):
        parts.append({
            "fixed_city": "I cannot leave my city.",
            "prefers_region": "I'd strongly prefer to stay near home, "
                              "though I might consider elsewhere in India.",
            "open_domestic": "I'm open to anywhere in India.",
            "open_international": "I'm open to going abroad.",
        }[student["mobility"]])
    if full and student["employability_priority"] == "high":
        parts.append("Getting a good job after graduation matters more to me "
                     "than anything else.")
    fb = session.get("feedback")
    if fb and (fb.get("liked") or fb.get("disliked")):
        bits = []
        if fb.get("liked"):
            bits.append("I liked " + ", ".join(fb["liked"]))
        if fb.get("disliked"):
            bits.append("please drop " + ", ".join(fb["disliked"]))
        parts.append("About the earlier suggestions: " + " but ".join(bits) + ".")
    return " ".join(parts)
