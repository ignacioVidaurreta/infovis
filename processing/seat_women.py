import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

COLS = 7
ROWS = 4

df = pd.read_csv("../datasets/seats_held_woman_eu.csv")

years = df.columns.values.tolist()[1:]

# Replace the awful long names. Hardcoded and awful i'm sorry
df["location"][0] = "EU 2020-"
df["location"][1] = "EU 2013-2020"

# We need to do some preprocessing to remove NaN values
df = df.dropna()
# We sort them for an easier view
df = df.sort_values(by=years, ascending=False)
df.reset_index(drop=True)

fig, axes = plt.subplots(nrows=ROWS, ncols=COLS)
fig.set_size_inches(30, 20)
# plt.rcParams['axes.titlepad'] = -14

total_countr = len(df)

current_row = 0
for i in range(total_countr):
  frame = df.iloc[i, :]

  title = frame.values[0]
  women = frame.values[1:]
  men = [ 1-x for x in women ]

  d = {'year': years, 'women': women, 'men': men}
  custom_df = pd.DataFrame(data=d)
  if i != 0 and i % COLS == 0:
    current_row+=1
  axis = axes[current_row][i % COLS]
  custom_df.plot.area(x='year', ax=axis)
  axis.set_title(title, y=0.7, fontsize=20, color="white")
  if i != 0:
    axis.get_legend().remove() # Only keep first legend

fig.savefig("../media/seats_held_women_eu.png")