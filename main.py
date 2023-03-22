import utils.fetch as fetch
import json
import utils.email as email
import requests
from bs4 import BeautifulSoup
import utils.modify_json as modify_json
import configparser 
import os

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
    no_ps_deals, ps_message = fetch.prices("PS4", ps_games)

    #   Sends message about PS to email
    if no_ps_deals > 0:
        email.send(ps_message, "PS4")

    #   Fetches data for each Oculus game and compiles a message to send to the email
    no_oculus_deals, oculus_message = fetch.prices("Oculus", oculus_games)

    #   Sends message about PS to email
    if no_oculus_deals > 0:
        email.send(oculus_message, "Oculus")

    #   Writes data to json file
    with open(config["GLOBAL"]["RESULT_FILE"], "w") as file:
        json.dump(games, file, indent=2, separators=(',', ': '))


if __name__ == "__main__":
    main()