import time, json
import numpy as np
import pandas as pd
from datasets import load_dataset
import laya
from laya.common import ece_score

print("Loading test split for evaluation...")
ds_test = load_dataset("LocalLLaMA/typed-decisions", "all", split="test")

agent_ft = laya.Agent(OUTPUT_DIR, device="cuda")

predictions = []
latencies_ms = []

print(f"Evaluating {len(ds_test)} test cases on GPU...")
t0_eval = time.time()

for i, row in enumerate(ds_test):
    case_id = row["id"]
    workflow = row["workflow"]
    state = json.loads(row["state"])
    questions = json.loads(row["questions"])
    gold = json.loads(row["gold"])
    
    t0 = time.perf_counter()
    res = agent_ft.predict(state, questions)
    dt_ms = (time.perf_counter() - t0) * 1000
    latencies_ms.append(dt_ms)
    
    predictions.append({
        "id": case_id,
        "workflow": workflow,
        "pred": res["answers"],
        "gold": gold,
        "questions": questions,
        "latency_ms": dt_ms
    })

print(f"Evaluated all {len(ds_test)} cases in {time.time() - t0_eval:.1f}s!")