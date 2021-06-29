import os
import requests
import pandas as pd
import datetime
import pyodbc

server = 'jim-chem02.rgarrison.net\ZINC'
database = 'ZINCProd'
username = 'jason'
password = 'Jason123!'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

while True:
    csv_file = input('CSV file path: ')
    csv_file = csv_file.strip('\"')
    f_name, f_ext = os.path.splitext(csv_file)

    if f_ext == '.csv':
        csv_path = os.path.dirname(csv_file)
        break
    else:
        print('Please input the path of a CSV file.')
        continue

time_start = datetime.datetime.now()

data = pd.read_csv(csv_file)

id_list = []
testarray = []

for i in range(len(data)):
    zinc_id = data.loc[i][0].split('__')[0]
    binding_affinity = data.loc[i][1]
    url = 'https://zinc15.docking.org/substances/' + zinc_id

    r = requests.get(url)
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    first_table = df_list[0]
    logp = first_table.loc[:, 'logP'][0]
    mwt = first_table.loc[:, 'Mwt'][0]

    if 'pH range' in str(df_list):
        print('3D')
        third_table = df_list[2]
        tpsa = third_table.loc[:, 'tPSA Å²'][0]
        rotbonds = third_table.loc[:, 'Rotatablebonds'][0]
    else:
        print('2D')
        tpsa = 'null'
        rotbonds = 'null'

    count = cursor.execute("""
    INSERT INTO ZINCProd (zinc_id, binding_affinity, logp, mwt, tpsa, rotbonds) 
    VALUES (?,?,?,?,?,?)""",
    zinc_id, binding_affinity, logp, mwt, tpsa, rotbonds).rowcount
    cnxn.commit()
    print('Rows inserted: ' + str(count))

    # testarray.append([zinc_id, binding_affinity, first_table.loc[:, 'logP'][0],  first_table.loc[:, 'Mwt'][0], tpsa, rotbonds])

# final_df = pd.DataFrame(testarray, columns=['ZINC ID', 'Binding affinity (kcal/mol)', 'logP', 'MW', 'tPSA', 'Rotatable bonds'])
# print(final_df.to_string())

time_end = datetime.datetime.now()

print('Run time:', time_end - time_start)



