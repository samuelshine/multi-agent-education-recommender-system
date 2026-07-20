#!/bin/bash
# Wait for the H1 full-mode batch (PID 86362), then run the single-prompt condition.
while kill -0 86362 2>/dev/null; do sleep 30; done
cd "$(dirname "$0")/.."
EVAL_IDS=$(python3 -c "
import json
ids=[s['student_id'] for s in json.load(open('datagen/out/students.json'))[:100]]
print(','.join(ids))")
python3 run_pipeline.py --students "$EVAL_IDS" --sessions 1 --all-revealed \
  --mode single_prompt --out runs_h1 --metrics
