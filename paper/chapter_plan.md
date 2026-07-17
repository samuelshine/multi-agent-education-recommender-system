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
| Related Work | ~1.5 p (incl. table) | Drafted; full-text Cluster A/F read pending (load-bearing) |
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
| **1** (Jul 16–22) | De-risk | ~~Send Elahi email~~ SENT 07-16; ~~`gemma4:e4b` spike~~ DONE 07-16, verdict GO (`implementation/spike/SPIKE_REPORT.md`); full-text read Cluster F (3 papers) then Cluster A closest matches — **in progress (author)**; ~~start synthetic-dataset generator~~ v1 DONE 07-16 (`implementation/datagen/`, 300 students / 200 programs / 60k qrels, validated) |
| **2** (Jul 23–29) | Build | ~~5-agent prototype~~ scaffold DONE EARLY 07-16 (`implementation/agentrec/`, smoke test passed: 2 students end-to-end, 0 fallbacks, NDCG@5 0.88 wiring verified — real headline numbers await full batches); multi-session memory test PASSED 07-16 (3 students × 3 sessions, 0 fallbacks: budget-drift override enforced, vague-goal convergence 3→0 uncertainty notes, disliked programs never resurfaced; simulated-user feedback added to CLI); ~~HRSPCA + StudieMe re-implementations~~ DONE 07-16 from full texts in `paper/sources/` (`implementation/baselines/` + `RECONSTRUCTION.md`, 13 logged reconstruction choices). **Baseline numbers on the synthetic eval split (100 students): HRSPCA NDCG@5 = 0.793, StudieMe = 0.673.** H1 bar is now concrete: the agentic pipeline must score ≥ 0.753 NDCG@5 (0.95 × HRSPCA) at full information. Gap honesty notes upgraded to full-text-verified in `literature_matrix.md` + `main.tex` Discussion |
| **3** (Jul 30–Aug 5) | Evaluate | STARTED EARLY 07-16: H1 batch running (100 students, full mode, full-information state — `runs_h1/`); remaining: single_prompt / no_memory / single_objective batches, H3 session batches, judging. **Judge decision (07-16): primary `qwen2.5:14b` (Qwen family), agreement judge `mistral-nemo:12b` (Mistral family) — cross-family vs. Gemma per self-preference-bias literature; blind, absolute rubric scoring (clarity/groundedness/usefulness 1–5); harness at `implementation/agentrec/eval/judge.py`; pull judge models only after eval batches (GPU contention)** |
| **4** (Aug 6–11) | Write & ship | Methodology/Results/Discussion/Conclusion prose; results-bearing abstract; resolve every remaining `\todo`; artifact README + license + release; citation check; internal review pass; venue formatting |

### Standing risks (accepted or mitigated)

1. Elahi non-response → synthetic carries H1 with stated limitation (fallback written
   into `main.tex`). *Update 2026-07-16: request email SENT; follow up ~Jul 23.*
2. ~~`gemma4:e4b` too weak for 5-agent reasoning~~ **RETIRED 2026-07-16** — week-1
   spike ran (25 calls, 5 profiles): 0 parse failures, 0 hallucinated KB ids, 0 budget
   violations, grounded explanations; verdict GO
   (`implementation/spike/SPIKE_REPORT.md`). Narrowed to three prototype-design items:
   lenient admission-plausibility checks, loose reflection-revision semantics, and
   evaluation-scale throughput (~2.5 min/student → plan overnight batches).
3. Gap collapses under full-text reading → thesis flips to improvement framing
   (contingency rule, Step 1).
4. Baseline re-implementation overruns → no weekly cap set (author's choice); mentor
   re-raises library-proxy fallback if it eats week 2.
5. Ablation shows agents ≤ single prompt → WR3 pre-commits honest reporting; paper
   survives on novelty + artifact.

## INSIGHT Collection

*(populated as dialogue produces user-articulated answers — quotes user's own words only)*
