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

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=11 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 16.82 |          62 |           0 |                    17.31 |                             0.49 |
| greed     |                  3    |          10 |           0 |                     3.49 |                             0.49 |
| model-20k |                  2.48 |           8 |           0 |                     2.97 |                             0.49 |
| model-800 |                  8.08 |          36 |           0 |                     8.57 |                             0.49 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=12 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 18.04 |          60 |           0 |                    18.51 |                             0.47 |
| greed     |                  3.32 |          10 |           0 |                     3.79 |                             0.47 |
| model-20k |                  2.84 |          12 |           0 |                     3.31 |                             0.47 |
| model-800 |                  9.62 |          26 |           0 |                    10.09 |                             0.47 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=13 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 16.38 |          52 |           0 |                    16.96 |                             0.58 |
| greed     |                  3.36 |          10 |           0 |                     3.94 |                             0.58 |
| model-20k |                  2.68 |          10 |           0 |                     3.26 |                             0.58 |
| model-800 |                 10.16 |          34 |           0 |                    10.74 |                             0.58 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=15 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 17.58 |          56 |           0 |                    18.1  |                             0.52 |
| greed     |                  3    |          10 |           0 |                     3.52 |                             0.52 |
| model-20k |                  2.5  |           8 |           0 |                     3.02 |                             0.52 |
| model-800 |                  9.64 |          32 |           0 |                    10.16 |                             0.52 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=16 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 19.64 |          60 |           0 |                    20.1  |                             0.46 |
| greed     |                  3.34 |          10 |           0 |                     3.8  |                             0.46 |
| model-20k |                  3.22 |          12 |           0 |                     3.68 |                             0.46 |
| model-800 |                 10.14 |          26 |           0 |                    10.6  |                             0.46 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=17 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 18.46 |          58 |           0 |                    18.9  |                             0.44 |
| greed     |                  3.2  |          10 |           0 |                     3.64 |                             0.44 |
| model-20k |                  3.2  |          10 |           0 |                     3.64 |                             0.44 |
| model-800 |                  8.1  |          30 |           0 |                     8.54 |                             0.44 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=18 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 21.24 |          70 |           0 |                    21.77 |                             0.53 |
| greed     |                  3.18 |          10 |           0 |                     3.71 |                             0.53 |
| model-20k |                  2.96 |          12 |           0 |                     3.49 |                             0.53 |
| model-800 |                  8.4  |          28 |           0 |                     8.93 |                             0.53 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=19 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 19.52 |          76 |           0 |                    20.03 |                             0.51 |
| greed     |                  3.28 |          10 |           0 |                     3.79 |                             0.51 |
| model-20k |                  3.2  |          12 |           0 |                     3.71 |                             0.51 |
| model-800 |                  8.18 |          32 |           0 |                     8.69 |                             0.51 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=20 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 22.12 |          82 |           0 |                    22.61 |                             0.49 |
| greed     |                  3.1  |          10 |           0 |                     3.59 |                             0.49 |
| model-20k |                  3.34 |          10 |           0 |                     3.83 |                             0.49 |
| model-800 |                  8.9  |          32 |           0 |                     9.39 |                             0.49 |


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=25 on 100 tests, weights [1, 10]) ===
| policy    |   mean_absolute_error |   max_error |   min_error |   policy_mean_difference |   grounded_truth_mean_difference |
|:----------|----------------------:|------------:|------------:|-------------------------:|---------------------------------:|
| random    |                 26.76 |          84 |           0 |                    27.2  |                             0.44 |
| greed     |                  2.84 |          10 |           0 |                     3.28 |                             0.44 |
| model-20k |                  5.1  |          28 |           0 |                     5.54 |                             0.44 |
| model-800 |                 24.2  |          60 |           0 |                    24.64 |                             0.44 |




