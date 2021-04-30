# from mesa import Model, Agent # dont use this 
# from mesa.time import RandomActivation
# from mesa.space import SingleGrid
# from mesa.datacollection import DataCollector

from mesa import Agent, Model
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Agent(Country):

    def __init__(self):

        super().__init__(pos, model)
        self.country = Country()
        p = np.random.random()
        if p > 0.5:
            self.gender = 0 # female
        else:
            self.gender = 1 # male
        self.income = np.random.random(self.country.avg_income, self.country.avg_income*0.1) # should be inherented from the country class - # google std of wage 
        self.happy =
        a = np.random.gamma(2,2,self.num_agents)
        self.age = np.floor(a*45/max(a)+25)
        self.ambition = 1/self.age # function of age 

    def willingness_to_move(self):
        return np.exp(self.gender*0.2 - self.age + self.ambition) / (np.exp(self.gender*0.2 - self.age + self.ambition)+1) # - self.country.attachment + self.income) # change this 
    
    def decide_to_move(thresh=0.3):
        if self.willingness_to_move() > thresh:
            return True

    def choose_country(self, countries_dict):
        p = np.array()
        for i, c in enumerate(countries_dict.values()):
            p[i] = c.gdp + ..
        p_scaled = p / p.sum()
        p_cumsum = p_scaled.cumsum()
        r = np.random.random()
        p_cumsum -= r
        return list(countries_dict.keys())[np.argmax(p_cumsum > 0)-1]

    def update_income(self):
        self.income = np.random.random(self.country.avg_income, self.country.avg_income*0.1)

    def step(self):

        if self.decide_to_move():
            self.country = countries_dict[self.choose_country()]
            self.update_income()
        self.age += 1


class Country():
    """
    Model class for the Schelling segregation model.
    """
    def __init__(self, data): # need a table with all those cols 

        self.population = data['pop']
        self.average_income = data['avg_inc']
        self.hdi = data['hdi']
        self.life_exp = data['life_exp']

        # policies to be defined 

        def attract_brains():
            self.average_income *= 1.1
        
        def keep_brains():
            

class MigrationModel():

    def __init__(self, N):

        self.num_agents = N
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = Agent(self)

        # Create countries
        for i in range(len(countries_dict)):
            c = Country(df)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.steps += 1 
        self.


# SAVE AND COMMIT 

    

