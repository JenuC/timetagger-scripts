"""Core functionality for PMT Profiler analysis."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

console = Console()

class MicroManagerInterface(ABC):
    """Abstract base class for Micro-Manager interface."""
    
    @abstractmethod
    def getLoadedDevices(self) -> List[str]:
        """Get list of loaded devices."""
        pass
    
    @abstractmethod
    def getDevicePropertyNames(self, device: str) -> List[str]:
        """Get property names for a device."""
        pass
    
    @abstractmethod
    def getDeviceObject(self, device: str) -> Any:
        """Get device object."""
        pass
    
    @abstractmethod
    def getAvailableConfigGroups(self) -> List[str]:
        """Get available configuration groups."""
        pass
    
    @abstractmethod
    def getDeviceAdapterNames(self) -> List[str]:
        """Get device adapter names."""
        pass
    
    @abstractmethod
    def setProperty(self, device: str, prop: str, value: Any) -> None:
        """Set device property."""
        pass
    
    @abstractmethod
    def waitForDevice(self, device: str) -> None:
        """Wait for device operation to complete."""
        pass
        
    @abstractmethod
    def getProperty(self, device: str, prop: str) -> str:
        """Get device property value."""
        pass

class MockMicroManager(MicroManagerInterface):
    """Mock implementation of Micro-Manager interface for testing."""
    
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
            },
            'DCCModule1': {
                'EnableOutputs': 'Off',
                'C3_GainHV': '0',
                'C3_Plus12V': 'Off',
                'C4_GainHV': '0',
                'C4_Plus12V': 'Off'
            }
        }
        self.config_groups = ['ENABLE', 'GAIN CONTROL PERCENT', 'Supply']
        self.device_adapters = ['BH_DCC', 'BH_DCC_DCU', 'Core', 'DemoCamera', 'DemoXYStage']

    def getLoadedDevices(self) -> List[str]:
        return list(self.devices.keys())

    def getDevicePropertyNames(self, device: str) -> List[str]:
        return self.devices.get(device, [])

    def getDeviceObject(self, device: str) -> Any:
        class MockDevice:
            def __init__(self, properties):
                self.properties = [
                    type('Property', (), {'name': k, 'value': v})
                    for k, v in properties.items()
                ]
        return MockDevice(self.device_properties.get(device, {}))

    def getAvailableConfigGroups(self) -> List[str]:
        return self.config_groups

    def getDeviceAdapterNames(self) -> List[str]:
        return self.device_adapters

    def setProperty(self, device: str, prop: str, value: Any) -> None:
        print(f"Setting {device}.{prop} = {value}")

    def waitForDevice(self, device: str) -> None:
        pass
        
    def getProperty(self, device: str, prop: str) -> str:
        return str(self.device_properties.get(device, {}).get(prop, 'Unknown'))

class MicroManager(MicroManagerInterface):
    """Real implementation of Micro-Manager interface."""
    
    def __init__(self):
        from pymmcore_plus import CMMCorePlus
        self.mmc = CMMCorePlus()
        mm_path = r'C:/Program Files/Micro-Manager-nightly-markt'
        self.mmc.loadSystemConfiguration(f'{mm_path}/DCC_alone.cfg')
    
    def getLoadedDevices(self) -> List[str]:
        return self.mmc.getLoadedDevices()
    
    def getDevicePropertyNames(self, device: str) -> List[str]:
        return self.mmc.getDevicePropertyNames(device)
    
    def getDeviceObject(self, device: str) -> Any:
        return self.mmc.getDeviceObject(device)
    
    def getAvailableConfigGroups(self) -> List[str]:
        return self.mmc.getAvailableConfigGroups()
    
    def getDeviceAdapterNames(self) -> List[str]:
        return self.mmc.getDeviceAdapterNames()
    
    def setProperty(self, device: str, prop: str, value: Any) -> None:
        self.mmc.setProperty(device, prop, value)
    
    def waitForDevice(self, device: str) -> None:
        self.mmc.waitForDevice(device)
        
    def getProperty(self, device: str, prop: str) -> str:
        return self.mmc.getProperty(device, prop) 