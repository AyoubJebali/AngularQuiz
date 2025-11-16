"""Test fixtures and sample data for the quiz application.

This module provides test data fixtures that can be used across
different test modules to ensure consistent test data.
"""

from .test_data import SAMPLE_QUIZ_DATA, SAMPLE_USERS

# Make it easy to import test data from anywhere in tests
__all__ = ["SAMPLE_QUIZ_DATA", "SAMPLE_USERS"]
