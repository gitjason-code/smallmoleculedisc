import os


def fileRangelist():
    global fileRange
    fileRange = []
    firstFile = int(input('Starting molview file number: '))
    lastFile = int(input('Last molview file number: '))

    while firstFile < lastFile+1:
        fileRange.append(str(firstFile))
        firstFile += 1


def fileAssembler():
    global fileList
    fileList = []
    for i in fileRange:
        configFile = fileInput + i + '.txt'
        fileList.append(configFile)


def receptorLigandassembler():
    global ligandList
    global receptor
    receptor = input('Receptor file name: ')
    ligand = input('General ligand file name: ')
    ligandList = []

    for number in fileRange:
        ligandFile = ligand + number
        ligandList.append(ligandFile)


def batchFilegenerator(fileType='.txt'):
    batchFileinput = input('Batch file name: ')
    batchFile = batchFileinput + fileType

    for file in fileList:
        with open(os.path.join(path, batchFile), 'a') as batch:
            pass
            batch.write(r'"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe" --config ' + file + '\n')


def configFileassembler():
    global fileInput
    global path

    path = input('File path: ')
    path = path.translate({ord('"'): None})

    fileInput = input('General config file name: ')

    fileRangelist()

    receptorLigandassembler()

    #centerX = input('center_x = ')
    #centerY = input('center_y = ')
    #centerZ = input('center_z = ')
    #sizeX = input('size_x = ')
    #sizeY = input('size_y = ')
    #sizeZ = input('size_z = ')

    centerX = '-35.362'
    centerY = '22.55'
    centerZ = '4.592'
    sizeX = '20'
    sizeY = '20'
    sizeZ = '20'

    exhaustiveness = input('exhaustiveness = ')

    outputNumber = input('Output file number e.g 1.0, 2.0...(1.0 usually for only 1 run): ')

    fileAssembler()

    for file, ligand in zip(fileList, ligandList):
        with open(os.path.join(path, file), 'w') as configFile:
            pass
            configFile.write('receptor = ' + receptor + '.pdbqt' + '\n')
            configFile.write('ligand = ' + ligand + '.pdbqt' + '\n')
            configFile.write('\n')
            configFile.write('center_x = ' + centerX + '\n')
            configFile.write('center_y = ' + centerY + '\n')
            configFile.write('center_z = ' + centerZ + '\n')
            configFile.write('\n')
            configFile.write('size_x = ' + sizeX + '\n')
            configFile.write('size_y = ' + sizeY + '\n')
            configFile.write('size_z = ' + sizeZ + '\n')
            configFile.write('\n')
            configFile.write('exhaustiveness = ' + exhaustiveness + '\n')
            configFile.write('\n')
            configFile.write('out = ' + ligand + '_' + outputNumber + '_out' + '.pdbqt' + '\n')

    proceed = input('Would you like to create a batch file as well? (yes or no): ')
    if proceed == 'yes':
        batchFilegenerator()
    else:
        return


configFileassembler()







