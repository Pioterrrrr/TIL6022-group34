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
        df_avia_pa = pd.read_csv(filepath[i])
        print(df_avia_pa.head())
    elif i == 6:
        print(filepath[i]+': ZACHOS')
        # write your code here
    elif i == 7:
        print(filepath[i]+': VASILIS')
        # write your code here
    elif i == 8:
        print(filepath[i]+': PIOTER')
        df_mar_pa = pd.read_csv(filepath[i],sep='\t')
        print(df_mar_pa.head())
    elif i == 9:
        print(filepath[i]+': PIOTER')
        df_rail_pa = pd.read_csv(filepath[i])
        print(df_rail_pa.head())

