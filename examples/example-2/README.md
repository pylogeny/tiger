# Example 2: Computing Corrected TIGER Rates for Extreme Random Cognate Data

To run this code, just `cd` into the folder and type:

```
$ python run.py
```
*Results for Invariants*

|   Proportion | Characters   | CS-Size      | TIGER       | C-TIGER     |
|-------------:|:-------------|:-------------|:------------|:------------|
|          0   | 313 / 308    | 11.73 ± 5.40 | 0.71 ± 0.09 | 0.27 ± 0.19 |
|          0.2 | 313 / 245.17 | 9.06 ± 6.17  | 0.60 ± 0.17 | 0.30 ± 0.20 |
|          0.4 | 313 / 184.42 | 7.04 ± 6.36  | 0.55 ± 0.24 | 0.30 ± 0.20 |
|          0.6 | 313 / 122.51 | 5.01 ± 5.92  | 0.53 ± 0.31 | 0.30 ± 0.20 |
|          0.8 | 313 / 61.87  | 3.04 ± 4.68  | 0.53 ± 0.36 | 0.30 ± 0.20 |

*Results for Singletons*

|   Proportion | Characters   | CS-Size      | TIGER       | C-TIGER     |
|-------------:|:-------------|:-------------|:------------|:------------|
|          0   | 313 / 308    | 11.73 ± 5.40 | 0.71 ± 0.09 | 0.27 ± 0.19 |
|          0.2 | 313 / 245.22 | 13.96 ± 7.47 | 0.71 ± 0.12 | 0.30 ± 0.20 |
|          0.4 | 313 / 184.27 | 16.79 ± 8.26 | 0.75 ± 0.11 | 0.29 ± 0.20 |
|          0.6 | 313 / 122.39 | 19.67 ± 8.03 | 0.81 ± 0.10 | 0.30 ± 0.20 |
|          0.8 | 313 / 61.82  | 22.46 ± 6.70 | 0.87 ± 0.10 | 0.30 ± 0.20 |

# Original Preparation of Uralex Data

The file `uralex.tsv` was produced as follows (using `pyedictor`):

```
$ git clone https://github.com/lexibank/uralex.git
$ pip install pyedictor
$ cd uralex
$ edictor wordlist --addon=cogid_cognateset_id:cog --name=uralex
```
