#!/bin/bash
# Wait for the H2/H3 chain (PID 24401), then run the v2 full-mode H1 batch.
while kill -0 24401 2>/dev/null; do sleep 60; done
cd "$(dirname "$0")/.."
EVAL_IDS=$(python3 -c "
import json
ids=[s['student_id'] for s in json.load(open('datagen/out/students.json'))[:100]]
print(','.join(ids))")
python3 run_pipeline.py --students "$EVAL_IDS" --sessions 1 --all-revealed \
  --mode full --v2 --out runs_h1 --metrics
echo "V2_BATCH_DONE"
