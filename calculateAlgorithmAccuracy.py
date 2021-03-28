def calculate_accuracy(ecg_signal, x):
    tp_sum = 0
    fp_sum = 0
    fn_sum = 0
    w = 0
    duration_sum = 0

    file_text = open("accuracy.txt", "w")
    file_text.write("Signal     TP      FP      FN      Se      +P      Execution_time\n")

    for signal in ecg_signal:
        tp = 0
        fn = 0
        fp = 0

        file_text.write(ecg_signal[signal]['signal_name'])
        file_text.write("        ")

        beat_annotation = ecg_signal[signal]['annotation_beat_samples']
        beat_samples = ecg_signal[signal]['beat_samples']

        size_beat = len(beat_samples)
        size_annotation = len(beat_annotation)

        max_samples_vary = round(0.078 * ecg_signal[signal]['fs'])

        for i in range(0, size_beat):
            beat_flag = 0
            for j in range(0, size_annotation):
                diff = abs(beat_samples[i] - beat_annotation[j])
                if diff <= max_samples_vary:
                    tp += 1
                    beat_flag = 1
                    break

            if beat_flag == 0:
                fp += 1

        for i in range(0, size_annotation):
            annotation_flag = 0
            for j in range(0, size_beat):
                diff = abs(beat_annotation[i] - beat_samples[j])
                if diff <= max_samples_vary:
                    annotation_flag = 1
                    break

            if annotation_flag == 0:
                fn += 1

        print('TP:' + str(tp) + '\nFN:' + str(fn) + '\nFP:' + str(fp))

        se = tp / (tp + fn)
        p = tp / (tp + fp)

        file_text.write('{0:4d}'.format(tp))
        file_text.write("  ")
        file_text.write('{0:4d}'.format(fp))
        file_text.write("    ")
        file_text.write('{0:4d}'.format(fn))
        file_text.write("    ")
        file_text.write('{0:.3f}'.format(se))
        file_text.write("    ")
        file_text.write('{0:.3f}'.format(p))
        file_text.write("    ")
        file_text.write('{0:.3f}'.format(x[w]))
        file_text.write('\n')

        tp_sum += tp
        fp_sum += fp
        fn_sum += fn
        duration_sum += x[w]
        w += 1

    se_sum = tp_sum / (tp_sum + fn_sum)
    p_sum = tp_sum / (tp_sum + fp_sum)
    execution_time = duration_sum / w

    file_text.write("Total:     ")
    file_text.write('{0:4d}'.format(tp_sum))
    file_text.write("  ")
    file_text.write('{0:4d}'.format(fp_sum))
    file_text.write("    ")
    file_text.write('{0:4d}'.format(fn_sum))
    file_text.write("    ")
    file_text.write('{0:.3f}'.format(se_sum))
    file_text.write("    ")
    file_text.write('{0:.3f}'.format(p_sum))
    file_text.write("    ")
    file_text.write('{0:.3f}'.format(execution_time))
    #file_text.write("      ")
