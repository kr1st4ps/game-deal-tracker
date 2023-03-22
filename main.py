import utils.fetch as fetch
import json
import utils.email as email
import requests
from bs4 import BeautifulSoup
import utils.modify_json as modify_json
import configparser 
import os

if os.name == "nt":
    os_slash = "\\"
else:
    os_slash = "/"

config = configparser.ConfigParser()
config.read("utils" + os_slash + "config.ini")

#TODO check plus price in ps store
#TODO shorten the fetching code for each console
#TODO prettify code in email.py
#TODO add steam
#TODO add Amazon
#TODO fix The Devil In Me 0 price
#TODO fix dark pictures anthology and symbol issue
#TODO prettify email (fonts, size, pictures)

#   Loads json of games that need to be in the local games.json
game_list_api = BeautifulSoup(requests.get(config["USER DEFINED"]["GAME_LIST"]).text, "html.parser")
game_list = json.loads(str(game_list_api))
ps_game_list = game_list["PS4"]
oculus_game_list = game_list["Oculus"]

#   Opens local games.json file
with open(config["GLOBAL"]["RESULT_FILE"], "r") as file:
    games = json.load(file)
ps_games = games["PS4"]
oculus_games = games["Oculus"]
#steam_games = games["Steam"]

#   Updates local games.json
ps_games = modify_json.update("PS4", ps_game_list, ps_games)
oculus_games = modify_json.update("Oculus", oculus_game_list, oculus_games)

#   Fetches data for each PS game and compiles a message to send to the email
ps_message = "These games from your wishlist have good deals:\n"
no_ps_deals = 0
for game in ps_games:

    previous_price = game["price"]

    price, base_price, best_price = fetch.ps4(game["name"], True, True, True)

    game["price"] = price
    game["base price"] = base_price
    if game["best price"] is None:
        game["best price"] = best_price

    if previous_price < price:
        game["notification"] = False

    if game["notification"] == False and game["price"] <= game["best price"]:
        game["notification"] == True
        no_ps_deals += 1
        game["best price"] = game["price"]
        ps_message += "\n\t" + game["name"] + " is now " + str(game["best price"]) + "\n"

    

#   Fetches data for each Oculus game and compiles a message to send to the email
oculus_message = "These games from your wishlist have good deals:\n"
no_oculus_deals = 0
for game in oculus_games:
    previous_price = game["price"]

    price, base_price, best_price = fetch.oculus(game["name"], True, True, True)

    game["price"] = price
    game["base price"] = base_price
    if game["best price"] is None:
        game["best price"] = best_price

    if previous_price < price:
        game["notification"] = False

    if game["notification"] == False and game["price"] <= game["best price"]:
        game["notification"] == True
        no_oculus_deals += 1
        game["best price"] = game["price"]
        oculus_message += "\n\t" + game["name"] + " is now " + str(game["best price"]) + "\n"


#   Sends message about PS to email
if no_ps_deals > 0:
    email.send(ps_message, "PS4")

#   Sends message about PS to email
if no_oculus_deals > 0:
    email.send(oculus_message, "Oculus")

#   Writes data to json file
with open(config["GLOBAL"]["RESULT_FILE"], "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))
