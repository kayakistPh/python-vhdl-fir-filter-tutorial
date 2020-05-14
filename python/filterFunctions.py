# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
import math


def PlotFilterFunction(b, fs):
    # Plot the perameters of the Filter
    w_filter, h_filter = signal.freqz(b)
    w_filterAsHz = w_filter * fs / (2 * np.pi)
    plt.semilogx(w_filterAsHz, 20 * np.log10(abs(h_filter)))
    plt.title("Filter frequency response")
    plt.xlabel("Frequency [Hz]")
    plt.ylabel("Amplitude [dB]")
    plt.margins(0, 0.1)
    plt.show()


def WhiteNoiseGen(fs, bits):
    low = (2 ** (bits - 1)) * -1
    high = 2 ** (bits - 1)
    noise = np.random.randint(int(low), int(high), size=int(fs / 10))
    return noise


def fft(x, fs, SegmentLength):
    # plot an FFT
    f, Pxx_spec = signal.welch(
        x, fs, "hanning", nperseg=SegmentLength, noverlap=None, scaling="spectrum"
    )
    plt.figure()
    plt.loglog(f, np.sqrt(Pxx_spec))
    plt.xlabel("frequency [Hz]")
    plt.ylabel("Spectrum [Bits RMS]")
    plt.show()


def MathsFilter(numtaps_fir, b, signal):
    # Begin by padding the front with 0's matching the number of filter taps.
    zeros = np.zeros(numtaps_fir)
    SignalToFilter = np.concatenate([zeros, signal])
    outputSignal = np.zeros(len(signal))
    # For loop to go through each of the elements
    for i in range((numtaps_fir + 1), len(signal)):
        FilterResult = np.multiply((SignalToFilter[x - numtaps_fir : i]), b)
        outputSignal[i - numtaps_fir] = np.sum(FilterResult)
    return outputSignal


def CalculateFIR(fs, stopband, fcutoff, pass_ripple, stop_supression):
    # Calculate the required taps localy if not using PyFDA
    n = (
        (2 / 3)
        * np.log10(1 / (10 * pass_ripple * stop_supression))
        * (fs / (stopband - fcutoff))
    )
    n = int(np.ceil(math.sqrt(n ** 2)))
    b = signal.firwin(n, cutoff=(fcutoff / (fs / 2)), window="hamming")
    return b


def dBtoReal(db):
    return 10 ** (db / 20)
