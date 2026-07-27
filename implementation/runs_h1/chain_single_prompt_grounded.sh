#!/bin/bash
# Review-requested ablation (2026-07-27): grounded single-prompt condition,
# isolating architecture from instruction wording. Same 100-student
# full-information eval split as the other H1 conditions.
cd "$(dirname "$0")/.."

wait_ollama() {
  for i in $(seq 1 60); do
    curl -s --max-time 3 http://localhost:11434/api/tags >/dev/null && return 0
    echo "[chain] ollama down, waiting ($i/60)..."; sleep 30
  done
  echo "[chain] FATAL: ollama unreachable for 30 min"; exit 1
}

run_stage() {
  local name="$1"; shift
  for attempt in 1 2 3; do
    wait_ollama
    echo "[chain] stage=$name attempt=$attempt $(date '+%H:%M:%S')"
    if python3 "$@"; then echo "[chain] stage=$name OK"; return 0; fi
    echo "[chain] stage=$name attempt=$attempt FAILED"
  done
  echo "[chain] FATAL: stage=$name failed 3 attempts"; exit 1
}

EVAL_IDS=$(python3 -c "
import json
ids=[s['student_id'] for s in json.load(open('datagen/out/students.json'))[:100]]
print(','.join(ids))")

run_stage single_prompt_grounded run_pipeline.py --students "$EVAL_IDS" --sessions 1 \
  --all-revealed --mode single_prompt_grounded --out runs_h1 --metrics

for judge in qwen2.5:14b mistral-nemo:12b; do
  tag=single_prompt_grounded_$(echo "$judge" | tr ':.' '__')
  run_stage "judge_${tag}" -m agentrec.eval.judge --runs runs_h1/single_prompt_grounded \
    --judge "$judge"
done
echo "ALL_GROUNDED_ABLATION_DONE"
