import pandas as pd

tables0 = pd.read_html('https://www.x-rates.com/table/?from=USD&amount=1')
tables = pd.DataFrame(tables0)

tables_gryvna0 = pd.read_html('https://finance.i.ua')
tables_gryvna = pd.DataFrame(tables_gryvna0)
#tables.columns = ["Value", "Full_name", "Valid_to", "In_grivnas"]

#Special_column = tables.loc[tables.Full_name == "Доллар".lower(), 'In_grivnas']

#print(tables[0]['Полное название'].head())
"""for i in range(0, len(Special_column)):
    for number in Special_column[i].split(" "):"""
#print(float(list(tables.loc[tables.Full_name == "Доллар".lower(), 'In_grivnas'])[0].split()[0]))
short = tables[0][0]
short.columns = ['Currency', 'From_dollar', 'To_dollar']
long = tables[0][1]
long.columns = ['Currency', 'From_dollar', 'To_dollar']
#for i in long['Currency']:
long = long.append({'Currency': 'Ukrainian Hryvna', 'From_dollar': tables_gryvna[0][0].iloc[0]['НБУ'], 'To_dollar': str(1/float(tables_gryvna[0][0].iloc[0]['НБУ']))},
                   ignore_index=True)
#print(tables_gryvna[0][0].iloc[0]['НБУ'])
print(long)

#print(type(tables))