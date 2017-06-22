from fitness.base_ff_classes.base_ff import base_ff
import pandas as pd
import random  # todo delete random
from math import floor

class trading2(base_ff):
    """
    derived from Py-max
    """
    maximise = True  # True as it ever was.

    global df_global
    in_file = "../../data/AAPL UW Equity.csv"
    df_global = pd.read_csv(in_file)

    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
    
    def evaluate(self, ind, **kwargs):
        # ind.phenotype will be a string, including function definitions etc.
        # When we exec it, it will create a value XXX_output_XXX, but we exec
        # inside an empty dict for safety.
        random.seed(12345)

        p, d = ind.phenotype, {}

        d["points"] = int((len(df_global) - 105) / 17)  # Number of data points available per year . . we have 17 years of data
        d["cash"] = 10000
        d["shares"] = 0

        for i in range(1):  # Loop 15 times - one for each year of data . . . roughly
            start = i * d["points"]  # Start of that year
            end = (i + 1) * d["points"]  # End of that year
            for j in range(start, end):  # Loop for each day in that year
                x = 0
                for k in range(start, end):
                    point = "point_" + str(x)
                    d[point] = df_global.iloc[j + x, 4]
                    x = x + 1
                d["last_price"] = d[point]

                # todo exec on this point
                exec(p, d)

                if d["XXX_output_XXX"] > 0:  # If > 0, buy as many shares as we can
                    quantity = floor(d["cash"] / d["last_price"])
                    d["shares"] = d["shares"] + quantity
                    d["cash"] = d["cash"] - quantity * d["last_price"]
                else:  # Sell all
                    d["cash"] = d["cash"] + d["shares"] * d["last_price"]
                    d["shares"] = 0
            d["cash"] = d["cash"] + d["shares"] * d["last_price"]
            d["shares"] = 0

        # Get the output
        s = d["cash"]  # this is the program's output: cash after trading.
        print(d["cash"])
        
        return s
