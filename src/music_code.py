from enum import IntEnum
import re


class RootNote(IntEnum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11


class Code:
    def __init__(self, code_order: list[str]) -> None:
        pass

    def str_to_code(self, str_code: str) -> list[int]:
        pattern = re.compile("([C | D | E | F | G | A | B])")
        match = pattern.match(str_code)
        if match == None:
            return []
        print(match.group(0))
        # root = RootNote[match.group(0)].value

        # if str_code[1:] == "":
        #     # Major
        #     return self.major(root)
        return []

    def major(self, root: int):
        return [root, (root + 4) % 12, (root + 7) % 12]


if __name__ == "__main__":
    print(Code([]).str_to_code("A"))
