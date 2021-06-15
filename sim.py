
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

## --------------------- RUN SIMULATION ------------------------ ## 

model = MigrationModel(data, policies=True)
model.run(4)

## --------------------- PLOTS ------------------------------ ##

# destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
#         'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
#         'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
#         'Switzerland', 'United Kingdom', 'United States']
# plot_immigration_flow(model.countries_report[model.countries_report.country.isin(destinations)])

top_destinations = ['Australia', 'Canada', 'Chile', 'Germany', 'New Zealand','United Kingdom', 'United States']
# plot_immigration_flow(model.countries_report[model.countries_report.country.isin(top_destinations)])

# plot_em_countries = ['Angola', 'Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Belarus',
#        'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
#        'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso',
#        'Burundi', 'Cabo Verde', 'Cambodia']
# plot_emmigration_flow(model.countries_report[model.countries_report.country.isin(plot_em_countries)&(model.countries_report.step>0)])

df1 = model.countries_report[model.countries_report.country.isin(top_destinations)]
df1['num_of_immigrants'] = model.countries_report.num_of_immigrants.diff(periods = 137)
df1['num_of_emmigrants'] = model.countries_report.num_of_emmigrants.diff(periods = 137)
df1['num_of_immigrants'] = df1['num_of_immigrants'].fillna(0)
df1['num_of_emmigrants'] = df1['num_of_emmigrants'].fillna(0)
plot_immigration_flow(df1)


## ------------------------- ANALYSIS ------------------------------ ##

# number of new immigrantes at each step
model.countries_report.groupby('step')['num_of_immigrants'].sum().diff()
model.countries_report['num_of_emmigrants'].sum()

model.countries_report.groupby(['country'])['num_of_emmigrants'].sum().sort_values(ascending=False)[:50]
# average population in sender countries 
senders = set(data.country.unique()) - set(destinations)
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

# A given country statistics
model.get_country_stats('Austria')

# most popular destinations at each step
model.countries_report.groupby(['step', 'country'])['num_of_immigrants'].sum().sort_values(ascending=False)[:50]


