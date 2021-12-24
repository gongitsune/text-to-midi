import re


class Code:
    CODES = {
        re.compile(r"m"): [0, 3, 7],
        re.compile(r"sus4"): [0, 5, 7],
        re.compile(r"\(b5\)|\(-5\)"): [0, 4, 6],
        re.compile(r"\(#5\)|\(\+5\)|aug"): [0, 4, 8],
    }
    ROOT_NOTE = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}

    def __init__(self, code_order: list[str]) -> None:
        pass

    def str_to_code(self, str_code: str) -> list[int]:
        code_pattern = re.compile(r"(.)(#|b)?(.+)?")
        code_match = code_pattern.match(str_code)
        if not code_match:
            return []

        # Plus 1 for sharps, minus 1 for flats
        root = (
            self.ROOT_NOTE[code_match.group(1)]
            + {"#": 1, "b": -1, None: 0}[code_match.group(2)]
        )

        target = code_match.group(3)
        # Major
        if not target:
            return list(map(lambda x: x + root, [0, 4, 7]))
        # Other
        for regex, code in self.CODES.items():
            match = regex.match(target)
            if match:
                return list(map(lambda x: x + root, code))
        return []

    def to_numbers(self, root: int, offsets: list[int]) -> list[int]:
        return [root + offset for offset in offsets]


if __name__ == "__main__":
    print(Code([]).str_to_code("C(-5)"))
    print(Code([]).str_to_code("C(b5)"))
