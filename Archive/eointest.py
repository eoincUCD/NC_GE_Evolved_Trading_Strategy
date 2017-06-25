import pandas as pd

in_file = "../data/AAPL UW Equity.csv"
df = pd.read_csv(in_file)

for i in [246,247,248]:
    PX_OPEN = list(df['PX_OPEN'][i - 246:i])
    print(PX_OPEN)