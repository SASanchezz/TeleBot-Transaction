import pandas as pd

tables0 = pd.read_html('https://kurs.com.ua/nbu')
tables = tables0[0]
tables.columns = ["Value", "Full_name", "Valid_to", "In_grivnas"]

Special_column = tables.loc[tables.Full_name == "Доллар".lower(), 'In_grivnas']

#print(tables[0]['Полное название'].head())
"""for i in range(0, len(Special_column)):
    for number in Special_column[i].split(" "):"""
#print(list(tables["Full_name"]))