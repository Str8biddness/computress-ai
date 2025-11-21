# src/symbolic_engine/expression_eval.py

"""
Expression Evaluation Engine Module

This module provides an expression evaluation engine for parsing, evaluating,
and simplifying symbolic expressions. It includes a parser for string expressions,
an evaluator for symbolic trees, and methods for building and manipulating
expression trees.

Key Features:
- Parser: Parses string expressions into symbolic expression trees.
- ExpressionEvaluator: Evaluates and simplifies expressions.
- Support for basic arithmetic operators (+, -, *, /, ^) and symbols.
- Handles parentheses and operator precedence.

Usage:
    from src.symbolic_engine.expression_eval import Parser, ExpressionEvaluator

    parser = Parser()
    expr = parser.parse("x + 2 * y")
    evaluator = ExpressionEvaluator()
    result = evaluator.evaluate(expr, x=3, y=4)  # Output: 11
    simplified = evaluator.simplify(expr)  # Simplify symbolically
"""

import re
from typing import Union, Dict, Any, List
from .operators import Symbol, SymbolicExpression, Add, Subtract, Multiply, Divide, Power


class Parser:
    """
    Parser for converting string expressions into symbolic expression trees.
    Supports basic arithmetic: +, -, *, /, ^, and parentheses.
    """

    def __init__(self):
        self.tokens = []
        self.pos = 0

    def tokenize(self, expression: str) -> List[str]:
        """
        Tokenize the input expression string.

        Args:
            expression: String expression to tokenize.

        Returns:
            List of tokens.
        """
        # Regex for tokens: numbers, symbols (letters), operators, parentheses
        token_pattern = r'(\d+\.?\d*|[a-zA-Z_][a-zA-Z0-9_]*|[+\-*/^()])'
        self.tokens = re.findall(token_pattern, expression.replace(' ', ''))
        self.pos = 0
        return self.tokens

    def parse(self, expression: str) -> SymbolicExpression:
        """
        Parse the string expression into a symbolic expression tree.

        Args:
            expression: String expression.

        Returns:
            SymbolicExpression tree.
        """
        self.tokenize(expression)
        result = self.expression()
        if self.pos < len(self.tokens):
            raise ValueError(f"Unexpected token: {self.tokens[self.pos]}")
        return result

    def expression(self) -> SymbolicExpression:
        """
        Parse addition and subtraction (lowest precedence).

        Returns:
            SymbolicExpression.
        """
        left = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('+', '-'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.term()
            if op == '+':
                left = Add(left, right)
            elif op == '-':
                left = Subtract(left, right)
        return left

    def term(self) -> SymbolicExpression:
        """
        Parse multiplication and division.

        Returns:
            SymbolicExpression.
        """
        left = self.power()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in ('*', '/'):
            op = self.tokens[self.pos]
            self.pos += 1
            right = self.power()
            if op == '*':
                left = Multiply(left, right)
            elif op == '/':
                left = Divide(left, right)
        return left

    def power(self) -> SymbolicExpression:
        """
        Parse exponentiation.

        Returns:
            SymbolicExpression.
        """
        left = self.factor()
        if self.pos < len(self.tokens) and self.tokens[self.pos] == '^':
            self.pos += 1
            right = self.power()  # Right-associative
            left = Power(left, right)
        return left

    def factor(self) -> SymbolicExpression:
        """
        Parse factors: numbers, symbols, or parenthesized expressions.

        Returns:
            SymbolicExpression.
        """
        token = self.tokens[self.pos]
        self.pos += 1
        if token == '(':
            expr = self.expression()
            if self.pos >= len(self.tokens) or self.tokens[self.pos] != ')':
                raise ValueError("Mismatched parentheses")
            self.pos += 1
            return expr
        elif token.isdigit() or '.' in token:
            return float(token) if '.' in token else int(token)
        elif token.isalpha():
            return Symbol(token)
        else:
            raise ValueError(f"Invalid token: {token}")


class ExpressionEvaluator:
    """
    Evaluator for symbolic expressions, including evaluation with values and simplification.
    """

    def __init__(self):
        pass

    def evaluate(self, expr: SymbolicExpression, **kwargs: Dict[str, Union[float, int]]) -> Union[float, int, SymbolicExpression]:
        """
        Evaluate the symbolic expression with given symbol values.

        Args:
            expr: SymbolicExpression to evaluate.
            **kwargs: Symbol names to numeric values.

        Returns:
            Numeric result or symbolic expression if not fully evaluable.
        """
        return expr.evaluate(**kwargs)

    def simplify(self, expr: SymbolicExpression) -> SymbolicExpression:
        """
        Simplify the symbolic expression.

        Args:
            expr: SymbolicExpression to simplify.

        Returns:
            Simplified SymbolicExpression.
        """
        return expr.simplify()

    def build_tree(self, expression: str) -> SymbolicExpression:
        """
        Build an expression tree from a string (convenience method using Parser).

        Args:
            expression: String expression.

        Returns:
            SymbolicExpression tree.
        """
        parser = Parser()
        return parser.parse(expression)

    def to_string(self, expr: SymbolicExpression) -> str:
        """
        Convert expression tree back to string.

        Args:
            expr: SymbolicExpression.

        Returns:
            String representation.
        """
        return str(expr)

    def substitute(self, expr: SymbolicExpression, substitutions: Dict[str, Union[SymbolicExpression, float, int]]) -> SymbolicExpression:
        """
        Substitute symbols in the expression with other expressions or values.

        Args:
            expr: Original expression.
            substitutions: Dict of symbol names to replacements.

        Returns:
            Substituted expression.
        """
        if isinstance(expr, Symbol) and expr.name in substitutions:
            return substitutions[expr.name]
        elif isinstance(expr, SymbolicExpression) and hasattr(expr, 'args'):
            new_args = [self.substitute(arg, substitutions) for arg in expr.args]
            return expr.__class__(*new_args)
        else:
            return expr
