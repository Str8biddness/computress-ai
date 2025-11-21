# src/integration/uscl_interface.py
"""
USCL Interface Module

This module provides an interface for Unified Symbolic Consciousness Language (USCL).
It handles parsing, generating, and interpreting USCL expressions for symbolic
communication and reasoning.

Key Features:
- USCLInterface: Main interface for USCL operations.
- Parsing and generation of USCL expressions.
- Integration with symbolic engine.

Usage: from src.integration.uscl_interface import USCLInterface

interface = USCLInterface()
parsed = interface.parse_expression("consciousness.level = 0.8")
generated = interface.generate_expression({"consciousness": {"level": 0.8}})
"""

import re
from typing import Dict, Any, Optional, Union
import logging

from ..symbolic_engine.expression_eval import Parser, ExpressionEvaluator

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class USCLInterface:
    """Interface for Unified Symbolic Consciousness Language."""

    def __init__(self):
        self.parser = Parser()
        self.evaluator = ExpressionEvaluator()

    def parse_expression(self, expression: str) -> Optional[Dict[str, Any]]:
        """
        Parse a USCL expression into a dictionary.

        Args:
            expression: USCL expression string.

        Returns:
            Parsed dictionary or None if failed.
        """
        try:
            # Simple parsing: assume key = value or key.subkey = value
            parts = expression.split('=')
            if len(parts) != 2:
                raise ValueError("Invalid expression format")
            key_path = parts[0].strip().split('.')
            value_str = parts[1].strip()
            # Try to evaluate value
            value = self.evaluator.evaluate(self.parser.parse(value_str))
            result = {}
            current = result
            for key in key_path[:-1]:
                current[key] = {}
                current = current[key]
            current[key_path[-1]] = value
            return result
        except Exception as e:
            logger.error(f"Failed to parse USCL expression '{expression}': {e}")
            return None

    def generate_expression(self, data: Dict[str, Any]) -> str:
        """
        Generate a USCL expression from a dictionary.

        Args:
            data: Data dictionary.

        Returns:
            USCL expression string.
        """
        def flatten_dict(d, prefix=''):
            items = []
            for k, v in d.items():
                new_key = f"{prefix}.{k}" if prefix else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        flat = flatten_dict(data)
        expressions = [f"{k} = {v}" for k, v in flat.items()]
        return '; '.join(expressions)

    def evaluate_expression(self, expression: str, context: Dict[str, Union[float, int]] = None) -> Any:
        """
        Evaluate a USCL expression with context.

        Args:
            expression: Expression to evaluate.
            context: Variable context.

        Returns:
            Evaluated result.
        """
        context = context or {}
        try:
            parsed = self.parser.parse(expression)
            return self.evaluator.evaluate(parsed, **context)
        except Exception as e:
            logger.error(f"Failed to evaluate expression '{expression}': {e}")
            return None

    def translate_to_symbolic(self, uscl_expr: str) -> Optional[str]:
        """
        Translate USCL to symbolic expression.

        Args:
            uscl_expr: USCL expression.

        Returns:
            Symbolic string or None.
        """
        parsed = self.parse_expression(uscl_expr)
        if parsed:
            return self.generate_expression(parsed)
        return None
