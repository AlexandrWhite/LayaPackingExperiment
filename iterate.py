import random
import subprocess
from pprint import pprint 

def generate_cases(example):
    #example  = {"diff": 3, "ans": [0, 1, 0, 1, 0], "stones": [5, 8, 13, 27, 14]}

    ans = example["ans"]
    stones = example["stones"]
    piles = [[], []]


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
                "label": "pile_1",
                "probabilities": {
                    "pile_1": 1 if ans[i] == 0 else 0,
                    "pile_2": 1 if ans[i] == 1 else 0,
                },
            }
        }


        record = {
            "state": state,
            "question": question,
            "gold": gold,
        }

        pprint(record)
        print("----------------------------")

        piles[ans[i]].append(stone)

def generate_example(n):
    stones = [random.randint(1, 10) for i in range(n)]
    input_data = ' '.join(map(str, [n]+stones))

    result = subprocess.run(
        ['./grounded_truth'], 
        input=input_data, 
        capture_output=True, 
        text=True
    )
    print(result)

# generate_cases({"diff": 3, "ans": [0, 1, 0, 1, 0], "stones": [5, 8, 13, 27, 14]})
generate_example(4)

