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
    smilesList.append(smiles.split(' ')[0])
    idList.append(data.loc[:, 'MolPort Id'][i])
    i += 1

moles = dict(zip(idList, smilesList))

with open(os.path.join(path, title + '.smi'), 'w') as smilesFile:
    pass
    for molportId in moles:
        smilesFile.write(moles.get(molportId) + ' ' + molportId + '\n')



