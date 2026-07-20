#!/bin/bash
# Post-batch GPU queue (2026-07-19): unconfound H2, then judge explanations.
# Stage 1: single_objective under the v2 pruning policy (56 conflict students) so the
#          H2 comparison (multi- vs single-objective) holds pruning policy constant.
# Stages 2-7: LLM-as-judge over the three explanation-bearing systems x two judges
#          (qwen2.5:14b primary, mistral-nemo:12b agreement), blind, absolute rubric.
cd "$(dirname "$0")/.."

wait_ollama() {
  for i in $(seq 1 60); do
    curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null && return 0
    echo "[judge-chain] ollama down, waiting ($i/60)..."; sleep 30
  done
  echo "[judge-chain] FATAL: ollama unreachable"; exit 1
}

run_stage() {
  local name="$1"; shift
  for attempt in 1 2 3; do
    wait_ollama
    echo "[judge-chain] stage=$name attempt=$attempt $(date '+%H:%M:%S')"
    if python3 "$@"; then echo "[judge-chain] stage=$name OK"; return 0; fi
    echo "[judge-chain] stage=$name attempt=$attempt FAILED"
  done
  echo "[judge-chain] FATAL: stage=$name failed 3 attempts"; exit 1
}

CONFLICT_IDS=$(python3 -c "
import json
ss=[s for s in json.load(open('datagen/out/students.json'))[:100] if s['h2_conflict']]
print(','.join(s['student_id'] for s in ss))")

run_stage single_objective_v2 run_pipeline.py --students "$CONFLICT_IDS" --sessions 1 \
  --all-revealed --mode single_objective --v2 --out runs_h1 --metrics

for judge in qwen2.5:14b mistral-nemo:12b; do
  for dir in runs_h1/full runs_h1/full_v2 runs_h1/single_prompt; do
    tag=$(basename "$dir")_$(echo "$judge" | tr ':.' '__')
    run_stage "judge_${tag}" -m agentrec.eval.judge --runs "$dir" --judge "$judge"
  done
done
echo "ALL_JUDGE_STAGES_DONE"
