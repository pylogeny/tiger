"""
Compute traditional and corrected TIGER scores for different datasets.
"""
from lingpy import *
from matplotlib import pyplot as plt
from pylotiger import get_set_partitions, get_rates, corrected_pas
from pylodata.wordlist import get_multistate_patterns
import statistics
from tabulate import tabulate
from phylogemetric.delta import DeltaScoreMetric

def get_matrix(taxa, patterns):
    
    matrix = {t: [] for t in taxa}
    for p, v in patterns.items():
        for taxon in taxa:
            matrix[taxon] += [v[taxon][0] if v[taxon] else "-"]
    return matrix


dsets = [
        "uralex",
        "dravlex",
        "wichmannmixezoquean",
        "dunnaslian",
        "felekesemitic",
        "hattorijaponic",
        "deepadungpalaung",
        ]

labels = [
        "Uralic",
        "Dravidian",
        "Mixe-Zoquean",
        "Aslian",
        "Semitic",
        "Japonic",
        "Palaung",
        ]

table = []
data = []
for i, ds in enumerate(dsets):
    wl = Wordlist(ds+'.tsv')
    wl.renumber("cog")
    print("# "+ds)
    cogs, cogsprop = [], []
    for cogid, (idxs, languages) in wl.iter_cognates("cogid", "doculect"):
        cogs += [len(set(languages))]
        cogsprop += [len(set(languages)) / wl.width]
    wl.calculate("diversity")
    patterns = get_multistate_patterns(wl, ref="cogid", missing=None)[0]
    sp = get_set_partitions(patterns, wl.cols)
    rates1 = get_rates(sp, partition_func=None)
    rates2 = get_rates(
            sp, partition_func=corrected_pas,
            partition_kw={"excluded": None})
    delta = DeltaScoreMetric(matrix=get_matrix(wl.cols, patterns)).score()
    data += [[list(rates1.values()), list(rates2.values()), cogsprop, wl.diversity]]
    table += [[
        labels[i],
        wl.width,
        wl.height,
        wl.diversity,
        "{0} / {1}".format(len(rates1), len(rates2)),
        cogs.count(1) / len(cogs),
        cogs.count(wl.width) / len(cogs),
        "{0:.2f} ± {1:.2f}".format(
            statistics.mean(rates1.values()),
            statistics.stdev(rates1.values())),
        "{0:.2f} ± {1:.2f}".format(
            statistics.mean(rates2.values()),
            statistics.stdev(rates2.values())),
        "{0:.2f} ± {1:.2f}".format(
            statistics.mean(delta.values()),
            statistics.stdev(delta.values())),
        ]]
print(tabulate(
    table, 
    headers=[
        "Dataset", "Languages", "Concepts", "Diversity",
        "Chars",
        "Singletons", "Invariants",
        "TIGER", "C-TIGER", "Delta"],
    tablefmt="pipe",
    floatfmt=".2f"))

plt.clf()
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
myrange = list(range(1, 20, 3))
vparts = ax.violinplot(
        [row[0] for row in data], 
        myrange, showmeans=True,
        widths=[0.95 for x in myrange],
        )
for vp in vparts["bodies"]:
    vp.set_facecolor("cornflowerblue")
vparts = ax.violinplot(
        [row[1] for row in data], 
        [x+1 for x in myrange], showmeans=True,
        widths=[0.95 for x in myrange],
        )
for vp in vparts["bodies"]:
    vp.set_facecolor("crimson")

vparts = ax.violinplot(
        [row[2] for row in data], 
        [x+2 for x in myrange], showmeans=True,
        widths=[0.95 for x in myrange],
        )
for vp in vparts["bodies"]:
    vp.set_facecolor("black")


ax.set_xticks([x+1 for x in myrange])
for x in myrange:
    ax.axvline(
            x+2.5, 
            -0.05, 
            1.05,
            color="black", linestyle="-", linewidth=0.5)
ax.plot(
        [x+1 for x in myrange], [row[3] for row in data], "o",
        color="black")
ax.set_xticklabels(labels, rotation=45)
ax.set_ylim(-0.05, 1.05)
ax.set_xlim(0.0, 21.5)
plt.savefig('experiment-3.pdf')
