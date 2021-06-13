
"""
This module loads data and initializes agents and countries.
"""
import pandas as pd
from Agent import *
from Country import *

class MigrationModel():

    np.random.RandomState(seed=0)

    def __init__(self, data, num_agents=30):   # input is a table with all info for countries, columns: 'country', '1', 'gdp', 'life_exp'...

        self.data = data
        self.countries_dict = {}
        self.agentlist = []
        self.num_agents = num_agents # in each country
        self.epoch = 0
        self.countries_report = pd.DataFrame(columns = ['step', 'country', 'num_of_immigrants', 'num_of_emmigrants', 'population'])
        self.agents_report = pd.DataFrame(columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])
        self.destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']

    def initialize_agents(self):
        k = 0
        for country in self.data.country.unique():
            for agent in range(self.num_agents):
                a = Agent(k*self.num_agents+agent, country, self.countries_dict)
                self.agentlist.append(a)
            k += 1
    
    def add_agents(self, country):
        
        a = Agent(self.agentlist[-1:][0].id+1, country, self.countries_dict)
        a.timestep = self.epoch
        self.agentlist.append(a)
        self.countries_dict[a.home_country].population += 1

        # print(f'Agent {a} is added')

    def initialize_countries(self):

        for country in self.data.country.unique():
            c = Country(self.data, self.num_agents, country) # self.data is dataframe with all info about countries
            self.countries_dict[country] = c

    def run(self, EPOCHS=30, policies = False, policy_start_year = 3, policy_countries = ['Sweden']):

        if policies == True:
            policy_matrix = np.ones(self.data.loc[:, 'co2':'gdp'].shape)

            # increase ExpEd
            policy_matrix[self.data[(self.data.country.isin(policy_countries))&(self.data.year > policy_start_year)].index, 2] = 2
            # increase ExpRd
            policy_matrix[self.data[(self.data.country.isin(policy_countries))&(self.data.year > policy_start_year)].index, 1] = 3
            # increase ExpHealth
            policy_matrix[self.data[(self.data.country.isin(policy_countries))&(self.data.year > policy_start_year)].index, 3] = 2
        
            self.data.loc[:, 'co2':'gdp'] = self.data.loc[:, 'co2':'gdp'] * policy_matrix
            print('Policies in place')

        self.initialize_countries()
        self.initialize_agents()

        while self.epoch <= EPOCHS:
            print(f'Step {self.epoch+1} has started. 13/06')
            print(f'number of agents at step {self.epoch}:', len(self.agentlist))

            for c in self.countries_dict.values():

                self.countries_report = self.countries_report.append(c.reporter(), ignore_index=True)
                c.step()
                if self.epoch == 0:
                    c.community_network = pd.DataFrame({k: 0 for k, v in self.countries_dict[c._name].num_of_immigrants.items()}, index=[0]).T
            
            for a in self.agentlist:
                a.step()
                if a.unmoved == False:
                    self.countries_dict[a.home_country].num_of_emmigrants[a.country._name] += 1
                    self.countries_dict[a.home_country].population -= 1
                    self.countries_dict[a.country._name].num_of_immigrants[a.home_country] += 1
                    self.countries_dict[a.country._name].population += 1
                self.agents_report = self.agents_report.append(a.reporter(), ignore_index=True)
                if a.unmoved == False:
                    self.agentlist.remove(a)
                if a.age > 30:
                    self.add_agents(a.country._name)
                    try:
                        self.agentlist.remove(a)
                    except ValueError:
                        continue
                    print(f'Agent {a} is added')

            for c in self.destinations: # collect community network strength info 
                df = pd.DataFrame({k: v/sum(self.countries_dict[c].num_of_immigrants.values()) for k, v in self.countries_dict[c].num_of_immigrants.items()}, index=[0]).T
                self.countries_dict[c].community_network = pd.concat([self.countries_dict[c].community_network, df], axis=1)
            
            if self.epoch == EPOCHS:
                for c in self.countries_dict.values():
                    self.countries_report = self.countries_report.append(c.reporter(), ignore_index=True)

            self.epoch +=1
        print("Simulation completed")

    def get_country_stats(self, country):
        df = self.countries_report[self.countries_report.country == country]
        return df
    

