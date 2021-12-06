# Compute TIGER Rates for Phylogenetic Data

This is a pure Python implementation of the TIGER rates ([Cummins and McInerney 2011](https://doi.org/10.1093/sysbio/syr064)), which can be computed for all kinds of phylogenetic data. The creation of the package was inspired by a study of [Syrjänenen et al. (2021)](https://doi.org/10.1093/jole/lzab004) in which the authors present a new implementation of TIGER rate computation for linguistic purposes. Since the implementation by Syrjänen et al. does not come along as a package, but rather as a commandline tool, whose application from within Python scripts is not straightforward, I decided to reimplement the rate computation based on the description in both publications in the form of a small Python package without further dependencies.  

# Workflow

In order to compute TIGER rates for your phylogenetic characters, your characters should be stored in the form of a nested Python dictionary in which each character is represented by a key, which links to a dictionary representing the character states. The character states themselves are represented by a dictionary with taxonomic units (language varieties, species) as key and character states being represented as values in the form of a list, allowing for polymorphous characters per taxonomic unit and for missing data, which would be passed as an empty list. In this form, character states can be conveniently stored in JSON format, such as the following examples from Cummins and McInerney, `A = CTTAA`, and `B = AGGGG`:

```json
{
  "A": {
    "1": ["C"],
    "2": ["T"],
    "3": ["T"],
    "4": ["A"],
    "5": ["A"]
  },
  "B": {
    "1": ["A"],
    "2": ["G"],
    "3": ["G"],
    "4": ["G"],
    "5": ["G"]
  }
}
```

With your characters stored in this form, you can then convert them to set partitions:

```python
>>> from pylotiger import get_set_partitions
>>> characters = {"A": {"1": ["C"], "2": ["T"], "3": ["T"], "4": ["A"], "5": ["A"]}, "B": {"1": ["A"], "2": ["G"], "3": ["G"], "4": ["G"], "5": ["G"]}}
>>> taxa = ["1", "2", "3", "4", "5"]
>>> set_partitions = get_set_partitions(characters, taxa)
```

The output is a dictionary with a character as a key and the corresponding set partition as a value. Set partitions consist of `frozensets` in which the taxonomic units (represented by numbers 1 to 5 here) are grouped. 

```python
>>> set_partitions
{'A': {frozenset({'1'}), frozenset({'4', '5'}), frozenset({'2', '3'})},
 'B': {frozenset({'1'}), frozenset({'2', '3', '4', '5'})}}
```

Since our implementation allows for polymorphous characters, it is possible that different set partitions contain the same taxonomic unit. If state information for a given character is missing, the corresponding taxonomic unit would not appear in any of the set partitions.

Having computed the set partitions, we can compare them with each other. Cummins and McInerney report that comparing A with B yields the score 0.5, while comparing B with A yields 1.

```python
>>> from pylotiger import get_partition_agreement_score
>>> get_partition_agreement_score(set_partitions["A"], set_partitions["B"])
0.5
>>> get_partition_agreement_score(set_partitions["B"], set_partitions["A"])
1
```

In order to compute the rates, we now use the exemplary data from the study of Syrjänen et al. (2021).

```json
{
  "X": {
    "a": ["A"],
    "b": ["B"],
    "c": ["A"],
    "d": ["A"],
    "e": ["C"]
  },
  "Y": {
    "a": ["D"],
    "b": ["D"],
    "c": ["E"],
    "d": ["E"],
    "e": ["F"]
  },
  "Z": {
    "a": ["G"],
    "b": ["H"],
    "c": ["H"],
    "d": ["H"],
    "e": ["H"]
  }
}
```

Here, the authors report rates of 0.5835 for character X and Y, and 0.667 for character Z.

```python
>>> from pylotiger import get_rates
>>> characters = {"X": {"a": ["A"], "b": ["B"], "c": ["A"], "d": ["A"], "e": ["C"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["F"] }, "Z": {"a": ["G"], "b": ["H"], "c": ["H"], "d": ["H"], "e": ["H"]}}
>>> taxa = ["a", "b", "c", "d", "e"]
>>> set_partitions = get_set_partitions(characters, taxa)
>>> rates = get_rates(set_partitions)
>>> for char in "XYZ":
...     print(char, "{0:.4f}".format(rates[char]))
X 0.5833
Y 0.5833
Z 0.6667
```

Note that in this version, the rate computation is not optimized with respect to repeating character values. As a result, the current implementation may take some time when being used to investigate datasets with many characters.

## Computing the Corrected TIGER Rates 

The TIGER rates are supposed to test the tree-likeness of a given dataset. In the form presented by Cummins and McInerney, *invariant characters* which have the same character state across all taxonomic units are not explicitly excluded from the data. This may be considered as problematic, since invariant characters do not provide any specific information about the subgrouping. In the original partition agreement score, however, they will always yield the score 1 when compared to *any* other set partition, as we can easily see when setting our character "X" in the previous example to reflect identical character states and comparing it with the other characters.

```python
>>> characters = {"X": {"a": ["A"], "b": ["A"], "c": ["A"], "d": ["A"], "e": ["A"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["F"] }, "Z": {"a": ["G"], "b": ["H"], "c": ["H"], "d": ["H"], "e": ["H"]}}
>>> taxa = ["a", "b", "c", "d", "e"]
>>> set_partitions = get_set_partitions(characters, taxa)
>>> for char in "YZ":
...     print("X vs.", char, "{0:.4f}".format(get_partition_agreement_score(set_partitions["X"], set_partitions[char])))
X vs. Y 1.0000
X vs. Z 1.0000
```

Conversely, if a characters has distinct states for all taxonomic units, all *other* set partitions in the data will receive a score of 1 when compared to it, as we can see easily when modifying character "X" in our example to have different states for all taxonomic units.

```python
>>> characters = {"X": {"a": ["A"], "b": ["B"], "c": ["C"], "d": ["D"], "e": ["E"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["F"] }, "Z": {"a": ["G"], "b": ["H"], "c": ["H"], "d": ["H"], "e": ["H"]}}
>>> taxa = ["a", "b", "c", "d", "e"]
>>> set_partitions = get_set_partitions(characters, taxa)
>>> for char in "YZ":
...     print(char, "vs. X", "{0:.4f}".format(get_partition_agreement_score(set_partitions[char], set_partitions["X"])))
Y vs. X 1.0000
Z vs. X 1.0000
```

One might argue that this kind of behavior is consistent with the original rate calculation, but when working with concrete language data, I found that the inclusion of characters which are not informative for the subgrouping may at times skew the scores, giving the impression that a dataset is highly tree-like, only because it contains many characters with singleton character states. For this reason, this implementation of TIGER rates provides a corrected version of the partition agreement score, which differs from the original partition agreement score in three respects:

1. singletons (character states that occur only once in the data) are excluded from the compatibility calculation,
2. invariant character states (which are identical for all characters) are excluded from the calculation, and
3. instead of dividing the matches (where partition A includes the partition B) by the number of sets in partition B, we divide by the number of intersections, which allows to catch those cases in which a character state is compatible with two partitions.

With respect to the handling of 1 and 2, we have two possibilities: we can set the score to 0 if we encounter a case of a character that consists only of singleton states or has only invariant states, or we can ignore it from the calculation.

To compute the corrected TIGER scores, all one needs to do is to import the `corrected_pas()` function and to pass it as the argument `partition_func` to the `get_rates()` function.

```python
>>> from pylotiger import corrected_pas
>>> characters = {"X": {"a": ["A"], "b": ["B"], "c": ["C"], "d": ["D"], "e": ["E"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["E"] }, "Z": {"a": ["G"], "b": ["G"], "c": ["G"], "d": ["H"], "e": ["H"]}}
>>> taxa = ["a", "b", "c", "d", "e"]
>>> set_partitions = get_set_partitions(characters, taxa)
>>> for x in "XYZ":
...     for y in "XYZ":
...         pas1 = get_partition_agreement_score(set_partitions[x], set_partitions[y])
...         pas2 = corrected_pas(set_partitions[x], set_partitions[y])
...         print("{0} | {1} | {2:.2f} | {3}".format(x, y, pas1, "{0:.2f}".format(pas2) if pas2 is not None else "None"))
X | X | 1.00 | None
X | Y | 0.00 | None
X | Z | 0.00 | None
Y | X | 1.00 | None
Y | Y | 1.00 | 1.00
Y | Z | 0.50 | 0.33
Z | X | 1.00 | None
Z | Y | 0.50 | 0.33
Z | Z | 1.00 | 1.00
```

As can be seen from this example, we exclude all comparisons with character X, for which the function yields `None`. When computing TIGER rates, these characters will be excluded from the rate calculation. Furthermore, the calculation of scores for character Y (states: DDEEE) and Z (states: GGGHH) also shows a crucial difference, in so far, as we identify three possible links between character states in Z and character states in Y (G=abc → D=ab, G=abc → E=cde, and H=de → E=cde), of which only one is compatible (G → D). As a result, the score is set to 0.33 (1/3) instead of 0.5, as in the calculation of the original TIGER partition agreement rates.


