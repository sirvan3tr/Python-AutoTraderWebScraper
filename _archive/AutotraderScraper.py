import requests
import sys
import csv
import re
from bs4 import BeautifulSoup
from dataclasses import dataclass


def create():
    print("creating new file")
    name = input("enter the name of file:")
    extension = input("enter extension of file:")
    try:
        name = name+"."+extension
        file = open(name, 'a')
        file.close()
    except FileExistsError:
        print("error occured")
        sys.exit(0)


"""
https://www.autotrader.co.uk/
car-search?postcode=w37aq
&price-from=500
&price-to=50000
&make=Porsche
&include-delivery-option=on
&advertising-location=at_cars
&page=1
&year-from
&year-from=2015
&year-to=2018
&maximum-mileage=15000
&fuel-type=Diesel|Petrol
"""


class URLParams:
    base_url: "https://www.autotrader.co.uk"


@dataclass
class SearchQuery:
    make: None
    series: None
    year_from: None
    year_to: None
    min_mileage: None
    max_mileage: None
    fuel_type: None
    post_code: None
    price_from: 500
    price_to: 80000
    page: 1

    def url(self):
        """Construc the AutoTrader URL from the queries"""
        {
            "price-from": price_from
        }
        pass

# Get the total number of pages
url = urlfunc('bmw', '1_series', '2012', '2016', 'from_5000_miles', 'up_to_60000_miles', 'diesel', 1)
r = requests.get(url)

soup = BeautifulSoup(r.content, "html.parser")

t = soup.find('li', class_="paginationMini__count").find_all('strong')
currentpage = t[0].contents
totalpages = t[1].contents

#file=open('db.txt','a')
#file.close()
file = open("db.csv", "w")
writer = csv.writer(file)

for pageNum in range(int(totalpages[0])):
    attrlist = []
    url = urlfunc('bmw', '1_series', '2012', '2016', 'from_5000_miles', 'up_to_60000_miles', 'diesel', pageNum)
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    t = soup.find('li', class_="paginationMini__count").find_all('strong')
    currentpage = t[0].contents
    totalpages = t[1].contents

    results = soup.find_all('div', class_='search-result__r1')

    for result in results:
        title = result.find('a', {'class' : 'gui-test-search-result-link'})
        title = title.contents[0].encode('utf-8')
        title = re.sub('[^A-Za-z0-9]+', '', title)

        price = result.find('div', class_='search-result__price')
        for prix in price.contents:
            prix = prix.encode('utf-8')
        price = re.sub('[^A-Za-z0-9]+', '', prix)
        attrlist.append(title)
        attrlist.append(price)

        content = result.find('div', class_='search-result__content')
        #attributes = result.find('ul', class_='search-result__attributes').find('li')
        attributes = result.find("ul", { "class" : "search-result__attributes" })
        attrchildren = attributes.find_all('li', recursive=False)

        for attr in attrchildren:
            at = re.sub('[^A-Za-z0-9 ]+', '', attr.contents[0])
            if at:
                attrlist.append(at)

        print(attrlist)
        writer.writerow(attrlist)


        del attrlist [:]

    print(' ')

file.close()
