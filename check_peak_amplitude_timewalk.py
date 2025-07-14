import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

files = glob.glob("PMT CSV Files/*.csv")

# 1. Collect peak amplitudes and 50% crossing times for each pulse
peak_amplitudes = []
fifty_percent_times = []

for file in files:
    df = pd.read_csv(file, header=21)
    time = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    amplitude = pd.to_numeric(df.iloc[:, 1], errors='coerce') * 1000
    norm_amplitude = -amplitude / amplitude.min()
    # Peak amplitude (use min because pulses are negative)
    peak = amplitude.min()
    peak_amplitudes.append(peak)
    # 50% crossing
    fifty_percent = norm_amplitude.min() / 2
    idxs = np.where(np.diff(np.sign(norm_amplitude - fifty_percent)))[0]
    if len(idxs) > 0:
        crossing_time = time.iloc[idxs[0]]
        fifty_percent_times.append(crossing_time)
    else:
        fifty_percent_times.append(np.nan)

peak_amplitudes = np.array(peak_amplitudes)
fifty_percent_times = np.array(fifty_percent_times)

# 2. Bin by peak amplitude
n_bins = 10
valid = ~np.isnan(fifty_percent_times)
amps = peak_amplitudes[valid]
times = fifty_percent_times[valid]
mean_amp = np.mean(amps)

# Define amplitude bins (e.g., 0-50, 50-100, ..., up to max amplitude)
bin_width = 20  # mV
min_amp = np.floor(amps.min() / bin_width) * bin_width
max_amp = np.ceil(amps.max() / bin_width) * bin_width
bin_edges = np.arange(min_amp, max_amp + bin_width, bin_width)

# Bin the amplitudes
bin_indices = np.digitize(amps, bin_edges) - 1

bin_centers = []
jitter_rms = []

for i in range(len(bin_edges) - 1):
    in_bin = bin_indices == i
    if np.sum(in_bin) > 1:
        bin_time = times[in_bin]
        mean_time = np.mean(bin_time)
        rms = np.std(bin_time - mean_time) * 1e9  # ns
        # Center of the bin for plotting
        center = (bin_edges[i] + bin_edges[i+1]) / 2
        bin_centers.append(center)
        jitter_rms.append(rms)

# Plot as a bar plot (histogram)
plt.figure()
plt.bar(bin_centers, jitter_rms, width=bin_width*0.9, align='center', edgecolor='k')
plt.xlabel('Peak Amplitude (mV)')
plt.ylabel('RMS Jitter at 50% (ns)')
plt.title('Jitter vs. Peak Amplitude')
plt.yscale('log')
plt.grid(axis='y')
plt.show()