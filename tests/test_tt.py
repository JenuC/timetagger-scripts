"""Tests for TimeTagger functionality."""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from pmt_profiler.tt import TimeTaggerManager, TIMETAGGER_AVAILABLE

# Skip all tests if TimeTagger is not available
pytestmark = pytest.mark.skipif(
    not TIMETAGGER_AVAILABLE,
    reason="TimeTagger module is not available"
)

@pytest.fixture
def mock_timetagger():
    """Fixture that provides a mock TimeTagger instance."""
    with patch('TimeTagger.createTimeTagger') as mock_create:
        mock_tagger = MagicMock()
        mock_create.return_value = mock_tagger
        yield mock_tagger

def test_timetagger_initialization(mock_timetagger):
    """Test that TimeTaggerManager initializes correctly."""
    tt = TimeTaggerManager()
    assert tt.tagger == mock_timetagger
    mock_timetagger.reset.assert_called_once()
    mock_timetagger.clearOverflows.assert_called_once()

def test_set_trigger_level(mock_timetagger):
    """Test setting trigger level."""
    tt = TimeTaggerManager()
    tt.set_trigger_level(-1, -0.01)
    mock_timetagger.setTriggerLevel.assert_called_once_with(-1, -0.01)

def test_get_darkcounts(mock_timetagger):
    """Test getting dark counts."""
    tt = TimeTaggerManager()
    
    # Mock the Counter class
    mock_counter = MagicMock()
    mock_counter.isRunning.side_effect = [True, True, False]  # Run twice, then stop
    mock_counter.getData.return_value = [100.0, 200.0]
    
    # Mock tqdm to prevent actual progress bar display during tests
    with patch('TimeTagger.Counter', return_value=mock_counter), \
         patch('pmt_profiler.tt.tqdm') as mock_tqdm:
        # Configure mock tqdm instance
        mock_progress = MagicMock()
        mock_progress.start_t = 0
        mock_tqdm.return_value = mock_progress
        
        data = tt.get_darkcounts([-1, 1], collection_time_sec=1, timing_resolution_sec=1)
        
        assert data == [100.0, 200.0]
        mock_counter.startFor.assert_called_once()
        mock_tqdm.assert_called_once()
        mock_progress.close.assert_called_once()

def test_close(mock_timetagger):
    """Test closing TimeTagger resources."""
    tt = TimeTaggerManager()
    tt.close()
    assert tt.tagger is None

def test_timetagger_not_available():
    """Test behavior when TimeTagger is not available."""
    with patch('pmt_profiler.tt.TIMETAGGER_AVAILABLE', False):
        with pytest.raises(RuntimeError, match="TimeTagger module is not available"):
            TimeTaggerManager() 