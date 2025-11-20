# src/symbolic_engine/operators.py

"""
Symbolic Computation Engine - Operators Module

This module provides a symbolic computation engine for mathematical operations,
symbolic manipulation, and algebraic expressions. It includes base classes and
concrete operator implementations for building and evaluating symbolic expressions.

Key Features:
- SymbolicExpression: Abstract base class for all symbolic entities.
- Symbol: Represents symbolic variables.
- SymbolicOperator: Abstract base class for operators.
- Concrete operators: Add, Subtract, Multiply, Divide, Power.

Usage:
    from src.symbolic_engine.operators import Symbol, Add, Multiply

    x = Symbol('x')
    y = Symbol('y')
    expr = Add(Multiply(x, 2), y)
    print(expr)  # Output: (x * 2) + y
    result = expr.evaluate(x=3, y=4)  # Output: 10.0
"""

from abc import ABC, abstractmethod
from typing import Union, List, Dict, Any
import numbers


class SymbolicExpression(ABC):
    """
    Abstract base class for all symbolic expressions.
    """

    @abstractmethod
    def evaluate(self, **kwargs: Dict[str, Union[float, int]]) -> Union[float, int, 'SymbolicExpression']:
        """
        Evaluate the expression. If all symbols are provided with numeric values,
        return a numeric result; otherwise, return a symbolic expression.

        Args:
            **kwargs: Dictionary of symbol names to numeric values.

        Returns:
            Numeric value or symbolic expression.
        """
        pass

    @abstractmethod
    def simplify(self) -> 'SymbolicExpression':
        """
        Simplify the expression symbolically.

        Returns:
            Simplified symbolic expression.
        """
        pass

    @abstractmethod
    def __str__(self) -> str:
        """
        String representation of the expression.

        Returns:
            String representation.
        """
        pass

    def __eq__(self, other: object) -> bool:
        """
        Check equality with another expression.

        Args:
            other: Another object to compare.

        Returns:
            True if equal, False otherwise.
        """
        return isinstance(other, SymbolicExpression) and str(self) == str(other)

    def __hash__(self) -> int:
        """
        Hash for the expression based on its string representation.

        Returns:
            Hash value.
        """
        return hash(str(self))


class Symbol(SymbolicExpression):
    """
    Represents a symbolic variable.
    """

    def __init__(self, name: str):
        """
        Initialize a symbol with a name.

        Args:
            name: Name of the symbol.
        """
        self.name = name

    def evaluate(self, **kwargs: Dict[str, Union[float, int]]) -> Union[float, int, 'Symbol']:
        """
        Evaluate the symbol. If a value is provided in kwargs, return it;
        otherwise, return the symbol itself.

        Args:
            **kwargs: Dictionary of symbol names to values.

        Returns:
            Numeric value or the symbol.
        """
        if self.name in kwargs:
            value = kwargs[self.name]
            if isinstance(value, (int, float)):
                return value
            else:
                raise ValueError(f"Value for symbol '{self.name}' must be numeric.")
        return self

    def simplify(self) -> 'Symbol':
        """
        Simplify the symbol (no-op for symbols).

        Returns:
            The symbol itself.
        """
        return self

    def __str__(self) -> str:
        """
        String representation of the symbol.

        Returns:
            Symbol name.
        """
        return self.name


class SymbolicOperator(SymbolicExpression):
    """
    Abstract base class for symbolic operators.
    """

    def __init__(self, *args: SymbolicExpression):
        """
        Initialize the operator with arguments.

        Args:
            *args: Symbolic expressions as operands.
        """
        if not args:
            raise ValueError("Operator must have at least one argument.")
        self.args = list(args)

    @abstractmethod
    def _op(self, *values: Union[float, int]) -> Union[float, int]:
        """
        Perform the operation on numeric values.

        Args:
            *values: Numeric operands.

        Returns:
            Numeric result.
        """
        pass

    def evaluate(self, **kwargs: Dict[str, Union[float, int]]) -> Union[float, int, 'SymbolicOperator']:
        """
        Evaluate the operator. If all arguments evaluate to numbers, compute the result;
        otherwise, return a new operator with evaluated arguments.

        Args:
            **kwargs: Dictionary of symbol names to values.

        Returns:
            Numeric result or symbolic operator.
        """
        evaluated_args = [arg.evaluate(**kwargs) for arg in self.args]
        if all(isinstance(arg, numbers.Number) for arg in evaluated_args):
            try:
                return self._op(*evaluated_args)
            except ZeroDivisionError:
                raise ZeroDivisionError(f"Division by zero in {self}")
        else:
            return self.__class__(*evaluated_args)

    def simplify(self) -> 'SymbolicExpression':
        """
        Simplify the operator by simplifying its arguments.
        (Basic implementation; can be extended for algebraic simplifications.)

        Returns:
            Simplified expression.
        """
        simplified_args = [arg.simplify() for arg in self.args]
        # Basic identity simplifications
        if isinstance(self, Add):
            # Remove zeros
            non_zero = [arg for arg in simplified_args if not (isinstance(arg, numbers.Number) and arg == 0)]
            if not non_zero:
                return 0
            elif len(non_zero) == 1:
                return non_zero[0]
            else:
                return Add(*non_zero)
        elif isinstance(self, Multiply):
            # Remove ones, handle zeros
            if any(isinstance(arg, numbers.Number) and arg == 0 for arg in simplified_args):
                return 0
            non_one = [arg for arg in simplified_args if not (isinstance(arg, numbers.Number) and arg == 1)]
            if not non_one:
                return 1
            elif len(non_one) == 1:
                return non_one[0]
            else:
                return Multiply(*non_one)
        elif isinstance(self, Power):
            base, exp = simplified_args
            if isinstance(exp, numbers.Number) and exp == 1:
                return base
            elif isinstance(exp, numbers.Number) and exp == 0:
                return 1
            elif isinstance(base, numbers.Number) and base == 1:
                return 1
        # Default: return with simplified args
        return self.__class__(*simplified_args)


class Add(SymbolicOperator):
    """
    Addition operator.
    """

    def _op(self, *values: Union[float, int]) -> Union[float, int]:
        """
        Perform addition.

        Args:
            *values: Numeric values to add.

        Returns:
            Sum of values.
        """
        return sum(values)

    def __str__(self) -> str:
        """
        String representation of addition.

        Returns:
            Formatted string.
        """
        return ' + '.join(f"({arg})" if isinstance(arg, SymbolicOperator) else str(arg) for arg in self.args)


class Subtract(SymbolicOperator):
    """
    Subtraction operator.
    """

    def __init__(self, left: SymbolicExpression, right: SymbolicExpression):
        """
        Initialize subtraction.

        Args:
            left: Left operand.
            right: Right operand.
        """
        super().__init__(left, right)

    def _op(self, left: Union[float, int], right: Union[float, int]) -> Union[float, int]:
        """
        Perform subtraction.

        Args:
            left: Left value.
            right: Right value.

        Returns:
            Difference.
        """
        return left - right

    def __str__(self) -> str:
        """
        String representation of subtraction.

        Returns:
            Formatted string.
        """
        left, right = self.args
        return f"({left}) - ({right})"


class Multiply(SymbolicOperator):
    """
    Multiplication operator.
    """

    def _op(self, *values: Union[float, int]) -> Union[float, int]:
        """
        Perform multiplication.

        Args:
            *values: Numeric values to multiply.

        Returns:
            Product of values.
        """
        result = 1
        for v in values:
            result *= v
        return result

    def __str__(self) -> str:
        """
        String representation of multiplication.

        Returns:
            Formatted string.
        """
        return ' * '.join(f"({arg})" if isinstance(arg, SymbolicOperator) else str(arg) for arg in self.args)


class Divide(SymbolicOperator):
    """
    Division operator.
    """

    def __init__(self, numerator: SymbolicExpression, denominator: SymbolicExpression):
        """
        Initialize division.

        Args:
            numerator: Numerator.
            denominator: Denominator.
        """
        super().__init__(numerator, denominator)

    def _op(self, numerator: Union[float, int], denominator: Union[float, int]) -> Union[float, int]:
        """
        Perform division.

        Args:
            numerator: Numerator value.
            denominator: Denominator value.

        Returns:
            Quotient.
        """
        if denominator == 0:
            raise ZeroDivisionError("Division by zero.")
        return numerator / denominator

    def __str__(self) -> str:
        """
        String representation of division.

        Returns:
            Formatted string.
        """
        numerator, denominator = self.args
        return f"({numerator}) / ({denominator})"


class Power(SymbolicOperator):
    """
    Power (exponentiation) operator.
    """

    def __init__(self, base: SymbolicExpression, exponent: SymbolicExpression):
        """
        Initialize power.

        Args:
            base: Base expression.
            exponent: Exponent expression.
        """
        super().__init__(base, exponent)

    def _op(self, base: Union[float, int], exponent: Union[float, int]) -> Union[float, int]:
        """
        Perform exponentiation.

        Args:
            base: Base value.
            exponent: Exponent value.

        Returns:
            Power result.
        """
        return base ** exponent

    def __str__(self) -> str:
        """
        String representation of power.

        Returns:
            Formatted string.
        """
        base, exponent = self.args
        return f"({base})^({exponent})"
