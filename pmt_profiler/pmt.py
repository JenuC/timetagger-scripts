"""PMT control functions for PMT Profiler analysis."""

import time
from rich.console import Console
from rich.progress import Progress
from .core import MicroManager, MockMicroManager

console = Console()

def start_cooler(mmc: MicroManager, channel: str = 'C3', cooling_time: float = 5.0) -> None:
    """Start PMT cooler with a timer.
    
    Args:
        mmc: Micro-Manager instance
        channel: PMT channel (default: C3)
        cooling_time: Time to wait for cooling in seconds (default: 5.0)
    """
    with Progress() as progress:
        task = progress.add_task("[cyan]Starting PMT cooler...", total=int(cooling_time))
        
        # Set cooler parameters
        mmc.setProperty('DCCModule1', f'{channel}_CoolerVoltage', 2.6)
        mmc.setProperty('DCCModule1', f'{channel}_Cooling', 'On')
        mmc.setProperty('DCCModule1', f'{channel}_CoolerCurrentLimit', 1.0)
        
        # Wait for specified time with progress bar
        while not progress.finished:
            time.sleep(1)
            progress.update(task, advance=1)
            
    console.print("[green]PMT cooler started successfully")

def start_PMT(mmc: MicroManager, gain: int, channel: str = 'C3', cooling_time: float = 5.0) -> None:
    """Start PMT with specified gain and channel.
    
    Args:
        mmc: Micro-Manager instance
        gain: PMT gain value
        channel: PMT channel (default: C3)
        cooling_time: Time to wait for cooling in seconds (default: 5.0). Set to 0 to skip cooling.
    """
    # Start the cooler first if cooling time is greater than 0
    if cooling_time > 0:
        start_cooler(mmc, channel, cooling_time)
    else:
        console.print("[red]Warning: PMT cooler is not being used!")
    
    # Set gain for the specified channel
    mmc.setProperty('DCCModule1', channel+'_GainHV', gain)
    # Enable outputs
    mmc.setProperty('DCCModule1', 'EnableOutputs', 'On')
    # Enable +12V for the channel
    mmc.setProperty('DCCModule1', channel+'_Plus12V', 'On')
    # Wait for device to complete operations
    mmc.waitForDevice('DCCModule1')
    console.print(f"[green]PMT started on channel {channel} with gain {gain}")

def stop_PMT(mmc: MicroManager, gain: int = 0, channel: str = 'C3') -> None:
    """Stop PMT by setting gain to 0 and disabling outputs.
    
    Args:
        mmc: Micro-Manager instance
        gain: Final gain value (default: 0)
        channel: PMT channel (default: C3)
    """
    # Set gain to 0 for the specified channel
    mmc.setProperty('DCCModule1', channel+'_GainHV', gain)
    # Disable outputs
    mmc.setProperty('DCCModule1', 'EnableOutputs', 'Off')
    # Disable +12V for the channel
    mmc.setProperty('DCCModule1', channel+'_Plus12V', 'Off')
    # Turn off cooling
    mmc.setProperty('DCCModule1', f'{channel}_Cooling', 'Off')
    # Wait for device to complete operations
    mmc.waitForDevice('DCCModule1')
    console.print(f"[red]PMT stopped on channel {channel}") 