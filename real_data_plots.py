import matplotlib.pyplot as plt
import numpy as np
from plots import *
import pandas as pd 

data = pd.read_csv('data/all_emigrants_high_interpolated.csv')
data = data.iloc[:,1:]

df_countries = pd.read_csv('df_for_final_sim_137unique.csv').drop('Unnamed: 0', axis=1)
countries_with_data = df_countries.country.unique()

destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']
len(destinations)

len(set(countries_with_data) - set(destinations))
assert len([c for c in destinations if c in countries_with_data]) == len(destinations)

row_migration_by_destination = pd.read_csv('row_migration_by_destination.csv')
row_migration_by_destination.iloc[:, 1:] = row_migration_by_destination.iloc[:, 1:].diff(axis=1)
row_migration_by_destination_melt = row_migration_by_destination.melt('country_to', var_name='year', value_name='num_of_immigrants')
row_migration_by_destination_melt = row_migration_by_destination_melt.rename({'country_to': 'country', 'year':'step'}, axis=1)
row_migration_by_destination_melt.step = row_migration_by_destination_melt.step.map({k:v for k, v in zip(row_migration_by_destination_melt.step.unique(), np.arange(1,32))})
plot_immigration_flow(row_migration_by_destination_melt[~row_migration_by_destination_melt.country.isin(['United States', 'Canada', 'United Kingdom'])])


all_emigrants_high_net = pd.read_csv('data/all_emigrants_high_net.csv')
all_emigrants_high_net = all_emigrants_high_net.drop(columns=['Unnamed: 0', '1980', '1981', '1982', '1983', '1984', 'country_from'])
all_emigrants_high_net_melt = all_emigrants_high_net.melt('country_to', var_name='year', value_name='num_of_immigrants')
all_emigrants_high_net_melt = all_emigrants_high_net_melt.rename({'country_to': 'country', 'year':'step'}, axis=1)
all_emigrants_high_net_melt.step = all_emigrants_high_net_melt.step.map({k:v for k, v in zip(all_emigrants_high_net_melt.step.unique(), np.arange(1,27))})
all_emigrants_high_net_melt = all_emigrants_high_net_melt.groupby(['country', 'step']).sum().reset_index()
all_emigrants_high_net_melt.num_of_immigrants /= 1000
plot_immigration_flow(all_emigrants_high_net_melt)

## TOP COUNTRIES ##
top_destinations = ['Australia', 'Canada', 'Chile', 'Germany', 'New Zealand','United Kingdom', 'United States']
top_destinations_df = all_emigrants_high_net_melt[all_emigrants_high_net_melt.country.isin(top_destinations)]
plot_immigration_flow(top_destinations_df)



## SECONDARY CHOICE COUNTRIES ##
second_choice_df = ['Denmark', 'Finland', 'Ireland',
        'Netherlands','Portugal', 'Sweden',
        'Switzerland']
plot_immigration_flow(all_emigrants_high_net_melt[~all_emigrants_high_net_melt.country.isin(top_destinations)])



row_migration_by_destination_melt.step.nunique()
row_migration_by_destination_melt[~row_migration_by_destination_melt.country.isin(['United States', 'Canada', 'United Kingdom'])]

