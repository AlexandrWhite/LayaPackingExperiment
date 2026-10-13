| Model         | Kind             |   Accuracy |   Soft Acc |   Brier |   ECE |
|:--------------|:-----------------|-----------:|-----------:|--------:|------:|
| Laya          | fine-tuned       |      0.862 |      0.82  |   0.191 | 0.041 |     
| Greed         | rule             |      0.533 |      0.533 |   0.915 | 0.457 |     
| Random        | rule             |      0.518 |      0.518 |   0.945 | 0.472 |     
| Laya          | without-training |      0.504 |      0.511 |   0.515 | 0.119 |     
| Spam (pile_1) | rule             |      0.5   |      0.5   |   0.98  | 0.49  |     
| Spam (pile_2) | rule             |      0.5   |      0.5   |   0.98  | 0.49  | 


=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=10 on 200 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 2.99 |         10 |          0 |
| laya fine_tuned_20k |                 2.51 |         10 |          0 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=100 on 200 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 3.01 |         10 |          0 |
| laya fine_tuned_20k |               414.74 |        506 |         42 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=30 on 50 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 2.52 |          8 |          0 |
| laya fine_tuned_20k |                19.64 |         80 |          0 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=20 on 50 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 3.08 |          8 |          0 |
| laya fine_tuned_20k |                 3.2  |         10 |          0 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=10 on 50 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 2.44 |         10 |          0 |
| laya fine_tuned_20k |                 2.68 |         10 |          0 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=10 on 100 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 2.8  |         10 |          0 |
| laya fine_tuned_20k |                 2.24 |         10 |          0 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=15 on 100 tests, weights [1, 10]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                  3   |         10 |          0 |
| laya fine_tuned_20k |                  2.5 |          8 |          0 |

=== HEAD-TO-HEAD BENCHMARK TABLE (n_stones=15 on 100 tests, weights [1, 20]) ===
| policy              |   mean_absolute_diff |   max_diff |   min_diff |
|:--------------------|---------------------:|-----------:|-----------:|
| greed               |                 6.2  |         18 |          0 |
| laya fine_tuned_20k |                10.78 |         70 |          0 |