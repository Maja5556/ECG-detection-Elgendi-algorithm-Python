import loadECG
import QRSdetection_elgendi

path_to_data = 'mitdb/'
path_to_data1 = 'mitdb/forcsv/'
extension = input('What signal want to load (.dat, .csv or .mat):\n').lower()

all_signals = False
one_or_all = input('Do you want to load ONE or ALL signal?\n').lower()

if one_or_all == 'one':
    signal = input('Which? Need to give signal number!\n')
    path_to_data += signal
    path_to_data1 += signal
elif one_or_all == 'all':
    all_signals = True
else:
    print('You need to write \n ONE - if you want to load one signal or \n ALL - if you want to load or signals')
    exit()

bool_var = {'true': True, 'false': False}
# temp = input('Do you want to plot signal/s?\n If yes -> True\n If no -> False\n').lower()
temp = 'false'
draw_graph = bool_var[temp]

# num_of_samples = int(input('Enter number of samples:\n'))
num_of_samples = 1000

if extension == '.dat':
    loadECG.signal_element['extension'] = '.dat'
    loadECG.load_signals_dat(path_to_data, draw_graph, num_of_samples, all_signals)
elif extension == '.csv':
    loadECG.signal_element['extension'] = '.csv'
    loadECG.load_signals_csv(path_to_data1, draw_graph, num_of_samples, all_signals)
elif extension == '.mat':
    loadECG.signal_element['extension'] = '.mat'
    loadECG.load_signals_mat(path_to_data, draw_graph, num_of_samples, all_signals)
else:
    print('Wrong input!')

# Detect QRS
QRSdetection_elgendi.detect_qrs(loadECG.data, draw_graph)
