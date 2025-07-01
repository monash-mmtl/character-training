"""
Multi-Med: Medical AI Diagnostic Benchmark

A sophisticated medical diagnostic system that simulates doctor-patient interactions using multiple AI agents to diagnose medical cases.
"""

from .llm_config import get_model_config
from .agents import process_single_case

__version__ = "1.0.0"
__all__ = [
    'get_model_config',
    'process_single_case'
] 