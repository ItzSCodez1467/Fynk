from astNodes import *
from errors import error
from tokens import TokenType, TokenStream

class Parser:
    def __init__(self, tokens: TokenStream):
        self.tokens = tokens

    @property
    def current(self):
        return self.tokens.current

    def consume(self, expected_type: TokenType):
        if self.current.type == expected_type:
            self.tokens.advance()
        else:
            self.err(f'ParserError: Expected {expected_type} but got {self.current}')

    def err(self, msg, ln=None):
        error(fp=self.tokens.filepath,
              ln=ln if ln is not None else self.current.ln,
              msg=msg)

    def factor(self):
        if self.current.type == TokenType.INT:
            node = self.current
            self.consume(TokenType.INT)
            return IntegerLiteral(node, node.ln, node.col)
        if self.current.type == TokenType.FLOAT:
            node = self.current
            self.consume(TokenType.FLOAT)
            return FloatLiteral(node, node.ln, node.col)
        if self.current.type == TokenType.STRING:
            node = self.current
            self.consume(TokenType.STRING)
            return StringLiteral(node, node.ln, node.col)
        if self.current.type == TokenType.BOOL:
            node = self.current
            self.consume(TokenType.BOOL)
            return BooleanLiteral(node, node.ln, node.col)
        if self.current.type == TokenType.IDENTIFIER:
            node = self.current
            self.consume(TokenType.IDENTIFIER)
            return Identifier(node, node.ln, node.col)
        if self.current.type == TokenType.LEFT_PAREN:
            self.consume(TokenType.LEFT_PAREN)
            node = self.expr()
            self.consume(TokenType.RIGHT_PAREN)
            return node
        if self.current == TokenType.INCREMENT or self.tokens.peek() == TokenType.INCREMENT:
            return self.increment()
        if self.current == TokenType.DECREMENT or self.tokens.peek() == TokenType.DECREMENT:
            return self.decrement()


        self.err(f'ParserError: Expected <INT | FLOAT | STRING | BOOL | IDENTIFIER> but got {self.current}')
        return None # For static code analysis

    def leftRecursionMethod(self, func, ops):
        lft = func()

        while self.current.type in ops:
            op = self.current
            self.consume(self.current.type)
            rgt = func()

            lft = BinaryExpression(lft, op, rgt, lft.ln, lft.col)

        return lft

    def term(self):
        return self.leftRecursionMethod(self.factor, [TokenType.MULTIPLY, TokenType.DIVIDE])

    def expr(self):
        return self.leftRecursionMethod(self.term, [TokenType.PLUS, TokenType.MINUS])

    def expr_stmt(self):
        main_node = self.expr()
        self.consume(TokenType.SEMICOLON)
        return main_node

    def incDecCmn(self, op, node):
        if self.current.type == op:
            self.consume(op)
            _id = self.current
            self.consume(TokenType.IDENTIFIER)
        else:
            _id = self.current
            self.consume(TokenType.IDENTIFIER)
            self.consume(op)

        return node(_id, _id.ln, _id.col)

    def increment(self):
        return self.incDecCmn(TokenType.INCREMENT, IncrementExpression)

    def decrement(self):
        return self.incDecCmn(TokenType.DECREMENT, DecrementExpression)

    def increment_stmt(self):
        main_node = self.increment()
        self.consume(TokenType.SEMICOLON)
        return main_node

    def decrement_stmt(self):
        main_node = self.decrement()
        self.consume(TokenType.SEMICOLON)
        return main_node

    def assignment(self):
        id_ = Identifier(self.current.value, self.current.ln, self.current.col)
        self.consume(TokenType.IDENTIFIER)
        self.consume(TokenType.ASSIGN)
        val = self.expr()
        return AssignmentExpression(id_, val, id_.ln, id_.col)

    def assignment_stmt(self):
        main_node = self.assignment()
        self.consume(TokenType.SEMICOLON)
        return main_node

    def eq(self):
        lft = self.expr()
        self.consume(TokenType.EQUAL)
        rgt = self.expr()
        return EqualityExpression(lft, rgt, lft.ln, lft.col)

    def eq_stmt(self):
        main_node = self.eq()
        self.consume(TokenType.SEMICOLON)
        return main_node

    def ieq(self):
        lft = self.expr()
        self.consume(TokenType.NOT_EQUAL)
        rgt = self.expr()
        return InequalityExpression(lft, rgt, lft.ln, lft.col)

    def ieq_stmt(self):
        main_node = self.ieq()
        self.consume(TokenType.SEMICOLON)
        return main_node

    def parse_program(self):
        stmts = []
        while self.current.type != TokenType.EOF:
            stmts.append(self.ieq_stmt())
        return Program(stmts)