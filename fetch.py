import requests
from bs4 import BeautifulSoup
import json
import re

def game_list():
    search = json.load(BeautifulSoup(requests.get("https://raw.githubusercontent.com/kr1st4ps/game-deal-tracker/main/mailcode.txt?token=GHSAT0AAAAAAB6NJ2ZORLCZTYMQL4OC4SECY7BKF6Q").text, "html.parser"))

def ps4(game_name):
    url = "https://psprices.com/region-gb/search/?q=" + game_name.replace(" ", "+")
    search = BeautifulSoup(requests.get(url).text, "html.parser")

    for item in search.find_all('div', {'class':'component--game-card col-span-6 sm:col-span-4 md:col-span-3 lg:col-span-3 xl:col-span-2'}):
        item_json = json.loads(item["data-props"])
        if item_json["name"].lower() == game_name.lower():
            #name = item_json["name"]
            #ps_store_code = item_json["sku"]
            #is_lowest = item_json["is_lowest_price"]
            #psprices_url = item_json["url"]
            #cover_url = item_json["cover"]
            #discount = item_json["last_update"]["discount_percent"]
            price_full = float(item_json["last_update"]["price_old"].replace("£", ""))
            price = float(item_json["last_update"]["price"].replace("£", ""))
            price_plus = float(item_json["last_update"]["price_plus"].replace("£", ""))
            
            return price, price_plus

    
    return None, None

def ps4_best(game_name):
    url = "https://psprices.com/region-gb/search/?q=" + game_name.replace(" ", "+")
    search = BeautifulSoup(requests.get(url).text, "html.parser")

    for item in search.find_all('div', {'class':'component--game-card col-span-6 sm:col-span-4 md:col-span-3 lg:col-span-3 xl:col-span-2'}):
        item_json = json.loads(item["data-props"])
        if item_json["name"].lower() == game_name.lower():
            url = "https://psprices.com" + item_json["url"]
            game_page = BeautifulSoup(requests.get(url).text, "html.parser")
            prices = game_page.find_all(text=re.compile("^\£"))
            if len(prices) == 3:
                best_price = float(prices[1].replace("£", ""))
            else:
                best_price = float(prices[2].replace("£", ""))
                
            return best_price
    
    return None

def ps4_base(game_name):
    url = "https://psprices.com/region-gb/search/?q=" + game_name.replace(" ", "+")
    search = BeautifulSoup(requests.get(url).text, "html.parser")

    for item in search.find_all('div', {'class':'component--game-card col-span-6 sm:col-span-4 md:col-span-3 lg:col-span-3 xl:col-span-2'}):
        item_json = json.loads(item["data-props"])
        if item_json["name"].lower() == game_name.lower():
            url = "https://psprices.com" + item_json["url"]
            game_page = BeautifulSoup(requests.get(url).text, "html.parser")
            prices = game_page.find_all(text=re.compile("^\£"))
            if len(prices) == 3:
                best_price = float(prices[0].replace("£", ""))
            else:
                best_price = float(prices[1].replace("£", ""))
                
            return best_price
    
    return None