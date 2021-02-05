import csv
import pandas as pd

df = pd.read_csv(
    r"C:\Program Files (x86)\Geobid\Osnowy\Punkty.txt",
    header=None,
    decimal=".",
    sep=",",
)
print(df)
print(df.dtypes)

# pd.to_numeric(df[7])

# print(df)
# print(df.dtypes)
df.to_csv(
    r"C:\Program Files (x86)\Geobid\Osnowy\Punktyexcel.txt",
    header=None,
    sep="\t",
    index=False,
    # quoting=csv.QUOTE_NONNUMERIC,
)
