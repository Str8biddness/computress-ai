# src/integration/aios_connector.py
"""
AIOS Connector Module

This module provides a connector to an external AI Operating System (AIOS).
It handles connection, data exchange, and integration with the consciousness
modeling system.

Key Features:
- AIOSConnector: Manages connection to AIOS.
- Data synchronization and command execution.
- Error handling and reconnection logic.

Usage: from src.integration.aios_connector import AIOSConnector

connector = AIOSConnector(host="localhost", port=8080)
connector.connect()
data = connector.fetch_data("consciousness_metrics")
"""

import socket
import json
import time
import logging
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIOSConnector:
    """Connector for interacting with AI Operating System."""

    def __init__(self, host: str, port: int, timeout: int = 10):
        """
        Initialize the connector.

        Args:
            host: AIOS host.
            port: AIOS port.
            timeout: Connection timeout.
        """
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket: Optional[socket.socket] = None
        self.connected = False

    def connect(self) -> bool:
        """
        Connect to AIOS.

        Returns:
            True if connected, False otherwise.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            self.connected = True
            logger.info(f"Connected to AIOS at {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to AIOS: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """
        Disconnect from AIOS.
        """
        if self.socket:
            self.socket.close()
        self.connected = False
        logger.info("Disconnected from AIOS")

    def send_command(self, command: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Send a command to AIOS.

        Args:
            command: Command name.
            params: Command parameters.

        Returns:
            Response from AIOS or None if failed.
        """
        if not self.connected:
            logger.warning("Not connected to AIOS")
            return None
        try:
            message = json.dumps({"command": command, "params": params}).encode()
            self.socket.sendall(message)
            response = self.socket.recv(4096).decode()
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error sending command to AIOS: {e}")
            return None

    def fetch_data(self, data_type: str) -> Optional[Any]:
        """
        Fetch data from AIOS.

        Args:
            data_type: Type of data to fetch.

        Returns:
            Fetched data or None.
        """
        response = self.send_command("fetch_data", {"type": data_type})
        if response and "data" in response:
            return response["data"]
        return None

    def push_data(self, data_type: str, data: Any) -> bool:
        """
        Push data to AIOS.

        Args:
            data_type: Type of data.
            data: Data to push.

        Returns:
            True if successful, False otherwise.
        """
        response = self.send_command("push_data", {"type": data_type, "data": data})
        return response and response.get("status") == "success"

    def is_connected(self) -> bool:
        """
        Check if connected to AIOS.

        Returns:
            True if connected, False otherwise.
        """
        return self.connected

    def reconnect(self) -> bool:
        """
        Attempt to reconnect to AIOS.

        Returns:
            True if reconnected, False otherwise.
        """
        self.disconnect()
        time.sleep(1)  # Wait before reconnecting
        return self.connect()
