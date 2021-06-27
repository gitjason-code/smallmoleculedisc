from os import listdir
import numpy as np
import pandas as pd
import datetime


def user_inputs():
    global file_source
    global csv_file_name
    global time_start

    file_source = input('Path of output files: ')
    file_source = file_source.translate({ord('"'): None})

    csv_file_name = input('.csv file name: ')

    time_start = datetime.datetime.now()


def output_file_finder():
    global file_names

    from os.path import isfile, join
    files_in_folder = [f for f in listdir(file_source) if isfile(join(file_source, f))]

    file_names = []
    for file_name in files_in_folder:
        if '_log' in file_name:
            file_names.append(file_name)


def data_finder():
    global output_data

    output_data = [['MolPort ID', 'Binding Affinity (kcal/mol)']]

    for file in file_names:

        output_file = open(file_source + '\\' + file)
        data = output_file.readlines()
        isolated_data = []

        line_num = 15

        try:
            while line_num >= 15:
                if '   1' in data[line_num]:
                    break
                else:
                    line_num += 1
            data[line_num].split(' ')
        except IndexError:
            print(file + ' contains an error and was not used in data collection.')
        else:
            for ele in data[line_num].split(' '):
                if ele.strip():
                    isolated_data.append(ele)
            output_data.append([file.split('_log.txt')[0], isolated_data[1]])

    compiled_data = np.array(output_data)
    sorted_compiled_data = compiled_data[compiled_data[:, 1].argsort()[::-1][:len(compiled_data)]]

    csv_file_maker(sorted_compiled_data)


def csv_file_maker(sorted_compiled_data):
    df = pd.DataFrame(sorted_compiled_data)
    df.to_csv(file_source + '\\' + csv_file_name + '.csv', header=None, index=None)


user_inputs()
output_file_finder()
data_finder()

time_end = datetime.datetime.now()

print('Run time:', time_end - time_start)



