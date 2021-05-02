# from mesa import Model, Agent # dont use this 
# from mesa.time import RandomActivation
# from mesa.space import SingleGrid
# from mesa.datacollection import DataCollector

# from mesa import Agent, Model
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

class Agent():

    def __init__(self, home_country, countries_dict):

        self.countries_dict = countries_dict
        self.country = countries_dict[home_country]
        p = np.random.random()
        if p > 0.5:
            self.gender = 0 # female
        else:
            self.gender = 1 # male
        self.income = np.random.normal(self.country.average_income, self.country.average_income*0.1) # should be inherented from the country class - # google std of wage 
        # self.happy = 
        a = np.random.gamma(2,2,348) # change this 
        self.age = np.random.choice(np.floor(a*45/max(a)+25))
        self.ambition = np.random.normal() # declines with age
        self.unmoved = True # has the agent already moved or not? 

    def willingness_to_move(self):
        return self.gender*self.ambition - self.ambition*self.age/75 + self.ambition 
    
    def decide_to_move(self, thresh=0.3):
        if self.willingness_to_move() > 0:
            return True
        else:
            return False

    def choose_country(self):
        p = np.zeros(len(self.countries_dict))
        for i, c in enumerate(self.countries_dict.values()):
            p[i] = np.random.random() # change this
        p_scaled = p / p.sum()
        p_cumsum = p_scaled.cumsum()
        r = np.random.random()
        p_cumsum -= r
        return list(self.countries_dict.keys())[np.argmax(p_cumsum > 0)-1]

    def update_income(self):
        self.income = np.random.random(self.country.average_income, self.country.average_income*0.2)

    def step(self):
        if self.unmoved:
            if self.decide_to_move():
                self.country.num_of_emmigrants += 1 # increase num of emmigrants in home country
                self.country.population -= 1 # decrease population in home country
                self.country = self.countries_dict[self.choose_country()] 
                self.update_income()
                self.country.population += 1 # increase population in destination country
                self.country.num_of_immigrants += 1 # increase num of immigrants in destination country
                self.unmoved = False
        self.age += 1

class Country():

    def __init__(self, data): # input is a table with all those columns

        self.population = data['pop'].values[0]
        self.average_income = data['avg_inc'].values[0]
        # self.hdi = data['hdi']
        self.life_exp = data['life_exp'].values[0]
        self.gdp = data['gdp'].values[0]
        self.num_of_immigrants = 0
        self.num_of_emmigrants = 0
        self.name = data['country'].values[0]

        # policies to be defined 

        def attract_brains():
            self.average_income *= 1.1
        
        # def keep_brains():
            



# SAVE AND COMMIT 

    

