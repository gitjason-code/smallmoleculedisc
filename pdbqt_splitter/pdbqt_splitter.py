import os
import random

while True:
    pdbqt_file = input('PDBQT file path: ')
    pdbqt_file = pdbqt_file.strip('\"')
    f_name, f_ext = os.path.splitext(pdbqt_file)

    if f_ext == '.pdbqt':
        pdbqt_dir = os.path.dirname(pdbqt_file)
        break
    else:
        print('Please input the path of a multi-model pqbqt file.')

with open(pdbqt_file) as f:
    content = f.readlines()

start = 0
start_list = []
file_list = []

for line in content:
    if 'MODEL' in line:
        start_list.append(start)
    elif 'Name' in line:
        name = line.split(' ')[4].replace('\n', '')
        if name in file_list:
            file_list.append(name + '_variant' + str(random.randint(0, 100)))
        else:
            file_list.append(name)

    start += 1

file_count = 0

for i in range(len(start_list)):
    with open(os.path.join(pdbqt_dir, file_list[i] + '.pdbqt'), 'w') as pdbqtFile:
        pass
        if i < len(start_list) - 1:
            for j in range(start_list[i] + 1, start_list[i+1] - 1):
                pdbqtFile.write(content[j])
        else:
            for j in range(start_list[i] + 1, len(content)):
                pdbqtFile.write(content[j])

    file_count += 1

print(file_count, 'files were successfully created.')















