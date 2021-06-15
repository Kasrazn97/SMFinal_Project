
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
model.run(3)

## --------------------- PLOTS ------------------------------ ##

destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']
top_destinations = ['Australia', 'Canada', 'Chile', 'Germany', 'New Zealand','United Kingdom', 'United States']

# cumulative emigration flow
plot_em_countries = ['Angola', 'Argentina', 'Armenia', 'Azerbaijan', 'Bahrain', 'Belarus',
       'Bolivia', 'Bosnia and Herzegovina', 'Botswana',
       'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso',
       'Burundi', 'Cabo Verde', 'Cambodia']
plot_emmigration_flow(model.countries_report[model.countries_report.country.isin(plot_em_countries)&(model.countries_report.step>0)])

# net immigration flow
df1 = model.countries_report[model.countries_report.country.isin(top_destinations)]
df1['num_of_immigrants'] = model.countries_report.num_of_immigrants.diff(periods = 137)
df1['num_of_emmigrants'] = model.countries_report.num_of_emmigrants.diff(periods = 137)
df1['num_of_immigrants'] = df1['num_of_immigrants'].fillna(0)
df1['num_of_emmigrants'] = df1['num_of_emmigrants'].fillna(0)
plot_immigration_flow(df1)

# A given country statistics
model.get_country_stats('Austria')
model.agents_report.head()
model.countries_report[model.countries_report.step==1].head()


