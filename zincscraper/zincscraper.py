import os
import requests
import pandas as pd
import html5lib
import bs4
import datetime
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=jim-chem02\zinc;'
                      'Database=ZINCProd;'
                      'Trusted_Connection=yes;'
                      'username=jason;'
                      'password=Jason123!;')

cursor = conn.cursor()

while True:
    csv_file = input('CSV file path: ')
    csv_file = csv_file.strip('\"')
    f_name, f_ext = os.path.splitext(csv_file)

    if f_ext == '.csv':
        break
    else:
        print('Please input the path of a CSV file.')


time_start = datetime.datetime.now()

data = pd.read_csv(csv_file)

# testarray = []

for i in range(len(data)):
    zinc_id = data.loc[i][0].split('__')[0]
    binding_affinity = data.loc[i][1]

    url = 'http://zinc15.docking.org/substances/' + zinc_id
    r = requests.get(url)

    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    first_table = df_list[0]

    logp = first_table.loc[:, 'logP'][0]
    mwt = first_table.loc[:, 'Mwt'][0]

    if 'pH range' in str(df_list):
        third_table = df_list[2]
        tpsa = third_table.loc[:, 'tPSA Å²'][0]
        rotbonds = third_table.loc[:, 'Rotatablebonds'][0]
    else:
        tpsa = 'null'
        rotbonds = 'null'

    count = cursor.execute("""
    INSERT INTO ZINCProd.dbo.Prodmain (zincid, bindaff, logp, mwt, tpsa, rotbonds) 
    VALUES (?,?,?,?,?,?)""",
    str(zinc_id), str(binding_affinity), str(logp), str(mwt), str(tpsa), str(rotbonds)).rowcount
    conn.commit()

    delete_dup = cursor.execute("""
    WITH cte AS (
        SELECT
            zincid,
            ROW_NUMBER() OVER (
                PARTITION BY
                    zincid
                ORDER BY
                    zincid
            ) row_num
        FROM
            ZINCProd.dbo.Prodmain
    )
    DELETE FROM cte
    WHERE row_num > 1;
    """)
    delete_dup.commit()

    mol_num = i + 1
    print(str(mol_num) + '/' + str(len(data)) + ' molecules added to database.')

    # testarray.append([zinc_id, binding_affinity, first_table.loc[:, 'logP'][0],  first_table.loc[:, 'Mwt'][0], tpsa, rotbonds])

# final_df = pd.DataFrame(testarray, columns=['ZINC ID', 'Binding affinity (kcal/mol)', 'logP', 'MW', 'tPSA', 'Rotatable bonds'])
# print(final_df.to_string())

time_end = datetime.datetime.now()

print('Run time:', time_end - time_start)



