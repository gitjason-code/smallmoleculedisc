import os
import pandas as pd


def path_input():  # user input of csv file path
    global csv_file
    global f_name
    global f_ext
    global smiles_path

    while True:
        csv_file = input('CSV file path: ')
        csv_file = csv_file.strip('\"')
        f_name, f_ext = os.path.splitext(csv_file)

        if f_ext == '.csv':
            smiles_path = os.path.dirname(csv_file)
            break
        else:
            print('Please input the path of a CSV file.')
            continue


def csv_converter():  # reads csv file and extracts SMILES strings and molecule IDs
    global id_list
    global smiles_list
    global moles
    global smiles_id_list

    data = pd.read_csv(csv_file)  # reads .csv file

    i = 0
    smiles_id_list = []

    for smiles in data.loc[:, 'SMILES']:
        try:
            if len(str(smiles)) > 1:
                smiles_id_list.append([smiles.split(' ')[0], data.loc[:, 'MolPort Id'][i]])  # links smiles string and molecule ID in array
            else:
                print(data.loc[:, 'MolPort Id'][i] + ' does not meet requirements for SMILES string.')  # excludes smiles strings that are too short
        except AttributeError:
            print(data.loc[:, 'MolPort Id'][i] + ' does not meet requirements for SMILES string.')  # excludes non-SMILES strings

        i += 1

    smiles_writer()


def smiles_writer():  # creates .smi file
    with open(os.path.join(smiles_path, f_name + '.smi'), 'w') as smiles_file:
        pass
        for i in range(len(smiles_id_list)):
            smiles_file.write(smiles_id_list[i][0] + ' ' + smiles_id_list[i][1] + '\n')

    print('SMILES file successfully created.')


path_input()
csv_converter()

