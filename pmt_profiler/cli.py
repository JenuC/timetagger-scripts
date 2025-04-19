"""Command-line interface for PMT Profiler analysis."""

import argparse
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from .core import MockMicroManager, MicroManager
from .pmt import start_PMT, stop_PMT

console = Console()

def get_device_info(mmc):
    """Print information about loaded devices and their properties."""
    # Create a table for devices
    devices_table = Table(title="Loaded Devices", show_header=True, header_style="bold magenta")
    devices_table.add_column("Device", style="cyan")
    devices_table.add_column("Properties", style="green")
    
    # Add each device and its properties to the table
    for dev in mmc.getLoadedDevices():
        props = mmc.getDevicePropertyNames(dev)
        devices_table.add_row(dev, ", ".join(props))
    
    console.print(devices_table)
    console.print()

def get_DCC_DCU_properties(mmc):
    """Get properties of DCC_DCU module."""
    # Get device adapter names with BH
    device_adapter_names = mmc.getDeviceAdapterNames()
    bh_devices = [k for k in device_adapter_names if 'BH' in k]
    
    # Create a table for BH devices
    bh_table = Table(title="BH Devices Available", show_header=True, header_style="bold magenta")
    bh_table.add_column("Device", style="cyan")
    
    for device in bh_devices:
        bh_table.add_row(device)
    
    console.print(bh_table)
    console.print()
    
    # Get properties for DCCModule1
    device_name = 'DCCModule1'
    props = mmc.getDevicePropertyNames(device_name)
    
    # Create a table for DCCModule1 properties with values
    dcc_table = Table(
        title=f"Properties and Values for {device_name}", 
        show_header=True, 
        header_style="bold magenta"
    )
    dcc_table.add_column("Property", style="cyan")
    dcc_table.add_column("Value", style="green")
    
    # Get each property value
    for prop in props:
        try:
            value = mmc.getProperty(device_name, prop)
            dcc_table.add_row(prop, str(value))
        except Exception as e:
            dcc_table.add_row(prop, f"Error: {str(e)}")
    
    console.print(dcc_table)
    console.print()
    
    # Get properties for DCCHub
    device_name = 'DCCHub'
    props = mmc.getDevicePropertyNames(device_name)
    
    # Create a table for DCCHub properties with values
    hub_table = Table(
        title=f"Properties and Values for {device_name}", 
        show_header=True, 
        header_style="bold magenta"
    )
    hub_table.add_column("Property", style="cyan")
    hub_table.add_column("Value", style="green")
    
    # Get each property value
    for prop in props:
        try:
            value = mmc.getProperty(device_name, prop)
            hub_table.add_row(prop, str(value))
        except Exception as e:
            hub_table.add_row(prop, f"Error: {str(e)}")
    
    console.print(hub_table)
    console.print()

def main():
    parser = argparse.ArgumentParser(
        description="PMT Profiler Analysis Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Start PMT with gain 65 on channel C3:
    python -m pmt_profiler.cli --pmt start --gain 65 --channel C3
  
  Stop PMT on channel C3:
    python -m pmt_profiler.cli --pmt stop --channel C3
  
  Run in mock mode (no hardware required):
    python -m pmt_profiler.cli --mock --pmt start --gain 65
        """
    )
    
    parser.add_argument(
        '--mock', 
        action='store_true', 
        help='Use mock Micro-Manager for testing without hardware'
    )
    
    parser.add_argument(
        '--pmt', 
        choices=['start', 'stop'], 
        help='Control PMT: start to enable, stop to disable'
    )
    
    parser.add_argument(
        '--channel', 
        default='C3', 
        help='PMT channel to control (default: C3)'
    )
    
    parser.add_argument(
        '--gain', 
        type=int, 
        default=65, 
        help='PMT gain value (default: 65)'
    )
    
    parser.add_argument(
        '--info', 
        action='store_true', 
        help='Display device information and properties'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize Micro-Manager - always use mock if --mock flag is provided
    try:
        mmc = MockMicroManager() if args.mock else MicroManager()
    except Exception as e:
        # If there's an error initializing the real Micro-Manager, fall back to mock
        print(f"Error initializing Micro-Manager: {e}")
        print("Falling back to mock Micro-Manager")
        mmc = MockMicroManager()
    
    # Display device information if requested
    if args.info:
        console.print(Panel.fit("Device Information", style="bold blue"))
        get_device_info(mmc)
        get_DCC_DCU_properties(mmc)
        return
    
    # Handle PMT control if requested
    if args.pmt == 'start':
        start_PMT(mmc, args.gain, args.channel)
    elif args.pmt == 'stop':
        stop_PMT(mmc, 0, args.channel)
    else:
        # If no specific action is requested, show help
        parser.print_help()

if __name__ == "__main__":
    main() 