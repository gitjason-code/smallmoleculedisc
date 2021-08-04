import os

while True:  # user input of multi-model pdbqt file
    pdbqt_file = input('PDBQT file path: ')
    pdbqt_file = pdbqt_file.strip('\"')
    f_name, f_ext = os.path.splitext(pdbqt_file)

    if f_ext == '.pdbqt':
        pdbqt_dir = os.path.dirname(pdbqt_file)
        break
    else:
        print('Please input the path of a multi-model pqbqt file.')

with open(pdbqt_file) as f:  # reads pdbqt file
    content = f.readlines()

start = 0  # line number of start of each pdbqt model
line_name_array = []

for line in content:
    if 'MODEL' in line:
        start_num = start
    elif 'Name' in line:
        mol_name = line.split(' ')[4].replace('\n', '')  # defines model name and removes \n from string
        line_name_array.append([start_num, mol_name])  # links starting line number and model name in array
    start += 1

j = 0
for i in range(len(line_name_array)):
    with open(os.path.join(pdbqt_dir, line_name_array[i][1] + '.pdbqt'), 'w') as pdbqtFile:  # creates new pdbqt file for each item in line_num_array
        pass
        if i < len(line_name_array) - 1:
            for j in range(line_name_array[i][0] + 1, line_name_array[i+1][0] - 1):
                pdbqtFile.write(content[j])
        else:
            for j in range(line_name_array[i][0] + 1, len(content)):
                pdbqtFile.write(content[j])

    j += 1











