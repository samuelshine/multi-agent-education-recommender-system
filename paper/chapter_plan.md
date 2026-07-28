# Chapter Plan + INSIGHT Collection (Plan Mode)

Living document produced by `academic-paper` plan mode (Socratic chapter-by-chapter
guidance). Updated incrementally as dialogue rounds complete — do not treat as finished
until every chapter below has a Chapter Summary and Step 3 (Argument Stress Test) has run.

## Plan Mode Configuration Record

| Parameter | Value |
|---|---|
| **Topic** | Agentic multi-agent LLM architecture for pre-admission, cross-institution higher-education decision support |
| **Existing Materials** | Literature matrix (30+ sources, `literature_matrix.md`), research design draft (RQs/H, `research_design.md`), full paper skeleton with 9 `\todo{}` markers (`main.tex`, compiles to `main.pdf`), 37-entry bibliography (`references.bib`) |
| **Structure Preference** | IEEE conference paper (already set in `main.tex`: Intro, Related Work, Architecture, Methodology, Evaluation Plan, Discussion, Conclusion) |
| **Operational Mode** | plan |
| **Handoff Source** | none (in-repo existing draft, not a deep-research handoff) |

**Source note:** materials above were confirmed by reading the repo directly, not by
re-asking the 3-question plan-mode intake — the intake's own "existing materials
inventory" principle is satisfied by direct inspection here.

## Step 0 — Research Readiness Check

Research foundation is **not** lacking; deep-research is not needed. Open items instead:

1. `research_design.md` explicitly flags: RQs/H1–H3 drafted but **never stress-tested
   against the author in Socratic dialogue** — this is the concrete task Step 1 and Step 3
   below exist to close.
2. Contribution claims (3, in `research_design.md` and `main.tex` §Introduction) have not
   passed Step 2.5 Contribution Sharpening.
3. Dataset decision (`main.tex` Methodology `\todo`) was narrowed in the prior session to
   three candidates but not committed.
4. 9 `\todo{}` markers remain in `main.tex`, all blocked on the prototype/evaluation not
   yet existing.

## Step 1 — Thesis Crystallization

*Status: Round 1 complete (2026-07-16); Round 2 in progress.*

### Round 1 answers (author's own words)

- **[INSIGHT: thesis_framing]** On the "scope difference vs. contribution" challenge:
  "This is aimed to improve the current system and a more optimised flow for the same.
  Building a comparison and developing on what is there currently is the aim."
- **[INSIGHT: claim_priority]** On worse-accuracy-but-better-explanations: "I would
  consider better explanations a betterment of the system."
- **[INSIGHT: intended_impact]** On what the reader should take away: "That this system
  can be implemented and used actively in the field and not just lay in the archives as a
  research paper."

### Tensions surfaced (Round 1 → Round 2 agenda)

1. **Novelty vs. improvement framing.** `main.tex` Introduction claims *first
   agentic-LLM system at a new decision scope* (novelty thesis); the author's Round 1
   answer frames the work as *optimising and building on existing systems* (improvement
   thesis). These demand different Related Work postures and different evaluation burdens.
   → Round 2 Q1.
2. **H1 accuracy commitment vs. author's actual priority.** H1 hard-commits to
   "comparable-or-better top-k accuracy," but the author would accept an accuracy loss if
   explanations improve. As written, H1 is falsifiable in a way the author doesn't
   actually care about — a self-set trap. → Round 2 Q2.
3. **Deployment ambition vs. 1-month paper scope.** "Used actively in the field" is an
   aspiration the paper itself cannot demonstrate; needs to be translated into something
   the paper *can* evidence (artifact release, reproducibility, pilot) or explicitly
   deferred to future work. → Round 2 Q3.

### Round 2 answers (author's own words, 2026-07-16)

- **[INSIGHT: thesis_choice]** "I want either of them. If one works, then drop the
  other. I would prefer a" — primary framing is **(a) the novelty thesis** (first agentic
  multi-agent LLM system at the pre-admission decision scope), with (b) the improvement
  thesis held as **explicit fallback** if the gap collapses under full-text verification
  of Cluster A/F papers.
- **[INSIGHT: accuracy_floor]** "No loss in accuracy." — H1's "comparable-or-better
  top-$k$ accuracy" stands as a **hard commitment**; the author accepts the
  falsifiability risk. (Note: this supersedes the Round 1 leaning that explanation gains
  alone would suffice.)
- **[INSIGHT: deployability_evidence]** "A released open-source artifact anyone can run."
  — Contribution 3 is now concrete: public repo, runnable by third parties, cited in the
  paper. Real-data pilot and field deployment stay in Future Work.

### Step 1 output — Sharpened thesis statement

> This paper claims the **first agentic multi-agent LLM architecture for pre-admission,
> cross-institution university/program decision support** (novelty-led), evidenced by
> (i) a verified literature gap, (ii) a five-agent prototype released as a runnable
> open-source artifact, and (iii) an evaluation showing **no loss in top-$k$ accuracy**
> against classical baselines alongside measurably better explanation quality,
> adaptivity, and cold-start robustness.
>
> **Contingency rule (author-set):** if full-text reading of Cluster A/F kills the gap
> claim, drop the novelty framing and re-lead as an improvement paper (b) — comparative
> evaluation then becomes the primary contribution and must carry the paper alone.
>
> **GAP VERIFIED — novelty thesis LOCKED (2026-07-16).** Author full-text verdict on
> Cluster F: `onlinecoursemaskg` recommends online courses to students; `advisingwise`
> advises already-enrolled students with a human in the loop; `agenticedurec` recommends
> in-program learning pathways — "none of them are pre-admission recommendations"
> (author's words). Contingency framing is now dormant. Source PDFs for most of the
> original survey are in `paper/sources/`.

**Consequences for existing docs:**
- H1 in `research_design.md` / `main.tex`: unchanged in substance ("comparable-or-better"
  = author's "no loss" floor) — now confirmed rather than provisional.
- Contribution 3: reword from "released as an artifact" to explicit open-source runnable
  release. Done in `research_design.md`; `main.tex` keeps its `\todo` (claim finalizes
  only when the artifact exists) but the wording inside it is updated.
- The full-text reading of Cluster A/F (already an open item) is now **load-bearing for
  the thesis choice itself**, not just Related Work hygiene — highest-priority task.
  *(Since completed for the decisive set — see GAP VERIFIED block above.)*

## Step 2 — Chapter-by-Chapter Negotiation

Chapters already have first-draft skeletons in `main.tex` (Introduction, Related Work,
Architecture); this session's job is to pressure-test those, not draft from zero.
Methodology/Results/Discussion/Conclusion remain thin (marked `\todo`) and need real
negotiation once the dataset decision lands.

### Methodology — Round 1 (2026-07-16)

**Accuracy floor revised (supersedes Step 1 "no loss"):**
- **[INSIGHT: accuracy_floor_v2]** "What if I include loss in accuracy upto 5%?" — H1
  becomes a **non-inferiority claim with a 5% margin**: accuracy may trail the classical
  baseline by at most 5%, and explanation/adaptivity/cold-start gains carry the
  contribution. Open (Round 2): 5 *percentage points absolute* vs. *5% relative*, and on
  which headline metric (NDCG@k vs. precision@k) — must be pinned before any experiment
  runs, or it looks post-hoc.

**Dataset decision:**
- **[INSIGHT: dataset_strategy]** "let's do b and can we do a synthesized dataset?...
  remind me for the mail" — **dual-dataset design**: (b) Elahi et al. university-ratings
  data as the primary H1 accuracy benchmark (request email drafted at
  `elahi_data_request_email.md`; reminder memory saved); synthetic constraint-preference
  dataset (seeded from the public 20k career CSV) as the **only** testbed for H2
  (conflicting constraints) and H3 (cold-start/sessions), since Elahi's data has no
  constraint fields or session structure. Mentor assessment: synthetic is ~2–3 days of
  work and mandatory for H2/H3, not optional. Fallback if Elahi never replies: synthetic
  carries H1 too, with the "self-graded exam" limitation stated openly.

**Baselines:**
- **[INSIGHT: baseline_fidelity]** "To evaluate it, we should do the implementation as
  it was." — Faithful re-implementation of HRSPCA (2012) and StudieMe (2019), not
  library proxies. Risk flagged for Round 2: 2012/2019 papers likely underspecify
  hyperparameters/preprocessing; need a documented-deviation rule and a timeline cap.

**LLM / artifact runtime:**
- **[INSIGHT: llm_runtime]** "i want to run it on ollama now, but upto the user to run
  on anything and bring your own API key" — development + paper experiments on **Ollama
  (local open-weights)**; released artifact is **provider-agnostic** (BYO API key or
  local model). Open (Round 2): pin the exact model name/size for reproducibility;
  confirm hardware can sustain evaluation sweeps.

### Methodology — Round 2 answers (author's own words, 2026-07-16)

- **[INSIGHT: margin_definition]** "5% NDCG relative, Use NDCG if that is a better
  metric." — **5% relative non-inferiority margin on NDCG@$k$** as the headline metric
  (mentor confirms NDCG@$k$ is the right headline: it is rank-sensitive, standard for
  top-$k$ recommendation, and already named in RQ1); precision@$k$/recall@$k$ reported
  as secondary metrics.
- **[INSIGHT: reconstruction_rule]** "Log everything in the appendix table, i wont
  exceed one month" — every underspecified detail in the HRSPCA/StudieMe
  re-implementations gets a best-faith choice **logged in an appendix reconstruction
  table**; the one-month deadline is the hard cap. (Note: author declined a *weekly*
  sub-cap on baseline work — risk accepted; if baselines eat week 2, the mentor will
  re-raise the library-proxy fallback.)
- **[INSIGHT: model_pin]** "I can run gemma4:e4b" — paper experiments pinned to the
  Gemma e4b-class model on Ollama. **Verify the exact Ollama tag** (`ollama list`) —
  the e4b suffix matches Gemma's effective-4B naming; the paper must cite the exact
  tag + version. **Capability risk flagged:** a ~4B-effective model powering five
  agents is the single biggest technical risk to H1's explanation-quality claim —
  run a half-day spike (one full pipeline pass on 5 sample students) before building
  everything on it. Artifact stays provider-agnostic, so readers can run larger models.

### Methodology — Chapter Summary (converged 2026-07-16, 2 rounds)

| Element | Decision |
|---|---|
| Datasets | Dual: Elahi ratings (H1 accuracy, request pending) + synthetic seeded from public 20k career CSV (H2/H3; H1 fallback with stated limitation) |
| Baselines | Faithful re-implementation of HRSPCA + StudieMe + single-prompt-LLM ablation; deviations logged in appendix table |
| Headline metric | NDCG@$k$, 5% **relative** non-inferiority margin; precision@$k$/recall@$k$ secondary |
| Runtime | Ollama, Gemma e4b-class (exact tag TBV); artifact provider-agnostic (BYO key / local) |
| Accepted risks | Elahi non-response; no weekly cap on baseline work; small-model capability (mitigate via spike test first) |

## Chapter word-budget allocation (IEEE conference, ~6–8 pp)

| Chapter | Budget | Status |
|---|---|---|
| Introduction | ~0.75 p | Drafted, aligned with thesis (a) |
| Related Work | ~1.5 p (incl. table) | Drafted; gap verified full-text for Cluster F + `hrspca`/`studieme` (2026-07-16); peripheral Cluster A abstract-verified, stated openly in Discussion |
| Architecture | ~1.25 p (incl. figure) | Drafted |
| Methodology | ~1 p | Decisions locked this session; prose next |
| Evaluation/Results | ~1.5 p | Blocked on prototype |
| Discussion & Limitations | ~0.5 p | Blocked on results |
| Conclusion | ~0.25 p | Blocked on results |

| Chapter | Draft status | Plan-mode status |
|---|---|---|
| Introduction | Full draft in `main.tex` | Not yet stress-tested |
| Literature Review / Related Work | Full draft + positioning table | Not yet stress-tested |
| Architecture | Full draft + figure | Not yet stress-tested |
| Methodology | Skeleton only, dataset `\todo` | Not started |
| Evaluation Plan | Skeleton only | Not started |
| Discussion | Skeleton only | Not started |
| Conclusion | Skeleton only | Not started |

## Step 2.5 — Contribution Sharpening

*Complete (2026-07-16).* Model pin also finalized this round: **`gemma4:e4b`** confirmed
as the primary experiment model; **`gemma4:12b`** available on the author's hardware as
an option (mentor suggestion, author to decide: running both would give a cheap
model-scale ablation and a stronger H1 defense — if e4b explanations are weak, 12b may
carry the headline numbers).

- **[INSIGHT: contribution_claim]** (author's own words, verbatim): "They could know
  whether the system that I built is better than any system before, and how I went about
  building the system, the architecture, the workflow, the process, the agents and how
  they interact with each other and also see the better explainability of the system.
  Anyone can run the OpenSource artifact to learn and utilise the project to see how it
  works."

Three contribution components identifiable in the author's statement: (1) a comparative
verdict ("whether the system... is better"), (2) a transparent build record
(architecture, workflow, agent interactions), (3) a runnable open-source artifact.
**Tension carried into Step 3:** "better than any system *before*" claims more than the
evaluation design can support (two re-implemented classical baselines + one
single-prompt ablation, on one small real dataset + one synthetic). → Step 3 Q1.

## Step 3 — Argument Stress Test

*Complete (2026-07-16, 1 round).*

### Answers (author's own words)

- **[INSIGHT: claim_scope]** "Let it come in those topics when successful." — Claims in
  the paper stay scoped to the compared baselines and measured dimensions; broader
  "better than what came before" language is deferred until the system proves itself
  beyond the paper. → Writing Rule WR1.
- **[INSIGHT: explanation_measurement]** "Better explainability and better system design
  to give more tailored outputs. Use LLM-as-a-judge." — Explanation quality is measured
  via **LLM-as-judge**. Mentor constraint attached: the judge model must be a *different,
  stronger* model than `gemma4` (no self-judging), and LLM-as-judge validity goes into
  Limitations. → Writing Rule WR2.
- **[INSIGHT: ablation_stance]** "It is an open bet. But I know for a fact that agents
  will work better as in my experience, breaking down a task always yields better
  results." — The agents-vs-single-prompt ablation is acknowledged as a genuine open
  question; the author holds a prior (decomposition wins) but the paper must present the
  ablation as a test, not a foregone conclusion. If the ablation shows no gain, the
  novelty thesis + released artifact still carry the paper. → Writing Rule WR3.

### Writing rules for Phase 4 (drafting) — binding

- **WR1 (claim scope):** every superiority claim names its comparators and dimensions;
  no "better than existing/any systems" phrasing anywhere, including abstract and
  conclusion.
- **WR2 (judge independence):** LLM-as-judge uses a judge model ≠ experiment model;
  judge model, prompt/rubric (clarity, groundedness-in-retrieved-evidence, usefulness),
  and validity limitation are all reported.
- **WR3 (honest ablation):** the single-prompt baseline is framed as a genuine test of
  the architecture; the paper pre-states what each outcome would mean.

## PLAN MODE OUTPUT — Final Chapter Plan & Action Plan (2026-07-16)

Planning is complete: thesis chosen (novelty-led, fallback documented), H1 pinned (5%
relative NDCG@k non-inferiority), dual-dataset design, faithful baselines with appendix
reconstruction table, `gemma4:e4b` (+optional `12b` ablation), LLM-as-judge, three
binding writing rules. Remaining `\todo` markers in `main.tex` are all blocked on
execution, not on decisions.

### Week-by-week (deadline ~2026-08-11)

| Week | Focus | Concrete outputs |
|---|---|---|
| **1** (Jul 16–22) | De-risk | ~~Send Elahi email~~ SENT 07-16; ~~`gemma4:e4b` spike~~ DONE 07-16, verdict GO (`implementation/spike/SPIKE_REPORT.md`); ~~full-text read Cluster F~~ DONE (author, by 07-18 — all three confirmed in-program/enrolled-only; GAP VERIFIED, see Step 1 verdict); ~~start synthetic-dataset generator~~ v1 DONE 07-16 (`implementation/datagen/`, 300 students / 200 programs / 60k qrels, validated) |
| **2** (Jul 23–29) | Build | ~~5-agent prototype~~ scaffold DONE EARLY 07-16 (`implementation/agentrec/`, smoke test passed: 2 students end-to-end, 0 fallbacks, NDCG@5 0.88 wiring verified — real headline numbers await full batches); multi-session memory test PASSED 07-16 (3 students × 3 sessions, 0 fallbacks: budget-drift override enforced, vague-goal convergence 3→0 uncertainty notes, disliked programs never resurfaced; simulated-user feedback added to CLI); ~~HRSPCA + StudieMe re-implementations~~ DONE 07-16 from full texts in `paper/sources/` (`implementation/baselines/` + `RECONSTRUCTION.md`, 13 logged reconstruction choices). **Baseline numbers on the synthetic eval split (100 students): HRSPCA NDCG@5 = 0.793, StudieMe = 0.673.** H1 bar is now concrete: the agentic pipeline must score ≥ 0.753 NDCG@5 (0.95 × HRSPCA) at full information. Gap honesty notes upgraded to full-text-verified in `literature_matrix.md` + `main.tex` Discussion |
| **3** (Jul 30–Aug 5) | Evaluate | STARTED EARLY 07-16: H1 batch running (100 students, full mode, full-information state — `runs_h1/`); remaining: single_prompt / no_memory / single_objective batches, H3 session batches, judging. **Judge decision (07-16): primary `qwen2.5:14b` (Qwen family), agreement judge `mistral-nemo:12b` (Mistral family) — cross-family vs. Gemma per self-preference-bias literature; blind, absolute rubric scoring (clarity/groundedness/usefulness 1–5); harness at `implementation/agentrec/eval/judge.py`; pull judge models only after eval batches (GPU contention)** |
| **4** (Aug 6–11) | Write & ship | Methodology/Results/Discussion/Conclusion prose; results-bearing abstract; resolve every remaining `\todo`; artifact README + license + release; citation check; internal review pass; venue formatting |

### H1 RESULTS (2026-07-18) — pre-registered accuracy criterion NOT met

Completed runs, 100-student eval split, full information: five-agent NDCG@5 **0.706**
(bar was 0.753; HRSPCA 0.793) — **11% relative shortfall, outside the margin.**
Single-prompt baseline **0.830** beats everything → the WR3 reversal scenario
materialized on accuracy. Diagnostics: the gap is a **list-length effect** — Reflection
abstains rather than pads (70% of shortlists < 5, mean 3.9); at emitted length the
five-agent rank quality is 0.827 ≈ single-prompt 0.830, precision 0.904 ≈ 0.912, both
≫ classical. Written into `main.tex` Results verbatim per pre-commitment: verdict
stands, list-length diagnostic reported as metric-design finding, no post-hoc metric
swap. Architecture's remaining case rests on: explanation quality (judges pending),
H2 conflict subset, H3 cold-start (batches running). Author decision (2026-07-18): **ship documented v2, report both versions.**
v2 implemented same day (`--v2` flag; reflection drops only hard violations +
deterministic backfill to k; v1 untouched); single-student validation passed (5-item
list, no backfill needed — prompts alone fixed length); v2 paragraph added to
`main.tex` Results with pending-numbers todo; v2 batch chained after H2/H3.

### Batch status (2026-07-18, after Ollama outage)

The 07-18 morning chain died mid-H3 when the Ollama server went down (connection
refused, ~ST0014); its `ALL_H2_H3_DONE` line is spurious — the script had no error
handling. Verified state at 13:00: **H2 single_objective complete (56/56 conflict
students)**; H3 full 42/90; H3 no_memory 1/90; v2 H1 batch not started (waiter watched
a dead PID). Relaunched as `runs_h1/chain_resume.sh` (health-checked, 3-attempt retry
per stage, resumes from existing records): H3 full remainder → H3 no_memory → v2 full
batch. Expected wall time ~10–13 h at ~200 s/record.

### FULL RESULTS IN (2026-07-19/20) — all eval batches complete

Overnight chain finished (`ALL_STAGES_DONE`). Computed via `implementation/analyze_results.py`
(reproducible from run records):

- **H1/v2:** v2 NDCG@5 **0.806** (list 4.76) — **clears the 0.753 bar**, exceeds
  HRSPCA (0.793); P@5 0.898 ≈ v1's 0.904; abstention diagnosis causally confirmed.
  Single-prompt still leads on NDCG@5 (0.830): no architectural accuracy advantage,
  either policy. Written into `main.tex` Results.
- **H2 (56-student conflict subset): NOT SUPPORTED on accuracy — final (2026-07-20).**
  v1 policy: multi 0.666 < single 0.718 (abstention-coupled). Matched v2 policy: multi
  0.792 vs single **0.793 — tie**. Verdict written into `main.tex` with the diagnosis
  (oracle already encodes all objectives; prefiltered single-objective ranking recovers
  the signal). H2's remaining case rides on judged explanation quality (trade-off
  naming on conflict cases).
- **H3:** s1 identical by construction (0.583 both); memory wins s2 (+0.041) and s3
  (+0.019), stabilizes recall (no-memory decays 0.126→0.090; full holds). Supported
  in direction, modest at n=30; reframed honestly as *adaptivity* gain in `main.tex`.
- **Judging: COMPLETE (2026-07-20) — H1's explanation claim is SUPPORTED, decisively.**
  Cross-judge (qwen2.5:14b + mistral-nemo:12b) mean scores, n=100:
  groundedness 4.92 (v1) / 4.92 (v2) vs **3.96 single-prompt**; usefulness 3.65/3.60
  vs **2.80**; clarity 4.11/4.06 vs 3.69. Corroborated by invented-claims counts:
  single-prompt flagged in 64/100 (qwen) and 33/100 (mistral) explanations vs 5-9/100
  for the five-agent conditions. Inter-judge agreement far tighter on five-agent
  (0.09-0.15 groundedness) than single-prompt (1.26) — judges disagree most exactly
  where single-prompt is hardest to verify. **This is the paper's central empirical
  result**: architecture loses on raw NDCG@5, wins decisively on the explainability
  claim that WR1/WR2 pre-committed to measuring. H2 conflict-subset check confirms the
  gap holds unchanged on the 56 financially-constrained students — H2's contribution
  survives qualitatively even though it failed on oracle-graded ranking. All numbers
  verified via `implementation/analyze_judge.py`, written into `main.tex` Results.
- **Methodology + Baselines prose written** (Datasets / Baselines subsections);
  appendix skeleton added for the reconstruction table.

### FOUR WRITING TASKS DONE (2026-07-20) — down to 3 real todos

Abstract rewritten (results-bearing: explainability-wins/accuracy-ties framing),
7→5 merge todo resolved (H3 fused-mechanism result stands in for the ablation),
conclusion rewritten (findings-bearing, 3 concrete future-work items), appendix
reconstruction table ported in full (13 rows, both baselines). Funding statement
resolved: no external funding, MCA curriculum work at CHRIST (Deemed to be
University), Bengaluru — author-confirmed. Paper builds clean, 8 pages.

### ARTIFACT PUBLIC (2026-07-21) — repo prep closed out

Repo confirmed public at `github.com/samuelshine/multi-agent-education-recommender-system`.
Caught and fixed: GitHub's default branch was still `main` (near-empty — 1 file, the
original commit), so a visitor would have seen nothing; changed default branch to
`dev` (`gh repo edit --default-branch dev`) so the real content (paper, prototype,
license, run-record evidence) is what people actually land on.

Contribution 3 and the Data Availability Statement `\todo`s resolved with the real
URL; Data Availability also states plainly that the Elahi dataset was never obtained
and results use synthetic data only (matches memory: no reply as of 2026-07-21).
`\usepackage{url}` added to the preamble (was missing, broke the build once `\url{}`
was used).

**Remaining `\todo`s (2, both intentionally open, not blocked):**
1. Contribution 3's older wording is fully resolved — no longer a todo.
2. AI-Assisted Writing Disclosure — venue-specific wording; author said keep
   general for now (no target venue chosen yet), open by choice.
3. (line 15 is the `\todo{}` macro's own comment, not a real task.)

Paper is functionally submission-ready pending only a target-venue choice.

### Standing risks (accepted or mitigated)

1. Elahi non-response → synthetic carries H1 with stated limitation (fallback written
   into `main.tex`). *Update 2026-07-16: request email SENT; follow up ~Jul 23.*
2. ~~`gemma4:e4b` too weak for 5-agent reasoning~~ **RETIRED 2026-07-16** — week-1
   spike ran (25 calls, 5 profiles): 0 parse failures, 0 hallucinated KB ids, 0 budget
   violations, grounded explanations; verdict GO
   (`implementation/spike/SPIKE_REPORT.md`). Narrowed to three prototype-design items:
   lenient admission-plausibility checks, loose reflection-revision semantics, and
   evaluation-scale throughput (~2.5 min/student → plan overnight batches).
3. ~~Gap collapses under full-text reading~~ **RETIRED** — author full-text read of all
   three Cluster F systems confirms none address pre-admission choice; contingency
   framing dormant. *Residual soft spot:* `multidmensionalrecsysuni` (closest classical
   scope match, 2024) is still abstract-verified only and its PDF is not in
   `paper/sources/` — a reviewer pointing there is the last realistic gap attack;
   worth a full-text skim before submission.
4. Baseline re-implementation overruns → no weekly cap set (author's choice); mentor
   re-raises library-proxy fallback if it eats week 2.
5. Ablation shows agents ≤ single prompt → WR3 pre-commits honest reporting; paper
   survives on novelty + artifact.

## INSIGHT Collection

*(populated as dialogue produces user-articulated answers — quotes user's own words only)*

## Post-draft editorial pass (2026-07-21) — diagram, paragraph, and structure audit

User request: verify the architecture diagram against the implementation, verify every
paragraph, remove all "one-month timeline" references, and check IEEE structural
conventions. Findings and fixes, all applied to `main.tex` and rebuilt clean (8 pages,
0 errors, 0 undefined refs):

**Diagram bug (the reported page-3 layout issue).** The old `tikzpicture` let node
widths auto-expand to fit unwrapped text; the Recommendation \& Planning Agent box grew
wide enough that `right=16mm of recplan` pushed the Memory \& Reflection Agent box past
`\columnwidth`, overlapping "IV. RESEARCH DESIGN" in the right column — this is almost
certainly what read as "some agents aren't mentioned" (the box wasn't missing, it was
visually clipped/overlapped). Fixed by redesigning as a single vertical chain with an
explicit `text width` on every node (fixed width can't silently overflow again) and a
dashed cross-session feedback arrow from Memory \& Reflection back to Profiling,
looping left within the column. Re-rendered and visually confirmed: no overlap, all 5
agents clearly labeled.

**Diagram/text did not match implementation (verified by reading `agentrec/*.py`
directly):**
- The diagram and prose showed Recommend feeding Explain directly, with Memory \&
  Reflection off to the side. `pipeline.py` actually runs Recommend $\to$ Reflect
  $\to$ Explain in sequence — reflection happens *before* explanation, not beside it.
  Fixed: diagram and paragraph order now match `pipeline.py`'s real sequence.
- "Retrieval Agent... retrieval-augmented generation... against an education-specific
  knowledge base" — no embeddings, vector store, or external-corpus query exist
  anywhere in the code (`grep` for embed/vector/faiss/chroma/RAG returned nothing
  outside prose). The real mechanism: a deterministic keyword-scored prefilter (code,
  200$\to$20 programs) then an LLM selects from that in-context list. Fixed: paragraph
  now describes this accurately; dropped "RAG" from the diagram label.
- "Profiling \& Constraint Agent... elicits... through structured dialogue" — `pipeline.py`
  calls profiling once per session on a single rendered message (`simulate.py`); no
  multi-turn clarifying-question loop exists. Continuity is cross-session memory
  injection, a different mechanism. Fixed: paragraph now says single-turn extraction
  per session, continuity via persisted memory.
- The deterministic hard-constraint prefilter and post-reflection guard
  (`agentrec/README.md` "Safety guards" — confirmed real, already documented there)
  were never mentioned in the Architecture section at all, even though they are what
  actually guarantees budget/location/admission constraints are never violated, not
  agent judgment. Added a paragraph naming both explicitly.

**Numeric/internal-consistency errors, caught by re-running `analyze_results.py` /
`analyze_judge.py` fresh against the committed run records and cross-checking every
sentence against the output:**
- Abstract said explanations were "grounded... in 91–95%" for the five-agent system,
  but that quietly dropped the agreement judge's 0/100-invented-claims score (100%
  grounded) for both v1 and v2 — an inconsistent range next to the single-prompt
  figure (36–67%), which *did* span both judges. Fixed to "91–100%".
- Abstract said v2 "matches classical baselines" — v2's NDCG@5 (0.806) actually
  *exceeds* both HRSPCA (0.793) and StudieMe (0.673), and the Results section itself
  already says "exceeding." Fixed abstract wording to match.
- Evaluation Plan's Conditions paragraph claimed H3 feedback "react[s] to what each
  system actually recommended in the prior session" — false. Read
  `datagen/generate.py::gen_sessions`: liked/disliked programs come from the oracle's
  fixed per-student utility ranking, computed once at dataset-generation time,
  identical across every condition. This directly contradicted the Discussion
  section's own (correct) "simulated-user feedback derived from the oracle." Fixed the
  Evaluation Plan sentence to match reality and the Discussion section.
- Table II bolded *two different* NDCG@5 values in the same column (HRSPCA 0.793 and
  single-prompt 0.830) — a confusing double-max signal. Removed the bold from
  HRSPCA's cell; only the true column maximum (single-prompt) is now bold.
- Introduction still said Sections IV/V guide "experiments currently under
  development" — stale now that Results (Section VI) is fully populated. Fixed.
- Verified (not just trusted) against the artifact: the "4 validated-fallback events
  across 500 agent calls" table caption, the `gemma4:e4b` tag, and the 100-eval/200-
  historical HRSPCA split all matched the actual run records and code exactly — no
  drift found there.

**"One-month timeline" removal.** Two occurrences in `main.tex`: the 7$\to$5 merge
justification (Architecture section) reworded to "buildability within a single-author
prototype's scope"; the LLM-as-judge limitation (Discussion) reworded to drop "within
this paper's timeline" entirely. (Historical mentions in this file and
`research_design.md` are process/planning records, not the manuscript — left as-is
unless the author wants those scrubbed too.)

**IEEE structural fixes.**
- `\appendix` block was living at the very end, after Acknowledgment / Data
  Availability / Author Contributions / COI / AI-Disclosure. Canonical IEEEtran order
  (per the class's own `bare_conf.tex` template) is Conclusion $\to$ Appendix $\to$
  Acknowledgment $\to$ References. Moved the appendix block to directly follow the
  Conclusion.
- The move exposed a redundant heading: `\appendix` auto-prints "APPENDIX" as a label,
  and the section was titled `\section*{Appendix: Baseline Reconstruction Table}`,
  rendering as a doubled "APPENDIX / APPENDIX: BASELINE RECONSTRUCTION TABLE." Retitled
  to just "Baseline Reconstruction Table" so the auto-generated label isn't duplicated.
- Confirmed section numbering (I–VIII), keyword placement, figure/table caption
  conventions (IEEEtran auto-formats these correctly, no manual issue), and citation
  order are all IEEE-conformant; no further structural issues found.

Not touched: `paper/sources/` (correctly gitignored, never public), the 2 remaining
`\todo`s (AI-disclosure wording — open by author's explicit choice pending a venue
decision), `research_design.md`/this file's own historical "one-month" mentions.

## Mentor-feedback revision pass (2026-07-21)

Six items from the author's mentor, all applied to `main.tex`, rebuilt clean (9 pages,
0 errors, 0 undefined refs — grew from 8 pages due to added content, expected):

1. **Metrics justification.** Evaluation Plan's "Metrics" paragraph expanded: NDCG@5
   chosen over precision/recall because it is rank-sensitive and consumes the oracle's
   0--3 graded relevance directly (precision/recall collapse this to a binary cutoff);
   $k=5$ justified as matching both the classical baselines' own output length and a
   plausible student-facing shortlist size; precision/recall kept as secondary because
   they're what prior classical-RS papers report and readers will look for first.
2. **Fig. 1 caption shortened.** Was a full explanatory paragraph (arrow meanings,
   memory persistence, deterministic filter mention) — cut to one sentence. Safe to
   cut because every fact it stated is already in the body paragraphs immediately
   below the figure (checked line-by-line before cutting, nothing lost).
3. **"D. Positioning" heading removed** from Related Work. Interpreted narrowly: only
   the subsection heading was removed; the gap-summary paragraph and Table I stayed as
   trailing unlabeled content of Section II (the user said remove the heading, not the
   table — flagged this interpretation in case it needs revisiting).
4. **& 6. Float placement fixed.** Added `\usepackage{placeins}` +
   `\FloatBarrier` after Related Work, after Architecture, after H1's accuracy
   subsection, and after the Explanation-quality subsection. This is what separated
   Table I from Fig. 1 (previously crowded together) and pins Table II/III to their
   own subsections instead of drifting. Table I and Fig. 1 now land in different
   columns of the same page (Related Work ends / Architecture begins on the same
   physical page) rather than genuinely different pages — flagged as the interpretation
   taken; a hard page break is available if the mentor wants literal page separation,
   but isn't standard IEEE practice and would waste column space.
5. **Table unification (the biggest item).** Table II (accuracy) went from 4 rows to
   5: added the "Five-agent v2 (revised)" row (previously v2 only existed in prose,
   never in the table). Table III (explanation quality) went from 3 rows to 5: added
   HRSPCA/StudieMe rows marked "---" with a footnote explaining they're non-generative
   ranking pipelines with no natural-language output to score (confirmed via
   `grep -n explanation baselines/*.py` → zero hits, so "N/A" is accurate, not a
   dodge). Terminology unified across both tables: "HRSPCA (re-impl.)", "StudieMe
   (re-impl.)", "Single-prompt baseline" (was inconsistently "Single-prompt LLM
   baseline" in one table), "Five-agent v1 (pre-registered)", "Five-agent v2
   (revised)" — identical labels in both tables now. Bolding convention also made
   consistent: true column maximum bolded in every performance-metric column in both
   tables (previously R@5 was never bolded even when single-prompt had the max, and
   Table III's Clarity column was never bolded even though v1 had the max) — both
   tables now state this rule in their caption. Version-change footnote added directly
   under Table II (v1 vs. v2 definition) and cross-referenced from Table III's
   footnote, satisfying "explain the changes done between versions" without bloating
   either caption (kept in line with item 2's short-caption preference).

Two intentional interpretation calls flagged above (item 3 scope, item 6 same-page-
different-column vs. literal different pages) — surface these to the author before
next commit in case either needs adjusting.

## FloatBarrier reverted (2026-07-21) — author caught a real regression

The item-4/6 `\FloatBarrier` fix from the mentor-feedback pass caused exactly the
trade-off flagged at the time: on page 2, Table I couldn't fit at the top of either
column (both already held running text), and because `\FloatBarrier` refuses to let
*any* later content pass until the float resolves, the entire remainder of the page 2
right column went blank and Table I got pushed to page 3 — a large, non-continuous
gap. Author caught this and asked for strictly continuous text, strict IEEEtran
template adherence.

**Fix: removed all 4 `\FloatBarrier`s and the `placeins` package entirely.**
`\FloatBarrier`/`placeins` were never part of the standard IEEEtran conference
template to begin with, so removing them is itself a move toward stricter template
compliance, not away from it. Reverted to default LaTeX float placement (bare `[t]`
positioning, already in place). Rebuilt at 8 pages (down from 9 — confirms the barrier
was the direct cause of the extra page). Every one of the 8 pages re-rendered and
visually inspected end to end: zero blank gaps anywhere, including the last page
(both columns run close to the bottom, satisfying IEEE's own last-page-balance
guidance for free). Table I and Fig. 1 land sequentially in the same column on page 3
under default placement — not the separate-column layout the barrier produced, but
also not literally crowded/overlapping (that was the pre-existing diagram-overflow
bug, already fixed independently in an earlier pass) — clean and standard-looking.

**Lesson for future edits:** default LaTeX float placement is the safer choice for
IEEE two-column camera-ready output. Forcing placement (via `\FloatBarrier`, `[H]`,
etc.) trades gap-free flow for placement precision, and IEEE conference papers
generally prize the former. Prefer default behavior unless a float is visibly
drifting to a clearly wrong section.

## Self-review pass + grounded single-prompt ablation (2026-07-27)

Ran a full simulated peer-review panel (EIC + 3 reviewers + Devil's Advocate) against
the paper as it stood after the FloatBarrier revert. Findings, ranked, and what was
done about each:

1. **No statistical test behind two "statistically indistinguishable" claims**
   (H1 emitted-length NDCG vs. single-prompt; H2 conflict-subset v2 multi- vs.
   single-objective). Fixed: added a paired-bootstrap-CI section to
   `analyze_results.py` (10,000 resamples, `paired_bootstrap_ci()` +
   `ndcg_at_own_length()`), part of the released, deterministic, reproducible
   artifact. Both CIs cross zero, confirming the original claims — now with numbers
   attached (main.tex: H1 diagnostics paragraph, H2 subsection).
2. **Explanation-quality gap confounded architecture with instruction wording** —
   the single-prompt baseline was never given the Explanation Agent's explicit
   grounding directive, so the groundedness/usefulness advantage could have been
   pure prompting, not architecture. This was the review's highest-value finding.
   **Built a fourth condition, `single_prompt_grounded`** (`agentrec/prompts.py`:
   `SINGLE_PROMPT_GROUNDED`; `agentrec/pipeline.py`: new mode sharing the
   single-prompt code path), ran it on the full 100-student H1 eval split
   (`runs_h1/chain_single_prompt_grounded.sh`, zero fallbacks), judged it with both
   qwen2.5:14b and mistral-nemo:12b. Result: clarity 3.81, groundedness 4.47,
   usefulness 3.23 — squarely between the ungrounded baseline (3.69/3.96/2.80) and
   five-agent v1 (4.11/4.92/3.65), closing ~53% of the groundedness gap, ~51% of
   usefulness, only ~29% of clarity, at no cost to NDCG@5/precision@5. Added as a
   new row to Table II and Table III, a new "Isolating architecture from
   instruction" paragraph in Results, and a qualifying sentence in the Conclusion
   and Abstract — the paper's causal story is now "half prompting, half
   architecture" rather than an unexamined architecture-only claim.
3. **Citation-accuracy bug found via deep verification, not just abstract-skim**:
   `main.tex` twice claimed `llmagentrecsyssurvey` (Peng et al.) "explicitly
   identifies limited higher-education application as an open direction." Fetched
   and read the full 7-page arXiv PDF (2502.10050) — no mention of education
   anywhere, including its own named Future Directions (architecture, evaluation
   standardization, security). **This was a real, load-bearing misattribution**,
   not a peripheral one (it backed Introduction contribution #2). Fixed both
   occurrences to instead cite the survey's *silence* on education as evidence of
   the gap, without claiming the survey says so itself. Also live-verified
   `taurecbenchmark`, `advisingwise`, `agenticedurec`, `onlinecoursemaskg`,
   `bertopicprogramrec` via arXiv/Crossref/Semantic Scholar — all confirmed real
   and accurately characterized. Logged in `literature_matrix.md`'s honesty-note
   section (second verification pass).
4. **Fig. 1 omitted the two deterministic prefilter/guard components** that the
   prose calls "the mechanism that actually guarantees hard-constraint
   satisfaction." Added both as small dashed gray boxes inline in the pipeline
   chain (`gate` TikZ style, same 50mm text width as the agent boxes to avoid
   reopening the earlier width-overflow bug) — visually distinct from the solid
   agent boxes, verified render at 150dpi shows no overflow or overlap.
5. **H3's "67 have a session-3 budget-revision event (H3 conditions)" reads as
   describing the H3 evaluation cohort but doesn't** — H3's reported results use a
   fixed 30-student subsample (first 30 in eval order), of which only 5 actually
   carry that event; the 67-count is a dataset-wide stress-test subset for future
   analysis. Confirmed via direct inspection of `sessions.json` events. Reworded
   both the Datasets paragraph and the H3 Results opening sentence to make this
   explicit.
6. **"Pre-registered" was asserted narratively with no external anchor.** Added a
   footnote to H1's first "pre-registered" mention citing the actual commit hashes:
   `9b47ce4` (2026-07-17, evaluation design committed, results section still had
   agentic rows pending) before `ba7757e` (2026-07-20, results computed and
   written up) — both verifiable in the repo's public git history.

Rebuilt after every change; visually re-inspected all 9 pages via pymupdf render
each time. Paper grew 8→9 pages (footnote + new table row + new paragraphs), no
overflow, no gaps, continuous flow preserved throughout.

**Not done / left as-is:** the review also flagged that `Data Availability
Statement`/`Author Contributions`/`Conflict of Interest` sections are
Frontiers/journal conventions rather than standard IEEE-conference boilerplate —
deferred until the target venue's CFP is known (same open item as the AI-disclosure
`\todo{}`).

## Re-review pass (2026-07-28) — closing the gap the ablation itself left open

Ran the reviewer skill again against the paper post-ablation. Every finding from the
2026-07-27 pass verified as correctly resolved. The re-review's own top finding was
about internal consistency: the newly-added grounded-ablation gap-closure percentages
(53%/51%/29%) were themselves unsupported point estimates — the exact category of
claim the prior pass had just fixed elsewhere in the paper. Applying the paper's own
new standard to its newest content:

1. **Added a paired-bootstrap decomposition to `analyze_judge.py`**
   (`paired_bootstrap_ci()` + `cross_judge_scores()`), splitting the full
   ungrounded→five-agent-v1 gap into an "instruction effect" (grounded − ungrounded)
   and residual "architecture effect" (v1 − grounded) per dimension, each with a 95%
   CI over the same 100 students. All six intervals exclude zero — both effects are
   real, not noise. Updated numbers: groundedness 53%/47% split
   ($+0.515$ CI $[+0.320,+0.705]$ / $+0.450$ CI $[+0.305,+0.600]$), usefulness
   50%/50%, clarity 29%/71%. Replaced the old point-estimate sentence in Results with
   this CI-backed version.
2. **Fixed "roughly halves" for the invented-claims counts** (main.tex explanation
   quality subsection) — 64→42 is a third fewer, 33→6 is over four-fifths fewer;
   neither is "roughly half." Reworded to state both precisely.
3. **Added a caveat that the grounded ablation isn't perfectly isolated by design**:
   the single-prompt conditions produce ranking and explanation in the same LLM call,
   so an instruction-wording change could in principle leak into ranking too. Noted
   this explicitly and pointed to the near-identical NDCG@5 (0.830 vs. 0.831) as the
   empirical check that it didn't, rather than asserting isolation as a given.
4. **Fixed a circular cross-reference**: Table II's footnote pointed to
   `Section~\ref{sec:results}` from inside a table already in that section. Now names
   the specific subsection ("Section VI, Explanation quality").
5. Not done (flagged as very low priority, tangential to H2's actual question):
   running the grounded condition on the H2 conflict subset. H2 is about
   multi-vs-single-objective reasoning, not grounding instructions, so this is a
   completeness nicety rather than a substantive gap.

Rebuilt, checked log for overfull boxes/undefined refs (none), rendered and visually
inspected pages 5–7 (the changed ones). Still 9 pages, continuous flow preserved.
