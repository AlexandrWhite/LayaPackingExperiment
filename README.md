docker buildx build  . -t laya_experiment
docker run -itd --name stone_packing --mount "type=bind,source=$($PWD.Path),target=/workspace" --gpus all laya_experiment
docker exec -it stone_packing /bin/bash


| Model         | Kind             |   Accuracy |   Soft Acc |   Brier |   ECE |
|:--------------|:-----------------|-----------:|-----------:|--------:|------:|
| Laya          | fine-tuned       |      0.862 |      0.82  |   0.191 | 0.041 |     
| Greed         | rule             |      0.533 |      0.533 |   0.915 | 0.457 |     
| Random        | rule             |      0.518 |      0.518 |   0.945 | 0.472 |     
| Laya          | without-training |      0.504 |      0.511 |   0.515 | 0.119 |     
| Spam (pile_1) | rule             |      0.5   |      0.5   |   0.98  | 0.49  |     
| Spam (pile_2) | rule             |      0.5   |      0.5   |   0.98  | 0.49  | 


=== HEAD-TO-HEAD BENCHMARK TABLE ===
| Model         | Kind             |   Accuracy |   Soft Acc |   Brier |   ECE |   Score MAE |   ms/case |
|:--------------|:-----------------|-----------:|-----------:|--------:|------:|------------:|----------:|
| Laya          | fine-tuned20k    |      0.844 |      0.824 |   0.186 | 0.013 |           0 |      20.1 |
| Greed         | rule             |      0.583 |      0.582 |   0.817 | 0.407 |           0 |       0   |
| Laya          | fine-tuned       |      0.524 |      0.525 |   0.764 | 0.353 |           0 |      20   |
| Spam (pile_2) | rule             |      0.5   |      0.5   |   0.98  | 0.49  |           0 |       0   |
| Spam (pile_1) | rule             |      0.5   |      0.5   |   0.98  | 0.49  |           0 |       0   |
| Random        | rule             |      0.496 |      0.496 |   0.988 | 0.494 |           0 |       0   |
| Laya          | without-training |      0.477 |      0.489 |   0.575 | 0.16  |           0 |      20.4 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=10 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 12.86 |          44 |           0 |                    13.4  |                             0.54 |
| greed     |                  2.8  |          10 |           0 |                     3.34 |                             0.54 |
| model-20k |                  2.24 |          10 |           0 |                     2.78 |                             0.54 |
| model-800 |                  6.76 |          26 |           0 |                     7.3  |                             0.54 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=30 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 25.92 |          76 |           0 |                    26.54 |                             0.62 |
| greed     |                  2.66 |           8 |           0 |                     3.28 |                             0.62 |
| model-20k |                 22.16 |          80 |           0 |                    22.78 |                             0.62 |
| model-800 |                 45.38 |          90 |           2 |                    46    |                             0.62 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=5 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 12.32 |          40 |           0 |                    13.39 |                             1.07 |
| greed     |                  2.52 |           8 |           0 |                     3.59 |                             1.07 |
| model-20k |                  1.38 |           8 |           0 |                     2.45 |                             1.07 |
| model-800 |                  6.74 |          24 |           0 |                     7.81 |                             1.07 |


