"""TimeTagger control functions for PMT Profiler analysis."""

import time
from typing import List, Optional
from rich.console import Console

console = Console()

try:
    import TimeTagger as TT
    from TimeTagger import Countrate, Counter
    TIMETAGGER_AVAILABLE = True
except ImportError:
    TIMETAGGER_AVAILABLE = False
    console.print("[yellow]TimeTagger module not found. TimeTagger functionality will be disabled.")

class TimeTaggerManager:
    """Manager class for TimeTagger operations."""
    
    def __init__(self):
        """Initialize TimeTagger and reset settings."""
        if not TIMETAGGER_AVAILABLE:
            raise RuntimeError("TimeTagger module is not available")
            
        self.tagger = TT.createTimeTagger()
        self.reset()
        
    def reset(self) -> None:
        """Reset the TimeTagger and clear overflows."""
        if not TIMETAGGER_AVAILABLE:
            raise RuntimeError("TimeTagger module is not available")
            
        self.tagger.reset()
        self.tagger.clearOverflows()
        console.print("[green]TimeTagger reset and overflows cleared")
        
    def set_trigger_level(self, channel: int, level: float) -> None:
        """Set trigger level for a channel.
        
        Args:
            channel: Channel number
            level: Trigger level in volts
        """
        if not TIMETAGGER_AVAILABLE:
            raise RuntimeError("TimeTagger module is not available")
            
        self.tagger.setTriggerLevel(channel, level)
        console.print(f"[green]Set trigger level for channel {channel} to {level}V")
        
    def get_darkcounts(
        self,
        channels: List[int],
        collection_time_sec: float = 5,
        timing_resolution_sec: float = 1
    ) -> List[float]:
        """Get dark counts from specified channels.
        
        Args:
            channels: List of channel numbers to measure
            collection_time_sec: Total collection time in seconds
            timing_resolution_sec: Time resolution in seconds
            
        Returns:
            List of count rates for each channel
        """
        if not TIMETAGGER_AVAILABLE:
            raise RuntimeError("TimeTagger module is not available")
            
        binwidth = timing_resolution_sec * 1E12  # Convert to picoseconds
        n_values = int(collection_time_sec / timing_resolution_sec)
        
        with console.status("[cyan]Collecting dark counts...") as status:
            counter = Counter(self.tagger, channels, binwidth, n_values)
            counter.startFor(capture_duration=binwidth * n_values)
            
            while counter.isRunning():
                time.sleep(0.1)  # Check every 100ms
                
            data = counter.getData()
            
        console.print(f"[green]Dark counts collected for {len(channels)} channels")
        return data
        
    def close(self) -> None:
        """Clean up TimeTagger resources."""
        if hasattr(self, 'tagger'):
            self.tagger = None
            console.print("[green]TimeTagger resources cleaned up") 