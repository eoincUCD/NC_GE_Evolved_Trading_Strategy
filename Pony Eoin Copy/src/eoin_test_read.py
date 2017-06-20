import pandas as pd
import random
from math import floor

random.seed(12345)
in_file = "../../data/AAPL UW Equity.csv"
df = pd.read_csv(in_file)

# start at first data point in 2000
# We have 17.5 years worth of data and will ignore 2017 (the 0.5yr)
# Split data into 16 years with the 17th being a test case

d = {}
d["cash"] = 10000
d["shares"] = 0

for i in range(16):  # Loop 16 times - one for each year of data . . . roughly
    start = i * int((len(df) - 105) / 17)  # Start of that year . . . we have 17 years of data
    end = (i+1) * int((len(df) - 105) / 17)  # End of that year
    print(i, start, end)
    for j in range(start, end):  # Loop for each day in that year
        x = 0
        point = "point_" + str(x)
        for k in range(start, end):
            d[point] = df.iloc[start+j+x, 4]
            x +=1
        # print(j, ":", d)
        d["last_price"] = d[point]

        # todo exec on this point

        out = random.random()
        if out < 0.5:
            d["recommendation"] = "buy"
        else:
            d["recommendation"] = "sell"

        if d["recommendation"] == "buy":  # If buy, buy as many shares as we can
            quantity = floor(d["cash"]/d["last_price"])
            d["shares"] = d["shares"] + quantity
            d["cash"] = d["cash"] - quantity * d["last_price"]
        else:
            d["cash"] = d["cash"] + d["shares"] * d["last_price"]
            d["shares"] = 0

    d["cash"] = d["cash"] + d["shares"] * d["last_price"]
    d["shares"] = 0
    d["XXX_output_XXX"] = d["cash"]
    print(i, ": Final result, cash remaining after 10000:", d["XXX_output_XXX"])