import pandas as pd
import numpy as np

class Country():

    def __init__(self, data): # input is a table with all info for a country, columns: 'country', '1', 'gdp', 'life_exp'...

        self.data = data
        # self.population = data['pop'].values
        self.average_income = data['gdp'].values
        # self.life_exp = data['life_exp'].values
        # self.hdi = data['HDI'].values
        # self.employment = data['employment'].values
        self.num_of_immigrants = 0
        self.num_of_emmigrants = 0
        self._name = data['country'].values[0]
        self.timestep = 0
        self.prob = 0 # probability of being chosen as a distination

        # policies to be defined 

    def attract_brains(self):
        self.average_income *= 1.1
        # def keep_brains():
            
    def grow_population(self):
        self.population *= 1.0005
    
    def set_country_probability(self):
        """
        Returns probability for a country to be chosen as a destination at step t
        """
        betas = np.array([0.005, 0.0023, 0.019, 0.002]) # we will only define them here (they are set, unchangable values)
        country_data = self.data.iloc[self.timestep].to_numpy()[1:5] # starting from 2nd column get a data array for a particular year 
        p = np.exp(np.dot(betas,country_data))/(1+np.exp(np.dot(betas,country_data)))
        # print(p)
        return p

    def __repr__(self): # print info about agent
        return f'{self._name}, number of immigrants: {self.num_of_immigrants}, number of emmigrants:{self.num_of_emmigrants}'
    
    def reporter(self):
        values = self.timestep, self._name, self.num_of_immigrants, self.num_of_emmigrants
        df = pd.DataFrame(values, index=None).T
        df.columns = ['step', 'country', 'num_of_immigrants', 'num_of_emmigrants']
        return df

    def step(self):
        """ 
        Update everything
        """
        # if self.name in [list of EU countruies here]:
        self.prob = self.set_country_probability()
        self.timestep += 1


