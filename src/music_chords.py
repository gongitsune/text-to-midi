import re

from error import ChordException


class Chord:
    CHORD_DIC = {
        re.compile(r"m"): [0, 3, 7],
        re.compile(r"sus4"): [0, 5, 7],
        re.compile(r"\(b5\)|\(-5\)"): [0, 4, 6],
        re.compile(r"\(#5\)|\(\\+5\)|aug"): [0, 4, 8],
        re.compile(r"6"): [0, 4, 7, 9],
        re.compile(r"7"): [0, 4, 7, 10],
        re.compile(r"M7"): [0, 4, 7, 11],
        re.compile(r"\(add9\)|add9"): [0, 2, 4, 7],
        re.compile(r"9"): [0, 2, 4, 7, 10],
        re.compile(r"\(-9\)"): [0, 1, 4, 7],
        re.compile(r"\(\+9\)"): [0, 3, 4, 7],
        re.compile(r"dim"): [0, 3, 6],
        re.compile(r"11"): [0, 4, 5, 7, 10],
        re.compile(r"13"): [0, 4, 7, 9, 10],
        # Combination
        re.compile(r"7sus4"): [0, 5, 7, 10],
        re.compile(r"6\(add9\)"): [0, 2, 4, 7, 9],
        re.compile(r"m6"): [0, 3, 7, 9],
        re.compile(r"m6\((add9|9)\)"): [0, 2, 3, 7, 9],
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
        re.compile(r"7\(\+5\)"): [0, 4, 8, 10],
        re.compile(r"7\(-9\)"): [0, 1, 4, 7, 10],
        re.compile(r"7\(\+9\)"): [0, 3, 4, 7, 10],
        re.compile(r"13\(-9\)"): [0, 1, 4, 7, 9, 10],
    }
    ROOT_NOTE = {
        "C": 0,
        "C#": 1,
        "D": 2,
        "D#": 3,
        "E": 4,
        "F": 5,
        "F#": 6,
        "G": 7,
        "G#": 8,
        "A": 9,
        "A#": 10,
        "B": 11,
    }

    def __init__(self, chord: str) -> None:
        """Chord analysis

        Args:
            chord (str): Chord to analysis
        """
        self.chord = chord

    def components(self) -> list[str]:
        """Returns the single notes that make up the chord

        Returns:
            list[str]: Components
        """
        return [
            [note for note in self.ROOT_NOTE.items() if note[1] == num][0][0]
            for num in self.note_numbers()
        ]

    def note_numbers(self) -> list[int]:
        """Returns the midi note numbers that make up the code

        Raises:
            ChordException: Chord exception

        Returns:
            list[int]: Midi note numbers
        """
        chords_pattern = re.compile(r"(.)(#|b)?(.+)?")
        chords_match = chords_pattern.match(self.chord)
        if not chords_match:
            return []

        # Plus 1 for sharps, minus 1 for flats
        root = (
            self.ROOT_NOTE[chords_match.group(1)]
            + {"#": 1, "b": -1, None: 0}[chords_match.group(2)]  # noqa
        )

        target = chords_match.group(3)
        # Major
        if not target:
            return self.normalize(root, [0, 4, 7])
        # Other
        for regex, chords in self.CHORD_DIC.items():
            match = regex.fullmatch(target)
            if match:
                return self.normalize(root, chords)
        raise ChordException(f"Unknown chord: {target}")

    def normalize(self, root: int, offsets: list[int]) -> list[int]:
        """Generate a note number based on the root and normalize it from 0 to 11

        Args:
            root (int): Root midi note number
            offsets (list[int]): Chord based on C

        Returns:
            list[int]: Chord
        """
        return [(root + offset) % 12 for offset in offsets]


if __name__ == "__main__":
    chords_case = ["C7", "Csus4", "C7sus4"]
    print(Chord("B7(+9)").note_numbers())
