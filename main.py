import fetch
import json
from send_mail import send
#TODO fix The Devil In Me
#TODO add scheduling
#TODO add oculus store
#TODO add steam

with open("games.json", "r") as file:
    games = json.load(file)
ps_games = games["PS4"]


message = "These games from your wishlist have good deals:\n"
for game in ps_games:
    if game["best price"] is None:
        game["best price"] = fetch.ps4_best(game["name"])
    
    game["price"], game["price plus"] = fetch.ps4(game["name"])

    if game["price"] == game["best price"]:
        message += "\n\t" + game["name"] + " is now " + game["price"] + "\n"
    elif game["price"] < game["best price"]:
        game["best price"] = game["price"]
        message += "\n\t" + "ALL TIME LOW - " + game["name"] + " is now just " + game["price"] + "\n"

send(message, "PS4")


with open("games.json", "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))
