import marimo as mo
import pathlib
from pymmcore_plus import CMMCorePlus, find_micromanager
import numpy as np
import plotly.graph_objects as go
from typing import Optional

# Create the app
app = mo.App()

# Title cell
@app.cell
def title():
    mo.md("# Time Tagger Data Analysis")
    mo.md("Interactive interface for analyzing time-tagging data from Micro-Manager")
    return None

# Micro-Manager setup cell
@app.cell
def setup_micromanager():
    mo.md("## Micro-Manager Setup")
    
    # Find Micro-Manager installation
    mm_path = find_micromanager()
    mo.md(f"Found Micro-Manager at: {mm_path}")
    
    # Initialize CMMCorePlus
    mmc = CMMCorePlus()
    mmc.loadSystemConfiguration(str(pathlib.Path(mm_path) / "DCC_alone.cfg"))
    
    return mmc

# Device configuration cell
@app.cell
def device_config(mmc):
    mo.md("## Device Configuration")
    
    # Display loaded devices
    devices = mmc.getLoadedDevices()
    mo.md(f"Loaded devices: {devices}")
    
    # Display device properties
    for dev in devices:
        props = mmc.getDevicePropertyNames(dev)
        mo.md(f"### {dev} Properties")
        mo.md(f"```\n{props}\n```")
    
    return devices

# Data acquisition cell
@app.cell
def data_acquisition(mmc):
    mo.md("## Data Acquisition")
    
    # Create controls for acquisition parameters
    exposure_time = mo.slider("Exposure Time (ms)", min=1, max=1000, value=100)
    num_frames = mo.slider("Number of Frames", min=1, max=1000, value=10)
    
    # Acquisition button
    if mo.button("Start Acquisition"):
        # Set exposure time
        mmc.setExposure(exposure_time)
        
        # Initialize data storage
        frames = []
        
        # Acquire frames
        for _ in range(num_frames):
            mmc.snapImage()
            img = mmc.getImage()
            frames.append(img)
        
        return np.array(frames)
    
    return None

# Data visualization cell
@app.cell
def visualize_data(frames: Optional[np.ndarray]):
    if frames is not None:
        mo.md("## Data Visualization")
        
        # Create time trace plot
        fig = go.Figure()
        
        # Plot mean intensity over time
        mean_intensity = np.mean(frames, axis=(1, 2))
        fig.add_trace(go.Scatter(
            y=mean_intensity,
            mode='lines+markers',
            name='Mean Intensity'
        ))
        
        fig.update_layout(
            title='Time Trace',
            xaxis_title='Frame Number',
            yaxis_title='Mean Intensity',
            showlegend=True
        )
        
        mo.plot(fig)
        
        # Display statistics
        mo.md(f"""
        ### Statistics
        - Mean intensity: {np.mean(mean_intensity):.2f}
        - Std deviation: {np.std(mean_intensity):.2f}
        - Max intensity: {np.max(mean_intensity):.2f}
        - Min intensity: {np.min(mean_intensity):.2f}
        """)

if __name__ == "__main__":
    mo.run() 