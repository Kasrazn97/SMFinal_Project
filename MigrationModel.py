"""
This module loads data and initializes agents and countries.
"""

from Agent import *
from Country import *

class MigrationModel():

    def __init__(self):


    self.datacollector = DataCollector(model_reporters={"County Population": lambda m1: list(m1.county_population_list),
                                                        "County Influx": lambda m2: list(m2.county_flux),
                                                        "Deaths": lambda m3: m3.deaths,
                                                        "Births": lambda m4: m4.births,
                                                        "Total Population": lambda m5: m5.num_agents})
