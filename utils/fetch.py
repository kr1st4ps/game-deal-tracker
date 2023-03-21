import requests
from bs4 import BeautifulSoup
import json
import re
import configparser
import os

#   Checks which OS
if os.name == "nt":
    os_slash = "\\"
else:
    os_slash = "/"

#   Opens config file
config = configparser.ConfigParser()
config.read("utils" + os_slash + "config.ini")

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
    url = config["GLOBAL"]["PSPRICES"] + config["USER DEFINED"]["PSPRICES_REGION"] + config["GLOBAL"]["PSPRICES_QUERY"] + game_name.replace(" ", "+")

    #   Fetches html string from URL
    search = BeautifulSoup(requests.get(url).text, "html.parser")

    #   Looks for the correct game
    for item in search.find_all('div', {'class':'component--game-card col-span-6 sm:col-span-4 md:col-span-3 lg:col-span-3 xl:col-span-2'}):
        ps_data = json.loads(item["data-props"])
        if ps_data["name"].lower() == game_name.lower():

            #   Fetches current price and price with PS+ subscription 
            if current_price_trigger:
                price = float(ps_data["last_update"]["price"].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
            else:
                price = None
            
            #   Fetches lowest price the game has ever been
            if base_price_trigger or best_price_trigger:
                base_price, best_price = None

                #   Opens games page
                url = config["GLOBAL"]["PSPRICES"] + ps_data["url"]
                game_page = BeautifulSoup(requests.get(url).text, "html.parser")

                #   Finds all prices in html string
                prices = game_page.find_all(text=re.compile("^\{}".format(config["USER DEFINED"]["PSPRICES_CURRENCY"])))

                #   If the game is currently discounted, there will be more prices in html string
                if len(prices) == 3:
                    if best_price_trigger:
                        best_price = float(prices[1].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    if base_price_trigger:
                        best_price = float(prices[0].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                else:
                    if best_price_trigger:
                        best_price = float(prices[2].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    if base_price_trigger:
                        best_price = float(prices[1].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))

            
            return price, base_price, best_price


def oculus(game_name, action=None):
    url = config["GLOBAL"]["ODEALS"] + config["GLOBAL"]["ODEALS_QUERY"] + game_name.replace(" ", "+")
    search = BeautifulSoup(requests.get(url).text, "html.parser")
    for item in search.find_all('div', {'class':'col-xl-2 col-lg-3 col-md-4 col-6 mb-4'}):
        if item.find('span', {'class':'badge badge-pill badge-secondary'}).text == "Quest":
            if action == "best price" or action == "base price":
                url = item.find('a', {'class':'game-item'})["href"]
                game_page = BeautifulSoup(requests.get(url).text, "html.parser")
                if action == "base price":
                    prices = []
                    for item in game_page.find('div', {'class': 'col-lg-4 col-md-5 col-12'}).find_all(text=re.compile(r".* USD$")):
                        prices.append(float(item.replace(" USD", "")))
                    return max(prices)
                elif action == "best price":
                    return float(game_page.find_all('div', {'class': 'col-4 text-center'})[1].find('strong', {'class': 'text-success h4'}).text.strip().replace(" USD", ""))
            else:
                return float(item.find('strong', {'class':'text-danger'}).text.replace(" USD", ""))