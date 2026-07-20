#!/bin/bash
# Resume chain after the 2026-07-18 Ollama outage killed chain_h2_h3.sh mid-H3.
# Stages: H3 full (resume 42/90) -> H3 no_memory (resume 1/90) -> v2 H1 batch (0/100).
# Each stage: wait for Ollama, then run with up to 3 attempts (records resume, so
# retries are cheap). Loud failure — no misleading DONE on error.
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

H3_IDS=$(python3 -c "
import json
print(','.join(s['student_id'] for s in json.load(open('datagen/out/students.json'))[:30]))")
EVAL_IDS=$(python3 -c "
import json
print(','.join(s['student_id'] for s in json.load(open('datagen/out/students.json'))[:100]))")

run_stage h3_full run_pipeline.py --students "$H3_IDS" --sessions 1,2,3 \
  --mode full --out runs_h3 --metrics
run_stage h3_no_memory run_pipeline.py --students "$H3_IDS" --sessions 1,2,3 \
  --mode no_memory --out runs_h3 --metrics
run_stage v2_full run_pipeline.py --students "$EVAL_IDS" --sessions 1 --all-revealed \
  --mode full --v2 --out runs_h1 --metrics
echo "ALL_STAGES_DONE"
