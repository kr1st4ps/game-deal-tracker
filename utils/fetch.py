import requests
from bs4 import BeautifulSoup
import json
import re
import configparser
import os
import logging
import utils.email as email
import time

#   Checks which OS
if os.name == "nt":
    os_slash = "\\"
else:
    os_slash = "/"

#   Opens config file
config = configparser.ConfigParser()
config.read("utils" + os_slash + "config.ini")

#   Sets up logging
logging.basicConfig(filename="logs.log",
                    filemode='a',
                    format='%(levelname)s:%(asctime)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)


def prices(console, games):
    #   Fetches data for each game and compiles a message to send to the email
    message = "These games from your wishlist have good deals:\n"
    error_msg = ""
    no_deals = 0
    for game in games:

        logging.info("Fetching price for {} from {} store".format(game["name"], console))

        previous_price = game["price"]

        if console == "PS4":
            try:
                price, base_price, best_price = ps4(game["name"], True, True, True)
            except Exception as e:
                error_txt = "Encountered exception -{}- for {} of {}".format(e, game["name"], console)
                logging.error(error_txt)
                error_msg += error_txt + "\n\n"
                continue
        elif console == "Oculus":
            try:
                price, base_price, best_price = oculus(game["name"], True, True, True)
            except Exception as e:
                error_txt = "Encountered exception -{}- for {} of {}".format(e, game["name"], console)
                logging.error(error_txt)
                error_msg += error_txt + "\n\n"
                continue

        game["price"] = price
        game["base price"] = base_price
        if game["best price"] is None:
            game["best price"] = best_price
        if previous_price is not None and previous_price < price:
            game["notification"] = False

        if (game["notification"] == False and game["price"] <= game["best price"]) or (game["notification"] == True and game["price"] < game["best price"]):
            game["notification"] = True
            no_deals += 1
            game["best price"] = game["price"]
            message += "\n\t" + game["name"] + " is now " + str(game["best price"]) + "\n"

        if len(error_msg) > 0:
            email.send(error_msg, "error")

    return no_deals, message, games

#   Other item tags in psprices website
    #name = ps_data["name"]
    #ps_store_code = ps_data["sku"]
    #is_lowest = ps_data["is_lowest_price"]
    #psprices_url = ps_data["url"]
    #cover_url = ps_data["cover"]
    #discount = ps_data["last_update"]["discount_percent"]
    #price_full = float(ps_data["last_update"]["price_old"].replace(config["GLOBAL"]["PSPRICES_CURRENCY"], ""))
def ps4(game_name, current_price_trigger=None, base_price_trigger=None, best_price_trigger=None):
    #   Creates a URL with passed game name
    url = config["GLOBAL"]["PSPRICES"] + config["USER DEFINED"]["PSPRICES_REGION"] + config["GLOBAL"]["PSPRICES_QUERY"] + game_name.replace(" ", "+") + "&platform=" + config["USER DEFINED"]["PSPRICES_PLATFORM"]

    #   Fetches html string from URL
    search = BeautifulSoup(conn(url, game_name), "html.parser")

    #   Looks for the correct game
    for item in search.find_all('div', {'class':'component--game-card col-span-6 sm:col-span-4 md:col-span-3 lg:col-span-3 xl:col-span-2'}):
        if json.loads(item["data-props"])["top_category"] == "game":
            ps_data = json.loads(item["data-props"])
        else:
            continue
        
        if ps_data["name"].lower() == game_name.lower():

            #   Fetches current price and price with PS+ subscription 
            if current_price_trigger:
                price = float(ps_data["last_update"]["price"].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
            else:
                price = None
            
            #   Fetches lowest price the game has ever been
            if base_price_trigger or best_price_trigger:
                base_price = best_price = None

                #   Opens games page
                url = config["GLOBAL"]["PSPRICES"] + ps_data["url"]
                game_page = BeautifulSoup(conn(url, game_name), "html.parser")

                #   Finds all prices in html string
                prices = game_page.find_all(text=re.compile("^\{}".format(config["USER DEFINED"]["PSPRICES_CURRENCY"])))

                #   If the game is currently discounted, there will be more prices in html string
                if len(prices) == 3:
                    if best_price_trigger:
                        best_price = float(prices[1].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    if base_price_trigger:
                        base_price = float(prices[0].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                else:
                    if best_price_trigger:
                        best_price = float(prices[2].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    if base_price_trigger:
                        base_price = float(prices[1].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))

            return price, base_price, best_price


def oculus(game_name, current_price_trigger=None, base_price_trigger=None, best_price_trigger=None):

    #   Creates a URL with passed game name
    url = config["GLOBAL"]["ODEALS"] + config["GLOBAL"]["ODEALS_QUERY"] + game_name.replace(" ", "+")

    #   Fetches html string from URL
    search = BeautifulSoup(conn(url, game_name), "html.parser")

    #   Looks for the correct game
    for item in search.find_all('div', {'class':'col-xl-2 col-lg-3 col-md-4 col-6 mb-4'}):
        if item.find('span', {'class':'badge badge-pill badge-secondary'}).text == "Quest":

            #   Fetches current price and price with PS+ subscription 
            if current_price_trigger:
                price = float(item.find('strong', {'class':'text-danger'}).text.replace(" USD", ""))
            else:
                price = None

            #   Fetches lowest price the game has ever been
            if base_price_trigger or best_price_trigger:
                base_price = best_price = None

                #   Opens games page
                url = item.find('a', {'class':'game-item'})["href"]
                game_page = BeautifulSoup(conn(url, game_name), "html.parser")

                if base_price_trigger:
                    prices = []
                    for item in game_page.find('div', {'class': 'col-lg-4 col-md-5 col-12'}).find_all(text=re.compile(r".* USD$")):
                        prices.append(float(item.replace(" USD", "")))
                    base_price = max(prices)

                if best_price_trigger:
                    best_price = float(game_page.find_all('div', {'class': 'col-4 text-center'})[1].find('strong', {'class': 'text-success h4'}).text.strip().replace(" USD", ""))


            return price, base_price, best_price

    
def conn(url, name):
    while True:    
        try:
            html = requests.get(url)
            break
        except:
            time.sleep(60)
            logging.error("Trying to fetch again - {}".format(name))
            continue

    return html.text