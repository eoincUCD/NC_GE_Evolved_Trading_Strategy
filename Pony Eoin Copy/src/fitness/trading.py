from fitness.base_ff_classes.base_ff import base_ff
import pandas as pd


class trading(base_ff):
    """
    derived from Py-max
    """
    
    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
    
    def evaluate(self, ind, **kwargs):
        # ind.phenotype will be a string, including function definitions etc.
        # When we exec it, it will create a value XXX_output_XXX, but we exec
        # inside an empty dict for safety.
        
        p, d = ind.phenotype, {}

        d["y"] = 1000.0
        maximise = True  # True as it ever was.


        # todo - loop over each day/year/number of days to be evaluated over (ideally test on every day we have data)
        # ie from 2001 to 2015 . . . test on 2016/17 for report
            # fill dictionary with last 12 months data
            # Exec the phenotype.
            # result is a buy/sell/hold order recommendation for that day
            # implement order for day in question
            # add to saved fitness function

        # sell any stocks at last day price
        exec(p, d)

        # Get the output
        s = d['XXX_output_XXX']  # this is the program's output: a number.
        
        return s
