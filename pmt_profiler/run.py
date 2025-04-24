from pmt_profiler.tt import TimeTaggerManager
from pmt_profiler.pmt import start_PMT, stop_PMT
from pmt_profiler.core import MicroManager
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

# Create data directory if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created data directory: {data_dir}")

# Create a TimeTagger manager
tt = TimeTaggerManager()
mm2 = MicroManager()
# Set trigger levels
tt_channels=[-1, 1]
tt.set_trigger_level(tt_channels[0], -0.01)  # For start channel 10mV 
    # we can trigger PMT wihtout fast-preamp at 1mV
    # swabian spec say min detction is 100mV
collection_time_sec=60
timing_resolution_sec=1

pmt_channel = 'C1'

for cooling_time in [0,30]:
    start_PMT(mmc=mm2.mmc, gain=65,cooling_time=cooling_time,channel=pmt_channel)
    # Get dark counts with progress bar
    print(f"\nCollecting dark counts for {collection_time_sec} seconds...")
    data = tt.get_darkcounts(tt_channels,collection_time_sec,timing_resolution_sec)
    stop_PMT(mmc = mm2.mmc,channel=pmt_channel)

    time_points = np.arange(0, collection_time_sec, timing_resolution_sec)
    style.use('ggplot')        
    plt.figure(figsize=(10, 6))
    for i, tt_channel in enumerate(tt_channels):
        plt.plot(
            time_points,
            data[i],
            marker='o',
            linestyle='-',
            label=f'Channel {tt_channel}',
            alpha=0.7
        )
    plt.title('Dark Counts Over Time', pad=20)
    plt.xlabel('Time (s)')
    plt.ylabel('Count Rate (Hz)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    # Create timestamp for unique filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save the plot
    plot_filename = os.path.join('data', f'dark_counts_{timestamp}.png')
    plt.savefig(plot_filename)

    # Save the data as CSV
    df = pd.DataFrame({
        'Time (s)': time_points,
        **{f'Channel {ch} Count Rate (Hz)': data[i] for i, ch in enumerate(tt_channels)}
    })
    csv_filename = os.path.join('data', f'dark_counts_{timestamp}_ctime_{cooling_time}.csv')
    df.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")
    print(f"Plot saved to {plot_filename}")

plt.show()
tt.close()
