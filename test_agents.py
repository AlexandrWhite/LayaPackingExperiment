import json 
import random 
import subprocess

import numpy as np
import pandas as pd 

from laya import Router
from random_agent import RandomDecision
from greed_agent import GreedDecision 
from spam_agent import SpamDecision

TESTS = 11
MAX_WEIGHT = 10
N_STONES = 10

random.seed(42)

def generate_example(stones):
    n = len(stones)
    input_data = ' '.join(map(str, [n]+stones))

    result = subprocess.run(
        ['./grounded_truth'], 
        input=input_data, 
        capture_output=True, 
        text=True
    )
    example = json.loads(result.stdout)
    return example


def describe(heap1, heap2, stone, target_pile):
    if target_pile == 1:
        w1, w2 = sum(heap1) + stone, sum(heap2)
    else:
        w1, w2 = sum(heap1), sum(heap2) + stone
    return (
        f"Put it in pile_{target_pile}. "
        f"pile_1 weight will be {w1}, pile_2 weight will be {w2}, "
        f"difference: {abs(w1 - w2)}."
    )


def run_example(model, example, verbose=False):
    stones = example["stones"]
    heap1 = []
    heap2 = []

    state = {
    "remaining_stones": stones,
    "pile_1_stones": heap1,
    "pile_2_stones": heap2,
    "pile_1_weight": sum(heap1),
    "pile_2_weight": sum(heap2),
    "current_diff": sum(heap2)-sum(heap1),
    "task": "Distribute all the remaining stones so that the weight difference between the two piles is minimal." 
    }

    for i, stone in enumerate(stones):
        # print(state)
        question = {
            "solve": {
                "instructions": f"Which pile should the stone with a weight of {stone} be placed in?",
                "criteria": {
                    "pile_1": describe(heap1, heap2, stone, target_pile=1),
                    "pile_2": describe(heap1, heap2, stone, target_pile=2),
                },
                "type": "choice"
            }
        }

        result = model.predict(state, question)
        model_decision = result["answers"]["solve"]["choice"]

        if model_decision == "pile_1":
            heap1.append(stone)
        else:
            heap2.append(stone)

        state = {
            "remaining_stones": stones[i+1:],
            "pile_1_stones": heap1,
            "pile_2_stones": heap2,
            "pile_1_weight": sum(heap1),
            "pile_2_weight": sum(heap2),
            "current_diff": abs(sum(heap2)-sum(heap1)),
            "task": "Distribute all the remaining stones so that the weight difference between the two piles is minimal." 
        }

    if verbose:
        print("----------------------------------")
        print(f"Pile 1 {heap1}")
        print(f"Pile 2 {heap2}")
        print(f"Diff", abs(sum(heap1) - sum(heap2)))
        print(f"Correct Diff {example['diff']}")
        print(f"Correct Answer {example['ans']}")
        print("----------------------------------")

    model_result = abs(sum(heap1) - sum(heap2))
    grounded_truth_result = example['diff']
    err = abs(model_result-grounded_truth_result)
    diff = model_result
    
    return err, diff


def show_progress(name, progress, total, width=40):
    ratio = progress / total if total else 0
    filled = int(width * ratio)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r [{bar}] ({progress}/{total}) running for {name}", end="", flush=True)


def check_model(model, policy_name, examples):
    errors = []
    diffs = []
    grounded_truth_difference = []

    for i, example in enumerate(examples):
        err, diff = run_example(model, example, verbose=False)
        errors.append(err)
        diffs.append(diff)
        grounded_truth_difference.append(example["diff"])
        show_progress(policy_name, i+1, TESTS)
    print()

    result_row = {
        "policy": policy_name, 
        "mean_absolute_error": np.mean(errors), 
        "max_error": np.max(errors), 
        "min_error":np.min(errors),
        "policy_mean_difference": np.mean(diffs),
        "grounded_truth_mean_difference": np.mean(grounded_truth_difference)
    }
    
    return result_row
        

 
# stones = [10,1]
# example = generate_example(stones)

# run_example(model = GreedDecision(), example=example, verbose = True)
# quit()

Router(models={"english": "laya_finetuned_stone_packing-20k"})

examples = []
for i in range(TESTS):
    inputs = sorted([random.randint(1, MAX_WEIGHT) for i in range(1, N_STONES)])
    examples.append(generate_example(inputs))

model_20k=Router(models={"english": "laya_finetuned_stone_packing-20k"})
model_600=Router(models={"english": "laya_finetuned_stone_packing"})

comprassion_data = [
    check_model(RandomDecision(), "random", examples),
    check_model(GreedDecision(), "greed", examples),
    check_model(model_20k, "model-20k", examples),
    check_model(model_600, "model-600", examples)
]

df_comp = pd.DataFrame(comprassion_data)
print(f"=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones={N_STONES} on {TESTS} tests, weights [1, {MAX_WEIGHT}]) ===\n")
print(df_comp.to_markdown(index=False))
