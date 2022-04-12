import os
from os import listdir
import argparse
from os.path import isfile, join


def pdbqt_retrieve(dir_path):  # validates directory of .pdbqt files and extracts .pdbqt file names
    if not os.path.isdir(dir_path):
        print('Directory does not exist! Re-enter a valid file path.\n')
        dir_path = input()
        return pdbqt_retrieve(dir_path)

    dir_path = dir_path.strip("\"")
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    file_list = [file_name for file_name in files if file_name.endswith('.pdbqt')]

    return file_list, dir_path


def batch_file_generator(file_list, dir_path):
    for file in file_list:
        with open(os.path.join(dir_path, 'start.bat'), 'a') as batch:
            batch.write(r'"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe" ' 
                        r'--config ' + file.split('.pdbqt')[0] + '_config' + '.txt' + '\n')


def config_file_assembler(coordinates, dimensions, exhaust, input_path, receptor, file_list):
    # creates config file for each .pdbqt file to be AutoDock Vina
    coords = [coord.strip() for coord in coordinates.split(',')]
    try:  # validates x, y, and z coords present and in correct format
        center_x, center_y, center_z = coords
    except ValueError:
        print('x, y, and z coordinates required. Example: "1.8,22.0,44,3"')
        exit()

    dimensions = [dimension.strip() for dimension in dimensions.split(',')]
    try:  # validates x, y, and, z dimensions present and in correct format
        size_x, size_y, size_z = dimensions
    except ValueError:
        print('x, y, and z dimensions of docking region required. Example: "20,30,35"')
        exit()

    for file in file_list:
        with open(os.path.join(input_path, file.split('.pdbqt')[0]) + '_config' + '.txt', 'w') \
                as config_file:
            config_file.write('receptor = ' + receptor + '.pdbqt' + '\n')
            config_file.write('ligand = ' + file + '\n')
            config_file.write('\n')
            config_file.write('center_x = ' + center_x + '\n')
            config_file.write('center_y = ' + center_y + '\n')
            config_file.write('center_z = ' + center_z + '\n')
            config_file.write('\n')
            config_file.write('size_x = ' + size_x + '\n')
            config_file.write('size_z = ' + size_y + '\n')
            config_file.write('size_y = ' + size_z + '\n')
            config_file.write('\n')
            config_file.write('exhaustiveness = ' + exhaust + '\n')
            config_file.write('\n')
            config_file.write('log = ' + file.split('.pdbqt')[0] + '_log' + '.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        help="Directory of .pdbqt files")
    parser.add_argument('-c',
                        '--coordinates',
                        help="x,y,z coordinates for docking separated by comma",
                        default='-35.362,22.55,4.592',
                        nargs='?')
    parser.add_argument('-s',
                        '--dimensions',
                        help="x,y,z docking dimensions separated by a comma",
                        default='20,20,20',
                        nargs='?')
    parser.add_argument('-e',
                        '--exhaust',
                        help="Docking exhaustiveness",
                        default='8',
                        type=str,
                        nargs='?')
    parser.add_argument('-r',
                        '--receptor',
                        help="Name of receptor .pdbqt file (must be in same dir as .pdbqt ligand "
                             "files)",
                        type=str)
    args = parser.parse_args()

    file_names, pdbqt_dir = pdbqt_retrieve(args.directory)
    batch_file_generator(file_names, pdbqt_dir)
    config_file_assembler(args.coordinates, args.dimensions, args.exhaust, pdbqt_dir,
                          args.receptor, file_names)
