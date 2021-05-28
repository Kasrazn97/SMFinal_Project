
# create class to collect stats - data collector 

class Statistics(object):
    """
    The statistics class is just a bundle of functions together without a permanent instance of data.
    Thus, every time it is called Statistics() it is initiated anew.
    The functions include average price of the firms, regional GDP - based on FIRMS' revenues, GDP per
    capita, unemployment, families' wealth, GINI, regional GINI and commuting information.
    """
    def __init__(self):

    def calculate_average_workers(self, firms):
        dummy_avg_workers = np.sum([firms[firm].num_employees for firm in firms.keys()])
        return dummy_avg_workers / len(firms)

    # Calculate wealth: families, firms and profits
    def calculate_families_median_wealth(self, families):
        return np.median([family.sum_balance() for family in families])
