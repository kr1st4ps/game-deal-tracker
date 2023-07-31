import utils.fetch as fetch
import json
import utils.email as email
import requests
from bs4 import BeautifulSoup
import utils.modify_json as modify_json
import configparser 
import os
import schedule
import time


def main():

    #   Checks OS
    if os.name == "nt":
        os_slash = "\\"
    else:
        os_slash = "/"

    #   Opens config file
    config = configparser.ConfigParser()
    config.read("utils" + os_slash + "config.ini")

    #   Loads json of games that need to be in the local games.json
    while True:    
        try:
            game_list_api = BeautifulSoup(requests.get(config["USER DEFINED"]["GAME_LIST"]).text, "html.parser")
            break
        except:
            time.sleep(60)
            continue
    game_list = json.loads(str(game_list_api))
    ps4_game_list = game_list["PS4"]
    ps5_game_list = game_list["PS5"]
    oculus_game_list = game_list["Oculus"]

    #   Opens local games.json file
    with open(config["GLOBAL"]["RESULT_FILE"], "r") as file:
        games = json.load(file)
    ps4_games = games["PS4"]
    ps5_games = games["PS5"]
    oculus_games = games["Oculus"]

    #   Updates local games.json
    ps4_games = modify_json.update("PS4", ps4_game_list, ps4_games)
    ps5_games = modify_json.update("PS5", ps5_game_list, ps5_games)
    oculus_games = modify_json.update("Oculus", oculus_game_list, oculus_games)

    #   Fetches data for each PS game and compiles a message to send to the email
    no_ps4_deals, ps4_message, ps4_games = fetch.prices("PS4", ps4_games)
    no_ps5_deals, ps5_message, ps5_games = fetch.prices("PS5", ps5_games)

    #   Sends message about PS to email
    if no_ps4_deals > 0:
        email.send(ps4_message, "PS4")
    if no_ps5_deals > 0:
        email.send(ps5_message, "PS5")

    """#   Fetches data for each Oculus game and compiles a message to send to the email
    no_oculus_deals, oculus_message, oculus_games = fetch.prices("Oculus", oculus_games)

    #   Sends message about PS to email
    if no_oculus_deals > 0:
        email.send(oculus_message, "Oculus")"""

    #   Writes data to json file
    with open(config["GLOBAL"]["RESULT_FILE"], "w") as file:
        json.dump(games, file, indent=2, separators=(',', ': '))


schedule.every().hour.at(":05").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)