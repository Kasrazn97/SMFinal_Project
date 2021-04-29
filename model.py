# from mesa import Model, Agent # dont use this 
# from mesa.time import RandomActivation
# from mesa.space import SingleGrid
# from mesa.datacollection import DataCollector

from mesa import Agent, Model

class Agent(Country):

    def __init__(self):

        super().__init__(pos, model)
        self.country = Country()
        p = np.random.random()
        if p > 0.5:
            
        self.gender
        self.income = self.random.random(self.avg_income, .. ) # should be inherented from the country class - # google std of wage 
        self.ambition = self.random.random() # function of age 
        self.happy = 
        
    def willingness_to_move(self):
        return np.exp(self.gender*0.2 + self.age + self.ambition - self.country.attachment + self.income) # change this 
    
    def decide_to_move(thresh):
        if self.willingness_to_move() > thresh:
            return True 

    def choose_country(self, countries):
        p = np.array()
        for i, country in enumerate(countries):
            c = Country(country)
            p[i] = c.gdp + ..
        p_scaled = p / p.sum()
        p_cumsum = p_scaled.cumsum()
        r = np.random.random()
        p_cumsum -= r
        return countries[np.argmax(p_cumsum > 0)-1]

    def step(self):
        similar = 0
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Country():
    """
    Model class for the Schelling segregation model.
    """
    def __init__(self, data): # need a table with all those cols 

        self.population = data['pop']
        self.average_income = data['avg_inc']
        self.hdi = data['hdi']
        self.life_exp = data['life_exp'] 
        self.attachment = data['attachment']
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            {"happy": "happy"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
        )

        # Set up agents
        # We use a grid iterator that returns
        # the coordinates of a cell as well as
        # its contents. (coord_iter)
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = SchellingAgent((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)



class MigrationModel():

    def __init__(self, N):
        self.num_agents = N
        # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self)

    def step(self):
        """
        Run one step of the model. If All agents are happy, halt the model.
        """
        self.steps += 1  # Reset counter of happy agents
        self.schedule.step()
        self.datacollector.collect(self)

        if self.happy == self.schedule.get_agent_count():
            self.running = False



    

