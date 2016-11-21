from bs4 import BeautifulSoup
import requests

# url = raw_input("www.pro-football-reference.com/players/A")

r  = requests.get("http://www.pro-football-reference.com/players/A")

data = r.text

soup = BeautifulSoup(data, "lxml")

for link in soup.find_all('table'):
    print(link)

# http://www.pro-football-reference.com/players/A/