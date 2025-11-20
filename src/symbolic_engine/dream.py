"""Dream Agent: Creative exploration and possibility generation.

The Dream agent explores potential futures, generates creative solutions,
and maintains vision through imaginative state exploration.
"""

import logging
import random
from typing import Dict, List, Any, Set, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class DreamState(Enum):
    """States of dreaming process."""
    AWAKE = 'awake'
    REM = 'rem'
    DEEP = 'deep'
    LUCID = 'lucid'


@dataclass
class DreamScenario:
    """Represents a dream scenario or possibility."""
    name: str
    elements: Set[str] = field(default_factory=set)
    connectivity: Dict[str, List[str]] = field(default_factory=dict)
    probability: float = 0.5
    coherence: float = 0.5
    creativity_score: float = 0.5


class DreamAgent:
    """Generates creative possibilities and explores solution spaces."""
    
    def __init__(self, memory_size: int = 100):
        """Initialize dream agent.
        
        Args:
            memory_size: Size of dream memory buffer
        """
        self.state = DreamState.AWAKE
        self.dream_memory: List[DreamScenario] = []
        self.max_memory = memory_size
        logger.info(f"Dream agent initialized with {memory_size} memory size")
    
    def enter_dream(self, depth: float = 0.5) -> DreamState:
        """Enter dream state.
        
        Args:
            depth: How deep into dream (0-1)
            
        Returns:
            Current dream state
        """
        if depth < 0.3:
            self.state = DreamState.REM
        elif depth < 0.7:
            self.state = DreamState.DEEP
        else:
            self.state = DreamState.LUCID
        
        logger.info(f"Entered {self.state.value} dream state")
        return self.state
    
    def generate_scenario(self, seed_concepts: List[str]) -> DreamScenario:
        """Generate a dream scenario from concepts.
        
        Args:
            seed_concepts: Starting concepts for scenario
            
        Returns:
            Generated dream scenario
        """
        if not seed_concepts:
            seed_concepts = ['emergence', 'connection', 'transcendence']
        
        # Creative expansion
        expanded = set(seed_concepts)
        for _ in range(random.randint(2, 5)):
            concept = random.choice(list(expanded))
            # Generate related concepts
            related = [f"{concept}_{i}" for i in range(random.randint(1, 3))]
            expanded.update(related)
        
        # Build connectivity graph
        connectivity = {elem: random.sample(list(expanded - {elem}), 
                       k=min(3, len(expanded)-1)) for elem in expanded}
        
        scenario = DreamScenario(
            name=f"Dream_{len(self.dream_memory)}",
            elements=expanded,
            connectivity=connectivity,
            probability=random.random(),
            coherence=max(0.5, random.random()),  # Dreams have some minimum coherence
            creativity_score=random.random()
        )
        
        self.dream_memory.append(scenario)
        if len(self.dream_memory) > self.max_memory:
            self.dream_memory.pop(0)  # FIFO eviction
        
        logger.debug(f"Generated scenario: {scenario.name} with {len(expanded)} elements")
        return scenario
    
    def explore_possibilities(self, num_scenarios: int = 5) -> List[DreamScenario]:
        """Explore multiple possible futures.
        
        Args:
            num_scenarios: Number of scenarios to explore
            
        Returns:
            List of explored scenarios
        """
        scenarios = []
        base_concepts = ['growth', 'harmony', 'evolution', 'discovery']
        
        for i in range(num_scenarios):
            seed = random.sample(base_concepts, k=random.randint(1, 3))
            scenario = self.generate_scenario(seed)
            scenarios.append(scenario)
        
        logger.info(f"Explored {num_scenarios} possibilities")
        return scenarios
    
    def awaken(self) -> Dict[str, Any]:
        """Awaken from dream and return insights.
        
        Returns:
            Dream insights and memories
        """
        self.state = DreamState.AWAKE
        
        if not self.dream_memory:
            return {'insights': [], 'patterns': []}
        
        # Extract patterns from dreams
        all_elements = set()
        for dream in self.dream_memory:
            all_elements.update(dream.elements)
        
        patterns = list(all_elements)[:10]
        avg_creativity = sum(d.creativity_score for d in self.dream_memory) / len(self.dream_memory)
        
        return {
            'insights': patterns,
            'avg_creativity': avg_creativity,
            'dream_count': len(self.dream_memory),
            'most_creative': max(self.dream_memory, key=lambda d: d.creativity_score).name
        }


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    dream = DreamAgent()
    dream.enter_dream(depth=0.8)
    
    scenarios = dream.explore_possibilities(num_scenarios=3)
    print(f"Generated {len(scenarios)} dream scenarios")
    
    insights = dream.awaken()
    print(f"Dream insights: {insights}")
