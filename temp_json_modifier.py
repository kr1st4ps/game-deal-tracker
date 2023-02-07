import json
import sys

with open("games.json", "r") as file:
    games = json.load(file)

console_games = games["PS4"]
for item in console_games:
    item["notification"] = False

with open("games.json", "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))