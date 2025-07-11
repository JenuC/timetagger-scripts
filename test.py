import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy import stats

files = glob.glob("PMT CSV Files/*.csv")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# Varying amplitude values
trigger_timing = []
peak_amplitudes = []

# Normalized values
norm_trigger_timing = []
norm_peak_amplitudes = []
fifty_percent_points = []


for file in files:
    df = pd.read_csv(file, header=21)
    time = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    amplitude = pd.to_numeric(df.iloc[:, 1], errors='coerce') * 1000  # Convert V to mV
    norm_amplitude=-amplitude/amplitude.min()    #normalization
    ax2.plot(time, norm_amplitude, alpha=0.7, linewidth=0.5)
    norm_peak_amplitudes.append(norm_amplitude.min())  # Most negative peak

    ax1.plot(time, amplitude, alpha=0.7, linewidth=0.5)

    # Find trigger crossing 
    trigger_value = -30.0  # mV
    trigger_time_index = np.where(np.diff(np.sign(amplitude - trigger_value)))[0]
    if len(trigger_time_index) > 0:
            crossing_idx = trigger_time_index[0]
            trigger_time = time.iloc[crossing_idx]
            trigger_timing.append(trigger_time)

    # Find 50% point for jitter analysis
    fifty_percent = (norm_amplitude.min())/2
    print(fifty_percent)
    fifty_percent_index = np.where(np.diff(np.sign(norm_amplitude - fifty_percent)))[0]
    if len(fifty_percent_index) > 0:
            crossing_idx = fifty_percent_index[0]
            fifty_percent_time = time.iloc[crossing_idx]
            fifty_percent_points.append(fifty_percent_time)
           
# Convert to arrays
trigger_timing = np.array(trigger_timing)
peak_amplitudes = np.array(peak_amplitudes)
fifty_percent_points = np.array(fifty_percent_points)



# How normalized 50 percent points deviate from mean timing 
mean_fifty_percent = np.mean(fifty_percent_points)
norm_time_deviation = fifty_percent_points - mean_fifty_percent

# Do same analysis but for non normalized amplitudes
mean_trigger_time = np.mean(trigger_timing) 
trigger_time_deviation = trigger_timing - mean_trigger_time

print(f"Mean normalized 50 percent time: {mean_fifty_percent*1e9:.3f} ns")
print(f"Normalized timing deviation with respect to mean (std): {np.std(norm_time_deviation)*1e9:.3f} ns")

print(f"Mean Trigger Time without normalization: {mean_fifty_percent*1e9:.3f} ns")
print(f"Trigger timing deviation with respect to mean (std): {np.std(trigger_time_deviation)*1e9:.3f} ns")


ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude (mV)')
ax1.set_title('Original PMT Pulses')
ax1.grid()

ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Normalized Amplitude')
ax2.set_title('Normalized PMT Pulses')
ax2.grid()

plt.tight_layout()
plt.show()





