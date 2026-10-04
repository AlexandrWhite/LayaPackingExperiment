from laya import Router
import json 
import random 
import subprocess

random.seed(42)

router = Router(models={
    "english": "laya_finetuned_stone_packing"
})  

router = Router()

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


def test():
    example = generate_example(10)
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




    for stone in stones:
        question = {
            "action": {
                "instructions": f"Which pile should the stone with a weight of {stone} be placed in?",
                "criteria": {
                    "pile_1": describe(heap1, heap2, stone, target_pile=1),
                    "pile_2": describe(heap1, heap2, stone, target_pile=2),
                },
                "type": "choice"
            }
        }

        result = router.predict(state, question)
        model_decision = result["answers"]["action"]["choice"]

        if model_decision == "pile_1":
            heap1.append(stone)
        else:
            heap2.append(stone)

        state = {
            "remaining_stones": stones,
            "pile_1_stones": heap1,
            "pile_2_stones": heap2,
            "pile_1_weight": sum(heap1),
            "pile_2_weight": sum(heap2),
            "current_diff": sum(heap2)-sum(heap1),
            "task": "Distribute all the remaining stones so that the weight difference between the two piles is minimal." 
        }

    # print(f"Pile 1: {heap1}")
    # print(f"Pile 2: {heap2}")
    # print(f"Difference:", abs(sum(heap1) - sum(heap2)))
    # print(f"Minimal Difference {example['diff']}")

    model_result = abs(sum(heap1) - sum(heap2))
    grounded_truth_result = example['diff']
    sq_err = (model_result-grounded_truth_result)**2
    return sq_err

TESTS = 100

err = 0
for i in range(TESTS):
    err += test()/TESTS
print(err)
