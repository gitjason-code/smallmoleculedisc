import os

path = input('File path: ')
path = path.strip('\"')

filepath = path.split('\\')
newpath = path.replace(filepath[len(filepath)-1], '')

with open(path) as f:
    content = f.readlines()

start = 0
startlist = []
filelist = []

for line in content:
    if 'MODEL' in line:
        startlist.append(start)
    elif 'Name' in line:
        name = line.split(' ')[4].replace('\n', '')
        if name in filelist:
            filelist.append(name + '_variant')
        else:
            filelist.append(name)
    start += 1

for i in range(len(startlist)):
    with open(os.path.join(newpath, filelist[i] + '.pdbqt'), 'w') as pdbqtFile:
        pass
        if i < len(startlist) - 1:
            for j in range(startlist[i] + 1, startlist[i+1] - 1):
                pdbqtFile.write(content[j])
        else:
            for j in range(startlist[i] + 1, len(content)):
                pdbqtFile.write(content[j])















