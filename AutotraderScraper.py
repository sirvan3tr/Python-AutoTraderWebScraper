import requests, sys, urllib2, csv, re
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
