import random
random.seed(42)

class RandomDecision:
    def __init__(self):
        pass

    def predict(self, state, questions):
        #current_weight = re.findall(r"\d+",questions["solve"]["instructions"])[0]

        choice_pile = random.choice(["pile_1", "pile_2"])
        
        pile1_prob = 0.99 if choice_pile == "pile_1" else 0.01
        pile2_prob = 0.99 if choice_pile == "pile_2" else 0.01

        res = { 'model': 'random-model', 
                'answers': {
                      'solve': {
                        'type': 'choice', 
                        'choice': choice_pile, 
                        'probabilities': {'pile_1': pile1_prob, 'pile_2': pile2_prob}, 
                        'confidence': 1.0, 
                        'answer_confidence': 1.0, 
                        'action': {'act_probability': 1.0}}
                      },
                      'usage': {'input_tokens': 0, 'output_tokens': 0}
            }

        return res 