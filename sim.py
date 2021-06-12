
"""
This module runs the simulation.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from Agent import *
from Country import *
from MigrationModel import *
from plots import *

def load_data(file_path):
    """
    Data should be in .csv format. [add any data transformations here]
    """
    data = pd.read_csv(file_path)
    if data.columns[0] == 'Unnamed: 0':
        data = data.drop('Unnamed: 0', axis=1)
    # change year to timestep
    # data.year = data.year.map({k:v for k, v in zip(data.year.unique(), np.arange(len(data.year)))})
    # data = data[data['year'] != 39]
    # scaler = MinMaxScaler() # rescale data
    # X = scaler.fit_transform(data.iloc[:,1:6]) # only indicators
    # df = pd.DataFrame(X)
    # df.columns = data.iloc[:,1:6].columns
    # df = pd.concat([data['country'], df, data['year']], axis=1)
    return data

# data = load_data('all_data.csv')
# data.drop('y', axis=1, inplace=True)
data = load_data('df_for_final_sim_137unique.csv')
# data.country.nunique()
# data.year = data.year.map({k:v for k, v in zip(data.year.unique(), np.arange(40))})
# data = data[data['year'] != 39]
data.co2 = data.co2 / 10000
data.gdp = np.log(data.gdp)

model = MigrationModel(data.dropna())
model.run(2)
model.get_country_stats('Bulgaria')

## --------------------- PLOTS ------------------------------ ##

destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']

plot_immigration_flow(model.countries_report[model.countries_report.country.isin(destinations)])

plt.bar(model.countries_report[model.countries_report.country == 'Germany']['step'], model.countries_report[model.countries_report.country == 'Germany']['num_of_immigrants'])

plot_em_countries = ['Angola', 'Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Belarus',
       'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
       'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso',
       'Burundi', 'Cabo Verde', 'Cambodia']

plot_emmigration_flow(model.countries_report[model.countries_report.country.isin(plot_em_countries)])

df1 = model.countries_report
df1['num_of_immigrants'] = model.countries_report.num_of_immigrants.diff(periods = 137)
df1['num_of_immigrants'] = df1['num_of_immigrants'].fillna(0)

## ------------------------- CHECKS ------------------------------ ##

model.countries_report[model.countries_report.country == 'Burkina Faso']
model.countries_report.step.max()+1.5
model.agents_report.head(30)
model.countries_report.country.unique()[:30]
model.agents_report.groupby('step').status.sum()
model.agents_report.groupby('step').status.value_counts()
model.agents_report.groupby('agent').status.sum()
model.agents_report.agent.nunique()
model.agents_report[(model.agents_report.step == 1)&(model.agents_report.status == False)]

model.agents_report[model.agents_report.agent == 4106][-20:]

model.countries_report.groupby('step')['num_of_immigrants'].sum()
# model.create_countries()
model.countries_dict['Australia'].get_data_diff()
model.countries_dict['Albania'].new_born
print(len(model.countries_dict['Togo'].prob))
# model.countries_dict['Australia'].data_diff
# model.countries_dict['Australia'].population
for c in model.countries_dict.keys():
    print(model.countries_dict[c].new_born)

model.get_country_stats('Austria')

model.agentlist[-1:][0].id
# pd.read_csv('/Users/aliyadavletshina/Desktop/Bocconi/modeling&simulation/final_project/SMFinal_Project/data/Country_probabilities.csv')
# pd.read_csv('data/Education_index.csv')

# data = pd.read_csv('data/countries_data_1.csv', sep=';', nrows=31)
# data = data.drop_duplicates(subset='country')
# data = data.reset_index(drop=True)
# all_data = pd.DataFrame()
# for country in data.country.unique():
#     df = pd.DataFrame(np.tile(data[data.country == country], (30,1)))
#     all_data = all_data.append(df, ignore_index=True)
# all_data.columns = data.columns
# all_data['gdp'] = all_data['gdp'].apply(lambda x: np.log(x))
# all_data.to_csv('all_data.csv', header=True)
# data = pd.read_csv('all_data.csv').drop('Unnamed: 0', axis=1)

# countries_dict = {}
# destinations = ['Austria', 'Germany']
# for country in data.country.unique():
#     c = Country(data[data['country'] == country]) # df is dataframe with all info about countries
#     countries_dict[country] = c

# destinations_names = [country for country in list(countries_dict.keys()) if country in destinations]
# destinations = {k: v for k,v in countries_dict.items() if k in destinations_names}


## ------------------- MERGING DATA WITH ALL INDICATORS ------------------ ##

co2 = load_data('data/Ok/CO2.csv')
co2['Country Name'].nunique()

expRD = load_data('data/Ok/ExpRD.csv')
expRD['Country Name'].nunique()

GDP = load_data('data/Ok/GDP.csv')
GDP['Country Name'].nunique()

expEd = load_data('data/Ok/GovExpEdu.csv')
expEd['Country Name'].nunique()

expHealth = load_data('data/Ok/GovExpHealth.csv')
expHealth['Country Name'].nunique()

lifeExp = load_data('data/Ok/LifeExpectency.csv')
lifeExp['Country Name'].nunique()

def set_country_index(df):
    df = df.rename({'Country Name': 'country', 'variable':'year'}, axis=1)
    df = df.set_index(['country', 'year'])
    return df

co2 = set_country_index(co2)
expRD = set_country_index(expRD)
expEd = set_country_index(expEd)
expHealth = set_country_index(expHealth)
lifeExp = set_country_index(lifeExp)
gdp = set_country_index(GDP)

co2.columns = ['co2']
expRD.columns = ['expRD']
expEd.columns = ['expEd']
expHealth.columns = ['expHealth']
lifeExp.columns = ['lifeExp']
gdp.columns = ['gdp']

data = co2.join(expRD).join(expEd).join(expHealth).join(gdp)
data = data.reset_index()
data.columns
cols = ['country', 'co2', 'expRD', 'expEd', 'expHealth', 'gdp', 'year']
data = data[cols]

data.dropna().groupby('year').country.nunique()
data.year = data.year.map({k:v for k, v in zip(data.year.unique(), np.arange(40))})
data = data[data['year'] != 39]
data.dropna().to_csv('df_for_final_sim_137unique.csv') 

df = load_data('data/all_emigrants_high.csv')
df.iloc[:, 1:8].interpolate(axis=1, )
