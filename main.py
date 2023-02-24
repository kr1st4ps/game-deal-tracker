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
    if game["best price"] is None:
        game["best price"] = fetch.ps4(game["name"], "best price")
    
    game["base price"] = fetch.ps4(game["name"], "base price")
    if game["price"] == None:
        game["price"] = game["base price"]
    old_price = game["price"]
    game["price"], game["price plus"] = fetch.ps4(game["name"])
    if old_price < game["price"]:
        game["notification"] = False

    if game["price"] == game["best price"] and game["price"] != game["base price"] and game["notification"] == False:
        game["notification"] == True
        ps_message += "\n\t" + game["name"] + " is now " + str(game["price"]) + "\n"
        no_ps_deals += 1
    elif game["price"] < game["best price"] and game["notification"] == False:
        game["best price"] = game["price"]
        game["notification"] == True
        ps_message += "\n\t" + "ALL TIME LOW - " + game["name"] + " is now just " + str(game["price"]) + "\n"
        no_ps_deals += 1

#   Fetches data for each Oculus game and compiles a message to send to the email
oculus_message = "These games from your wishlist have good deals:\n"
no_oculus_deals = 0
for game in oculus_games:
    if game["best price"] is None:
        game["best price"] = fetch.oculus(game["name"], "best price")
    
    game["base price"] = fetch.oculus(game["name"], "base price")
    if game["price"] == None:
        game["price"] = game["base price"]
    old_price = game["price"]
    game["price"] = fetch.oculus(game["name"])
    if old_price < game["price"]:
        game["notification"] = False

    if game["price"] == game["best price"] and game["price"] != game["base price"] and game["notification"] == False:
        game["notification"] == True
        oculus_message += "\n\t" + game["name"] + " is now " + str(game["price"]) + "\n"
        no_oculus_deals += 1
    elif game["price"] < game["best price"] and game["notification"] == False:
        game["best price"] = game["price"]
        game["notification"] == True
        oculus_message += "\n\t" + "ALL TIME LOW - " + game["name"] + " is now just " + str(game["price"]) + "\n"
        no_oculus_deals += 1

#   Sends message about PS to email
if no_ps_deals > 0:
    email.send(ps_message, "PS4")

#   Sends message about PS to email
if no_oculus_deals > 0:
    email.send(oculus_message, "Oculus")

#   Writes data to json file
with open(config["GLOBAL"]["RESULT_FILE"], "w") as file:
    json.dump(games, file, indent=2, separators=(',', ': '))
