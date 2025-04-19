"""Command-line interface for PMT Profiler analysis."""

import argparse
from rich.console import Console
from rich.table import Table
from .core import MockMicroManager, MicroManager
from .pmt import start_PMT, stop_PMT

console = Console()

def get_device_info(mmc):
    """Print information about loaded devices and their properties."""
    print("Loaded devices:", mmc.getLoadedDevices())
    for dev in mmc.getLoadedDevices():
        print(f"{dev}: {mmc.getDevicePropertyNames(dev)}")

def get_DCC_DCU_properties(mmc):
    """Get properties of DCC_DCU module."""
    # Get device adapter names with BH
    device_adapter_names = mmc.getDeviceAdapterNames()
    bh_devices = [k for k in device_adapter_names if 'BH' in k]
    print("\nBH devices available as dll:", bh_devices)
    
    # Find properties of BH_DCC_DCU adapter
    device = mmc.getDeviceObject('DCCHub')
    
    # Create a table for device properties using rich
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    for prop in device.properties:
        table.add_row(prop.name, str(prop.value))
    
    console.print(table)
    
    # Get the property names of one of BH DCC_DCU module
    props = mmc.getDevicePropertyNames('DCCModule1')
    print("\nDCCModule1 Properties:")
    for prop in props:
        print(prop)

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