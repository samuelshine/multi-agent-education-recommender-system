# Literature Matrix

Working reference for the paper's Related Work section and gap argument. Not for
submission — condensed into a table in `main.tex`. Citation keys refer to
`references.bib`.

## Cluster A — Classical educational/university recommenders (target user: prospective student, pre-admission)

| Key | Year | Method | Target user | Decision scope | Evaluation | Limitation |
|---|---|---|---|---|---|---|
| `hrspca` | 2012 | Hybrid CF + knowledge-based | Prospective student | Single-institution admission prediction | Prediction accuracy | Static, no dialogue/adaptivity, single institution |
| `studieme` | 2019 | Content-based (TF-IDF, cosine similarity) | Prospective student | College choice | Similarity/precision | No reasoning, no explainability, no career/financial integration |
| `universityadmissionrecommendersystem` | n/d | Classical ML | Secondary school students | Admission recommendation | Not specified | Predates LLM/agentic methods entirely |
| `smartcollegeadmrecommendationsys` | 2025 | ML classification | Prospective student | College admission | Accuracy | Recent but still single-model, non-agentic, no explainability |
| `userprofilinguniversityrecsys` | 2016 | Info retrieval-based profiling | Prospective student | University choice | Not specified | Profiling only, no planning/multi-objective reasoning |
| `contentbasedrecsys` | 2020 | Content-based filtering | Prospective student | University choice | Precision/recall | No adaptivity, no dialogue |
| `multidmensionalrecsysuni` | 2024 | Multidimensional rec (rule/ML) | Prospective student | University **and major** selection | User evaluation study | **Closest classical match to our decision scope** — but no agentic reasoning, memory, or explainability layer |
| `companalysisrecsys` | 2022 | Comparative study of CF/CB/hybrid | Prospective student | University major & career guidance | Comparative accuracy | Confirms fragmentation of methods; no unified adaptive framework |
| `recommendersyshighered` | 2024 | Systematic review | Prospective/enrolled | Academic choice (broad) | N/A (review) | Explicitly documents the static-pipeline / weak-explainability gap this proposal targets |
| `serendipityuniversitycourserecsys` | 2020 | RNN / course2vec / BOW | **Enrolled** student | In-program course choice | Online user study (N=70) | Different decision scope (post-enrollment) |
| `recommendationsyscomplexconstraints` | 2011 | Constraint-based | **Enrolled** student | In-program course sequencing | System deployment (CourseRank) | Different decision scope (post-enrollment) |
| `universityrecsyselahi` | 2022 | CF (SVD, KNN variants), 7 algorithms compared | Prospective student | Cross-institution university choice | Offline RMSE (5-fold CV) + online user study (N=52): accuracy, diversity, perceived personalization, satisfaction, novelty, SUS | Pre-agentic CF; small rating sample (1,515 ratings / 80 users / 551 universities); **dataset available on request from authors; its two-phase offline+online evaluation protocol is a direct model for our Evaluation Plan** |
| `bertopicprogramrec` | 2025 | BERTopic topic modeling over course descriptions | Prospective student | Academic program selection | Qualitative study (N=65): satisfaction (98%), adoption intent (94%), coverage, personalization score | Recent but still single-model NLP, non-agentic, no multi-objective constraints, institutional dataset (80 programs / 5,000+ courses) not public |
| `careerrecfeatureselection` | 2025 | ML classification (RF best) + RF feature selection | Undergraduate student | **Career path** (33 IT job labels), not university choice | Accuracy / precision / recall / F1 (RF: 0.90 / 0.95 / 0.91 / 0.93) | Career scope adjacent to ours (career-goal dimension only); non-agentic; **uses a public 20,000-record dataset (GitHub, see Datasets section)** |

## Cluster B — General recommender system foundations (method background, not domain-specific)

| Key | Year | Contribution |
|---|---|---|
| `recommendationsys` | 2015 | CF/CB/hybrid principles and evaluation — foundational reference |
| `recommendationsysml` | 2020 | ML approaches to recommendation |
| `mlalgorithmsrecommendersys` | 2015 | Systematic review of ML algorithms in RS |
| `frameworkintrecommendersys` | 2017 | General intelligent RS framework (Fuzzy Cognitive Maps) |
| `knowledgebasedrecsys` | 2014 | Knowledge-based RS foundations |
| `contextawarerecsys` | 2017 | Context-aware RS review |

## Cluster C — Conversational recommenders (interaction paradigm background)

| Key | Year | Contribution |
|---|---|---|
| `convrecommendersys` | 2018 | Original conversational RS formulation |
| `advcrs` | 2021 | Survey of advances/challenges in CRS |

## Cluster D — Agentic AI foundations (non-recommendation-specific)

| Key | Year | Contribution |
|---|---|---|
| `agenticaiarchitectures` | 2025 | Agentic AI architectures, protocols, design challenges |
| `agenticaisurvey` | 2025 | Comprehensive survey of agentic AI (planning, autonomy, governance) — general, not RS-specific |

## Cluster E — Agentic / multi-agent / LLM-agent recommenders (general domain — e-commerce, content, retrieval)

| Key | Year | Method | Domain | Limitation relative to our target |
|---|---|---|---|---|
| `agenticaiframeworkrecommendersystem` | 2024 | Agentic multi-agent framework | E-commerce | **Nearly identical title to this project's original framing** — but general-domain, not education; no educational features, datasets, or evaluation metrics |
| `multiagentrecommendersys` | 2025 | Multi-agentic design patterns (industrial tutorial) | E-commerce | Tutorial/survey, not an education application |
| `llmagentrecsyssurvey` | 2025 | Survey: recommender-oriented / interaction-oriented / simulation-oriented agentic paradigms | General | Confirms (with evidence) limited higher-education application — supports our stated Domain 2 limitation directly |
| `taurecbenchmark` | 2026 | Verifiable benchmark for agentic RS | General (5 model families tested) | No education-specific benchmark exists — opportunity for a secondary (evaluation) contribution |
| `ragpersonalisedrecommendations` | 2025 | RAG + transformer personalization | E-commerce | Same architecture family (retrieval + generation), different domain |
| `llmexplanationforrecommendersys` | 2024 | LLM-generated post-hoc explanations | General | Explainability layer only, not full agentic pipeline |

## Cluster F — Agentic / multi-agent systems specifically applied to education (2025-2026) — **the decisive competitor set**

| Key | Year/Venue | Target user | Decision scope | Architecture | Why it is close but NOT our gap |
|---|---|---|---|---|---|
| `advisingwise` | 2025, arXiv (cs.HC) | **Enrolled** CS grad students | Advising Q&A within an already-declared program | 3-phase: query processing, ReAct retrieval, human-in-loop response gen | Assumes program is already fixed; answers questions, does not recommend which university/program to choose; human-in-loop drafting, not autonomous planning |
| `agenticedurec` | 2026, WSDM Companion | **Enrolled** learners (6,000+ users, deployed) | In-program learning-pathway sequencing | 18+ agents, 4-tier hierarchy (perception/domain/coordination/strategy) | Post-enrollment curriculum adaptation, not pre-admission institution/program choice |
| `onlinecoursemaskg` | 2025, AI4Ed Symposium | **Enrolled** students | In-curriculum course selection | Profiling agent + KG retrieval agent + recommendation agent | Architecture shape nearly identical to a naive first-draft of our design — but scoped to course-level, not institution/program-level, and no multi-objective (career/financial/location/employability) reasoning |

## Cluster G — Education-RS reviews and pre-LLM multi-agent lineage (supporting background)

Added 2026-07-15 from author-supplied URLs. None of these threaten the gap; the two MAS
papers matter for Related Work honesty — "multi-agent" educational recommenders predate
LLMs, so the paper's novelty claim must rest on *agentic LLM* architecture + decision
scope, not on the phrase "multi-agent" alone.

| Key | Year | Type | Contribution / relevance |
|---|---|---|---|
| `humancapacitybuildingmas` | 2008 | Empirical MAS system | Cooperative-agent CF recommender for professional course selection (pre-LLM). Earliest multi-agent educational-RS precedent in the corpus; survey-collected data, not public; reports 90% ranking accuracy |
| `adaptivemaselearning` | 2020 | 4-page survey | Reviews adaptive multi-agent e-learning recommenders (pre-LLM); no dataset, no metrics |
| `recsyseducationreview` | 2021 | Systematic review (98 papers) | Education-RS landscape 2015–2020: CF/CB/hybrid dominate, ML rising; complements `recommendersyshighered` |
| `slreducationalrecsys` | 2023 | Systematic review (16 papers) | Documents **scarcity of public educational datasets** (only 1 of 16 studies used one) and that pedagogical-effectiveness evaluation appears in only 37.5% of studies — citable support for both our dataset problem and the evaluation-framework gap |

## Candidate datasets & evaluation resources (from Cluster A additions, checked 2026-07-15)

| Source | What it is | Availability | Fit |
|---|---|---|---|
| `careerrecfeatureselection` → Dataset A | 20,000 records × 35 features, 33 IT-career class labels (academic scores, IQ, coding skill, interests, personality, workshops, certifications) | **Public**: `github.com/KLGLUG/student-career-area-prediction-using-machine-learning` (`Project Code/roo_data.csv`, ~4.9 MB, licensed; repo verified live 2026-07-15) | Student-features → career-label supervision. Covers the **career-goal dimension only** — no university/program/financial/location data. Usable to (a) ground the Profiling Agent's career inference, (b) seed synthetic student profiles for the planned synthetic dataset |
| `universityrecsyselahi` rating data | 1,515 ratings, 80 users, 551 universities + metadata for 12,003 crawled universities | On request from authors ("without undue reservation") | The only known **university-choice** preference dataset. Small, but directly the right decision scope; worth emailing authors early given the 1-month timeline |
| `universityrecsyselahi` protocol | Two-phase evaluation: offline 5-fold CV (RMSE) then online user study (accuracy, diversity, perceived personalization, satisfaction, novelty, SUS) | Published method | Template for our Evaluation Plan's standard-metrics + user-study split |
| `careerrecfeatureselection` metrics | Accuracy / precision / recall / F1 baselines from 6 ML classifiers (RF best: 0.90/0.95/0.91/0.93) | Published numbers on the public dataset | Ready-made classical-ML baseline numbers if we evaluate the career dimension on Dataset A |

## The gap this paper targets

Every paper in Cluster F that combines agentic/multi-agent LLM methods with education
targets an **already-enrolled** student inside an **already-chosen** institution/program
(advising, pathway sequencing, course selection). Every paper in Cluster A that targets
the **pre-admission, cross-institution** decision (which university, which program) uses
**pre-agentic** methods (CF/CB/KB/ML classification) with static pipelines, weak
explainability, and no long-term memory or multi-objective planning across career goals,
financial constraints, location, and employability outcomes simultaneously.

**No paper in the corpus occupies the intersection**: agentic multi-agent LLM architecture
× pre-admission cross-institution university/program decision support. This is the gap
statement the Introduction and Related Work build toward. A live web search for this exact
intersection (2026-07-11) surfaced only vendor marketing content (admissions-funnel SaaS
copy), not peer-reviewed work — see session notes.

**Honesty note on scope of this check** *(updated 2026-07-16)*: this matrix was
originally built from abstracts and metadata (fetched live, not fabricated) plus the
author's own prior reading. Full-text verification status:

- **Cluster F — VERIFIED (author full-text read, 2026-07-16):** `onlinecoursemaskg`
  recommends online courses; `advisingwise` advises already-enrolled students with a
  human in the loop; `agenticedurec` recommends in-program learning pathways. None
  extends to pre-admission recommendation. The gap claim stands.
- **Cluster A (partial) — `hrspca` and `studieme` VERIFIED (full-text read during
  baseline re-implementation, 2026-07-16):** HRSPCA is a rule-based cascade
  (knowledge-discovery rules + historical predictor) with a web-form portal; StudieMe
  is TF-IDF/cosine over resume text with a GRE-cutoff filter. Neither has agentic,
  dialogue, memory, or LLM elements. Source PDFs for most of the survey are now in
  `paper/sources/`.
- Remaining Cluster A entries are still abstract-verified only; they are supporting
  citations, not the gap's load-bearing edge.
