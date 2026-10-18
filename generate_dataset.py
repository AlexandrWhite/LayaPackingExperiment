import random
import subprocess
import json
import os 
from pathlib import Path 
from copy import deepcopy
import numpy as np 
from copy import deepcopy



DS_FOLDER = "dataset"

TRAIN_EXAMPLES = 1000
TEST_EXAMPLES = 500

random.seed(0)

def generate_cases(example, split):
    #split variable with possible values "train", "test", "val"
    #example  = {"diff": 3, "ans": [0, 1, 0, 1, 0], "stones": [5, 8, 13, 27, 14]}

    ans = example["ans"]
    stones = example["stones"]
    piles = [[], []]

    records = []

    for i,stone in enumerate(stones):
        state = {
            "remaining_stones": list(stones[i:]),
            "pile_1_stones": piles[0],
            "pile_2_stones": piles[1],
            "pile_1_weight": sum(piles[0]),
            "pile_2_weight": sum(piles[1]),
            "difference": abs(sum(piles[0]) - sum(piles[1])),
            "task": ("Distribute all the remaining stones so that the "
                        "weight difference between the two piles is minimal.")
        }

        def describe(heap1, heap2, stone, target_pile):
            if target_pile == 0:
                w1, w2 = sum(heap1) + stone, sum(heap2)
            else:
                w1, w2 = sum(heap1), sum(heap2) + stone
            return (
                f"Put it in pile_{target_pile+1}. "
                f"pile_1 weight will be {w1}, pile_2 weight will be {w2}, "
                f"difference will be {abs(w1 - w2)}."
            )

        question = {
            "solve": {
                "instructions": f"Which pile should the stone with a weight of {stone} be placed in?",
                "criteria": {
                    "pile_1": describe(piles[0], piles[1], stone, 0),
                    "pile_2": describe(piles[0], piles[1], stone, 1),
                },
                "type": "choice",
            }
        }

        gold = {
            "solve": {
                "label": "pile_1" if ans[i] == 0 else "pile_2",
                "probabilities": {
                    "pile_1": 1.0 if ans[i] == 0 else 0.0,
                    "pile_2": 1.0 if ans[i] == 1 else 0.0,
                },
            }
        }

        record = {
            "split" : split,
            "state": deepcopy(state),
            "question": deepcopy(question),
            "gold": deepcopy(gold),
        }

        
        records.append(record)
        piles[ans[i]].append(stone)

    return records


def generate_example(n):
    stones = [random.randint(1, 10) for i in range(n)]
    input_data = ' '.join(map(str, [n]+stones))

    result = subprocess.run(
        ['./grounded_truth'], 
        input=input_data, 
        capture_output=True, 
        text=True
    )
    example = json.loads(result.stdout)
    #example  = {"diff": 3, "ans": [0, 1, 0, 1, 0], "stones": [5, 8, 13, 27, 14]}
    return example


def generate(n, split):
    example = generate_example(n)
    mirror_example = deepcopy(example)

    for i, p_bit in enumerate(mirror_example["ans"]):
        if p_bit == 0:
            mirror_example["ans"][i] = 1
        else:
            mirror_example["ans"][i] = 0

    cases = generate_cases(example, split)
    mirror_cases = generate_cases(mirror_example, split)

    for case in mirror_cases:
        cases.append(case)
    
    return cases 


def even_odds(cases):
    gold_cnt = np.array([0, 0])
    labels = ["pile_1", "pile_2"]

    #we want sample with equal golden for pile 1 and pile
    for case in cases:
        if case["gold"]["solve"]["label"] == "pile_1":
            gold_cnt[0] += 1
        elif case["gold"]["solve"]["label"] == "pile_2":
            gold_cnt[1] += 1
    
    skip_numbers = gold_cnt - np.min(gold_cnt)
    
    for case in cases:
        pile = case["gold"]["solve"]["label"]
        pile_idx = labels.index(pile)

        if skip_numbers[pile_idx] > 0:
            skip_numbers[pile_idx] -= 1
            continue
        yield case 


os.makedirs(DS_FOLDER, exist_ok=True)


with open(Path(DS_FOLDER)/"train.json", "w", encoding="utf-8") as out:
    cases = []
    for _ in range(TRAIN_EXAMPLES):
        n = random.randint(1,20)
        case = generate(n, "train")
        for row in case:
            cases.append(row)

    for case in even_odds(cases):
        out.write(json.dumps(case, ensure_ascii=False) + "\n")
    


with open(Path(DS_FOLDER)/"test.json", "w", encoding="utf-8") as out:
    cases = []
    for _ in range(TEST_EXAMPLES):
        n = random.randint(1,20)
        case = generate(n, "test")
        for row in case:
            cases.append(row)

    for case in even_odds(cases):
        out.write(json.dumps(case, ensure_ascii=False) + "\n")
        
