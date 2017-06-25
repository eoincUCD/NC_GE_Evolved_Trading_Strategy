from fitness.base_ff_classes.base_ff import base_ff
import pandas as pd


class trading(base_ff):
    """
    derived from Py-max
    """
    maximise = True  # True as it ever was.

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()

        in_file = "../data/AAPL UW Equity.csv"
        df = pd.read_csv(in_file)
        self.data = df[['PX_OPEN','PX_HIGH','PX_LOW']]

        self.training = self.data[:-246]
        self.test = self.data
        self.n_vars = len(self.data)

        self.training_test = True
    
    def evaluate(self, ind, **kwargs):
        # ind.phenotype will be a string, including function definitions etc.
        # When we exec it, it will create a value XXX_output_XXX, but we exec
        # inside an empty dict for safety.

        dist = kwargs.get('dist', 'training')

        if dist == "training":
            # Set training datasets.
            data = self.training
            start = 246

        elif dist == "test":
            # Set test datasets.
            data = self.test
            start = len(self.test) - 246

        p, d = ind.phenotype, {}
        print(p)

        n_points = len(data)  # Number of data points available . . we have 17 years of data

        cash, shares = 10000, 0

        for i in range(start, n_points):

            d['PX_OPEN'] = list(data['PX_OPEN'][i-246:i])  # Only pass in one year worth of data
            d['PX_HIGH'] = list(data['PX_HIGH'][i-246:i])
            d['PX_LOW'] = list(data['PX_LOW'][i-246:i])
            d['n_points'] = len(d['PX_OPEN'])

            exec(p, d)

            last_price = data['PX_OPEN'][i]

            if d["XXX_output_XXX"] > 0:  # If > 0, buy as many shares as we can
                quantity = cash / last_price
                shares = shares + quantity
                cash = cash - quantity * last_price
            else:  # Sell all
                cash = cash + shares * last_price
                shares = 0

        # print(len(data), cash, shares)

        cash = cash + shares * last_price

        return cash


# --debug --grammar_file test.pybnf --verbose --fitness_function trading2 --generations 20 --population 20 --random_seed 517470
# add cache
# --target_seed_folder my_seeds