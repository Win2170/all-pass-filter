import sounddevice as sd
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


sampling_rate = 44100
duration_in_seconds = 5
highpass = False
amplitude = 0.3

duration_in_samples = int(duration_in_seconds * sampling_rate)

white_noise = np.random.default_rng().uniform(-1, 1, duration_in_samples)
input_signal = white_noise

cutoff_frequency = np.geomspace(20000, 20, input_signal.shape[0])

allpass_output = np.zeros_like(input_signal)

dn_1 = 0

for n in range(input_signal.shape[0]):
    break_frequency = cutoff_frequency[n]

    tan = np.tan(np.pi * break_frequency / sampling_rate)

    a1 = (tan-1)/(tan+1)

    allpass_output[n] = a1 * input_signal[n] + dn_1

    dn_1 = input_signal[n] - a1 * allpass_output[n]

if highpass:
    allpass_output *= -1

filter_output = input_signal + allpass_output

filter_output *= 0.5

filter_output *= amplitude

sd.play(filter_output, sampling_rate)
sd.wait()

time = np.linspace(0, duration_in_seconds, duration_in_samples)

plt.figure(figsize=(10, 4))
plt.plot(time, cutoff_frequency)
plt.title("Cutoff Frequency Sweep (20 kHz - 20Hz)")
plt.xlabel("Time (In seconds)")
plt.ylabel("Frequency (In Hz)")
plt.yscale("log")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 4))
plt.specgram(filter_output, Fs=sampling_rate, NFFT=1024, noverlap=512)
plt.title("Spectogram of White Noise (Time-Varying Lowpass)")
plt.xlabel("Time (seconds)")
plt.ylabel("Frequency (Hz)")
plt.colorbar(label="Intensity (dB)")
plt.tight_layout()
plt.show()
