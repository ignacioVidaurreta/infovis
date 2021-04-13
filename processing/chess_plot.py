import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

df = pd.read_csv("puzzles2.csv")

# Translate strings to datetime
df.loc[:, 'date'] = pd.to_datetime(df.loc[:, 'date'], format="%d/%m/%Y")

# We want to make "Failed" puzzles as negative score to display
df.loc[(df.result == "failed"), "score"] = - df.loc[(df.result == "failed"), "score"]
chart = alt.Chart(df).mark_bar().encode(
    x='date',
    y='score',
    color=alt.Color('result', scale=alt.Scale(domain=["solved", "failed"], range=["#06d6a0", "#ef476f"])),
    tooltip = [
      alt.Tooltip('date'),
      alt.Tooltip('result'),
      alt.Tooltip('score'),
    ]
).properties(
    width=1000,
    height=500,
    title="Puzzles Solved"
).interactive()

# We calculate the solved-failed difference to get a quick
# glance on performance
solved = list(df.loc[(df.result == "solved"), "score"])
failed = list(df.loc[(df.result == "failed"), "score"])

diff = [x - abs(y) for x,y in zip(solved, failed)]
d = {"date": list(df.loc[:, "date"].unique()), "diff": diff}
new_df = pd.DataFrame(data=d)
#new_df.plot(x="date")
diff_chart = alt.Chart(new_df).mark_circle(size=40).encode(
    x = "date",
    y = "diff",
    color = alt.value("black"),
    tooltip = [
      alt.Tooltip('date'),
      alt.Tooltip('diff'),
    ]
).interactive()

final_chart = chart + diff_chart

final_chart.save(f"../html/puzzle_score.html", embed_options={'renderer':'svg'})