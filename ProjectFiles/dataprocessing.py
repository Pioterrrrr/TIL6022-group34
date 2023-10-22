import pandas as pd
import os
pydir = os.path.dirname(__file__)
datadir = pydir+'\\data\\'
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
    filepath.append(pydir + '\\data\\' + file)

# print(filepath)

for i in range(len(filepath)):
    if i<=4:
        print(filepath[i]+': NISZO+DAVIDE')
        #write your code here
    elif i == 5:
        print(filepath[i]+': PIOTR PIETRZAK')
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
        print(filepath[i]+': PIOTR PIETRZAK')
        # passenger count in thousands of passengers, from 2017
        df_mar_pa = pd.read_csv(filepath[i])
        df_mar_pa = df_mar_pa.iloc[:,6:9]
        time_periods = df_mar_pa['TIME_PERIOD'].unique()
        reporting_entities = df_mar_pa['rep_mar'].unique()
        mar_countries = []
        for r in reporting_entities:
            country = r[:2]
            if country not in mar_countries:
                mar_countries.append(country)
        df_mar_pa_relevant = pd.DataFrame(columns=df_mar_pa.columns)
        # mar_sum = df_mar_pa[(df_mar_pa['TIME_PERIOD']=='2020-Q2')&(df_mar_pa['rep_mar'].str.startswith('BE'))].sum(numeric_only=True)
        # print(mar_sum)
        index_df_mar = 0;
        for country in mar_countries:
            for quarter in time_periods:
                mar_sum = df_mar_pa[(df_mar_pa['TIME_PERIOD']==quarter)&(df_mar_pa['rep_mar'].str.startswith(country))].sum(numeric_only=True)
                # print(mar_sum.iloc[0])
                df_mar_pa_relevant = pd.concat([df_mar_pa_relevant,pd.DataFrame({'rep_mar':country,
                                                                                 'TIME_PERIOD':quarter,
                                                                                 'OBS_VALUE':mar_sum.iloc[0]},index=[index_df_mar])])
                index_df_mar += 1
        df_mar_pa_relevant = df_mar_pa_relevant.rename({
            'rep_mar': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')
        print(df_mar_pa_relevant.head())
    elif i == 9:
        print(filepath[i]+': PIOTR PIETRZAK')
        # passenger count in thousands of passengers, from 2004
        df_rail_pa = pd.read_csv(filepath[i])
        rail_countries = df_rail_pa['geo'].unique()
        df_rail_pa_relevant = df_rail_pa.iloc[:, 4:7]
        df_rail_pa_relevant = df_rail_pa_relevant.rename({
            'geo': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')
        print(df_rail_pa_relevant.head())

