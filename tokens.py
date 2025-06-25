from enum import Enum

class TokenType(Enum):
    EOF = 'EOF'

    INT = 'INT'
    FLOAT = 'FLOAT'
    STRING = 'STRING'
    IDENTIFIER = 'IDENTIFIER'
    KEYWORD = 'KEYWORD'
    BOOL = 'BOOL'

    PLUS = 'PLUS'
    MINUS = 'MINUS'
    MULTIPLY = 'MULTIPLY'
    DIVIDE = 'DIVIDE'

    ASSIGN = 'ASSIGN'
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    LESS_THAN = 'LESS_THAN'
    LESS_THAN_OR_EQUAL = 'LESS_THAN_OR_EQUAL'
    GREATER_THAN = 'GREATER_THAN'
    GREATER_THAN_OR_EQUAL = 'GREATER_THAN_OR_EQUAL'

    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'

    INCREMENT = 'INCREMENT'
    DECREMENT = 'DECREMENT'

    LEFT_PAREN = 'LEFT_PAREN'
    RIGHT_PAREN = 'RIGHT_PAREN'
    LEFT_BRACE = 'LEFT_BRACE'
    RIGHT_BRACE = 'RIGHT_BRACE'
    LEFT_BRACKET = 'LEFT_BRACKET'
    RIGHT_BRACKET = 'RIGHT_BRACKET'
    COMMA = 'COMMA'
    DOT = 'DOT'
    COLON = 'COLON'

class Token:
    def __init__(self, type_, value, ln, col):
        self.type = type_
        self.value = value
        self.ln = ln
        self.col = col

    def __repr__(self):
        return str({
            'kind': 'Token',
            'type': self.type,
            'self.value': self.value,
            'line': self.ln,
            'column': self.col
        })

class TokenStream:
    def __init__(self, tokens, filepath):
        self.tokens = tokens
        self.pos = -1
        self.filepath = filepath

    @property
    def current(self):
        if self.pos < 0 or self.pos >= len(self.tokens):
            return Token(TokenType.EOF, '', -1, -1)
        return self.tokens[self.pos]

    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1

    def peek(self, distance=1):
        if self.pos + distance < len(self.tokens):
            return self.tokens[self.pos + distance]
        return Token(TokenType.EOF, '', -1, -1)

    def __repr__(self):
        return str({
            'kind': 'TokenStream',
            'tokens': [str(token) for token in self.tokens],
            'current_pos': self.pos,
            'filepath': self.filepath
        })