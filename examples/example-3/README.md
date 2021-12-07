# Experiment 3: Using TIGER rates on linguistic data

Just type:
```
$ python run.py
```

This will yield:

| Dataset      |   Languages |   Concepts |   Diversity | Chars     |   Singletons |   Invariants | TIGER       | C-TIGER     | Delta       |
|:-------------|------------:|-----------:|------------:|:----------|-------------:|-------------:|:------------|:------------|:------------|
| Uralic       |          27 |        313 |        0.37 | 313 / 307 |         0.64 |         0.00 | 0.68 ± 0.13 | 0.30 ± 0.20 | 0.17 ± 0.03 |
| Dravidian    |          20 |        100 |        0.33 | 100 / 96  |         0.64 |         0.00 | 0.65 ± 0.10 | 0.20 ± 0.17 | 0.30 ± 0.04 |
| Mixe-Zoquean |          10 |        110 |        0.23 | 110 / 89  |         0.41 |         0.06 | 0.55 ± 0.24 | 0.28 ± 0.16 | 0.18 ± 0.03 |
| Aslian       |          32 |        146 |        0.19 | 146 / 145 |         0.40 |         0.00 | 0.55 ± 0.10 | 0.20 ± 0.15 | 0.24 ± 0.02 |
| Semitic      |          21 |        150 |        0.18 | 150 / 143 |         0.47 |         0.01 | 0.58 ± 0.13 | 0.21 ± 0.21 | 0.26 ± 0.03 |
| Japonic      |          10 |        200 |        0.15 | 200 / 120 |         0.40 |         0.17 | 0.60 ± 0.32 | 0.26 ± 0.17 | 0.27 ± 0.07 |
| Palaung      |          16 |        100 |        0.08 | 100 / 64  |         0.16 |         0.15 | 0.53 ± 0.34 | 0.28 ± 0.16 | 0.20 ± 0.02 |

# Original Preparation of Data

The wordlist files can be produced with `make`:

```
$ make clone
$ make wordlists
```
