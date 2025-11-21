# src/consciousness/metacognition.py
"""
Metacognition Module

This module implements metacognitive processes for consciousness modeling,
including self-reflection, cognitive monitoring, self-awareness assessment,
introspection mechanisms, and meta-learning capabilities. It provides classes
for processing metacognitive information and improving cognitive performance.

Key Features:
- MetacognitiveProcessor: Central processor for metacognitive functions.
- SelfReflection: Handles reflection on thoughts and actions.
- CognitiveMonitor: Monitors cognitive processes and performance.
- Methods for assessment, introspection, and meta-learning.

Usage: from src.consciousness.metacognition import MetacognitiveProcessor

processor = MetacognitiveProcessor()
processor.reflect_on_decision("decision_name", outcome="success")
awareness = processor.assess_self_awareness()
print(awareness)  # Output: e.g., 0.8
"""

from typing import List, Dict, Any, Optional, Tuple
import time
from dataclasses import dataclass
from enum import Enum

class ReflectionType(Enum):
    """Types of self-reflection."""
    DECISION = "decision"
    THOUGHT = "thought"
    ACTION = "action"
    EMOTION = "emotion"

@dataclass
class ReflectionRecord:
    """Record of a self-reflection instance."""
    type: ReflectionType
    content: str
    outcome: Optional[str] = None
    insights: List[str] = None
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.insights is None:
            self.insights = []

@dataclass
class CognitiveMetrics:
    """Metrics for cognitive monitoring."""
    accuracy: float  # 0.0 to 1.0
    efficiency: float  # 0.0 to 1.0
    error_rate: float  # 0.0 to 1.0
    timestamp: float

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()

class SelfReflection:
    """Handles self-reflection mechanisms."""

    def __init__(self):
        self.reflection_history: List[ReflectionRecord] = []

    def reflect(self, reflection_type: ReflectionType, content: str, outcome: Optional[str] = None) -> ReflectionRecord:
        """
        Perform a self-reflection.

        Args:
            reflection_type: Type of reflection.
            content: Content of the reflection.
            outcome: Optional outcome or result.

        Returns:
            ReflectionRecord instance.
        """
        record = ReflectionRecord(type=reflection_type, content=content, outcome=outcome)
        self.reflection_history.append(record)
        return record

    def add_insight(self, record: ReflectionRecord, insight: str):
        """
        Add an insight to a reflection record.

        Args:
            record: The reflection record.
            insight: The insight to add.
        """
        record.insights.append(insight)

    def get_reflections(self, reflection_type: Optional[ReflectionType] = None) -> List[ReflectionRecord]:
        """
        Get reflections, optionally filtered by type.

        Args:
            reflection_type: Type to filter by, or None for all.

        Returns:
            List of ReflectionRecord instances.
        """
        if reflection_type:
            return [r for r in self.reflection_history if r.type == reflection_type]
        return self.reflection_history.copy()

class CognitiveMonitor:
    """Monitors cognitive processes and performance."""

    def __init__(self):
        self.metrics_history: List[CognitiveMetrics] = []
        self.error_log: List[Dict[str, Any]] = []

    def record_metrics(self, accuracy: float, efficiency: float, error_rate: float):
        """
        Record cognitive metrics.

        Args:
            accuracy: Accuracy score (0.0 to 1.0).
            efficiency: Efficiency score (0.0 to 1.0).
            error_rate: Error rate (0.0 to 1.0).
        """
        metrics = CognitiveMetrics(accuracy=accuracy, efficiency=efficiency, error_rate=error_rate, timestamp=time.time())
        self.metrics_history.append(metrics)

    def log_error(self, error_type: str, description: str, context: Optional[Dict[str, Any]] = None):
        """
        Log a cognitive error.

        Args:
            error_type: Type of error.
            description: Description of the error.
            context: Optional context information.
        """
        error_entry = {
            'type': error_type,
            'description': description,
            'context': context or {},
            'timestamp': time.time()
        }
        self.error_log.append(error_entry)

    def get_average_metrics(self) -> Dict[str, float]:
        """
        Get average cognitive metrics.

        Returns:
            Dictionary of average metrics.
        """
        if not self.metrics_history:
            return {'accuracy': 0.0, 'efficiency': 0.0, 'error_rate': 0.0}

        total_accuracy = sum(m.accuracy for m in self.metrics_history)
        total_efficiency = sum(m.efficiency for m in self.metrics_history)
        total_error_rate = sum(m.error_rate for m in self.metrics_history)
        count = len(self.metrics_history)

        return {
            'accuracy': total_accuracy / count,
            'efficiency': total_efficiency / count,
            'error_rate': total_error_rate / count
        }

    def analyze_performance(self) -> Dict[str, Any]:
        """
        Analyze performance trends.

        Returns:
            Dictionary with analysis results.
        """
        if len(self.metrics_history) < 2:
            return {'trend': 'insufficient_data'}

        recent = self.metrics_history[-5:]  # Last 5 records
        avg_recent_accuracy = sum(m.accuracy for m in recent) / len(recent)
        avg_overall_accuracy = self.get_average_metrics()['accuracy']

        trend = 'improving' if avg_recent_accuracy > avg_overall_accuracy else 'declining'

        return {
            'trend': trend,
            'recent_average_accuracy': avg_recent_accuracy,
            'overall_average_accuracy': avg_overall_accuracy,
            'error_count': len(self.error_log)
        }

class MetacognitiveProcessor:
    """Central processor for metacognitive functions, integrating reflection, monitoring, and learning."""

    def __init__(self):
        self.self_reflection = SelfReflection()
        self.cognitive_monitor = CognitiveMonitor()
        self.self_awareness_level: float = 0.5  # 0.0 to 1.0
        self.introspection_depth: float = 0.3  # 0.0 to 1.0
        self.meta_learning_rules: Dict[str, Any] = {}  # Rules learned from experiences

    def reflect_on_decision(self, decision: str, outcome: str) -> ReflectionRecord:
        """
        Reflect on a decision and its outcome.

        Args:
            decision: Description of the decision.
            outcome: Outcome of the decision.

        Returns:
            ReflectionRecord.
        """
        record = self.self_reflection.reflect(ReflectionType.DECISION, decision, outcome)
        # Adjust self-awareness based on reflection
        self.self_awareness_level = min(1.0, self.self_awareness_level + 0.05)
        return record

    def introspect(self, topic: str, depth: float = 0.5) -> Dict[str, Any]:
        """
        Perform introspection on a topic.

        Args:
            topic: Topic to introspect on.
            depth: Depth of introspection (0.0 to 1.0).

        Returns:
            Dictionary with introspection results.
        """
        self.introspection_depth = depth
        insights = []
        if depth > 0.7:
            insights.append("Deep insight: Patterns in behavior identified.")
        elif depth > 0.4:
            insights.append("Moderate insight: Awareness of biases.")
        else:
            insights.append("Shallow insight: Basic self-observation.")

        # Increase self-awareness
        self.self_awareness_level = min(1.0, self.self_awareness_level + depth * 0.1)

        return {
            'topic': topic,
            'depth': depth,
            'insights': insights,
            'timestamp': time.time()
        }

    def assess_self_awareness(self) -> float:
        """
        Assess current self-awareness level.

        Returns:
            Self-awareness score (0.0 to 1.0).
        """
        # Base on reflections, metrics, and introspection
        reflection_factor = min(1.0, len(self.self_reflection.reflection_history) / 10.0)
        metrics_factor = self.cognitive_monitor.get_average_metrics()['accuracy']
        introspection_factor = self.introspection_depth

        self.self_awareness_level = (reflection_factor + metrics_factor + introspection_factor) / 3.0
        return self.self_awareness_level

    def monitor_cognition(self, accuracy: float, efficiency: float, error_rate: float):
        """
        Monitor cognitive performance.

        Args:
            accuracy: Accuracy score.
            efficiency: Efficiency score.
            error_rate: Error rate.
        """
        self.cognitive_monitor.record_metrics(accuracy, efficiency, error_rate)
        if error_rate > 0.5:
            self.self_reflection.reflect(ReflectionType.THOUGHT, "High error rate detected", "Need improvement")

    def meta_learn(self, experience: str, lesson: str):
        """
        Learn from an experience to improve future cognition.

        Args:
            experience: Description of the experience.
            lesson: Lesson learned.
        """
        self.meta_learning_rules[experience] = lesson
        # Apply learning: e.g., adjust monitoring or reflection strategies
        self.self_awareness_level = min(1.0, self.self_awareness_level + 0.02)

    def get_meta_learning_rules(self) -> Dict[str, Any]:
        """
        Get learned meta-rules.

        Returns:
            Dictionary of rules.
        """
        return self.meta_learning_rules.copy()

    def cognitive_monitoring_report(self) -> Dict[str, Any]:
        """
        Generate a report on cognitive monitoring.

        Returns:
            Dictionary with report data.
        """
        avg_metrics = self.cognitive_monitor.get_average_metrics()
        performance_analysis = self.cognitive_monitor.analyze_performance()
        reflections = self.self_reflection.get_reflections()

        return {
            'average_metrics': avg_metrics,
            'performance_analysis': performance_analysis,
            'reflection_count': len(reflections),
            'self_awareness_level': self.self_awareness_level,
            'introspection_depth': self.introspection_depth
        }

    def reset(self):
        """
        Reset the metacognitive processor.
        """
        self.self_reflection = SelfReflection()
        self.cognitive_monitor = CognitiveMonitor()
        self.self_awareness_level = 0.5
        self.introspection_depth = 0.3
        self.meta_learning_rules.clear()
