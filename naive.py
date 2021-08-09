import itertools
import sys
from typing import Tuple, List


# CELL_COUNT = 30_00000
TOKENS = {
    "+": "INC",
    "-": "DEC",
    "<": "L_SHIFT",
    ">": "R_SHIFT",
    ".": "OUTPUT",
    ",": "INPUT",
    "[": "OPEN_LOOP",
    "]": "CLOSE_LOOP"
}

UNARY_TOKENS = {
    sym: token for sym, token in zip(map("".join, itertools.product(["0", "1"], repeat=3)), TOKENS.values())
}

BF_TO_UN = {
    sym: token for sym, token in zip(TOKENS.keys(), UNARY_TOKENS.keys())
}

def balanced(program: str) -> bool:
    stack = []
    for i, token in enumerate(program):
        if token == "OPEN_LOOP":
            stack.append("OPEN_LOOP")
        elif token == "CLOSE_LOOP":
            if not stack:
                return False

            curr_token = stack.pop()
            if token == "CLOSE_LOOP" and curr_token != "OPEN_LOOP":
                return False

    return not stack

class Interpreter:

    def __init__(self, program: str, token_map: dict[str, str] = TOKENS) -> None:
        self.program: str = program
        self.token_map = token_map
        # self.cells: List[int] = [0 for _ in range(CELL_COUNT)]
        # self.cells: List[int] = [0 for _ in range(program.count(">")+1)]
        self.cells = [0] * self.lex().count("R_SHIFT")
        self.pointer: int = 0
        self.token_map = token_map
        # self.interpret()

    def bf_to_unary(self, save_file=None):
        result = []
        for i, sym in enumerate(self.program):
            result.append(BF_TO_UN.get(sym, ""))

        if save_file is None:
            return result
        else:
            with open(save_file, "w") as unary_file:
                unary_file.write("".join(result))

    def current(self) -> int:
        return self.cells[self.pointer]

    def lex(self) -> List[str]:
        # return [TOKENS.get(char, None) for i, char in enumerate(self.program)]
        tokens = []
        # for i, char in enumerate(self.program):
        #     if char in self.token_map:
        #         tokens.append(self.token_map[char])
        for c in range(0, len(self.program), 3):
            char = "".join(map(str, (self.program[c], self.program[c+1], self.program[c+2])))
            if char in self.token_map:
                tokens.append(self.token_map[char])

        return tokens

    def syntax(self) -> bool:
        return balanced(self.lex())

    def interpret(self) -> None:
        if not self.syntax():
            raise Exception("Syntax Error")
        # else:
        #     print("syntax ok")

        i: int = 0
        lexed: List[str] = self.lex()
        while i <= len(lexed) - 1:
            token: str = lexed[i]
            if token == "INC":
                self.increment()
            elif token == "DEC":
                if self.current() > 0:
                    self.decrement()
            elif token == "R_SHIFT":
                self.shift_right()
            elif token == "L_SHIFT":
                self.shift_left()
            elif token == "OUTPUT":
                self.output()
            elif token == "INPUT":
                self.input_()
            elif token == "OPEN_LOOP":
                if self.cells[self.pointer] == 0:
                    open_braces = 1
                    while open_braces > 0:
                        i += 1
                        if lexed[i] == "OPEN_LOOP":
                            open_braces += 1
                        elif lexed[i] == "CLOSE_LOOP":
                            open_braces -= 1
            elif token == "CLOSE_LOOP":
                open_braces = 1
                while open_braces > 0:
                    i -= 1
                    if lexed[i] == "OPEN_LOOP":
                        open_braces -= 1
                    elif lexed[i] == "CLOSE_LOOP":
                        open_braces += 1
                i -= 1

            i += 1

    def increment(self) -> None:
        self.cells[self.pointer] += 1

    def decrement(self) -> None:
        self.cells[self.pointer] -= 1

    def shift_left(self) -> None:
        if self.pointer <= 0:
            print("Error: cell number is less than 0")
        else:
            self.pointer -= 1

    def shift_right(self) -> None:
        self.pointer += 1

    def output(self) -> None:
        print(chr(self.cells[self.pointer]), end="")

    def input_(self) -> None:
        new_val: str = input("\n")
        self.cells[self.pointer] = ord(new_val)


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as file:
            program = file.read()
        # print(program)
        interp = Interpreter(program=program, token_map=UNARY_TOKENS)
        print(interp.lex())
        interp.interpret()
    else:
        print("Usage:", sys.argv[0], "filename")


if __name__ == "__main__":
    main()
    print(UNARY_TOKENS)