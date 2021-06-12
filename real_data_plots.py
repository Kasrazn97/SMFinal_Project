import matplotlib.pyplot as plt
import numpy as np
from plots import *

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
row_migration_by_destination_melt = row_migration_by_destination.melt('country_to', var_name='year', value_name='num_of_immigrants')
row_migration_by_destination_melt = row_migration_by_destination_melt.rename({'country_to': 'country', 'year':'step'}, axis=1)
row_migration_by_destination_melt.step = row_migration_by_destination_melt.step.map({k:v for k, v in zip(row_migration_by_destination_melt.step.unique(), np.arange(1,32))})

plot_immigration_flow(row_migration_by_destination_melt)
row_migration_by_destination_melt.step.nunique()


