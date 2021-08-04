from os import listdir
import numpy as np
import pandas as pd
import datetime


def user_inputs():  # prompts user for log files directory and .csv file name
    global file_source
    global csv_file_name
    global time_start

    file_source = input('Path of output files: ')  # defines location of log files
    file_source = file_source.strip('\"')  # removes quotes from file path

    csv_file_name = input('.csv file name: ')  # defines file name of .csv file

    time_start = datetime.datetime.now()


def output_file_finder():  # searches through directory for log files
    global file_names

    from os.path import isfile, join
    files_in_folder = [f for f in listdir(file_source) if isfile(join(file_source, f))]

    file_names = []
    for file_name in files_in_folder:
        if '_log' in file_name:
            file_names.append(file_name)


def data_finder():  # retrieves data from each log file
    global output_data

    output_data = [['MolPort ID', 'Binding Affinity (kcal/mol)']]

    for file in file_names:
        output_file = open(file_source + '\\' + file)
        data = output_file.readlines()  # returns list where each line in file is a list item
        isolated_data = []  # empty list that data will be added to

        line_num = 15  # starts file search at line 15

        try:
            while line_num >= 15:
                if '   1' in data[line_num]:  # unique location of data
                    break
                else:
                    line_num += 1
        except IndexError:  # catches errors in log file
            print(file + ' contains an error and was not used in data collection.')
        else:
            data_loc = data[line_num].split(' ')
            for ele in data_loc:
                if ele.strip():  # removes spaces from data_loc
                    isolated_data.append(ele)

            output_data.append([file.split('_log.txt')[0], isolated_data[1]])  # appends output data with molecule ID and binding affinity

        output_file.close()

    compiled_data = np.array(output_data)  # converts array to numpy array
    sorted_compiled_data = compiled_data[compiled_data[:, 1].argsort()[::-1][:len(compiled_data)]]  # sorts array from smallest to largest binding affinity

    csv_file_maker(sorted_compiled_data)


def csv_file_maker(sorted_compiled_data):  # creates .csv files from numpy array
    df = pd.DataFrame(sorted_compiled_data)
    df.to_csv(file_source + '\\' + csv_file_name + '.csv', header=None, index=None)


user_inputs()
output_file_finder()
data_finder()

time_end = datetime.datetime.now()

print('Run time:', time_end - time_start)  # prints run time of script



