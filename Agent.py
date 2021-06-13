
"""
This module defines the attributes and methods of an Agent class. Agents are highly-skilled people
who decide to move or to stay in the home country based on their ambition. 
"""

import numpy as np
import pandas as pd

class Agent():

    np.random.RandomState(seed=0)

    def __init__(self, id, home_country, countries_dict): # home_country STRING, countries_dict DICT

        self.id = id
        self.home_country = home_country
        self.countries_dict = countries_dict
        self.country = self.countries_dict[self.home_country]
        p = np.random.random()
        if p > 0.5:
            self.gender = 0 # female
        else:
            self.gender = 1 # male
        self.age = int(np.random.uniform(0,30,1))
        self.ambition = np.random.random() # declines with age
        self.unmoved = True
        self.timestep = 0

    def willingness_to_move(self):
        alpha0, alpha1, alpha2 = 1, 0.01, 1
        if self.age <= 30:
            return alpha0*self.ambition + alpha1**self.gender*self.ambition - alpha2*self.ambition*self.age/30
        else:
            return 0
        # TODO: calibrate coefficients 
    
    def decide_to_move(self, thresh=0.2):
        p = np.random.random()
        # print(self.willingness_to_move())
        if self.willingness_to_move() > p:
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
        NAcoef = 0.1
        BenefitCoef = 0.2

        p = np.array(self.country.prob)
        network_abroad = []
        benefits = []

        if self.timestep > 0:
            for c in destinations: # compute the share of immigrants from my country as a share of all immigrants in the destination country 
                benefits.append(self.countries_dict[c].benefits) # store benefits of each country
                if sum(self.countries_dict[c].num_of_immigrants.values()) != 0:
                    network_abroad.append(self.countries_dict[c].num_of_immigrants[self.country._name]/sum(self.countries_dict[c].num_of_immigrants.values()))
                else:
                    network_abroad.append(0)
            print('network abroad', network_abroad)
        else:
            network_abroad = np.zeros(len(p))
            benefits = np.zeros(len(p))

        p = p + NAcoef*np.array(network_abroad) + BenefitCoef*np.array(benefits)
        p_scaled = p / p.sum()
        p_cumsum = p_scaled.cumsum()
        r = np.random.uniform(0,1,1)
        country_id = np.argmax((p_cumsum - r) > 0)
        if country_id == -1:
            country_id = 0
        return destinations[country_id]
        
    # def update_income(self):
    #     self.income = np.random.normal(self.country.average_income, self.country.average_income*0.2)

    def __repr__(self): 
        """ Print info about agent """
        gender = self.gender*'male'+(1-self.gender)*'female'
        return f'Agent {self.id}, {gender}, {self.age} years old, from {self.home_country}.'

    def reporter(self):
        values = [self.timestep, self.id, self.age, self.ambition, self.home_country, self.country._name, self.unmoved, self.willingness_to_move()]
        df = pd.DataFrame(columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])
        df.loc[0] = values
        return df

    def step(self):
        if self.unmoved:
            if self.decide_to_move():
                chosen_country = self.choose_country()
                if self.country._name != chosen_country:
                    self.country.num_of_emmigrants[self.country._name] += 1 # increase num of emmigrants in home country to a certain country
                    self.country.population -= 1
                    self.country = self.countries_dict[chosen_country] 
                    self.country.num_of_immigrants[chosen_country] += 1 # increase num of immigrants in destination country
                    self.country.population += 1
                    self.unmoved = False
        self.age += 1
        self.timestep += 1
        if self.age > 30:
            self.country.new_born += 1



########--------------- if we decide to add network ---------------##########
# probability for an edge to exist
# p = 0.5

# ASSUMPTION: This array contains all desired nodes
# nodes = [...]

# g = nx.Graph()
# g.add_nodes_from(nodes)

# for u, v in combinations(g, 2):
#     if random.random() < p:
#         g.add_edge(u, v)

# SAVE AND COMMIT 

    


