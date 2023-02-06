from bs4 import BeautifulSoup
import requests
import re


url = "https://psprices.com" + "/region-gb/game/5623312/marvel-s-midnight-suns-digital-edition"
search = BeautifulSoup(requests.get(url).text, "html.parser")
item = float(search.find_all(text=re.compile("^\£"))[1].replace("£", ""))
print(item)