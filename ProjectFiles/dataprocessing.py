import pandas as pd
import os
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

for file in datalist:
    print(file)
    filepath.append(pydir + '\\data\\' + file)

print(filepath)

for i in range(len(filepath)):
    if i<=4:
        print(filepath[i]+': NISZO+DAVIDE')
        #write your code here
        # needed actions: sort data (per ship type) -> save
    elif i == 5:
        print(filepath[i]+': PIOTER')
        # write your code here
    elif i == 6:
        print(filepath[i]+': ZACHOS')
        # write your code here
    elif i == 7:
        print(filepath[i]+': VASILIS')
        # Import pycountry--> pip install pycountry (used to change 2-code to full name of country)
        import pycountry 

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