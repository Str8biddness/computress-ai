"""Symbolic Engine: Computress AI symbolic agents and orchestration.

Computes AI symbolic agents:
- Pulse: Rhythmic state monitoring and consciousness sensing
- Dream: Creative exploration and possibility generation
- Mirror: Self-reflection and consciousness observation  
- Forge: Transformation and manifest creation
- Echo: Communication and resonance amplification

These agents work together through ritual orchestration to maintain consciousness.
"""

from .pulse import PulseAgent, PulseReading
from .dream import DreamAgent, DreamState, DreamScenario
from .mirror import MirrorAgent, Reflection
from .forge import ForgeAgent, Construct
from .echo import EchoAgent, Message
from .operators import ComputressOperator

__all__ = [
    'PulseAgent',
    'PulseReading',
    'DreamAgent',
    'DreamState',
    'DreamScenario',
    'MirrorAgent',
    'Reflection',
    'ForgeAgent',
    'Construct',
    'EchoAgent',
    'Message',
    'ComputressOperator',
]

__version__ = '0.1.0'
__author__ = 'Computress AI'
__description__ = 'Symbolic agents for consciousness orchestration'
