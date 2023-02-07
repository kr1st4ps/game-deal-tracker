import fetch
import json
import email
import requests
from bs4 import BeautifulSoup
import modify_json
import configparser #TODO Implement

#TODO fix The Devil In Me
#TODO prettify email (fonts, size, pictures)
#TODO add oculus store
#TODO add steam

#   Loads json of games that need to be in the local games.json
game_list_api = BeautifulSoup(requests.get("https://kr1st4ps.github.io/Data/games_list.json").text, "html.parser")
game_list = json.load(game_list_api)
ps_game_list = game_list["PS4"]

#   Opens local games.json file
with open("games.json", "r") as file:
    games = json.load(file)
ps_games = games["PS4"]
steam_games = games["Steam"]
oculus_games = games["Oculus"]

#TODO for steam and oculus as well
#   Collects games from the local json
list_of_current_games = []
for game_from_json in ps_games:
    list_of_current_games.append(game_from_json["name"])

#   Adds new games (if any) to local json
for game_from_list in ps_game_list:
    if game_from_list in list_of_current_games:
        list_of_current_games.remove(game_from_list)
    else:
        ps_games = modify_json.add(game_from_list, ps_games, "PS4")

#   Removes (if needed) games from local json
for game in list_of_current_games:
    ps_games = modify_json.remove(game_from_list, ps_games)

#   Fetches data for each game and compiles a message to send to the email
message = "These games from your wishlist have good deals:\n"
for game in ps_games:
    if game["best price"] is None:
        game["best price"] = fetch.ps4_best(game["name"])
    
    game["base price"] = fetch.ps4_base(game["name"])
    old_price = game["price"]
    game["price"], game["price plus"] = fetch.ps4(game["name"])
    if old_price < game["price"]:
        game["notification"] = False

    if game["price"] == game["best price"] and game["price"] != game["base price"] and game["notification"] == False:
        game["notification"] == True
        message += "\n\t" + game["name"] + " is now " + str(game["price"]) + "\n"
    elif game["price"] < game["best price"] and game["notification"] == False:
        game["best price"] = game["price"]
        game["notification"] == True
        message += "\n\t" + "ALL TIME LOW - " + game["name"] + " is now just " + str(game["price"]) + "\n"

#   Sends message to email
email.send(message, "PS4")

#   Writes data to json file
with open("games.json", "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))
