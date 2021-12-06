"""
Check varying degrees of invariants and singletons in the TIGER rates.
"""
from lingpy import *
from pylotiger import get_set_partitions, get_rates, corrected_pas
from pylodata.wordlist import get_multistate_patterns
import statistics
from tabulate import tabulate
import random
from tqdm import tqdm as progressbar

def add_singletons(wordlist, prop=None, ref="randomid", cognates="cogid"):
    prop = prop or 0.25
    concepts = wordlist.rows
    selected = random.sample(concepts, int(prop * len(concepts)+0.5))
    cogid = max(wordlist.get_etymdict(ref=cognates))+1
    C = {idx: wordlist[idx, cognates] for idx in wordlist}
    for concept in selected:
        idxs = wordlist.get_list(row=concept, flat=True)
        for idx in idxs:
            C[idx] = cogid
            cogid += 1
    wordlist.add_entries(ref, C, lambda x: x)


def add_invariants(wordlist, prop=None, ref="randomid", cognates="cogid"):
    prop = prop or 0.25
    concepts = wordlist.rows
    selected = random.sample(concepts, int(prop * len(concepts)+0.5))
    cogid = max(wordlist.get_etymdict(ref=cognates))+1
    C = {idx: wordlist[idx, cognates] for idx in wordlist}
    for concept in selected:
        idxs = wordlist.get_list(row=concept, flat=True)
        for idx in idxs:
            C[idx] = cogid
        cogid += 1
    wordlist.add_entries(ref, C, lambda x: x)


RUNS = 100
wl = Wordlist('uralex.tsv')
wl.renumber("cog")
patterns = get_multistate_patterns(wl, ref="cogid", missing="Ø")[0]
sp = get_set_partitions(patterns, wl.cols)
plens = [len(x) for x in sp.values()]
rates1 = get_rates(sp, partition_func=None)
rates2 = get_rates(sp, partition_func=corrected_pas)

table = [[
    "0.0",
    "{0} / {1}".format(len(rates1), len(rates2)),
    "{0:.2f} ± {1:.2f}".format(
        statistics.mean(plens),
        statistics.stdev(plens)),
    "{0:.2f} ± {1:.2f}".format(
        statistics.mean(rates1.values()),
        statistics.stdev(rates1.values())),
    "{0:.2f} ± {1:.2f}".format(
        statistics.mean(rates2.values()),
        statistics.stdev(rates2.values())),
        ]]

table2 = [table[0]]
for prop in [0.2, 0.4, 0.6, 0.8]:
    scores = []
    for i in progressbar(range(RUNS)):
        ts = "rn"+str(i)+"_"+str(int(10*prop+0.5))
        add_invariants(wl, prop=prop, ref=ts)
        patterns = get_multistate_patterns(wl, ref=ts, missing=None)[0]
        sp = get_set_partitions(patterns, wl.cols)
        plens = [len(x) for x in sp.values()]
        rates1 = get_rates(sp, partition_func=None)
        rates2 = get_rates(sp, partition_func=corrected_pas)

        scores += [[
            len(rates1), 
            len(rates2),
            statistics.mean(plens),
            statistics.stdev(plens),
            statistics.mean(rates1.values()),
            statistics.stdev(rates1.values()),
            statistics.mean(rates2.values()),
            statistics.stdev(rates2.values()),
            ]]
    table2 += [[
            "{0:.2f}".format(prop),
            "{0} / {1:.2f}".format(
                len(rates1),
                statistics.mean([row[1] for row in scores])),
            "{0:.2f} ± {1:.2f}".format(
                statistics.mean([row[2] for row in scores]),
                statistics.mean([row[3] for row in scores])),
            "{0:.2f} ± {1:.2f}".format(
                statistics.mean([row[4] for row in scores]),
                statistics.mean([row[5] for row in scores])),
            "{0:.2f} ± {1:.2f}".format(
                statistics.mean([row[6] for row in scores]),
                statistics.mean([row[7] for row in scores])),
            ]]
print("# Invariants")
print(tabulate(table2, 
    headers=[
        "Proportion", "Characters", 
        "CS-Size", "TIGER", "C-TIGER"
        ],
    tablefmt="pipe"))


for prop in [0.2, 0.4, 0.6, 0.8]:
    scores = []
    for i in progressbar(range(RUNS)):
        ts = "r"+str(i)+"_"+str(int(10*prop+0.5))
        add_singletons(wl, prop=prop, ref=ts)
        patterns = get_multistate_patterns(wl, ref=ts, missing=None)[0]
        sp = get_set_partitions(patterns, wl.cols)
        plens = [len(x) for x in sp.values()]
        rates1 = get_rates(sp, partition_func=None)
        rates2 = get_rates(sp, partition_func=corrected_pas)

        scores += [[
            len(rates1), 
            len(rates2),
            statistics.mean(plens),
            statistics.stdev(plens),
            statistics.mean(rates1.values()),
            statistics.stdev(rates1.values()),
            statistics.mean(rates2.values()),
            statistics.stdev(rates2.values()),
            ]]
    table += [[
            "{0:.2f}".format(prop),
            "{0} / {1:.2f}".format(
                len(rates1),
                statistics.mean([row[1] for row in scores])),
            "{0:.2f} ± {1:.2f}".format(
                statistics.mean([row[2] for row in scores]),
                statistics.mean([row[3] for row in scores])),
            "{0:.2f} ± {1:.2f}".format(
                statistics.mean([row[4] for row in scores]),
                statistics.mean([row[5] for row in scores])),
            "{0:.2f} ± {1:.2f}".format(
                statistics.mean([row[6] for row in scores]),
                statistics.mean([row[7] for row in scores])),
            ]]
print("# Singletons")
print(tabulate(table, 
    headers=[
        "Proportion", "Characters", 
        "CS-Size", "TIGER", "C-TIGER"
        ],
    tablefmt="pipe"))




