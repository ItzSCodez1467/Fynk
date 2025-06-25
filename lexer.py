from errors import error
from tokens import Token, TokenType, TokenStream


class Lexer:
    def __init__(self, fp):
        self.fp = fp

        with open(fp, 'r') as f:
            self.source = f.read()
        self.pos = -1
        self.ln = 0
        self.col = 0

        self.advance()

    @property
    def current(self): return self.peek(0)

    def advance(self):
        if self.current == '\n':
            self.ln += 1
            self.col = 0
        else: self.col += 1
        self.pos += 1

    def peek(self, distance=1):
        if self.pos + distance < len(self.source): return self.source[self.pos + distance]
        return None

    def lex(self):
        # TODO: Lex a single token
        return None

    def tokenize(self):
        # TODO: Call lex() repeatedly until EOF and return TokenStream
        return TokenStream(self.lex(), self.fp)