"""*********************************************************************************************************************
Project Title: Evolving Short-Term Trading Strategies with Machine Learning
************************************************************************************************************************
UCD Assignment Details:
Date Started: 12/06/17
Revision 0
Date Submitted:
Student Name (Student Number): Eoin Carroll (16202781)
Module Code: UCD MIS40980
Module Title: Natural Computing & Applications
Assessment Title: Natural Computing Project
Module Co-ordinator: Michael O'Neill
************************************************************************************************************************
Instructions:
1.  Copy this python file into a folder
2.  Insure the folder includes sub folders - data and logs
3.  Data folder should either contain the raw data from Bloomberg or processed equities csv files
************************************************************************************************************************
Functions included:
************************************************************************************************************************
Github:
The project was made available on Github with the following URL.
The datafile is too large to store on Github, will share via another service. Contact Eoin for details
https://github.com/eoincUCD/NC-Nueral-Network-Trading-Strategy
************************************************************************************************************************
References:
************************************************************************************************************************
Dataset:
The dataset includes the following details for every S&P 500 component on each trading day from 05/2000 to 05/2017:
• Price to earnings ratio – Actual, Predicted
• Year on year growth
• Open, High, Low, Close prices
• Number of shares, number of trades
• Analysist recommendations buy, hold, sell
*********************************************************************************************************************"""


"""*********************************************************************************************************************
Import libraries
*********************************************************************************************************************"""


import pandas as pd
import numpy as np
import time
import datetime
import random


def generate_csv():  # Save each equity in it's own csv file
    in_file = "data/data.xlsx"
    print("Generating CSVs - this will take sometime.")
    startTime = time.time()
    out_file_name = "logs/" + time.strftime("%Y%m%d-%H%M%S") + "_generate_CSV" + ".txt"  # Log file name
    out_file = open(out_file_name, "w")
    out_file.write("Date and time: " + str(datetime.datetime.now()) + "\n")

    # Rename equities with / in the name in data excel file
    df = pd.read_excel(in_file, header=None)

    # for loop - number columns / 13
    for i in range(500):
        equity = df.iloc[0][i*14]
        out_file.write("Equity saved to CSV: " + equity + "\n")
        df_equity = df.loc[1:, i*14:i*14+12]
        df_equity.to_csv("data/" + equity + ".csv", index=False, header=False)  # export file
        print(equity)

    # Save list of equities

    out_file.write("Time taken to generate: " + str(time.time() - startTime))  # Log time taken
    out_file.close()


if __name__ == "__main__":  # Run program
    # generate_csv()
    print("Complete")