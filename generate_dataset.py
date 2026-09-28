import json

DATASET_PATH = "cases.jsonl"


def generate_cases(stone, stones, heap1, heap2, correct_pile, out_file):
    state = {
        "remaining_stones": list(stones),
        "pile_1_stones": list(heap1),
        "pile_2_stones": list(heap2),
        "pile_1_weight": sum(heap1),
        "pile_2_weight": sum(heap2),
        "current_diff": sum(heap2) - sum(heap1),
        "task": ("Distribute all the remaining stones so that the "
                 "weight difference between the two piles is minimal.")
    }

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

    question = {
        "action": {
            "instructions": f"Which pile should the stone with a weight of {stone} be placed in?",
            "criteria": {
                "pile_1": describe(heap1, heap2, stone, target_pile=1),
                "pile_2": describe(heap1, heap2, stone, target_pile=2),
            },
            "type": "choice",
        }
    }

    gold = {
        "action": {
            "label": "pile_{}",
            "probabilities": {
                "pile_1": 1 if ans[i] == 1 else 0,
                "pile_2": 1 if correct_pile == 2 else 0,
            },
        }
    }

    # Склеиваем всё в один record и пишем как одну JSONL-строку
    record = {
        "state": state,
        "question": question,
        "gold": gold,
    }
    out_file.write(json.dumps(record, ensure_ascii=False) + "\n")


with open("grounded.jsonl", "r") as f, open(DATASET_PATH, "w", encoding="utf-8") as out:
    for line in f.readlines()[:10]:
        data = json.loads(line)

        # важно: копия списка, иначе remove() ломает итерацию
        for stone in list(data["stones"]):
        
            pile_id = 1
            if stone in data["pile_1"]:
                pile = data["pile_1"]
            else:
                pile = data["pile_2"]
                pile_id = 2

            # --- удаляем камень ---
            pile.remove(stone)
            data["stones"].remove(stone)

            generate_cases(stone, data["stones"], data["pile_1"],
                           data["pile_2"], pile_id, out)

            # --- возвращаем камень обратно ---
            pile.append(stone)
            data["stones"].append(stone)