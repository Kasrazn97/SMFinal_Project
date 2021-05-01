import pandas as pd

from model import *
# num_agents = N

data = pd.read_excel('countries_data.xlsx')
data.head()

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
        a = Agent(home_country=country, countries_dict=countries_dict)
        agentlist.append(a)

epochs = 0

while epochs < 31:
    print(f'Step {epoch} has started')

    for a in agentlist:
        a.step()
