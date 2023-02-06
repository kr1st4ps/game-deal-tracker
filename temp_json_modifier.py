import json
import sys

with open("/Users/kristapsalmanis/projects/kr1st4ps.github.io/Data/games.json", "r") as file:
    games = json.load(file)

console_games = games["PS4"]
for item in console_games:
    item["base price"] = None

with open("/Users/kristapsalmanis/projects/kr1st4ps.github.io/Data/games.json", "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))