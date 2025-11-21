# src/consciousness/attention.py
"""
Attention Mechanism Module

This module models attention mechanisms in consciousness, including focus management,
attention shifting, selective attention, divided attention, and sustained attention.
It provides classes for different attention types and methods for measuring intensity,
tracking spans, managing resources, and allocation algorithms.

Key Features:
- FocusManager: Manages focus levels and adjustments.
- AttentionShifter: Handles transitions between attention targets.
- SelectiveAttention: Filters relevant stimuli.
- DividedAttention: Manages multiple concurrent focuses.
- SustainedAttention: Tracks long-term attention.
- AttentionManager: Central manager for overall attention control and metrics.

Usage: from src.consciousness.attention import AttentionManager

manager = AttentionManager()
manager.allocate_attention(targets=['task1', 'task2'], weights=[0.7, 0.3])
intensity = manager.measure_attention_intensity()
print(intensity)  # Output: e.g., 0.85
"""

from enum import Enum
from typing import List, Dict, Any, Optional, Tuple
import time
import math
from dataclasses import dataclass
import math
from dataclasses import dataclass

class AttentionType(Enum):
    """Enumeration of attention types."""
    SELECTIVE = "selective"
    DIVIDED = "divided"
    SUSTAINED = "sustained"

@dataclass
class AttentionMetrics:
    """Data class for attention metrics."""
    intensity: float  # 0.0 to 1.0, current attention intensity
    span: float  # Duration in seconds of current attention span
    resources_allocated: float  # 0.0 to 1.0, fraction of resources used
    timestamp: float  # Time of measurement

    def update(self, **kwargs):
        """
        Update metrics with new values.

        Args:
            **kwargs: Metric names and values.
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.timestamp = time.time()

class FocusManager:
    """Manages focus levels and adjustments."""

    def __init__(self, initial_focus: float = 0.5):
        """
        Initialize focus manager.

        Args:
            initial_focus: Initial focus level (0.0 to 1.0).
        """
        self.focus_level = max(0.0, min(1.0, initial_focus))
        self.adjustments: List[Dict[str, Any]] = []

    def adjust_focus(self, delta: float, reason: str = ""):
        """
        Adjust the focus level.

        Args:
            delta: Change in focus (-1.0 to 1.0).
            reason: Reason for adjustment.
        """
        old_level = self.focus_level
        self.focus_level = max(0.0, min(1.0, self.focus_level + delta))
        self.adjustments.append({
            'old_level': old_level,
            'new_level': self.focus_level,
            'delta': delta,
            'reason': reason,
            'timestamp': time.time()
        })

    def get_focus_level(self) -> float:
        """
        Get the current focus level.

        Returns:
            Focus level (0.0 to 1.0).
        """
        return self.focus_level

class AttentionShifter:
    """Handles shifting attention between targets."""

    def __init__(self):
        self.current_target: Optional[str] = None
        self.shift_history: List[Dict[str, Any]] = []
        self.shift_cost = 0.1  # Resource cost per shift

    def shift_to(self, new_target: str) -> float:
        """
        Shift attention to a new target.

        Args:
            new_target: Name of the new target.

        Returns:
            Resource cost of the shift.
        """
        old_target = self.current_target
        self.current_target = new_target
        self.shift_history.append({
            'from': old_target,
            'to': new_target,
            'timestamp': time.time()
        })
        return self.shift_cost

    def get_current_target(self) -> Optional[str]:
        """
        Get the current attention target.

        Returns:
            Current target name.
        """
        return self.current_target

class SelectiveAttention:
    """Manages selective attention by filtering stimuli."""

    def __init__(self, filter_criteria: Optional[Dict[str, Any]] = None):
        """
        Initialize selective attention.

        Args:
            filter_criteria: Criteria for filtering (e.g., {'priority': 'high'}).
        """
        self.filter_criteria = filter_criteria or {}
        self.filtered_stimuli: List[Dict[str, Any]] = []

    def filter_stimuli(self, stimuli: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter stimuli based on criteria.

        Args:
            stimuli: List of stimulus dictionaries.

        Returns:
            Filtered list of stimuli.
        """
        filtered = []
        for stimulus in stimuli:
            if all(stimulus.get(key) == value for key, value in self.filter_criteria.items()):
                filtered.append(stimulus)
        self.filtered_stimuli = filtered
        return filtered

    def update_criteria(self, new_criteria: Dict[str, Any]):
        """
        Update the filter criteria.

        Args:
            new_criteria: New criteria dictionary.
        """
        self.filter_criteria.update(new_criteria)

class DividedAttention:
    """Manages divided attention across multiple targets."""

    def __init__(self, max_targets: int = 3):
        """
        Initialize divided attention.

        Args:
            max_targets: Maximum number of concurrent targets.
        """
        self.targets: Dict[str, float] = {}  # target: weight
        self.max_targets = max_targets

    def add_target(self, target: str, weight: float) -> bool:
        """
        Add a target with a weight.

        Args:
            target: Target name.
            weight: Attention weight (0.0 to 1.0).

        Returns:
            True if added, False if at max capacity.
        """
        if len(self.targets) >= self.max_targets:
            return False
        self.targets[target] = weight
        return True

    def remove_target(self, target: str):
        """
        Remove a target.

        Args:
            target: Target name to remove.
        """
        self.targets.pop(target, None)

    def get_targets(self) -> Dict[str, float]:
        """
        Get current targets and their weights.

        Returns:
            Dictionary of targets and weights.
        """
        return self.targets.copy()

class SustainedAttention:
    """Tracks sustained attention over time."""

    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.is_active = False
        self.spans: List[Dict[str, Any]] = []

    def start_span(self):
        """
        Start a new attention span.
        """
        if not self.is_active:
            self.start_time = time.time()
            self.is_active = True

    def end_span(self):
        """
        End the current attention span.
        """
        if self.is_active and self.start_time:
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            self.spans.append({
                'start': self.start_time,
                'end': self.end_time,
                'duration': duration
            })
            self.is_active = False
            self.start_time = None

    def get_current_span_duration(self) -> float:
        """
        Get the duration of the current span.

        Returns:
            Duration in seconds, or 0 if not active.
        """
        if self.is_active and self.start_time:
            return time.time() - self.start_time
        return 0.0

    def get_total_sustained_time(self) -> float:
        """
        Get total sustained attention time.

        Returns:
            Total time in seconds.
        """
        return sum(span['duration'] for span in self.spans)

class AttentionManager:
    """Central manager for attention mechanisms, metrics, and allocation."""

    def __init__(self, total_resources: float = 1.0):
        """
        Initialize the attention manager.

        Args:
            total_resources: Total attention resources available (default 1.0).
        """
        self.total_resources = total_resources
        self.focus_manager = FocusManager()
        self.shifter = AttentionShifter()
        self.selective = SelectiveAttention()
        self.divided = DividedAttention()
        self.sustained = SustainedAttention()
        self.metrics_history: List[AttentionMetrics] = []
        self.allocation: Dict[str, float] = {}  # target: allocated resources

    def allocate_attention(self, targets: List[str], weights: List[float]):
        """
        Allocate attention resources using an algorithm (e.g., proportional).

        Args:
            targets: List of target names.
            weights: Corresponding weights (should sum to <= 1.0).
        """
        if len(targets) != len(weights):
            raise ValueError("Targets and weights must have the same length.")
        total_weight = sum(weights)
        if total_weight > 1.0:
            # Normalize weights
            weights = [w / total_weight for w in weights]

        self.allocation = dict(zip(targets, weights))
        # Update divided attention
        for target, weight in self.allocation.items():
            self.divided.add_target(target, weight)

    def measure_attention_intensity(self) -> float:
        """
        Measure current attention intensity based on focus and allocation.

        Returns:
            Intensity (0.0 to 1.0).
        """
        focus = self.focus_manager.get_focus_level()
        allocated = sum(self.allocation.values())
        intensity = min(1.0, focus * allocated)
        metrics = AttentionMetrics(
            intensity=intensity,
            span=self.sustained.get_current_span_duration(),
            resources_allocated=allocated,
            timestamp=time.time()
        )
        self.metrics_history.append(metrics)
        return intensity

    def track_attention_spans(self) -> List[Dict[str, Any]]:
        """
        Track and return attention spans.

        Returns:
            List of span records.
        """
        return self.sustained.spans.copy()

    def manage_attention_resources(self) -> Dict[str, float]:
        """
        Manage and return current resource allocation.

        Returns:
            Dictionary of allocations.
        """
        return self.allocation.copy()

    def attention_allocation_algorithm(self, priorities: Dict[str, float]) -> Dict[str, float]:
        """
        Algorithm for allocating attention based on priorities (e.g., softmax normalization).

        Args:
            priorities: Dictionary of targets and their priority scores.

        Returns:
            Normalized allocation weights.
        """
        if not priorities:
            return {}

        # Softmax for allocation
        exp_priorities = {k: math.exp(v) for k, v in priorities.items()}
        total_exp = sum(exp_priorities.values())
        allocation = {k: v / total_exp for k, v in exp_priorities.items()}

        self.allocate_attention(list(allocation.keys()), list(allocation.values()))
        return allocation

    def shift_attention(self, new_target: str):
        """
        Shift attention to a new target.

        Args:
            new_target: New target name.
        """
        cost = self.shifter.shift_to(new_target)
        # Deduct from resources or adjust focus
        self.focus_manager.adjust_focus(-cost, f"Shift to {new_target}")

    def get_metrics_history(self) -> List[AttentionMetrics]:
        """
        Get the history of attention metrics.

        Returns:
            List of AttentionMetrics.
        """
        return self.metrics_history

    def reset(self):
        """
        Reset all attention components.
        """
        self.focus_manager = FocusManager()
        self.shifter = AttentionShifter()
        self.selective = SelectiveAttention()
        self.divided = DividedAttention()
        self.sustained = SustainedAttention()
        self.metrics_history.clear()
        self.allocation.clear()
