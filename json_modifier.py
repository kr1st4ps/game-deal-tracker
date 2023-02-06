import json

with open("games.json", "r") as file:
    games = json.load(file)

ps_games = games["PS4"]

for game in ps_games:
    game["best price"] = None

with open("games.json", "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))