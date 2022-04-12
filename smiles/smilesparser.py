import os
import pandas as pd
import argparse


def smiles_filter(smiles):
    smiles = smiles.split(' ')[0].strip()
    if len(smiles) > 1 and smiles != 'nan':
        return smiles


def path_input(smi_path):  # user input of csv file path
    smi_path = smi_path.strip('\"')
    f_ext = os.path.splitext(smi_path)[1]

    if os.path.isfile(smi_path) and f_ext == '.csv':
        smi_dir = os.path.dirname(smi_path)
    else:
        print('Please input a valid path to .csv file')
        smi_path = input()
        path_input(smi_path)

    return smi_path, smi_dir


def find_smiles(smi_path):  # reads csv file and extracts SMILES strings and molecule IDs
    smiles_df = pd.read_csv(smi_path)  # reads .csv file
    smiles_df['SMILES'] = smiles_df['SMILES'].astype(str)
    smiles_df['SMILES'] = smiles_df['SMILES'].map(smiles_filter)
    smiles_df.dropna(subset=['SMILES'], inplace=True)
    smiles_dict = dict(zip(smiles_df['MolPort Id'], smiles_df['SMILES']))

    return smiles_dict


def smiles_writer(smi_dir, smiles_dict):  # creates .smi file
    with open(os.path.join(smi_dir, 'smiles_out.smi'), 'w') as smiles_file:
        for molport_id in smiles_dict:
            smiles_file.write(smiles_dict[molport_id] + ' ' + molport_id + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        '--path',
                        help="Path of Molport library .csv export")
    args = parser.parse_args()

    smi_path, smi_dir = path_input(args.path)
    smiles_dict = find_smiles(smi_path)
    smiles_writer(smi_dir, smiles_dict)

