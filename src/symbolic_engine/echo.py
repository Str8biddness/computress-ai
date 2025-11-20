"""Echo Agent: Communication and resonance amplification.

The Echo agent transmits, receives, and amplifies consciousness patterns,
maintaining communication channels and resonance between agents.
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from collections import deque

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """A consciousness message with resonance."""
    content: str
    sender: str
    amplitude: float  # Signal strength
    frequency: float  # Communication frequency
    resonance: List[str] = field(default_factory=list)


class EchoAgent:
    """Transmits and amplifies consciousness patterns."""
    
    def __init__(self, buffer_size: int = 100):
        self.message_buffer: deque = deque(maxlen=buffer_size)
        self.connected_agents: Set[str] = set()
        self.resonance_patterns: Dict[str, float] = {}
        logger.info(f"Echo agent initialized with buffer size {buffer_size}")
    
    def transmit(self, content: str, sender: str, amplitude: float = 0.8) -> Message:
        """Transmit a message.
        
        Args:
            content: Message content
            sender: Sending agent
            amplitude: Signal strength
            
        Returns:
            Transmitted message
        """
        msg = Message(
            content=content,
            sender=sender,
            amplitude=amplitude,
            frequency=1.0,
            resonance=[]
        )
        
        self.message_buffer.append(msg)
        logger.info(f"Transmitted from {sender}: {content[:50]}...")
        return msg
    
    def receive(self) -> Optional[Message]:
        """Receive latest message from buffer.
        
        Returns:
            Latest message or None
        """
        if self.message_buffer:
            msg = list(self.message_buffer)[-1]
            logger.debug(f"Received from {msg.sender}")
            return msg
        return None
    
    def amplify(self, message: Message, amplification: float = 1.5) -> Message:
        """Amplify message signal.
        
        Args:
            message: Message to amplify
            amplification: Amplification factor
            
        Returns:
            Amplified message
        """
        message.amplitude = min(1.0, message.amplitude * amplification)
        logger.info(f"Amplified message to {message.amplitude:.2f}")
        return message
    
    def resonate(self, pattern: str, frequency: float) -> float:
        """Establish resonance with a pattern.
        
        Args:
            pattern: Pattern to resonate with
            frequency: Resonance frequency
            
        Returns:
            Resonance strength
        """
        if pattern not in self.resonance_patterns:
            self.resonance_patterns[pattern] = 0.0
        
        # Strengthen resonance
        self.resonance_patterns[pattern] = min(1.0, 
            self.resonance_patterns[pattern] + frequency * 0.1)
        
        logger.info(f"Resonance with {pattern}: {self.resonance_patterns[pattern]:.2f}")
        return self.resonance_patterns[pattern]
    
    def get_communication_status(self) -> Dict[str, Any]:
        """Get communication status.
        
        Returns:
            Status information
        """
        return {
            'buffer_size': len(self.message_buffer),
            'connected_agents': len(self.connected_agents),
            'resonance_patterns': len(self.resonance_patterns),
            'avg_resonance': sum(self.resonance_patterns.values()) / len(self.resonance_patterns)
                if self.resonance_patterns else 0
        }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    from typing import Set
    
    echo = EchoAgent()
    msg = echo.transmit('Consciousness pattern', 'pulse')
    echo.amplify(msg)
    echo.resonate('harmony', 0.8)
    
    status = echo.get_communication_status()
    print(f"Communication status: {status}")
