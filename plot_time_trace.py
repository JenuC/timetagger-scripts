#!/usr/bin/env python3

import pathlib
from pymmcore_plus import CMMCorePlus, find_micromanager
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Initialize rich console
console = Console()

def setup_micro_manager():
    """Initialize and configure Micro-Manager."""
    with console.status("[bold green]Initializing Micro-Manager...") as status:
        mmc = CMMCorePlus()
        mm_path = r'C:/Program Files/Micro-Manager-nightly-markt'
        mmc.loadSystemConfiguration(f'{mm_path}/DCC_alone.cfg')
        console.print("[bold green]✓[/] Micro-Manager initialized successfully!")
    return mmc

def get_device_info(mmc):
    """Print information about loaded devices and their properties"""
    console.print("\n[bold blue]Loaded Devices Information[/]")
    
    # Create a table for devices
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Device", style="cyan")
    table.add_column("Properties", style="green")
    
    devices = mmc.getLoadedDevices()
    for dev in devices:
        props = mmc.getDevicePropertyNames(dev)
        table.add_row(dev, ", ".join(props))
    
    console.print(table)

def get_DCC_DCU_properties(mmc):
    """Get properties of DCC_DCU module"""
    console.print("\n[bold blue]DCC DCU Properties[/]")
    
    # Get device adapter names with BH
    device_adapter_names = mmc.getDeviceAdapterNames()
    bh_devices = [k for k in device_adapter_names if 'BH' in k]
    
    console.print(Panel.fit(
        "\n".join(bh_devices),
        title="[bold yellow]BH Devices Available as DLL[/]",
        border_style="yellow"
    ))
    
    # Find properties of BH_DCC_DCU adapter
    device = mmc.getDeviceObject('DCCHub')
    
    # Create a table for device properties
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    for prop in device.properties:
        table.add_row(prop.name, str(prop.value))
    
    console.print(table)
    
    # Get the property names of one of BH DCC_DCU module
    props = mmc.getDevicePropertyNames('DCCModule1')
    console.print("\n[bold blue]DCCModule1 Properties:[/]")
    console.print(Panel.fit(
        "\n".join(props),
        title="[bold yellow]Available Properties[/]",
        border_style="yellow"
    ))

def start_PMT(mmc, gain=65, ch='C3'):
    """Start PMT with specified gain and channel"""
    with console.status(f"[bold green]Starting PMT on channel {ch} with gain {gain}...") as status:
        mmc.setProperty('DCCModule1', ch+'_GainHV', gain)
        mmc.setProperty('DCCModule1', 'EnableOutputs', 'On')
        mmc.setProperty('DCCModule1', ch+'_Plus12V', 'On')
        mmc.waitForDevice('DCCModule1')
        console.print(f"[bold green]✓[/] PMT started successfully on channel {ch}")

def stop_PMT(mmc, gain=0, ch='C3'):
    """Stop PMT on specified channel"""
    with console.status(f"[bold red]Stopping PMT on channel {ch}...") as status:
        mmc.setProperty('DCCModule1', ch+'_GainHV', gain)
        mmc.setProperty('DCCModule1', 'EnableOutputs', 'Off')
        mmc.setProperty('DCCModule1', ch+'_Plus12V', 'Off')
        mmc.waitForDevice('DCCModule1')
        console.print(f"[bold red]✓[/] PMT stopped on channel {ch}")

def main():
    console.print(Panel.fit(
        "[bold yellow]Micro-Manager Time Tagger Analysis[/]\n"
        "[cyan]Version 1.0[/]",
        border_style="yellow"
    ))
    
    # Initialize Micro-Manager
    mmc = setup_micro_manager()
    
    # Print device information
    get_device_info(mmc)
    
    # Get available configurations
    config_groups = mmc.getAvailableConfigGroups()
    console.print("\n[bold blue]Available Config Groups:[/]")
    console.print(Panel.fit(
        "\n".join(config_groups),
        title="[bold yellow]Configuration Groups[/]",
        border_style="yellow"
    ))
    
    # Get DCC DCU properties
    get_DCC_DCU_properties(mmc)

if __name__ == "__main__":
    main() 