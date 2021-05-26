from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

from mesa.batchrunner import BatchRunner

import random
import numpy as np
import sys
import matplotlib.pyplot as plt
# %matplotlib inline
# %config InlineBackend.figure_format = 'svg'
plt.rcParams.update({'font.size': 9, 'font.style': 'normal', 'font.family':'serif'})

def compute_S(model):
    return  sum([1 for a in model.schedule.agents if a.health == 'Susceptible'])

def compute_I(model):
    return  sum([1 for a in model.schedule.agents if a.health == 'Infected'])

def compute_R(model):
    return  sum([1 for a in model.schedule.agents if a.health == 'Recovered'])


class SIR_Agent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

        if random.random() < 0.05:
            self.health = 'Infected'
        else:
            self.health = 'Susceptible'

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def try_to_infect_neighbors(self):
        neighbors_nodes = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True)
        susceptible_neighbors = [a for n in neighbors_nodes for a in self.model.grid.get_cell_list_contents(n.pos) if
                                 a.health == 'Susceptible']

        for a in susceptible_neighbors:
            if self.random.random() < self.model.beta:
                a.health = 'Infected'

    def try_to_recovery(self):
        if random.random() < 1 / (self.model.gamma):
            self.health = 'Recovered'

    def step(self):
        self.move()
        if self.health == 'Infected':
            self.try_to_infect_neighbors()
            self.try_to_recovery()


class SIR_Model(Model):
    """SIR MODEL: """

    def __init__(self, N, width, height, beta, gamma):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.beta = beta
        self.gamma = gamma
        self.running = True

        # Create agents
        for i in range(self.num_agents):
            a = SIR_Agent(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Infected": compute_I,
                             "Susceptibles": compute_S,
                             "Recovered": compute_R})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        self.tot_infected = compute_I(self)  # <--- if there are no more infected, we want to stop the simulation
        if self.tot_infected == 0:
            self.running = True

model = SIR_Model(100, 10, 10, 0.04, 7)

while model.schedule.steps < 60:
    model.step()

RES = model.datacollector.get_model_vars_dataframe()
print('Simulation is over!')