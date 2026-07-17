"""HRSPCA baseline — faithful re-implementation of Ragab, Mashat & Khedra (ISDA 2012),
"HRSPCA: Hybrid recommender system for predicting college admission", adapted to this
paper's pre-admission cross-institution task.

Original architecture (paper §III-§IV, full text read 2026-07-16):
  1. Track Recommender (TR): rule-based sorter/filter assigning students to study
     tracks (scientific/literary/affiliated/no-prep/rejected) via knowledge rules.
  2. College Recommender (CR): classifier + allocator. Allocation requires (i) passing
     preparatory courses, (ii) minimum prerequisite course scores per college,
     (iii) Weighted Relative Rate (WRR), (iv) college capacity.
  3. College Predictor (CP): compares the student with historical admitted-student
     data (GPA + qualification marks) to predict most-probable colleges.

Every adaptation/underspecified choice is logged in RECONSTRUCTION.md (H-1..H-7).
Deterministic, stdlib only.
"""

import math

ADJACENT = {  # mirror of datagen field adjacency (track analog, see H-2)
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


class HRSPCA:
    def __init__(self, programs, train_students, train_qrels,
                 w_wrr=0.5, w_cp=0.5, k_neighbors=10):
        self.programs = programs
        self.by_id = {p["program_id"]: p for p in programs}
        self.train = train_students
        self.train_qrels = train_qrels          # student_id -> {program_id: grade}
        self.w_wrr, self.w_cp, self.k = w_wrr, w_cp, k_neighbors

    # ---- stage 1: Track Recommender (rule-based field track, H-2)
    def _track_ok(self, student, program):
        fields = set(program["fields"])
        goal = student["career_goal_field"]
        return goal in fields or bool(fields & ADJACENT[goal])

    # ---- stage 2: College Recommender rules (H-3, H-4)
    def _rules_ok(self, student, program):
        # prerequisite minimum-score rule analog: student grade meets program bar
        return student["academic_pct"] >= program["min_grade_pct"]

    def _wrr(self, student, program):
        # Weighted Relative Rate (formula lost to a figure in the source PDF; H-5):
        # student's weighted score relative to the program's admission bar.
        rel = student["academic_pct"] / max(program["min_grade_pct"], 1)
        apt = student["coding_skill"] / 9.0           # aptitude analog (H-5)
        return 0.5 * min(rel, 1.5) / 1.5 + 0.5 * apt

    # ---- stage 3: College Predictor (historical kNN, H-6)
    def _similarity(self, a, b):
        d_grade = abs(a["academic_pct"] - b["academic_pct"]) / 100
        d_skill = abs(a["coding_skill"] - b["coding_skill"]) / 9
        d_field = 0.0 if a["career_goal_field"] == b["career_goal_field"] else \
            (0.5 if b["career_goal_field"] in ADJACENT[a["career_goal_field"]] else 1.0)
        return 1.0 - (0.4 * d_grade + 0.2 * d_skill + 0.4 * d_field)

    def _predictor_votes(self, student):
        sims = sorted(((self._similarity(student, t), t) for t in self.train
                       if t["student_id"] != student["student_id"]),
                      key=lambda x: -x[0])[: self.k]
        votes = {}
        for sim, t in sims:
            for pid, g in self.train_qrels.get(t["student_id"], {}).items():
                if g >= 2:                       # historically "admitted-and-suitable"
                    votes[pid] = votes.get(pid, 0.0) + sim * (g / 3)
        mx = max(votes.values(), default=1.0)
        return {pid: v / mx for pid, v in votes.items()}

    def recommend(self, student, k=5):
        votes = self._predictor_votes(student)
        scored = []
        for p in self.programs:
            if not self._track_ok(student, p):
                continue
            if not self._rules_ok(student, p):
                continue
            score = self.w_wrr * self._wrr(student, p) + \
                self.w_cp * votes.get(p["program_id"], 0.0)
            scored.append((score, p["program_id"]))
        scored.sort(key=lambda t: (-t[0], t[1]))
        return [pid for _, pid in scored[:k]]
