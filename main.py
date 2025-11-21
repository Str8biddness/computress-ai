# main.py
"""
Main Entry Point

This is the main entry point for the Computress AI consciousness modeling system.
It initializes components, starts the system, and handles shutdown.

Usage: python main.py
"""

import signal
import sys
import logging
import json
from typing import Dict, Any

from src.integration.api_server import APIServer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config() -> Dict[str, Any]:
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load config.json: {e}. Using defaults.")
        return {}

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("Shutdown signal received. Exiting gracefully...")
    sys.exit(0)

def main():
    """Main entry point"""
    logger.info("Starting Computress AI System...")
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Load configuration
    config = load_config()
    logger.info(f"Loaded configuration: {config.get('system', {}).get('name', 'Computress AI')}")
    
    # Initialize API server
    api_config = config.get('api', {})
    host = api_config.get('host', '0.0.0.0')
    port = api_config.get('port', 5000)
    
    logger.info(f"Starting API server on {host}:{port}")
    server = APIServer(host=host, port=port)
    
    try:
        server.run()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
    except Exception as e:
        logger.error(f"Error running server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
