import pytest

from pylotiger import get_set_partitions, get_rates
import pylotiger
from pathlib import Path
import json


def test_get_rates():

    pth = Path(pylotiger.__file__).parent.parent / "tests" / "data.json"
    with open(pth) as f:
        data = json.load(f)
    sptns = get_set_partitions(data["patterns"], data["taxa"])
    rates = get_rates(sptns, selected_chars=["1", "2", "3", "4", "5"])
    for i in [1, 2, 3, 4, 5]:
        assert round(rates[str(i)], 2) == round(data["results"][i-1], 2)
    sptns2 = get_set_partitions(data["patterns"], data["taxa"],
            filter_extremes=True) 
    rates2 = get_rates(sptns2, selected_chars=["1", "2", "3", "4", "5"])
    assert round(rates2["1"], 2) == 0.03
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



