import pandas as pd
import os
import warnings

datadir = 'data/'
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
    print(file)
    filepath.append('data/' + file)

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
        # write your code here
    elif i == 7:
        print(filepath[i]+': VASILIS')
        # write your code here
    elif i == 8:
        print(filepath[i]+': PIOTER')
        # write your code here
    elif i == 9:
        print(filepath[i]+': PIOTER')
        # write your code here

