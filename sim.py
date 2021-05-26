import pandas as pd
import numpy as np

from Agent import *
from Country import *

# num_agents = N

data = pd.read_csv('data/countries_data.csv', sep=';', nrows=31)
data = data.drop(1)
all_data = pd.DataFrame()

for country in data.country.unique():
    df = pd.DataFrame(np.tile(data[data.country == country], (30,1)))
    all_data = all_data.append(df, ignore_index=True)
all_data.columns = data.columns

all_data.to_csv('all_data.csv', header=True)
data = pd.read_csv('all_data.csv').drop('Unnamed: 0', axis=1)

# INITIALIZE POPULATION
# countries_pop = {} # dictionary of countries and number of agents there
# for country in data.country.unique():
#     countries_pop[country] = data[data.country == country]['pop'].values[0]

# Create dictionary of countries
countries_dict = {}
for country in data.country.unique():
    c = Country(data[data['country'] == country]) # df is dataframe with all info about countries
    countries_dict[country] = c

# countries_dict['Australia'].data

# Create list of agents
agentlist = []
k = 0
for country in list(countries_dict.keys()):
    for agent in range(30):
        a = Agent(k*30+agent, country, countries_dict)
        agentlist.append(a)
    k += 1
agentlist[300:310]
epochs = 0

while epochs < 31:
    print(f'Step {epochs} has started')
    for a in agentlist:
        a.step()
    for c in countries_dict.values():
        c.step()
    epochs +=1

countries_dict['Austria'].timestep
countries_dict['Austria'].data.iloc[0].to_numpy()[1:5]

for c in list(countries_dict.keys()):
    print(countries_dict[c].name, countries_dict[c].num_of_emmigrants)

# collect data



