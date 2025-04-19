"""Tests for PMT functionality."""

import pytest
from pmt_profiler.pmt import start_PMT, stop_PMT

def test_start_pmt(mock_mm):
    """Test starting the PMT."""
    start_PMT(mock_mm, gain=65, channel='C3')
    # In a real test, we would capture the output and verify the correct
    # properties were set. For now, we're just testing that it doesn't raise exceptions.

def test_stop_pmt(mock_mm):
    """Test stopping the PMT."""
    stop_PMT(mock_mm, gain=0, channel='C3')
    # In a real test, we would capture the output and verify the correct
    # properties were set. For now, we're just testing that it doesn't raise exceptions. 