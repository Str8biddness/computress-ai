# src/integration/api_server.py
"""
API Server Module

This module provides a REST API server for interacting with the consciousness
modeling system. It exposes endpoints for agents, symbolic operations, and
system status.

Key Features:
- APIServer: Flask-based REST API server.
- Endpoints for agent management, symbolic evaluation, and status.
- JSON-based communication.

Usage: from src.integration.api_server import APIServer

server = APIServer()
server.run()
"""

from flask import Flask, request, jsonify
import logging
from typing import Dict, Any

from .uscl_interface import USCLInterface
from ..symbolic_engine.expression_eval import ExpressionEvaluator, Parser

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIServer:
    """REST API server for the system."""

    def __init__(self, host: str = "0.0.0.0", port: int = 5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.uscl_interface = USCLInterface()
        self.evaluator = ExpressionEvaluator()
        self.parser = Parser()
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/status', methods=['GET'])
        def get_status():
            return jsonify({"status": "running", "message": "API server is active"})

        @self.app.route('/evaluate', methods=['POST'])
        def evaluate_expression():
            data = request.json
            expression = data.get('expression')
            context = data.get('context', {})
            if not expression:
                return jsonify({"error": "Expression required"}), 400
            result = self.evaluator.evaluate(self.parser.parse(expression), **context)
            return jsonify({"result": result})

        @self.app.route('/uscl/parse', methods=['POST'])
        def parse_uscl():
            data = request.json
            expression = data.get('expression')
            if not expression:
                return jsonify({"error": "Expression required"}), 400
            parsed = self.uscl_interface.parse_expression(expression)
            return jsonify({"parsed": parsed})

        @self.app.route('/uscl/generate', methods=['POST'])
        def generate_uscl():
            data = request.json
            data_dict = data.get('data')
            if not data_dict:
                return jsonify({"error": "Data required"}), 400
            generated = self.uscl_interface.generate_expression(data_dict)
            return jsonify({"generated": generated})

    def run(self):
        """
        Run the API server.
        """
        logger.info(f"Starting API server on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)
