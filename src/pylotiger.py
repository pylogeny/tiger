"""Calculate TIGER values following Cummins and McInerney (2011)"""

from collections import defaultdict
import statistics


def get_rates(
        set_partitions,
        selected_chars=None,
        partition_func=None,
        partition_kw=None,
        ):
    """
    Compute the rate for one character.

    @param set_partitions: The set partitions returned by the
      get_set_partitions function.
    @selected_chars: If passed as a list, the computation will only look at the
      characters selected.
    @partition_func: Allows to pass a modified function that computes partition
      agreement scores, such as the corrected_pas function, for example.
    @partition_kw: Keywords passed to the partition agreement score function.
    """
    partition_func = partition_func or get_partition_agreement_score
    partition_kw = partition_kw or {}
    rates = {}
    chars = [char for char, ps in set_partitions.items() if ps]
    selected_chars = selected_chars or chars
    for i, char in enumerate(selected_chars):
        scores = []
        for j, charB in enumerate(chars):
            if i != j:
                scores += [partition_func(
                        set_partitions[char],
                        set_partitions[charB],
                        **partition_kw
                        )]
        rates[char] = statistics.mean(scores)
    return rates


def get_partition_agreement_score(partitionA, partitionB):
    """
    Compute the partition agreement score for two partitions.
    """
    scores = []
    for i, prtB in enumerate(partitionB):
        score = 0
        for j, prtA in enumerate(partitionA):
            if prtB.issubset(prtA):
                score = 1
                break
        scores += [score]
    return statistics.mean(scores or [0])


def corrected_pas(partitionA, partitionB, taxlen=None):
    """
    Computed corrected partition agreement score.

    The corrected partition agreement score corrects for singleton character
    states and for character states that recur in all the taxonomic units in
    the data. These extreme cases are successively ignored when computing the
    partition agreement score.
    """
    links, matches = [], []
    # prune by getting number of taxa described by partition
    if not taxlen:
        all_taxa = set()
        for prt in partitionA.union(partitionB):
            for taxon in prt:
                all_taxa.add(taxon)
        taxlen = len(all_taxa)
    for i, prtB in enumerate(partitionB):
        for j, prtA in enumerate(partitionA):
            if taxlen > len(prtA) > 1 and taxlen > len(prtB) > 1:
                if prtA.intersection(prtB):
                    links += [1]
                if prtB.issubset(prtA):
                    matches += [1]
    if matches:
        return sum(matches)/sum(links)
    return 0


def get_set_partitions(characters, taxa):
    """
    Retrieve set partitions from patterns.

    @param characters: Characters coded as a dictionary with keys for each
      characters and values consisting of a dictionary with taxa as key and
      character states added in a list.
    @param taxa: The taxonomic units passed as a list.
    """
    parts = {}
    for char, vals in characters.items():
        parts[char] = set()
        converter = defaultdict(set)
        active_chars = [t for t, chars in vals.items() if chars]

        for taxon in taxa:
            for state in vals[taxon]:
                converter[state].add(taxon)
        for state, partition in converter.items():
            parts[char].add(frozenset(partition))
    return parts


