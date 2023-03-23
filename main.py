import requests
from bs4 import BeautifulSoup
import datetime
from selenium import webdriver
import time
headers = {"User-Agent" : 'Mozilla/5.0'}
driver = webdriver.Chrome()

cityRus={"Krasnoyarsk":37, "Moscow":2, "Khabarovsk":80, "Vladivostok":19, "Blagoveshensk":15, "Irkutsk":28}
cityOutside={"Thailand":87, "Turkish":92, "Egypt":29, "UAE":68, "Venezuela":21, "Cuba":48, "Vietnam":22}

def link_parser():
    for i in range(len(cityRus)):
        for j in range(len(cityOutside)):
            URL = f"https://tinkoff.travelata.ru/search#?fromCity={list(cityRus.values())[i]}&toCountry={list(cityOutside.values())[j]}" \
                  f"&dateFrom={format(datetime.date.today()+datetime.timedelta(weeks=2),'%d.%m.%Y')}" \
                  f"&dateTo={format(datetime.date.today()+datetime.timedelta(weeks=2),'%d.%m.%Y')}&nightFrom=8&nightTo=15&adults=2&hotelClass=all" \
                  f"&meal=all&priceFrom=0&priceTo=200000&sid=9knkkpjhqq&sort=priceUp"

            driver.minimize_window()
            driver.get(URL)
            time.sleep(40)
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, "html.parser")
            links = soup.find_all("span", {"class": "serpHotelCard__btn-price"})
            for link in links:
                print(str(link.get_text()))

            # page = requests.get(URL, headers=headers)
            # soup = BeautifulSoup(page.text, "html.parser")
            # for linnk in soup.find_all('span', {"class": "serpHotelCard__btn-price"}):
            #     links=linnk.text
            #     if links.text < 180000:
            #         print(links.text)
            #     else:
            #         continue


def main():
    link_parser()
    driver.quit()

if __name__ == '__main__':
    main()


