import os
from os import listdir

def libraryconfiggenerator():
    global fileList
    global filesource

    filesource = input('Path of .pdbqt files: ')
    filesource = filesource.translate({ord('"'): None})

    from os.path import isfile, join
    onlyfiles = [f for f in listdir(filesource) if isfile(join(filesource, f))]

    fileList = []
    for filename in onlyfiles:
        if filename.endswith('.pdbqt'):
            fileList.append(filename)

def batchFilegenerator():
    batchFileinput = input('Batch file name: ')
    batchFile = batchFileinput + '.bat'

    for file in fileList:
        with open(os.path.join(filesource, batchFile), 'a') as batch:
            pass
            batch.write(r'"C:\Program Files (x86)\The Scripps Research Institute\Vina\vina.exe" --config ' + file.split('.pdbqt')[0] + '_config' + '.txt' + '\n')

def configfileassembler():
    global fileInput
    global path
    global receptor
    global fileList

    receptor = input('Receptor file name: ')

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

    # exhaustiveness = input('exhaustiveness = ')
    exhaustiveness = '8'

    for file in fileList:
        with open(os.path.join(filesource, file.split('.pdbqt')[0]) + '_config' + '.txt', 'w') as configFile:
            pass
            configFile.write('receptor = ' + receptor + '.pdbqt' + '\n')
            configFile.write('ligand = ' + file + '\n')
            configFile.write('\n')
            configFile.write('center_x = ' + centerX + '\n')
            configFile.write('center_y = ' + centerY + '\n')
            configFile.write('center_z = ' + centerZ + '\n')
            configFile.write('\n')
            configFile.write('size_x = ' + sizeX + '\n')
            configFile.write('size_z = ' + sizeZ + '\n')
            configFile.write('size_y = ' + sizeY + '\n')
            configFile.write('\n')
            configFile.write('exhaustiveness = ' + exhaustiveness + '\n')
            configFile.write('\n')
            configFile.write('log = ' + file.split('.pdbqt')[0] + '_log' + '.txt')

    proceed = input('Would you like to create a batch file as well? (y or n): ')
    if proceed == 'y':
        batchFilegenerator()
    else:
        return


libraryconfiggenerator()

configfileassembler()

