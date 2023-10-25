import pandas as pd
import os
import numpy as np
pydir = os.path.dirname(__file__)
datadir = pydir+'\\data\\'
datalist = os.listdir(datadir)
filepath = []

# if filepath.endswith('xlsx'):
# df = pd.read_excel(filepath)
# elif filepath.endswith('csv'):
# df = pd.read_csv(filepath)
# else #tsv files
# df = pd.read_csv(filepath,sep='\t')

for file in datalist:
    # print(file)
    filepath.append(pydir + '\\data\\' + file)

# print(filepath)

for i in range(len(filepath)):
    if i<=4:
        print(filepath[i]+': NISZO+DAVIDE')
        # write your code here
    elif i == 5:
        # print(filepath[i]+': PIOTR PIETRZAK')
        # aviation passenger count from 2018

        #the dataframe is loaded
        df_avia_pa = pd.read_csv(filepath[i])

        #avia_countries stores all country codes present in the dataframe
        avia_countries = list(df_avia_pa['geo'].unique())

        # selecting the relevant columns with time period, country and passenger count
        df_avia_pa_relevant = df_avia_pa.iloc[:,7:10]

        # here, the column names are renamed into names i prefer
        df_avia_pa_relevant = df_avia_pa_relevant.rename({
            'geo': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')

        # this piece of code searches for the maximum passenger count per country in
        # any quarter of 2019 and saves it in a table
        country_avia_19max = []
        for country in avia_countries:
            country_avia_19max.append(df_avia_pa_relevant[
                                         (df_avia_pa_relevant['Geo'] == country) &
                                         (df_avia_pa_relevant['Time_period'].str.startswith('2019'))
                                         ].max()['Passengers_count'])

        # this piece of code normalizes the passenger count for each timestep
        # with the respective maximum amount from 2019 for a given country
        # and saves it into the column "Norm_2019"
        df_avia_pa_relevant['Norm_2019'] = [100 * df_passengers / country_avia_19max[avia_countries.index(df_country)]
                                           for df_country, df_time, df_passengers
                                           in df_avia_pa_relevant.itertuples(index=False)]

        # print(df_avia_pa_relevant)
    elif i == 6:
        print(filepath[i]+': ZACHOS')
        # write your code here
    elif i == 7:
        print(filepath[i]+': VASILIS')
        # write your code here
    elif i == 8:
        # print(filepath[i]+': PIOTR PIETRZAK')
        # maritime passenger count in thousands of passengers, from 2017
        # the dataframe is loaded
        df_mar_pa = pd.read_csv(filepath[i])

        # selecting the relevant columns with time period, reporting entity code and passenger count
        df_mar_pa = df_mar_pa.iloc[:, 6:9]
        time_periods = df_mar_pa['TIME_PERIOD'].unique()
        reporting_entities = df_mar_pa['rep_mar'].unique()

        # mar_countries stores all country codes present in the dataframe
        # here it is a little more complicated due to multiple reporting entities per country,
        # all of which start with that country's code
        mar_countries = []
        for r in reporting_entities:
            country = r[:2]
            if country not in mar_countries:
                mar_countries.append(country)

        #an empty dataframe for relevant data is created, with column names the same as in base dataframe
        df_mar_pa_relevant = pd.DataFrame(columns=df_mar_pa.columns)

        # this piece of code sums all passenger counts per country for a given timestamp
        # and adds the data to the new dataframe
        index_df_mar = 0
        for country in mar_countries:
            for quarter in time_periods:
                # this variable stores the sum for a given country & timestamp combination
                mar_sum = df_mar_pa[
                    (df_mar_pa['TIME_PERIOD'] == quarter) &
                    (df_mar_pa['rep_mar'].str.startswith(country))
                    ].sum(numeric_only=True)
                df_mar_pa_relevant = pd.concat(
                    [df_mar_pa_relevant,
                     pd.DataFrame({'rep_mar': country,
                                        'TIME_PERIOD': quarter,
                                        'OBS_VALUE': mar_sum.iloc[0]},
                                        index=[index_df_mar])])
                # index_df_mar variable serves as the index of the new dataframe and is incremented for every
                # new combination of country & timestamp
                index_df_mar += 1

        # here, the column names are renamed into names i prefer
        df_mar_pa_relevant = df_mar_pa_relevant.rename({
            'rep_mar': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')

        # 'BG' needs to be dropped because there is no data available for this country,
        #  resulting in division by zero when normalizing
        df_mar_pa_relevant = df_mar_pa_relevant.drop(df_mar_pa_relevant[df_mar_pa_relevant['Geo']=='BG'].index).reset_index(drop=True)
        mar_countries.remove('BG')

        # this piece of code multiplies all passenger counts by 1000, so that the unit is 1 instead of 1000
        df_mar_pa_relevant['Passengers_count'] *= 1000

        # this piece of code selects only data from after Q1 of 2018 (the years are lazily iterated one by one,
        # i'd think of a more elegant way of handling this if there was a need)
        df_mar_pa_relevant = df_mar_pa_relevant[
            df_mar_pa_relevant['Time_period'].str.startswith(tuple(["2018", "2019", "2020", "2021", "2022", "2023"]))]

        # this piece of code searches for the maximum passenger count per country in
        # any quarter of 2019 and saves it in a table
        country_mar_19max = []
        for country in mar_countries:
            country_mar_19max.append(df_mar_pa_relevant[
                                     (df_mar_pa_relevant['Geo'] == country) &
                                     (df_mar_pa_relevant['Time_period'].str.startswith('2019'))
                                     ].max()['Passengers_count'])

        # this piece of code normalizes the passenger count for each timestep
        # with the respective maximum amount from 2019 for a given country
        # and saves it into the column "Norm_2019"
        df_mar_pa_relevant['Norm_2019'] = [100*df_passengers/country_mar_19max[mar_countries.index(df_country)]
                                           for df_country,df_time,df_passengers
                                           in df_mar_pa_relevant.itertuples(index=False)]

        # print(df_mar_pa_relevant)
    elif i == 9:
        # print(filepath[i]+': PIOTR PIETRZAK')
        # passenger count in thousands of passengers, from 2004
        # the dataframe is loaded
        df_rail_pa = pd.read_csv(filepath[i])

        # rail_countries stores all country codes present in the dataframe
        rail_countries = list(df_rail_pa['geo'].unique())

        # selecting the relevant columns with time period, country and passenger count
        df_rail_pa_relevant = df_rail_pa.iloc[:, 4:7]

        # here, the column names are renamed into names i prefer
        df_rail_pa_relevant = df_rail_pa_relevant.rename({
            'geo': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')

        # this piece of code multiplies all passenger counts by 1000, so that the unit is 1 instead of 1000
        df_rail_pa_relevant['Passengers_count'] *= 1000

        # this piece of code selects only data from after Q1 of 2018 (the years are lazily iterated one by one,
        # i'd think of a more elegant way of handling this if there was a need)
        df_rail_pa_relevant = df_rail_pa_relevant[
            df_rail_pa_relevant['Time_period'].str.startswith(tuple(["2018","2019","2020","2021","2022","2023"]))]

        # this piece of code searches for the maximum passenger count per country in
        # any quarter of 2019 and saves it in a table
        country_rail_19max = []
        for country in rail_countries:
            country_rail_19max.append(df_rail_pa_relevant[
                                     (df_rail_pa_relevant['Geo'] == country) &
                                     (df_rail_pa_relevant['Time_period'].str.startswith('2019'))
                                     ].max()['Passengers_count'])

        # this piece of code normalizes the passenger count for each timestep
        # with the respective maximum amount from 2019 for a given country
        # and saves it into the column "Norm_2019"
        df_rail_pa_relevant['Norm_2019'] = [100 * df_passengers / country_rail_19max[rail_countries.index(df_country)]
                                           for df_country, df_time, df_passengers
                                           in df_rail_pa_relevant.itertuples(index=False)]

        # print(df_rail_pa_relevant)
