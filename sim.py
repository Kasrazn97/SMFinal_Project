import pandas as pd

from model import *
# num_agents = N

data = pd.read_excel('countries_data.xlsx')

countries_pop = {} # dictionary of countries and number of agents there  
for country in data.country:
    countries_pop[country] = data[data.country == country]['pop'].values[0]

# Create dictionary of countries
countries_dict = {}
for country in list(countries_pop.keys()):
    c = Country(data[data['country'] == country]) # df is dataframe with all info about countries
    countries_dict[country] = c

countries_dict['Australia'].population

# Create list of agents
agentlist = []
for country in list(countries_pop.keys()):
    for agent in range(countries_pop[country]):
        a = Agent(country, countries_dict)
        agentlist.append(a)

epochs = 0

while epochs < 31:
    print(f'Step {epochs} has started')

    for a in agentlist:
        a.step()
    epochs +=1

# countries_dict['Austria'].name

for c in list(countries_dict.keys()):
    print(countries_dict[c].name, countries_dict[c].num_of_emmigrants)

# collect data



