#!/usr/bin/env python3

import pathlib
from pymmcore_plus import CMMCorePlus, find_micromanager
from datetime import datetime

def setup_micro_manager():
    """Initialize and configure Micro-Manager."""
    mmc = CMMCorePlus()
    mm_path = r'C:/Program Files/Micro-Manager-nightly-markt'
    mmc.loadSystemConfiguration(f'{mm_path}/DCC_alone.cfg')
    return mmc

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
    #device.load('BH_DCC_DCU', 'DCCHub') 
    #device.initialize()
    for prop in device.properties:
        print(prop.name, prop.value) 
        
    # Get the property names of one of BH DCC_DCU module
    props = mmc.getDevicePropertyNames('DCCModule1')
    for prop in props:
        print(prop) 
    
def start_PMT(mmc,gain=65,ch='C3'):
    mmc.setProperty('DCCModule1',ch+'_GainHV',gain)
    mmc.setProperty('DCCModule1','EnableOutputs','On')
    mmc.setProperty('DCCModule1',ch+'_Plus12V','On')
    mmc.waitForDevice('DCCModule1')

def stop_PMT(mmc,gain=0,ch='C3'):
    mmc.setProperty('DCCModule1',ch+'_GainHV',gain)
    mmc.setProperty('DCCModule1','EnableOutputs','Off')
    mmc.setProperty('DCCModule1',ch+'_Plus12V','Off')
    mmc.waitForDevice('DCCModule1')


def main():
    # Initialize Micro-Manager
    mmc = setup_micro_manager()
    
    # Print device information
    get_device_info(mmc)
    
    # Get available configurations
    config_groups = mmc.getAvailableConfigGroups()
    print("\nAvailable config groups:", config_groups)
    
    
        

if __name__ == "__main__":
    main() 