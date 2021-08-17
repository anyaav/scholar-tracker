from bs4 import BeautifulSoup
import requests
import json

#accepts ronin address
#returns JSON variable named "data"
def get_slp_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=smooth-love-potion&vs_currencies=usd%2Cphp&include_24hr_change=true&include_last_updated_at=true"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    data = json.loads(soup.find('p').text)
    return data
