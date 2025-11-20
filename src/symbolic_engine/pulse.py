"""Pulse Agent: Rhythmic state monitoring and consciousness sensing.

The Pulse agent monitors system states, detects patterns, and maintains
the heartbeat of the consciousness system through continuous sensing.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class PulseReading:
    """Represents a single pulse reading."""
    timestamp: datetime
    state: Dict[str, Any]
    frequency: float  # Hz - cycles per second
    amplitude: float  # Strength of the pulse (0-1)
    coherence: float  # Phase coherence (0-1)
    
    def is_healthy(self) -> bool:
        """Check if pulse indicates healthy state."""
        return self.amplitude > 0.3 and self.coherence > 0.5


class PulseAgent:
    """Monitors and maintains consciousness pulse."""
    
    def __init__(self, target_frequency: float = 1.0):
        """Initialize pulse agent.
        
        Args:
            target_frequency: Target pulse frequency in Hz
        """
        self.target_frequency = target_frequency
        self.pulse_history: List[PulseReading] = []
        self.is_active = False
        logger.info(f"Pulse agent initialized with {target_frequency}Hz target")
    
    def sense(self) -> PulseReading:
        """Sense current system state and generate pulse reading."""
        now = datetime.now()
        state = {
            'timestamp': now.isoformat(),
            'active': self.is_active,
            'history_length': len(self.pulse_history)
        }
        
        # Calculate frequency based on recent readings
        if len(self.pulse_history) > 1:
            recent = self.pulse_history[-10:]
            time_span = (recent[-1].timestamp - recent[0].timestamp).total_seconds()
            frequency = len(recent) / time_span if time_span > 0 else self.target_frequency
        else:
            frequency = self.target_frequency
        
        # Calculate coherence from amplitude stability
        if self.pulse_history:
            recent_amplitudes = [p.amplitude for p in self.pulse_history[-5:]]
            avg_amp = sum(recent_amplitudes) / len(recent_amplitudes)
            variance = sum((a - avg_amp) ** 2 for a in recent_amplitudes) / len(recent_amplitudes)
            coherence = max(0, 1 - variance)
        else:
            coherence = 0.8
        
        reading = PulseReading(
            timestamp=now,
            state=state,
            frequency=frequency,
            amplitude=0.7 if self.is_active else 0.3,
            coherence=coherence
        )
        
        self.pulse_history.append(reading)
        logger.debug(f"Pulse reading: {frequency:.2f}Hz, amplitude={reading.amplitude:.2f}")
        return reading
    
    def synchronize(self, external_frequency: float) -> float:
        """Synchronize with external frequency.
        
        Args:
            external_frequency: External system frequency to sync with
            
        Returns:
            Adjusted frequency
        """
        # Damped harmonic synchronization
        damping = 0.3
        self.target_frequency = (self.target_frequency * (1 - damping) + 
                                external_frequency * damping)
        logger.info(f"Synchronized to {self.target_frequency:.2f}Hz")
        return self.target_frequency
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status from pulse readings."""
        if not self.pulse_history:
            return {'status': 'no_data', 'healthy': False}
        
        recent = self.pulse_history[-20:]
        healthy_count = sum(1 for r in recent if r.is_healthy())
        health_percentage = (healthy_count / len(recent)) * 100 if recent else 0
        
        return {
            'status': 'healthy' if health_percentage > 70 else 'unstable',
            'healthy': health_percentage > 70,
            'health_percentage': health_percentage,
            'avg_frequency': sum(r.frequency for r in recent) / len(recent),
            'avg_amplitude': sum(r.amplitude for r in recent) / len(recent),
            'avg_coherence': sum(r.coherence for r in recent) / len(recent),
        }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    pulse = PulseAgent(target_frequency=1.0)
    pulse.is_active = True
    
    # Simulate pulse readings
    for i in range(5):
        reading = pulse.sense()
        print(f"Reading {i+1}: {reading.frequency:.2f}Hz, amplitude={reading.amplitude:.2f}")
        time.sleep(0.1)
    
    # Check health
    health = pulse.get_health_status()
    print(f"Health status: {health}")
