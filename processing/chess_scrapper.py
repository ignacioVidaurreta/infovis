import altair as alt
from datetime import datetime
import pandas as pd
import re
import requests
_DATE_REGEX=r'(\d+\.\d+\.\d+)'
_NUM_REGEX = r'(\d+)'

def get_elo(pgn_data):
  white_data = pgn_data[4]
  is_white = False
  if username in white_data:
    is_white = True

  if is_white:
    resulting_elo = pgn_data[13]
  else:
    resulting_elo = pgn_data[14]

  return re.search(_NUM_REGEX, resulting_elo).group(1)

if __name__ == "__main__":
    # Get list of archives
    username="nach1to"
    elo_list = []
    dates = []
    acum = 1
    current_date = None

    # TODO: Tidy up using methods instead of spaghetti code
    archives = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives")
    for a_link in archives.json()["archives"]:
        archive = requests.get(a_link)
        games = archive.json()["games"]
        for game in games:
            if game["time_class"] != "blitz":
                continue # Skip any non-blitz game
            pgn_data = game["pgn"].split("\n")
            date = re.search(_DATE_REGEX, pgn_data[2]).group(1)
            print(f"Date: {date}")
            elo = int(get_elo(pgn_data))

            if current_date is not None and current_date == date:
                index = len(dates) - 1
                elo_list[index] = elo # Only use the latest elo
            else:
                elo_list.append(elo)
                dates.append(date)
                current_date = date
                print(f"ELO: {elo_list}")


# TODO: Separate Scraping from display
# Transform data into dataframe for Altair
df = pd.DataFrame(list(zip(dates, elo_list)), columns=["Date", "Elo"])

# We need a datetime object, not a string
df["Date"] = pd.to_datetime(df["Date"])

chart = alt.Chart(df).mark_line(point=True).encode(
    alt.X('Date', scale=alt.Scale(zero=False)),
    alt.Y('Elo', scale=alt.Scale(zero=False)),
    tooltip=["Elo", "Date"]
).properties(
    width=500,
    height=500,
    title="Elo over time"
)

# alt.renderers.enable('altair_viewer')
# chart.show()

chart.save("../html/blitz_elo.html")