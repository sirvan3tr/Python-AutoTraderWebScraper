"""
Copyrights (c) S Almasi 2022.
This is an experimental code and should not be used for any commercial purposes
at all.
"""
from dataclasses import dataclass
from re import search
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_url = "https://www.autotrader.co.uk"
# Without headers information you will get a 403 error
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


@dataclass
class SearchQuery:
    make: str = "Porsche"
    model: str = "911"
    year_from: str = "2011"
    year_to: str = "2021"
    min_mileage: int = 500
    max_mileage: int = 50_000
    fuel_type: str = "Petrol"
    postcode: str = "SW72AZ"
    price_from: int = 500
    price_to: int = 45_000
    page: int = 1

    def get_url_params(self):
        """Construct the AutoTrader URL parameters from the queries"""
        # Go through the paramaters and join them up
        params_list = []
        for param, value in self.__dict__.items():
            # Replace underscores with a dash to match url query params
            param_key = param.replace("_", "-") if '_' in param else param
            # Join the key and value, e.g. year-to=2015
            param_query = f'{param_key}={value}'
            params_list.append(param_query)
        return '&'.join(params_list)

    def url(self):
        return f'{base_url}/car-search?{self.get_url_params()}'


@dataclass
class Vehicle:
    make: str
    model: str
    date: str
    price: str
    specs: list
    title: str
    subtitle: str



def parse_page(page_number: int, search_query: SearchQuery):
    """Scrapes an Autotrader page (as they are paginated)

    :param page_number: The page number to scrape.
    :param search_query: SearchQuery instance; has all the necessary
    parameters to filter the vehicles by.
    :returns: List of Vehicle instances [Vehicle]
    """
    # Get the request URL from SearchQuery
    # TODO: Change this :(
    search_query.page = page_number
    url = search_query.url()
    try:
        r = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Error requesting the URL.")
        raise SystemExit(e)
    # Parse the HTML
    soup = BeautifulSoup(r.content, "html.parser")
    # Get the vehicle cards/items
    # TODO: Raise an error if the dom and classes are changed
    vehicle_cards = soup.find_all('li', class_='search-page__result')

    # Get the pagination numbers, if we have gone beyond the max pagination
    # then return an empty list.
    page_nums = list(map(lambda htmltag: int(htmltag.text),
        soup.find("li", class_="paginationMini__count").find_all("strong")))
    if page_number > max(page_nums):
        return []

    # List of vehicles to return
    vehicles = []  # [Vehicle]
    # For each of the vehicle html cards, scrape the data content
    for vehicle_card in vehicle_cards:
        # Price
        # TODO: Raise an error if the dom and classes are changed
        price = vehicle_card\
            .find("div", class_="product-card-pricing__price")\
            .span.text
        # Specs container; should be a ul
        # TODO: Raise an error if the dom and classes are changed
        specs_html = vehicle_card\
            .find("ul", class_="listing-key-specs")
        title = vehicle_card\
            .find("h3", class_="product-card-details__title")\
            .text\
            .strip()\
            .replace("\n", "")
        subtitle = vehicle_card\
            .find("p", class_="product-card-details__subtitle")\
            .text\
            .strip()\
            .replace("\n", "")
        # Actual specs, each is inside an li
        specs = list(map(lambda htmltag: htmltag.text,
                         specs_html.find_all("li", recursive=False)))
        # Construct the vehicle dataclass
        vehicle = Vehicle(make=search_query.make,
                          model=search_query.model,
                          date=datetime.now(),
                          price=price,
                          specs=specs,
                          title=title,
                          subtitle=subtitle
                        )
        vehicles.append(vehicle)
        # print(vehicle)
    return vehicles

def scrape(search_query):
    vehicle_count = 999
    page_number = 1
    vehicles = [] 

    while vehicle_count > 0:
        parsed_vehicles = parse_page(page_number=page_number,
                                     search_query=search_query)
        vehicle_count = len(parsed_vehicles)
        vehicles += parsed_vehicles
        time.sleep(0.5)
        page_number += 1
    
    return vehicles


if __name__ == '__main__':
    # Define your queries here
    search_query = SearchQuery()
    print(search_query.url())
    # print(parse_page(1, search_query))

    # import threading

    # for i in range(1, 2):
    #     t = threading.Thread(target=parse_page, args=(i, search_query))
    #     t.start()
    vehicles = scrape(search_query)
