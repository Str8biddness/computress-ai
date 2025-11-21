# src/agents/base_agent.py
"""
Base Agent Module

This module defines the base agent class for consciousness modeling agents.
It includes agent lifecycle management, state handling, perception-action loops,
goal management, and integration with symbolic reasoning.

Key Features:
- BaseAgent: Abstract base class for agents.
- Lifecycle methods: initialize, run, shutdown.
- State management: Tracks agent state, beliefs, goals.
- Perception-Action Loop: perceive, reason, act cycle.
- Goal Handling: Set, update, and check goals.
- Symbolic Reasoning: Integrates with symbolic engine for reasoning.

Usage: from src.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def perceive(self, inputs):
        # Custom perception logic
        pass

agent = MyAgent()
agent.initialize()
agent.run()
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
import time
import logging
from enum import Enum
from dataclasses import dataclass

# Assuming imports from other modules
from ..symbolic_engine.expression_eval import ExpressionEvaluator
from ..consciousness.awareness_states import AwarenessManager, AwarenessState
from ..consciousness.attention import AttentionManager
from ..consciousness.metacognition import MetacognitiveProcessor

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(Enum):
    """Enumeration of agent states."""
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    SHUTTING_DOWN = "shutting_down"
    TERMINATED = "terminated"

@dataclass
class Goal:
    """Represents an agent goal."""
    name: str
    description: str
    priority: float  # 0.0 to 1.0
    achieved: bool = False
    deadline: Optional[float] = None  # Timestamp

    def is_achieved(self) -> bool:
        """
        Check if the goal is achieved.

        Returns:
            True if achieved, False otherwise.
        """
        return self.achieved

    def check_deadline(self) -> bool:
        """
        Check if the goal has passed its deadline.

        Returns:
            True if deadline passed, False otherwise.
        """
        if self.deadline and time.time() > self.deadline:
            return True
        return False

class BaseAgent(ABC):
    """Abstract base class for agents in the consciousness model."""

    def __init__(self, name: str):
        """
        Initialize the base agent.

        Args:
            name: Name of the agent.
        """
        self.name = name
        self.state = AgentState.INITIALIZING
        self.beliefs: Dict[str, Any] = {}  # Agent's beliefs (could include symbolic expressions)
        self.goals: List[Goal] = []
        self.perception_history: List[Dict[str, Any]] = []
        self.action_history: List[Dict[str, Any]] = []

        # Consciousness components
        self.awareness_manager = AwarenessManager()
        self.attention_manager = AttentionManager()
        self.metacognition_processor = MetacognitiveProcessor()

        # Symbolic reasoning (placeholder for integration)
        self.symbolic_knowledge: Dict[str, Any] = {}

        self.start_time = time.time()
        logger.info(f"Agent {self.name} initialized.")

    def initialize(self):
        """
        Initialize the agent. Override in subclasses for custom setup.
        """
        self.state = AgentState.RUNNING
        self.awareness_manager.transition_to(AwarenessState.AWAKE)
        logger.info(f"Agent {self.name} started running.")

    def run(self):
        """
        Main run loop for the agent. Implements the perception-action loop.
        """
        while self.state == AgentState.RUNNING:
            try:
                # Perception
                inputs = self.perceive()

                # Reason
                reasoning_output = self.reason(inputs)

                # Act
                self.act(reasoning_output)

                # Update state
                self.update_state()

                # Small delay to simulate real-time processing
                time.sleep(0.1)

            except Exception as e:
                logger.error(f"Error in agent {self.name} run loop: {e}")
                self.shutdown()

    def shutdown(self):
        """
        Shutdown the agent.
        """
        self.state = AgentState.SHUTTING_DOWN
        logger.info(f"Agent {self.name} shutting down.")
        # Perform cleanup
        self.state = AgentState.TERMINATED
        logger.info(f"Agent {self.name} terminated.")

    @abstractmethod
    def perceive(self) -> Dict[str, Any]:
        """
        Perceive the environment. Must be implemented by subclasses.

        Returns:
            Dictionary of perceived inputs.
        """
        pass

    def reason(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reason based on inputs. Uses symbolic reasoning and consciousness components.

        Args:
            inputs: Perceived inputs.

        Returns:
            Dictionary of reasoning outputs.
        """
        # Update beliefs
        self.update_beliefs(inputs)

        # Check goals
        active_goals = [g for g in self.goals if not g.is_achieved()]

        # Symbolic reasoning (basic example)
        reasoning_result = self.symbolic_reasoning(inputs)

        # Metacognitive reflection
        self.metacognition_processor.introspect("Current reasoning process", depth=0.5)

        return {
            'active_goals': active_goals,
            'reasoning_result': reasoning_result,
            'suggested_actions': self.generate_actions(reasoning_result)
        }

    @abstractmethod
    def act(self, reasoning_output: Dict[str, Any]):
        """
        Act based on reasoning output. Must be implemented by subclasses.

        Args:
            reasoning_output: Output from reasoning.
        """
        pass

    def update_state(self):
        """
        Update the agent's internal state.
        """
        # Update awareness based on activity
        if self.attention_manager.measure_attention_intensity() > 0.8:
            self.awareness_manager.transition_to(AwarenessState.FOCUSED)

        # Check for goal achievements
        for goal in self.goals:
            if not goal.is_achieved() and self.check_goal_achievement(goal):
                goal.achieved = True
                logger.info(f"Goal '{goal.name}' achieved by agent {self.name}.")

        # Remove expired goals
        self.goals = [g for g in self.goals if not g.check_deadline() or g.is_achieved()]

    def set_goal(self, name: str, description: str, priority: float, deadline: Optional[float] = None):
        """
        Set a new goal for the agent.

        Args:
            name: Goal name.
            description: Goal description.
            priority: Priority (0.0 to 1.0).
            deadline: Optional deadline timestamp.
        """
        goal = Goal(name=name, description=description, priority=priority, deadline=deadline)
        self.goals.append(goal)
        logger.info(f"Goal '{name}' set for agent {self.name}.")

    def update_beliefs(self, inputs: Dict[str, Any]):
        """
        Update agent beliefs based on inputs.

        Args:
            inputs: New inputs to incorporate.
        """
        self.beliefs.update(inputs)
        # Could integrate symbolic updates here

    def symbolic_reasoning(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform symbolic reasoning. Placeholder for integration with symbolic engine.

        Args:
            inputs: Inputs for reasoning.

        Returns:
            Reasoning results.
        """
        # Example: Simple rule-based reasoning
        result = {}
        if 'stimulus' in inputs:
            result['inference'] = f"Processed stimulus: {inputs['stimulus']}"
        return result

    def generate_actions(self, reasoning_result: Dict[str, Any]) -> List[str]:
        """
        Generate possible actions based on reasoning.

        Args:
            reasoning_result: Results from reasoning.

        Returns:
            List of action suggestions.
        """
        actions = []
        if 'active_goals' in reasoning_result and reasoning_result['active_goals']:
            actions.append("Pursue goals")
        if 'inference' in reasoning_result:
            actions.append("Log inference")
        return actions

    def check_goal_achievement(self, goal: Goal) -> bool:
        """
        Check if a goal is achieved. Override in subclasses for specific logic.

        Args:
            goal: The goal to check.

        Returns:
            True if achieved, False otherwise.
        """
        # Default: Assume not achieved; subclasses should implement
        return False

    def get_state_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the agent's current state.

        Returns:
            Dictionary with state information.
        """
        return {
            'name': self.name,
            'state': self.state.value,
            'awareness_state': self.awareness_manager.get_current_state().value if self.awareness_manager.get_current_state() else None,
            'attention_intensity': self.attention_manager.measure_attention_intensity(),
            'self_awareness': self.metacognition_processor.assess_self_awareness(),
            'active_goals': len([g for g in self.goals if not g.is_achieved()]),
            'beliefs_count': len(self.beliefs),
            'uptime': time.time() - self.start_time
        }

    def pause(self):
        """
        Pause the agent.
        """
        if self.state == AgentState.RUNNING:
            self.state = AgentState.PAUSED
            logger.info(f"Agent {self.name} paused.")

    def resume(self):
        """
        Resume the agent.
        """
        if self.state == AgentState.PAUSED:
            self.state = AgentState.RUNNING
            logger.info(f"Agent {self.name} resumed.")
