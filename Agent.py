# from mesa import Model, Agent # dont use this 
# from mesa.datacollection import DataCollector
import numpy as np
import pandas as pd

# from mesa.time import RandomActivation
# from mesa.space import SingleGrid
# from mesa import Agent, Model
# from networkx import nx
# import matplotlib.pyplot as plt
# import seaborn as sns
# from itertools import combinations # for the network

class Agent():

    def __init__(self, id, home_country, countries_dict): # home_country STRING, countries_dict DICT

        self.id = id
        self.home_country = home_country
        # self.countries_dict = countries_dict
        self.country = countries_dict[self.home_country]
        p = np.random.random()
        if p > 0.5:
            self.gender = 0 # female
        else:
            self.gender = 1 # male
        self.income = np.random.normal(self.country.average_income, self.country.average_income*0.2) # should be inherented from the country class - # google std of wage 
        # a = np.random.gamma(2,2,348) # change this 
        # self.age = np.random.choice(np.floor(a*45/max(a)+25))
        self.age = int(np.random.uniform(0,30,1))
        self.ambition = np.random.random() # declines with age
        self.unmoved = True
        self.timestep = 0

    def willingness_to_move(self):
        return self.ambition + 0.1*self.gender*self.ambition - self.ambition*self.age/30 # TOADD: self.country.emmigrants/self.country.population
        # TODO: calibrate coefficients 
    
    def decide_to_move(self, thresh=0.3):
        if self.willingness_to_move() > thresh:
            return True
        else:
            return False

    def choose_country(self, countries_dict):
        """
        Returns a chosen country among EU countries
        """
        # destinations = [country for country in list(countries_dict.keys() if c in [list of destinations here])
        # destinations_dict = {k: v for k,v in countries_dict.items() if k in destinations}
        countries = list(countries_dict.keys())
        p = np.zeros(len(countries_dict))
        for i, c in enumerate(countries_dict.values()):
            p[i] = c.prob
        # print( [(k,v) for k,v in zip(countries_dict.keys(), p)], p.sum())
        p_scaled = p / p.sum()
        p_cumsum = p_scaled.cumsum()
        r = np.random.uniform(0,1,1)
        # print(r)
        # print(p_cumsum - r)
        # print(np.argmax((p_cumsum - r) > 0)-1)
        country_id = np.argmax((p_cumsum - r) > 0)
        if country_id == -1:
            country_id = 0
        # print(country_id)
        return countries[country_id]
        
    def update_income(self):
        self.income = np.random.normal(self.country.average_income, self.country.average_income*0.2)

    def __repr__(self): 
        """ Print info about agent """
        gender = self.gender*'male'+(1-self.gender)*'female'
        return f'Agent {self.id}, {gender}, {self.age} years old, from {self.home_country}.'

    def reporter(self):
        values = [self.timestep, self.id, self.age, self.ambition, self.home_country, self.country._name, self.unmoved, self.willingness_to_move()]
        df = pd.DataFrame(columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])
        df.loc[0] = values
        return df

    def step(self, countries_dict):
        if self.unmoved:
            if self.decide_to_move():
                self.country.num_of_emmigrants += 1 # increase num of emmigrants in home country
                # self.country.population -= 1 # decrease population in home country
                self.country = countries_dict[self.choose_country(countries_dict)] 
                self.update_income()
                # self.country.population += 1 # increase population in destination country
                self.country.num_of_immigrants += 1 # increase num of immigrants in destination country
                self.unmoved = False
        self.age += 1
        self.timestep += 1



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

    


