import pandas as pd
import os
print(os.getcwd())
pydir = os.path.dirname(__file__)
print(pydir)
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
    filepath.append(pydir+'\\data\\' + file)

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
        # write your code here
    elif i == 8:
        print(filepath[i]+': PIOTER')
        # write your code here
    elif i == 9:
        print(filepath[i]+': PIOTER')
        # write your code here

