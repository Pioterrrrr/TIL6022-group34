import pandas as pd
import os
datadir = 'data/'
datalist = os.listdir(datadir)
filepath = []

# if filepath.endswith('xlsx'):
# df = pd.read_excel(filepath)
# elif filepath.endswith('csv'):
# df = pd.read_csv(filepath)
#else #tsv files
# df = pd.read_csv(filepath,sep='\t')

for file in datalist:
    print(file)
    filepath.append('data/' + file)

print(filepath)

for i in range(len(filepath)):
    if i<=4:
        print(filepath[i]+': NISZO+DAVIDE')
        #write your code here
    elif i == 5:
        print(filepath[i]+': PIOTER')
        # from 2018
        df_avia_pa = pd.read_csv(filepath[i])
        avia_countries = df_avia_pa['geo'].unique()
        df_avia_pa_relevant = df_avia_pa.iloc[:,7:10]
        df_avia_pa_relevant = df_avia_pa_relevant.rename({
            'geo':'Geo','TIME_PERIOD':'Time_period','OBS_VALUE': 'Passengers_count'
        }, axis='columns')
        print(df_avia_pa_relevant.head())
    elif i == 6:
        print(filepath[i]+': ZACHOS')
        # write your code here
    elif i == 7:
        print(filepath[i]+': VASILIS')
        # write your code here
    elif i == 8:
        print(filepath[i]+': PIOTER')
        # passenger count in thousands of passengers, from 2017 (columns go to 1997, but with no data)
        df_mar_pa = pd.read_csv(filepath[i],sep='\t')
        print(df_mar_pa.columns)
    elif i == 9:
        print(filepath[i]+': PIOTER')
        # passenger count in thousands of passengers, from 2004
        df_rail_pa = pd.read_csv(filepath[i])
        rail_countries = df_rail_pa['geo'].unique()
        df_rail_pa_relevant = df_rail_pa.iloc[:, 4:7]
        print(df_rail_pa_relevant.columns[2])
        df_rail_pa_relevant = df_rail_pa_relevant.rename({
            'geo': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')
        print(df_rail_pa_relevant.head())

