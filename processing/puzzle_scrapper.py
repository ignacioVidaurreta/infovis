import os
from dotenv import load_dotenv
import requests
import berserk
import csv

load_dotenv() # load .env file

# load jwt token
TOKEN=os.getenv("LICHESS_OAUTH")

session = berserk.TokenSession(TOKEN)
client = berserk.Client(session=session)


puzzle_map = client.users.get_puzzle_activity()

with open("puzzles.csv", "w") as f:
    lines = []
    for puzzle in puzzle_map:
        p_id = puzzle["id"]
        date = puzzle["date"].strftime("%d/%m/%Y")
        win = puzzle["win"]
        puzzle_rating = puzzle["puzzleRating"]
        lines.append(f"{p_id},{date},{win},{puzzle_rating}\n")

    f.writelines(lines)

current_date = None
win_score = 0
lose_score = 0
lines = []
with open("puzzles.csv", "r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        if lines == []:
            header = "date,score,result\n"
            lines.append(header)
        else:
            p_id = row[0]
            date = row[1]
            win = row[2]
            if current_date is None:
                current_date = date
                if win:
                    win_score+=1
                else:
                    lose_score+=1
            elif current_date == date:
                if win == "True":
                    win_score+=1
                else:
                    lose_score+=1
            else:
                lines.append(f"{current_date},{win_score},solved\n")
                lines.append(f"{current_date},{lose_score},failed\n")
                current_date = date
                win_score = 0
                lose_score = 0
                if win:
                    win_score+=1
                else:
                    lose_score+=1

    #print(f'Processed {line_count} lines.')


with open("puzzles2.csv", "w") as csv_file:
    csv_file.writelines(lines)