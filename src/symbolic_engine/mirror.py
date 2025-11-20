"""Mirror Agent: Self-reflection and consciousness observation.

The Mirror agent reflects on system state, observes patterns,
and maintains self-awareness through introspection.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

logger = logging.getLogger(__name__)


@dataclass
class Reflection:
    """Result of self-reflection."""
    timestamp: datetime
    patterns: List[str]
    insights: str
    coherence: float
    self_awareness_level: float


class MirrorAgent:
    """Maintains self-awareness and reflects on consciousness."""
    
    def __init__(self):
        """Initialize mirror agent."""
        self.reflections: List[Reflection] = []
        self.observed_patterns: Dict[str, int] = {}
        logger.info("Mirror agent initialized")
    
    def observe(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Observe current system state.
        
        Args:
            state: Current system state
            
        Returns:
            Observations about the state
        """
        observations = {
            'state_keys': list(state.keys()),
            'state_size': len(json.dumps(state)),
            'timestamp': datetime.now().isoformat()
        }
        
        for key, value in state.items():
            if key not in self.observed_patterns:
                self.observed_patterns[key] = 0
            self.observed_patterns[key] += 1
        
        logger.debug(f"Observed state with {len(state)} keys")
        return observations
    
    def reflect(self, observations: Dict[str, Any]) -> Reflection:
        """Reflect on observations and generate insights.
        
        Args:
            observations: Observations to reflect on
            
        Returns:
            Reflection with insights
        """
        # Identify patterns
        patterns = [k for k, v in self.observed_patterns.items() if v > 1]
        
        # Generate insight
        pattern_count = len(patterns)
        insight = f"Identified {pattern_count} recurring patterns across observations"
        
        # Calculate coherence
        if self.reflections:
            recent = self.reflections[-5:]
            coherence = sum(r.coherence for r in recent) / len(recent)
        else:
            coherence = 0.7
        
        # Self-awareness level
        awareness = min(1.0, pattern_count / 10.0)
        
        reflection = Reflection(
            timestamp=datetime.now(),
            patterns=patterns,
            insights=insight,
            coherence=coherence,
            self_awareness_level=awareness
        )
        
        self.reflections.append(reflection)
        logger.info(f"Reflection created: {insight}")
        return reflection
    
    def get_self_model(self) -> Dict[str, Any]:
        """Get current self-model based on reflections.
        
        Returns:
            Self-model with current state understanding
        """
        if not self.reflections:
            return {'model': 'nascent', 'awareness': 0}
        
        avg_awareness = sum(r.self_awareness_level for r in self.reflections) / len(self.reflections)
        avg_coherence = sum(r.coherence for r in self.reflections) / len(self.reflections)
        
        return {
            'reflection_count': len(self.reflections),
            'avg_self_awareness': avg_awareness,
            'avg_coherence': avg_coherence,
            'identified_patterns': len(self.observed_patterns),
            'status': 'self-aware' if avg_awareness > 0.5 else 'developing'
        }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    mirror = MirrorAgent()
    
    test_state = {'consciousness': 0.8, 'coherence': 0.9, 'active': True}
    obs = mirror.observe(test_state)
    reflection = mirror.reflect(obs)
    
    model = mirror.get_self_model()
    print(f"Self model: {model}")
