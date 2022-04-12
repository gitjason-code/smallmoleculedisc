import os
import argparse


def path_validation(pdbqt_path):  # validates multi-model .pdbqt file path
    pdbqt_path = pdbqt_path.strip('\"')
    f_ext = os.path.splitext(pdbqt_path)[1]

    if os.path.isfile(pdbqt_path) and f_ext == '.pdbqt':
        return pdbqt_path, os.path.dirname(pdbqt_path)
    else:
        print('Please input the path of a multi-model pqbqt file.')
        pdbqt_path = input()
        path_validation(pdbqt_path)


def find_files(pdbqt_path):  # Finds compound name and start index of each .pdbqt file in batch
    with open(pdbqt_path) as f:
        lines = f.readlines()

    line_name_array = []
    for index, line in enumerate(lines):
        if 'Name' in line:
            mol_name = line.split(' ')[4].replace('\n', '')
            line_name_array.append([index-1, mol_name])

    return line_name_array, lines


def file_write(file_info, out_dir, multi_pdbqt):  # writes individual .pdbqt files from batch
    for i in range(len(file_info)):
        with open(os.path.join(out_dir, file_info[i][1] + '.pdbqt'), 'w') as parsed_file:
            if i < len(file_info) - 1:
                for j in range(file_info[i][0] + 1, file_info[i+1][0] - 1):
                    parsed_file.write(multi_pdbqt[j])
            else:
                for j in range(file_info[i][0] + 1, len(multi_pdbqt)):
                    parsed_file.write(multi_pdbqt[j])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help="Multi-model .pdbqt file")
    args = parser.parse_args()

    pdbqt_path, pdbqt_dir = path_validation(args.path)
    file_start, content = find_files(pdbqt_path)
    file_write(file_start, pdbqt_dir, content)











