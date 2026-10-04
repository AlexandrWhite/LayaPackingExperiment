import re 

class GreedDecision:
    def __init__(self):
        pass

    def predict(self, state, questions):
        #current_weight = re.findall(r"\d+",questions["solve"]["instructions"])[0]


        if state["pile_1_weight"] < state["pile_2_weight"]:
            choice_pile = "pile_1"
        else:
            choice_pile = "pile_2"
        

        pile1_prob = 0.99 if choice_pile == "pile_1" else 0.01
        pile2_prob = 0.99 if choice_pile == "pile_2" else 0.01

        res = { 'model': 'random-model', 
                'answers': {'solve': 
                    {
                      'type': 'choice', 
                      'choice': choice_pile, 
                      'probabilities': {'pile_1': pile1_prob, 'pile_2': pile2_prob}, 
                      'confidence': 1.0, 
                      'answer_confidence': 1.0, 
                      'action': {'act_probability': 1.0}}},
                      'usage': {'input_tokens': 0, 'output_tokens': 0}
                    }

        return res 
        
# row = {"split": "test", "state": {"remaining_stones": [10], "pile_1_stones": [], "pile_2_stones": [3, 4, 1], "pile_1_weight": 0, "pile_2_weight": 8, "difference": 8, "task": "Distribute all the remaining stones so that the weight difference between the two piles is minimal."}, "question": {"solve": {"instructions": "Which pile should the stone with a weight of 10 be placed in?", "criteria": {"pile_1": "Put it in pile_1. pile_1 weight will be 10, pile_2 weight will be 8, difference will be 2.", "pile_2": "Put it in pile_2. pile_1 weight will be 0, pile_2 weight will be 18, difference will be 18."}, "type": "choice"}}, "gold": {"solve": {"label": "pile_1", "probabilities": {"pile_1": 1, "pile_2": 0}}}}

# gd = GreedDecision()
# print(gd.predict(row["state"], row["question"]))