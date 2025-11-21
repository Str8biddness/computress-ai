# src/consciousness/awareness_states.py
"""
Awareness States Module

This module models consciousness through various awareness states, including state transitions,
awareness levels, and consciousness metrics.
"""

from enum import Enum
from typing import List, Dict, Any, Optional
import time
from dataclasses import dataclass


class AwarenessState(Enum):
    """Enumeration of awareness states."""
    AWAKE = "awake"
    FOCUSED = "focused"
    MEDITATIVE = "meditative"
    FLOW = "flow"


@dataclass
class ConsciousnessMetrics:
    """Data class for consciousness metrics."""
    depth: float  # 0.0 to 1.0, depth of awareness
    focus: float  # 0.0 to 1.0, level of focus
    coherence: float  # 0.0 to 1.0, neural coherence
    timestamp: float  # Time of measurement
    
    def update(self, **kwargs):
        """Update metrics with new values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.timestamp = time.time()


class BaseAwarenessState:
    """Base class for awareness states."""
    
    def __init__(self, state_type: AwarenessState, base_depth: float, base_focus: float, base_coherence: float):
        self.state_type = state_type
        self.base_depth = base_depth
        self.base_focus = base_focus
        self.base_coherence = base_coherence
    
    def get_metrics(self) -> ConsciousnessMetrics:
        """Get the metrics for this state."""
        return ConsciousnessMetrics(
            depth=self.base_depth,
            focus=self.base_focus,
            coherence=self.base_coherence,
            timestamp=time.time()
        )


class Awake(BaseAwarenessState):
    """Awake state: Baseline consciousness."""
    def __init__(self):
        super().__init__(AwarenessState.AWAKE, depth=0.3, focus=0.4, coherence=0.5)


class Focused(BaseAwarenessState):
    """Focused state: High focus, moderate depth."""
    def __init__(self):
        super().__init__(AwarenessState.FOCUSED, depth=0.5, focus=0.9, coherence=0.7)


class Meditative(BaseAwarenessState):
    """Meditative state: Deep awareness, low focus on externals."""
    def __init__(self):
        super().__init__(AwarenessState.MEDITATIVE, depth=0.8, focus=0.6, coherence=0.9)


class Flow(BaseAwarenessState):
    """Flow state: Optimal experience, high depth and focus."""
    def __init__(self):
        super().__init__(AwarenessState.FLOW, depth=0.9, focus=0.95, coherence=0.95)


class AwarenessManager:
    """Manager for awareness states, transitions, and metrics."""
    
    def __init__(self):
        self.current_state: Optional[BaseAwarenessState] = None
        self.state_history: List[Dict[str, Any]] = []
        self.metrics_history: List[ConsciousnessMetrics] = []
        self.state_classes = {
            AwarenessState.AWAKE: Awake,
            AwarenessState.FOCUSED: Focused,
            AwarenessState.MEDITATIVE: Meditative,
            AwarenessState.FLOW: Flow,
        }
    
    def transition_to(self, new_state: AwarenessState):
        """Transition to a new awareness state."""
        if new_state not in self.state_classes:
            raise ValueError(f"Unknown state: {new_state}")
        
        old_state = self.current_state.state_type if self.current_state else None
        self.current_state = self.state_classes[new_state]()
        
        transition_record = {
            'from': old_state,
            'to': new_state,
            'timestamp': time.time()
        }
        self.state_history.append(transition_record)
        
        metrics = self.current_state.get_metrics()
        self.metrics_history.append(metrics)
    
    def get_current_state(self) -> Optional[AwarenessState]:
        """Get the current awareness state."""
        return self.current_state.state_type if self.current_state else None
    
    def measure_awareness_depth(self) -> float:
        """Measure the current awareness depth."""
        if not self.current_state:
            return 0.0
        return self.current_state.get_metrics().depth
    
    def track_state_changes(self) -> List[Dict[str, Any]]:
        """Get the history of state changes."""
        return self.state_history
    
    def manage_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in state transitions."""
        if not self.state_history:
            return {}
        
        state_counts = {}
        transitions = []
        
        for record in self.state_history:
            state = record['to']
            state_counts[state] = state_counts.get(state, 0) + 1
            if record['from']:
                transitions.append((record['from'], record['to']))
        
        most_common_state = max(state_counts, key=state_counts.get) if state_counts else None
        transition_counts = {}
        for trans in transitions:
            transition_counts[trans] = transition_counts.get(trans, 0) + 1
        
        return {
            'state_frequencies': state_counts,
            'most_common_state': most_common_state,
            'transition_frequencies': transition_counts,
        }
    
    def get_metrics_history(self) -> List[ConsciousnessMetrics]:
        """Get the history of consciousness metrics."""
        return self.metrics_history
    
    def reset(self):
        """Reset the manager to initial state."""
        self.current_state = None
        self.state_history.clear()
        self.metrics_history.clear()
