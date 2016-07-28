import requests, sys, urllib2
from bs4 import BeautifulSoup

def create():
    print("creating new  file")
    name=raw_input ("enter the name of file:")
    extension=raw_input ("enter extension of file:")
    try:
        name=name+"."+extension
        file=open(name,'a')

        file.close()
    except:
            print("error occured")
            sys.exit(0)

def urlfunc(make, series, yearfrom, yearto, minmileage, maxmileage, fueltype, page):
    urlun = 'http://www.autotrader.co.uk/search/used/cars/'+str(make)+'/'+str(series)+'/postcode/'
    urldeux = 'w37aq/radius/1500/year-from/'+str(yearfrom)+'/year-to/'+str(yearto)+'/minimum-mileage/'+str(minmileage)+'/maximum-mileage/'+str(maxmileage)+'/'
    urltrois = 'fuel-type/'+str(fueltype)+'/sort/default/searchcontext/default/page/'+str(page)+'/onesearchad/new%2Cnearlynew%2Cused'
    return urlun + urldeux + urltrois

#for number in range(10):
url = urlfunc('bmw', '1_series', '2012', '2016', 'from_5000_miles', 'up_to_60000_miles', 'diesel', 1)
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

t = soup.find('li', class_="paginationMini__count").find_all('strong')
currentpage = t[0].contents
totalpages = t[1].contents

results = soup.find_all('div', class_='search-result__r1')

#file=open('db.txt','a')
#file.close()
file = open("db.txt", "w")
file.write(totalpages[0]+'\n')
for result in results:
    price = result.find('div', class_='search-result__price')
    for prix in price.contents:
        prix = prix.encode('utf-8')
    print(prix)
    file.write(prix+"\n")

file.close()
