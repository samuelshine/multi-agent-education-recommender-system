#!/bin/bash
# H2: single_objective on the conflict subset (all-revealed), then
# H3: scripted sessions 1-3, full + no_memory, first 30 eval students.
cd "$(dirname "$0")/.."
CONFLICT_IDS=$(python3 -c "
import json
ss=[s for s in json.load(open('datagen/out/students.json'))[:100] if s['h2_conflict']]
print(','.join(s['student_id'] for s in ss))")
python3 run_pipeline.py --students "$CONFLICT_IDS" --sessions 1 --all-revealed \
  --mode single_objective --out runs_h1 --metrics
H3_IDS=$(python3 -c "
import json
print(','.join(s['student_id'] for s in json.load(open('datagen/out/students.json'))[:30]))")
python3 run_pipeline.py --students "$H3_IDS" --sessions 1,2,3 \
  --mode full --out runs_h3 --metrics
python3 run_pipeline.py --students "$H3_IDS" --sessions 1,2,3 \
  --mode no_memory --out runs_h3 --metrics
echo "ALL_H2_H3_DONE"
