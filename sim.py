from model import *


num_agents = N
countries_pop = {} # dictionary of countries and number of agents there  
        

# Create dictionary of countries
countriesdict = {}
for country in list(countries_pop.keys()):
    c = Country(df[df['country'] == country]) # df is dataframe with all info about countries
    countriesdict[country] = c

# Create list of agents
agentlist = []
for country in list(countries_pop.keys()):
    for agent in range(countries_pop[country].values()):
        a = Agent(self, country)
        agentlist.append(a)

epochs = 0

while epochs < 31:
    print(f'Step {epoch} has started')

    for a in agentlist:
        a.step()
