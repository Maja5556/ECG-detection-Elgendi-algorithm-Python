import wfdb as wf
import glob
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat

data = {}
signal_element = {
    'signal_name': None,
    'signal_samples': [],
    'annotation_beat_samples': [],
    'fs': None,
    'extension': None,
    'beat_samples': []
}


def load_annotation(path):
    beat_annotations = ('N', 'L', 'R', 'B', 'A', 'a', 'J', 'S', 'V', 'r', 'F', 'e', 'j', 'n', 'E', 'f', 'Q', '?', '/')
    annotation = wf.rdann(path, 'atr')
    signal_element['fs'] = annotation.fs

    annotation_beat_samples = []
    for i in range(len(annotation.sample)):
        if annotation.symbol[i] in beat_annotations:
            annotation_beat_samples.append((annotation.sample[i]))

    signal_element['annotation_beat_samples'] = annotation_beat_samples


def load_signals_dat(path, make_plot, samples_num, all_signals):
    if all_signals:
        # List of path name for all .dat files
        dat_path = glob.glob(path + '*.dat')
    else:
        dat_path = [path + '.dat']

    for file in dat_path:
        if file[-7:-4] == '114':
            record = wf.rdrecord(file[:-4], channels=[1])
        else:
            record = wf.rdrecord(file[:-4], channels=[0])
        signal_element['signal_name'] = file[-7:-4]
        if signal_element['signal_name']=='200'or signal_element['signal_name']=='108':
            signal_element['signal_samples'] = ((np.array(record.p_signal))*(-1)).flatten()
        #elif signal_element['signal_name']=='207':
            #signal_element['signal_samples'] = (abs(np.array(record.p_signal))).flatten()
        else:
            signal_element['signal_samples'] = (np.array(record.p_signal)).flatten()
        if signal_element['fs'] is None:
            signal_element['fs'] = 360
        load_annotation(file[:-4])
        data[file[-7:-4]] = signal_element.copy()

        if make_plot:
            plot_graph(data[file[-7:-4]], samples_num)


def load_signals_csv(path, make_plot, samples_num, all_signals):
    if all_signals:
        csv_path = glob.glob(path + '*.csv')
    else:
        csv_path = [path + '.csv']

    for file in csv_path:
        with open(file) as csv_file:
            # next(csv_file)  # skip first line
            # next(csv_file)  # skip second line
            lines = csv_file.readlines()
            sample = []
            if file[-7:-4] == '114':
                for line in lines:
                    row = line.split(',')
                    row[1].rstrip('\n')
                    sample.append(float(row[1]))
            elif file[-7:-4] == '200'or file[-7:-4] == '108':
                for line in lines:
                    row = line.split(',')
                    sample.append(float(row[0])*(-1))
            #elif file[-7:-4] == '207':
               # for line in lines:
                 #   row = line.split(',')
                  #  sample.append(abs(float(row[0])))
            else:
                for line in lines:
                    row = line.split(',')
                    sample.append(float(row[0]))

        signal_element['signal_name'] = file[-7:-4]
        signal_element['signal_samples'] = sample
        if signal_element['fs'] is None:
            signal_element['fs'] = 360
        load_annotation(file[:-4])
        data[file[-7:-4]] = signal_element.copy()

        if make_plot:
            plot_graph(data[file[-7:-4]], samples_num)


def load_signals_mat(path, make_plot, samples_num, all_signals):
    if all_signals:
        mat_path = glob.glob(path + '*.mat')
    else:
        mat_path = [path + '.mat']

    for file in mat_path:
        signal_element['signal_name'] = file[-7:-4]
        if signal_element['signal_name'] == '200' or signal_element['signal_name'] == '108':
            signal_element['signal_samples'] = loadmat(file, mat_dtype=True)['val'][0] * (-1)
        elif signal_element['signal_name'] == '114':
            signal_element['signal_samples'] = loadmat(file, mat_dtype=True)['val'][1]
        #elif signal_element['signal_name'] == '207':
           # signal_element['signal_samples'] = abs(loadmat(file, mat_dtype=True)['val'][0])
        else:
            signal_element['signal_samples'] = loadmat(file, mat_dtype=True)['val'][0]
        if signal_element['fs'] is None:
            signal_element['fs'] = 360
        load_annotation(file[:-4])
        data[file[-7:-4]] = signal_element.copy()

        if make_plot:
            plot_graph(data[file[-7:-4]], samples_num)


def plot_graph(signal_data, samples_num):
    n = len(signal_data['signal_samples'][0:samples_num])
    t = np.arange(0, n / signal_data['fs'], 1 / signal_data['fs'])
    plt.plot(t, signal_data['signal_samples'][0:samples_num], color='royalblue')
    plt.xlabel('time[s]', loc='center')
    plt.ylabel('voltage[mV]', loc='center')
    plt.title('Record ' + signal_data['signal_name'] + ' from MIT-BIH Arrhythmia Database')
    plt.show()
