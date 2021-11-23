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

## Pruning Uninformative Character States

The TIGER rates are supposed to test the tree-likeness of a given dataset. In the form presented by Cummins and McInerney, characters which have the same character state across all taxonomic units are not explicitly excluded from the data. This may be considered as problematic, since characters which have the same states for all taxonomic units do not provide any specific information about the subgrouping. Consequently, they will always yield the score 1 when compared to *any* other set partition, as we can easily see when setting our character "X" in the previous example to reflect identical character states and comparing it with the other characters.

```python
>>> characters = {"X": {"a": ["A"], "b": ["A"], "c": ["A"], "d": ["A"], "e": ["A"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["F"] }, "Z": {"a": ["G"], "b": ["H"], "c": ["H"], "d": ["H"], "e": ["H"]}}
>>> taxa = ["a", "b", "c", "d", "e"]
>>> set_partitions = get_set_partitions(characters, taxa)
>>> for char in "YZ":
        print("X vs.", char, "{0:.4f}".format(get_partition_agreement_score(set_partitions["X"], set_partitions[char])))
X vs. Y 1.0000
X vs. Z 1.0000
```

Conversely, if a characters has distinct states for all taxonomic units, all *other* set partitions in the data will receive a score of 1 when compared to it, as we can see easily when modifying character "X" in our example to have different states for all taxonomic units.

```python
>>> characters = {"X": {"a": ["A"], "b": ["B"], "c": ["C"], "d": ["D"], "e": ["E"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["F"] }, "Z": {"a": ["G"], "b": ["H"], "c": ["H"], "d": ["H"], "e": ["H"]}}
>>> taxa = ["a", "b", "c", "d", "e"]
>>> set_partitions = get_set_partitions(characters, taxa)
>>> for char in "YZ":
        print(char, "vs. X", "{0:.4f}".format(get_partition_agreement_score(set_partitions[char], set_partitions["X"])))
Y vs. X 1.0000
Z vs. X 1.0000
```

One might argue that this kind of behavior is consistent with the original rate calculation, but when working with concrete language data, I found that the inclusion of characters which are not informative for the subgrouping may at times skew the scores, giving the impression that a dataset is highly tree-like, only because it contains many characters with singleton character states. For this reason, the computatin of the set partitions was extended in such a way that *extremes*, that is, character states which occur either only once in a character or repeat across all taxonomic units, can be filtered out. As a result, the set partitions which are computed from the data will only consist of partitions that contain *at least* two taxonomic units and at most one taxonomic unit less than the total number of characters. If no extreme cases occur in the data, the scores will be identical with the original TIGER rate scores. But if they occur, they will have an impact. If there are many singletons, for example, the overall similarity of all individual characters to all other characters in the data, will be lowered. If there are many characters with identical states for all taxonomic units in the data, these characters would not be listed when plotting and comparing character rates. While I cannot claim this score to be superior to the original TIGER scores, I think that these TIGER scores corrected for uninformative cases are useful to be considered when dealing with datasets that are skewed in either of the two directions.

To compute the corrected TIGER scores, all one needs to do is to set the `filter_extremes` argument in the function computing the set partitions to `True`.

```python
characters = {"X": {"a": ["A"], "b": ["B"], "c": ["C"], "d": ["D"], "e": ["E"] }, "Y": {"a": ["D"], "b": ["D"], "c": ["E"], "d": ["E"], "e": ["F"] }, "Z": {"a": ["G"], "b": ["H"], "c": ["H"], "d": ["H"], "e": ["H"]}}
taxa = ["a", "b", "c", "d", "e"]
set_partitions = get_set_partitions(characters, taxa, filter_extremes=True)
for p, sets in set_partitions.items():
    print(p, repr(sets))
X set()
Y {frozenset({'c', 'd'}), frozenset({'a', 'b'})}
Z {frozenset({'e', 'd', 'c', 'b'})}
```

As can be seen in this example, excluding "extreme" character states will yield
an empty set for character X. When computing TIGER rates for this dataset,
character X would consequently be excluded from the computation. Additionally,
however, the filtering also excludes the singleton character states from
characters Y and Z. As a result, teh partition agreement score from Y to Z
changes from 0.667 to 0.5, since from two informative partitions in Y only one
is compatible with the partition in Z. The score from Z to Y changes to 0,
since the only partition left in character Y is not compatible with either of
the two partitions left in Y.

```python
>>> get_partition_agreement_score(set_partitions["Z"], set_partitions["Y"])
0
>>> get_partition_agreement_score(set_partitions["Y"], set_partitions["Z"])
0.5
```
