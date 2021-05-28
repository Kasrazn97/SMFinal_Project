from numpy.core.defchararray import array, index
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame

from Agent import *
from Country import *
from MigrationModel import *

# data = pd.read_csv('data/countries_data_1.csv', sep=';', nrows=31)
# data = data.drop(1)
# all_data = pd.DataFrame()
# for country in data.country.unique():
#     df = pd.DataFrame(np.tile(data[data.country == country], (30,1)))
#     all_data = all_data.append(df, ignore_index=True)
# all_data.columns = data.columns
# all_data['gdp'] = all_data['gdp'].apply(lambda x: np.log(x))
# all_data.to_csv('all_data.csv', header=True)
# data = pd.read_csv('all_data.csv').drop('Unnamed: 0', axis=1)

# INITIALIZE POPULATION
# countries_pop = {} # dictionary of countries and number of agents there
# for country in data.country.unique():
#     countries_pop[country] = data[data.country == country]['pop'].values[0]

def load_data(file_path):
    """
    Data should be in .csv format. [add any data transformations here]
    """
    data = pd.read_csv(file_path)
    if data.columns[0] == 'Unnamed: 0':
        data = data.drop('Unnamed: 0', axis=1)
    return data

data = load_data('all_data.csv')
        
model = MigrationModel(data)
model.run(5)
model.get_stats()
model.countries_report[model.countries_report['country'] == 'Italy']
model.agents_report.head(20)

len(model.agentlist)
model.agents_report.groupby('step').status.sum()
model.agents_report.groupby('agent').status.sum()
model.countries_report.groupby('step')['num_of_emmigrants'].sum()


pd.read_csv('/Users/aliyadavletshina/Desktop/Bocconi/modeling&simulation/final_project/SMFinal_Project/data/Country_probabilities.csv')
pd.read_csv('data/Education_index.csv')


# countries_dict = {}
# destinations = ['Austria', 'Germany']
# for country in data.country.unique():
#     c = Country(data[data['country'] == country]) # df is dataframe with all info about countries
#     countries_dict[country] = c


# destinations_names = [country for country in list(countries_dict.keys()) if country in destinations]
# destinations = {k: v for k,v in countries_dict.items() if k in destinations_names}
