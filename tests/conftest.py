"""Common test fixtures for PMT Profiler tests."""

import pytest
from pmt_profiler.core import MockMicroManager

@pytest.fixture
def mock_mm():
    """Fixture that provides a mock Micro-Manager instance."""
    return MockMicroManager() 