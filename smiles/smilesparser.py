import os
import pandas as pd

csvFile = input('CSV file path: ')
csvFile = csvFile.strip('\"')

path = input('File destination: ')
path = path.strip('\"')

title = input('Output file title: ')

data = pd.read_csv(csvFile)

i = 0
idList = []
smilesList = []

for smiles in data.loc[:, 'SMILES']:
    try:
        if len(str(smiles)) > 1:
            smilesList.append(smiles.split(' ')[0])
            idList.append(data.loc[:, 'MolPort Id'][i])
        else:
            print(data.loc[:, 'MolPort Id'][i] + ' could not be added as SMILES string.')
    except AttributeError:
        print(data.loc[:, 'MolPort Id'][i] + ' could not be added as SMILES string.')

    i += 1

moles = dict(zip(idList, smilesList))

with open(os.path.join(path, title + '.smi'), 'w') as smilesFile:
    pass
    for molportId in moles:
        smilesFile.write(moles[molportId] + ' ' + molportId + '\n')



