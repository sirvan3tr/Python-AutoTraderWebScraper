import requests
from bs4 import BeautifulSoup



def urlfunc(make, series, yearfrom, yearto, minmileage, maxmileage, fueltype):
    urlun = 'http://www.autotrader.co.uk/search/used/cars/'+str(make)+'/'+str(series)+'/postcode/'
    urldeux = 'w37aq/radius/1500/year-from/'+str(yearfrom)+'/year-to/'+str(yearto)+'/minimum-mileage/'+str(minmileage)+'/maximum-mileage/'+str(maxmileage)+'/'
    urltrois = 'fuel-type/'+str(fueltype)+'/sort/default/searchcontext/default/page/1/onesearchad/new%2Cnearlynew%2Cused'
    return urlun + urldeux + urltrois

url = urlfunc('bmw', '1_series', '2012', '2016', 'from_5000_miles', 'up_to_60000_miles', 'diesel')
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

t = soup.find('li', class_="paginationMini__count").find_all('strong')
currentpage = t[0].contents
totalpages = t[1].contents

results = soup.find_all('div', class_='search-result__r1')

for result in results:
    price = result.find('div', class_='search-result__price')
    print(price)
