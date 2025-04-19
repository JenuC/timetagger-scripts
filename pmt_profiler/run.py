from pmt_profiler.tt import TimeTaggerManager
from pmt_profiler.pmt import start_PMT, stop_PMT
from pmt_profiler.core import MicroManager
import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm
import time

# Create data directory if it doesn't exist
data_dir = 'data'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    print(f"Created data directory: {data_dir}")

# Create a TimeTagger manager
tt = TimeTaggerManager()
mm2 = MicroManager()
# Set trigger levels
tt.set_trigger_level(-1, -0.01)  # For start channel
tt.set_trigger_level(1, -0.01)   # For stop channel

channels=[-1, 1]
collection_time_sec=5
timing_resolution_sec=1

start_PMT(mmc=mm2.mmc, gain=65)
# Get dark counts with progress bar
print(f"\nCollecting dark counts for {collection_time_sec} seconds...")
data = tt.get_darkcounts(channels,collection_time_sec,timing_resolution_sec)

import numpy as np
import matplotlib.pyplot as plt

time_points = np.arange(0, collection_time_sec, timing_resolution_sec)

from matplotlib import style
style.use('ggplot')        
plt.figure(figsize=(10, 6))

# Plot each channel
for i, channel in enumerate(channels):
    plt.plot(
        time_points,
        data[i],
        marker='o',
        linestyle='-',
        label=f'Channel {channel}',
        alpha=0.7
    )

stop_PMT(mmc = mm2.mmc)
# Clean up when done
tt.close()

# Customize plot
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
plt.show()

# Save the data as CSV
# Create a DataFrame with time points and count data
df = pd.DataFrame({
    'Time (s)': time_points,
    **{f'Channel {ch} Count Rate (Hz)': data[i] for i, ch in enumerate(channels)}
})

# Save to CSV
csv_filename = os.path.join('data', f'dark_counts_{timestamp}.csv')
df.to_csv(csv_filename, index=False)
print(f"Data saved to {csv_filename}")
print(f"Plot saved to {plot_filename}")

