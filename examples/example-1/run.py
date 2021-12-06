"""
Compare TIGER Scores for Simulated Data
"""

from pylotiger import get_set_partitions, get_rates, corrected_pas
import statistics
from pathlib import Path
from tqdm import tqdm as progressbar
from tabulate import tabulate

def parse_file(path):
    with open(path) as f:
        data = []
        for line in f:
            data += [line.strip().split(',')]
    patterns = {i: {} for i in range(1, len(data[0]))}
    for row in data[1:]:
        for i, char in enumerate(row[1:]):
            patterns[i+1][row[0]] = [char]
    return patterns, [row[0] for row in data[1:]]


table = []
for f in [
        "pure_tree", 
        "borrowing_05", 
        "borrowing_10", 
        "borrowing_15", 
        "borrowing_20", 
        "dialect", 
        "swamp"]:
    scoresA, scoresB = [], []
    for pth in progressbar(list(Path(f).glob("*.csv")), desc="{0}".format(f)):
        patterns, taxa = parse_file(pth)
        spt = get_set_partitions(patterns, taxa)
        ratesA = get_rates(spt)
        ratesB = get_rates(
                spt, partition_func=corrected_pas, 
                )
        scoreA = statistics.mean(ratesA.values())
        scoreB = statistics.mean(ratesB.values())
        scoresA += [scoreA]
        scoresB += [scoreB]
    print("{0:10} {1:.2f}   {2:.2f}  {3:.2f}  {4:.2f}".format(
        f,
        statistics.mean(scoresA),
        statistics.stdev(scoresA),
        statistics.mean(scoresB),
        statistics.stdev(scoresB)
        ))
    table += [[
        f,
        "{0:.2f} ± {1:.2f}".format(
            statistics.mean(scoresA),
            statistics.stdev(scoresA)),
        "{0:.2f} ± {1:.2f}".format(
            statistics.mean(scoresB),
            statistics.stdev(scoresB))]]
print(tabulate(table, headers=["Datasets", "TIGER", "C-TIGER"], tablefmt="pipe"))

