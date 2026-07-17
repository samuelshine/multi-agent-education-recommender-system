"""StudieMe baseline — faithful re-implementation of Sharma, Trehan, Chanana & Dawn
(RDCAPE 2019), "StudieMe: College Recommendation System", adapted to this paper's task.

Original pipeline (paper §(b)-(d), full text read 2026-07-16):
  1. User profile text (resume/LinkedIn) + GRE score.
  2. Hard filter: keep colleges whose GRE cutoff <= the user's GRE
     (paper Function #1: ds.loc[ds['GRE Score'] >= gre] filters by cutoff).
  3. TF-IDF vectorization + cosine similarity between user text and subject/college
     documents (paper Function #3, sklearn TfidfVectorizer with stop words).
  4. Rank matched colleges, return the top ones.
  (Faculty-matching stage omitted — no faculty analog in our catalog; S-4.)

Deviations logged in RECONSTRUCTION.md (S-1..S-5). Deterministic, stdlib only.
"""

import math
import re
from collections import Counter

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "from", "has",
    "have", "i", "in", "is", "it", "its", "me", "my", "of", "on", "or", "that",
    "the", "to", "was", "we", "were", "will", "with", "you", "your", "am", "can",
    "about", "also", "im", "hi", "most", "than", "so", "not", "now", "no",
}


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower())
            if t not in STOPWORDS and len(t) > 1]


def program_document(p):
    return " ".join([
        p["program"], p["institution"], p["city"], p["country"],
        " ".join(f.replace("_", " ") for f in p["fields"]),
    ])


class StudieMe:
    def __init__(self, programs):
        self.programs = programs
        self.docs = {p["program_id"]: tokenize(program_document(p)) for p in programs}
        n = len(programs)
        df = Counter(tok for toks in self.docs.values() for tok in set(toks))
        self.idf = {t: math.log(n / c) for t, c in df.items()}
        self.vecs = {pid: self._tfidf(toks) for pid, toks in self.docs.items()}

    def _tfidf(self, toks):
        tf = Counter(toks)
        total = sum(tf.values()) or 1
        return {t: (c / total) * self.idf.get(t, math.log(len(self.docs)))
                for t, c in tf.items()}

    @staticmethod
    def _cosine(a, b):
        dot = sum(w * b.get(t, 0.0) for t, w in a.items())
        na = math.sqrt(sum(w * w for w in a.values()))
        nb = math.sqrt(sum(w * w for w in b.values()))
        return dot / (na * nb) if na and nb else 0.0

    def recommend(self, student, user_text, k=5):
        user_vec = self._tfidf(tokenize(user_text))
        scored = []
        for p in self.programs:
            # GRE-cutoff analog: program admission bar <= student's academic score (S-2)
            if p["min_grade_pct"] > student["academic_pct"]:
                continue
            scored.append((self._cosine(user_vec, self.vecs[p["program_id"]]),
                           p["program_id"]))
        scored.sort(key=lambda t: (-t[0], t[1]))
        return [pid for _, pid in scored[:k]]
