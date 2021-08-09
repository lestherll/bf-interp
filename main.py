from dataclasses import dataclass


@dataclass
class Token:
    name: str
    symbol: str

TOKENS = {
    "+":          Token("INC", r"+"),
    "-":          Token("DEC", r"-"),
    "<":   Token("SHIFT_LEFT", r"<"),
    ">":  Token("SHIFT_RIGHT", r">"),
    ".":       Token("OUTPUT", r"."),
    ",":        Token("INPUT", r","),
    "[":    Token("OPEN_LOOP", r"["),
    "]":   Token("CLOSE_LOOP", r"]"),
}


class Lexer:

    def __init__(self, program: str):
        self.program = program

    def result(self):
        # cell_count = max(1, self.program.count(">"))
        tokens = [0 for _ in range(len(self.program))]
        for i, char in enumerate(self.program):
            tokens[i] = TOKENS[char]
        return tokens

class Interpreter:
    ...


lexer = Lexer(">>[<<+>>],.")
for i in lexer.result():
    print(i)
