from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import json
headers = {"User-Agent" : 'Mozilla/5.0'}

url="https://tinkoff.travelata.ru/hotel/16445#?fromCity=37" \
    "&dateFrom=30.03.2023&dateTo=30.03.2023&nightFrom=8&nightTo=15&adults=2&priceFrom=6000&priceTo=50000000&meal=all&activeTab=tours&sid=mst1hzeni0&hsid=ult0ns3fo8"
def get_link():
    # get information from site_link for create AE template
    driver = webdriver.Chrome()
    driver.minimize_window()
    driver.get(url)
    time.sleep(0.2)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    start_index = url.find("&dateFrom=") + len("&dateFrom=")
    four_characters = url[start_index:start_index + 5]
    city_direct=soup.find('div', {"class": "resortName"}).text.strip().split(', ')[1]
    country_nameExp= soup.find('div', {"class": "resortName"}).text.strip().split(',')[0]
    link = (soup.find('span', {"class": "hotelTour__nights-in-tour"}).text.strip()).replace(",", "")
    price_text = soup.find('div', {"class": "hotelTour__price-block__btn"}).text.strip().split(' руб.')[0]
    hotel = (four_characters, city_direct,country_nameExp, link, price_text)
    print(hotel)
    driver.quit()

    # extract data from website
    # create a dictionary to store the data
    data = {
        "four_characters": four_characters,
        "city_direct": city_direct,
        "country_nameExp": country_nameExp,
        "link": link,
        "price_text": price_text
    }

    # write the data to a JSON file
    with open("data.json", "w") as outfile:
        json.dump(data, outfile)

def main():
    get_link()

if __name__=='__main__':
    main()

