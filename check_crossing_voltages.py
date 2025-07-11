import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob


files = glob.glob("PMT CSV Files/*.csv")

# Define thresholds (10% to 100% in 10 or 20 steps)
n_points = 50
thresholds = np.linspace(0.1, 1.0, n_points)
jitter_rms_list = []

# For each threshold, collect crossing times for all pulses
all_crossing_times = {thr: [] for thr in thresholds}

for file in files:
    df = pd.read_csv(file, header=21)
    time = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    amplitude = pd.to_numeric(df.iloc[:, 1], errors='coerce') * 1000
    norm_amplitude = -amplitude / amplitude.min()
    for thr in thresholds:
        value = norm_amplitude.min() * thr  # since norm_amplitude.min() is negative
        idxs = np.where(np.diff(np.sign(norm_amplitude - value)))[0]
        if len(idxs) > 0:
            crossing_idx = idxs[0]
            crossing_time = time.iloc[crossing_idx]
            all_crossing_times[thr].append(crossing_time)

# Calculate RMS jitter for each threshold
for thr in thresholds:
    times = np.array(all_crossing_times[thr])
    if len(times) > 1:
        mean_time = np.mean(times)
        rms_jitter = np.std(times - mean_time) * 1e9  # ns
        jitter_rms_list.append(rms_jitter)
    else:
        jitter_rms_list.append(np.nan)

# Plot jitter curve
plt.figure()
plt.plot(thresholds * 100, jitter_rms_list, marker='o')
plt.xlabel('Threshold (% of peak)')
plt.ylabel('RMS Jitter (ns)')
plt.title('Jitter Curve vs. Amplitude Threshold')
plt.yscale('log')
plt.grid()
plt.show()