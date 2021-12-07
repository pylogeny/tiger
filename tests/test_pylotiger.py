import pytest

from pylotiger import get_set_partitions, get_rates, corrected_pas
import pylotiger
from pathlib import Path
import json


def test_get_rates():

    pth = Path(__file__).parent / "data.json"
    with open(pth) as f:
        data = json.load(f)
    sptns = get_set_partitions(data["patterns"], data["taxa"])
    rates = get_rates(sptns, selected_chars=["1", "2", "3", "4", "5"])
    for i in [1, 2, 3, 4, 5]:
        assert round(rates[str(i)], 2) == round(data["results"][i-1], 2)
    rates2 = get_rates(
            sptns, selected_chars=["1", "2", "3", "4", "5"],
            partition_func=corrected_pas)
    assert round(rates2["1"], 2) == 0.01
    assert round(rates2["1"], 2) < round(rates["1"], 2)
    
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

    parts = get_set_partitions(characters, taxa)
    rates = get_rates(parts)
    assert round(rates["X"], 2) == 0.54
    assert round(rates["A"], 2) == 1.00

    chars = {
            "C": {
                "a": ["A"],
                "b": ["A"],
                "c": ["C"],
                "d": ["C"],
                "e": ["C"]
                },
            "D": {
                "a": ["A"],
                "b": ["A"],
                "c": ["A"],
                "d": ["C"],
                "e": ["C"]
                },
            "E": {
                "a": ["A"],
                "b": ["A"],
                "c": ["A"],
                "d": ["A"],
                "e": []
                }
            }

    parts = get_set_partitions(chars, taxa)
    rates = get_rates(parts, partition_func=corrected_pas)
    assert corrected_pas(parts["C"], parts["D"]) == 1/3
    assert corrected_pas(parts["C"], parts["E"], taxlen=4, excluded="X") == "X"




