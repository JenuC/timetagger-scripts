"""PMT control functions for PMT Profiler analysis."""

from .core import MicroManager, MockMicroManager

def start_PMT(mmc: MicroManager, gain: int, channel: str = 'C3') -> None:
    """Start PMT with specified gain and channel."""
    # Set gain for the specified channel
    mmc.setProperty('DCCModule1', channel+'_GainHV', gain)
    # Enable outputs
    mmc.setProperty('DCCModule1', 'EnableOutputs', 'On')
    # Enable +12V for the channel
    mmc.setProperty('DCCModule1', channel+'_Plus12V', 'On')
    # Wait for device to complete operations
    mmc.waitForDevice('DCCModule1')
    print(f"PMT started on channel {channel} with gain {gain}")

def stop_PMT(mmc: MicroManager, gain: int = 0, channel: str = 'C3') -> None:
    """Stop PMT by setting gain to 0 and disabling outputs."""
    # Set gain to 0 for the specified channel
    mmc.setProperty('DCCModule1', channel+'_GainHV', gain)
    # Disable outputs
    mmc.setProperty('DCCModule1', 'EnableOutputs', 'Off')
    # Disable +12V for the channel
    mmc.setProperty('DCCModule1', channel+'_Plus12V', 'Off')
    # Wait for device to complete operations
    mmc.waitForDevice('DCCModule1')
    print(f"PMT stopped on channel {channel}") 