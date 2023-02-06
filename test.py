import requests
from bs4 import BeautifulSoup

search = BeautifulSoup(requests.get("https://raw.githubusercontent.com/kr1st4ps/game-deal-tracker/main/mailcode.txt?token=GHSAT0AAAAAAB6NJ2ZORLCZTYMQL4OC4SECY7BKF6Q").text, "html.parser")

print(search)