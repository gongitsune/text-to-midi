import json
import itertools
import markov
from music_chords import Chord


def to_chord(chord_list: list[str]):
    return list(map(lambda x: Chord(x).note_numbers(), chord_list))


with open("dist/chords_data.json", "r") as f:
    data: list[list[str]] = json.load(f)
    molding_data = list(itertools.chain.from_iterable(data))
    model = markov.make_model(molding_data, order=4)
    result = [
        elem
        for elem in markov.make_result(model, max_items=10, seed="G", num=1)[0]
        if elem != "[EOF]" and elem != "[BOF]" and "on" not in elem
    ]
    print(result)
    print(to_chord(result))
