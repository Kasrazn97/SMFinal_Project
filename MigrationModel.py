
"""
This module loads data and initializes agents and countries.
"""
import pandas as pd
from Agent import *
from Country import *

class MigrationModel():

    def __init__(self, data, num_agents=30):   # input is a table with all info for countries, columns: 'country', '1', 'gdp', 'life_exp'...

        self.data = data
        self.countries_dict = {}
        self.agentlist = []
        self.num_agents = num_agents
        self.epoch = 0
        self.countries_report = pd.DataFrame(columns = ['step', 'country', 'num_of_immigrants', 'num_of_emmigrants', 'population'])
        self.agents_report = pd.DataFrame(columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])

    def create_agents(self):
        k = 0
        for country in self.data.country.unique():
            for agent in range(self.num_agents):
                a = Agent(k*self.num_agents+agent, country, self.countries_dict)
                self.agentlist.append(a)
            k += 1
    
    def create_countries(self):

        for country in self.data.country.unique():
            c = Country(self.data, self.num_agents, country) # self.data is dataframe with all info about countries
            self.countries_dict[country] = c

    def run(self, EPOCHS=30, policy=False):

        # if policy == True:
        #     policy_matrix = np.ones(self.data.shape)
        #     policy_matrix[data[(data.country == 'Italy')*(data.year > 3)]['gdp'].index, 1] = 1
        #     self.data = self.data * policy_matrix

        self.create_countries()
        self.create_agents()

        while self.epoch < EPOCHS:
            print(f'Step {self.epoch+1} has started')
            for c in self.countries_dict.values():
                c.step()
                self.countries_report = self.countries_report.append(c.reporter(), ignore_index=True)
            for a in self.agentlist:
                a.step()
                self.agents_report = self.agents_report.append(a.reporter(), ignore_index=True)
            self.epoch +=1
        print("Simulation completed")

    def get_stats(self):
        df = pd.DataFrame(columns=['country', 'immigrants', 'emmigrants'])
        for i, c in enumerate(list(self.countries_dict.keys())):
            df.loc[i] = [self.countries_dict[c]._name, self.countries_dict[c].num_of_immigrants, self.countries_dict[c].num_of_emmigrants]
        return df
