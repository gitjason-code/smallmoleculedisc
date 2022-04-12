from os import listdir
import os
import pandas as pd
import argparse
import numpy as np
from os.path import isfile, join


def retrieve_logs(log_dir):  # retrieves .log files from directory
    log_dir = log_dir.strip('\"')
    if not os.path.isdir(log_dir):
        print('Please input a valid directory')
        retrieve_logs(log_dir)

    logs = [log for log in listdir(log_dir) if isfile(join(log_dir, log)) and '_log' in log]

    return logs, log_dir


def data_finder(logs, log_dir):  # retrieves data from each log file
    output_data = [['MolPort ID', 'Binding Affinity (kcal/mol)']]

    for file_name in logs:
        with open(join(log_dir, file_name), 'r') as log_file:
            contents = log_file.readlines()

        data = []
        line_num = 15  # starts file search at line 15

        try:
            while line_num >= 15:
                if '   1' in contents[line_num]:  # unique location of data
                    break
                else:
                    line_num += 1
        except IndexError:  # catches errors in log file
            print(file_name + ' contains an error and was not used in data collection.')
        else:
            data_loc = contents[line_num].split(' ')
            print(data_loc)
            for ele in data_loc:
                if ele.strip():  # removes empty items from data_loc
                    data.append(ele)

            # appends output data with molecule ID and binding affinity
            output_data.append([file_name.split('_log.txt')[0], data[1]])

    compiled_data = np.array(output_data)  # converts array to numpy array
    compiled_data = compiled_data[compiled_data[:, 1].argsort()[::-1][:len(compiled_data)]]  # sorts array from smallest to largest binding affinity

    csv_file_maker(compiled_data, log_dir)

    return compiled_data


def csv_file_maker(compiled_data, log_dir):  # creates .csv files from numpy array
    df = pd.DataFrame(compiled_data)
    df.to_csv(join(log_dir, 'docking_results.csv'), header=None, index=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        help="Directory of .log files")
    args = parser.parse_args()

    log_files, logs_dir = retrieve_logs(args.directory)
    results = data_finder(log_files, logs_dir)
    csv_file_maker(results, logs_dir)





