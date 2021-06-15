
"""
This module defines the attributes and methods of an Agent class. Agents are highly-skilled people
who decide to move or to stay in the home country based on their ambition. 
"""

import numpy as np
import pandas as pd

class Agent():

    def __init__(self, id, home_country, countries_dict): # home_country STRING, countries_dict DICT

        self.id = id
        self.home_country = home_country
        self.countries_dict = countries_dict
        self.country = self.countries_dict[self.home_country]
        p = np.random.random()
        if p < 0.5:
            self.gender = 0 # female
        else:
            self.gender = 1 # male
        self.age = int(np.random.uniform(0,30,1))
        self.ambition = np.random.random() 
        self.unmoved = True
        self.timestep = 0

    def willingness_to_move(self):
        alpha1, alpha2, alpha3 = 0.01, 0.5, 0.02
        if self.age <= 30:
            return self.ambition + alpha1**self.gender*self.ambition - alpha2*self.ambition*self.age/30 - alpha3*self.countries_dict[self.home_country].restrictions
        else:
            return 0
    
    def decide_to_move(self, thresh=0.2): 
        if self.willingness_to_move() > thresh:
            return True
        else:
            return False

    def choose_country(self):
        """
        Returns a chosen country among destination countries 
        """
        destinations = ['Australia', 'Austria', 'Canada', 'Chile', 'Denmark', 'Finland',
        'France', 'Germany', 'Greece', 'Ireland', 'Luxembourg',
        'Netherlands', 'New Zealand', 'Norway', 'Portugal', 'Sweden',
        'Switzerland', 'United Kingdom', 'United States']
        NAcoef = 10

        p = np.array(self.country.prob)
        network_abroad = []

        if self.timestep > 0:
            for c in destinations: # compute the share of immigrants from my country as a share of all immigrants in the destination country 
                if sum(self.countries_dict[c].num_of_immigrants.values()) > 0:
                    network_abroad.append(self.countries_dict[c].num_of_immigrants[self.country._name]/sum(self.countries_dict[c].num_of_immigrants.values()))
                else:
                    network_abroad.append(0)
            print('network abroad', network_abroad)
        else:
            network_abroad = np.zeros(len(p))

        p = p + NAcoef*np.array(network_abroad)
        p_scaled = p / p.sum()
        p_cumsum = p_scaled.cumsum()
        r = np.random.uniform(0,1,1)
        country_id = np.argmax((p_cumsum - r) > 0)
        if country_id == -1:
            country_id = 0
        return destinations[country_id]
        
    def __repr__(self): 
        """ Print info about agent """
        gender = self.gender*'male'+(1-self.gender)*'female'
        return f'Agent {self.id}, {gender}, {self.age} years old, from {self.home_country}.'

    def reporter(self):
        """
        Collects data about an agent at each step
        """
        values = [self.timestep, self.id, self.age, self.ambition, self.home_country, self.country._name, self.unmoved, self.willingness_to_move()]
        df = pd.DataFrame(columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])
        df.loc[0] = values
        return df

    def step(self):
        if self.unmoved:
            if self.decide_to_move():
                chosen_country = self.choose_country()
                if self.country._name != chosen_country:
                    self.country = self.countries_dict[chosen_country] 
                    self.unmoved = False
        self.age += 1
        self.timestep += 1

    


