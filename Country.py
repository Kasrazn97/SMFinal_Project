
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
        self.num_of_immigrants = {k:0 for k in self.data.country}
        self.num_of_emmigrants = {k:0 for k in self.data.country}
        self.new_born = 0 
        self._name = country_name
        self.timestep = 0
        self.prob = list() # probability of being chosen as a distination
        self.benefits = 0
        self.destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']
        self.community_network = None

    # def grow_gdp(self): 
    #     self.data[(self.data['country'] == self._name)&(self.data['year'] == self.timestep)]['gdp'] *= 1.05
    
    # def increase_expEd(self): 
    #     self.data[(self.data['country'] == self._name)&(self.data['year'] == self.timestep)]['expEd'] += 5

    def keep_brains(self):
        self.benefits += 1
            
    # def grow_population(self):
    #     self.population += 2

    def get_data_diff(self):
        """
        Returns the differences of all indicators of a given country and of all others
        """

        self.data_diff = pd.DataFrame()
        # if (self.timestep == 3)&(self._name == 'Sweden'):
        #     self.keep_brains()
        #     print('Policies in place')
        data = self.data[self.data['year'] == self.timestep]
        for c in self.destinations:
        # for c in data.country.unique():
            df = pd.DataFrame(data[data['country'] == c].iloc[0,1:] - data[data['country'] == self._name].iloc[0,1:]).T
            self.data_diff = self.data_diff.append(df, ignore_index=True)
        self.data_diff['beta0'] = np.ones(len(self.data_diff))
        cols = self.data_diff.columns.tolist()
        cols = cols[-1:] + cols[:-2] # add beta0 as the first column
        self.data_diff = self.data_diff[cols]

    def set_country_probability(self): 
        """
        For a given country returns probabilities to go to other countries at step t
        """
        self.prob = []

# Intercept    1.679889e-02
# co2          1.159363e-07
# expRD        1.323871e-03
# expEd       -6.152302e-04
# expHealth   -5.340156e-04
# gdp         -1.130067e-14

        betas = np.array([1.679889e-02, -1.159363e-07, 1.323871e-03, 6.152302e-04, 5.340156e-04, 1.130067e-7]) # we will only define them here (they are set, unchangable values)
        denominator = 0
        for i in range(len(self.data_diff)):
            country_data_diff = self.data_diff.loc[i].to_numpy() # [1:len(betas)]
            denominator += np.exp(np.dot(betas,country_data_diff))
        for i in range(len(self.data_diff)):
            country_data_diff = self.data_diff.loc[i].to_numpy() # [1:len(betas)]
            # print(country_data_diff)
            p = np.exp(np.dot(betas, country_data_diff))/denominator # prob-s to go to other countries
            # p = 1/(1+np.exp(np.dot(betas,country_data_diff))) # prob-s to go to other countries
            # print(p)
            self.prob.append(p)

    def __repr__(self): 
        return f'{self._name}, number of immigrants: {self.num_of_immigrants}, number of emmigrants:{self.num_of_emmigrants}'
    
    def reporter(self): # num of emmigrants and immigrants should increase each step
        values = self.timestep, self._name, sum(self.num_of_immigrants.values()), sum(self.num_of_emmigrants.values()), self.population
        df = pd.DataFrame(values, index=None).T
        df.columns = ['step', 'country', 'num_of_immigrants', 'num_of_emmigrants', 'population']
        return df

    def step(self):
        """ 
        Update everything
        """
        self.get_data_diff()
        print(self._name, 'got diff')
        self.set_country_probability()
        # print(self.prob)
        self.timestep += 1
        # self.grow_population()
        self.new_born = 0


