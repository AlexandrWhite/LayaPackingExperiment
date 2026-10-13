import json 
import random 
import subprocess

import numpy as np
import pandas as pd 

from laya import Router
from random_agent import RandomDecision
from greed_agent import GreedDecision 
from spam_agent import SpamDecision


TESTS = 100
MAX_WEIGHT = 20
N_STONES = 15

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
        print(f"Pile 1: {heap1}")
        print(f"Pile 2: {heap2}")
        print(f"Difference:", abs(sum(heap1) - sum(heap2)))
        print(f"Minimal Difference {example['diff']}")
        print(f"Correct Answer {example['ans']}")

    model_result = abs(sum(heap1) - sum(heap2))
    grounded_truth_result = example['diff']
    err = abs(model_result-grounded_truth_result)

    return err


def check_model(model, examples):
    errors = []
    for example in examples:
        errors.append(run_example(model, example))
    return errors
        

 
stones = [6,5,4,3,2,1]
example = generate_example(stones)

run_example(model = Router(models={"english": "laya_finetuned_stone_packing-20k"}), example=example, verbose = True)
quit()
examples = [generate_example(n=N_STONES) for i in range(TESTS)]

errors_random = np.array(check_model(RandomDecision(), examples))
errors_greed = np.array(check_model(GreedDecision(), examples))
# errors_spam_pile_1 = np.array(check_model(SpamDecision(spam_option="pile_1"), examples))
# errors_spam_pile_2 = np.array(check_model(SpamDecision(spam_option="pile_2"), examples))
# errors_laya_orig = np.array(check_model(Router(), examples))
# errors_laya_fine_tuned = np.array(check_model(Router(models={"english": "laya_finetuned_stone_packing"}), examples))
errors_laya_fine_tuned_20k = np.array(check_model(Router(models={"english": "laya_finetuned_stone_packing-20k"}), examples))


result_greed = {"policy": "greed", "mean_absolute_diff": np.mean(errors_greed), "max_diff": np.max(errors_greed), "min_diff":np.min(errors_greed)}
# result_random = {"policy": "random", "mean_absolute_diff": np.mean(errors_random), "max_diff": np.max(errors_random), "min_diff":np.min(errors_random)}
# result_spam_1 = {"policy": "spam pile_1", "mean_absolute_diff": np.mean(errors_spam_pile_1), "max_diff": np.max(errors_spam_pile_1), "min_diff":np.min(errors_spam_pile_1)}
# result_spam_2 = {"policy": "spam pile_2", "mean_absolute_diff": np.mean(errors_spam_pile_2), "max_diff": np.max(errors_spam_pile_2), "min_diff":np.min(errors_spam_pile_2)}
# result_laya_orig = {"policy": "laya", "mean_absolute_diff": np.mean(errors_laya_orig), "max_diff": np.max(errors_laya_orig), "min_diff":np.min(errors_laya_orig)}
# result_laya_fine_tuned = {"policy": "laya fine_tuned", "mean_absolute_diff": np.mean(errors_laya_fine_tuned), "max_diff": np.max(errors_laya_fine_tuned), "min_diff":np.min(errors_laya_fine_tuned)}
result_laya_fine_tuned20k = {"policy": "laya fine_tuned_20k", "mean_absolute_diff": np.mean(errors_laya_fine_tuned_20k), "max_diff": np.max(errors_laya_fine_tuned_20k), "min_diff":np.min(errors_laya_fine_tuned_20k)}


comprassion_data = [result_greed, 
                    # result_random, 
                    # result_spam_1, 
                    # result_spam_2, 
                    # result_laya_orig, 
                    # result_laya_fine_tuned, 
                    result_laya_fine_tuned20k
                ]

df_comp = pd.DataFrame(comprassion_data)
print(f"=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones={N_STONES} on {TESTS} tests, weights [1, {MAX_WEIGHT}]) ===\n")
print(df_comp.to_markdown(index=False))
