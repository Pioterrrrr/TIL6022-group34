import pandas as pd
import os
import warnings
import pycountry # Import pycountry--> pip install pycountry (used to change 2-code to full name of country)

pydir = os.path.dirname(__file__)
datadir = pydir + '\\data\\'

datalist = os.listdir(datadir)
filepath = []

# if filepath.endswith('xlsx'):
# df = pd.read_excel(filepath)
# elif filepath.endswith('csv'):
# df = pd.read_csv(filepath)
#else #tsv files
# df = pd.read_csv(filepath,sep='\t')

warnings.filterwarnings("ignore", message="Workbook contains no default style, apply openpyxl's default")

for file in datalist:
#     print(file)
    filepath.append(pydir + '\\data\\' + file)

print(filepath)

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
        data_5 = data_5[(data_5 != 0).all(1)]   # Remove rows with at least one 0 value

        # Assign column names to data_5
        for j, name in enumerate(column_names):
            data_5.columns.values[j] = name

        co2_tot = data_5.groupby([data_5.columns[1]])[data_5.columns[2]].agg(
            ['sum', 'count']).reset_index()
        co2_tot = co2_tot.rename(columns={'sum': 'CO2_sum', 'count': 'Element_count'})
        co2_tot['CO2 per ship [t]'] = co2_tot['CO2_sum'] / co2_tot['Element_count']
        co2_tot = co2_tot.iloc[:, [0, 3]]

        # group ship by ship type and reported year +  sum of co2 [tons]
        co2 = data_5.groupby([data_5.columns[0], data_5.columns[1]])[data_5.columns[2]].agg(
            ['sum', 'count']).reset_index()
        # group ship by ship type and reported year +  sum of time at sea [hours]
        time = data_5.groupby([data_5.columns[0], data_5.columns[1]])[data_5.columns[3]].agg(
            ['sum', 'count']).reset_index()

        # rename columns including new elements
        co2 = co2.rename(columns={'sum': 'CO2_sum', 'count': 'Element_count'})
        time = time.rename(columns={'sum': 'Time_sum', 'count': 'Element_count'})

        # calcualtions of the average co2 emission and time at sea per ship category (considering the availbale ship data each year)
        co2['CO2 per ship [t]'] = co2['CO2_sum'] / co2['Element_count']
        time['Time at sea per ship [hours]'] = time['Time_sum'] / time['Element_count']

        # delete of not relevant ship category
        ship_type = ['Passenger ship', 'Container ship', 'Bulk carrier', 'LNG carrier', 'Oil tanker']
        co2 = co2[co2[co2.columns[0]].isin(ship_type)]
        time = time[time[time.columns[0]].isin(ship_type)]

        # new dataset with only relevant data (co2 emission and time at sea per ship per year)
        co2 = co2.iloc[:, [0, 1, 4]]
        time = time.iloc[:, [0, 1, 4]]

        # building table
        co2 = co2.pivot(index=co2.columns[0], columns=co2.columns[1], values=co2.columns[2])
        time = time.pivot(index=time.columns[0], columns=time.columns[1], values=time.columns[2])

        print(co2)
        print(time)
        print(co2_tot)

    elif i == 5:
        print(filepath[i]+': PIOTER')
        # write your code here
    elif i == 6:
        print(filepath[i]+': ZACHOS')
        sheet_name = 'fossil_CO2_by_sector_country_su'  # Replace with the actual sheet name
        df_edgar = pd.read_excel(filepath[i], sheet_name=sheet_name)
        df_edgar = df_edgar.iloc[1450:1458,51:57]
        edgarsum = df_edgar.sum()
        df_edgar = pd.concat([df_edgar, edgarsum.to_frame().T], ignore_index=True)
        
        df_edgar = df_edgar.iloc[8,:].to_frame()
        edgar_norm = df_edgar/df_edgar.max()*100
        df_edgar_relevant = pd.concat([df_edgar, edgar_norm], ignore_index=True,axis=1)
        df_edgar_relevant = df_edgar_relevant.rename({
            df_edgar_relevant.columns[0]:'CO2_sum', df_edgar_relevant.columns[1]:'C02_normalized'
        },axis='columns')
        print(df_edgar_relevant)
        
        #Pre-Processing if we use emissions per category (normalized): 
        df_edgar_categories = pd.read_excel(filepath[i], sheet_name=sheet_name)
        df_edgar_categories = df_edgar_categories.iloc[1450:1458,51:57]
        df_edgar_categories = df_edgar_categories.apply(lambda row: (row) / (row.max()), axis=1)

        df_edgar_categories_norm = df_edgar_categories.reset_index(drop=True)
        
        custom_index_names = ["Agriculture", "Buildings", "Fuel Exploitation", 
                              "Industrial Combustion", "Power Industry", "Processes","Transport", "Waste"
                             ] 
        df_edgar_categories_norm.index = custom_index_names
        print(df_edgar_categories_norm)
        
    elif i == 7:
        print(filepath[i]+': VASILIS')
        
        

        # Read CSV file
        df_cargo = pd.read_csv(filepath[i])

        # Keep only the relevant columns (country, time-period, cargo)
        df_cargo = df_cargo.iloc[:,[6, 7, 8]]

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
                country = pycountry.countries.get(alpha_2 = code)
                if country:
                    country_name = country.name
                    country_mapping[code] = country_name
                else:
                    if code == "EL":
                        country_mapping[code] = "Greece"   # Dataset has EL insted of GR
                    elif code == "UK":
                        country_mapping[code] = "United Kingdom" # Dataset has UK insted of GB     
            except LookupError:
                country_mapping[code] = "Not Found"
        df_cargo["Country"] = df_cargo["Country"].map(country_mapping)

        # Reform the table into multiple columns
        df_cargo = df_cargo.groupby(["Time-period", "Country"])["Cargo [tons]"].sum().unstack()

        # Print the processed table
        print(df_cargo.head())

    elif i == 8:
        print(filepath[i]+': PIOTER')
        # write your code here
    elif i == 9:
        print(filepath[i]+': PIOTER')
        # write your code here