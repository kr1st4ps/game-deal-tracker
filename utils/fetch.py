import requests
from bs4 import BeautifulSoup
import json
import re
import configparser
import os

if os.name == "nt":
    os_slash = "\\"
else:
    os_slash = "/"

config = configparser.ConfigParser()
config.read("utils" + os_slash + "config.ini")

#   Other item tags in psprices website
    #name = item_json["name"]
    #ps_store_code = item_json["sku"]
    #is_lowest = item_json["is_lowest_price"]
    #psprices_url = item_json["url"]
    #cover_url = item_json["cover"]
    #discount = item_json["last_update"]["discount_percent"]
    #price_full = float(item_json["last_update"]["price_old"].replace(config["GLOBAL"]["PSPRICES_CURRENCY"], ""))
def ps4(game_name, action=None):
    url = config["GLOBAL"]["PSPRICES"] + config["USER DEFINED"]["PSPRICES_REGION"] + config["GLOBAL"]["PSPRICES_QUERY"] + game_name.replace(" ", "+")
    search = BeautifulSoup(requests.get(url).text, "html.parser")
    price = 0

    for item in search.find_all('div', {'class':'component--game-card col-span-6 sm:col-span-4 md:col-span-3 lg:col-span-3 xl:col-span-2'}):
        item_json = json.loads(item["data-props"])
        if item_json["name"].lower() == game_name.lower():
            if action == "best price" or action == "base price":
                url = config["GLOBAL"]["PSPRICES"] + item_json["url"]
                game_page = BeautifulSoup(requests.get(url).text, "html.parser")
                prices = game_page.find_all(text=re.compile("^\{}".format(config["USER DEFINED"]["PSPRICES_CURRENCY"])))
                if len(prices) == 3:
                    if action == "best price":
                        price = float(prices[1].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    elif action == "base price":
                        price = float(prices[0].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                else:
                    if action == "best price":
                        price = float(prices[2].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    elif action == "base price":
                        price = float(prices[1].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                    
                return price
            else:
                price = float(item_json["last_update"]["price"].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                price_plus = float(item_json["last_update"]["price_plus"].replace(config["USER DEFINED"]["PSPRICES_CURRENCY"], ""))
                
                return price, price_plus


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