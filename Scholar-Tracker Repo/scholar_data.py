from bs4 import BeautifulSoup
import requests
import json

#accepts ronin address
#returns JSON variable named "data"
def getdata(address):
    url = f"https://api.lunaciarover.com/stats/0x{address[6:]}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    data = json.loads(soup.find('p').text)
    return data