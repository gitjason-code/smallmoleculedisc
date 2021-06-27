import os
import pandas as pd


def path_input():
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


def csv_converter():
    global id_list
    global smiles_list
    global moles

    data = pd.read_csv(csv_file)

    i = 0
    id_list = []
    smiles_list = []

    for smiles in data.loc[:, 'SMILES']:
        try:
            if len(str(smiles)) > 1:
                smiles_list.append(smiles.split(' ')[0])
                id_list.append(data.loc[:, 'MolPort Id'][i])
            else:
                print(data.loc[:, 'MolPort Id'][i] + ' does not meet requirements for SMILES string.')
        except AttributeError:
            print(data.loc[:, 'MolPort Id'][i] + ' does not meet requirements for SMILES string.')

        i += 1

    moles = dict(zip(id_list, smiles_list))

    smiles_writer()


def smiles_writer():
    with open(os.path.join(smiles_path, f_name + '.smi'), 'w') as smiles_file:
        pass
        for molport_id in moles:
            smiles_file.write(moles[molport_id] + ' ' + molport_id + '\n')

    print('SMILES file successfully created.')


path_input()
csv_converter()

