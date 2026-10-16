import time, json
import numpy as np
import pandas as pd
from datasets import load_dataset
import laya
from laya.common import ece_score
from huggingface_hub import snapshot_download
from datasets import get_dataset_split_names
from random_agent import RandomDecision
from greed_agent import GreedDecision
from spam_agent import SpamDecision 

ds_test = load_dataset("json", data_dir="dataset", split="test")

def evaluate_agent(agent_ft, model_name, kind, cost="0.00$ (self-hosted)"):
    predictions = []
    latencies_ms = []

    t0_eval = time.time()


    for i, row in enumerate(ds_test):
        state = row["state"]
        questions = row["question"]
        gold = row["gold"]

        t0 = time.perf_counter()
        res = agent_ft.predict(state, questions)
        
        dt_ms = (time.perf_counter() - t0) * 1000
        latencies_ms.append(dt_ms)

        predictions.append({
            "pred": res["answers"],
            "gold": gold,
            "questions": questions,
            "latency_ms": dt_ms
        })

    print(f"Evaluated all {len(ds_test)} cases in {time.time() - t0_eval:.1f}s!")

    accuracies = []
    soft_accuracies = []
    brier_scores = []
    kl_divs = []
    tv_distances = []
    score_maes = []
    within_one = []
    all_confs = []
    all_corrects = []

    for item in predictions:
        pred_answers = item["pred"]
        gold_answers = item["gold"]
        questions = item["questions"]
        
        for qid, qdef in questions.items():
            p_ans = pred_answers[qid]
            g_ans = gold_answers[qid]
            q_type = qdef["type"]
            
            # 1. Choice
            if q_type == "choice":
                keys = list(qdef["criteria"].keys())
                pred_choice = p_ans["choice"]
                gold_label = str(g_ans["label"])
                
                is_corr = float(pred_choice == gold_label)
                accuracies.append(is_corr)
                all_corrects.append(is_corr)
                
                p_probs = np.array([p_ans["probabilities"].get(k, 1e-6) for k in keys], dtype=float)
                g_probs = np.array([g_ans["probabilities"].get(k, 1e-6) for k in keys], dtype=float)
                p_probs /= p_probs.sum()
                g_probs /= g_probs.sum()
                
                all_confs.append(float(p_probs.max()))
                soft_accuracies.append(float((p_probs * g_probs).sum()))
                brier_scores.append(float(((p_probs - g_probs) ** 2).sum()))
                tv_distances.append(float(0.5 * np.abs(p_probs - g_probs).sum()))
                kl_divs.append(float((g_probs * np.log(np.clip(g_probs / p_probs, 1e-12, 1e4))).sum()))
                
            # 2. Noul
            elif q_type == "noul":
                p_val = p_ans["noul"]
                g_val = g_ans.get("noul", g_ans.get("probabilities", {}).get("true", 0.5))
                gold_label = str(g_ans["label"]).lower()
                
                pred_label = "true" if p_val >= 0.5 else "false"
                is_corr = float(pred_label == gold_label)
                accuracies.append(is_corr)
                all_corrects.append(is_corr)
                all_confs.append(float(max(p_val, 1.0 - p_val)))
                
                p_dist = np.array([1.0 - p_val, p_val])
                g_dist = np.array([1.0 - g_val, g_val])
                
                soft_accuracies.append(float((p_dist * g_dist).sum()))
                brier_scores.append(float(((p_dist - g_dist) ** 2).sum()))
                tv_distances.append(float(0.5 * np.abs(p_dist - g_dist).sum()))
                kl_divs.append(float((g_dist * np.log(np.clip(g_dist / p_dist, 1e-12, 1e4))).sum()))
                
            # 3. Score
            elif q_type == "score":
                p_score = p_ans["score"]
                g_score = g_ans.get("score", 0.0)
                score_maes.append(abs(p_score - g_score))
                within_one.append(float(abs(p_score - g_score) <= 1.0))
                
                # Use argmax of probabilities for discrete prediction
                n_levels = len(qdef.get("criteria", []))
                p_probs_score = np.array([p_ans["probabilities"].get(str(i), 0.0) for i in range(n_levels)])
                if p_probs_score.sum() > 0:
                    p_probs_score /= p_probs_score.sum()
                    p_lvl = int(np.argmax(p_probs_score))
                    all_confs.append(float(p_probs_score.max()))
                else:
                    p_lvl = int(round(p_score))
                    all_confs.append(0.5)
                    
                g_lvl = int(g_ans.get("label", int(round(g_score))))
                is_corr = float(p_lvl == g_lvl)
                accuracies.append(is_corr)
                all_corrects.append(is_corr)

    laya_acc = np.mean(accuracies)
    laya_soft_acc = np.mean(soft_accuracies)
    laya_brier = np.mean(brier_scores)
    laya_kl = np.mean(kl_divs)
    laya_tv = np.mean(tv_distances)
    laya_ece = ece_score(np.array(all_confs), np.array(all_corrects))
    laya_mae = np.mean(score_maes) if score_maes else 0.0
    laya_within1 = np.mean(within_one) if within_one else 0.0
    laya_latency = np.percentile(latencies_ms, 50)


    return {
        "Model": model_name,
        "Kind": kind,
        "Accuracy": round(laya_acc, 3),
        "Soft Acc": round(laya_soft_acc, 3),
        "Brier": round(laya_brier, 3),
        "ECE": round(laya_ece, 3),
        "Score MAE": round(laya_mae, 3),
        "ms/case": round(laya_latency, 1)
    }

comparison_data = []

agent_ft = laya.Agent("models/laya_finetuned_stone_packing",device="cuda")
laya_base_row = evaluate_agent(agent_ft, "Laya", "fine-tuned" , "0.00$ (self-hosted)")
comparison_data.append(laya_base_row)

agent_ft = laya.Agent("models/laya_finetuned_stone_packing-20k",device="cuda")
laya_fine20k_row = evaluate_agent(agent_ft, "Laya", "fine-tuned20k" , "0.00$ (self-hosted)")
comparison_data.append(laya_fine20k_row)


agent_ft = laya.Agent(device="cuda")
laya_base_row = evaluate_agent(agent_ft, "Laya", "without-training" , "0.00$ (self-hosted)")
comparison_data.append(laya_base_row)


random_agent = RandomDecision()
random_row = evaluate_agent(random_agent, "Random", "rule")
comparison_data.append(random_row)

greed_agent = GreedDecision()
greed_row = evaluate_agent(greed_agent, "Greed", "rule")
comparison_data.append(greed_row)

spam_pile1_agent = SpamDecision(spam_option="pile_1")
spam_pile1_row = evaluate_agent(spam_pile1_agent, "Spam (pile_1)", "rule")
comparison_data.append(spam_pile1_row)

spam_pile2_agent = SpamDecision(spam_option="pile_2")
spam_pile2_row = evaluate_agent(spam_pile2_agent, "Spam (pile_2)", "rule")
comparison_data.append(spam_pile2_row)

df_comp = pd.DataFrame(comparison_data)
print("=== HEAD-TO-HEAD BENCHMARK TABLE ===\n")
df_comp_sorted = df_comp.sort_values(by="Accuracy", ascending=False)

print(df_comp_sorted.to_markdown(index=False))

