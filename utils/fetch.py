import requests
from bs4 import BeautifulSoup
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

        if console == "PS4" or console == "PS5":
            try:
                price, discount, full_price = ps(game["name"], console)
            except Exception as e:
                error_txt = "Encountered exception -{}- for {} of {}".format(e, game["name"], console)
                logging.error(error_txt)
                error_msg += error_txt + "\n\n"
        """elif console == "Oculus":
            try:
                price, base_price, best_price = oculus(game["name"], True, True, True)
            except Exception as e:
                error_txt = "Encountered exception -{}- for {} of {}".format(e, game["name"], console)
                logging.error(error_txt)
                error_msg += error_txt + "\n\n"
                continue"""

        #   Updates json
        game["price"] = price
        game["base price"] = base_price

        if game["best price"] is None:
            game["best price"] = price

        if price < previous_price:
            game["notification"] = True
            no_deals += 1
            game["best price"] = game["price"]
            if discount == None:
                message += "\n\t" + game["name"] + " base price has been lowered to " + config["USER DEFINED"]["PSSTORE_CURRENCY"] + str(full_price) + "!\n"
            else:
                message += "\n\t" + game["name"] + " is now discounted by " + discount + " and is " + config["USER DEFINED"]["PSSTORE_CURRENCY"] + str(price) + "!\n"

        if len(error_msg) > 0:
            email.send(error_msg, "error")

    return no_deals, message, games


def ps(game_name, console):
    #   Creates a URL with passed game name
    url = config["GLOBAL"]["PSSTORE"] + config["USER DEFINED"]["PSSTORE_REGION"] + "/search/" + game_name

    #   Fetches html string from URL
    search = BeautifulSoup(conn(url, game_name), "html.parser")

    #   Looks for the correct game
    for item in search.find_all('li', {'class':''}):

        #   Checks name, console, and type
        try:
            name = item.find('span', {"class":'psw-t-body psw-c-t-1 psw-t-truncate-2 psw-m-b-2'})
            consoles = [tag.text for tag in item.find_all('span', {"class":'psw-platform-tag psw-p-x-2 psw-l-line-left psw-t-tag psw-on-graphic'})]
            try:
                product_type = item.find('span', {"class":'psw-product-tile__product-type psw-t-bold psw-t-size-1 psw-t-truncate-1 psw-c-t-2 psw-t-uppercase psw-m-b-1'})
            except:
                product_type = None

            if name.text != game_name or console not in consoles or product_type is not None:
                continue

        except:
            continue
      
        #   Finds current price
        price = item.find('span', {"class":'psw-m-r-3'})

        # Finds discount and full price (if the game is discounted)
        try:
            discount = item.find('span', {"class":'psw-body-2 psw-badge__text psw-badge--none psw-text-bold psw-p-y-0 psw-p-2 psw-r-1 psw-l-anchor'})
            full_price = item.find('s', {"class":'psw-c-t-2'})
        except:
            discount = None
            full_price = price

    return price, discount, full_price


def oculus(game_name, current_price_trigger=None, base_price_trigger=None, best_price_trigger=None):

    #   Creates a URL with passed game name
    url = config["GLOBAL"]["ODEALS"] + config["GLOBAL"]["ODEALS_QUERY"] + game_name.replace(" ", "+")

    #   Fetches html string from URL
    search = BeautifulSoup(conn(url, game_name), "html.parser")

    #   Looks for the correct game
    for item in search.find_all('div', {'class':'col-xl-2 col-lg-3 col-md-4 col-6 mb-4'}):
        if item.find('span', {'class':'badge badge-pill badge-secondary'}).text == "Quest":

            #   Fetches current price
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