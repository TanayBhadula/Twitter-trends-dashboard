import pandas as pd
import glob

path = r'csv_files/' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

frame = pd.concat(li, axis=0, ignore_index=True)
#frame['country'] = frame['country'].fillna("Worldwide")

frame.to_csv("merged.csv", index=False)

# load the resultant csv file
 
# and view the data
 