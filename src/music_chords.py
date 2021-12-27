import re


class Chords:
    chords = {
        re.compile(r"m"): [0, 3, 7],
        re.compile(r"sus4"): [0, 5, 7],
        re.compile(r"\(b5\)|\(-5\)"): [0, 4, 6],
        re.compile(r"\(#5\)|\(\+5\)|aug"): [0, 4, 8],
        re.compile(r"6"): [0, 4, 7, 9],
        re.compile(r"7"): [0, 4, 7, 10],
        re.compile(r"M7"): [0, 4, 7, 11],
        re.compile(r"\(add9\)"): [0, 2, 4, 7],
        re.compile(r"9"): [0, 2, 4, 7, 10],
        re.compile(r"\(-9\)"): [0, 1, 4, 7],
        re.compile(r"\(+9\)"): [0, 3, 4, 7],
        re.compile(r"dim"): [0, 3, 6],
        re.compile(r"11"): [0, 4, 5, 7, 10],
        re.compile(r"13"): [0, 4, 7, 9, 10],
        # Combination
        re.compile(r"7sus4"): [0, 5, 7, 10],
        re.compile(r"6\(add9\)"): [0, 2, 4, 7, 9],
        re.compile(r"m6"): [0, 3, 7, 9],
        re.compile(r"m6\(add9\)"): [0, 2, 3, 7, 9],
        re.compile(r"dim7"): [0, 3, 6, 9],
        re.compile(r"m7"): [0, 3, 7, 10],
        re.compile(r"m7\(-5\)"): [0, 3, 6, 10],
        re.compile(r"m\(add9\)"): [0, 2, 3, 7],
        re.compile(r"m9"): [0, 2, 3, 7, 10],
        re.compile(r"m7\(add9\)"): [0, 2, 3, 7, 10],
        re.compile(r"mM7"): [0, 3, 7, 11],
        re.compile(r"M7\(add9\)"): [0, 2, 4, 7, 11],
        re.compile(r"mM7\(add9\)"): [0, 2, 3, 7, 11],
        re.compile(r"7\(add9\)"): [0, 2, 4, 7, 10],
        re.compile(r"7\(-5\)"): [0, 4, 6, 10],
        re.compile(r"7\(+5\)"): [0, 4, 8, 10],
        re.compile(r"7\(-9\)"): [0, 1, 4, 7, 10],
        re.compile(r"7\(+9\)"): [0, 3, 4, 7, 10],
        re.compile(r"13\(-9\)"): [0, 1, 4, 7, 9, 10],
    }
    ROOT_NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

    def __init__(self, chords_order: list[str]) -> None:
        pass

    def str_to_chords(self, str_chords: str) -> list[int]:
        chords_pattern = re.compile(r"(.)(#|b)?(.+)?")
        chords_match = chords_pattern.match(str_chords)
        if not chords_match:
            return []

        # Plus 1 for sharps, minus 1 for flats
        root = (
            self.ROOT_NOTE[chords_match.group(1)]
            + {"#": 1, "b": -1, None: 0}[chords_match.group(2)]
        )

        target = chords_match.group(3)
        # Major
        if not target:
            return list(map(lambda x: x + root, [0, 4, 7]))
        # Other
        for regex, chords in self.chords.items():
            match = regex.fullmatch(target)
            if match:
                return list(map(lambda x: x + root, chords))
        return []

    def to_numbers(self, root: int, offsets: list[int]) -> list[int]:
        return [root + offset for offset in offsets]


if __name__ == "__main__":
    chords_case = ["C7", "Csus4", "C7sus4"]
    chords = Chords([])
    for str_chords in chords_case:
        print(chords.str_to_chords(str_chords))
