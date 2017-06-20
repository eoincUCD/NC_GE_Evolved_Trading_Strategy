import pandas as pd
import random
import time
from math import floor

random.seed(12345)
in_file = "../../data/AAPL UW Equity.csv"
df = pd.read_csv(in_file)

out_file_name = "../../logs/" + time.strftime("%Y%m%d-%H%M%S") + "_test_fitness.txt"  # Log file name
out_file = open(out_file_name, "w")  # Open log file

# start at first data point in 2000
# We have 17.5 years worth of data and will ignore 2017 (the 0.5yr)
# Split data into 17 years with the 17th being a test case

d = {}
d["points"] = int((len(df) - 105) / 17)  # Number of data points available per year . . . we have 17 years of data
d["cash"] = 10000
d["shares"] = 0

for i in range(15):  # Loop 15 times - one for each year of data . . . roughly
    start = i * d["points"]  # Start of that year
    end = (i+1) * d["points"]  # End of that year
    for j in range(start, end):  # Loop for each day in that year
        x = 0
        for k in range(start, end):
            point = "point_" + str(x)
            d[point] = df.iloc[j+x, 4]
            x = x + 1
        d["last_price"] = d[point]

        # todo exec on this point

        d["out"] = random.random()
        if d["out"] < 0.5:
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

        out_file.write(str(i) + " " + str(j) + " " + str(d) + "\n")

    d["cash"] = d["cash"] + d["shares"] * d["last_price"]
    d["shares"] = 0
    d["XXX_output_XXX"] = d["cash"]

out_file.write("Final result, cash remaining after 10000:" + str(d["XXX_output_XXX"]) + "\n")
print("Final result, cash remaining after 10000:", d["XXX_output_XXX"])
out_file.close()
