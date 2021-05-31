
"""
This module defines the attributes and methods of a Country class. Some countries are only 'senders', 
some are both senders and receivers.
"""

import pandas as pd
import numpy as np

# from Agent import *

class Country():

    def __init__(self, data, num_agents, country_name): # input is a table with all info for a country, columns: 'country', '1', 'gdp', 'life_exp'...
        
        self.data = data
        self.data_diff = pd.DataFrame()
        self.population = num_agents
        self.num_of_immigrants = 0
        self.num_of_emmigrants = 0
        self._name = country_name
        self.timestep = 0
        self.prob = list() # probability of being chosen as a distination

        # policies to be defined 

    def improve_indicator(self, indicator): # this is stupid now , needs change 
        self.data[(self.data['country'] == self._name)*(self.data['year'] == self.timestep)]['indicator'] *= 1.001

    def attract_brains(self):
        self.average_income *= 1.1

    def keep_brains():
        self.benefits += 1
            
    def grow_population(self):
        self.population *= 1.05

    def get_data_diff(self):
        """
        Returns the differences of all indicators of a given country and of all others
        """
        self.data_diff = pd.DataFrame()
        data = self.data[self.data['year'] == self.timestep]
        for c in data.country.unique():
            df = pd.DataFrame(data[data['country'] == c].iloc[0,1:] - data[data['country'] == self._name].iloc[0,1:]).T
            self.data_diff = self.data_diff.append(df, ignore_index=True)
        self.data_diff['beta0'] = np.ones(len(self.data_diff))
        cols = self.data_diff.columns.tolist()
        cols = cols[-1:] + cols[:-2]
        self.data_diff = self.data_diff[cols]

    def set_country_probability(self): 
        """
        Returns probability for a country to be chosen as a destination at step t
        """
        self.prob = []
        betas = np.array([0.005, 0.0023, 0.019, 0.002, 0.002]) # we will only define them here (they are set, unchangable values)
        for i in range(len(self.data_diff)):
            country_data_diff = self.data_diff.loc[i].to_numpy() # [1:len(betas)]
            # print(country_data_diff)
            p = np.exp(np.dot(betas,country_data_diff))/(1+np.exp(np.dot(betas,country_data_diff)))
            # print(p)
            # print(self.prob)
            # print(self.prob.append(p))
            self.prob.append(p)

    def __repr__(self): 
        return f'{self._name}, number of immigrants: {self.num_of_immigrants}, number of emmigrants:{self.num_of_emmigrants}'
    
    def reporter(self): # num of emmigrants and immigrants should increase each step
        values = self.timestep, self._name, self.num_of_immigrants, self.num_of_emmigrants, self.population
        df = pd.DataFrame(values, index=None).T
        df.columns = ['step', 'country', 'num_of_immigrants', 'num_of_emmigrants', 'population']
        return df

    def step(self):
        """ 
        Update everything
        """
        # if self.name in [list of EU countruies here]:
        self.get_data_diff()
        print(self._name, 'got diff')
        self.set_country_probability()
        self.timestep += 1
        self.grow_population()


