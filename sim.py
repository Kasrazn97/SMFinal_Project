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
model.run()
model.get_stats()
model.countries_report
model.agents_report.head()

model.countries_dict['']

model.countries_dict['Italy'].reporter()
agents_report = pd.DataFrame(['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])

df_test = pd.DataFrame(columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move'])
df_test.append(np.array(model.agentlist[0].reporter()).reshape(1,len(model.agentlist[0].reporter()))[0])
pd.concat(df_test, np.array(list(model.agentlist[0].reporter()))

np.array([3,4,5,]).reshape(1,3)
pf = model.agentlist[0].reporter()
pf.columns = ['step', 'agent', 'age', 'ambition', 'home_country', 'country', 'status', 'willingness_to_move']
df_test.append(pf)
countries_report
pd.concat([df_test, pd.DataFrame(model.agentlist[0].reporter()).T], axis=0, ignore_index=True)

vals = 4,5,6


pd.read_csv('/Users/aliyadavletshina/Desktop/Bocconi/modeling&simulation/final_project/SMFinal_Project/data/Country_probabilities.csv')
pd.read_csv('data/Education_index.csv')

# countries_dict = {}
# destinations = ['Austria', 'Germany']
# for country in data.country.unique():
#     c = Country(data[data['country'] == country]) # df is dataframe with all info about countries
#     countries_dict[country] = c


# destinations_names = [country for country in list(countries_dict.keys()) if country in destinations]
# destinations = {k: v for k,v in countries_dict.items() if k in destinations_names}
