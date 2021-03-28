from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
import numpy as np
import calculateAlgorithmAccuracy as acc
import time


def statical_mean_of_signal(signal):
    signal_size = len(signal)
    signal_sum = 0
    for i in range(signal_size):
        signal_sum += signal[i]
    return signal_sum / signal_size


def plot_graph(data, fs, samples_num):
    n = len(data[0:samples_num])
    t = np.arange(0, n / fs, 1 / fs)
    plt.plot(t, data[0:samples_num], color='royalblue')
    plt.xlabel('time[s]', loc='center')
    plt.show()

def detect_qrs(ecg_signal, plotGraph):
    #sampl_num = 500
    duration = []
    for signal in ecg_signal:
        start = time.time()
        x_kon = []
        ecg = (ecg_signal[signal]['signal_samples'])
        fs = 360
        ecg_signal[signal]['fs'] = 360
        # Filtering
        low = 8.0 / (0.5 * fs)
        high = 20.0 / (0.5 * fs)
        bw, aw = butter(3, [low, high], btype='bandpass')
        ecg_filtered = filtfilt(bw, aw, ecg, padtype='odd', padlen=3 * (max(len(bw), len(aw)) - 1))
        # if plotGraph:
        # plot_graph(ecg_filtered, fs, sampl_num)
        # Squaring values
        ecg_sqr = np.power(ecg_filtered, 2)
        # if plotGraph:
        # plot_graph(ecg_sqr, fs, sampl_num)

        # Generates blocks of interest
        t_qrs = 0.097  # approximate duration of the QRS
        t_beat = 0.611  # approximate duration of a heartbeat
        matrix_i = np.ones(round(t_qrs * fs)) / round(t_qrs * fs)
        # ma_qrs = np.convolve(ecg_sqr, matrix_i, 'same')
        npad1 = len(matrix_i) - 1
        full = np.convolve(ecg_sqr, matrix_i, 'full')
        first = npad1 - (npad1 // 2)
        ma_qrs = full[first:first + len(ecg_sqr)]
        matrix_i = np.ones(round(t_beat * fs)) / round(t_beat * fs)
        # ma_beat = np.convolve(ecg_sqr, matrix_i, 'same')

        npad2 = len(matrix_i) - 1
        full = np.convolve(ecg_sqr, matrix_i, 'full')
        first = npad2 - (npad2 // 2)
        ma_beat = full[first:first + len(ecg_sqr)]

        # Thresholding
        beta = 0.08
        ecg_mean = statical_mean_of_signal(ecg_sqr)
        alpha = (beta * ecg_mean)
        threshold_2 = round(t_qrs * 360)
        threshold_1 = []
        for i in range(len(ma_beat)):
            threshold_1.append(ma_beat[i] + alpha)
        blocks_of_interest = np.zeros(len(ma_qrs))
        for n in range(len(ma_qrs)):
            if ma_qrs[n] > threshold_1[n]:
                blocks_of_interest[n] = 0.1
            else:
                blocks_of_interest[n] = 0
        a = []
        b = []
        x = []
        for i in range(len(blocks_of_interest)):
            if (i == 0) and (blocks_of_interest[0] == 0.1):
                a.append(0)
            if i == len(blocks_of_interest) - 1:
                if blocks_of_interest[i] == 0.1:
                    b.append(i)
            else:
                if (blocks_of_interest[i] == 0) and (blocks_of_interest[i + 1] == 0.1):
                    a.append(i + 1)
                if (blocks_of_interest[i] == 0.1) and (blocks_of_interest[i + 1] == 0):
                    b.append(i)
        blocks = []
        for i in range(len(a)):
            blocks.append((b[i] + 1) - a[i])
        for i in range(len(a)):
            if blocks[i] >= threshold_2:
                x_r_peak_location = np.argmax(ecg_filtered[a[i]:b[i]]) + a[i]
                if not x:
                    x.append(x_r_peak_location)
                elif (abs(x_r_peak_location - x[-1])) > round(0.3 * fs):
                    x.append(x_r_peak_location)
        for i in range(len(x)):
            if (x[i] - round(0.03 * 360)) < 0:
                begin = 0
            else:
                begin = (x[i] - round(0.03 * 360))
            if (x[i] + round(0.03 * 360)) > (len(ecg_signal[signal]['signal_samples']) - 1):
                #end = len(ecg_signal[signal]['signal_samples']) - 1
                end = len(ecg_signal[signal]['signal_samples'])
            else:
                end = x[i] + round(0.03 * 360)+1
            x_kon.append(np.argmax(ecg_signal[signal]['signal_samples'][begin:end]) + begin)
        end = time.time()
        duration.append(end - start)
        ecg_signal[signal]['beat_samples'] = x_kon.copy()
        # print(ecg_signal[signal]['beat_samples'])
        # print(ecg_signal[signal]['annotation_beat_samples'])
    acc.calculate_accuracy(ecg_signal, duration)
