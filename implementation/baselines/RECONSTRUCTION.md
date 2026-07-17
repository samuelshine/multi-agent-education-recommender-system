# Baseline Reconstruction Table

The paper commits to faithful re-implementation of HRSPCA (Ragab et al., ISDA 2012)
and StudieMe (Sharma et al., RDCAPE 2019), with every underspecified or
task-adaptation choice logged here (author decision 2026-07-16, `chapter_plan.md`
Methodology Round 1–2). This file becomes the paper's appendix reconstruction table.

Source texts: full PDFs in `../../paper/sources/`, read 2026-07-16. The HRSPCA PDF
carries a damaged font map (glyphs shifted by 29 code points); text was recovered by
deterministic decoding, but **digits and two figures (WRR formula table, pseudocode
figures) did not survive extraction** — entries H-5/H-7 below reconstruct those from
the surrounding prose.

## HRSPCA (hybrid knowledge-rules + historical predictor)

| # | Original (paper) | Our data lacks / underspecifies | Reconstruction choice |
|---|---|---|---|
| H-1 | Two cascaded recommenders + college predictor over KAU admission data | Different catalog (200 fictional cross-institution programs) | Cascade preserved: track filter → rule filter + WRR ranking, fused with historical-predictor votes |
| H-2 | Track Recommender sorts students into scientific/literary/affiliated tracks via weighted-degree rules (Table 2 group A) | Our students have no Saudi track structure | Track ≙ career-goal field cluster: programs pass the track stage iff their field matches the student's goal field or an adjacent field (same adjacency map as the dataset generator) |
| H-3 | College allocation requires passing all preparatory-year courses (R2-1) | No preparatory year | Rule dropped; nearest analog (meeting the program's admission bar) kept via H-4 |
| H-4 | Minimum prerequisite course scores per college (rules C–F, "B+ in English/Math/…") | Per-course grades absent from catalog and student records | Single-threshold analog: `academic_pct >= min_grade_pct` |
| H-5 | "Weighted Relative Rate" ranking (formula in Table 3 — image, unrecoverable; prose says weighted student score relative to college criteria) | Exact weights unknown | WRR = 0.5·min(grade/bar, 1.5)/1.5 + 0.5·(coding_skill/9) — weighted composite of relative academic rate and aptitude analog, mirroring the Saudi weighted-rate convention (GPA + aptitude, equal weights) |
| H-6 | College Predictor compares student with historical admitted-student GPA data | No historical admissions for fictional programs | k-NN (k=10) over a held-out training split of students; "historically suitable" = oracle grade ≥ 2 in the training split; votes weighted by similarity × grade |
| H-7 | College capacity rule (R2-3) constrains allocation | Catalog has no capacity field | Rule dropped (no analog); noted as fidelity loss |
| H-8 | Predictor and allocator fused informally ("with the help of") | Fusion weights unspecified | score = 0.5·WRR + 0.5·predictor votes (equal weights, stated) |

**Known fidelity losses:** capacity constraint (H-7) and per-course prerequisites
(H-4). Neither can be expressed in the evaluation catalog; both losses make the
baseline *stronger*, not weaker (fewer hard filters → more candidates to rank).

## StudieMe (content-based TF-IDF)

| # | Original (paper) | Our data lacks / underspecifies | Reconstruction choice |
|---|---|---|---|
| S-1 | User profile from LinkedIn + resume text | No resumes | User document = the same rendered full-profile message the agentic system receives (fair-input principle) |
| S-2 | Hard filter: college GRE cutoff ≤ user GRE (Function #1) | No GRE | Admission-bar analog: `min_grade_pct <= academic_pct` |
| S-3 | TF-IDF (sklearn TfidfVectorizer, NLTK stopwords/lemmatization) + cosine | Zero-dependency artifact constraint | TF-IDF + cosine implemented in stdlib; small English stopword list; no lemmatization (stated deviation) |
| S-4 | Second stage matches faculty profiles by publication count | No faculty analog in catalog | Stage omitted; noted as fidelity loss |
| S-5 | Returns top-20 then top-15 ranked colleges | Our evaluation uses k=5 | Return top-k (k=5) — cutoff change only, ranking method unchanged |

## Input-fairness note (for the paper's Methodology)

Both classical baselines receive the student's **complete** profile (classical systems
assume a filled application form — this is exactly their design). The agentic system
receives progressively disclosed sessions. H1 comparisons therefore use the
full-information state (session 3); H3 exploits the session structure, where
classical systems have no mechanism and re-run statelessly.
