import pandas as pd
import os
import numpy as np
import warnings
import pycountry  # Import pycountry--> pip install pycountry (used to change 2-code to full name of country)

pydir = os.path.dirname(__file__)
datadir = pydir + '\\data\\'
datalist = os.listdir(datadir)
filepath = []

warnings.filterwarnings("ignore", message="Workbook contains no default style, apply openpyxl's default")
pd.set_option('display.max_columns', None)

for file in datalist:
    filepath.append(pydir + '\\data\\' + file)

# print(filepath)

data_5 = pd.DataFrame()  # combined data 1-5

for i in range(len(filepath)):
    if i == 0:
        df = pd.read_excel(filepath[i])
        df = df.iloc[2:, [2, 3, 23, 31]]
        data_5 = pd.concat([data_5, df], ignore_index=True)

    elif 0 < i < 4:
        df = pd.read_excel(filepath[i])
        df = df.iloc[2:, [2, 3, 23, 31]]
        data_5 = pd.concat([data_5, df], ignore_index=True)

    elif i == 4:
        df = pd.read_excel(filepath[i])
        column_names = df.iloc[1, [2, 3, 23, 31]].tolist()
        df = df.iloc[2:, [2, 3, 23, 31]]
        data_5 = pd.concat([data_5, df], ignore_index=True)
        data_5 = data_5.dropna()  # Remove rows with at least one empty (NaN) value
        data_5 = data_5[(data_5 != 0).all(1)]  # Remove rows with at least one 0 value

        # Assign column names to data_5
        for j, name in enumerate(column_names):
            data_5.columns.values[j] = name

        # calculation of the total C02 emission of all ships (total [Mt] and per ship [t])
        co2_tot = data_5.groupby([data_5.columns[1]])[data_5.columns[2]].agg(
            ['sum', 'count']).reset_index()
        co2_tot = co2_tot.rename(columns={'sum': 'CO2_sum', 'count': 'Element_count'})
        co2_tot['CO2 sum [Mt]'] = co2_tot['CO2_sum'] / (1000000)  # from [t] to [Mt]
        co2_tot['CO2 per ship [t]'] = co2_tot['CO2_sum'] / co2_tot['Element_count']
        co2_tot = co2_tot.iloc[:, [0, 3, 4]]

        # group ship by ship type and reported year +  sum of co2 [tons]
        co2 = data_5.groupby([data_5.columns[0], data_5.columns[1]])[data_5.columns[2]].agg(
            ['sum', 'count']).reset_index()
        # group ship by ship type and reported year +  sum of time at sea [hours]
        time = data_5.groupby([data_5.columns[0], data_5.columns[1]])[data_5.columns[3]].agg(
            ['sum', 'count']).reset_index()

        # rename columns including new elements
        co2 = co2.rename(columns={'sum': 'CO2_sum', 'count': 'Element_count'})
        time = time.rename(columns={'sum': 'Time_sum', 'count': 'Element_count'})

        # calcualtions of the average co2 emission and time at sea per ship category
        co2['CO2 per ship [t]'] = co2['CO2_sum'] / co2['Element_count']
        time['Time at sea per ship [hours]'] = time['Time_sum'] / time['Element_count']

        # delete of not relevant ship category
        ship_type = ['Passenger ship', 'Container ship', 'Bulk carrier', 'LNG carrier', 'Oil tanker']
        co2 = co2[co2[co2.columns[0]].isin(ship_type)]
        time = time[time[time.columns[0]].isin(ship_type)]

        co2_final = co2.iloc[:, [0, 1, 2]]  # C02 emissions in [t] per category per year
        co2 = co2.iloc[:, [0, 1, 4]]  # C02 emissions in [t] per ship per year
        time = time.iloc[:, [0, 1, 4]]  # time spent at sea in [h] per ship per year


        # Build a set of data frame with CO2 emissions [t] per ship per category
        ship_type_data = {}
        # List of relevant ship types
        relevant_ship_types = ['Passenger ship', 'Container ship', 'Bulk carrier', 'LNG carrier', 'Oil tanker']
        for ship_type in relevant_ship_types:
            # Filter data for the specific ship type
            ship_type_df = co2[co2['Ship type'] == ship_type]
            # Pivot the ship type data
            ship_type_pivot = ship_type_df.pivot(index='Reporting Period', columns='Ship type',
                                                 values='CO2 per ship [t]')
            # Reset index to make 'Reporting Period' a column
            ship_type_pivot = ship_type_pivot.reset_index()
            # Store the pivoted data in the dictionary
            ship_type_data[ship_type] = ship_type_pivot
        # Merge the data for all ship types based on the 'Reporting Period'
        merged_data = ship_type_data[relevant_ship_types[0]]
        for ship_type in relevant_ship_types[1:]:
            merged_data = pd.merge(merged_data, ship_type_data[ship_type], on='Reporting Period', how='outer')
        # Set the 'Reporting Period' column as the index
        merged_data = merged_data.set_index('Reporting Period')
        # Reset the index to include 'Reporting Period' as a column
        merged_data = merged_data.reset_index()
        # Sort the DataFrame by 'Reporting Period'
        co2 = merged_data.sort_values('Reporting Period')

        # Build a dataframe with CO2 emissions [t] per each ship category
        ship_type_data = {}
        # List of relevant ship types
        relevant_ship_types = ['Passenger ship', 'Container ship', 'Bulk carrier', 'LNG carrier', 'Oil tanker']
        for ship_type in relevant_ship_types:
            # Filter data for the specific ship type
            ship_type_df = co2_final[co2_final['Ship type'] == ship_type]
            # Pivot the ship type data
            ship_type_pivot = ship_type_df.pivot(index='Reporting Period', columns='Ship type',
                                                 values='CO2_sum')
            # Reset index to make 'Reporting Period' a column
            ship_type_pivot = ship_type_pivot.reset_index()
            # Store the pivoted data in the dictionary
            ship_type_data[ship_type] = ship_type_pivot
        # Merge the data for all ship types based on the 'Reporting Period'
        merged_data = ship_type_data[relevant_ship_types[0]]
        for ship_type in relevant_ship_types[1:]:
            merged_data = pd.merge(merged_data, ship_type_data[ship_type], on='Reporting Period', how='outer')
        # Set the 'Reporting Period' column as the index
        merged_data = merged_data.set_index('Reporting Period')
        # Reset the index to include 'Reporting Period' as a column
        merged_data = merged_data.reset_index()
        # Sort the DataFrame by 'Reporting Period'
        co2_final = merged_data.sort_values('Reporting Period')

        # Calculation of CO2 emissions in [t] for the not considered ship category
        co2_final['Total Co2 emission [t]'] = co2_tot['CO2 sum [Mt]'] * 1000000
        co2_final['Other ships'] = (co2_final['Total Co2 emission [t]'] - co2_final['Bulk carrier']
                                    - co2_final['Container ship'] - co2_final['Passenger ship'] - co2_final[
                                        'Oil tanker']
                                    - co2_final['LNG carrier'])
        co2_final = co2_final.iloc[:, [0, 1, 2, 3, 4, 5, 7]]

        # Build a set of data frame withtime spent at sea [hours] per ship per category
        ship_type_data = {}
        # List of relevant ship types
        relevant_ship_types = ['Passenger ship', 'Container ship', 'Bulk carrier', 'LNG carrier', 'Oil tanker']
        for ship_type in relevant_ship_types:
            # Filter data for the specific ship type
            ship_type_df = time[time['Ship type'] == ship_type]
            # Pivot the ship type data
            ship_type_pivot = ship_type_df.pivot(index='Reporting Period', columns='Ship type',
                                                 values='Time at sea per ship [hours]')
            # Reset index to make 'Reporting Period' a column
            ship_type_pivot = ship_type_pivot.reset_index()
            # Store the pivoted data in the dictionary
            ship_type_data[ship_type] = ship_type_pivot
        # Merge the data for all ship types based on the 'Reporting Period'
        merged_data = ship_type_data[relevant_ship_types[0]]
        for ship_type in relevant_ship_types[1:]:
            merged_data = pd.merge(merged_data, ship_type_data[ship_type], on='Reporting Period', how='outer')
        # Set the 'Reporting Period' column as the index
        merged_data = merged_data.set_index('Reporting Period')
        # Reset the index to include 'Reporting Period' as a column
        merged_data = merged_data.reset_index()
        # Sort the DataFrame by 'Reporting Period'
        time = merged_data.sort_values('Reporting Period')


        # Print dataset in csv format
        df_co2_path = pydir + '\\DATA_PROCESSED\\df_ship_co2.csv'
        co2.to_csv(df_co2_path)
        df_time_path = pydir + '\\DATA_PROCESSED\\df_ship_time.csv'
        time.to_csv(df_time_path)
        df_co2tot_path = pydir + '\\DATA_PROCESSED\\df_ship_co2_total.csv'
        co2_tot.to_csv(df_co2tot_path)
        df_co2final_path = pydir + '\\DATA_PROCESSED\\df_ship_co2_final.csv'
        co2_final.to_csv(df_co2final_path)

    elif i == 5:
        # print(filepath[i]+': PIOTR PIETRZAK')
        # aviation passenger count from 2018

        # the dataframe is loaded
        df_avia_pa = pd.read_csv(filepath[i])

        # avia_countries stores all country codes present in the dataframe
        avia_countries = list(df_avia_pa['geo'].unique())

        # selecting the relevant columns with time period, country and passenger count
        df_avia_pa_relevant = df_avia_pa.iloc[:, 7:10]

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
        df_avia_path = pydir + '\\DATA_PROCESSED\\df_passengers_avia.csv'
        df_avia_pa_relevant.to_csv(df_avia_path)

    elif i == 6:
        # print(filepath[i]+': ZACHOS')
        sheet_name = 'fossil_CO2_by_sector_country_su'  # Replace with the actual sheet name
        df_edgar = pd.read_excel(filepath[i], sheet_name=sheet_name)
        df_edgar = df_edgar.iloc[1450:1458, 51:57]
        edgarsum = df_edgar.sum()
        df_edgar = pd.concat([df_edgar, edgarsum.to_frame().T], ignore_index=True)

        df_edgar = df_edgar.iloc[8, :].to_frame()
        edgar_norm = df_edgar / df_edgar.max() * 100
        df_edgar_relevant = pd.concat([df_edgar, edgar_norm], ignore_index=True, axis=1)
        df_edgar_relevant = df_edgar_relevant.rename({
            df_edgar_relevant.columns[0]: 'CO2_sum', df_edgar_relevant.columns[1]: 'C02_normalized'
        }, axis='columns')
        # print(df_edgar_relevant)

        # Pre-Processing if we use emissions per category (normalized):
        df_edgar_categories = pd.read_excel(filepath[i], sheet_name=sheet_name)
        df_edgar_categories = df_edgar_categories.iloc[1450:1458, 51:57]
        df_edgar_categories = df_edgar_categories.apply(lambda row: (row) / (row.max()), axis=1)

        df_edgar_categories_norm = df_edgar_categories.reset_index(drop=True)

        custom_index_names = ["Agriculture", "Buildings", "Fuel Exploitation",
                              "Industrial Combustion", "Power Industry", "Processes", "Transport", "Waste"
                              ]
        df_edgar_categories_norm.index = custom_index_names
        # print(df_edgar_categories_norm)
        df_emissions_path = pydir + '\\DATA_PROCESSED\\df_emissions.csv'
        df_edgar_relevant.to_csv(df_emissions_path)

    elif i == 7:
        # print(filepath[i]+': VASILIS')

        # Read CSV file
        df_cargo = pd.read_csv(filepath[i])

        # Keep only the relevant columns (country, time-period, cargo)
        df_cargo = df_cargo.iloc[:, [6, 7, 8]]

        # Rename those columns
        df_cargo.columns = ["Country", "Time-period", "Cargo [tons]"]

        # Remove data that is specific to particular cities within each country (contain "_")
        # Remove data that is dated later than 2022.  
        df_cargo = df_cargo[~(df_cargo["Country"].str.contains("_") | df_cargo["Time-period"].str.contains("2023"))]

        # Replace 2-letter code with full name of the country
        # __!!!___FOR THIS STEP pycountry IS NEEDED__!!!__ --> pip install pycountry
        country_mapping = {}
        for code in df_cargo["Country"].unique():
            try:
                country = pycountry.countries.get(alpha_2=code)
                if country:
                    country_name = country.name
                    country_mapping[code] = country_name
                else:
                    if code == "EL":
                        country_mapping[code] = "Greece"  # Dataset has EL insted of GR
                    elif code == "UK":
                        country_mapping[code] = "United Kingdom"  # Dataset has UK insted of GB
            except LookupError:
                country_mapping[code] = "Not Found"
        df_cargo["Country"] = df_cargo["Country"].map(country_mapping)

        # Reform the table into multiple columns
        df_cargo = df_cargo.groupby(["Time-period", "Country"])["Cargo [tons]"].sum().unstack()

        # Print the processed table
        # print(df_cargo.head())
        df_cargo_path = pydir + '\\DATA_PROCESSED\\df_cargo_mar.csv'
        df_cargo.to_csv(df_cargo_path)

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

        # an empty dataframe for relevant data is created, with column names the same as in base dataframe
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
        df_mar_pa_relevant = df_mar_pa_relevant.drop(
            df_mar_pa_relevant[df_mar_pa_relevant['Geo'] == 'BG'].index).reset_index(drop=True)
        mar_countries.remove('BG')

        # BE and UK have stopped providing data to the dataset from 2020, and ME has inconsistent data with many
        # quarters stating zero passengers. They are removed from Q3 of 2020 forward, so that they can still show up in
        # the joint line graph, but do not interfere with passenger drop calculations
        df_mar_pa_relevant = df_mar_pa_relevant.drop(
            df_mar_pa_relevant[df_mar_pa_relevant['Geo'].str.startswith(
                tuple(['BE', 'UK', 'ME'])) & df_mar_pa_relevant['Time_period'].str.startswith(tuple(['2020-Q3','2020-Q4','2021','2022','2023']))].index
        ).reset_index(drop=True)
        # FR and EU have zero passengers reported from 2022 and onward
        df_mar_pa_relevant = df_mar_pa_relevant.drop(
            df_mar_pa_relevant[df_mar_pa_relevant['Geo'].str.startswith(
                tuple(['FR','EU'])) & df_mar_pa_relevant['Time_period'].str.startswith(
                tuple(['2022', '2023']))].index
        ).reset_index(drop=True)
        # SE, NO, NL, DK and IT have zero passengers reported for 2023
        df_mar_pa_relevant = df_mar_pa_relevant.drop(
            df_mar_pa_relevant[df_mar_pa_relevant['Geo'].str.startswith(
                tuple(['SE','NO','NL','DK','IT'])) & df_mar_pa_relevant['Time_period'].str.startswith('2023')].index
        ).reset_index(drop=True)
        # FI has zero passengers reported for q2 of 2023 and im plotting them later
        df_mar_pa_relevant = df_mar_pa_relevant.drop(
            df_mar_pa_relevant[df_mar_pa_relevant['Geo'].str.startswith(
                tuple(['FI'])) & df_mar_pa_relevant['Time_period'].str.startswith('2023-Q2')].index
        ).reset_index(drop=True)

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
        df_mar_pa_relevant['Norm_2019'] = [100 * df_passengers / country_mar_19max[mar_countries.index(df_country)]
                                           for df_country, df_time, df_passengers
                                           in df_mar_pa_relevant.itertuples(index=False)]

        df_mar_path = pydir + '\\DATA_PROCESSED\\df_passengers_mar.csv'
        df_mar_pa_relevant.to_csv(df_mar_path)

    elif i == 9:
        # print(filepath[i]+': PIOTR PIETRZAK')
        # TWO UNITS: millions of km travelled and passenger count in thousands of passengers, from 2004
        # the dataframe is loaded
        df_rail_pa = pd.read_csv(filepath[i])

        # rail_countries stores all country codes present in the dataframe
        rail_countries = list(df_rail_pa['geo'].unique())

        # selecting the proper unit (thousands of passengers) and relevant columns with time period,
        # country and passenger count
        df_rail_pa_relevant = df_rail_pa[df_rail_pa['unit']=='THS_PAS'].iloc[:, 4:7]

        # here, the column names are renamed into names i prefer
        df_rail_pa_relevant = df_rail_pa_relevant.rename({
            'geo': 'Geo', 'TIME_PERIOD': 'Time_period', 'OBS_VALUE': 'Passengers_count'
        }, axis='columns')

        # this piece of code removes AT, BA, RS, BE and all coupled EU data because they are missing data either entirely,
        # or in key time ranges
        df_rail_pa_relevant = df_rail_pa_relevant.drop(
            df_rail_pa_relevant[df_rail_pa_relevant['Geo'].str.startswith(tuple(['AT', 'BA', 'RS', 'EU27_2007', 'BE', 'EU28', 'EU27_2020']))].index
        ).reset_index(drop=True)
        rail_countries = [elm for elm in rail_countries if elm not in {'AT', 'RS', 'BA', 'EU27_2007', 'BE', 'EU28', 'EU27_2020'}]

        # this piece of code multiplies all passenger counts by 1000, so that the unit is 1 instead of 1000
        df_rail_pa_relevant['Passengers_count'] *= 1000

        # this piece of code selects only data from after Q1 of 2018 (the years are lazily iterated one by one,
        # i'd think of a more elegant way of handling this if there was a need)
        df_rail_pa_relevant = df_rail_pa_relevant[
            df_rail_pa_relevant['Time_period'].str.startswith(tuple(["2018", "2019", "2020", "2021", "2022", "2023"]))]

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

        df_rail_path = pydir + '\\DATA_PROCESSED\\df_passengers_rail.csv'
        df_rail_pa_relevant.to_csv(df_rail_path)
