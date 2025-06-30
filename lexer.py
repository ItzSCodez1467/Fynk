from errors import error
from keywords import keywords
from tokens import Token, TokenType, TokenStream
from parser import Parser


class Lexer:
    def __init__(self, fp):
        self.fp = fp

        try:
            with open(fp, 'r') as f:
                self.source = f.read()
        except Exception as e:
            error(fp, 0, f"FileError: {e}", "Unable to read source file.")

        self.pos = -1
        self.ln = 1
        self.col = 0
        self.advance()

    @property
    def current(self):
        return self.peek(0)

    def advance(self):
        self.pos += 1
        if self.pos < len(self.source):
            ch = self.source[self.pos]
            if ch == '\n':
                self.ln += 1
                self.col = 0
            else:
                self.col += 1

    def peek(self, distance=1):
        if self.pos + distance < len(self.source):
            return self.source[self.pos + distance]
        return None

    def skipIrrelevant(self):
        while self.current is not None:
            if self.current == '#':
                while self.current is not None and self.current != '\n':
                    self.advance()
            elif self.current.isspace() or self.current in ['\r', '\t', '\n']:
                self.advance()
            else:
                break

    def makeNumber(self):
        numStr = ''
        hasDot = False
        startLn, startCol = self.ln, self.col

        while self.current is not None and (self.current.isdigit() or self.current == '.'):
            if self.current == '.':
                if hasDot:
                    error(self.fp, self.ln, f"LexerError: Unexpected '.'", "Multiple decimal points in number.")
                hasDot = True

            numStr += self.current
            self.advance()

        if hasDot:
            return Token(TokenType.FLOAT, numStr, startLn, startCol)
        return Token(TokenType.INT, numStr, startLn, startCol)

    def makeString(self):
        startLn, startCol = self.ln, self.col
        quote = self.current
        strContent = ''
        self.advance()

        while self.current is not None and self.current != quote:
            if self.current == '\\':  # escape handling
                self.advance()
                if self.current is None:
                    break
                escape_char = {
                    'n': '\n',
                    't': '\t',
                    '"': '"',
                    "'": "'",
                    '\\': '\\'
                }.get(self.current, self.current)
                strContent += escape_char
            else:
                if ord(self.current) < 32 and self.current != '\n':
                    error(self.fp, self.ln, f"LexerError: Unprintable character in string", "Control characters must be escaped.")
                strContent += self.current
            self.advance()

        if self.current == quote:
            self.advance()
            return Token(TokenType.STRING, strContent, startLn, startCol)
        oppQuote = '"' if quote == "'" else "'"
        error(self.fp, startLn, f"LexerError: Unclosed string literal starting with {oppQuote}{quote}{oppQuote}",
              "Check your syntax.")
        return None  # static checker peace

    def makeIdentifierKW(self):
        startLn, startCol = self.ln, self.col
        id_ = ''

        while self.current is not None and (self.current.isalnum() or self.current == '_'):
            id_ += self.current
            self.advance()

        if id_ == 'True': return Token(TokenType.BOOL, True, startLn, startCol)
        elif id_ == 'False': return Token(TokenType.BOOL, False, startLn, startCol)
        else:
            if id_ in keywords:
                return Token(TokenType.KEYWORD, id_, startLn, startCol)
            return Token(TokenType.IDENTIFIER, id_, startLn, startCol)

    def lex(self):
        self.skipIrrelevant()

        # EOF
        if self.current is None:
            return Token(TokenType.EOF, '', self.ln, self.col)

        # INT / FLOAT
        if self.current.isdigit() or (self.current == '.' and self.peek() and self.peek().isdigit()):
            return self.makeNumber()

        # STRING
        if self.current in ('"', "'"):
            return self.makeString()

        # IDENTIFIER / KEYWORD / BOOL
        if self.current.isalpha() or self.current == '_':
            return self.makeIdentifierKW()

        # PLUS
        if self.current == '+' and self.peek() != '+':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.PLUS, '+', startLn, startCol)

        # MINUS
        if self.current == '-' and self.peek() != '-':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.MINUS, '-', startLn, startCol)

        # MULTIPLY
        if self.current == '*':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.MULTIPLY, '*', startLn, startCol)

        # DIVIDE
        if self.current == '/':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.DIVIDE, '/', startLn, startCol)

        # ASSIGNMENT
        if self.current == '=' and self.peek() != '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.ASSIGN, '=', startLn, startCol)

        # EQUALITY
        if self.current == '=' and self.peek() == '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            self.advance()
            return Token(TokenType.EQUAL, '==', startLn, startCol)

        # INEQUALITY
        if self.current == '!' and self.peek() == '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            self.advance()
            return Token(TokenType.NOT_EQUAL, '!=', startLn, startCol)

        # LESS THAN
        if self.current == '<' and self.peek() != '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.LESS_THAN, '<', startLn, startCol)

        # LESS THAN OR EQUAL TO
        if self.current == '<' and self.peek() == '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            self.advance()
            return Token(TokenType.LESS_THAN_OR_EQUAL, '<=', startLn, startCol)

        # GREATER THAN
        if self.current == '>' and self.peek() != '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.GREATER_THAN, '>', startLn, startCol)

        # GREATER THAN OR EQUAL TO
        if self.current == '>' and self.peek() == '=':
            startLn, startCol = self.ln, self.col
            self.advance()
            self.advance()
            return Token(TokenType.GREATER_THAN_OR_EQUAL, '>=', startLn, startCol)

        # AND
        if self.current == '&':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.AND, '&', startLn, startCol)

        # OR
        if self.current == '|':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.OR, '|', startLn, startCol)

        # NOT
        if self.current == '!':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.NOT, '!', startLn, startCol)

        # INCREMENT
        if self.current == '+' and self.peek() == '+':
            startLn, startCol = self.ln, self.col
            self.advance()
            self.advance()
            return Token(TokenType.INCREMENT, '++', startLn, startCol)

        # DECREMENT
        if self.current == '-' and self.peek() == '-':
            startLn, startCol = self.ln, self.col
            self.advance()
            self.advance()
            return Token(TokenType.DECREMENT, '-', startLn, startCol)

        # LEFT PAREN
        if self.current == '(':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.LEFT_PAREN, '(', startLn, startCol)

        # RIGHT PAREN
        if self.current == ')':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.RIGHT_PAREN, ')', startLn, startCol)

        # LEFT BRACE
        if self.current == '{':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.LEFT_BRACE, '{', startLn, startCol)

        # RIGHT BRACE
        if self.current == '}':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.RIGHT_BRACE, '}', startLn, startCol)

        # LEFT BRACKET
        if self.current == '[':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.LEFT_BRACKET, '[', startLn, startCol)

        # RIGHT BRACKET
        if self.current == ']':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.RIGHT_BRACKET, ']', startLn, startCol)

        # COMMA
        if self.current == ',':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.COMMA, ',', startLn, startCol)

        # DOT
        if self.current == '.':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.DOT, '.', startLn, startCol)

        # COLON
        if self.current == ':':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.COLON, ':', startLn, startCol)

        # SEMICOLON
        if self.current == ';':
            startLn, startCol = self.ln, self.col
            self.advance()
            return Token(TokenType.SEMICOLON, ';', startLn, startCol)

        # Unexpected character
        error(self.fp, self.ln, f"LexerError: Unexpected character '{self.current}'", "Check your syntax.")
        return None

    def tokenize(self):
        tokens = []
        while True:
            token = self.lex()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return TokenStream(tokens, self.fp)


if __name__ == "__main__":
    lexer = Lexer('example.fynk')
    token_stream = lexer.tokenize()
    print(token_stream)
    parser = Parser(token_stream)
    program = parser.parse_program()

    print(program) # AST