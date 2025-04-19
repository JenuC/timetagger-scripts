#!/usr/bin/env python3

import pathlib
from datetime import datetime
from rich.console import Console
from rich.table import Table

# Initialize rich console
console = Console()

class MockCMMCorePlus:
    def __init__(self):
        self.devices = {
            'DCCHub': ['SimulateDevice', 'Simulated', 'UseModule1', 'UseModule2', 'UseModule3'],
            'DCCModule1': ['EnableOutputs', 'C3_GainHV', 'C3_Plus12V', 'C4_GainHV', 'C4_Plus12V'],
            'Core': ['AutoFocus', 'AutoShutter', 'Camera', 'ChannelGroup', 'Focus', 'Galvo', 'ImageProcessor']
        }
        self.device_properties = {
            'DCCHub': {
                'SimulateDevice': 'No',
                'Simulated': 'No',
                'UseModule1': 'Yes',
                'UseModule2': 'No',
                'UseModule3': 'No'
            }
        }
        self.config_groups = ['ENABLE', 'GAIN CONTROL PERCENT', 'Supply']
        self.device_adapters = ['BH_DCC', 'BH_DCC_DCU', 'Core', 'DemoCamera', 'DemoXYStage']

    def getLoadedDevices(self):
        return list(self.devices.keys())

    def getDevicePropertyNames(self, device):
        return self.devices.get(device, [])

    def getDeviceObject(self, device):
        class MockDevice:
            def __init__(self, properties):
                self.properties = [
                    type('Property', (), {'name': k, 'value': v})
                    for k, v in properties.items()
                ]
        return MockDevice(self.device_properties.get(device, {}))

    def getAvailableConfigGroups(self):
        return self.config_groups

    def getDeviceAdapterNames(self):
        return self.device_adapters

    def setProperty(self, device, prop, value):
        print(f"Setting {device}.{prop} = {value}")

    def waitForDevice(self, device):
        pass

def setup_micro_manager():
    """Initialize and configure Micro-Manager."""
    return MockCMMCorePlus()

def get_device_info(mmc):
    """Print information about loaded devices and their properties"""
    print("Loaded devices:", mmc.getLoadedDevices())
    for dev in mmc.getLoadedDevices():
        print(f"{dev}: {mmc.getDevicePropertyNames(dev)}")

def get_DCC_DCU_properties(mmc):
    """Get properties of DCC_DCU module"""
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

def start_PMT(mmc, gain=65, ch='C3'):
    """Start PMT with specified gain and channel"""
    mmc.setProperty('DCCModule1', ch+'_GainHV', gain)
    mmc.setProperty('DCCModule1', 'EnableOutputs', 'On')
    mmc.setProperty('DCCModule1', ch+'_Plus12V', 'On')
    mmc.waitForDevice('DCCModule1')
    print(f"PMT started on channel {ch}")

def stop_PMT(mmc, gain=0, ch='C3'):
    """Stop PMT on specified channel"""
    mmc.setProperty('DCCModule1', ch+'_GainHV', gain)
    mmc.setProperty('DCCModule1', 'EnableOutputs', 'Off')
    mmc.setProperty('DCCModule1', ch+'_Plus12V', 'Off')
    mmc.waitForDevice('DCCModule1')
    print(f"PMT stopped on channel {ch}")

def main():
    # Initialize Micro-Manager
    mmc = setup_micro_manager()
    
    # Print device information
    get_device_info(mmc)
    
    # Get available configurations
    config_groups = mmc.getAvailableConfigGroups()
    print("\nAvailable config groups:", config_groups)
    
    # Get DCC DCU properties
    get_DCC_DCU_properties(mmc)
    
    # Test PMT functions
    print("\nTesting PMT functions:")
    start_PMT(mmc)
    stop_PMT(mmc)

if __name__ == "__main__":
    main() 