"""
This module loads data and initializes agents and countries.
"""
import pandas as pd
import numpy as np

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
            c = Country(self.data, self.num_agents) # self.data is dataframe with all info about countries
            self.countries_dict[country] = c

    def run(self, EPOCHS=30):

        self.create_countries()
        self.create_agents()

        while self.epoch < EPOCHS:
            print(f'Step {self.epoch+1} has started')
            for c in self.countries_dict.values():
                c.step()
                # print(c.reporter())
                self.countries_report = self.countries_report.append(c.reporter(), ignore_index=True)
            for a in self.agentlist:
                a.step(self.countries_dict)
                # print(a.reporter())
                self.agents_report = self.agents_report.append(a.reporter(), ignore_index=True)
            self.epoch +=1
        print("Simulation completed")

    def get_stats(self):
        df = pd.DataFrame(columns=['country', 'immigrants', 'emmigrants'])
        for i, c in enumerate(list(self.countries_dict.keys())):
            df.loc[i] = [self.countries_dict[c]._name, self.countries_dict[c].num_of_immigrants, self.countries_dict[c].num_of_emmigrants]
        return df
            # print(self.countries_dict[c]._name, self.countries_dict[c].num_of_immigrants)



    # self.datacollector = DataCollector(model_reporters={"County Population": lambda m1: list(m1.county_population_list),
    #                                                     "County Influx": lambda m2: list(m2.county_flux),
    #                                                     "Deaths": lambda m3: m3.deaths,
    #                                                     "Births": lambda m4: m4.births,
    #                                                     "Total Population": lambda m5: m5.num_agents})
