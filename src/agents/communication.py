# src/agents/communication.py
"""
Communication Module for Agents

This module handles inter-agent communication, including message passing,
protocols, and event handling. It supports various communication patterns
like point-to-point, broadcast, and publish-subscribe.

Key Features:
- Message: Data class for messages.
- CommunicationHub: Central hub for managing communications.
- Protocols: Support for different communication patterns.
- Event handling for asynchronous communication.

Usage: from src.agents.communication import CommunicationHub, Message

hub = CommunicationHub()
hub.register_agent("agent1")
message = Message(sender="agent1", receiver="agent2", content="Hello")
hub.send_message(message)
"""

from typing import Dict, List, Any, Optional, Callable
import time
import logging
from dataclasses import dataclass
from enum import Enum
from queue import Queue
import threading

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Types of messages."""
    INFO = "info"
    REQUEST = "request"
    RESPONSE = "response"
    COMMAND = "command"
    EVENT = "event"

@dataclass
class Message:
    """Represents a message between agents."""
    sender: str
    receiver: Optional[str]  # None for broadcast
    content: Any
    message_type: MessageType = MessageType.INFO
    timestamp: float = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()
        if self.metadata is None:
            self.metadata = {}

class CommunicationHub:
    """Central hub for agent communications."""

    def __init__(self):
        self.agents: Dict[str, Queue] = {}  # agent_name: message_queue
        self.subscriptions: Dict[str, List[str]] = {}  # topic: list of agent_names
        self.event_handlers: Dict[str, List[Callable]] = {}  # event_type: list of handlers
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def register_agent(self, agent_name: str):
        """
        Register an agent with the hub.

        Args:
            agent_name: Name of the agent.
        """
        if agent_name not in self.agents:
            self.agents[agent_name] = Queue()
            logger.info(f"Agent {agent_name} registered with communication hub.")
        else:
            logger.warning(f"Agent {agent_name} already registered.")

    def unregister_agent(self, agent_name: str):
        """
        Unregister an agent from the hub.

        Args:
            agent_name: Name of the agent.
        """
        if agent_name in self.agents:
            del self.agents[agent_name]
            # Remove from subscriptions
            for topic, subscribers in self.subscriptions.items():
                if agent_name in subscribers:
                    subscribers.remove(agent_name)
            logger.info(f"Agent {agent_name} unregistered from communication hub.")
        else:
            logger.warning(f"Agent {agent_name} not registered.")

    def send_message(self, message: Message):
        """
        Send a message to an agent or broadcast.

        Args:
            message: The message to send.
        """
        if message.receiver is None:
            # Broadcast
            for agent_queue in self.agents.values():
                agent_queue.put(message)
            logger.info(f"Broadcast message from {message.sender}: {message.content}")
        elif message.receiver in self.agents:
            self.agents[message.receiver].put(message)
            logger.info(f"Message sent from {message.sender} to {message.receiver}: {message.content}")
        else:
            logger.warning(f"Receiver {message.receiver} not registered.")

    def publish_event(self, topic: str, content: Any, sender: str):
        """
        Publish an event to subscribed agents.

        Args:
            topic: Event topic.
            content: Event content.
            sender: Sender agent name.
        """
        if topic in self.subscriptions:
            message = Message(sender=sender, receiver=None, content=content, message_type=MessageType.EVENT)
            for agent_name in self.subscriptions[topic]:
                if agent_name in self.agents:
                    self.agents[agent_name].put(message)
            logger.info(f"Event published to topic '{topic}' by {sender}: {content}")
        else:
            logger.warning(f"No subscribers for topic '{topic}'.")

    def subscribe_to_topic(self, agent_name: str, topic: str):
        """
        Subscribe an agent to a topic.

        Args:
            agent_name: Name of the agent.
            topic: Topic to subscribe to.
        """
        if agent_name not in self.agents:
            logger.warning(f"Agent {agent_name} not registered.")
            return
        if topic not in self.subscriptions:
            self.subscriptions[topic] = []
        if agent_name not in self.subscriptions[topic]:
            self.subscriptions[topic].append(agent_name)
            logger.info(f"Agent {agent_name} subscribed to topic '{topic}'.")

    def unsubscribe_from_topic(self, agent_name: str, topic: str):
        """
        Unsubscribe an agent from a topic.

        Args:
            agent_name: Name of the agent.
            topic: Topic to unsubscribe from.
        """
        if topic in self.subscriptions and agent_name in self.subscriptions[topic]:
            self.subscriptions[topic].remove(agent_name)
            logger.info(f"Agent {agent_name} unsubscribed from topic '{topic}'.")

    def get_messages(self, agent_name: str) -> List[Message]:
        """
        Get pending messages for an agent.

        Args:
            agent_name: Name of the agent.

        Returns:
            List of messages.
        """
        if agent_name not in self.agents:
            logger.warning(f"Agent {agent_name} not registered.")
            return []
        messages = []
        while not self.agents[agent_name].empty():
            messages.append(self.agents[agent_name].get())
        return messages

    def register_event_handler(self, event_type: str, handler: Callable):
        """
        Register an event handler.

        Args:
            event_type: Type of event.
            handler: Handler function.
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
        logger.info(f"Event handler registered for '{event_type}'.")

    def trigger_event(self, event_type: str, **kwargs):
        """
        Trigger an event and call handlers.

        Args:
            event_type: Type of event.
            **kwargs: Event data.
        """
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(**kwargs)
                except Exception as e:
                    logger.error(f"Error in event handler for '{event_type}': {e}")

    def start(self):
        """
        Start the communication hub.
        """
        self.running = True
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.start()
        logger.info("Communication hub started.")

    def stop(self):
        """
        Stop the communication hub.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("Communication hub stopped.")

    def _run_loop(self):
        """
        Internal run loop for processing.
        """
        while self.running:
            # Process any global events or maintenance
            time.sleep(0.1)

    def get_status(self) -> Dict[str, Any]:
        """
        Get the status of the communication hub.

        Returns:
            Dictionary with status information.
        """
        return {
            'registered_agents': list(self.agents.keys()),
            'topics': list(self.subscriptions.keys()),
            'event_handlers': list(self.event_handlers.keys()),
            'running': self.running
        }
