"""Cross-session memory store — the Memory half of Memory & Reflection (H3).

One JSON file per student under the store dir. `no_memory` ablation simply never
constructs a store, so the pipeline sees session 1 conditions every time.
"""

import json
from pathlib import Path


class MemoryStore:
    def __init__(self, root):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, student_id):
        return self.root / f"{student_id}.json"

    def load(self, student_id) -> dict | None:
        p = self._path(student_id)
        return json.loads(p.read_text()) if p.exists() else None

    def update(self, student_id, session_no, constraints, final_shortlist, feedback):
        mem = self.load(student_id) or {"student_id": student_id, "sessions": []}
        mem["sessions"].append({
            "session": session_no,
            "constraints": constraints,
            "final_shortlist": final_shortlist,
            "feedback": feedback,
        })
        self._path(student_id).write_text(json.dumps(mem, indent=1))

    def render_block(self, student_id) -> str | None:
        """Compact MEMORY block injected into profiling/recommend prompts."""
        mem = self.load(student_id)
        if not mem or not mem["sessions"]:
            return None
        last = mem["sessions"][-1]
        liked, disliked = [], []
        for s in mem["sessions"]:
            fb = s.get("feedback") or {}
            liked += fb.get("liked", [])
            disliked += fb.get("disliked", [])
        return (
            "MEMORY (from earlier sessions — start from this, newer statements win):\n"
            + json.dumps({
                "known_constraints": last["constraints"],
                "previously_shortlisted": last["final_shortlist"],
                "student_liked": liked, "student_disliked": disliked,
            }, indent=1)
        )
