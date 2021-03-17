import os

csvFile = input('CSV file path: ')
csvFile = csvFile.translate({ord('"'): None})

path = input('File destination: ')
path = path.strip('\"')

title = input('Output file title: ')

import pandas as pd
data = pd.read_csv(csvFile)

smilesList = []
for smiles in data.loc[:, 'SMILES']:
    splitSmiles = smiles.split(' ')
    smilesList.append(splitSmiles[0])

idList = []
for molportId in data.loc[:, 'MolPort Id']:
    idList.append(molportId)

moles = dict(zip(idList, smilesList))

with open(os.path.join(path, title + '.smi'), 'w') as smilesFile:
    pass
    for molportId in moles:
        smilesFile.write(moles.get(molportId) + ' ' + molportId + '\n')



