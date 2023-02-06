import fetch
import json
#TODO fix The Devil In Me
#TODO add scheduling
#TODO add oculus store
#TODO add steam


with open("games.json", "r") as file:
    games = json.load(file)




ps_games = games["PS4"]

for game in ps_games:
    if game["best price"] is None:
        game["best price"] = fetch.ps4_best(game["name"])
    
    game["price"], game["price plus"] = fetch.ps4(game["name"])

    if game["price"] == game["best price"]:
        #TODO SEND MESSAGE
        print(1)
    elif game["price"] < game["best price"]:
        game["best price"] = game["price"]
        #TODO SEND MESSAGE




with open("games.json", "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))
