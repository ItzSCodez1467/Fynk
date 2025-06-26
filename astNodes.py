import json

class ASTNode:
    def to_dict(self):
        result = {"kind": self.__class__.__name__}
        for attr, value in self.__dict__.items():
            result[attr] = self._serialize(value)
        return result

    def _serialize(self, value):
        if isinstance(value, ASTNode):
            return value.to_dict()
        elif isinstance(value, list):
            return [self._serialize(v) for v in value]
        else:
            return value

    def __repr__(self):
        return json.dumps(self.to_dict(), indent=2)

class Program(ASTNode):
    def __init__(self, body):
        self.body = body

class IntegerLiteral(ASTNode):
    def __init__(self, value, ln, col):
        self.ln = ln
        self.col = col
        self.value = value

class FloatLiteral(ASTNode):
    def __init__(self, value, ln, col):
        self.ln = ln
        self.col = col
        self.value = value

class StringLiteral(ASTNode):
    def __init__(self, value, ln, col):
        self.ln = ln
        self.col = col
        self.value = value

class IdentifierLiteral(ASTNode):
    def __init__(self, name, ln, col):
        self.ln = ln
        self.col = col
        self.name = name

class KeywordLiteral(ASTNode):
    def __init__(self, keyword, ln, col):
        self.ln = ln
        self.col = col
        self.keyword = keyword

class BooleanLiteral(ASTNode):
    def __init__(self, value, ln, col):
        self.ln = ln
        self.col = col
        self.value = value

class BinaryExpression(ASTNode):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class AssignmentExpression(ASTNode):
    def __init__(self, target, value, ln, col):
        self.ln = ln
        self.col = col
        self.target = target
        self.value = value

class EqualityExpression(ASTNode):
    def __init__(self, left, right, ln, col):
        self.ln = ln
        self.col = col
        self.left = left
        self.right = right

class InequalityExpression(ASTNode):
    def __init__(self, left, right, ln, col):
        self.ln = ln
        self.col = col
        self.left = left
        self.right = right

class LogicalExpression(ASTNode):
    def __init__(self, left, operator, right, ln, col):
        self.ln = ln
        self.col = col
        self.left = left
        self.operator = operator
        self.right = right

class IncrementExpression(ASTNode):
    def __init__(self, target, ln, col):
        self.ln = ln
        self.col = col
        self.target = target

class DecrementExpression(ASTNode):
    def __init__(self, target, ln, col):
        self.ln = ln
        self.col = col
        self.target = target

class Delimiter(ASTNode):
    def __init__(self, value, ln, col):
        self.ln = ln
        self.col = col
        self.value = value