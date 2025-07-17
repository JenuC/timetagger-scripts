#!/usr/bin/env python
"""Module to control Tektronix MDO32 oscilloscope using tm_devices."""

import os
import sys
import time
from datetime import datetime
from tm_devices import DeviceManager
from tm_devices.drivers.pi.mdo.mdo3k import MDO3K
from rich.console import Console
from rich.progress import Progress

console = Console()

def connect_to_oscilloscope(ip_address: str = None) -> MDO3K:
    """Connect to the MDO32 oscilloscope.
    
    Args:
        ip_address: IP address of the oscilloscope (optional)
        
    Returns:
        MDO3K: Connected oscilloscope instance
    """
    # Create device manager
    dm = DeviceManager()
    
    # Connect to the oscilloscope
    if ip_address:
        scope = dm.add_mdo3k(ip_address)
    else:
        # Try to find the first available MDO3K
        scopes = dm.list_devices(device_type="MDO3K")
        if not scopes:
            raise RuntimeError("No MDO3K oscilloscopes found")
        scope = dm.add_mdo3k(scopes[0])
    
    console.print(f"[green]Connected to {scope.model} at {scope.resource_name}")
    return scope

def load_settings(scope: MDO3K, settings_file: str) -> None:
    """Load settings from a file into the oscilloscope.
    
    Args:
        scope: MDO3K oscilloscope instance
        settings_file: Path to the settings file
    """
    if not os.path.exists(settings_file):
        raise FileNotFoundError(f"Settings file not found: {settings_file}")
    
    console.print(f"[cyan]Loading settings from {settings_file}...")
    scope.commands.recall.setup.write(f'"{settings_file}"')
    console.print("[green]Settings loaded successfully")

def capture_waveform(scope: MDO3K, channel: int = 1) -> None:
    """Capture a waveform from the specified channel.
    
    Args:
        scope: MDO3K oscilloscope instance
        channel: Channel number to capture
    """
    console.print(f"[cyan]Capturing waveform from channel {channel}...")
    
    # Set up acquisition
    scope.commands.acquire.state.write("RUN")
    scope.commands.acquire.stopafter.write("SEQUENCE")
    scope.commands.acquire.numacq.write(1)
    
    # Wait for acquisition to complete
    with Progress() as progress:
        task = progress.add_task("[cyan]Waiting for acquisition...", total=100)
        while scope.commands.acquire.state.query() == "RUN":
            time.sleep(0.1)
            progress.update(task, advance=1)
    
    console.print("[green]Waveform captured successfully")

def export_waveform(scope: MDO3K, channel: int = 1, filename: str = None) -> str:
    """Export the captured waveform to a file.
    
    Args:
        scope: MDO3K oscilloscope instance
        channel: Channel number to export
        filename: Output filename (optional)
        
    Returns:
        str: Path to the exported file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"waveform_ch{channel}_{timestamp}.csv"
    
    console.print(f"[cyan]Exporting waveform to {filename}...")
    
    # Set up data export
    scope.commands.data.source.write(f"CH{channel}")
    scope.commands.data.start.write(1)
    scope.commands.data.stop.write(1000)  # Adjust based on your needs
    scope.commands.data.encdg.write("ASCII")
    scope.commands.data.filename.write(f'"{filename}"')
    
    # Export the data
    scope.commands.data.export.write()
    
    console.print("[green]Waveform exported successfully")
    return filename

def main():
    """Main function to run the script."""
    try:
        # Parse command line arguments
        import argparse
        parser = argparse.ArgumentParser(description="Control Tektronix MDO32 oscilloscope")
        parser.add_argument("--ip", help="IP address of the oscilloscope")
        parser.add_argument("--settings", help="Path to settings file")
        parser.add_argument("--channel", type=int, default=1, help="Channel number (default: 1)")
        parser.add_argument("--output", help="Output filename for waveform data")
        args = parser.parse_args()
        
        # Connect to the oscilloscope
        scope = connect_to_oscilloscope(args.ip)
        
        # Load settings if provided
        if args.settings:
            load_settings(scope, args.settings)
        
        # Capture and export waveform
        capture_waveform(scope, args.channel)
        export_waveform(scope, args.channel, args.output)
        
    except Exception as e:
        console.print(f"[red]Error: {e}")
        sys.exit(1)
    finally:
        # Clean up
        if 'scope' in locals():
            scope.close()
            console.print("[green]Oscilloscope connection closed")

if __name__ == "__main__":
    main() 