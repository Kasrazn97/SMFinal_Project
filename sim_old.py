
"""
This module runs the simulation.
"""

import pandas as pd
import numpy as np

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
    return data

data = load_data('df_for_final_sim_137unique.csv')
data.co2 = data.co2 / 10000
data.gdp = np.log(data.gdp)
data = data.dropna()

## --------------------- 1ST RUN ------------------------------ ##

model = MigrationModel(data, policies=True)
model.run(4)

## --------------------- PLOTS ------------------------------ ##

destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']
plot_immigration_flow(model.countries_report[model.countries_report.country.isin(destinations)])
model.countries_report.country.nunique()




top_destinations = ['Australia', 'Canada', 'Chile', 'Germany', 'New Zealand','United Kingdom', 'United States']
plot_immigration_flow(model.countries_report[model.countries_report.country.isin(top_destinations)])

plot_em_countries = ['Angola', 'Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Belarus',
       'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
       'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso',
       'Burundi', 'Cabo Verde', 'Cambodia']
plot_emmigration_flow(model.countries_report[model.countries_report.country.isin(plot_em_countries)&(model.countries_report.step>0)])
model.countries_report[model.countries_report.country.isin(plot_em_countries)&(model.countries_report.step>0)]

df1 = model.countries_report[model.countries_report.country.isin(top_destinations)]
df1['num_of_immigrants'] = model.countries_report.num_of_immigrants.diff(periods = 137)
df1['num_of_emmigrants'] = model.countries_report.num_of_emmigrants.diff(periods = 137)
df1['num_of_immigrants'] = df1['num_of_immigrants'].fillna(0)
df1['num_of_emmigrants'] = df1['num_of_emmigrants'].fillna(0)
plot_immigration_flow(df1)
df1.groupby('step')['num_of_immigrants'].sum()

plt.bar(df1[df1.country == 'Sweden']['step'], df1[df1.country == 'Sweden']['num_of_immigrants'])

model.countries_dict['Sweden'].num_of_emmigrants
len(model.agentlist)


plt.bar(df1[df1.country == 'Sweden']['step'], df1[df1.country == 'Sweden']['num_of_immigrants'])

model.countries_report.groupby('step')['population'].mean()
model.countries_dict[c].num_of_immigrants


## ------------------------- ANALYSIS ------------------------------ ##

data[(data.year == 0)&(data.country.isin(destinations))].sort_values('gdp')
senders = set(data.country.unique()) - set(destinations)
data_on_senders = data[data.country.isin(senders)]
data_on_destinations = data[data.country.isin(destinations)]

data_on_senders[data_on_senders.year <= 4].iloc[:, 1:].groupby('year').mean()
data_on_destinations[data_on_destinations.year <= 4].iloc[:, 1:].groupby('year').mean()

plt.plot(data_on_senders.year.unique(), data_on_senders.iloc[:, 1:].groupby('year').mean())
plt.plot(data_on_senders.year.unique(), data_on_destinations.iloc[:, 1:].groupby('year').mean())
plt.legend()
data_on_destinations.iloc[:, 1:].groupby('year').mean()

data_on_senders[data_on_senders.year > 4].iloc[:, 1:].groupby('year').mean()
data_on_destinations[data_on_destinations.year > 4].iloc[:, 1:].groupby('year').mean()

## ------------------------- CHECKS ------------------------------ ##

# number of new immigrantes at each step
model.countries_report.groupby('step')['num_of_immigrants'].sum().diff()
model.countries_report.groupby('step')['num_of_emmigrants'].sum().diff()
model.countries_report['num_of_emmigrants'].sum()

model.countries_report.groupby(['country'])['num_of_emmigrants'].sum().sort_values(ascending=False)[:50]
# average population in sender countries 
for col in ['step', 'num_of_immigrants', 'num_of_emmigrants', 'population']:
    model.countries_report[col] =  model.countries_report[col].astype('int64')
model.countries_report[model.countries_report.country.isin(senders)].groupby('step').population.describe()

# average population in destination countries 
model.countries_report[model.countries_report.country.isin(destinations)].groupby('step').population.describe()

# avg number of emmigrants in sender countries
model.countries_report[model.countries_report.country.isin(senders)].groupby('step')['num_of_emmigrants'].mean()
model.countries_report[model.countries_report.country.isin(destinations)].groupby('step')['num_of_emmigrants'].mean()

# average willingness_to_move at each step
model.agents_report.willingness_to_move = model.agents_report.willingness_to_move.astype('float')
model.agents_report.groupby('step').willingness_to_move.describe()

# average age at each step
model.agents_report.age = model.agents_report.age.astype('float')
model.agents_report.groupby('step').age.describe()

# status of agents at each step
model.agents_report.groupby('step').status.value_counts()

# A given country statistics
model.get_country_stats('Austria')

# most popular destinations at each step
model.countries_report.groupby(['step', 'country'])['num_of_immigrants'].sum().sort_values(ascending=False)[:50]

model.countries_dict['Angola'].data_diff

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


fruits = ['apple', 'pear', 'ananas']
for word in fruits:
    if word != 'banana':
        fruits.append('banana')

model.agents_report.groupby('step').agent.nunique()
