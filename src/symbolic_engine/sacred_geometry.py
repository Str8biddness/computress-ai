# src/symbolic_engine/sacred_geometry.py

"""
Sacred Geometry Mathematics Module

This module provides classes and methods for sacred geometry computations,
including golden ratio, Fibonacci sequences, Platonic solids, sacred angles,
geometric patterns, and mathematical constants relevant to consciousness modeling.
It integrates with the symbolic computation engine for symbolic manipulations.

Key Features:
- GoldenRatio: Class for golden ratio calculations.
- Fibonacci: Class for generating Fibonacci sequences.
- PlatonicSolid: Base class for Platonic solids with subclasses for each.
- SacredAngles: Class for sacred angles and related calculations.
- GeometricPatterns: Class for generating geometric patterns.
- Constants: Mathematical constants for consciousness modeling.

Usage:
    from src.symbolic_engine.sacred_geometry import GoldenRatio, Fibonacci

    phi = GoldenRatio()
    print(phi.value)  # Output: 1.618033988749895

    fib = Fibonacci()
    seq = fib.generate(10)  # Generate first 10 Fibonacci numbers
    print(seq)  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
"""

import math
from typing import List, Tuple, Union, Dict, Any
from abc import ABC, abstractmethod
from .operators import Symbol, SymbolicExpression, Add, Multiply, Power  # Assuming relative import from operators.py


# Mathematical Constants for Consciousness Modeling
class Constants:
    """
    Mathematical constants used in sacred geometry and consciousness modeling.
    """
    PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio
    PI = math.pi
    E = math.e
    SQRT_2 = math.sqrt(2)
    SQRT_3 = math.sqrt(3)
    SQRT_5 = math.sqrt(5)
    # Esoteric constants (e.g., for consciousness modeling)
    TETRAHEDRAL_CONSTANT = math.sqrt(2) / 3  # Related to tetrahedron
    OCTAHEDRAL_CONSTANT = math.sqrt(2)  # Related to octahedron
    ICOSAHEDRAL_CONSTANT = (math.sqrt(5) + 1) / 2  # Related to icosahedron


class GoldenRatio:
    """
    Class for golden ratio calculations and manipulations.
    """

    def __init__(self):
        self.value = Constants.PHI

    def ratio(self, a: Union[float, int, SymbolicExpression], b: Union[float, int, SymbolicExpression]) -> Union[float, SymbolicExpression]:
        """
        Calculate the golden ratio between two values: (a + b) / a or a / b.

        Args:
            a: First value.
            b: Second value.

        Returns:
            Golden ratio result.
        """
        if isinstance(a, SymbolicExpression) or isinstance(b, SymbolicExpression):
            return Divide(Add(a, b), a)  # Symbolic: (a + b) / a
        else:
            return (a + b) / a if a != 0 else float('inf')

    def nth_fibonacci_ratio(self, n: int) -> float:
        """
        Approximate golden ratio using nth Fibonacci numbers.

        Args:
            n: Index for Fibonacci approximation.

        Returns:
            Approximation of phi.
        """
        fib = Fibonacci()
        seq = fib.generate(n + 1)
        return seq[-1] / seq[-2] if seq[-2] != 0 else float('inf')

    def geometric_transform(self, point: Tuple[float, float], scale: float = 1.0) -> Tuple[float, float]:
        """
        Apply a golden ratio-based geometric transformation (e.g., scaling).

        Args:
            point: (x, y) coordinates.
            scale: Scaling factor.

        Returns:
            Transformed point.
        """
        x, y = point
        return (x * self.value * scale, y * self.value * scale)


class Fibonacci:
    """
    Class for generating Fibonacci sequences.
    """

    def __init__(self):
        self.memo = {0: 0, 1: 1}

    def generate(self, n: int) -> List[Union[int, SymbolicExpression]]:
        """
        Generate the first n Fibonacci numbers.

        Args:
            n: Number of terms.

        Returns:
            List of Fibonacci numbers.
        """
        if n < 0:
            raise ValueError("n must be non-negative.")
        for i in range(2, n):
            if i not in self.memo:
                self.memo[i] = self.memo[i-1] + self.memo[i-2]
        return [self.memo[i] for i in range(n)]

    def symbolic_generate(self, n: int) -> List[SymbolicExpression]:
        """
        Generate symbolic Fibonacci sequence using symbols.

        Args:
            n: Number of terms.

        Returns:
            List of symbolic expressions.
        """
        if n < 0:
            raise ValueError("n must be non-negative.")
        seq = [Symbol('F0'), Symbol('F1')]
        for i in range(2, n):
            seq.append(Add(seq[i-1], seq[i-2]))
        return seq[:n]

    def ratio_convergence(self, n: int) -> List[float]:
        """
        Generate ratios of consecutive Fibonacci numbers to show convergence to phi.

        Args:
            n: Number of ratios.

        Returns:
            List of ratios.
        """
        seq = self.generate(n + 1)
        return [seq[i+1] / seq[i] for i in range(1, n) if seq[i] != 0]


class PlatonicSolid(ABC):
    """
    Abstract base class for Platonic solids.
    """

    def __init__(self, edge_length: Union[float, SymbolicExpression] = 1.0):
        self.edge_length = edge_length

    @property
    @abstractmethod
    def vertices(self) -> int:
        pass

    @property
    @abstractmethod
    def edges(self) -> int:
        pass

    @property
    @abstractmethod
    def faces(self) -> int:
        pass

    @abstractmethod
    def volume(self) -> Union[float, SymbolicExpression]:
        """
        Calculate the volume of the solid.

        Returns:
            Volume.
        """
        pass

    @abstractmethod
    def surface_area(self) -> Union[float, SymbolicExpression]:
        """
        Calculate the surface area of the solid.

        Returns:
            Surface area.
        """
        pass

    def geometric_transform(self, transformation: str, **kwargs) -> 'PlatonicSolid':
        """
        Apply a geometric transformation (e.g., scale, rotate).

        Args:
            transformation: Type of transformation ('scale', 'rotate').
            **kwargs: Parameters for transformation.

        Returns:
            Transformed solid (new instance).
        """
        if transformation == 'scale':
            scale_factor = kwargs.get('scale_factor', 1.0)
            new_edge = Multiply(self.edge_length, scale_factor) if isinstance(self.edge_length, SymbolicExpression) else self.edge_length * scale_factor
            return self.__class__(new_edge)
        else:
            raise NotImplementedError(f"Transformation '{transformation}' not implemented.")


class Tetrahedron(PlatonicSolid):
    """
    Tetrahedron Platonic solid.
    """

    @property
    def vertices(self) -> int:
        return 4

    @property
    def edges(self) -> int:
        return 6

    @property
    def faces(self) -> int:
        return 4

    def volume(self) -> Union[float, SymbolicExpression]:
        """
        Volume of tetrahedron: (sqrt(2) / 12) * edge^3

        Returns:
            Volume.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            return Multiply(Power(self.edge_length, 3), Constants.TETRAHEDRAL_CONSTANT)
        else:
            return (math.sqrt(2) / 12) * (self.edge_length ** 3)

    def surface_area(self) -> Union[float, SymbolicExpression]:
        """
        Surface area of tetrahedron: sqrt(3) * edge^2

        Returns:
            Surface area.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            return Multiply(Power(self.edge_length, 2), Constants.SQRT_3)
        else:
            return math.sqrt(3) * (self.edge_length ** 2)


class Cube(PlatonicSolid):
    """
    Cube Platonic solid.
    """

    @property
    def vertices(self) -> int:
        return 8

    @property
    def edges(self) -> int:
        return 12

    @property
    def faces(self) -> int:
        return 6

    def volume(self) -> Union[float, SymbolicExpression]:
        """
        Volume of cube: edge^3

        Returns:
            Volume.
        """
        return Power(self.edge_length, 3)

    def surface_area(self) -> Union[float, SymbolicExpression]:
        """
        Surface area of cube: 6 * edge^2

        Returns:
            Surface area.
        """
        return Multiply(6, Power(self.edge_length, 2))


class Octahedron(PlatonicSolid):
    """
    Octahedron Platonic solid.
    """

    @property
    def vertices(self) -> int:
        return 6

    @property
    def edges(self) -> int:
        return 12

    @property
    def faces(self) -> int:
        return 8

    def volume(self) -> Union[float, SymbolicExpression]:
        """
        Volume of octahedron: (sqrt(2) / 3) * edge^3

        Returns:
            Volume.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            return Multiply(Power(self.edge_length, 3), Constants.OCTAHEDRAL_CONSTANT / 3)
        else:
            return (math.sqrt(2) / 3) * (self.edge_length ** 3)

    def surface_area(self) -> Union[float, SymbolicExpression]:
        """
        Surface area of octahedron: 2 * sqrt(3) * edge^2

        Returns:
            Surface area.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            return Multiply(Multiply(2, Constants.SQRT_3), Power(self.edge_length, 2))
        else:
            return 2 * math.sqrt(3) * (self.edge_length ** 2)


class Dodecahedron(PlatonicSolid):
    """
    Dodecahedron Platonic solid.
    """

    @property
    def vertices(self) -> int:
        return 20

    @property
    def edges(self) -> int:
        return 30

    @property
    def faces(self) -> int:
        return 12

    def volume(self) -> Union[float, SymbolicExpression]:
        """
        Volume of dodecahedron: (15 + 7*sqrt(5)) / 4 * edge^3

        Returns:
            Volume.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            const = Divide(Add(15, Multiply(7, Constants.SQRT_5)), 4)
            return Multiply(const, Power(self.edge_length, 3))
        else:
            return ((15 + 7 * math.sqrt(5)) / 4) * (self.edge_length ** 3)

    def surface_area(self) -> Union[float, SymbolicExpression]:
        """
        Surface area of dodecahedron: 3 * sqrt(25 + 10*sqrt(5)) * edge^2

        Returns:
            Surface area.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            const = Multiply(3, Power(Add(25, Multiply(10, Constants.SQRT_5)), 0.5))
            return Multiply(const, Power(self.edge_length, 2))
        else:
            return 3 * math.sqrt(25 + 10 * math.sqrt(5)) * (self.edge_length ** 2)


class Icosahedron(PlatonicSolid):
    """
    Icosahedron Platonic solid.
    """

    @property
    def vertices(self) -> int:
        return 12

    @property
    def edges(self) -> int:
        return 30

    @property
    def faces(self) -> int:
        return 20

    def volume(self) -> Union[float, SymbolicExpression]:
        """
        Volume of icosahedron: (5 * (3 + sqrt(5))) / 12 * edge^3

        Returns:
            Volume.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            const = Divide(Multiply(5, Add(3, Constants.SQRT_5)), 12)
            return Multiply(const, Power(self.edge_length, 3))
        else:
            return (5 * (3 + math.sqrt(5)) / 12) * (self.edge_length ** 3)

    def surface_area(self) -> Union[float, SymbolicExpression]:
        """
        Surface area of icosahedron: 5 * sqrt(3) * edge^2

        Returns:
            Surface area.
        """
        if isinstance(self.edge_length, SymbolicExpression):
            return Multiply(Multiply(5, Constants.SQRT_3), Power(self.edge_length, 2))
        else:
            return 5 * math.sqrt(3) * (self.edge_length ** 2)


class SacredAngles:
    """
    Class for sacred angles and related calculations.
    """

    SACRED_ANGLES = {
        'pentagon': 72,  # Degrees
        'pentagram': 36,
        'hexagon': 60,
        'octagon': 45,
        'decagon': 36,
    }

    def get_angle(self, shape: str) -> float:
        """
        Get the sacred angle for a shape.

        Args:
            shape: Name of the shape.

        Returns:
            Angle in degrees.
        """
        return self.SACRED_ANGLES.get(shape.lower(), 0)

    def radians(self, shape: str) -> float:
        """
        Get the sacred angle in radians.

        Args:
            shape: Name of the shape.

        Returns:
            Angle in radians.
        """
        degrees = self.get_angle(shape)
        return math.radians(degrees)

    def geometric_transform(self, angle_deg: float, point: Tuple[float, float], rotation_center: Tuple[float, float] = (0, 0)) -> Tuple[float, float]:
        """
        Rotate a point by a sacred angle around a center.

        Args:
            angle_deg: Rotation angle in degrees.
            point: (x, y) point to rotate.
            rotation_center: (cx, cy) center of rotation.

        Returns:
            Rotated point.
        """
        cx, cy = rotation_center
        x, y = point
        rad = math.radians(angle_deg)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        x_new = cx + (x - cx) * cos_a - (y - cy) * sin_a
        y_new = cy + (x - cx) * sin_a + (y - cy) * cos_a
        return (x_new, y_new)


class GeometricPatterns:
    """
    Class for generating geometric patterns, such as spirals or fractals.
    """

    def fibonacci_spiral(self, n: int, scale: float = 1.0) -> List[Tuple[float, float]]:
        """
        Generate points for a Fibonacci spiral.

        Args:
            n: Number of points.
            scale: Scaling factor.

        Returns:
            List of (x, y) points.
        """
        fib = Fibonacci()
        seq = fib.generate(n)
        points = []
        angle = 0
        for i, length in enumerate(seq[1:], start=1):  # Skip F0
            x = length * math.cos(angle) * scale
            y = length * math.sin(angle) * scale
            points.append((x, y))
            angle += math.radians(90)  # Quarter turn for spiral
        return points

    def golden_spiral(self, n: int, scale: float = 1.0) -> List[Tuple[float, float]]:
        """
        Generate points for a golden spiral using golden ratio.

        Args:
            n: Number of points.
            scale: Scaling factor.

        Returns:
            List of (x, y) points.
        """
        phi = GoldenRatio().value
        points = []
        angle = 0
        radius = 1
        for _ in range(n):
            x = radius * math.cos(angle) * scale
            y = radius * math.sin(angle) * scale
            points.append((x, y))
            radius *= phi
            angle += math.radians(90)  # Quarter turn
        return points

    def fractal_tree(self, depth: int, length: float = 100, angle: float = 25) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
        """
        Generate lines for a fractal tree pattern.

        Args:
            depth: Recursion depth.
            length: Initial branch length.
            angle: Branching angle in degrees.

        Returns:
            List of line segments as ((x1, y1), (x2, y2)).
        """
        def recurse(x, y, angle_rad, length, depth):
            if depth == 0:
                return []
            x2 = x + length * math.cos(angle_rad)
            y2 = y + length * math.sin(angle_rad)
            lines = [((x, y), (x2, y2))]
            new_length = length * 0.7  # Reduce length
            lines.extend(recurse(x2, y2, angle_rad + math.radians(angle), new_length, depth - 1))
            lines.extend(recurse(x2, y2, angle_rad - math.radians(angle), new_length, depth - 1))
            return lines

        return recurse(0, 0, math.pi / 2, length, depth)  # Start upwards
