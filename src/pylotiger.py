"""Calculate TIGER values following Cummins and McInerney (2011)"""

from collections import defaultdict
import statistics


def get_rates(
        set_partitions
        ):
    """
    Compute the rate for one character.
    """
    rates = {}
    chars = [char for char, ps in set_partitions.items() if ps]
    for i, char in enumerate(chars):
        scores = []
        for j, charB in enumerate(chars):
            if i != j:
                scores += [get_partition_agreement_score(
                        set_partitions[char],
                        set_partitions[charB]
                        )]
        rates[char] = statistics.mean(scores)
    return rates


def get_partition_agreement_score(partitionA, partitionB):
    """
    Compute the partition agreement score for two partitions.
    """
    scores = []
    for i, prtA in enumerate(partitionB):
        score = 0
        for j, prtB in enumerate(partitionA):
            if prtA.issubset(prtB):
                score = 1
                break
        scores += [score]
    return statistics.mean(scores or [0])


def get_set_partitions(characters, taxa, filter_extremes=False):
    parts = {}
    for char, vals in characters.items():
        parts[char] = set()
        converter = defaultdict(set)
        for taxon in taxa:
            for state in vals[taxon]:
                converter[state].add(taxon)
        for state, partition in converter.items():
            if filter_extremes:
                if 1 < len(partition) < len(taxa):
                    parts[char].add(frozenset(partition))
            else:
                parts[char].add(frozenset(partition))
    return parts


if __name__ == "__main__":

    characters = {
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
                },
            "A": {
                "a": ["H"],
                "b": ["H"],
                "c": ["H"],
                "d": ["H"],
                "e": ["H"]
                },
            "B": {
                "a": ["A"],
                "b": ["B"],
                "c": ["C"],
                "d": ["D"],
                "e": ["E"]
                }
            }
    taxa = list("abcde")

    parts = get_set_partitions(characters, taxa, filter_extremes=True)
    for i, charA in enumerate("XYZAB"):
        for j, charB in enumerate("XYZAB"):
            print(charA, charB, "{0:.2f}".format(
                get_partition_agreement_score(
                        parts[charA],
                        parts[charB])
                ))

    rates = get_rates(parts)
    for char, rate in rates.items():
        print(char, rate)



